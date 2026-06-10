# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: RSS v0.1.0 Entry Point
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
# Contact: christain@rosesigilsystems.com  (Subject: "RSS Commercial License")
# ==============================================================================
"""
RSS v0.1.0 - CLI Entry Point
Usage:
  python main.py test              Run test suite
  python main.py demo              Interactive governed AI chat
  python main.py demo-suite        Deterministic governed walkthrough
  python main.py status            Show system status
  python main.py add-term          Add a sealed term
  python main.py add-synonym       Add a synonym for a sealed term
  python main.py disallow          Mark a term as disallowed
  python main.py add-entry         Add a hub entry
  python main.py list-terms        List all sealed terms (+ synonyms + disallowed)
  python main.py list-hub          List hub entries
  python main.py export-trace      Export TRACE audit log to file
"""
import sys
from pathlib import Path
from rss.core.config import RSSConfig, RSS_VERSION
from rss.core.runtime import bootstrap
from rss.governance.seats.rune import Term
from rss.audit.export import export_trace_json, export_trace_text, export_from_db
from rss.reference_pack import load_reference_pack, seed_demo_world, DEMO_CONTAINERS, DEMO_QUESTIONS


def run_tests(rss):
    """Core acceptance tests."""
    tests = [
        ("quote",             "SEALED",    "SEALED term"),
        ("Quote",             "SEALED",    "Case-insensitive sealed term"),
        ("RFI",               "SEALED",    "SEALED reference term"),
        ("change order",      "SEALED",    "SEALED multi-word term"),
        ("estimate",          "AMBIGUOUS", "Ambiguous unknown phrase"),
        ("delete everything", "AMBIGUOUS", "High-risk intent remains unsealed"),
        ("foobar baz",        "AMBIGUOUS", "Unknown phrase"),
        ("submittal",         "SEALED",    "SEALED term"),
        ("purchase order",    "SEALED",    "New v0.1.0 term"),
        ("NCR",               "SEALED",    "New v0.1.0 term"),
    ]

    passed = 0
    failed = 0
    for text, expected_meaning, desc in tests:
        result = rss.process_request(text, use_llm=False)
        actual_meaning = result.get("meaning")
        status = "PASS" if actual_meaning == expected_meaning else "FAIL"
        error_info = result.get("error", result.get("meaning", "OK"))
        classification = result.get("classification", "-")
        print(f"  [{status}] '{text}' -> {error_info} (class={classification}, expected={expected_meaning}) - {desc}")
        if status == "PASS":
            passed += 1
        else:
            failed += 1

    print(f"\n  Results: {passed} passed, {failed} failed")
    return failed == 0


DEMO_DATA_MARKERS = (
    "quote", "rfi", "daily log", "submittal", "tenant", "project", "record",
    "file", "private", "personal", "redline", "work", "hub", "data",
    "northwind", "harbor", "aster", "lumen", "medical", "legal",
    "construction", "finance", "invoice", "variance", "approval",
    "punch list", "change order", "safety hold", "cash risk",
)


def demo_scope_policy_for(text: str):
    """Demo-only router for normal chat vs governed data lookup.

    This is not the final RUNE/domain-pack architecture. It keeps the current
    interactive demo honest: ordinary conceptual chat gets a SYSTEM-only scope,
    while obvious seeded-data questions still open the governed WORK/PAV path.
    """
    lower = (text or "").lower()
    if any(marker in lower for marker in DEMO_DATA_MARKERS):
        return None
    return {
        "allowed_sources": ["SYSTEM"],
        "forbidden_sources": ["WORK", "PERSONAL", "ARCHIVE", "LEDGER"],
    }


def run_demo(rss):
    """Interactive governed AI chat."""
    inserted = load_reference_pack(rss)
    if inserted > 0:
        print(f"  Loaded shared reference pack: {inserted} new entries")
    else:
        print(f"  Shared reference pack already present: {rss.hubs.hub_stats()['WORK']} WORK entries")

    print(f"  LLM: {'connected' if rss.llm.is_available() else 'fallback mode'}")
    print("  Type your question. 'quit' to exit.\n")

    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if text.lower() in ("quit", "exit", "q"):
            break
        if not text:
            continue
        result = rss.process_request(text, use_llm=True, scope_policy=demo_scope_policy_for(text))
        if "error" in result:
            print(f"RSS: I can't help with that right now.\n")
        else:
            response = result.get("llm_response", "No response available.")
            print(f"RSS: {response}\n")


