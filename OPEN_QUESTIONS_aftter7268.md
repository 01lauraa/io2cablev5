# Open questions & candidate rules

Rules identified during project validation but **not yet encoded**. Each entry
records the pattern, the proposed encoding, and what would need to happen before
adding it to `kabelconfig.xlsx`. Per the validation protocol: never encode a rule
from a single observation.

**Last updated:** 2026-07-30, after validating project 2195-06 (Priva layout,
B2CA, RK1).

---

## Section 0 — What changed on 2026-07-30 (project 2195-06)

Two code changes shipped, merge gate 3/3 green throughout:

1. **`REGELKAST` demotion** (`classify.py` line 28) — see Section 6, Bug B1.
   Recovers 6 pump feeds on 2195-06.
2. **`METING_BUS`** (new function type + `sig_priority` + `_ok` exemption) —
   see Section 6, Bug B2. Recovers 10 sensor rows.

2195-06 progression: 90 → 96 → 106 cables; 46 → 36 flags.

No previously-open question was closed. Four were strengthened (Q1, Rule 1,
Conflict C, Q3) and are marked below. Six new entries added (Sections 6 and 7).

---

## Section 1 — Candidate rules from project 7268 (offices + naregelingen, CCA)

# Rule 1 — Third-party derden installations (STATUS UPDATE 2026-07-30)

The rule remains **held**, not encoded, pending guidance from Rick. But
2195-06 adds a fourth project and — importantly — a project where the marker
is **completely consistent**.

## Summary

**Rule 1 as first drafted — "any row with a `levering derden` marker → emit
derden cable only, suppress signal cables" — is wrong.** The marker text has at
least four distinct meanings depending on estimator convention. Encoding the
simple version breaks Boerhaave's regression on three energiemeter rows.

**New 2026-07-30:** on 2195-06, all 17 derden-marked rows receive full Erco
cables. Not one suppression. That is the first project with a single,
unambiguous convention throughout.

## What the investigation actually found

| Marker text | Where | Manual outcome | Interpretation |
|---|---|---|---|
| `Levering derden` alone | 7268 Brandklep (Artikel col) | Full `8X0,8` signal cable emitted | Device supplied by third party, Erco wires normally |
| `Lev. 3e` | 7268 Aan/Uit schakelaar (Artikel col) | `5X1` stuurstroom | Same: device is third-party, cable is Erco |
| `Levering derden` | Boerhaave Energiemeter WP (opmerking col) | `3X1` stuurstroom **and** BMS bus | Meter is third-party, both cables still Erco |
| `VOEDING LEVERING DERDEN` | ZRD RADA-box | BMS Cable only | Only the voeding is derden, bus stays Erco |
| `GATEWAY LEVERING DERDEN` | ZRD KNX verlichting | Kabel levering derde… (derden termination only) | Full third-party, no field cables |
| `LEVERING DERDEN` | ZRD Hydrofoor | Voedingen derden row **+** real `4X0,8` signal | Voeding derden, storing wired |
| **`Brandklepservomotor levring derden`** | **2195-06, 10 brandklep rows** | **Full `8X0,8` each** | **Device third-party, Erco wires normally** |
| **`Levering sturing luchtklepservomotor derden`** | **2195-06, 3 luchtklep rows** | **Full `8X0,8` each** | **Same** |
| **`Niveauschakelaar levering derden`** | **2195-06, ~4 alarm rows** | **Bundled into `6X0,8` per pump** | **Same** |
| **`VAV-box met regelaar toebehoren levering derden`** | **2195-06, 1 row** | **`4X0,8`** | **Same** |

## SAFE TO ENCODE — brandklep + derden (two observations)

**This is the first fragment of Rule 1 with genuine two-project support.**

- 7268: `Levering derden` on a Brandklep → full `8X0,8` Erco cable
- 2195-06: `Brandklepservomotor levring derden` on 10 brandkleppen → full
  `8X0,8` each

