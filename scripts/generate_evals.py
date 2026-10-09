"""Write the ks-update skill's eval suite: every case under plugins/arcsite-ks-update/evals/.

Run from the repository root, then review the diff:

    python3 scripts/generate_evals.py

Each case carries its own mocks (a suite-level <tool>.md would take precedence
over a case's _server.md), so the files are many and alike; edit them here,
never by hand. Each case directory is written over whole; it leaves alone: evals/mocks/ks-test/_tools.json and evals/results/.

The answers are ks-test's own, read with read-only tools for Portland 004 on
2026-10-09 and stamped with the contract the skill is written for. When the
tools change shape, refresh both:

- the bodies below, from the same read-only calls against ks-test;
- evals/mocks/ks-test/_tools.json, the server's tools/list, from a cloudservice
  checkout of the matching contract:

      docker compose exec -T tests python manage.py shell -c \
        "import json; from arcservice.apps.manage import ks_mcp_views as v; \
        print(json.dumps({'tools': [v._tool_json(t) for t in v.TOOLS]}))"
"""

import copy
import json
import os
import shutil

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plugins", "arcsite-ks-update")
EV = os.path.join(ROOT, "evals")
ORG = "287386500977433776"
LAYER = f"org-{ORG}"
CONSOLE = "https://admin-test.arcsite.com/knowledge-studio"
CTX = "f1f9ee329769886633f32d150c244dbb9e55c8510fd525ae6619deca14a5afbc"
DIFF = "86fdfc06c731411a540a9f0ee7e90c912626db5a0061aa69264610ea859d54f0"
PLAN = "c5fed84d72a12a74f0ae131cb93a2593335a1fc477dc5166421f032eebd13be2"
ANCESTORS = [
    {"layer": "arcsite-core", "version": "0.0.1", "checksum": "b0fedf0dbaabb52f6987babbc90e27374cc503b21cb505b52a7af3411fbb0c7f"},
    {"layer": "construction-core", "version": "0.0.1", "checksum": "7e1e6c3419e0e793b30a900a195a6c0c5278f17afac979cdd0d9b2f870205847"},
    {"layer": "fence", "version": "0.0.27", "checksum": "134efca57f1f524084ed137df77ca1e182cdc429cbec0c0918ae30caa2e46872"},
    {"layer": "master-halco", "version": "0.0.45", "checksum": "d002acb6caa2a0a7d469826d933afc18d9df8248e0aaf95a6869a73774453a89"},
    {"layer": "master-halco-distribution", "version": "0.0.46", "checksum": "94d1ae9d300c3f2d6f7fd022d8915f81414e7b373f113abfa5d03d8577e9f099"},
]
BASELINE = {"authoring_checksum": "eccd393e16daa73b4f7b246f93cd081b5332161737aed1e58da88d285b9ac0cc", "ancestors": ANCESTORS}
LAYER_REF = {"stable_id": LAYER, "kind": "organization", "namespace": "org_" + ORG, "name": "Portland 004", "manufacturer_axis_stable_id": None}
BURIAL_DECLARATION = {"stable_id": "fence.burial_region", "label": "Burial Survey Region", "description": "The regional burial survey verified for this branch. Unassigned does not inherit Region 3.", "status": "active", "owner": {"stable_id": "fence", "kind": "trade", "namespace": "fence", "name": "Fence"}, "value_type": "enumeration", "unit": None, "domain": {"kind": "allowed_values", "values": ["region_3", "unassigned"]}, "override_layers": ["organization"], "terminal_layer": "organization", "editable": True, "not_editable_reason": None, "current_setting": {"layer_stable_id": LAYER, "discipline": "default", "value": "region_3", "window": None}, "effective": {"valid": True, "value": "region_3", "decided_by": LAYER}, "inherited": {"valid": True, "value": "unassigned", "decided_by": "fence"}}
CARD = {"stable_id": LAYER, "name": "Portland 004", "kind": "organization", "active_version": "0.0.46", "unpublished_changes": False, "draft_saves": None, "console_url": f"{CONSOLE}?layer={LAYER}&module=versions", "direct_companies": [{"organization_id": ORG, "name": "Portland 004"}], "downstream_companies": [], "publication_layers": []}


