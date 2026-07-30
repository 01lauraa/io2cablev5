# Open questions & candidate rules

Rules identified during project validation but **not yet encoded**. Each entry
records the pattern, the proposed encoding, and what would need to happen before
adding it to `kabelconfig.xlsx`. Per the validation protocol: never encode a rule
from a single observation.

---

## Section 1 — Candidate rules from project 7268 (offices + naregelingen, CCA)

# Rule 1 — Third-party derden installations (STATUS UPDATE)

This replaces the earlier version of Rule 1 in `docs/OPEN_QUESTIONS.md` Section 1.
The rule has been investigated across two more projects and is **held**, not
encoded, pending guidance from Rick.

## Summary

**Rule 1 as first drafted — "any row with a `levering derden` marker → emit
derden cable only, suppress signal cables" — is wrong.** The marker text has at
least four distinct meanings depending on estimator convention. Encoding the
simple version breaks Boerhaave's regression on three energiemeter rows. The
name-based portion of the rule (kWh-meter, roldeur, MIVA, etc.) still looks
sound but was not encoded, so the merge gate is left untouched.

## What the investigation actually found

Across three projects, rows carrying a `levering derden` / `lev. 3e` marker
resolve to four different outcomes in the manual:

| Marker text | Where | Manual outcome | Interpretation |
|---|---|---|---|
| `Levering derden` alone | 7268 Brandklep (Artikel col) | Full `8X0,8` signal cable emitted | Device supplied by third party, Erco wires normally |
| `Lev. 3e` | 7268 Aan/Uit schakelaar (Artikel col) | `5X1` stuurstroom | Same: device is third-party, cable is Erco |
| `Levering derden` | Boerhaave Energiemeter WP (opmerking col) | `3X1` stuurstroom **and** BMS bus | Meter is third-party, both cables still Erco |
| `VOEDING LEVERING DERDEN` | ZRD RADA-box | BMS Cable only | Only the voeding is derden, bus stays Erco |
| `GATEWAY LEVERING DERDEN` | ZRD KNX verlichting | Kabel levering derde… (derden termination only) | Full third-party, no field cables |
| `LEVERING DERDEN` | ZRD Hydrofoor | Voedingen derden row **+** real `4X0,8` signal | Voeding derden, storing wired |

## Why this defeats simple encoding

The marker text is identical or nearly so across all six cases. Same phrase,
six different outcomes. Distinguishing them from data would need at least one
of:

- **Extra context columns** — but the marker sits alone; there is no adjacent
  column that reliably qualifies it
- **Project-level convention parameter** — but the ambiguity exists *within*
  the same project (ZRD has three of the four outcomes across three rows)
- **Voltage/current signal** — Boerhaave's rows have `voltage=24V DC`; the
  others don't. Fragile, and would need to be validated on a fourth project
  before trusting

## What still looks safe (and is what I'd encode when authorized)

The **name-based synonyms** are unambiguous across both projects that contain
them. These devices are consistently derden-terminated regardless of the
marker text:

- `kWh-meter`, `kWh meter`
- `roldeur`, `vluchtdeur`
- `overspanningsbeveiliging` (also observed misspelled `overspannning`)
- `dali verlichting`, `terreinverlichting`
- `veegpuls verlichting`, `schemerschakelaar`, `buitenverlichting`,
  `gevelverlichting`, `knx verlichting`
- `miva`, `liftinstallatie`, `lift storing`
- `wcd vrijgave`
- `inbraakcentrale`, `verkeerslicht`

Cable to emit for these: `Kabel levering derde totaan RK, aansluiten kastzijde Erco`
(no procescode, no bekabeling-naar, no signal cables).

Impact if encoded: ~15 rows in 7268 and ~20 rows in ZRD move from "no cable
derived" to correct. Estimated blind accuracy: 7268 ≈37% → ≈50%; ZRD ≈17% →
≈35%. Boerhaave regression stays green because none of these device names
appear in it.

## Questions for Rick before encoding anything marker-based

1. **`Levering derden` in Boerhaave's Energiemeter WP opmerking** — was the
   estimator's intent "meter itself is utility-supplied but we still run our
   own 3X1 stuurstroom and BMS to it"? Or was the manual inconsistent with the
   standard and should those three rows have been a single derden termination?

2. **`Voeding` vs `Gateway` vs bare `Levering derden`** in ZRD — is this the
   estimator distinguishing three different scopes (voeding-only vs
   full-scope vs signal-only), or is it just spelling variation that happens
   to match the manual outcome by accident?

3. **Convention parameter** — would it be reasonable to add a per-project
   `derden_marker_scope` parameter (voeding_only / full / signal_only) that
   the estimator sets when the marker convention is fixed across a project?
   Or is the convention actually per-row, in which case the text is the
   only signal we have?