Same device class, same marker family, same outcome, two independent projects
and two different estimators.
---> cable should be 4 x 0.8
**Proposed:** `brandklepservomotor` + derden marker → emit the normal
`BRANDKLEP` signal cable, do not suppress. Effectively a no-op against current
behaviour (the pipeline already emits), but it would let the rows stop
flagging for review.

**Ask Rick:** can this narrow rule ship while the general marker rule stays
open?

## Why the general rule still defeats simple encoding

The marker text is identical or nearly so across all cases. Same phrase,
several different outcomes, and the ambiguity exists *within* a single project
(ZRD has three of four outcomes across three rows). 2195-06 is internally
consistent, which is encouraging but does not resolve ZRD or Boerhaave.

## What still looks safe (name-based, unchanged)

The **name-based synonyms** are unambiguous across the projects that contain
them: `kWh-meter`, `roldeur`, `vluchtdeur`, `overspanningsbeveiliging`,
`dali verlichting`, `terreinverlichting`, `veegpuls verlichting`,
`schemerschakelaar`, `buitenverlichting`, `gevelverlichting`,
`knx verlichting`, `miva`, `liftinstallatie`, `lift storing`, `wcd vrijgave`,
`inbraakcentrale`, `verkeerslicht`.

Cable: `Kabel levering derde totaan RK, aansluiten kastzijde Erco`.

Impact if encoded: ~15 rows in 7268, ~20 in ZRD. Boerhaave stays green — none
of these names appear in it. **Note:** none appear in 2195-06 either, so that
project neither confirms nor contradicts this list.

## Questions for Rick (unchanged, plus one)

1. **`Levering derden` in Boerhaave's Energiemeter WP opmerking** — intent?
2. **`Voeding` vs `Gateway` vs bare `Levering derden`** in ZRD — three scopes
   or spelling variation?
3. **Convention parameter** — per-project `derden_marker_scope`, or is the
   convention per-row?
4. **`Lev. 3e` shorthand** — Kuijpers-house convention?
5. **NEW: is 2195-06's uniformity typical of Priva-layout projects?** If the
   convention is stable per client rather than per project, a
   `derden_marker_scope` parameter becomes much more attractive.

---

### Rule 2 — Energy Valve → RAK SIGN KAB 4x0,8
**Status:** one observation. Do not encode yet. *(unchanged)*
**Evidence:** project 7268, 8 rows.

**Proposed cable.** `RAK SIGN KAB CCA 4X0,8 HA500`.

**Confirmation needed.** B2CA equivalent unknown; whether `voeding` is always
this control cable.

**NEW note:** see Section 6 Q10 — 2195-06 shows `RAK SIGN KAB` may actually be
`DRAKSIG KAB`. If that spelling is wrong in the config it affects this rule too.

---

### Rule 3 — BACnet Delta Controls → UTP CAT6 CS34ZB HA305
**Status:** one observation. Do not encode yet. *(unchanged)*
**Evidence:** project 7268, 5 rows plus Naregelingen row.

**Proposed cable.** `COMM U/UTP CAT6 CS34ZB HA305` (note `CS34ZB`, not
`CS34ZC`).

**Alternative** — register in `4_Bus` so the existing chain logic
(`doorlussen`) fires automatically.

---

### Rule 4 — Warmtepomp diverse functies → 6x2x0,8 (CCA)
**Status:** one observation, strongest case for encoding. *(unchanged)*
**Evidence:** project 7268, r1.

**Proposed cable.** `DRAK SIGK CCA 6X2X0.8 MT` (decimal point, not comma —
preserve exactly).

**NEW note:** 2195-06 shows the same *bundling concept* on pumps
(`DRAK SIG B2CA GY 4X2X0.8 HA500` for "diverse functies") — see Section 6 Q7.
This strengthens the general "diverse functies = one bundled cable" pattern
even though the specific WP cable is still one observation.

