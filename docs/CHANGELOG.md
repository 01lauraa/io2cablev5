# Changelog

Every change traced to the project and row that proved it. Buckets per
`docs/VALIDATION_PROTOCOL.md`: BUG · CONFIG · PARAM · DATA · ASK · ACCEPT.

Format: `[BUCKET] change — evidence (project / row)`

---

## v5 — 7222 (nieuwe regelkast, technische ruimte 4e verdieping), B2CA/DRAK, 5 panels
First project on the **B2CA/DRAK** family combination and on the client8 layout.
Manual: 793 wires over five panels (RK1 349, RK02 166, RK03 155, RK04 55,
RK05 55) plus a Naregelingen sheet, 6-2-2026, Rick van Deurzen.

Blind 22.6% → **33.4% exact / 45.4% on conductor specs**. Four fixes merged;
merge gate 3/3 green. The dominant remaining error is one config cell.

Full detail in `OPEN_QUESTIONS.md` Section 0d.

### PARAM — `signaalfamilie` inherited again (4th occurrence)
Run made with `signaalfamilie = JOBA`; this client is **DRAK**. Emitted
`JOBA ST.STR B2CA HCHOZ 2X1 MT` ×361 against a manual count of 35, and zero of
the manual's three commonest cables. The same run scored 77.3% when cables were
collapsed into function buckets — the classifier was working and the parameter
hid it. *(7222 / whole list)*

**Fourth run lost to `0_Parameters`.** The parameter echo on the summary line is
still the highest value-per-line change outstanding; add a staleness warning
when `brandklasse`/`signaalfamilie` are unchanged from the previous run.

### BUG — `classify_row` was blind to `procescode`
The client8 layout puts the device name in the tag column and a part number in
`Omschrijving` (`Dakafvoerkap (droog)` / `Servomotor Open/Dicht`;
`Buitenluchtklep` / `GCA126.1E Damper actuator`). The match text was
`omschrijving + type + opmerking`, so the identifying word was invisible.
Added `norm.procescode`. *(7222 / r144-145 + Buitenluchtklep rows)*

Verified with the new `classify_diff.py`: three locked projects NO CHANGE, 7222
28 rows changed, **all `None → type`** — nothing already classified was
reclassified. 11 spec matches.

### BUG — `DO` was invisible to the whole signal path
`classify.py`'s I/O fallback went `AI → DI → AO`; `_ok()` in `rules.py` gated on
`AI`/`DI`/`AO`. A device whose only signal is a digital **output** selected no
type and no cable. Added a `DO` branch → new `KLEP_OD_ZONDER_TERUGMELDING`
(`4x0,8`). `KLEP_OD` could not be reused — it is the with-feedback variant
(`8X0,8`, "open/close + feedback(s)"). *(7222 / r144-145 Dakafvoerkap,
`Voeding=230`, `Digital uit=1`; manual 139-142 = feed + `GY 4X0,8`)*

Recorded because it cost three runs: widening `_ok()` to accept `DO` for
`MELDING`/`VRIJGAVE`/`BEDRIJF_STORING` made every DO-only row select
`BEDRIJF_STORING` (`6X0,8`) and masked the new type. Reverted.

### CONFIG — `servomotor` synonym removed
It names the **actuator**, never the device, and collided in three directions:
2195-06's `Brandklepservomotor levring derden` (ties with `brandklep` at prio
70, wins on length — 13 rows on an unfixtured project), 7222's 14
`ChangeOver6 Servomotor … temperatuur sensoren` (beat `temperatuur` at 65), and
7268's 6 Energy Valve accessories.

**New general rule:** component and attribute nouns (`servomotor`,
`hulpschakelaar`, `aansluitset`, `base`, `module`) must not become device
classes. Same failure as the v3 `DERDEN` primary-hijack, from a different
direction. *(7222, 2195-06, 7268)*

### CONFIG + BUG — pump signal rule
`POMP` classified correctly but was **inert** — absent from `sig_priority`, so
it could never select a signal cable. 7222 emitted `GY 2X0,8` on 40 pump rows;
2195-06 emitted nothing on five.