4. **`Lev. 3e` shorthand and its Artikel-column placement in 7268** — is
   this a Kuijpers-house convention, or does the same estimator also use
   `Levering derden` interchangeably? If the shorthand always means
   "device supplied by third party, Erco cables normally," then
   `Lev. 3e` could be a *safe* trigger for "keep signal cables, add derden
   note" but not for "suppress signal cables."

## Current state of the code

Nothing was committed. My working copy briefly had the encoding but it broke
Boerhaave 3/15; I rolled it back. Merge gate 3/3 green. No files on your side
need reverting because the changes were never pushed to your machine.

## Related update: Naregelingen BOM writer

Now has three confirmations (Tilburg + 7268 + ZRD) of the same aggregated
`Stuks | onderdeel | wcd | totaal | materiaal | bekabeling naar` layout.
Batched status is closed — this is genuinely buildable when we get to it. The
BOM writer would produce a separate output file per project (page 7 of the
Erco manual), not additional rows in the main cable list.

---

### Rule 2 — Energy Valve → RAK SIGN KAB 4x0,8
**Status:** one observation. Do not encode yet.
**Evidence:** project 7268, 8 rows across r34, r37, r43, r48, r58, r61, r48, r84.

**Pattern.** Belimo Energy Valve — a valve with integrated power meter and
BACnet. `Energyvalve verwarmen voeding`, `Energyvalve koelen voeding`. Also
generates a BACnet cable (see Rule 3).

**Proposed emitted cable.**
`RAK SIGN KAB CCA 4X0,8 HA500`.

**Proposed synonyms (`1_Synoniemen`, priority ~85):**
```
energyvalve voeding    -> ENERGY_VALVE_VOEDING
energyvalve            -> ENERGY_VALVE_VOEDING (fallback, priority 60)
```

**Proposed cable table row (`2_Kabelkeuze`):**
```
ENERGY_VALVE_VOEDING | RAK SIGN KAB CCA 4X0,8 HA500 | ??? (B2CA equivalent unknown)
```

**Confirmation needed.**
1. B2CA family equivalent — no validated project string.
2. Whether Energy Valve `voeding` is always this control cable, or ever the power
   feed to a bigger unit.

---

### Rule 3 — BACnet Delta Controls → UTP CAT6 CS34ZB HA305
**Status:** one observation. Do not encode yet.
**Evidence:** project 7268, 5 rows (BACnet koppelingen r35, 38, 44, 49, 59, 62)
plus the Naregelingen `Communicatie Delta Controls` row.

**Pattern.** BACnet-IP field-device chain. Second and later devices show
`doorlussen` in `bekabeling naar`.

**Proposed emitted cable.**
`COMM U/UTP CAT6 CS34ZB HA305`. Note **`CS34ZB`**, not the `CS34ZC` variant used
for RK-onderling communicatie.

**Proposed synonyms (`1_Synoniemen`, priority ~85):**
```
bacnet koppeling     -> BUS_BACNET_DELTA
communicatie delta   -> BUS_BACNET_DELTA
delta controls       -> BUS_BACNET_DELTA
```

**Proposed cable table row (`2_Kabelkeuze`):**
```
BUS_BACNET_DELTA | COMM U/UTP CAT6 CS34ZB HA305 | COMM U/UTP CAT6 CS34ZB HA305
```

**Alternative — register as a bus protocol in `4_Bus` instead of `2_Kabelkeuze`**
so the existing bus-chain logic (`doorlussen` on 2nd and later) fires
automatically.

**Confirmation needed.**
1. Whether Delta Controls always maps to this cable, or whether other BACnet
   suppliers use different jackets.
2. Whether `CS34ZB` and `CS34ZC` differ meaningfully in practice — if
   interchangeable, one rule suffices.

---

### Rule 4 — Warmtepomp diverse functies → 6x2x0,8 (CCA)
**Status:** one observation but strongest case for encoding.
**Evidence:** project 7268, r1.

**Pattern.** `Warmtepomp diverse functies` — one bundled cable per WP for the
mixed I/O (bedrijf, storing, sturing, etc.). This is likely the CCA-family
equivalent of the `JOBA HCH-JZ 12X1 B2CA` bundle already validated for
Duitslandlaan and Fonkel (both B2CA).

**Proposed emitted cable.**
`DRAK SIGK CCA 6X2X0.8 MT`.
Note: manual writes `6X2X0.8` with decimal *point*, not the comma used
elsewhere. Preserve exactly.

**Proposed synonyms (`1_Synoniemen`, priority ~90):**
```
warmtepomp diverse functies -> WP_DIVERSE_FUNCTIES
warmtepomp diverse          -> WP_DIVERSE_FUNCTIES (fallback, priority 70)
```

**Proposed cable table row (`2_Kabelkeuze`):**
```
WP_DIVERSE_FUNCTIES | DRAK SIGK CCA 6X2X0.8 MT | JOBA HCH-JZ 12X1 B2CA MT
```