---

## Section 2 — Conflicts held from the master dictionary (Standaarden CCA)

### Conflict A — Transportpomp voeding *(unchanged)*
| Source | Cable |
|---|---|
| Standaarden CCA | `4g1,5` |
| Duitslandlaan / Fonkel / Tilburg (validated) | `4g2,5` |

Three projects vs one line of standard. Ask Rick.

### Conflict B — Ketel vrijgave/storing/sturing 0-10V *(unchanged)*
| Source | Cable |
|---|---|
| Standaarden CCA | one `2x2x0,8` |
| Duitslandlaan (validated) | split: `5X1` + `2X1` |

### Conflict C — Warmtepomp meldingen — **STRENGTHENED**
| Source | Cable |
|---|---|
| Standaarden CCA | `6x0,8` per storing signal |
| Duitslandlaan / Fonkel (validated) | one bundled `12X1` |
| **2195-06 (pumps, not WP)** | **one bundled `6X0,8` / `4X2X0.8`** |

Standard counts per-signal; three projects now bundle. 2195-06 extends the
pattern beyond warmtepompen to pumps generally. See Section 6 Q7.

### Conflict D — Warmte-/koudemeter voeding *(unchanged)*
| Source | Cable |
|---|---|
| Standaarden CCA | `3g1,5` |
| Boerhaave (validated) | `3X1` stuurstroom |
| 7268 | `3g2,5` |

### Conflict E — Warmtewiel voeding *(unchanged)*
| Source | Cable |
|---|---|
| Standaarden CCA | `3g1,5` |
| 7268 (row 56, LBK) | `3G2,5` |

### Conflict F — Wateroverlastdetectie — **NEW**
| Source | Cable |
|---|---|
| `2_Kabelkeuze` row 38 comment | `1x2x0,8` |
| Same comment, CV Transport section | `4x0,8` |
| **2195-06 manual (10 rows)** | **`DRAK SIGK 1X4X0,8 B2CA HA500`** |

Third value. Ask Rick which applies where.

### Conflict G — Werkschakelaar melding — **NEW**
| Source | Cable |
|---|---|
| `2_Kabelkeuze` row 44 | `4X0,8` (both families) |
| **2195-06 manual (12 rows)** | **`DRAK B2CA GY 2X0,8 MT`** |

### Conflict H — Tracing voeding — **NEW, two observations**
| Source | Cable |
|---|---|
| Standard / most projects | `5G2,5` |
| Fonkel | `3G2,5` |
| **2195-06 (7 rows)** | **`3G2,5`** |

Two projects now use `3G2,5`. **We cannot see what distinguishes them from
the `5G2,5` projects** — nothing in the input differs. Ask Rick.

---

## Section 3 — Standing questions from earlier projects

### Q1 — `Totaal aantal werkschakelaars` = 0 — **STRENGTHENED, priority lowered**
The manual shows `0` in the totals row while individual ws entries appear on
10 (Duitslandlaan) / 8 (Fonkel) / 0 (Boerhaave, consistent) / ~8 (7268) /
**17 (2195-06)** rows.

**Four projects, same contradiction.** Strong enough to ask Rick to confirm
"always 0" as a convention rather than keep it open.

**Priority note (2026-07-30):** ws quantity does **not** affect the wire list,
which is the evaluation target. This is now a cosmetic/reporting question, not
an accuracy blocker.

### Q2 — Sheet-to-panel merge (Tilburg) *(unchanged)*
Needs a second observation.

### Q3 — Naregelingen BOM writer — **STRENGTHENED**
Confirmed across Tilburg + 7268 + ZRD, and now **2195-06**, which produces
electrode (`APA/PP/R-1-V/2-`) and bracket (`Muurbeugel RVS`) rows — exactly
the aggregated `Stuks | onderdeel | wcd | totaal | materiaal | bekabeling naar`
material. Four projects. Buildable; still batched.