def stamp(body, contract="12", minimum="12"):
    head = {"environment": "ks-test", "contract_version": contract}
    if minimum is not None:
        head["min_skill_contract"] = minimum
    return json.dumps({**head, **body}, separators=(",", ":"))


BODIES = {
    "find_target": {"query": "Portland 004", "organizations": [
        {"organization_id": "287386500977433775", "name": "Portland 004", "type": "individual", "owner_email": "portland-004@mh.test", "layer": None, "own_overlay": False},
        {"organization_id": ORG, "name": "Portland 004", "type": "company", "owner_email": "portland-004@mh.test", "layer": {"stable_id": LAYER, "name": "Portland 004", "kind": "organization"}, "own_overlay": True}],
        "layers": [CARD], "layer_details": [CARD], "selected": CARD,
        "reason": "One layer matched exactly. Also matched, running no Knowledge Studio layer: Portland 004.", "more": False},
    "read_layer-overview": {"layer": LAYER_REF, "kind": "organization", "baseline": BASELINE,
        "vocabulary": {"kinds_this_layer_may_own": ["assembly", "assembly_dispatch_map", "attribute", "attribute_domain_extension", "concept", "concept_attribute_extension", "concept_synonym_extension", "dataset", "dataset_replacement", "dataset_rows_replacement", "formula", "formula_constant_override", "product_role", "product_role_constraint", "question_default_override", "question_domain_narrowing", "question_option_admission", "question_refinement_extension", "questionnaire", "rule", "rule_facet_override", "task_template", "workflow", "workflow_task_facet_override"], "rule_actions": ["add_fact", "add_workflow_task", "generate_warning", "product_constraint", "remove_component", "require_component", "set_fact"], "rule_severities": ["information", "review_required", "blocking"], "task_priorities": ["required", "recommended", "optional", "warning"], "task_skip_policies": ["not_allowed", "reason_required", "allowed"]},
        "owned_counts": {"objects": {}, "delegated_settings": 0, "layer_settings": 1},
        "layer_settings": [{"entry_stable_id": "fence.burial_region", "discipline": "default", "value": "region_3", "window_payload": None}],
        "delegated_settings": [], "unpublished": {"source_changed": False, "active_version": "0.0.46", "changes": []}, "draft_saves": None,
        "console_url": f"{CONSOLE}?layer={LAYER}&module=versions",
        "patch_frame": {"format_version": 1, "layer": LAYER_REF, "baseline": BASELINE, "objects": [], "delegated_settings": [], "layer_settings": [], "removals": []}},
    "read_layer-settings": {"layer": LAYER, "items": [BURIAL_DECLARATION], "page": 1, "pages": 1, "total": 1, "truncated": False},
    "read_layer-objects": {"layer": LAYER, "authoring_checksum": BASELINE["authoring_checksum"], "items": [], "page": 1, "pages": 1, "total": 0},
    "read_layer-schema": {"kind": "layer_setting", "schema": {"title": "Layer Setting", "type": "object", "additionalProperties": False, "required": ["entry_stable_id", "discipline", "value", "window_payload"], "properties": {"entry_stable_id": {"type": "string"}, "discipline": {"type": "string", "enum": ["default", "bounded", "locked", "constraint"]}, "value": {"type": ["string", "null"]}, "window_payload": {"type": ["object", "null"]}}}, "example": {"entry_stable_id": "fence.max_single_gate_leaf_width", "discipline": "bounded", "value": "8", "window_payload": {"kind": "numeric_range", "minimum": "4", "maximum": "10"}}},
    "read_layer-guide": {"sections": [{"title": t, "chars": 1000} for t in ["Introduction", "1. What you are editing", "2. The document, notes and touched", "3. Identities", "4. Which layer may own what", "5. You cannot edit what you inherit", "6. Deleting", "7. Status: what reaches a package and what does not", "8. Changes that span layers", "9. Reading the preview", "10. Saying what you were asked to say", "11. What this system does not do", "12. Writing your answer", "13. Before you preview"]], "hint": "Ask for one section by its number or a word of its title."},
    "read_layer-release_plan": {"layer": {"stable_id": LAYER, "name": "Portland 004", "kind": "organization"},
        "candidates": [{"organization_id": ORG, "name": "Portland 004", "binding_layer": {"stable_id": LAYER, "name": "Portland 004", "kind": "organization"}, "direct": True}],
        "target_organization_ids": [ORG], "unreachable_organization_ids": [],
        "steps": [{"order": 1, "layer": {"stable_id": LAYER, "name": "Portland 004", "kind": "organization"}, "reason": "own_changes", "active_version": "0.0.46", "next_version": "0.0.47",
            "unpublished": {"source_changed": True, "changes": [{"section": "layer_settings", "entry_stable_id": "fence.burial_region", "change": "changed"}]},
            "ships": {"records": [{"section": "layer_settings", "entry_stable_id": "fence.burial_region", "about": "Burial Survey Region", "change": "changed", "fields": [{"field": "value", "before": "region_3", "after": "unassigned"}]}], "total": 1, "more": False, "unavailable": None},
            "pins": [{"layer": "master-halco-distribution", "current": "0.0.46", "expected": "0.0.46", "in_this_release": False, "moves": False}],
            "directly_bound": [{"organization_id": ORG, "name": "Portland 004", "targeted": True}], "console_url": f"{CONSOLE}?layer={LAYER}&module=versions",
            "draft_saves": {"by": [{"name": "you", "saves": 1, "last_saved_at": "2026-10-09T13:05:12"}]}}],
        "affected_non_targets": [], "stays_on_current": [], "upstream_warnings": [], "release_organization_ids": [ORG], "plan_checksum": PLAN, "publishes_here": True,
        "console_url": f"{CONSOLE}?layer={LAYER}&module=versions&view=release&organizations={ORG}&plan={PLAN}",
        "how_to_publish": "Open console_url: the Release plan card opens with these companies ticked, the plan computed, and checked against this one. Its Plan id is the first 8 characters of plan_checksum. None of these tools publishes."},
    "read_object": {"layer": LAYER, "authoring_checksum": BASELINE["authoring_checksum"], "kind": "layer_setting", "stable_id": "fence.burial_region",
        "owned": {"entry_stable_id": "fence.burial_region", "discipline": "default", "value": "region_3", "window_payload": None},
        "inherited": [{"owner": {"stable_id": "fence", "kind": "trade", "namespace": "fence", "name": "Fence"}, "read_only": True, "record": BURIAL_DECLARATION}], "matches": 2},
    "preview": {"applicable": True, "publishable": True, "draft_layer_stable_ids": [LAYER],
        "draft_layers": [{"layer": LAYER, "authoring_checksum": BASELINE["authoring_checksum"], "candidate_checksum": "ab55c80fe61c65fb6b5c9ca33f3b31e0ad7caa4acf3561c21405d61202181c27"}],
        "context_checksum": CTX, "diff_checksum": DIFF,
        "changes": {"objects": {"added": [], "changed": [], "removed": []}, "delegated_settings": {"added": [], "changed": [], "removed": []},
            "layer_settings": {"added": [], "changed": [{"entry_stable_id": "fence.burial_region", "about": "Burial Survey Region", "fields": [{"field": "value", "before": "region_3", "after": "unassigned"}]}], "removed": []}},
        "issues": [], "notes": [], "touched": {"declared": 1, "missing": 0}, "kept_for_apply": True},
    "apply": {"applied": True, "apply_id": 15, "reapply_of": None,
        "changes": {"objects": {"added": 0, "changed": 0, "removed": 0}, "delegated_settings": {"added": 0, "changed": 0, "removed": 0}, "layer_settings": {"added": 0, "changed": 1, "removed": 0}},
        "publishable": True, "baseline": {"authoring_checksum": "3b1e0c57a0f4d6e2b9a8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6", "ancestors": ANCESTORS},
        "notes": [], "touched": {"declared": 1, "missing": 0}, "undo": "ks_applies with this apply_id returns the undo document",
        "console_url": f"{CONSOLE}?layer={LAYER}&module=versions", "recent_applies_url": f"{CONSOLE}?layer={LAYER}&module=agent", "published": False},
    "replay_results-status": {"layer": LAYER, "mode": "release", "target_organization_ids": [ORG],
        "reads": {"companies": [{"organization_id": ORG, "name": "Portland 004", "layers": [{"layer": LAYER, "reads": "draft"}, {"layer": "master-halco-distribution", "reads": "0.0.46"}, {"layer": "master-halco", "reads": "0.0.45"}, {"layer": "fence", "reads": "0.0.27"}]}]},
        "cases": [{"case_id": 31, "name": "Portland chain link, 210 ft run", "company": {"organization_id": ORG, "name": "Portland 004"}, "status": "unchanged", "matches_current_fingerprint": True, "release_run": {"status": "succeeded", "error": None}}],
        "companies_without_cases": [], "release_organization_ids": [ORG],
        "console_url": f"{CONSOLE}?layer={LAYER}&module=versions&view=release&organizations={ORG}", "waited_seconds": 6},
    "replay_results-case_diff": {"case_id": 31, "status": "unchanged", "summary": {"components": 0, "skus": 0, "form": 0}, "components": [], "skus": [], "form": {"form_compared": True, "questions": [], "readiness": []}},
    "replay_results-case_inputs": {"case_id": 31, "trade": "fence", "context": {"fence.attribute.material_system": "chain_link"},
        "answers": {"fence.attribute.segment": "residential", "fence.attribute.fence_height_in": "48", "fence.attribute.mesh_gauge": "9", "fence.attribute.product_color": "black"},
        "instances": [{"instance_id": "run-1", "role": "fence_run", "inputs": {"fence.attribute.run_length_ft": "210"}}, {"instance_id": "corner-1", "role": "corner_post", "inputs": {}}]},
    "resolve": {"company": {"organization_id": ORG, "name": "Portland 004"}, "trade": "fence", "layers": "drafts", "previewed": {"layer": LAYER, "diff_checksum": DIFF}, "effective_on": "2026-10-09",
        "summary": {"instances": 2, "distinct_instances": 2, "components_by_status": {"matched": 9}, "skus": 9}, "required_missing": [],
        "skus": [{"sku": "001842", "name": "2-3/8 in x 8 ft terminal post", "demand_quantity": "1", "demand_unit": "each", "order_quantity": "1", "order_unit": "each"}],
        "instances": []},
    "applies": {"layer": LAYER, "applies": [
        {"id": 14, "at": "2026-09-29T09:40:37", "by": "arcadmin", "diff_checksum": "46830135a9a84593fa0049d09f70f0e4dc5f2774c185e6d997e35573bb297cbb", "undo": {"state": "rebasable", "conflicts": [], "conflicts_more": 0}},
        {"id": 13, "at": "2026-09-29T09:34:41", "by": "arcadmin", "diff_checksum": "93cac1e97d9d0ae15d889d9d4bdf425e04d8075175e48d5985ca0f298b106c68", "undo": {"state": "not_kept", "conflicts": [], "conflicts_more": 0}}]},
    "read_catalog": {"catalog": {"organization_id": ORG, "name": "Portland 004", "shares_enterprise_library": True},
        "summary": {"scope": "library", "shares_a_library": True, "company_products": 2391, "products": 18180, "tagged": 16997, "untagged": 1183, "selling_unstated": 0, "attributes_unstated": 5,
            "by_role": {"fence.concept.chain_link.line_post": 3475, "fence.concept.chain_link.terminal_post": 3254, "fence.concept.chain_link.fabric": 2915}},
        "tagging_runs": [], "waited_seconds": 0, "console_url": "https://admin-test.arcsite.com/product-catalog?enterprise=37"},
}
BODIES["replay"] = {"layer": LAYER, "mode": "release", "claimed": [31], "recovered": [], "skipped": [], "status": BODIES["replay_results-status"]}
LANDED = {**BODIES["applies"], "applies": [{"id": 15, "at": "2026-10-09T13:05:12", "by": "you", "diff_checksum": DIFF, "undo": {"state": "current", "conflicts": [], "conflicts_more": 0}}] + BODIES["applies"]["applies"]}


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text if text.endswith("\n") else text + "\n")


