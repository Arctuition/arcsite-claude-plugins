# Reading a release Replay, and handing it over

Read this before reporting Replay results (section 7 of the skill) and before
writing the publish impact (section 8).

## What a release run reads

It runs the orders of every company the release moves — targeted or not — each
against the stack the release leaves in force. Release layers are read as
drafts; every other layer as the release leaves it: a release layer's direct
dependencies at their active version, and above those through the versions
their packages pin — not every layer at its active version.

A case that owes a baseline is not run against the release: `ks_replay` lists
it under `recovered` and runs its baseline instead (`skipped` when it could not
be queued: a run is already going, or its baseline failed), and `status` shows
`baseline_pending` until the baseline lands. A case that shows `not_run` has no
run of this release yet: call `ks_replay` again with the same ids and keep
waiting. Report `baseline_failed` as it is.

## Reading the results

A release run's result is the release's effect on those orders: it reads no
draft outside the release (another person's unpublished Trade edit is not in
it), so there is nothing to discount. `status` lists, per company, the
version of every layer a run of its cases would read now (`reads.companies`).
That is the current plan, worked out when you ask, not a record of what any
run read — no run records its versions. `matches_current_fingerprint: true`
(status `unchanged` or `changed`) says the fingerprint the run took when it
started equals today's: the sign its result belongs to this plan, not proof of
what it read. Give the plan in the summary for those cases as the plan their
results belong to; for any other case it is only what the next run will read.
`outdated` means the stack the run read has changed since: a draft in the
release was edited, or an upstream the release pins published a new version;
or the baseline it compared against is no longer the one in force (the
company's layer published or rolled back). A publish above that this release
does not read does not count. Run it again before handing over. A run that
fails because the release needs something only an unpublished layer outside it
holds is a publish that would fail too: name that layer (the plan's
`upstream_warnings`) and stop.

Report by company; say "no coverage" for `companies_without_cases`; show
failures, pending baselines and skipped cases as they are — never "all
passed". No difference does not prove the change is right. `ks_replay`
without `release_organization_ids` runs against every layer's draft; use it
only when asked to check the drafts as they stand, and then say its result
includes drafts the release would not publish.

`case_diff` lists only what moved. Components that changed the same way
are one row naming all their `instance_ids` (fourteen gates that lost the same
latch are one row). A case showing no difference on a
component does not mean the case lacks it — after an undo or a revert, back to
the baseline is the expected result. `catalog_changed: true` means both runs
read the same knowledge and still answered differently, so the difference is
not your patch: usually the Product catalog moved, but a deploy between the
two runs does the same. Report it as not this task's and say it is one of
those two; `catalog_changed: false` says nothing about where a difference
came from. A Slot that
went to `pending_facts` names what it waits on in `missing_facts`: check
whether your patch touched those facts before saying the change is or is not
yours. A case that failed with `answers_out_of_date` (or
`instance_answers_out_of_date`, for one instance's inputs) lists the
`removed_answers` in its `release_run.error` in `status`; `case_diff` shows
the order's `answers`. If your patch narrowed one of those questions, a real
order chose a value you took away: that is your change's effect — report it
and ask.

Replay compares components, SKUs and the form: each Question's wording,
visibility, required flag, options and default, readiness, and the warnings
Rules raise (name, severity, explanation). `case_diff` lists those under
`form`; `form_compared: false` means that case's baseline predates the form
check, so its form was not compared — the next run re-baselines it. A change
that moves none of these — a Workflow task — leaves every case unchanged, and
so does a Rule whose condition no saved order meets. Mark that request line
**not verified by Replay**, and say what would confirm it: a job where the
Rule's condition holds (or the task applies). You can run that yourself with
`ks_resolve` `layers: drafts` (`references/overlay-and-resolve.md`; with `previewed`, before
saving) and check its `warnings`; say
which job you ran.

## The publish impact

Publishing is the person's click; knowing what it does is your job. Before
handing over, work the release plan (section 7, step 1) into a **publish
impact** the person can act on without opening anything:

- **What ships, layer by layer.** Each `own_changes` step's `ships.records` is
  everything that layer's package will carry that its active package does
  not, whoever wrote it — measured as this release builds it, on the versions
  it pins above. So a value the layer holds for a Setting only this release
  declares upstream ships here too, and a value whose declaration this
  release withdraws upstream is listed as removed. Mark each record
  as this task's (you touched it) or not. For each one that is not, say what
  it changes (its `fields`, before → after) and that it ships with this
  release; if `ships.more` is true, say how many more there are (`ships.total`
  counts them all) and point to that layer's Versions module. Someone else's
  edit shipping is a decision for the person — ask if it looks unfinished or
  unrelated. `repin` steps ship nothing of their own. A step with
  `ships.unavailable` has a draft that cannot be built, and the publish would
  refuse for that reason: report it and stop.
- **Who moves, and what reaches them.** Every company the release moves:
  the targets, and `affected_non_targets` (bound to a layer this release
  publishes, moved whether ticked or not). For each, which of this release's changes it reads
  — the ones on layers above it in the plan. If the person does not accept a
  non-targeted company moving, stop and hand it back to them — you cannot keep
  that company on the old version.
- **Who does not move.** Each `stays_on_current` entry is a layer this release
  does not publish (`layer`), the versions it keeps (`keeps`), and the
  companies that read through it (`organizations`). Those companies are not
  out of reach: they read a changed layer through that one, stay on the old
  version for now, and get the change the next time that layer publishes,
  whoever publishes it and for whatever reason. Name each company with the
  layer it waits on, say that, and ask whether it should get the change now
  (tick it in the Release plan card) or is meant to stay as it is — in which
  case the change it would pick up later needs a decision of its own.
- **Real orders.** The release Replay (section 7), by company.
- **Not verified by Replay**, and how to check each.
- **Upstream.** `upstream_warnings`: `upstream_source_drift` is a layer above
  with unpublished content this release does not include — say whether the
  change depends on it; `upstream_pin_drift` is a layer above that still pins
  older packages (`pinned_requires` against `requires`) and needs publishing
  again, even with nothing of its own, before this layer reads the newer ones
  through it.

With several layers changed, use the release plan of the highest of them, with
every target company. Each layer you changed must be one of its steps with
`own_changes`. If one is not (it is not below that layer, or no chosen company
reads it), get that layer's release plan too, give its impact as well, and give
both links: each publishes in one go, but they are two releases.

**Release note.** Write one in English for the Release plan card's Release
note field, ready to paste: a line per layer that changes, saying what changed
and for whom (for example "Master Halco: residential top rail defaults to
1-5/8 in, as Master Halco confirmed"), then "Also ships: …" for records that
ship but were not this task's. Say the person can edit it.

Publishing is done in the Console, in one go. The release plan's
`console_url` opens the changed layer's Release plan card with these companies
already ticked and the plan computed, and it carries `plan_checksum`: the card
compares its own plan with yours and says whether it is the plan you handed
over. Its **Plan id** is the first 8 characters of `plan_checksum`. The person
checks the steps match your summary, reads What ships and the Release Replay
there, pastes the release note, and publishes every step at once. If the card
says it is not the plan you handed over, someone changed something after you
read it: ask them to come back so you read the release plan again and
summarise it anew; publishing stays held until they confirm they reviewed the
new plan. If the plan changes while they are reviewing, the
publish is refused and the card shows the new plan and what moved; nothing
ships that nobody reviewed. Give that link; don't tell them to publish layer by
layer.