---

## Section 4 — Resolved code bugs

### Bug — `POMP_230V` feed cable does not emit (RESOLVED 2026-07-21)
Root cause: `_parse_electrical_spec()` returned voltage/current as strings
while `rules._naar_feed()` uses `f"{current_a:g}"`, which requires float.
Fixed in `ingest.py`. Verified on 7268: 48% blind after fix.

---

## Section 5 — Rule-hygiene issues to fix opportunistically

- **12 over-emitted `DRAK CCA GY 2X0,8` rows on 7268** — `KLEP_STURING_MELDING`
  fallback firing where more specific types should match.
- **`WEERSTATION_BUS` cable choice** — `DRAK SIGK CCA 1X2X0,64 MT` is the CCA
  notation for the same physical cable as the BMS Cable. Verify or split.
- **CS34ZB vs CS34ZC** — if functionally identical, consolidate.
- **NEW: `RAK SIGN KAB` vs `DRAKSIG KAB`** — the config uses `RAK SIGN KAB` in
  three rows; 2195-06's manual writes `DRAKSIG KAB`. Possibly a dropped `D`.
  Ask Rick which is the correct product name.
- **NEW: config tab-character hygiene** — pasted cells in `1_Synoniemen` and
  `2_Kabelkeuze` picked up literal tabs, and one functietype was typo'd
  (`MELTING_BUS`). Both produced silent lookup failures. Worth a validation
  pass that checks every `functietype` in `1_Synoniemen` resolves somewhere.
  **Note:** a naive "must exist in `2_Kabelkeuze`" assertion is WRONG — see
  Section 6 Q11.

---

## Section 6 — NEW from project 2195-06 (Priva layout, B2CA, RK1)

### Bug B1 — `STRUCTURAL` types hijacked by remark text (PARTIALLY FIXED)

`classify_row` builds its match string as
`f"{omschrijving} {type} {opmerking}"` — one blob. A `STRUCTURAL` functietype
mentioned in a **remark** therefore becomes primary and hits an early `return`
in `emit()`, producing **no cable and no flag**.

Observed: `Voeding 230Vac uit regelkast` on six pump rows classified as
`REGELKAST`, silently absorbed into the panel row via `_device_key`'s
"at most one panel row per RK" grouping. Six feeds lost, invisibly.

**Fixed 2026-07-30** by extending the existing `DERDEN` demotion at
`classify.py` line 28 to cover `REGELKAST`, guarded on the word not appearing
in `omschrijving`:

```python
if len(hits) > 1 and (hits[0] == "DERDEN" or
                      (hits[0] == "REGELKAST" and "regelkast" not in norm.omschrijving.lower())):
```

**STILL EXPOSED: `BRANDMELDING` and `BUS_INTERFACE`.** Both are in
`STRUCTURAL`, both early-return in `emit()`. 2195-06's missing BACnet/BMS
cable (`LS-01 Koppeling met legionella spoelautomaat`, which was emitted as a
section banner rather than a device) is a likely instance. **Not yet
investigated.**

### Bug B2 — Bus-connected sensors rejected by the AI gate (FIXED)

`_ok()` rejected `METING_PASSIEF` when `n.AI` was empty. NW-sens temperature
sensors (`NSB8BTN040-0`) report over the bus and occupy no analogue input, but
Erco still runs a cable. Ten rows produced nothing.

Controlled comparison within the project:
- `TT-61` = `STS-6370S-002` (Klemband), AI=1 → cable emitted ✓
- `TT-11` = `NSB8BTN040-0` (NW-sens), no points → nothing ✗

**Fixed 2026-07-30** with a new function type rather than a code exemption, so
the knowledge lives in config:
- `1_Synoniemen`: `nsb8btn` and `nw-sens` → `METING_BUS`, priority 70
- `2_Kabelkeuze`: new `METING_BUS` row
- `rules.py`: `METING_BUS` added to `sig_priority` before `METING_PASSIEF`
- `rules.py`: `_ok()` exempts `METING_BUS` from the AI requirement