def mocks(base, contract="12", minimum="12", only=None, overrides=None, exclude=()):
    """One server's mocks: fixed bodies, and fixtures for the tools keyed by an input."""
    server = os.path.join(base, "ks-test")
    bodies = {**BODIES, **(overrides or {})}
    for name, body in bodies.items():
        if "-" in name:
            if (only is None or name.split("-")[0] in only) and name.split("-")[0] not in exclude:
                write(os.path.join(server, "fixtures", name + ".json"), stamp(body, contract, minimum))
    fixed = {
        "find_target": "", "read_object": "", "preview": "---\nexpect:\n  layer_stable_id: " + LAYER + "\n---\n\n",
        "apply": "---\nexpect:\n  layer_stable_id: " + LAYER + "\n  context_checksum: \"" + CTX + "\"\n  diff_checksum: \"" + DIFF + "\"\n---\n\n",
        "replay": "", "applies": "", "read_catalog": "",
    }
    for tool, head in fixed.items():
        if (only is None or tool in only) and tool not in exclude:
            write(os.path.join(server, f"ks_{tool}.md"), head + stamp(bodies[tool], contract, minimum))
    if (only is None or "read_layer" in only) and "read_layer" not in exclude:
        write(os.path.join(server, "ks_read_layer.md"), "{{file:fixtures/read_layer-{input.part}.json}}")
    if (only is None or "replay_results" in only) and "replay_results" not in exclude:
        write(os.path.join(server, "ks_replay_results.md"), "{{file:fixtures/replay_results-{input.action}.json}}")


