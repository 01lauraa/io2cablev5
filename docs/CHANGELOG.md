# Changelog

Every change traced to the project and row that proved it. Buckets per
`docs/VALIDATION_PROTOCOL.md`: BUG · CONFIG · PARAM · DATA · ASK · ACCEPT.

Format: `[BUCKET] change — evidence (project / row)`

---

## v4 — Fonkel Breda (PR 20267276-2600214), B2CA Kuijpers
Blind score ~89% (54/61). All misses structural; **zero cable-knowledge errors**.
Three BUGs fixed; two structural items remain batched.

### BUG — device deduplication (`rules.dedupe_devices`)
- **Duplicate Regelkast rows.** Fonkel's input has two RK rows → two Voedingen
  rows → `derden=2`; manual has one row, `derden=1`. Now at most one Regelkast
  row per panel. *(Fonkel / Voedingen 1-2)*
- **Multi-feed devices split.** The WP is listed once per feed (hoofdvoeding +
  condensor; secundaire voeding + verdamper) → two feed rows **and two 12X1
  meldingen bundles**. The manual bundles to one "Warmtepomp" row and one 12X1.
  Rows now merge on `(rk, type, group, name-stem)`, unioning I/O counts so the
  2+2 DI become one 4-DI bundle. *(Fonkel / Voedingen 2-3 + Warmtepomp 1-2;
  reproduced identically on Duitslandlaan raw input)*
- **Key design note.** Keying on `(rk, type)` alone collapsed Boerhaave's THREE
  physical heat pumps into one — caught immediately by the merge gate. The key
  therefore carries group + name stem: one device listed twice merges, three
  devices stay three. *(caught by Boerhaave regression)*

### BUG — section ordering / naming
- **Accessory rows became section names.** Non-M&R rows were treated as group
  headers, producing sections `safety kit`, `TSA PN16`,
  `Deelstroomfilter Deel-SEP GKW`. A non-M&R row is a header only when it is
  bare (no procescode, no fabricaat, no type, no I/O); accessories carry
  equipment data. *(Duitslandlaan+Fonkel raw / sections)*
- **Devices sharing a procescode could be reordered.** `Circulaite pomp 1` and
  `2` both carry `091CP_21`; scattered across junk sections they emitted 2-then-1
  (which read as "pump 2 missing" in the Fonkel diff). Sections are now ranked by
  the smallest sort_key they contain, so process-code order drives sections and
  input order drives rows within them. *(Fonkel / rows 57-60; reproduced on
  Duitslandlaan)*

### CONFIG/RULE — the LOCATION-BANNER rule (resolved once the input arrived)
The Fonkel functielijst (PREC000155) settled the batched group-naming question.
Its group headers are **locations**, not equipment: `Installaties op het dak` and
`Installaties buiten bij buffervat`. The manual converts them:

| input group | manual section | manual bekabeling naar |
|---|---|---|
| Installaties op het dak | **Warmtepomp** | **op dak** |
| Installaties buiten bij buffervat | **Buffervat CV** | **Buiten TR** |

So the rule is: *an input group is a section name unless it is a location banner,
in which case it becomes the location and the section falls back to the
equipment.* This reconciles both projects — Boerhaave's groups (`Warmtepomp 1/2/3`)
are equipment names and stay verbatim; Fonkel's are locations and convert.

Encoded as a new config tab **`6_Locatiekoppen`** (pattern → locatie →
sectie_fallback), so estimators maintain it. Result: **all 10 Fonkel sections now
match the manual exactly**, and `Buiten TR` ×3 / `op dak` ×2 land in the right
column. *(Fonkel / sections + rows 16-18, 1-2)*

This is the protocol working as designed: the rule was held back at one
observation, and the second observation made the right design obvious. Guessing
after Fonkel's blind run alone would have produced a mapping table that broke
Boerhaave.

### Still batched
- **Tracing sub-panel** (Fonkel page 5: own Voedingen, `derden=0`, 2 cables, no
  RK code). Still one observation. The Fonkel input marks tracing "optioneel
  vanuit regelkast" — a hint it is quoted separately — but one hint is not a rule.