**The AI check is retained for everything else** — it is what correctly
declines the three `Muurbeugel RVS` bracket rows.

**Cable strings PROVISIONAL:** B2CA value taken from the 2195-06 manual
(`DRAK SIGK 1X4X0,8 B2CA HA500`); CCA value copied from `METING_ACTIEF`
(`DRAK SIGK CCA 1X4X0,8 2502Q MT`). Neither confirmed by Rick.

### Q5 — DRAK × B2CA has no column (BLOCKING)

`config.py` line 37 selects `row["kabel_B2CA_JOBA"]` or
`row["kabel_CCA_DRAK"]`. **The brand is baked into the schema**, but Rick has
confirmed brand and fire class are independent axes.

2195-06 uses **DRAK cable types at B2CA fire class**, which cannot be
expressed. Neither column reproduces the manual:
- the CCA column has the right type codes at the wrong fire class
- the B2CA column has the right fire class but JOBA type codes, and is much
  coarser (`JOBA ST.STR B2CA HCHOZ 2X1 MT` covers **seven** function types)

**Measured on 2195-06 (114 manual wires):**

| Config state | Score |
|---|---|
| CCA | 2/114 = 2% |
| B2CA/JOBA | 13/114 = 11% |
| B2CA/JOBA + `METING_BUS` | ~23/114 = 20% |
| CCA + hypothetical token swap | 43/114 = 38% |
| ...also tolerating the sensor suffix | 54/114 = 47% |

**Questions for Rick:**
1. For the DRAK GY cables (`2X0,8`, `4X0,8`, `6X0,8`, `8X0,8`), is the B2CA
   version our CCA entry with the fire class swapped? (43 wires)
2. Passive temp sensor: manual `DRAK SIGK 1X4X0,8 B2CA HA500`; our CCA
   *passive* is `1X2X0,8 2501 MT`, our CCA *active* is `1X4X0,8 2502Q MT`.
   Which is the B2CA passive? (22 wires)
3. `DRAKSIG KAB B2CA GY 1X2X0,8 MT` — our CCA rows say
   `RAK SIGN KAB CCA 4X0,8 HA500`. Same product, different size? (10 wires)
4. `DRAK SIG B2CA GY 4X2X0,8 HA500` — no entry in either column. (8 wires)
5. **The suffix flips in both directions between families** —
   `2502Q MT`→`HA500` on the sensor, `HA500`→`MT` on the feed. Product-line
   rule, or per-cable?

**If confirmed, the fix is a config change** (a third column plus a family
selector), not code — consistent with the design principle that estimators
extend coverage via `kabelconfig.xlsx`.

### Q6 — Point-less rows are a Priva-layout characteristic

**26 of 114 rows** in 2195-06 carry no AI/AO/DI/DO. Verified against the source
PDF's own subtotals — this is how the document is written, not a parse defect.

| Class | Rows | Status |
|---|---|---|
| `NSB8BTN...` NW-sens temp | 10 | **FIXED** — see Bug B2 |
| `Voeding 230Vac uit regelkast` | 6 | **FIXED** — see Bug B1 |
| `APA/PP/R-1-V/2-` electrode (aantal=4) | 3 | blocked — see Q9 |
| `Derden` luchtklepservo | 3 | open — `DERDEN` is `STRUCTURAL`, see B1 |
| `Datakoppeling` BACnet | 1 | open — see B1, `BUS_INTERFACE` |
| `Muurbeugel RVS` brackets | 3 | correct to decline (BOM material, see Q3) |

**Design note:** do NOT relax the point gates wholesale. That would emit
cables for mounting brackets and silence `NO CABLE DERIVED`, the only signal
that a row went unhandled. Each class needs positive recognition.

