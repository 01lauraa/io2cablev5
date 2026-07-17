# io2cable — Function list → Cable list pipeline

Steps 1–3 of the 5-step pipeline (rules v2, validated on Duitslandlaan RK071 and
the lessons from the 112-meldkamer project). Deterministic core, AI only at the edges.

```
function list (xlsx) ──Layer A──┐
                                ├─► normalized table ─► REVIEW ─► classification ─► rules engine ─► cable list.xlsx + flags.txt
function list (pdf/scan) ─Layer B┘        (CSV/xlsx)    (human!)   (dictionary)      (config xlsx)
```

Dutch domain terms that appear literally on the physical cable lists are kept as-is
(RK = regelkast / control panel, ws = werkschakelaar / isolator switch, Voedingen =
feeds, doorlussen = daisy-chain, Werkzaamheden derden = work by third parties,
Onderstation algemeen = substation general, naregelingen = room/zone controls). The
generated cable list must match the house format string-for-string, so these are not
translated in the output.

## Quick start

```bash
# 1. Per project, fill in 0_Parameters in config/kabelconfig.xlsx
#    (brandklasse / fire class is MANDATORY — it cannot be derived from the I/O list)
# 2. Run:
python3 -m io2cable.pipeline \
    --config config/kabelconfig.xlsx \
    --input  path/to/function_list.xlsx \
    --out    out/ --rk RK071
```

Output in `out/`:
- `normalized_review.xlsx` — **must be reviewed by a human** before use
- `cable_list_<RK>.xlsx` — house format: nr | onderdeel | ws | proces code | kabel | bekabeling naar
- `flags.txt` — every human decision point (third-party scope, n.t.b. items, tracing,
  WP hybrid, unknown terms)

## Mixed input formats (Layer A / Layer B)

- **Structured Excel** (fixed columns): straight through via `--input function_list.xlsx`.
  The header row is auto-detected; non-standard headers map via a `header_map`
  (see `config/header_map_*.xlsx`). Only rows flagged M&R="Ja" are included; group headers are
  carried down; "dak/bovendaks" (roof) in the group or description sets
  `locatie="op dak"`.
- **PDFs, scans, free-form files**: normalize with AI assistance (e.g. with Claude)
  into the canonical CSV schema (columns in `io2cable/schema.py::NORM_COLUMNS`;
  example: `fixtures/duitslandlaan_normalized.csv`) and pass that CSV as `--input`.
  The normalized table is the contract; everything downstream reads only this
  schema, never the source file.

In both cases: **review `normalized_review.xlsx` before Step 2** — a normalization
error otherwise silently corrupts everything after it.

## What the estimators maintain themselves (no code required)

Everything lives in `config/kabelconfig.xlsx`:

| Tab | Contents |
|---|---|
| 0_Parameters | per project: fire class (CCA/B2CA), cable family, length class, room-control system, tracing scope, panel location |
| 1_Synoniemen | classification dictionary — **add every manual correction here**; the system gets smarter with each project |
| 2_Kabelkeuze | function type → cable string per family (one family switch = one parameter) |
| 3_Voedingen | feed classes, ws assignment, "bekabeling naar" templates (kW/A/V) |
| 4_Bus | bus cables per protocol, daisy-chain behaviour |
| 5_Vaste_teksten | literal house strings (third-party strings, connection lead, fire alarm, totals rows) |

A change to the cable standard = editing a cell, not code.

## Built-in rules v2 (proven on Duitslandlaan)

- 1 row = 1 physical cable; feed always separate; an AO can get its own cable (E-boiler)
- group order = ascending process-code prefix (071→081→091); rows without a code (WP,
  tracing) lead; sections kept contiguous
- "Totaal voedingen derden aansluiten" counts only cables arriving at the RK;
  device-side feeds = "Werkzaamheden derden"
- ws total computed from the ws column (the real list showed 0 — open question, see
  the validation report)
- daisy-chain: the 1st bus device gets its location, the 2nd+ get "doorlussen";
  a Modbus-IP field device uses the BMS cable, not UTP
- energy meter = bus + a separate 24V feed cable; meter option sensors = "Via
  aansluitsnoer…", no cable
- 400V frequency-controlled pumps = 4G2,5 (no neutral)
- WP = a single 12X1 for all meldingen; n.t.b. items omitted + flagged
- fire alarm always closes Onderstation algemeen; outdoor sensor only if it is in the input

## Housekeeping

`config/kabelconfig.xlsx` is the source of truth — edit it directly.
`build_config.py` only bootstraps a fresh copy and is generated from the live
workbook; after editing the workbook run `python3 dump_config.py` so the two
never drift apart.

## Regression tests — the merge gate

```bash
python3 run_all_tests.py     # every project regression; nothing merges unless green
```

Currently: Duitslandlaan 18/18, Boerhaave 15/15.

## Validating a new project

Read **`docs/VALIDATION_PROTOCOL.md`** first. In short:

1. Run **blind** — fill parameters, change nothing else
2. Hand over four things: `input.xlsx`, `manual.pdf`, `out_blind/` (incl. flags.txt), `config_used.xlsx`
3. Every mismatch gets exactly one bucket: **BUG · CONFIG · PARAM · DATA · ASK · ACCEPT**
4. BUG/CONFIG → fix now. PARAM/structural → **batch** until a 2nd project confirms. ASK → ask, never guess.
5. Lock it in: fixture + `projects/<name>/test.py` + CHANGELOG entry + scorecard row
6. `python3 run_all_tests.py` must be green

| Doc | Purpose |
|---|---|
| `docs/VALIDATION_PROTOCOL.md` | the loop and the rules of engagement |
| `docs/CHANGELOG.md` | every change → bucket → project → row that proved it |
| `docs/SCORECARD.md` | blind accuracy per project, and the trend |
| `projects/<name>/` | input, manual, config, fixture, test, validation write-up |

## Still to build (steps 4–5)

- Step 4: full house-format generator (Erco header, logo, pagination, Naregelingen sheet)
- Step 5: review screen bundling flags.txt + normalized_review.xlsx into one sign-off flow
- Layer B helper: prompt template for PDF→CSV normalization

## Non-standard column layouts (per client)

Every client's functielijst has a slightly different header row, so the mapping
from their columns to the canonical fields is **an editable Excel file**, not code:

- `config/header_map_kuijpers.xlsx` — the Kuijpers/Servex layout (used by IO.xlsx)

To support a new client: open that file, edit the `client_header` -> `canonical_field`
rows on the **HeaderMap** sheet (the **valid_fields** sheet lists every allowed target),
save it as `config/header_map_<client>.xlsx`, and pass it with `--header-map`.
No Python editing required.

Standard-layout files need no map at all — omit the flag.

## Full command (one line)

```bash
python3 -m io2cable.pipeline \
    --config config/kabelconfig.xlsx \
    --input /path/to/IO.xlsx \
    --header-map config/header_map_kuijpers.xlsx \
    --out out --rk RK071
```
