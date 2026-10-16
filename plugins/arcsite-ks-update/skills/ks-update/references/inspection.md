# An inspection trade: intake, drawings, several sources

Foundation Repair and Pest Control stand on Inspection Core. A job there is an
inspection the crew runs in the ArcSite app — intake questions, drawings,
things on the drawings, a checklist — not an order the trade intake resolves.
The tools and the patch are the same; what the knowledge says is different in
the ways below. Before writing any of them, read guide section 10's rows for
the phrases quoted here and `part: schema` for `attribute`, `rule` and
`workflow`: the shapes are there, not here.

## Where an answer is given

- "Ask the homeowner before anyone goes on site" → a Workflow with
  `stage: intake`: one Task per question, every Task about the whole job (no
  `subject_concept_stable_id`). `on_site` is the default, and the only stage
  that counts towards whether a job got an inspection at all.
- A Fact a Concept carries is answered on things of that kind — a crack's
  width on the crack, a foundation's type on its drawing. A Fact no Concept
  carries is answered on the job. A job-level Task must not collect a Fact a
  Concept carries, and a thing never inherits such a Fact from above; the
  inspection app lists either as a content issue. What is drawn and what goes
  on a drawing is read off the `located_on` relationship.
- "Once movement is found, ask again how it has progressed" → `prompt_when` on
  the Task that already asks it, never a second Task collecting the same Fact.
- "Is any reading on this drawing significant", "was a prior pier found
  anywhere" → an Attribute with a `rollup` (Project yes/no only). For a record
  rather than a measurement, add `absence_confirmed_when`: only once somebody
  looked is "none here" false. A rollup is missing until the things under it
  have decided; "nothing significant yet" is never "level".
- A Rule reads one value per Fact in each scope: never combine a thing's own
  Fact with one it inherits in a single Rule. One judgment per Fact.

## Several sources answer one question

"The homeowner says nothing was repaired, the crew found old piers" has two
shapes, and which one is the trade's call: ask if you were not told (guide
section 10, "the sources disagree").

- **The same question, answered by each source, and agreement is what
  counts** → give the Attribute `accepts_observations: true` (a Project yes/no
  or single choice; the app sends one observation per source, a value or
  "does not know"), and take any "not sure" value out of its list: not knowing
  is said by the source, not chosen. Only a Rule's condition may read such an
  Attribute — a Formula, Dataset, Slot, trigger or form condition reading it is
  refused at preview; anywhere else, read a Rule's conclusion. Each Rule
  reading it says what to do when every source said it does not know
  (`when_unknown`: skip / fire / block; left out, it follows `when_missing`)
  and when the sources disagree (`when_conflicting`: `skip` acts only when
  every source's answer would, `fire` when any source's would, `block` — the
  default — stops the inspection, Not Ready, until somebody checks). A
  disagreement reaches a Rule only when it would change that Rule's outcome.
- **One source wins, or the sources answer different questions** → one Fact
  per source, and Rules that say which wins (precedence, cautious or escalate,
  all in guide section 10). No new field.
- An exclusion written on such a question ("no new piers where piers exist")
  also needs `when_missing: fire`, or a question nobody answered lets the
  value through (guide section 10, "don't offer this here").
- The Console warns about a `when_unknown` or `when_conflicting` on a Rule
  that reads no such question, and about a Rule whose disputed answers would
  take more than 64 combinations to decide; a run past that limit blocks.
- Taking a value out of a published Attribute's list is a vocabulary change:
  inspection drafts in the app still hold the old answer and are put right
  when the app next reads the knowledge. Say so in the hand-over.

## What Replay and `ks_resolve` cannot see

Replay cases and `ks_resolve` run the trade intake, not an inspection. An
inspection trade has no cases: report every company as "no coverage" and the
change as **not verified by Replay**. What confirms it: the Console's Test
panel on the Rule (`console_url` with `module=rules`, `kind=rule` and the
Rule's `object`), or the inspection app reading the layer's draft. Never report
an inspection change as verified.
