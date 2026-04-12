# ==============================================================================
# RSS v3 Kernel Runtime
# Module: Persistence Layer (SQLite + WAL)
# Copyright (c) 2025-2026 Christian Robert Rose
#
# DUAL-LICENSE NOTICE:
# This software is released under a Dual-License model.
#
# 1. GNU Affero General Public License v3.0 (AGPLv3)
#    You may use, distribute, and modify this code under the terms of the AGPLv3.
#    If you modify or distribute this software, or integrate it into your own
#    project, your entire project must also be open-sourced under the AGPLv3.
#    Network use is distribution: if you run a modified version of this software
#    on a server and allow users to interact with it remotely, you must make the
#    complete corresponding source code available to those users under AGPLv3.
#
# 2. Commercial / Contractor License Exception
#    If you wish to use this software in a closed-source, proprietary, or
#    commercial environment (including SaaS or network-accessible deployments)
#    without adhering to the AGPLv3 open-source requirements, you must obtain
#    a separate Contractor License from the author.
#
# Contact: rose.systems@outlook.com  (Subject: "Contact Us — RSS Commercial License")
# ==============================================================================
"""
RSS v3 — Persistence Layer (Production Hardened)
SQLite backend. TRACE, hubs, terms, and consent survive restarts.
Thread-safe + WAL-enabled version.

§4.4.3: hub_entries includes original_hub column.
§4.4.5: hub_entries includes purged column.
§6.7.3: system_state tracks SCHEMA_VERSION.
§6.8.2: _migrate_hub_entries() adds columns idempotently.
§6.8.3: save_trace_event() is used by migrations to emit SCHEMA_MIGRATED.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, UTC
from typing import List, Optional

from audit_log import TraceEvent

# §6.7.3 — Current persistence schema version.
# Bump this whenever a migration lands in _migrate_hub_entries() or elsewhere.
# On bootstrap, a mismatch between stored version and this constant triggers
# migration + a SCHEMA_MIGRATED TRACE event (emitted by Runtime, not Persistence,
# because Persistence is constructed before Runtime has a TRACE log).
CURRENT_SCHEMA_VERSION = 1


class Persistence:
    def __init__(self, db_path: str):
        self.db_path = db_path

        # allow multi-thread access
        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False,
            isolation_level=None,  # manual transaction control
        )

        self._lock = threading.RLock()

        # Track whether a migration occurred during this init — Runtime reads this
        # after construction to emit the SCHEMA_MIGRATED event. Migrations cannot
        # emit TRACE events themselves because TRACE is wired up in Runtime, not
        # Persistence, and Persistence is constructed first.
        self.migration_occurred: bool = False
        self.migration_details: list = []

        self._configure_db()
        self._create_tables()
        self._migrate_hub_entries()

    # -----------------------------------------------------
    # DB Configuration (Production Safety)
    # -----------------------------------------------------
    def _configure_db(self) -> None:
        with self.conn:
            self.conn.execute("PRAGMA journal_mode=WAL;")
            self.conn.execute("PRAGMA synchronous=NORMAL;")
            self.conn.execute("PRAGMA foreign_keys=ON;")

    # -----------------------------------------------------
    # Schema
    # -----------------------------------------------------
    def _create_tables(self) -> None:
        stmts = [
            """CREATE TABLE IF NOT EXISTS trace_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_code TEXT,
                authority TEXT,
                artifact_id TEXT,
                content_hash TEXT,
                byte_length INTEGER,
                parent_hash TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS hub_entries (
                id TEXT PRIMARY KEY,
                hub TEXT,
                content TEXT,
                redline INTEGER,
                timestamp TEXT,
                version INTEGER DEFAULT 1,
                original_hub TEXT DEFAULT '',
                purged INTEGER DEFAULT 0,
                provenance TEXT DEFAULT '[]'
            )""",
            """CREATE TABLE IF NOT EXISTS sealed_terms (
                term_id TEXT PRIMARY KEY,
                label TEXT,
                definition TEXT,
                constraints TEXT,
                version TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS consents (
                key TEXT PRIMARY KEY,
                action_class TEXT,
                container_id TEXT,
                requester TEXT,
                status TEXT,
                granted_at TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS synonyms (
                phrase TEXT PRIMARY KEY,
                term_id TEXT,
                confidence TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS disallowed_terms (
                phrase TEXT PRIMARY KEY,
                reason TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS system_state (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )""",
            # §5.2.1 — Container persistence
            """CREATE TABLE IF NOT EXISTS containers (
                container_id TEXT PRIMARY KEY,
                profile TEXT,
                state TEXT,
                created_at TEXT,
                lifecycle_log TEXT DEFAULT '[]'
            )""",
            """CREATE TABLE IF NOT EXISTS container_hub_entries (
                container_id TEXT,
                id TEXT,
                hub TEXT,
                content TEXT,
                redline INTEGER,
                timestamp TEXT,
                version INTEGER DEFAULT 1,
                original_hub TEXT DEFAULT '',
                purged INTEGER DEFAULT 0,
                provenance TEXT DEFAULT '[]',
                PRIMARY KEY (container_id, id)
            )""",
            "CREATE INDEX IF NOT EXISTS idx_trace_code ON trace_events(event_code)",
            "CREATE INDEX IF NOT EXISTS idx_trace_artifact ON trace_events(artifact_id)",
            "CREATE INDEX IF NOT EXISTS idx_hub_hub ON hub_entries(hub)",
            "CREATE INDEX IF NOT EXISTS idx_container_hub ON container_hub_entries(container_id, hub)",
        ]

        with self._lock, self.conn:
            for stmt in stmts:
                self.conn.execute(stmt)

    def _migrate_hub_entries(self) -> None:
        """Add original_hub and purged columns if upgrading from older schema.
        §6.8.2 — Idempotent column-addition migration.
        §6.8.3 — Records what changed in self.migration_details so Runtime
        can emit a SCHEMA_MIGRATED TRACE event after construction."""
        changes: list = []
        with self._lock:
            cur = self.conn.execute("PRAGMA table_info(hub_entries)")
            columns = {row[1] for row in cur.fetchall()}
            if "original_hub" not in columns:
                self.conn.execute(
                    "ALTER TABLE hub_entries ADD COLUMN original_hub TEXT DEFAULT ''"
                )
                changes.append("hub_entries.original_hub")
            if "purged" not in columns:
                self.conn.execute(
                    "ALTER TABLE hub_entries ADD COLUMN purged INTEGER DEFAULT 0"
                )
                changes.append("hub_entries.purged")
            if "provenance" not in columns:
                self.conn.execute(
                    "ALTER TABLE hub_entries ADD COLUMN provenance TEXT DEFAULT '[]'"
                )
                changes.append("hub_entries.provenance")

        if changes:
            self.migration_occurred = True
            self.migration_details = changes

    # -----------------------------------------------------
    # Schema Version (§6.7.3)
    # -----------------------------------------------------
    def get_schema_version(self) -> Optional[int]:
        """Return the stored schema version, or None if never set."""
        with self._lock:
            cur = self.conn.execute(
                "SELECT value FROM system_state WHERE key='SCHEMA_VERSION'"
            )
            row = cur.fetchone()
            if row is None:
                return None
            try:
                return int(row[0])
            except (TypeError, ValueError):
                return None

    def set_schema_version(self, version: int) -> None:
        """Record the schema version in system_state."""
        ts = datetime.now(UTC).isoformat()
        with self._lock, self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO system_state VALUES(?,?,?)",
                ("SCHEMA_VERSION", str(version), ts),
            )

    # -----------------------------------------------------
    # TRACE
    # -----------------------------------------------------
    def save_trace_event(self, event: TraceEvent) -> None:
        with self._lock, self.conn:
            self.conn.execute(
                """INSERT INTO trace_events
                (timestamp,event_code,authority,artifact_id,
                 content_hash,byte_length,parent_hash)
                 VALUES(?,?,?,?,?,?,?)""",
                (
                    event.timestamp.isoformat(),
                    event.event_code,
                    event.authority,
                    event.artifact_id,
                    event.content_hash,
                    event.byte_length,
                    event.parent_hash,
                ),
            )

    def load_all_trace(self) -> List[TraceEvent]:
        with self._lock:
            cur = self.conn.execute(
                """SELECT timestamp,event_code,authority,artifact_id,
                          content_hash,byte_length,parent_hash
                   FROM trace_events ORDER BY id"""
            )

            return [
                TraceEvent(
                    timestamp=datetime.fromisoformat(r[0]),
                    event_code=r[1],
                    authority=r[2],
                    artifact_id=r[3],
                    content_hash=r[4],
                    byte_length=r[5],
                    parent_hash=r[6],
                )
                for r in cur.fetchall()
            ]

    # -----------------------------------------------------
    # HUBS (§4.4.3 original_hub, §4.4.5 purged)
    # -----------------------------------------------------
    def save_hub_entry(self, entry) -> None:
        with self._lock, self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO hub_entries VALUES(?,?,?,?,?,?,?,?,?)",
                (
                    entry.id,
                    entry.hub,
                    entry.content,
                    int(entry.redline),
                    entry.timestamp.isoformat(),
                    getattr(entry, "version", 1),
                    getattr(entry, "original_hub", entry.hub),
                    int(getattr(entry, "purged", False)),
                    json.dumps(getattr(entry, "provenance", [])),
                ),
            )

    def load_hub_entries(self, hub: str) -> List[dict]:
        with self._lock:
            cur = self.conn.execute(
                "SELECT id,hub,content,redline,timestamp,version,original_hub,purged,provenance "
                "FROM hub_entries WHERE hub=?",
                (hub,),
            )

            results = []
            for r in cur.fetchall():
                prov_raw = r[8] if len(r) > 8 and r[8] else "[]"
                try:
                    prov = json.loads(prov_raw)
                except (json.JSONDecodeError, TypeError):
                    prov = []
                results.append({
                    "id": r[0],
                    "hub": r[1],
                    "content": r[2],
                    "redline": bool(r[3]),
                    "timestamp": r[4],
                    "version": r[5],
                    "original_hub": r[6] or r[1],
                    "purged": bool(r[7]) if r[7] is not None else False,
                    "provenance": prov,
                })
            return results

    # -----------------------------------------------------
    # CONTAINERS (§5.2.1 — survive restart)
    # -----------------------------------------------------
    def save_container(self, container) -> None:
        """Save container metadata (profile, state, lifecycle) to SQLite."""
        with self._lock, self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO containers VALUES(?,?,?,?,?)",
                (
                    container.container_id,
                    json.dumps(container.profile.to_dict()),
                    container.state,
                    container.created_at.isoformat(),
                    json.dumps(getattr(container, "lifecycle_log", [])),
                ),
            )

    def load_containers(self) -> List[dict]:
        """Load all container metadata from SQLite."""
        with self._lock:
            cur = self.conn.execute(
                "SELECT container_id, profile, state, created_at, lifecycle_log "
                "FROM containers"
            )
            results = []
            for r in cur.fetchall():
                try:
                    profile = json.loads(r[1])
                except (json.JSONDecodeError, TypeError):
                    profile = {}
                try:
                    lifecycle_log = json.loads(r[4]) if r[4] else []
                except (json.JSONDecodeError, TypeError):
                    lifecycle_log = []
                results.append({
                    "container_id": r[0],
                    "profile": profile,
                    "state": r[2],
                    "created_at": r[3],
                    "lifecycle_log": lifecycle_log,
                })
            return results

    def save_container_hub_entry(self, container_id: str, entry) -> None:
        """Save a hub entry belonging to a specific container."""
        with self._lock, self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO container_hub_entries "
                "VALUES(?,?,?,?,?,?,?,?,?,?)",
                (
                    container_id,
                    entry.id,
                    entry.hub,
                    entry.content,
                    int(entry.redline),
                    entry.timestamp.isoformat(),
                    getattr(entry, "version", 1),
                    getattr(entry, "original_hub", entry.hub),
                    int(getattr(entry, "purged", False)),
                    json.dumps(getattr(entry, "provenance", [])),
                ),
            )

    def load_container_hub_entries(self, container_id: str, hub: str) -> List[dict]:
        """Load hub entries for a specific container and hub."""
        with self._lock:
            cur = self.conn.execute(
                "SELECT id,hub,content,redline,timestamp,version,original_hub,purged,provenance "
                "FROM container_hub_entries WHERE container_id=? AND hub=?",
                (container_id, hub),
            )
            results = []
            for r in cur.fetchall():
                prov_raw = r[8] if len(r) > 8 and r[8] else "[]"
                try:
                    prov = json.loads(prov_raw)
                except (json.JSONDecodeError, TypeError):
                    prov = []
                results.append({
                    "id": r[0],
                    "hub": r[1],
                    "content": r[2],
                    "redline": bool(r[3]),
                    "timestamp": r[4],
                    "version": r[5],
                    "original_hub": r[6] or r[1],
                    "purged": bool(r[7]) if r[7] is not None else False,
                    "provenance": prov,
                })
            return results

    # -----------------------------------------------------
    # TERMS
    # -----------------------------------------------------
    def save_sealed_term(self, term) -> None:
        with self._lock, self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO sealed_terms VALUES(?,?,?,?,?)",
                (
                    term.id,
                    term.label,
                    term.definition,
                    json.dumps(term.constraints),
                    term.version,
                ),
            )

    def load_sealed_terms(self) -> List[dict]:
        with self._lock:
            cur = self.conn.execute(
                "SELECT term_id,label,definition,constraints,version FROM sealed_terms"
            )

            return [
                {
                    "id": r[0],
                    "label": r[1],
                    "definition": r[2],
                    "constraints": json.loads(r[3]),
                    "version": r[4],
                }
                for r in cur.fetchall()
            ]

    # -----------------------------------------------------
    # CONSENT
    # -----------------------------------------------------
    def save_consent(self, key: str, record) -> None:
        with self._lock, self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO consents VALUES(?,?,?,?,?,?)",
                (
                    key,
                    record.action_class,
                    record.container_id,
                    record.requester,
                    record.status,
                    record.granted_at.isoformat()
                    if record.granted_at
                    else None,
                ),
            )

    def load_consents(self) -> List[dict]:
        with self._lock:
            cur = self.conn.execute(
                "SELECT key,action_class,container_id,requester,status,granted_at FROM consents"
            )

            return [
                {
                    "key": r[0],
                    "action_class": r[1],
                    "container_id": r[2],
                    "requester": r[3],
                    "status": r[4],
                    "granted_at": r[5],
                }
                for r in cur.fetchall()
            ]

    # -----------------------------------------------------
    # SYNONYMS
    # -----------------------------------------------------
    def save_synonym(self, phrase: str, term_id: str, confidence: str) -> None:
        with self._lock, self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO synonyms VALUES(?,?,?)",
                (phrase.lower(), term_id, confidence),
            )

    def load_synonyms(self) -> List[dict]:
        with self._lock:
            cur = self.conn.execute(
                "SELECT phrase,term_id,confidence FROM synonyms"
            )
            return [
                {
                    "phrase": r[0],
                    "term_id": r[1],
                    "confidence": r[2],
                }
                for r in cur.fetchall()
            ]

    def delete_synonym(self, phrase: str) -> None:
        """Remove synonym from persistence (§2.4.4). No ghost mappings on restart."""
        with self._lock, self.conn:
            self.conn.execute(
                "DELETE FROM synonyms WHERE phrase=?",
                (phrase.lower(),),
            )

    # -----------------------------------------------------
    # DISALLOWED TERMS
    # -----------------------------------------------------
    def save_disallowed(self, phrase: str, reason: str) -> None:
        with self._lock, self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO disallowed_terms VALUES(?,?)",
                (phrase.lower(), reason),
            )

    def load_disallowed(self) -> List[dict]:
        with self._lock:
            cur = self.conn.execute(
                "SELECT phrase,reason FROM disallowed_terms"
            )
            return [
                {"phrase": r[0], "reason": r[1]}
                for r in cur.fetchall()
            ]

    # -----------------------------------------------------
    # SYSTEM STATE (Safe-Stop, config flags)
    # -----------------------------------------------------
    def enter_safe_stop(self, reason: str) -> None:
        """Persist Safe-Stop state. Survives restart. Only T-0 can clear."""
        ts = datetime.now(UTC).isoformat()
        with self._lock, self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO system_state VALUES(?,?,?)",
                ("SAFE_STOP", reason, ts),
            )

    def is_safe_stopped(self) -> dict:
        """Check if system is in persistent Safe-Stop. Returns {active, reason, timestamp} or {active: False}."""
        with self._lock:
            cur = self.conn.execute(
                "SELECT value, updated_at FROM system_state WHERE key='SAFE_STOP'"
            )
            row = cur.fetchone()
            if row:
                return {"active": True, "reason": row[0], "timestamp": row[1]}
            return {"active": False}

    def clear_safe_stop(self) -> None:
        """Clear Safe-Stop. Only T-0 may call this."""
        with self._lock, self.conn:
            self.conn.execute("DELETE FROM system_state WHERE key='SAFE_STOP'")

    # -----------------------------------------------------
    def event_count(self) -> int:
        with self._lock:
            return self.conn.execute(
                "SELECT COUNT(*) FROM trace_events"
            ).fetchone()[0]

    def close(self) -> None:
        with self._lock:
            self.conn.close()
