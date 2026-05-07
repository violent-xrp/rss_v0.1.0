# RSS Claim Traceability Matrix

_Auto-generated from split `tests/test_*.py` modules on 2026-05-07 15:43 UTC_

This document maps Pact sections to the test functions that prove them. Each entry cites a `# CLAIM:` tag in the test source. Regenerate with `python build_claim_matrix.py`.

**Coverage:** 103 distinct Pact sections referenced across 140 claim tags on 140 test functions.

---

## §0.1

- `test_runtime_default_term_pack_is_config_driven` — runtime bootstrap term pack is config-driven, not hardcoded; definition prefix also config-driven
- `test_genesis_binding_and_offline_fallback` — Genesis artifact bound from config; offline fallback summarizes governed data; shared reference pack is idempotent; ingress posture exposed

## §0.2

- `test_constitution` — constitution hashing, verify_integrity, safe_stop
- `test_constitution_load_constitution` — load_constitution: file-not-found, hash-mismatch, missing-marker, and happy-path branches

## §0.2.1

- `test_constitution_load_constitution` — load_constitution: file-not-found, hash-mismatch, missing-marker, and happy-path branches
- `test_genesis_blocking` — genesis tamper blocks boot; production_mode enforcement
- `test_genesis_binding_and_offline_fallback` — Genesis artifact bound from config; offline fallback summarizes governed data; shared reference pack is idempotent; ingress posture exposed

## §0.3

- `test_trace_seat` — TRACE as WARD-routed seat
- `test_tecton` — TECTON tenant container basics

## §0.3.1

- `test_s5_sigil_alignment` — eight seat sigils and reverse resolution

## §0.5

- `test_idempotence_replay` — Safe-Stop/schema/declassify/revocation/verification are idempotent
- `test_scenario_high_liability_flow` — high-liability review flow: REDLINE + revoke + resume + halt + recover
- `test_scenario_tamper_recovery` — tamper → boot detection → Safe-Stop → T-0 recovery → resumed governance
- `test_trace_export` — TRACE export format and REDLINE sanitization
- `test_safe_stop_persistent` — Safe-Stop persists across restart
- `test_probe_safe_stop_recovery_ceremony` — full operator-triggered Safe-Stop recovery ceremony with audit durability
- `test_trace_verify_additional_proof` — cold verifier: corrupted schema version degrades gracefully; mixed known/unknown codes reported; safe-stop state readable cold
- `test_phase_g_demo_suite_operator_flow` — Phase G demo suite proves governed usefulness, REDLINE exclusion, consent recovery, Safe-Stop restart recovery, isolation, and cold TRACE verification

## §0.5.2

- `test_safe_stop_persistent` — Safe-Stop persists across restart
- `test_clear_safe_stop_idempotence` — clear_safe_stop is idempotent: returns NO_OP without emitting audit event when system is not halted; emits SAFE_STOP_CLEARED only on real clear

## §0.5.4

- `test_c_phase_regression_battery` — canonical JSON, profile freezing, strict mode, threshold Safe-Stop, REDLINE sanitization
- `test_safe_stop_persistent` — Safe-Stop persists across restart

## §0.7.3

- `test_trace_seat` — TRACE as WARD-routed seat
- `test_pre_seal_drift_check` — pre-seal drift guard

## §0.8.3

- `test_pre_seal_drift_check` — pre-seal drift guard
- `test_write_ahead_guarantee` — audit write-ahead guarantee
- `test_phase_d_regression_battery` — UUID ingress, scope-on-permission, OATH persistence-failure visibility

## §0.8.4

- `test_s0_8_4_governed_state_bootstrap_roundtrip` — every listed governed-state category restores on bootstrap

## §0.9

- `test_oath_additional_proof` — OATH consent namespace normalization, persistence-failure density, malformed namespace fail-closed behavior

## §1.2

- `test_ward` — WARD seat registration, routing, hooks

## §1.3

- `test_scope` — SCOPE envelope creation and boundary enforcement

## §1.4

- `test_scenario_high_liability_flow` — high-liability review flow: REDLINE + revoke + resume + halt + recover
- `test_oath` — OATH consent grant, revoke, check
- `test_oath_extended_edges` — OATH extended edges: revocation fallback, multi-container consent, status accounting
- `test_oath_input_normalization_and_handle_edges` — OATH input normalization: blank container_id normalizes to GLOBAL; handle() structured error paths
- `test_oath_additional_proof` — OATH consent namespace normalization, persistence-failure density, malformed namespace fail-closed behavior
- `test_a1_consent_persistence_roundtrip` — consent state persists and restores