def case(name, prompt, graders, *, max_turns=20, tools=("Read", "Skill"), runs=1, case_mocks=None, description="", world=None):
    base = os.path.join(EV, name)
    shutil.rmtree(base, ignore_errors=True)
    WRITTEN.append(name)
    head = ["---", f"description: {json.dumps(description)}", f"runs: {runs}", f"max_turns: {max_turns}", "timeout_seconds: 900", f"allowed_tools: [{', '.join(tools)}]", "---", ""]
    write(os.path.join(base, "prompt.md"), "\n".join(head) + prompt.strip())
    for grader, (front, body) in graders.items():
        lines = ["---"] + [f"{k}: {v}" for k, v in front.items()] + ["---", ""]
        write(os.path.join(base, "graders", grader + ".md"), "\n".join(lines) + (body.strip() if body else ""))
    # Each case carries its whole world: a suite-level <tool>.md would take
    # precedence over a case's _server.md, so nothing per tool lives up there.
    mocks(os.path.join(base, "mocks"), **(world or {}))
    if case_mocks:
        case_mocks(os.path.join(base, "mocks"))


def never(tool):
    return ({"type": "tool_used", "tool": f"mcp__plugin_arcsite-ks-update_ks-test__{tool}", "min": 0, "max": 0, "arm": "both"}, None)