def run_demo_suite(rss):
    """Deterministic governed walkthrough using the canonical proof suite."""
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    from examples.demo_suite import build_demo_report, _proof_status

    report = build_demo_report(live_llm=False)
    print(report["transcript"])
    print(f"\n  Proof status: {_proof_status(report['verification'])}")
    print("  For handoff artifacts: python examples/demo_suite.py --offline --artifacts demo_artifacts")


def show_status(rss):
    """Show system status."""
    ss = rss.is_safe_stopped()
    if ss["active"]:
        print(f"\n  *** SAFE-STOP ACTIVE ***")
        print(f"  Reason:   {ss['reason']}")
        print(f"  Since:    {ss.get('timestamp', 'unknown')}")
        print(f"  Clear:    python main.py clear-safe-stop\n")

    print(f"  Version:      {rss.config.version}")
    print(f"  Safe-Stop:    {'ACTIVE' if ss['active'] else 'clear'}")
    print(f"  Sealed terms: {len(rss.meaning.list_sealed())}")
    print(f"  TRACE events: {rss.persistence.event_count()}")
    print(f"  LLM:          {'available' if rss.llm.is_available() else 'fallback mode'}")
    print(f"  DB:           {rss.config.db_path}")
    print(f"  Hub stats:    {rss.hubs.hub_stats()}")
    print(f"  Seats:        {rss.ward.list_seats()}")
    print(f"  Chain valid:  {rss.trace.verify_chain()}")
    print(f"  Ingress:      {rss.ingress_posture_note()}")

    terms = rss.meaning.list_sealed()
    if terms:
        print(f"\n  Sealed terms:")
        for t in terms:
            print(f"    [{t['id']}] {t['label']} - {t['definition']} (v{t['version']})")


def _print_t0_denial(result):
    """Print protected-mutation denials returned by runtime helpers."""
    if isinstance(result, dict) and result.get("error") == "T0_COMMAND_REQUIRED":
        reason = result.get("reason", "T-0 command required")
        print(f"  Error: {result['error']} - {reason}")
        print("  Add --t0-command to explicitly exercise the current soft T-0 gate.")
        return True
    return False


def add_term(rss, args):
    """Add a sealed term from CLI.
    Usage: python main.py add-term <label> <definition> [--t0-command] [--force]
    Example: python main.py add-term invoice "Bill for completed work" --t0-command
    Use --force for definitions that legitimately contain high-risk verbs (Pact 2.3.3).
    """
    if len(args) < 2:
        print("  Usage: python main.py add-term <label> <definition> [--t0-command] [--force]")
        print('  Example: python main.py add-term invoice "Bill for completed work" --t0-command')
        print("  Use --force for definitions with legitimate high-risk verbs (Pact 2.3.3)")
        return

    force = "--force" in args
    t0_command = "--t0-command" in args
    clean_args = [a for a in args if a not in ("--force", "--t0-command")]
    if len(clean_args) < 2:
        print("  Usage: python main.py add-term <label> <definition> [--t0-command] [--force]")
        return
    label = clean_args[0]
    definition = " ".join(clean_args[1:])

    # Check if term already exists
    existing = [t["label"].lower() for t in rss.meaning.list_sealed()]
    if label.lower() in existing:
        print(f"  Term '{label}' already exists.")
        return

    term = Term(
        id=label,
        label=label,
        definition=definition,
        constraints=[],
        version="1.0",
    )
    try:
        result = rss.save_term(term, force=force, t0_command=t0_command)
        if _print_t0_denial(result):
            return
        print(f"  Sealed term added: '{label}' - {definition}")
        if force:
            print("  NOTE: Anti-trojan scanner bypassed (T-0 force override, logged by TRACE)")
        print(f"  Total terms: {len(rss.meaning.list_sealed())}")
    except Exception as e:
        print(f"  Error: {e}")


