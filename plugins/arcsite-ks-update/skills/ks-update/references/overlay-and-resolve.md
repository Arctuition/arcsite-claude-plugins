# A company's own Overlay, binding, and what a job comes to

Section numbers are the skill's (SKILL.md).

## A company's own Overlay, and binding

Only when the person asked, or said yes to your offer in section 1.

1. `ks_create_layer` with `kind: organization`, `name`: the company's name,
   `stable_id`: `org-<organization_id>`, and `parent_layer_stable_ids`: the
   layer the company runs now (its `layer` in `ks_find_target`), plus any other
   Manufacturer layer the person says the company also buys from. It is
   created with an empty version `0.0.0` already published (`active_version`),
   so it reads exactly what its parents read, and it runs for nobody until a
   company is bound to it. A new Manufacturer or Enterprise Overlay is the same
   call with that `kind` and parents of a kind it may stand on; a Manufacturer
   stands on one Trade. A parent that has never published is refused: its
   publishing goes to the Console first.
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

## What a layer stands on

Only when the person asked: a company that also buys from another
Manufacturer, or an Enterprise taking on a brand its branches sell.
`ks_set_layer_parents` with the Enterprise or Organization layer and the
**whole** set it stands on afterwards (`parent_layer_stable_ids`), the parents
it keeps included: one left out is removed. Start from `stands_on` in the
layer's `ks_read_layer` overview, its present parents; the baseline's
`ancestors` are its whole closure, Cores included, and are not what this
takes. A Manufacturer layer's parents cannot change.

It is a draft change, like a saved patch: `next` says so, and `companies`
names who it reaches. Nobody's quotes move until the layer is published in the
Console, so hand over its release plan (sections 7 and 8). Until then a
company on it is not offered a Trade the new parent brings, and
`ks_resolve` with `layers: drafts` still reads the old parents. The authoring
side moves at once: the next `ks_read_layer` overview lists the new parent's
vocabulary, and patches can be written against it. Two refusals to report as
they come: a set the stack cannot hold (wrong kind of parent, no Trade
reached), and a set the layer's own records would stop compiling on, with the
records named.

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

**A job you write yourself** (from a description, a quote or a drawing, with
no saved case to copy) answers every Question the form asks it, not only the
required ones. The prototype opens each Question at its default and sends it;
`ks_resolve` takes only what you give it, and a Question left out is
unanswered, not defaulted: the knowledge that reads it does not apply, and
nothing in the result says so. A vinyl job of prebuilt panels sent without
its panel model is matched to posts of any model, every part still
`resolved`. So before the first run:

1. Read the questionnaire the context selects (`ks_read_layer` `part:
   objects`, `kind: questionnaire`, on the company's layer; the one whose
   `applies_when` the context meets), and in one `ks_read_object` call with
   `records`, the `question_default_override` of each of its Questions'
   attributes (a layer above the company may pre-select another value).
2. For each Question whose `ask_when` holds on the answers so far, send the
   person's answer; else its default: a `defaults` entry whose `when` holds
   (the questionnaire's and every override's count), else an override's
   `default_value`, else the questionnaire's own. A Question with no default
   and no answer: ask, or say it was left out.
3. Say in the summary which answers were defaults. A result with
   `required_missing` is not a finished job: answer those and run it again
   before reading what it buys.

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