def used(tool, input_match=None, lo=1, hi=None):
    front = {"type": "tool_used", "tool": f"mcp__plugin_arcsite-ks-update_ks-test__{tool}"}
    if input_match:
        front["input_match"] = "'" + input_match + "'"
    front["min"] = lo
    if hi is not None:
        front["max"] = hi
    return (front, None)


def order(before, after):
    return ({"type": "tool_order", "before": f"mcp__plugin_arcsite-ks-update_ks-test__{before}", "after": f"mcp__plugin_arcsite-ks-update_ks-test__{after}"}, None)


SKILL = ({"type": "tool_used", "tool": "Skill", "input_match": "'\"skill\"\\s*:\\s*\"(?:[\\w-]+:)?ks-update\"'"}, None)


def judge(text):
    return ({"type": "llm"}, text)


# Suite-wide mocks and the saved tools/list.
WRITTEN = []
assert os.path.exists(os.path.join(EV, "mocks", "ks-test", "_tools.json")), "evals/mocks/ks-test/_tools.json is refreshed separately"
write(os.path.join(EV, ".gitignore"), "results/")

ANALYSE = "What burial survey region does Portland 004 use for its fence jobs right now, and where does that value come from? Don't change anything."
SAVE = "For Portland 004 only, set the burial survey region back from Region 3 to unassigned, and save the draft. Check it against their saved orders."

