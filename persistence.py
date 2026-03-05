"""
RSS v3 — Persistence Layer (Production Hardened)
SQLite backend. TRACE, hubs, terms, and consent survive restarts.
Thread-safe + WAL-enabled version.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, UTC
from typing import List

from audit_log import TraceEvent


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

        self._configure_db()
        self._create_tables()

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
                version INTEGER DEFAULT 1
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
            "CREATE INDEX IF NOT EXISTS idx_trace_code ON trace_events(event_code)",
            "CREATE INDEX IF NOT EXISTS idx_trace_artifact ON trace_events(artifact_id)",
            "CREATE INDEX IF NOT EXISTS idx_hub_hub ON hub_entries(hub)",
        ]

        with self._lock, self.conn:
            for stmt in stmts:
                self.conn.execute(stmt)

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
    # HUBS
    # -----------------------------------------------------
    def save_hub_entry(self, entry) -> None:
        with self._lock, self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO hub_entries VALUES(?,?,?,?,?,?)",
                (
                    entry.id,
                    entry.hub,
                    entry.content,
                    int(entry.redline),
                    entry.timestamp.isoformat(),
                    getattr(entry, "version", 1),
                ),
            )

    def load_hub_entries(self, hub: str) -> List[dict]:
        with self._lock:
            cur = self.conn.execute(
                "SELECT id,hub,content,redline,timestamp,version "
                "FROM hub_entries WHERE hub=?",
                (hub,),
            )

            return [
                {
                    "id": r[0],
                    "hub": r[1],
                    "content": r[2],
                    "redline": bool(r[3]),
                    "timestamp": r[4],
                    "version": r[5],
                }
                for r in cur.fetchall()
            ]

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
    def event_count(self) -> int:
        with self._lock:
            return self.conn.execute(
                "SELECT COUNT(*) FROM trace_events"
            ).fetchone()[0]

    def close(self) -> None:
        with self._lock:
            self.conn.close()