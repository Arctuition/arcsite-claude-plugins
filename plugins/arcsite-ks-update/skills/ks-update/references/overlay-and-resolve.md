# A company's own Overlay, binding, and what a job comes to

Section numbers are the skill's (SKILL.md).

## A company's own Overlay, and binding

Only when the person asked, or said yes to your offer in section 1.

1. `ks_create_layer` with `kind: organization`, `name`: the company's name,
   `stable_id`: `org-<organization_id>`, and `parent_layer_stable_id`: the
   layer the company runs now (its `layer` in `ks_find_target`). It is created
   with an empty version `0.0.0` already published (`active_version`), so it
   reads exactly what its parent reads, and it runs for nobody until a company
   is bound to it. A new Manufacturer or Enterprise Overlay is the same call
   with that `kind` and a parent of a kind it may stand on. A parent that has
   never published is refused: its publishing goes to the Console first.
2. `ks_bind_company` with the new layer and the company. It moves the
   company off `previous_layer` at once, and the company quotes on the new
   layer straight away; on an Organization Overlay made on the layer it ran,
   exactly as before. Do not publish it first. Only a layer made before layers
   were created this way can come back with a `warning`: the company cannot
   quote, and its catalog cannot be AI-tagged, until that layer is published,
   so hand over its release plan (sections 7 and 8).
3. Then write the company's change on its new layer (sections 2–6). Importing
   and AI-tagging its catalog (Roles and Attributes saved only in the draft
   included), `ks_resolve` with `layers: drafts` and Replay all work before
   anything more is published; the change reaches quotes when the person
   publishes it in the Console (by default the first publish is `0.0.1`).

Say in the summary which layer the company ran before and that it now runs
the new one.

## What a job comes to

`ks_resolve` runs one job for a company and returns what it would buy, with
nothing saved: `organization_id`, `trade` (the Trade layer, such as `fence`),
`context` (what picks the questionnaire, such as the material system),
`answers` and `instances` — one entry per thing on the drawing, each with
its `role` and its own `inputs` (a run's length, a gate's opening and type).
Seven end posts are seven entries; there is no count. Give each its own
`instance_id` (`post-1` … `post-7`) or leave them all out; two under one id
are refused. Keys are the full Fact and Attribute stable_ids the job is asked
in (`fence.attribute.segment`, not `segment`; a key the form does not ask is
refused as `unknown_answers`, naming it in `data.references`), so start from
a real order: read a
saved case with `ks_replay_results` `action: case_inputs` and change only what
differs. `layers: drafts` reads every layer's current draft, other people's
included (say so); the default reads what is published.

It reads the whole Enterprise library ranked the way the engine ranks it —
the same run a Replay case of the job makes — never one branch's shelf or
stock, so compare it with the prototype on All branches. The result has
`skus` (demand and order quantity with units, the by-SKU table), and per
instance its `components` (status, quantity, the `sku` and `name` it defaults
to, `missing_facts` while `pending_facts`), `warnings` and `required_missing`;
instances that came out the same are one entry listing their `instance_ids`.
A refusal that answers were taken away lists them in `data`. Each call takes
as long as a resolve in the prototype, often 20 seconds or more: run the jobs
you need, not variations for their own sake.

**A change not saved yet.** With `layers: drafts`, `previewed` takes the
`layer_stable_id`, `context_checksum` and `diff_checksum` of an applicable
`ks_preview` from the last 24 hours: the job reads that layer as the patch
would leave it, with nothing written, and the answer names it under
`previewed`. Use it to try a change on real jobs before applying it, and to
compare: the same job without `previewed` is what the drafts give today.
`candidate_needs_drafts` means `layers` was not `drafts`; `preview_not_kept`
means preview again; `candidate_outside_stack` means this company does not
read that layer.

Saving a job as a Replay case is not yours: a person does it in the prototype
(Duplicate the job, change it, Save as test case). Say which job is worth
keeping and why.
