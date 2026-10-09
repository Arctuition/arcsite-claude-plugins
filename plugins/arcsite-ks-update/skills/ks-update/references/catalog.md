# The Product catalog

Read this before reading, importing, tagging or editing a company's catalog.

A company's catalog is addressed by the company (`organization_id` from
`ks_find_target`, as a string). `ks_read_catalog` says whose library it is —
`shares_enterprise_library: true` means the company reads its Enterprise's
library, so an import or a tag lands there, for every company on it; say so —
how many Products there are, how many have no Role yet (`untagged`), counts by
Role, and the latest tagging runs. To find rows, give it `search` (part of a SKU
or name) and/or `role`: it lists matching rows 50 a page (`page`), each with
its Roles, stated Attributes and selling terms. Use it to find the SKUs an
edit should name, rather than guessing them. `vocabulary: true` adds the words
the catalog is described in, read from the company's knowledge with its drafts:
`roles` (each Role with the `attributes` a Product bought as it states and
which of them are `required`) and `attributes` (each once: `value_type`,
`unit`, `cardinality`, `allowed_values` with labels — null means an open
vocabulary, any value — and `extensible_below`: whether a layer below the
Trade may add values of its own). It comes 15 Roles a page, each page with
the Attributes its own Roles state: `vocabulary.pages` says how many, and
`vocabulary_page` asks for the next. `vocabulary_search` keeps only the Roles
whose stable_id or name contains it — a material system such as `chain_link`
or `vinyl` — so read the families the work is about, every page of them,
instead of reading Attributes one by one with `ks_read_object`. An Attribute
two pages both use appears on both. It leaves out what only the job answers
(questions about the fence being built); those are in the Questionnaire.

**Import.** The person gives a file. Turn its first sheet into CSV text with a
header row naming `Name` and any of `ArcSite ID`, `SKU`, `Description`
(map the vendor's column names onto these; leave every other column out;
never invent or clean up values). Pass that text as the tools' `csv`
argument; there is no file argument. A row finds its Product by ArcSite ID, then
SKU, then name; one that finds nothing adds a Product, and Products the sheet
leaves out are left alone. `ks_catalog_import_preview` → report `created`,
`updated` (with `updated_examples`), `unchanged`, and every row in `errors`.
Fix only a column you mapped wrongly; otherwise show the errors and ask. Apply
with `ks_catalog_import_apply`, the same text, only when the preview has
`error_count: 0` and the person asked to import. It is all rows or none. There
is no undo: a sheet that renames or re-SKUs existing Products changes them
until another import or the Console changes them back — say so before applying
one with `updated` above 0. More than about 3,000 rows: send parts, each with
the header, preview and apply each; each part is all or nothing. A very large
file is quicker through the Console's Import.

**Direct edits.** `ks_catalog_edit` writes what the Console's catalog screen
writes, for many rows in one call: a list of `edits`, each naming rows by
`skus` (or `product_ids` for a row with no SKU) and any of `role` with `tag`
true/false, `attributes` (Attribute stable_id → values in the vocabulary's
words; `[]` takes a statement back), and `selling` (`preset`, `unit`,
`amount`, `rounding`, `extra`). Stating a value needs the `role` it is
stated under, and only that Role's Attributes are accepted — read them first
if you are unsure. Clearing one (`[]`) needs no `role`, so a value left behind
by an Attribute nobody declares any more can still be taken off. The Role's selection policy (for example requested only) is one of
its Attributes: state it like any other. Always call it first as it defaults,
`dry_run: true`. The answer gives each edit's counts and `changed_skus`;
check the counts are what you meant. Add `detail: true` only for a small batch
whose values you need to show (each entry of `changes`, `before` → `after`):
for a large one it is too big for a tool result. Write with
`dry_run: false`, the same edits, only when the person asked for those
changes; the answer reads every changed row back. One edit that cannot be
made (a SKU not in the catalog, a Role or Attribute the company's knowledge
does not declare, a value outside the vocabulary) refuses the whole batch:
`errors` names each by `edits[N]`. There is no undo: a wrong edit is put right
by another edit, so say so before writing one that changes rows people tagged
by hand. Like an import, it lands in the Enterprise's library when the company
shares one.

**AI tagging.** `ks_catalog_tag` `action: start` queues a run over Products
with no Role yet; on those it fills only Attributes the row does not state, and
it never touches a row that already has a Role. Right after an import, or on
a catalog nobody has tagged before, start with `limit: 20` — a limited run
takes the newest untagged rows, which after an import are the ones it added —
wait with `ks_read_catalog` `wait_seconds: 15`
until no run is `alive`, report its `summary`, and give the result's
`console_url` (it opens the rows that run wrote) for the person to check
before you start the rest. `action: undo` with the run's `task_id` takes back
what that run wrote, except rows a person has changed since; only when asked.

Catalog changes are not drafts and are not in a release plan. To see their
effect on real orders: when the company's layer has no unpublished changes
(`ks_find_target` `unpublished_changes: false`), `ks_replay` on that layer
without `release_organization_ids` shows it, and differences marked
`catalog_changed` come from outside the knowledge — the catalog change, or a
deploy since the baseline; otherwise say the result also includes the drafts.