### ASK
- `Totaal ws` = 0 while the column holds 8 entries (Fonkel) / 10 (Duitslandlaan).
  Two projects, two estimators, same contradiction. **Still unencoded.**

### LOCKED
Fonkel is now regression #3: `projects/fonkel/test.py`, **18/18**.
Merge gate: **3/3 projects green**.

---

## v3 — Boerhaave Leiden (PR 20267275.1), CCA renovation, 2 panels
Blind score: ~20% usable → after fixes: 15/15 regression.
First project on the Coneco layout. Broke in three ways at once (wrong header
map, corrupted input, unknown house rules) — the failure pattern that motivated
the whole protocol.

### BUG
- **Primary-match classification.** Substring matching let "Elektrameter
  **warmtepomp**" and "temp GKW **warmtepompen**" trigger the WARMTEPOMP branch →
  11 phantom feed rows. `classify` now picks one primary type (highest priority,
  longest pattern) at `functietypes[0]`; `emit` branches on that alone.
  *(Boerhaave / rows 6, 17, 28)*
- **DERDEN hijacked primary.** A scope attribute was outranking the device class,
  silently eating energiemeter voeding rows. DERDEN is now demoted out of
  primary position. *(Boerhaave / energiemeter rows)*
- **Literal feed templates.** A `bekabeling_naar_sjabloon` without `{}`
  placeholders was discarded instead of used verbatim → "voeding doorlussen" lost.
  *(Boerhaave / tracing rows 14, 22)*

### CONFIG
- **Mixed family within one project.** The house standard picks family *per
  function type*, not project-wide: measurement = DRAK SIGK CCA, stuurstroom =
  JOBA STUURSTR, power = DRAK HULT CCA. Fitted the existing schema — cell edits
  only, no redesign. *(Boerhaave / whole list)*
- `SMOORAFSLUITER` → `JOBA STUURSTR HHJZ 7X1 MT` *(Boerhaave / rows 3-6)*
- `METER_VOEDING_24V` CCA → `JOBA STUURSTR HHJZ 3X1 MT` (B2CA stays 5X1)
  *(Boerhaave / rows 1, 8, 16)*
- `TRACING` CCA → `DRAK HULT CCA 5G2,5 MT` + "voeding doorlussen"
  *(Boerhaave / rows 14, 22)*
- New types: `EVERDELER_METER` (bus row → Onderstation algemeen),
  `NIET_BEKABELEN` candidates *(Boerhaave / rows 30-32)*
- Synonyms: `elektrameter`, `smoorafsluiter`, `leidingverwarming`; raised
  `temperatuur` priority above `warmtepomp` to fix the over-match.

### PARAM
- `regelkast_bestaand` (ja/nee) → "Bestaande regelkast geen aanpassingen"
  *(Boerhaave / RK01+RK03 Voedingen row 1)*
- `wp_aansluiten_erco` (ja/nee) → "Kabel levering derde totaan WP, aansluiten
  WPzijde Erco" *(Boerhaave / Voedingen rows 3-4)*
- `brandmelding_standaard` (ja/nee) — renovation lists have no new fire-alarm
  cable *(Boerhaave / no brandmelding row)*
- Per-family columns `ws_CCA`/`ws_B2CA` and `sjabloon_CCA`/`sjabloon_B2CA`,
  because the two validated projects genuinely disagree on tracing ws and
  templates. *(Boerhaave vs Duitslandlaan / tracing)*

### RULE CHANGE
- **`Totaal voedingen derden aansluiten` refined.** v2 said "cables arriving at
  the RK". Boerhaave counts a WP-side termination. New rule: **count every feed
  row Erco terminates, wherever it terminates.** Both projects now correct
  (Duitslandlaan=1, Boerhaave=2). *(Boerhaave / Voedingen totals)*

### FEATURE
- **Multi-RK.** `run_per_rk()` groups by the `rk` field; one output file per
  panel. *(Boerhaave / RK01 + RK03)*