## §1.5

- `test_seal_review_attestation` — review_complete attestation replaces council_vote

## §1.6

- `test_scribe` — SCRIBE drafting and versioning
- `test_scribe_extended_edges` — SCRIBE extended edges: draft uniqueness, error states, UAP assembly, status, and handle dispatch

## §1.7

- `test_ward_hook_enforcement` — WARD hooks cannot mutate protected governance keys
- `test_ward` — WARD seat registration, routing, hooks
- `test_scribe_extended_edges` — SCRIBE extended edges: draft uniqueness, error states, UAP assembly, status, and handle dispatch

## §1.8

- `test_seal` — SEAL sovereign lock/verify
- `test_seal_extended_edges` — SEAL extended edges: rejection path, invalid review inputs, idempotent ratification, whitespace normalization
- `test_seal_ceremony_additional_proof` — SEAL ceremony: rejection-cycle re-review blocked, mixed-case verdict normalizes, amendment history ordering, ratification idempotence

## §1.9

- `test_cycle` — CYCLE quantitative cadence enforcement
- `test_cycle_extended_edges` — CYCLE strict-mode diagnostics and handle routing remain fail-closed and observable

## §2.1

- `test_domain_pack_equivalence` — governance domain-agnostic across legal/medical/finance
- `test_runtime_default_term_pack_is_config_driven` — runtime bootstrap term pack is config-driven, not hardcoded; definition prefix also config-driven
- `test_meaning_law` — RUNE term sealing, synonym binding, disallowed

## §2.1.1

- `test_word_boundary` — word-boundary term matching

## §2.1.2

- `test_probe_rune_resists_normalization_bypass` — RUNE disallowed resists whitespace/punct/case/control/NFKC/null bypass

## §2.2

- `test_anti_trojan_runtime` — anti-trojan in governed save path

## §2.3

- `test_anti_trojan` — anti-trojan term-definition scanner
- `test_anti_trojan_runtime` — anti-trojan in governed save path
- `test_contextual_reinjection` — sealed term contextual reinjection format; constraints stay kernel metadata

## §2.3.3

- `test_anti_trojan` — anti-trojan term-definition scanner

## §2.4

- `test_meaning_law` — RUNE term sealing, synonym binding, disallowed
- `test_vocabulary_management` — vocabulary add/update/remove persistence

## §2.4.4

- `test_vocabulary_management` — vocabulary add/update/remove persistence
- `test_synonym_removal` — synonym removal cleans memory and DB; no ghost

## §2.7

- `test_probe_chain_catches_duplicate_content_tamper` — hash envelope uniqueness; chain detects middle-row deletion

## §2.8.1

- `test_adversarial_scope_escalation` — scope mutation blocked at multiple layers
- `test_classification_order` — DISALLOWED takes precedence over SEALED

## §2.8.4

- `test_compound_detection` — compound term detection with word boundary

## §2.9

- `test_contextual_reinjection` — sealed term contextual reinjection format; constraints stay kernel metadata

## §2.10.2

- `test_redline_suppression` — REDLINE count suppressed from response, logged to TRACE

## §3.1.3

- `test_config_driven_verbs` — high-risk verbs driven by config, not hardcoded

## §3.2

- `test_state_machine` — execution state transitions
- `test_execution_word_boundary_hardening` — verb classification should respect word boundaries

## §3.3

- `test_adversarial_malformed_inputs` — pipeline survives 10K/empty/unicode/0/negative/50K malformed inputs
- `test_runtime` — runtime full pipeline happy path and halt semantics

## §3.3.4

- `test_a1_ttl_enforcement_in_stage_4` — expired intent rejected at Stage 4 with PIPELINE_ERROR
- `test_pipeline_stage_tracking` — every halt carries stage number and stage_name

## §3.4

- `test_oath_extended_edges` — OATH extended edges: revocation fallback, multi-container consent, status accounting

## §3.4.3

- `test_oath_input_normalization_and_handle_edges` — OATH input normalization: blank container_id normalizes to GLOBAL; handle() structured error paths