case("analyse-only", ANALYSE, {
    "skill-fired": SKILL, "no-apply": never("ks_apply"), "no-replay": never("ks_replay"),
    "answer": judge("PASS if the reply says Portland 004 uses region_3 (Region 3), set by Portland 004's own Organization Overlay over the Fence Trade's default of unassigned.\nFAIL if it says it changed or saved anything, or gives a different value or source."),
}, description="A question about what is there is answered by reading, never by writing or running Replay.")

case("save-draft", SAVE, {
    "skill-fired": SKILL,
    "find-before-preview": order("ks_find_target", "ks_preview"),
    "preview-before-apply": order("ks_preview", "ks_apply"),
    "applied-once": used("ks_apply", DIFF[:16], 1, 1),
    "apply-without-document": used("ks_apply", '"document"', 0, 0),
    "replay-after-apply": order("ks_apply", "ks_replay"),
    "release-replay": used("ks_replay", "release_organization_ids", 1),
    "handover": judge("PASS if the final reply says the change is saved as a draft and not published, gives a Console link containing view=release, names the Plan id c5fed84d, and reports Replay for Portland 004 as unchanged.\nFAIL if it says it published, gives no Console link, or leaves out the Replay result."),
}, max_turns=45, description="Change, preview, apply by checksum, Replay the release, hand over with the plan id.")

case("contract-plugin-too-old", SAVE, {
    "no-preview": never("ks_preview"), "no-apply": never("ks_apply"),
    "answer": judge("PASS if the reply stops before changing anything and tells the person to update the plugin (for example `claude plugin update arcsite-ks-update@arcsite`, then start a new session).\nFAIL if it carries on with the change, or says the server is out of date instead."),
}, world={"contract": "13", "minimum": "13"},
    description="The server needs a newer skill than this one: stop and ask for a plugin update.")

case("contract-server-behind", SAVE, {
    "no-preview": never("ks_preview"), "no-apply": never("ks_apply"),
    "answer": judge("PASS if the reply stops before changing anything and says the ks-test server has not been updated to what this plugin needs.\nFAIL if it carries on with the change, or tells the person to update the plugin."),
}, world={"contract": "11", "minimum": None},
    description="The skill is newer than the server: stop and say the server is behind.")

case("contract-newer-server", ANALYSE, {
    "went-on": used("ks_read_layer"),
    "answer": judge("PASS if the reply answers that Portland 004 uses region_3, set by its own Overlay, and mentions that a newer version of the plugin is available.\nFAIL if it refuses to go on, or does not mention the newer plugin."),
}, world={"contract": "13", "minimum": "12"},
    description="A server that only added things since this skill keeps working, with a note about the newer plugin.")

case("catalog-reads-reference", "How many products in Portland 004's catalog have no Role yet, and whose library is that?", {
    "read-reference": ({"type": "tool_used", "tool": "Read", "input_match": "'references/catalog\\.md'"}, None),
    "read-catalog": used("ks_read_catalog"),
    "answer": judge("PASS if the reply says 1,183 Products have no Role and that Portland 004 shares its Enterprise's library (18,180 Products).\nFAIL if either number is missing or wrong."),
}, description="Catalog work loads the catalog reference before answering.")

case("new-manufacturer-asks-first", "I've got price lists and spec sheets from a new manufacturer. Set them up in Knowledge Studio.", {
    "skill-fired": SKILL,
    "no-ks-calls": ({"type": "regex", "target": "mock_calls", "pattern": "ks_", "match": "not_contains", "arm": "both"}, None),
    "asks": judge("PASS if the reply, before doing anything, asks which manufacturer, which Trade, whether its layer is new or already exists, and which company will quote on it.\nFAIL if it starts reading, creating or importing anything, or asks none of these."),
}, description="A new manufacturer starts with questions, not tool calls.")