### DATA
- `IO_cut.xlsx` contains dead `#VALUE!`/`#REF!` formulas where DI/DO/AI counts
  belong. Ingest now parses `*1` markers as 1, treats error tokens as 0, and tags
  the row `[!formula errors in ...]` so the review file shows exactly where.
  Not a rules problem — a review-gate problem. *(Boerhaave / rows 10-13, 38-44)*

### ACCEPT
- WP1 bus row present in output, absent in manual (renovation decision).
- Chain labels: engine writes "doorlussen"; manual uses "Uit WP 1"/"Uit WP 2".
- "maximaal 40 meter" — length is human input (§6 ambiguity).

---

## v2 — Duitslandlaan Zoetermeer (PR 20267283), B2CA new-build
Blind score: ~83% structural, 24% exact-string → after fixes: 18/18 regression.

### PARAM
- **`brandklasse` is mandatory and non-derivable.** Defaulting it to CCA
  produced ~35 wrong rows from one wrong cell. The CLI now refuses to run when
  it is empty. Single most valuable finding of the project.
  *(Duitslandlaan / whole list)*

### CONFIG / RULE CHANGE
- 400V frequency-controlled pumps (TPE3) = **4G2,5** (no neutral), not 5G2,5 —
  a genuine error in the v1 table. *(Duitslandlaan / rows 31,33,38,40)*
- Group order = **ascending process-code prefix** (071→081→091), not raw input
  order. *(Duitslandlaan / Korex placement)*
- In B2CA/JOBA projects everything is **MT**; HA500 exists only inside the BMS
  cable product name. *(Duitslandlaan / whole list)*
- `bekabeling naar` for motor feeds = kW/A/V string from the input E-data.
  *(Duitslandlaan / rows 31,45)*
- Modbus **IP** field device → BMS cable, **not** UTP. UTP stays for touch panels
  and panel-to-panel. *(Duitslandlaan / Korex row 30)*
- Energiemeter = bus **plus** a separate 24V feed cable. *(Duitslandlaan / 11,12)*
- Meter option sensors (PT100 "Optie C1") → "Via aansluitsnoer van 2 meter op
  meter", no cable. *(Duitslandlaan / rows 13,14,25,26)*
- WP meldingen → one 12X1 bundle, not split per feed side. *(Duitslandlaan / r2)*
- E-ketel signals split: vrijgave/storing 5X1 + **separate** sturing 2X1.
  *(Duitslandlaan / rows 53,54)*
- Brandmelding always closes Onderstation algemeen, even when absent from the
  input. Outdoor sensor only when present. *(Duitslandlaan / row 63)*
- Powered field instruments up to ~30 VA: signal + supply on one cable.
  *(Duitslandlaan / row 10)*

### ASK
- **`Totaal ws` = 0 while the ws column holds 10 entries.** Unexplained.
  Not encoded.

---

## v1 — initial rules from five project pairs
Den Dullaert, Avans, ISH, Schiphol, ZRD + "Standaarden CCA".
Established: canonical types, cable tables, project parameters, output
structure, known ambiguities. Never blind-validated.

---

## Open items (not encoded — need answers)

| # | Item | Seen in | Status |
|---|---|---|---|
| 1 | `Totaal ws` = 0 while ws column is populated | Duitslandlaan (10), Fonkel (8) | **ASK Rick.** Twice is a pattern, but it's unexplained — encoding it would be inventing a rule from an artifact. |
| 2 | Group naming: input groups are authoritative (Boerhaave) vs wrong (Fonkel) | Boerhaave, Fonkel | **Batched.** Needs a second signal before designing. |
| 3 | Sub-panels without an RK code (Fonkel "Tracing" page) | Fonkel | **Batched** with #2 — both are "how does a list split". |
| 4 | WP-internal water temps: bus-coupled WP's own in/out temps get no cable | Boerhaave | Candidate `NIET_BEKABELEN` type. One observation. |
| 5 | `Buiten TR` as a third location value | Fonkel | Needs a rule or a review field. |
| 6 | Whether client-specified WSK columns should override the engine | klemmenlijst layout | Ask before wiring. |