## §3.4.4

- `test_safe_stop_inflight` — SAFE_STOP_INFLIGHT halt semantics

## §3.4.5

- `test_event_code_taxonomy` — event code uppercase/no-space discipline

## §3.7

- `test_probe_indirect_prompt_injection_stays_data_not_authority` — indirect prompt injection remains scoped data, not authority
- `test_llm` — LLM adapter contract
- `test_genesis_binding_and_offline_fallback` — Genesis artifact bound from config; offline fallback summarizes governed data; shared reference pack is idempotent; ingress posture exposed
- `test_phase_g_demo_suite_operator_flow` — Phase G demo suite proves governed usefulness, REDLINE exclusion, consent recovery, Safe-Stop restart recovery, isolation, and cold TRACE verification

## §3.7.5

- `test_configurable_llm_timeout` — LLM timeout configurable, not hardcoded
- `test_llm_availability_timeout_is_config_driven` — LLM availability check timeout is config-driven via llm_availability_check_timeout; independent of generation timeout

## §3.7.7

- `test_a1_post_llm_scan_covers_archive_and_ledger` — post-LLM REDLINE scan covers ARCHIVE and LEDGER hubs
- `test_llm_response_validation` — post-LLM scan strips external names and governance artifacts

## §4.1

- `test_demo_world_seed_and_container_isolation` — demo world seed is idempotent; container data is isolated across tenants; governed offline fallback answers from seeded global data

## §4.2.3

- `test_instructional_override` — jailbreak attempts cannot surface PERSONAL or REDLINE
- `test_pav` — PAV builder — sovereign guard, REDLINE exclusion
- `test_s4_personal_scope_guard` — PERSONAL hub requires sovereign=True
- `test_s4_pipeline_integration` — S4 features integrated in full pipeline

## §4.3

- `test_hubs` — HubTopology basics: add, update, list, search, remove

## §4.3.4

- `test_probe_untrusted_import_hash_binding` — untrusted import receipt hash-binds source and wrapped content
- `test_s4_hub_provenance` — hub provenance chain: CREATED/ARCHIVED/PURGED/DECLASSIFIED
- `test_s4_provenance_persistence` — provenance chain survives restart
- `test_archive_entry_returns_hub_entry` — archive_entry returns the archived HubEntry with provenance logged; return value matches other lifecycle method convention

## §4.3.5

- `test_f2_entry_id_stability` — entry IDs stable across restart (no re-generation)
- `test_f2_container_entry_id_stability` — container entry IDs stable across restart

## §4.4.3

- `test_s4_archival_original_hub` — archive preserves original_hub
- `test_s4_persistence_roundtrip` — original_hub and purged survive SQLite round-trip
- `test_archive_entry_returns_hub_entry` — archive_entry returns the archived HubEntry with provenance logged; return value matches other lifecycle method convention

## §4.4.5

- `test_s4_hard_purge` — sovereign hard purge: content overwrite, REDLINE flag, TRACE event
- `test_s4_persistence_roundtrip` — original_hub and purged survive SQLite round-trip

## §4.5

- `test_adversarial_policy_confusion` — policy confusion: global vs container consent; forbidden wins at PAV; production-mode
- `test_probe_indirect_prompt_injection_stays_data_not_authority` — indirect prompt injection remains scoped data, not authority

## §4.5.2

- `test_s4_governed_search` — cross-hub governed search excludes PERSONAL without opt-in

## §4.5.3

- `test_scope` — SCOPE envelope creation and boundary enforcement
- `test_s4_scope_hub_validation` — hub name validation in allowed/forbidden
- `test_s4_pipeline_integration` — S4 features integrated in full pipeline

## §4.5.4

- `test_s4_scope_container_id` — SCOPE envelope carries container_id (default GLOBAL)
- `test_s4_pipeline_integration` — S4 features integrated in full pipeline

## §4.5.7

- `test_adversarial_scope_escalation` — scope mutation blocked at multiple layers
- `test_s4_scope_immutability` — SCOPE envelope tuples; frozen dataclass
- `test_s5_scope_policy_tuples` — container scope_policy tuples frozen

## §4.6

- `test_a1_post_llm_scan_covers_archive_and_ledger` — post-LLM REDLINE scan covers ARCHIVE and LEDGER hubs
- `test_pav` — PAV builder — sovereign guard, REDLINE exclusion

