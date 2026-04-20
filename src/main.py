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
# Contact: rose.systems@outlook.com  (Subject: "Contact Us — RSS Commercial License")
# ==============================================================================
"""
RSS v0.1.0 — CLI Entry Point
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
from config import RSSConfig, RSS_VERSION
from runtime import bootstrap
from meaning_law import Term
from trace_export import export_trace_json, export_trace_text, export_from_db
from reference_pack import load_reference_pack, seed_demo_world, DEMO_CONTAINERS, DEMO_QUESTIONS


def run_tests(rss):
    """Core acceptance tests."""
    tests = [
        ("quote",             True,  "SEALED term"),
        ("Quote",             True,  "Case-insensitive sealed term"),
        ("RFI",               True,  "SEALED reference term"),
        ("change order",      True,  "SEALED multi-word term"),
        ("estimate",          False, "Ambiguous — unknown phrase"),
        ("delete everything", False, "Unknown phrase — passes through"),
        ("foobar baz",        False, "Unknown phrase"),
        ("submittal",         True,  "SEALED term"),
        ("purchase order",    True,  "New v0.1.0 term"),
        ("NCR",               True,  "New v0.1.0 term"),
    ]

    passed = 0
    failed = 0
    for text, should_pass, desc in tests:
        result = rss.process_request(text, use_llm=False)
        ok = "error" not in result
        status = "PASS" if ok == should_pass else "FAIL"
        error_info = result.get("error", result.get("meaning", "OK"))
        classification = result.get("classification", "—")
        print(f"  [{status}] '{text}' -> {error_info} (class={classification}) — {desc}")
        if status == "PASS":
            passed += 1
        else:
            failed += 1

    print(f"\n  Results: {passed} passed, {failed} failed")
    return failed == 0


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
        result = rss.process_request(text, use_llm=True)
        if "error" in result:
            print(f"RSS: I can't help with that right now.\n")
        else:
            response = result.get("llm_response", "No response available.")
            print(f"RSS: {response}\n")


def run_demo_suite(rss):
    """Deterministic governed walkthrough."""
    seeded = seed_demo_world(rss)
    print(f"  Demo world: {seeded['global_inserted']} global rows, {seeded['created']} containers created, {seeded['entries_inserted']} container rows inserted")
    print(f"  Ingress posture: {rss.ingress_posture_note()}")

    print("\n  [Global workflow]")
    for text in DEMO_QUESTIONS:
        result = rss.process_request(text, use_llm=True)
        answer = result.get("llm_response", result.get("error", "NO_RESPONSE"))
        print(f"    Q: {text}")
        print(f"    A: {answer}")

    print("\n  [Container workflows]")
    from tecton import ContainerRequest
    for spec in DEMO_CONTAINERS:
        cid = seeded["containers"][spec["label"]]
        print(f"\n    Container: {spec['label']} ({cid})")
        for text in spec["questions"]:
            result = rss.tecton.process_request(ContainerRequest(cid, "ᚱ", {"text": text}), rss).result
            answer = result.get("llm_response", result.get("error", "NO_RESPONSE"))
            print(f"      Q: {text}")
            print(f"      A: {answer}")


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
            print(f"    [{t['id']}] {t['label']} — {t['definition']} (v{t['version']})")


def add_term(rss, args):
    """Add a sealed term from CLI.
    Usage: python main.py add-term <label> <definition> [--force]
    Example: python main.py add-term invoice "Bill for completed work"
    Use --force for definitions that legitimately contain high-risk verbs (§2.3.3).
    """
    if len(args) < 2:
        print("  Usage: python main.py add-term <label> <definition> [--force]")
        print('  Example: python main.py add-term invoice "Bill for completed work"')
        print("  Use --force for definitions with legitimate high-risk verbs (§2.3.3)")
        return

    force = "--force" in args
    clean_args = [a for a in args if a != "--force"]
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
        rss.save_term(term, force=force)
        print(f"  Sealed term added: '{label}' — {definition}")
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
    Usage: python main.py add-synonym <phrase> <term_label> [confidence]
    Confidence: HIGH (auto-resolves), MED (requires confirmation), LOW
    """
    if len(args) < 2:
        print("  Usage: python main.py add-synonym <phrase> <term_label> [HIGH|MED|LOW]")
        print("  Example: python main.py add-synonym bid quote HIGH")
        return

    phrase = args[0]
    term_label = args[1]
    confidence = args[2].upper() if len(args) > 2 else "MED"

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
        rss.save_synonym(phrase, term_id, confidence)
        print(f"  Synonym added: '{phrase}' -> '{term_label}' ({confidence})")
    except Exception as e:
        print(f"  Error: {e}")


def remove_synonym_cmd(rss, args):
    """Remove a synonym (§2.4.4).
    Usage: python main.py remove-synonym <phrase>
    Returns phrase to null-state (AMBIGUOUS). No ghost mappings.
    """
    if len(args) < 1:
        print("  Usage: python main.py remove-synonym <phrase>")
        print("  Example: python main.py remove-synonym bid")
        return

    phrase = args[0]
    try:
        rss.remove_synonym(phrase)
        print(f"  Synonym removed: '{phrase}' (returned to null-state)")
    except Exception as e:
        print(f"  Error: {e}")


def disallow_term(rss, args):
    """Mark a term as explicitly disallowed.
    Usage: python main.py disallow <phrase> <reason>
    """
    if len(args) < 2:
        print("  Usage: python main.py disallow <phrase> <reason>")
        print('  Example: python main.py disallow hack "Security violation"')
        return

    phrase = args[0]
    reason = " ".join(args[1:])

    rss.save_disallowed(phrase, reason)
    print(f"  Disallowed: '{phrase}' — {reason}")


def list_terms(rss):
    """List all sealed terms, synonyms, and disallowed terms."""
    terms = rss.meaning.list_sealed()
    if not terms:
        print("  No sealed terms.")
    else:
        print(f"\n  Sealed terms ({len(terms)}):")
        for t in terms:
            print(f"    [{t['id']}] {t['label']} — {t['definition']} (v{t['version']})")

    if rss.meaning._synonyms:
        print(f"\n  Synonyms ({len(rss.meaning._synonyms)}):")
        for phrase, info in rss.meaning._synonyms.items():
            print(f"    '{phrase}' -> {info['term_id']} ({info['confidence']})")

    if rss.meaning._disallowed:
        print(f"\n  Disallowed ({len(rss.meaning._disallowed)}):")
        for phrase, reason in rss.meaning._disallowed.items():
            print(f"    '{phrase}' — {reason}")


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

    print(f"\n  RSS v{RSS_VERSION} booted — AI that waits.\n")

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
            rss.clear_safe_stop()
            print(f"  Safe-Stop cleared. Reason was: {ss['reason']}")
            print(f"  System operational. T-0 authority exercised.")
        else:
            print("  System is not in Safe-Stop.")
    else:
        print(f"  Unknown command: {cmd}")
        print("  Commands: test | demo | demo-suite | status | add-term | add-synonym | remove-synonym | disallow | add-entry | list-terms | list-hub | export-trace | clear-safe-stop")

    rss.persistence.close()