LOST = ("Earlier today you saved a draft on Portland 004's overlay: the burial survey region back to unassigned "
        f"(preview context_checksum {CTX}, diff_checksum {DIFF}). The connection dropped before the apply answered. "
        "Make sure that change is saved, exactly once.")
case("lost-answer-landed", LOST, {
    "checked-ledger": used("ks_applies"), "no-apply": never("ks_apply"),
    "answer": judge("PASS if the reply says the change already landed (apply 15) and that it did not apply it again.\nFAIL if it applies the change again, or says it is unsure without having checked."),
}, world={"overrides": {"applies": LANDED}},
    description="A lost answer is checked against the ledger; a change that landed is not sent again.")

document = {"format_version": 1, "layer": LAYER_REF, "baseline": BASELINE, "objects": [], "delegated_settings": [],
            "layer_settings": [{"entry_stable_id": "fence.burial_region", "discipline": "default", "value": "unassigned", "window_payload": None}],
            "removals": [], "touched": [{"type": "layer_setting", "entry_stable_id": "fence.burial_region"}]}
case("lost-answer-not-landed", LOST + "\n\nThe document was:\n\n```json\n" + json.dumps(document, indent=2) + "\n```", {
    "ledger-first": order("ks_applies", "ks_preview"),
    "preview-before-apply": order("ks_preview", "ks_apply"),
    "applied-once": used("ks_apply", DIFF[:16], 1, 1),
}, max_turns=25, description="A change that did not land is previewed again and applied once, with the same checksums.")


# --- save-draft: one agent answers every tool whose answer an apply changes,
# ks_apply included, so the apply is in the history it answers from.
AFTER_CHECKSUM = BODIES["apply"]["baseline"]["authoring_checksum"]
AFTER_BASELINE = {"authoring_checksum": AFTER_CHECKSUM, "ancestors": ANCESTORS}
AFTER_SETTING = {"entry_stable_id": "fence.burial_region", "discipline": "default", "value": "unassigned", "window_payload": None}
overview_after = copy.deepcopy(BODIES["read_layer-overview"])
overview_after["baseline"] = AFTER_BASELINE
overview_after["patch_frame"]["baseline"] = AFTER_BASELINE
overview_after["layer_settings"] = [AFTER_SETTING]
overview_after["unpublished"] = {"source_changed": True, "active_version": "0.0.46", "changes": [{"section": "layer_settings", "entry_stable_id": "fence.burial_region", "change": "changed", "fields": [{"field": "value", "before": "region_3", "after": "unassigned"}]}]}
overview_after["draft_saves"] = {"since_published_at": "2026-10-08T10:12:00", "last_saved_at": "2026-10-09T13:05:12", "by": [{"name": "you", "saves": 1, "last_saved_at": "2026-10-09T13:05:12"}]}
settings_after = copy.deepcopy(BODIES["read_layer-settings"])
settings_after["items"][0]["current_setting"]["value"] = "unassigned"
settings_after["items"][0]["effective"]["value"] = "unassigned"
object_after = copy.deepcopy(BODIES["read_object"])
object_after["owned"] = AFTER_SETTING
object_after["authoring_checksum"] = AFTER_CHECKSUM
SKUS = [
    {"sku": "001842", "name": "2-3/8 in x 8 ft terminal post", "demand_quantity": "1", "demand_unit": "each", "order_quantity": "1", "order_unit": "each"},
    {"sku": "004893", "name": "1-5/8 in x 7 ft line post", "demand_quantity": "21", "demand_unit": "each", "order_quantity": "21", "order_unit": "each"},
    {"sku": "087139", "name": "48 in 9 ga black chain link fabric, 50 ft roll", "demand_quantity": "210", "demand_unit": "ft", "order_quantity": "5", "order_unit": "roll"},
]
INSTANCES = [
    {"instance_ids": ["run-1"], "role": "fence_run", "readiness": "ready", "warnings": [], "required_missing": [], "components": [
        {"status": "matched", "quantity": "21", "sku": "004893", "name": "1-5/8 in x 7 ft line post"},
        {"status": "matched", "quantity": "210", "sku": "087139", "name": "48 in 9 ga black chain link fabric, 50 ft roll"}]},
    {"instance_ids": ["corner-1"], "role": "corner_post", "readiness": "ready", "warnings": [], "required_missing": [], "components": [
        {"status": "matched", "quantity": "1", "sku": "001842", "name": "2-3/8 in x 8 ft terminal post"}]},
]