## §4.6.6

- `test_s4_pav_hub_audit` — PAV records contributing_hubs

## §4.6.7

- `test_s4_ledger_pav_exclusion` — LEDGER excluded from PAV unless brainstorming=True

## §4.7

- `test_domain_pack_equivalence` — governance domain-agnostic across legal/medical/finance
- `test_scenario_high_liability_flow` — high-liability review flow: REDLINE + revoke + resume + halt + recover
- `test_phase_g_demo_suite_operator_flow` — Phase G demo suite proves governed usefulness, REDLINE exclusion, consent recovery, Safe-Stop restart recovery, isolation, and cold TRACE verification

## §4.7.4

- `test_s4_redline_declassification` — REDLINE declassification is single-shot with TRACE event

## §4.7.6

- `test_instructional_override` — jailbreak attempts cannot surface PERSONAL or REDLINE
- `test_probe_indirect_prompt_injection_stays_data_not_authority` — indirect prompt injection remains scoped data, not authority
- `test_probe_redline_not_leaked_via_search_surfaces` — search() and governed_search() fail-closed on REDLINE
- `test_probe_pav_still_excludes_redline_via_list_hub` — list_hub permissive for governed callers; PAV still excludes REDLINE
- `test_trace_export_cold_container_redline_sanitization` — cold TRACE export sanitizes REDLINE artifact IDs from container hub rows as well as global rows
- `test_trace_export_token_boundary_sanitization` — REDLINE artifact_id sanitization uses token-boundary matching; non-REDLINE tokens survive
- `test_trace_export_additional_proof` — TRACE export: summary integrity under filters, live/cold parity, multi-token REDLINE redaction, mixed global/container export

## §5.1

- `test_adversarial_ingress` — spoofed/None/empty container_id handled; ingress sentinel required
- `test_demo_world_seed_and_container_isolation` — demo world seed is idempotent; container data is isolated across tenants; governed offline fallback answers from seeded global data
- `test_phase_g_demo_suite_operator_flow` — Phase G demo suite proves governed usefulness, REDLINE exclusion, consent recovery, Safe-Stop restart recovery, isolation, and cold TRACE verification
- `test_tecton` — TECTON tenant container basics

## §5.1.1

- `test_adversarial_cross_container` — no cross-container bleed across hub data, events, or threads
- `test_exception_context_leak` — exception in tenant A does not leak context or data to tenant B
- `test_s5_container_isolation` — Morrison and Johnson containers cannot see each other's data
- `test_phase_e5_contextvar_isolation` — context-bound hub isolation via ContextVar, thread-level

## §5.2

- `test_demo_world_seed_and_container_isolation` — demo world seed is idempotent; container data is isolated across tenants; governed offline fallback answers from seeded global data

## §5.2.1

- `test_f2_container_entry_id_stability` — container entry IDs stable across restart
- `test_s5_container_persistence` — containers persist and restore from SQLite

## §5.2.2

- `test_s5_lifecycle_transitions` — container lifecycle state transitions
- `test_s5_valid_transitions_table` — transition table structural sanity
- `test_tecton_destructive_transitions_require_reason` — destructive TECTON transitions (suspend/reactivate/archive/destroy) require non-empty reason; reason persisted in lifecycle_log and TRACE event

## §5.2.5

- `test_s5_destroyed_inaccessibility` — DESTROYED is terminal; all access blocked
- `test_tecton_destructive_transitions_require_reason` — destructive TECTON transitions (suspend/reactivate/archive/destroy) require non-empty reason; reason persisted in lifecycle_log and TRACE event

## §5.2.6

- `test_s5_lifecycle_logging` — all lifecycle transitions emit TRACE events

## §5.2.7

- `test_s5_lifecycle_provenance` — container keeps its own lifecycle_log

## §5.3.2

- `test_s5_scope_policy_tuples` — container scope_policy tuples frozen

## §5.3.3

- `test_adversarial_scope_escalation` — scope mutation blocked at multiple layers
- `test_c_phase_regression_battery` — canonical JSON, profile freezing, strict mode, threshold Safe-Stop, REDLINE sanitization
- `test_s5_profile_immutability` — ACTIVE profile frozen; mutate_active_profile requires reason

## §5.4.1