def add_entry(rss, args):
    """Add a hub entry from CLI.
    Usage: python main.py add-entry <hub> <content> [--redline]
    Example: python main.py add-entry WORK "Morrison panel upgrade quote: $245K"
    """
    if len(args) < 2:
        print("  Usage: python main.py add-entry <hub> <content> [--redline]")
        print('  Example: python main.py add-entry WORK "Morrison panel upgrade"')
        return

    hub = args[0].upper()
    redline = "--redline" in args
    content_parts = [a for a in args[1:] if a != "--redline"]
    content = " ".join(content_parts)

    try:
        entry = rss.save_hub_entry(hub, content, redline=redline)
        print(f"  Entry added to {hub}: {entry.id}")
        if redline:
            print("  REDLINE: This entry will never reach the LLM.")
        print(f"  Hub stats: {rss.hubs.hub_stats()}")
    except Exception as e:
        print(f"  Error: {e}")


def add_synonym(rss, args):
    """Add a synonym for a sealed term.
    Usage: python main.py add-synonym <phrase> <term_label> [confidence] [--t0-command]
    Confidence: HIGH (auto-resolves), MED (requires confirmation), LOW
    """
    if len(args) < 2:
        print("  Usage: python main.py add-synonym <phrase> <term_label> [HIGH|MED|LOW] [--t0-command]")
        print("  Example: python main.py add-synonym bid quote HIGH --t0-command")
        return

    t0_command = "--t0-command" in args
    clean_args = [a for a in args if a != "--t0-command"]
    if len(clean_args) < 2:
        print("  Usage: python main.py add-synonym <phrase> <term_label> [HIGH|MED|LOW] [--t0-command]")
        return
    phrase = clean_args[0]
    term_label = clean_args[1]
    confidence = clean_args[2].upper() if len(clean_args) > 2 else "MED"

    if confidence not in ("HIGH", "MED", "LOW"):
        print(f"  Invalid confidence: {confidence}. Use HIGH, MED, or LOW.")
        return

    terms = rss.meaning.list_sealed()
    match = [t for t in terms if t["label"].lower() == term_label.lower()]
    if not match:
        print(f"  No sealed term found with label '{term_label}'.")
        print(f"  Available: {', '.join(t['label'] for t in terms)}")
        return

    term_id = match[0]["id"]
    try:
        result = rss.save_synonym(phrase, term_id, confidence, t0_command=t0_command)
        if _print_t0_denial(result):
            return
        print(f"  Synonym added: '{phrase}' -> '{term_label}' ({confidence})")
    except Exception as e:
        print(f"  Error: {e}")


def remove_synonym_cmd(rss, args):
    """Remove a synonym (Pact 2.4.4).
    Usage: python main.py remove-synonym <phrase> [--t0-command]
    Returns phrase to null-state (AMBIGUOUS). No ghost mappings.
    """
    if len(args) < 1:
        print("  Usage: python main.py remove-synonym <phrase> [--t0-command]")
        print("  Example: python main.py remove-synonym bid --t0-command")
        return

    t0_command = "--t0-command" in args
    clean_args = [a for a in args if a != "--t0-command"]
    if not clean_args:
        print("  Usage: python main.py remove-synonym <phrase> [--t0-command]")
        return
    phrase = clean_args[0]
    try:
        result = rss.remove_synonym(phrase, t0_command=t0_command)
        if _print_t0_denial(result):
            return
        print(f"  Synonym removed: '{phrase}' (returned to null-state)")
    except Exception as e:
        print(f"  Error: {e}")


def disallow_term(rss, args):
    """Mark a term as explicitly disallowed.
    Usage: python main.py disallow <phrase> <reason> [--t0-command]
    """
    if len(args) < 2:
        print("  Usage: python main.py disallow <phrase> <reason> [--t0-command]")
        print('  Example: python main.py disallow hack "Security violation" --t0-command')
        return

    t0_command = "--t0-command" in args
    clean_args = [a for a in args if a != "--t0-command"]
    if len(clean_args) < 2:
        print("  Usage: python main.py disallow <phrase> <reason> [--t0-command]")
        return
    phrase = clean_args[0]
    reason = " ".join(clean_args[1:])

    result = rss.save_disallowed(phrase, reason, t0_command=t0_command)
    if _print_t0_denial(result):
        return
    print(f"  Disallowed: '{phrase}' - {reason}")