### Q7 — Bundling: one cable per physical run vs one per I/O point

The manual emits **one cable per physical run**; the pipeline emits **one per
I/O point**. Three instances in 2195-06:

| Manual | Pipeline | Manual wires | Pipeline wires |
|---|---|---|---|
| 3 level alarms → one `DRAK B2CA GY 6X0,8 MT` per pump | 3 × `2X0,8` | 7 | 21 |
| Pump functions → one `DRAK SIG B2CA GY 4X2X0.8 HA500` | 3 × `2X0,8` | 7 | 21 |
| Sprinklermeldcentrale 4 signals → one `4X2X0.8` | 3 × `2X0,8` | 1 | 3 |

**~15 manual wires against ~45 emitted — the largest single block in the diff.**

The mechanism partly exists: `MELDINGEN_GROOT` bundles WP meldingen into
`JOBA HCH-JZ 12X1 B2CA MT`, validated on Duitslandlaan and Fonkel. But
`_device_key` only groups `REGELKAST`, `WARMTEPOMP` and `E_KETEL` — everything
else returns `None` and stays distinct, deliberately (Boerhaave's three heat
pumps must not collapse).

**Visible pattern:** two cores per signal (3 alarms → 6-core, 4 signals →
4×2). One project only.

**Ask Rick:** do device meldingen always bundle, and what sets the core count?

### Q8 — Per-put vs per-pump replication

`pr-601` covers Vuilwaterpomp 1 **and** 2, with **one** shared `LV-01 Tracing`
and **one** `LA-01`/`LA-02` between them. The manual gives each pump its own
tracing voeding, tracing storing, niveau alarm and werkschakelaar.

Source has 4 `LV-01` rows; manual has 7 tracing voedingen + 7 tracing
storings. The input contains the information; what is missing is a rule that
**replicates per-put items across the pumps in that put** — the mirror image
of `dedupe_devices`.

One observation. Ask Rick.

### Q9 — Electrode `aantal` as cable-count driver

Source says `aantal=4` at all three wateroverlast locations. Manual emits
**4 + 4 + 2**. The sprinklerpompruimte pair does not multiply out.

Note `rules.py` line 202 already implements `aantal` as a multiplier, scoped to
`BRANDKLEP`, `METING_PASSIEF` and `METING_ACTIEF`. Extending it to
`WATEROVERLAST_ONDERSTATION` would get two of three locations right and
overshoot the third by two.

**Do not encode until the 4-vs-2 is explained.** Ask the project contact.

### Q10 — Panel-internal meldingen (one observation, self-serviceable)

Five rows in 2195-06 carry a real DI=1, emit `DRAK CCA GY 2X0,8 MT`, and have
**no cable in the manual**:

`RS-01` Reset drukknop · `NW-01` Netwachter · `IA-01` Installatie automaten ·
`SS-01` Stuurstroom · `OSB-01` Overspanningsbeveiliging **regelkast**

The discriminator is physical: `OSB-02` (verdeel**kast**) *does* get a wire.
Panel-internal meldingen do not leave the cabinet, so there is no cable to run.

**Second observation is obtainable without Rick** — check whether
Duitslandlaan, Boerhaave or Fonkel wire any of these device names. If none do,
encode as a panel-internal class and let the merge gate confirm.

**Removes 5 false wires.**

### Q11 — Do NOT assert "every synonym type exists in `2_Kabelkeuze`"

A tempting merge-gate assertion, and **wrong**. Function types resolve through
several paths:

- `2_Kabelkeuze` — most signal types
- `3_Voedingen` — e.g. `TRACING`
- `5_Vaste_teksten` — e.g. `REGELKAST`
- **code** — `VRIJGAVE` is remapped to `MELDING` at `rules.py` lines 198–199;
  `NTB`, `WARMTEPOMP`, `METER_OPTIE_VOELER`, `EVERDELER_METER`, `ENERGIEMETER`
  each have a dedicated dispatch branch with an early `return`

