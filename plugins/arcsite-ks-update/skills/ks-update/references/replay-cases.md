# Saving jobs as Replay cases

`ks_save_cases` keeps up to 20 jobs as one company's Replay cases in one call.
A case is the job only: `context`, `answers` and `instances`, the shape
`ks_resolve` takes. What Replay compares later changes with is what the
published knowledge answered for it when it was saved (its baseline), not the
supplier's quote. A case is live at once and shows on the Replay list of every
layer the company's knowledge reads, so save only when asked.

1. **Company and Trade.** `ks_find_target`. Save under the company the order
   was quoted for (a branch, not its Enterprise's library).
2. **Build each job** as for `ks_resolve`: copy a close saved case
   (`ks_replay_results action: case_inputs`) where there is one, and answer
   every Question the form asks (`references/overlay-and-resolve.md`, "A job
   you write yourself").
3. **Resolve each job first** (`ks_resolve`, published): a job that does not
   resolve will not get a baseline either. Compare it with the supplier's
   quote, and tell the person which answers you rebuilt rather than read.
4. **Save:** `ks_save_cases` with `organization_id`, `trade`, `cases` and
   `wait_seconds: 15`. Each case has:
   - `code`: your own, stable identity for it, such as the supplier's quote
     or order number (`mh-wood-31`). The same code with the same job comes
     back `unchanged`, so a batch can be sent again after a fix.
   - `name`: what a person reads on the Replay list (order, customer, the
     main spec).
   - `effective_on`: only when the person gives the day to price the order
     for; omitted, a new case gets today and a saved one keeps its day.
   - A job built to reach a rule no real order reaches: start its code with
     `synthetic-` and its name with `Synthetic:`, so nobody reads it as a real
     order.
5. **Read the answer.** Each case has an `outcome` (`created`, `replaced`,
   `unchanged`) and its `baseline`:
   - `queued` or `running`: `ks_replay_results action: status` on
     `target_layer` with `wait_seconds: 15` until it is done.
   - `failed`: `baseline.error` says why the job did not run (an answer the
     form does not know, a missing measurement). Fix that job and send it
     again under its code with `replace: true`.
6. **Refusals save nothing:** `case_invalid` (a malformed job, at
   `cases[i]`), `case_code_repeated`, and `case_code_taken`: the code already
   names a different case (`data.case_id`), perhaps one a person saved. Read
   it (`case_inputs`) and ask before sending `replace: true`.
7. A case is removed in the Console's Replay list; give the case ids.

Report each case's code, `case_id`, `outcome` and baseline, and the Replay
`console_url`.