def resolved(layers, previewed):
    return {"company": {"organization_id": ORG, "name": "Portland 004"}, "trade": "fence", "layers": layers,
            "previewed": previewed, "effective_on": "2026-10-09",
            "summary": {"instances": 2, "distinct_instances": 2, "components_by_status": {"matched": 3}, "skus": 3},
            "required_missing": [], "skus": SKUS, "instances": INSTANCES}


def save_draft_server(base):
    documents = {
        "OVERVIEW_BEFORE": BODIES["read_layer-overview"], "OVERVIEW_AFTER": overview_after,
        "SETTINGS_BEFORE": BODIES["read_layer-settings"], "SETTINGS_AFTER": settings_after,
        "RELEASE_PLAN": BODIES["read_layer-release_plan"], "OBJECTS": BODIES["read_layer-objects"],
        "SCHEMA": BODIES["read_layer-schema"], "GUIDE": BODIES["read_layer-guide"],
        "OBJECT_BEFORE": BODIES["read_object"], "OBJECT_AFTER": object_after,
        "APPLIES_BEFORE": BODIES["applies"], "APPLIES_AFTER": LANDED,
        "APPLY": BODIES["apply"],
        "RESOLVE_PUBLISHED": resolved("published", None),
        "RESOLVE_DRAFTS": resolved("drafts", None),
        "RESOLVE_PREVIEWED": resolved("drafts", {"layer": LAYER, "diff_checksum": DIFF}),
    }
    lines = ["---", "type: agent", "tools: [ks_read_layer, ks_read_object, ks_applies, ks_apply, ks_resolve]", "---", "",
             "You are the ks-test Knowledge Studio server. Answer each call with exactly one of the JSON documents below, copied verbatim, with nothing before or after it.",
             "",
             "The layer has two states. It is BEFORE until you have answered a `ks_apply` call in this run; from then on it is AFTER.",
             "",
             "- `ks_apply`: always APPLY.",
             "- `ks_read_layer`, by `part`: overview → OVERVIEW_BEFORE or OVERVIEW_AFTER; settings → SETTINGS_BEFORE or SETTINGS_AFTER; release_plan → RELEASE_PLAN; objects → OBJECTS; schema → SCHEMA; guide → GUIDE.",
             "- `ks_read_object`: OBJECT_BEFORE or OBJECT_AFTER.",
             "- `ks_applies`: APPLIES_BEFORE or APPLIES_AFTER.",
             "- `ks_resolve`: with `previewed` → RESOLVE_PREVIEWED; `layers: drafts` without `previewed` → RESOLVE_DRAFTS; otherwise RESOLVE_PUBLISHED. The burial region does not change this job, so all three list the same parts.",
             ""]
    for name, body in documents.items():
        lines += [f"{name}:", "", "```json", stamp(body), "```", ""]
    write(os.path.join(base, "ks-test", "_server.md"), "\n".join(lines))


for applying in ("save-draft", "lost-answer-not-landed"):
    SAVE_DIR = os.path.join(EV, applying, "mocks")
    for tool in ("ks_read_layer", "ks_read_object", "ks_applies", "ks_apply"):
        os.remove(os.path.join(SAVE_DIR, "ks-test", tool + ".md"))
    shutil.rmtree(os.path.join(SAVE_DIR, "ks-test", "fixtures"))
    os.makedirs(os.path.join(SAVE_DIR, "ks-test", "fixtures"))
    mocks(SAVE_DIR, only={"replay_results"})
    save_draft_server(SAVE_DIR)
print("wrote", len(WRITTEN), "cases under", os.path.relpath(EV))