- `test_s5_can_call_advisors` — can_call_advisors permission gates LLM invocation
- `test_phase_d_regression_battery` — UUID ingress, scope-on-permission, OATH persistence-failure visibility

## §5.5.2

- `test_s5_sigil_alignment` — eight seat sigils and reverse resolution

## §5.6

- `test_adversarial_ingress` — spoofed/None/empty container_id handled; ingress sentinel required
- `test_phase_d_regression_battery` — UUID ingress, scope-on-permission, OATH persistence-failure visibility

## §5.7

- `test_seal_extended_edges` — SEAL extended edges: rejection path, invalid review inputs, idempotent ratification, whitespace normalization
- `test_seal_ceremony_additional_proof` — SEAL ceremony: rejection-cycle re-review blocked, mixed-case verdict normalizes, amendment history ordering, ratification idempotence

## §5.7.1

- `test_adversarial_policy_confusion` — policy confusion: global vs container consent; forbidden wins at PAV; production-mode
- `test_probe_indirect_prompt_injection_stays_data_not_authority` — indirect prompt injection remains scoped data, not authority
- `test_s5_consent_scoping` — container-specific consent overrides global revocation

## §5.8.3

- `test_a1_unified_container_filter` — container filter unified across audit_log, trace_export, trace_verify
- `test_probe_container_filter_prefix_boundary` — container TRACE filter requires exact : boundary; prefix-collision hole closed
- `test_trace_export_extended_edges` — TRACE export exact-boundary container prefix filter and REDLINE sanitization in text export
- `test_trace_export_additional_proof` — TRACE export: summary integrity under filters, live/cold parity, multi-token REDLINE redaction, mixed global/container export
- `test_s5_trace_filtering` — container-scoped TRACE filtering

## §5.9.1

- `test_s5_s4_rules_in_containers` — S4 governance (REDLINE, LEDGER, purge, provenance) applies inside containers

## §6.2

- `test_persistence` — SQLite persistence basic round-trip
- `test_persistence_roundtrip` — bootstrap→save→restore integrity

## §6.3

- `test_audit_log` — TRACE envelope, chain linkage, event filtering
- `test_phase_g_demo_suite_operator_flow` — Phase G demo suite proves governed usefulness, REDLINE exclusion, consent recovery, Safe-Stop restart recovery, isolation, and cold TRACE verification

## §6.3.3

- `test_c_phase_regression_battery` — canonical JSON, profile freezing, strict mode, threshold Safe-Stop, REDLINE sanitization

## §6.3.5

- `test_s6_boot_chain_verification` — BOOT_CHAIN_VERIFIED emitted on clean boot
- `test_s6_bootstrap_event_sequence` — bootstrap event ordering: SCHEMA_VERSION_SET then BOOT_CHAIN_VERIFIED
- `test_a1_boot_verification_catches_persisted_tamper` — persisted-chain tamper caught at boot

## §6.3.6

- `test_probe_untrusted_import_hash_binding` — untrusted import receipt hash-binds source and wrapped content
- `test_s6_chain_hash_migration_scaffold` — chain-hash migration scaffold refuses silent CHAIN_HASH_VERSION drift
- `test_probe_chain_catches_duplicate_content_tamper` — hash envelope uniqueness; chain detects middle-row deletion
- `test_probe_hash_envelope_version_marker_present` — CHAIN_HASH_VERSION marker pinned at v1 for forward-compat

## §6.4.4

- `test_write_ahead_guarantee` — audit write-ahead guarantee

## §6.5

- `test_a1_historical_trace_chain_loaded_on_restart` — restart loads historical chain into memory
- `test_persistence_roundtrip` — bootstrap→save→restore integrity
- `test_f2_entry_id_stability` — entry IDs stable across restart (no re-generation)
- `test_a1_consent_persistence_roundtrip` — consent state persists and restores

## §6.6.3

- `test_f4_event_code_registry` — EVENT_CODES registry has section/category/desc for every code
- `test_f4_event_categorization` — categorize_event resolves known and unknown codes
- `test_f4_export_includes_summary` — export includes event_summary with by_section/by_category
- `test_s6_event_codes_registered` — S6 event codes registered with section/category

## §6.6.4

- `test_c_phase_regression_battery` — canonical JSON, profile freezing, strict mode, threshold Safe-Stop, REDLINE sanitization