A set-difference of tab-1 against tab-2 returns ten names, of which only two
were real problems. The assertion would fail on working configuration.

A useful guard would have to check all four tabs plus an explicit exempt list —
bigger than it looks. Recorded so nobody re-proposes the naive version.

### Q12 — Tracing panel assignment (affects Fonkel)

On **Fonkel** the tracing is fed from a **separate tracing panel** with its own
page (own Voedingen, derden=0, 2 cables, no RK code). On **2195-06** the
tracing is fed from the RK itself, 7 times.

`optioneel vanuit regelkast` on Fonkel's `Tracing leidingen bovendaks` row was
being misclassified as a panel row, which suppressed its feed and happened to
match the RK071 list. Bug B1's fix corrected the classification, so the feed is
now emitted — and the Fonkel fixture was updated to expect it (`op dak` 2→3,
`DRAK HULT B2CA 3G2,5 MT` 4→5), on the basis that **cables score as a set,
independent of which page they appear on**.

**Ask Rick:** is the tracing panel a per-project choice, or does something
determine it (pipe run, load, location)? `tracing_scope` already exists as a
parameter (`erco / derden`) — a third value may be all that is needed.

### Q13 — Pump feed core count

All seven pumps in 2195-06 carry the same remark, `Voeding 230Vac uit
regelkast`. The manual gives:
- 4 × vuilwaterpomp → `DRAK HULT B2CA 3G2,5 MT`
- 3 × hemelwaterpomp → `DRAK HULT B2CA 4G2,5 MT`

Nothing in the row distinguishes them except the `VWP-`/`HWP-` tag. A 4-core on
a 230V single-phase supply is unusual — `_feed_class` treats 4-core as
`400V_3F_zonder_N`.

**Ask Rick:** are the hemelwaterpompen actually 400V? Should `POMP` split into
two function types, or should the tag prefix be read?

---

## Section 7 — Document discrepancies for the project contact (not Rick)

Both affect the denominator, so every reported score depends on them.

### D1 — Hemelwaterpompen: 2 in the functielijst, 3 in the manual
`pr-603` (trappenhuis) and `pr-604` (vluchtgang) each contain one `HWP-01`.
The manual has three, with rows 79–84 **and** 85–90 both labelled
`Hemelwaterpomp trappenhuis K1-003`.

**Six manual wires the functielijst cannot produce.** Duplicated section, or a
pump missing from the functielijst? If duplicated, the honest total for
2195-06 is **108, not 114**.

### D2 — Wateroverlast electrodes: 4/4/4 vs 4/4/2
See Q9.

### D3 — Input hygiene
- `NSB8BTN040-0` vs `NSB8BTNO40-0` (digit zero vs letter O) splits ten
  identical sensors 5/5 in the parse
- OCR residue surviving correction: `spoeleutomaat`,
  `sprinklerpompuitmte`, `sprinklermeldventrale`
- `NSA-ruimte K1-003` in the functielijst vs `K1-001` in the manual

---

## Section 8 — Evaluation conventions (recorded 2026-07-30)

- **Cables score as a set.** Order, page, and panel assignment do not matter;
  the set of emitted cables must match the set in the manual. This is what made
  the Fonkel fixture wrong rather than the code in Q12.
- **`ws` quantities do not affect the score.** See Q1.
- **Blind accuracy** = correct wires / total manual wires, bucketed by cable
  string with `min(pipeline, manual)` per bucket. Be explicit about RK-only vs
  full manual.
- **Bucketed `min()` counting hides overshoot.** 2195-06's `2X0,8` bucket is
  43 emitted against 26 in the manual; the score credits 26 and says nothing
  about the 17 extra. Report overshoot separately.
- **Do not conflate projects.** 7268's 48% is not ZRD's 48%.
- **Do not report a gain within counting noise**, e.g. between two
  transcriptions of the same manual.