**Confirmation needed.** Whether `6X2X0,8` (CCA) and `12X1` (B2CA) are really
two variants of the same rule. Strong prior yes, but should be checked against
one more CCA WP project.

---

## Section 2 — Conflicts held from the master dictionary (Standaarden CCA)

The dictionary Rick shared conflicts with validated projects in four cases.
Encoding the dictionary literally breaks the merge gate; encoding validated
behaviour leaves the dictionary rules "on paper only." Ask Rick which is
authoritative before choosing.

### Conflict A — Transportpomp voeding
| Source | Cable |
|---|---|
| Standaarden CCA | `4g1,5` |
| Duitslandlaan manual (validated) | `4g2,5` |
| Fonkel manual (validated) | `4g2,5` |
| Tilburg manual (validated) | `4g2,5` |

Three projects vs one line of standard. Likely: standard is minimum spec,
practice runs one size up. Ask Rick.

### Conflict B — Ketel vrijgave/storing/sturing 0-10V
| Source | Cable |
|---|---|
| Standaarden CCA | one `2x2x0,8` |
| Duitslandlaan manual (validated) | split: `5X1` + `2X1` |

One project against the standard. Standard would break Duitslandlaan
regression if encoded literally.

### Conflict C — Warmtepomp meldingen
| Source | Cable |
|---|---|
| Standaarden CCA | `6x0,8` per storing signal |
| Duitslandlaan manual (validated) | one bundled `12X1` |
| Fonkel manual (validated) | one bundled `12X1` |

Standard counts per-signal; two projects agree on bundling.

### Conflict D — Warmte-/koudemeter voeding
| Source | Cable |
|---|---|
| Standaarden CCA | `3g1,5` (power) |
| Boerhaave manual (validated) | `3X1` stuurstroom |
| Project 7268 manual | `3g2,5` (power) |

Three sources, three different answers. Not derivable from data alone.

### Conflict E — Warmtewiel voeding
| Source | Cable |
|---|---|
| Standaarden CCA | `3g1,5` |
| Project 7268 manual (row 56, LBK section) | `3G2,5` |

Discovered during the 7268 overshoot analysis. One project vs standard.
Not encodable yet — the pipeline currently emits `3G2,5` (generic 230V feed
path) and the manual happens to agree, but that's coincidence, not the encoded
rule. If encoded literally as `3g1,5`, we'd need a synonym for `warmtewiel
voeding` that overrides the generic pump feed, and then Warmtewiel would ship
`3G1,5` which contradicts this project.
---

## Section 3 — Standing questions from earlier projects (unresolved)

### Q1 — `Totaal aantal werkschakelaars` = 0
The manual shows `0` in the totals row while individual ws entries appear on 10
(Duitslandlaan) / 8 (Fonkel) / 0 (Boerhaave, consistent) / ~8 (project 7268)
rows. Two estimators, same contradiction across three projects. Encoding
"always 0" without an answer would invent a rule from an artifact.

### Q2 — Sheet-to-panel merge (Tilburg)
Tilburg's manual merged input sheets 1 and 2 into a single RK1 cable list.
Currently the pipeline emits one panel per RK column value. Encoding a rule
here needs a second observation.

### Q3 — Naregelingen BOM writer
Confirmed as standard format across Tilburg + project 7268 (two projects now,
same aggregated Stuks/onderdeel/wcd/materiaal layout). Justified as buildable.
Not built yet — batched.

---

## Section 4 — Recurring code bug (not a rule question)

### Bug — `POMP_230V` feed cable does not emit (RESOLVED 2026-07-21)
Root cause: `_parse_electrical_spec()` returned voltage/current as strings while
`rules._naar_feed()` uses `f"{current_a:g}"` format, which requires float.
Every project where the fallback fired crashed silently at the first feed row.
Fixed in ingest.py by returning `float` for current_a and power_kw, `str` for
voltage. Verified on project 7268: 48% blind after fix (up from ~37%).



---

## Section 5 — Rule-hygiene issues to fix opportunistically

- **12 over-emitted `DRAK CCA GY 2X0,8` rows on project 7268** — the
  `KLEP_STURING_MELDING` fallback firing on rows that should have matched more
  specific types. Adding Rules 1 and 2 above suppresses most of these
  automatically, because higher-priority synonyms win first.

- **`WEERSTATION_BUS` cable choice** — added in the dictionary batch as
  `DRAK SIGK CCA 1X2X0,64 MT`. That is the CCA notation for the same physical
  cable as the BMS Cable used elsewhere. Worth verifying they're
  interchangeable in the article database, or split into two types.

- **CS34ZB vs CS34ZC** — the dictionary batch added `COMM_RK_ONDERLING` as
  `CS34ZC`. Rule 3 above would add `CS34ZB` for Delta Controls. If they are
  functionally the same, consolidate.