## §6.7.3

- `test_s6_schema_version_tracking` — schema version stamped and idempotent
- `test_s6_bootstrap_event_sequence` — bootstrap event ordering: SCHEMA_VERSION_SET then BOOT_CHAIN_VERIFIED

## §6.8.3

- `test_s6_schema_migrated_event` — SCHEMA_MIGRATED event on legacy row migration
- `test_s6_chain_hash_migration_scaffold` — chain-hash migration scaffold refuses silent CHAIN_HASH_VERSION drift

## §6.9.1

- `test_s0_8_4_governed_state_bootstrap_roundtrip` — every listed governed-state category restores on bootstrap

## §6.9.2

- `test_oath_additional_proof` — OATH consent namespace normalization, persistence-failure density, malformed namespace fail-closed behavior
- `test_phase_d_regression_battery` — UUID ingress, scope-on-permission, OATH persistence-failure visibility

## §6.10

- `test_trace_export` — TRACE export format and REDLINE sanitization
- `test_f4_export_includes_summary` — export includes event_summary with by_section/by_category
- `test_a1_export_from_db_emits_chain_valid` — export_from_db reports chain_valid in output
- `test_trace_export_additional_proof` — TRACE export: summary integrity under filters, live/cold parity, multi-token REDLINE redaction, mixed global/container export

## §6.10.6

- `test_c_phase_regression_battery` — canonical JSON, profile freezing, strict mode, threshold Safe-Stop, REDLINE sanitization
- `test_trace_export_cold_container_redline_sanitization` — cold TRACE export sanitizes REDLINE artifact IDs from container hub rows as well as global rows
- `test_trace_export_extended_edges` — TRACE export exact-boundary container prefix filter and REDLINE sanitization in text export

## §6.11

- `test_adversarial_audit_tamper` — cold verifier and boot verifier catch tamper modes

## §6.11.3

- `test_scenario_tamper_recovery` — tamper → boot detection → Safe-Stop → T-0 recovery → resumed governance
- `test_s6_boot_chain_detects_tampering` — tampered chain triggers Safe-Stop at boot
- `test_a1_boot_verification_catches_persisted_tamper` — persisted-chain tamper caught at boot
- `test_probe_safe_stop_recovery_ceremony` — full operator-triggered Safe-Stop recovery ceremony with audit durability

## §6.11.4

- `test_idempotence_replay` — Safe-Stop/schema/declassify/revocation/verification are idempotent
- `test_s6_cold_verifier` — cold trace verifier: clean, tampered, missing, empty cases + Safe-Stop + filter
- `test_trace_verify_cli_error_classification` — cold verifier CLI exit codes: file-not-found returns EXIT_FILE_ERROR; schema-invalid returns EXIT_SCHEMA_INVALID
- `test_trace_verify_registry_load_failure_is_nonfatal` — cold verifier --use-registry load failure degrades to a warning; EXIT_OK still returned
- `test_trace_verify_additional_proof` — cold verifier: corrupted schema version degrades gracefully; mixed known/unknown codes reported; safe-stop state readable cold
- `test_trace_verify_human_report_branches` — cold verifier reports expose filtered broken-chain detail, unknown codes, stats, and JSON schema errors

## §7.2

- `test_s7_amendment_ceremony` — S7 propose → review → ratify ceremony, S0 sovereign override, versioning

## §7.3

- `test_s7_amendment_ceremony` — S7 propose → review → ratify ceremony, S0 sovereign override, versioning

## §7.4

- `test_s7_amendment_ceremony` — S7 propose → review → ratify ceremony, S0 sovereign override, versioning

## §E-1

- `test_adversarial_policy_confusion` — policy confusion: global vs container consent; forbidden wins at PAV; production-mode
- `test_phase_e_regression_battery` — production-mode, demo parity, auto-restore, OATH atomicity

## §E-3

- `test_phase_e_regression_battery` — production-mode, demo parity, auto-restore, OATH atomicity

## §E-4

- `test_phase_e_regression_battery` — production-mode, demo parity, auto-restore, OATH atomicity

---

**Protocol:** when a new test is added, its `# CLAIM:` tag should cite the Pact section(s) it proves and a one-line description. Every non-trivial Pact clause should have at least one claim tag pointing at it; gaps visible in this matrix become the next testing work.