**Rick 2026-08-18:** the cable follows the **signal count**, not the pump type —
2 signals → `1x4x0,8`, 3 signals → `3x2x0,8`. Confirmed by the reissued CCA
dictionary (nine two-signal pump rows) and 7222's manual (`Circulatiepomp
vrijgave/storing` → `1X4X0,8` ×8; `Transportpomp vrijgave/storing/sturing` →
`3X2X0,8` ×32). Encoded as `POMP_2_SIGNALEN` / `POMP_3_SIGNALEN`, counted from
the I/O columns. **Pump-specific — do not generalise:** the same dictionary
gives a three-signal ketel `1x4x0,8` and a two-signal ventilator `2x2x0,8`.
19 wires. *(7222 / pump rows)*

### CONFIG — reissued CCA dictionary (Rick, 2026-08-18)
Every `1,5` cross-section → `2,5` (19 device types); 27 signal rows
`2x2x0,8 → 1x4x0,8`. Applied to `2_Kabelkeuze` rows 20, 22 and 45 (12 cells).
`3_Voedingen` needed no change — already at `2,5`.

**Closes Conflict A** (transportpomp `4g1,5` vs the validated projects' `4g2,5`
— the standard was stale, the projects were right), **Conflict E** (warmtewiel)
and **Conflict H** (tracing, at `5G2,5`).

`SMOORAFSLUITER` deliberately left at `7G1,5`: that value comes from Tilburg's
validated manual, not the standard. ASK.

### CONFIG — `header_map_client8.xlsx`
17 columns, five rows beyond the defaults. Note `Digital uit` — a **typo in the
client sheet** (missing the second `a`); without the map row, DO reads 0
sheet-wide with no flag.

### DATA — fourth silent-drop mechanism
The raw input has 26 columns in three repeating blocks; `cols.setdefault` keeps
only the first occurrence of each field and discards the rest with no flag.
Merged in Excel to get the run through, which breaks the blind-run contract.
Proper fix: collect every column index per field in `ingest`. *(7222 / raw
input)*

### NOT FIXED — the largest item
`kabel_B2CA_DRAK` `METING_PASSIEF` holds `DRAK SIGK B2CA 1X2X0,8 2501 MT`; the
manual uses `DRAK SIGK 1X4X0,8 B2CA HA500` on 220 rows. Right rows, wrong
string — **~190 wires from one cell**, more than everything merged here
combined. Blocked on an ASK: the reissued dictionary moved drukopnemers to
`1x4x0,8` but left field temperature sensors at `1x2x0,8`.

### ASK
Field sensor cable (~190 wires) · `Levering CWD/W` scope (~83) · open/dicht core
count (58 rows) · `SMOORAFSLUITER` `7g1,5` vs `7g2,5` · `3_Voedingen` `TRACING`
B2CA cell · `Leeswaarde`/`Verzendwaarde` · six `Detector` rows.
See `OPEN_QUESTIONS.md` Section 11, items 17-26.

### Tooling
`classify_diff.py` (required before any synonym or match-text change) and
`probe4.py` (verifies a classify edit reached the running code).

### NOT LOCKED
No fixture — the largest fix is untouched pending the sensor ASK.

**Process note.** Two `classify.py` edits sat unsaved for hours while three runs
were scored against code that did not contain them: VS Code's dirty-write guard
makes autosave a silent no-op once the on-disk mtime diverges. Verify with
`probe4.py` or `git status` before scoring. Prefer scripted patches.

---

## Sessions not recorded here
2195-06 (2026-07-30), 1363 (2026-07-31) and 7267 (2026-08-01) shipped code and
config changes that were logged in `OPEN_QUESTIONS.md` Sections 0, 0b and 0c
rather than here. The v-numbering therefore jumps from v4 to v5 across three
working sessions. Scores for all projects are in `OPEN_QUESTIONS.md` Section 12.

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

**The live list is `OPEN_QUESTIONS.md` Section 11** — 26 items, ordered by wires.
The table below is the original v1-v4 set, kept for provenance.

| # | Item | Seen in | Status |
|---|---|---|---|
| 1 | `Totaal ws` = 0 while ws column is populated | Duitslandlaan (10), Fonkel (8), 7268, 2195-06, 1363 | **ASK Rick.** Five projects. Cosmetic — ws does not affect the wire list. |
| 2 | Group naming: input groups authoritative (Boerhaave) vs wrong (Fonkel) | Boerhaave, Fonkel | **RESOLVED v4** — `6_Locatiekoppen`. |
| 3 | Sub-panels without an RK code (Fonkel "Tracing" page) | Fonkel, 2195-06 | **Batched.** See OQ Q12. |
| 4 | WP-internal water temps get no cable | Boerhaave | Candidate `NIET_BEKABELEN`. One observation. |
| 5 | `Buiten TR` as a third location value | Fonkel | **RESOLVED v4** — `6_Locatiekoppen`. |
| 6 | Whether client-specified WSK columns override the engine | klemmenlijst layout | Ask before wiring. |