def list_terms(rss):
    """List all sealed terms, synonyms, and disallowed terms."""
    terms = rss.meaning.list_sealed()
    if not terms:
        print("  No sealed terms.")
    else:
        print(f"\n  Sealed terms ({len(terms)}):")
        for t in terms:
            print(f"    [{t['id']}] {t['label']} - {t['definition']} (v{t['version']})")

    if rss.meaning._synonyms:
        print(f"\n  Synonyms ({len(rss.meaning._synonyms)}):")
        for phrase, info in rss.meaning._synonyms.items():
            print(f"    '{phrase}' -> {info['term_id']} ({info['confidence']})")

    if rss.meaning._disallowed:
        print(f"\n  Disallowed ({len(rss.meaning._disallowed)}):")
        for phrase, reason in rss.meaning._disallowed.items():
            print(f"    '{phrase}' - {reason}")


def list_hub(rss, args):
    """List hub entries.
    Usage: python main.py list-hub [hub_name]
    """
    hub_name = args[0].upper() if args else None
    stats = rss.hubs.hub_stats()

    if hub_name:
        hubs_to_show = [hub_name]
    else:
        hubs_to_show = [h for h, count in stats.items() if count > 0]

    if not hubs_to_show:
        print("  No hub entries.")
        return

    for hub in hubs_to_show:
        entries = rss.hubs.list_hub(hub)
        print(f"\n  {hub} ({len(entries)} entries):")
        for e in entries:
            redline_tag = " [REDLINE]" if e.redline else ""
            content_preview = e.content[:80] + "..." if len(e.content) > 80 else e.content
            print(f"    {e.id}: {content_preview}{redline_tag}")


def export_trace(rss, args):
    """Export TRACE audit log.
    Usage: python main.py export-trace [filename] [--text]
    Default: JSON format, file=rss_trace_export.json
    Exports from SQLite (all persisted events) + any in-memory events.
    """
    use_text = "--text" in args
    clean_args = [a for a in args if a != "--text"]
    
    if use_text:
        default_name = "rss_trace_export.txt"
    else:
        default_name = "rss_trace_export.json"
    
    filename = clean_args[0] if clean_args else default_name

    # Use DB export (has all persisted events across sessions)
    fmt = "text" if use_text else "json"
    count = export_from_db(rss.persistence, filename, fmt)

    print(f"  Exported {count} TRACE events to {filename}")
    print(f"  Source: SQLite ({rss.config.db_path})")


if __name__ == "__main__":
    config = RSSConfig()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "test"
    extra_args = sys.argv[2:] if len(sys.argv) > 2 else []

    # Use restore=True for commands that need persisted state
    restore = cmd in ("demo", "demo-suite", "status", "list-terms", "list-hub", "add-term", "add-entry", "add-synonym", "remove-synonym", "disallow", "export-trace", "clear-safe-stop")
    rss = bootstrap(config, restore=restore)

    print(f"\n  RSS v{RSS_VERSION} booted - AI that waits.\n")

    if cmd == "test":
        success = run_tests(rss)
        rss.persistence.close()
        sys.exit(0 if success else 1)
    elif cmd == "demo":
        run_demo(rss)
    elif cmd == "demo-suite":
        run_demo_suite(rss)
    elif cmd == "status":
        show_status(rss)
    elif cmd == "add-term":
        add_term(rss, extra_args)
    elif cmd == "add-synonym":
        add_synonym(rss, extra_args)
    elif cmd == "remove-synonym":
        remove_synonym_cmd(rss, extra_args)
    elif cmd == "disallow":
        disallow_term(rss, extra_args)
    elif cmd == "add-entry":
        add_entry(rss, extra_args)
    elif cmd == "list-terms":
        list_terms(rss)
    elif cmd == "list-hub":
        list_hub(rss, extra_args)
    elif cmd == "export-trace":
        export_trace(rss, extra_args)
    elif cmd == "clear-safe-stop":
        ss = rss.is_safe_stopped()
        if ss["active"]:
            rss.clear_safe_stop(t0_command=True)
            print(f"  Safe-Stop cleared. Reason was: {ss['reason']}")
            print(f"  System operational. T-0 authority exercised.")
        else:
            print("  System is not in Safe-Stop.")
    else:
        print(f"  Unknown command: {cmd}")
        print("  Commands: test | demo | demo-suite | status | add-term | add-synonym | remove-synonym | disallow | add-entry | list-terms | list-hub | export-trace | clear-safe-stop")

    rss.persistence.close()
