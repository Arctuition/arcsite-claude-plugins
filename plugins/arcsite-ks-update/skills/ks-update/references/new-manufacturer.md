# A new manufacturer from its sources

Section numbers are the skill's (SKILL.md).

When the person brings a manufacturer's material and wants it set up.

1. **Ask first**, before reading anything: which manufacturer, which Trade
   (for example `fence`), and whether it is a new layer or one that exists
   (`ks_find_target` its name). Ask which company quotes on it. A company or a
   user account that does not exist yet is not yours to create: the person
   makes it in the admin, then you go on.
2. **Sources.** Ask for a SKU export or price book (a spreadsheet) before
   anything else; it is where SKUs and values are reliable. Spec sheets and
   drawings come second. Warranty, care and installation documents state no
   values: skip them and say which files you skipped. A manufacturer with many
   brands or product lines: agree with the person which ones to do first, and
   do them one batch at a time.
3. **Numbers from PDFs.** Text taken from a drawing often loses fraction bars:
   "3 5/16" comes out as "31316". A number that does not fit its Attribute's
   unit or the sizes around it is to be shown to the person and confirmed;
   never correct it yourself.
4. **Create and bind first** (`references/overlay-and-resolve.md`): the Manufacturer layer on the
   Trade, then the company bound to it. Both are free now: the layer starts
   with an empty `0.0.0`, so the company quotes on what the Trade alone says.
5. **Read the vocabulary**: `ks_read_catalog` with `vocabulary: true` for
   that company, `vocabulary_search` set to each material system the sources
   cover, every page of each (`references/catalog.md`).
6. **Classify every value the sources state**, Attribute by Attribute:
   - in `allowed_values`, or the Attribute is open (`allowed_values: null`) →
     use the vocabulary's word when you import and tag;
   - not in it, `extensible_below: true` → the Manufacturer layer can add it:
     an `attribute_domain_extension` in this layer's patch (sections 2–6; read
     its `part: schema` first);
   - not in it, `extensible_below: false` → this layer cannot state it. It
     goes on the **Trade owner's list**;
   - a product with no Role it could be bought as → also the Trade owner's
     list;
   - a value the sources leave unclear or contradict → the
     **manufacturer's list**.
7. **Write two question lists** from that, never from memory: for the Trade
   owner (each closed value or missing Role, with the source value, the SKUs it
   affects and the file it came from) and for the manufacturer (each unclear
   value, with the same). Put both in the summary.
8. **Selling terms come from the price book too.** An import carries only
   name, SKU and description; the sheet's sell unit ("50 ft roll", "bag of
   100", "21 ft stick", "500 ft coil") becomes the row's selling terms after
   the import, with `ks_catalog_edit` `selling` (`references/catalog.md`): `preset:
   packages`, the package as `unit`, and as `amount` how much of the Role's
   `demand_unit` one package holds (a 50 ft roll of fabric demanded in ft is
   `amount: "50"`; a bag of 100 ties demanded each is `amount: "100"`). Set
   them before `ks_resolve`: a row without them is ordered one package per
   unit of demand, so 159 ties come out as 159 bags. A sell unit that does
   not say how much it holds goes on the manufacturer's list.
9. Then the usual steps: the layer's patch (sections 2–6), the catalog import,
   its selling terms and a first AI-tagging run of 20 (`references/catalog.md`), one real job
   through `ks_resolve` with `layers: drafts` (`references/overlay-and-resolve.md`), test cases saved by
   a person in the prototype, and Replay (section 7). Publishing stays the
   person's, in the Console (section 8).
