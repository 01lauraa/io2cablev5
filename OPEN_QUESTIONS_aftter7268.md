# Open questions & candidate rules

Rules identified during project validation but **not yet encoded**. Each entry
records the pattern, the proposed encoding, and what would need to happen before
adding it to `kabelconfig.xlsx`. Per the validation protocol: never encode a rule
from a single observation.

**Last updated:** 2026-08-21, after validating project 7-nieuw (muziekschool +
sport, scanned PDF, 96 wires) and ingesting project 7277 (two-row header).
Four answers from Rick encoded. See Section 0e.

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

## Section 0b — What changed on 2026-07-31 (project 1363 + Rick's answers)

**Project 1363** (Kuijpers `I-GA-78-FL--1RK00.xls`, three sheets merged:
`061 TG XL`, `RK 861`, `RK Algemeen`). Manual is **four panels** — RK-ALGMN
(108 rows), RK161 (13), RK861 (22), NEXT (17) — **160 wires total**.

| Run | Score |
|---|---|
| `brandklasse=CCA` (inherited from 2195-06, wrong) | 21/160 = 13% |
| `brandklasse=B2CA` | **72/160 = 45%** |

**Best blind first-pass score on any project to date.** No code changes; the
51-wire gain was one parameter. Exact matches: `JOBA ST.STR B2CA HCHJZ 5X1 MT`
20/20, `Via aansluitsnoer van 2 meter op meter` 6/6,
`JOBA ST.STR B2CA HCHOZ 2X1 MT` 34/47, BMS Cable 9/12.

**No new code changes shipped.** The four remaining blocks (below) are all
questions, not bugs.

**Rick answered three dictionary questions** — see Section 9. One is
actionable, two need follow-up before encoding.

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

## The name-based synonym list — **PARTLY FALSIFIED 2026-07-31**

Previously recorded as "unambiguous across the projects that contain them" and
safe to encode as derden terminations:

`kWh-meter` · `roldeur` · `vluchtdeur` · `overspanningsbeveiliging` ·
`dali verlichting` · `terreinverlichting` · `veegpuls verlichting` ·
`schemerschakelaar` · `buitenverlichting` · `gevelverlichting` ·
`knx verlichting` · `miva` · `liftinstallatie` · `lift storing` ·
`wcd vrijgave` · `inbraakcentrale` · `verkeerslicht`

Cable: `Kabel levering derde totaan RK, aansluiten kastzijde Erco`.

### `overspanningsbeveiliging` is DISPROVEN — remove it

An earlier revision of this file claimed none of these names appear in
2195-06. **That was wrong.** 2195-06 gives the same device name three
different outcomes:

| Row | Manual outcome |
|---|---|
| `OSB-02 Overspanningsbeveiliging verdeelkast` | `DRAKSIG KAB B2CA GY 1X2X0.8 MT` — a **real Erco signal cable** |
| `OSB-01 Overspanningsbeveiliging regelkast` | **no cable at all** — panel-internal, see Q10 |
| 7268 / ZRD | derden termination |

Encoding `overspanningsbeveiliging -> derden` would produce two wrong rows on
2195-06 and mask the panel-internal finding. **This is the marker-based Rule 1
failure reappearing in the name-based version:** same string, different
outcomes, no discriminator in the data except `regelkast` vs `verdeelkast`.

### The remaining sixteen names are UNVERIFIED, not safe

The list was compiled from 7268 and ZRD, before 2195-06 and 1363 existed, and
was never re-checked against them. Since one of seventeen entries turned out to
be wrong the first time a third project was consulted, the rest are
**one-context observations** until the same check is run.

**Required before encoding** — grep every manual and normalized.csv for each
name, and drop any that appears with a different outcome anywhere:

```powershell
python -c "
import pandas as pd,glob
names=['kwh-meter','kwh meter','roldeur','vluchtdeur','dali','terreinverlichting','veegpuls','schemerschakelaar','buitenverlichting','gevelverlichting','knx','miva','liftinstallatie','lift storing','wcd vrijgave','inbraakcentrale','verkeerslicht']
for f in glob.glob(r'projects\*\normalized.csv'):
    d=pd.read_csv(f,dtype=str).fillna('')
    blob=d.astype(str).agg(' '.join,axis=1).str.lower()
    for nm in names:
        hit=blob.str.contains(nm,regex=False)
        if hit.any(): print(f,'|',nm,'|',hit.sum(),'rows')
"
```

### The impact estimate is stale

"7268 ~37% -> ~50%, ZRD ~17% -> ~35%" predates the transportpomp feed fix
(7268 is now 48%) and was never re-measured. Neither 1363 nor 2195-06 contains
any of these names apart from the disproven one, so this work improves neither
current project. **Low priority** relative to the mechanism-level bugs in
Section 6.

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

### Rule 2 — Energy Valve → 4x0,8 + Modbus — **CONFIRMED BY RICK 2026-07-31**
**Status:** cable value confirmed by Rick; still blocked on two details.
**Evidence:** 7268 (8 rows) + Rick's confirmation, see R1 in Section 9.

**Cable.** `4x0,8` — CCA form `RAK SIGN KAB CCA 4X0,8 HA500` — **plus a Modbus
koppeling.** The Modbus half is new information from Rick and was not part of
the original rule.

**Still blocked on:**
1. **B2CA equivalent** — no validated project supplies it.
2. **Which Modbus cable** — the standard BMS Cable, or the `CS34ZB` variant
   from Rule 3? This also bears on whether Rule 3's trigger can ship.

**Spelling caveat:** 2195-06 writes `DRAKSIG KAB` where the config writes
`RAK SIGN KAB` — possibly a dropped `D`. If the config spelling is wrong, this
rule's CCA value inherits the error. See Section 11 item 11.

---

### Rule 3 — BACnet / RK-onderling → UTP CAT6 **CS34ZB** — **SECOND OBSERVATION 2026-07-31**
**Status:** two observations for the cable string; the *trigger* is still one.
**Evidence:**
- 7268: 5 BACnet Delta Controls rows + Naregelingen `Communicatie Delta Controls`
- **1363 `NEXT` panel: 16 x `COMM U/UTP CAT6 CS34ZB HA305`** for
  `Datacommunicatiekabel regelkast RK<nnn>`

**Cable.** `COMM U/UTP CAT6 CS34ZB HA305` — note `CS34ZB`, not `CS34ZC`.

**This upgrades the CS34ZB/CS34ZC hygiene item** (Section 5) from "consolidate
if identical" to a probable config error: two independent projects, two
different contexts (field BACnet chain, RK-onderling communicatie), same
string — while the config's `COMM_RK_ONDERLING` says `CS34ZC` and is
contradicted by 1363's manual on 16 rows.

**Ask Rick to confirm before changing `COMM_RK_ONDERLING`.** The two projects
agree with each other but disagree with whoever entered `CS34ZC`, and both
cables may legitimately exist for different purposes.

**Trigger still open.** 1363's 16 rows are not derivable from I/O at all (see
Q15), so registering the cable in `4_Bus` does not by itself generate them.

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

### Conflict A — Transportpomp voeding — **CLOSED 2026-08-18**

The reissued CCA dictionary moves `Transportpomp voeding` from `4g1,5` to
`4g2,5`, along with every other `1,5` cross-section in the document. The three
validated projects were right and the standard was stale. `3_Voedingen` already
held `2,5`, so **no config change was needed** — the pipeline had been correct
all along.

The load-based reading below still stands and is the general answer (see Q18);
this entry is closed only in the sense that the standard no longer disagrees.

Original 2026-07-31 reframing follows.
| Source | Cable | Load |
|---|---|---|
| Standaarden CCA | `4g1,5` | unspecified |
| Duitslandlaan / Fonkel / Tilburg (validated) | `4g2,5` | unspecified |
| **1363 `161CP_11/12` transportpomp** | **`4G6`** | **22 kW / 39,2 A / 400V** |
| **1363 `091CP_21` transportpomp ketelcircuit** | **`3G2,5`** | **0,76 kW / 3,45 A / 230V** |

**This may not be a conflict at all.** 1363 shows the same device type taking
`4G6` at 22 kW and `3G2,5` at 0,76 kW, which suggests cross-section is a
function of **load, not device type**. If so, `4g1,5` and `4g2,5` are both
correct at different loads and the "conflict" is an artefact of comparing
cables without their currents.

Supersedes the earlier reading. See **Q18** — ask Rick for the sizing table
rather than which single value is authoritative.

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

### Conflict D — Warmte-/koudemeter voeding — **FOURTH VALUE 2026-07-31**
| Source | Cable |
|---|---|
| Standaarden CCA | `3g1,5` (power) |
| Boerhaave (validated) | `3X1` stuurstroom |
| 7268 | `3g2,5` (power) |
| **1363 (`072EM11`, `062EM01`, `061EM01`)** | **`JOBA STUURSTR HHJZ 4X1 MT`** ×3 |

1363 sides with Boerhaave on *stuurstroom rather than power*, but at `4X1`
rather than `3X1`. So: two sources say power cable, two say stuurstroom, and
the two stuurstroom answers disagree on core count.

Note 1363 pairs each meter voeding with a separate `4-20mA sturing` row
(`JOBA ST.STR B2CA HCHOZ 2X1 MT`) — a two-cable pattern the config does not
model. Worth showing Rick alongside the question.

### Conflict E — Warmtewiel voeding — **CLOSED 2026-08-18**
| Source | Cable |
|---|---|
| Standaarden CCA (old) | `3g1,5` |
| 7268 (row 56, LBK) | `3G2,5` |
| **Standaarden CCA (reissued)** | **`3g2,5`** |

Same stale-value artefact as Conflict A. `2_Kabelkeuze` row 22
(`WARMTEWIEL_VOEDING`) updated to `3G2,5` in all four family columns. **Closed.**

### Conflict F — Wateroverlastdetectie — **NEW**
| Source | Cable |
|---|---|
| `2_Kabelkeuze` row 38 comment | `1x2x0,8` |
| Same comment, CV Transport section | `4x0,8` |
| **2195-06 manual (10 rows)** | **`DRAK SIGK 1X4X0,8 B2CA HA500`** |
| **7222 manual (2 rows)** | **`DRAK SIGK 1X4X0,8 B2CA HA500`** |

**Fourth value, but two projects now agree.** 7222 and 2195-06 both use
`1X4X0,8`, against the reissued dictionary which still carries **two** values
(`4x0,8` under CV Transport, `1x2x0,8` under Onderstation algemeen). Ask Rick
which applies where.

### Conflict G — Werkschakelaar melding — **NEW**
| Source | Cable |
|---|---|
| `2_Kabelkeuze` row 44 | `4X0,8` (both families) |
| **2195-06 manual (12 rows)** | **`DRAK B2CA GY 2X0,8 MT`** |

### Conflict H — Tracing voeding — **CLOSED 2026-08-18 at `5G2,5`**

The reissued dictionary confirms `5g2,5`, and 7222's manual uses `5G2,5` on six
rows. The `3G2,5` cases on Fonkel and 2195-06 are most likely smaller loads
(Q18) rather than a different rule.

**Follow-up:** `3_Voedingen`'s `TRACING` row has CCA `5G2,5` but B2CA `3G2,5`.
The B2CA cell looks wrong — ~6 wires on 7222. Added to Section 11.

Original entry follows.
| Source | Cable |
|---|---|
| Standard / most projects | `5G2,5` |
| Fonkel | `3G2,5` |
| **2195-06 (7 rows)** | **`3G2,5`** |
| 1363 | *no tracing rows — neither confirms nor contradicts* |

Two projects use `3G2,5`. **We cannot see what distinguishes them from the
`5G2,5` projects** — nothing in the input differs.

**Possible link to Q18:** if cross-section scales with load, `5G2,5` vs
`3G2,5` may be a core-count difference (5-core vs 3-core) driven by whether the
tracing circuit is three-phase. Speculative; do not encode. Worth asking in the
same breath as the sizing table.

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
- **CS34ZB vs CS34ZC** — **UPGRADED 2026-07-31.** Two projects (7268, 1363)
  write `CS34ZB`; `COMM_RK_ONDERLING` says `CS34ZC` and is contradicted by
  1363's manual on 16 rows. No longer a "consolidate if identical" item — it is
  a probable config error. See Rule 3.
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

**Cable strings PROVISIONAL — and now CONTRADICTED.** B2CA value taken from
the 2195-06 manual (`DRAK SIGK 1X4X0,8 B2CA HA500`); CCA value copied from
`METING_ACTIEF` (`DRAK SIGK CCA 1X4X0,8 2502Q MT`). Both are `1x4x0,8`.

**On 2026-07-31 Rick confirmed ruimtetemperatuur = `1x2x0,8`** (see R2,
Section 9), matching the dictionary and the existing `METING_PASSIEF` entry.
Either 2195-06's manual deviates on these rows, or a bus-connected sensor is
genuinely a different cable. **Unresolved — follow-up sent.**

The classification fix stands regardless: ten rows that previously emitted
nothing now emit a cable. Only the string is in doubt.

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

**PARTIALLY CLOSED 2026-08-18.** The *signal* half is answered — see Section 0d,
the pump signal rule. The *feed* half stays open and folds into Q18 (load-based
sizing): nothing in the row distinguishes a `3G2,5` pump from a `4G2,5` one
except the tag prefix.

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

---

## Section 8b — Re-audit log, 2026-07-31

Every pre-existing entry was re-tested against project 1363 and Rick's answers,
rather than only appending new findings. Result:

| Entry | Verdict |
|---|---|
| **Rule 1 name-based list** | **PARTLY FALSIFIED.** `overspanningsbeveiliging` disproven by 2195-06 (three outcomes for one name). Remaining sixteen names downgraded to unverified. A prior revision of this file wrongly stated none of these names appear in 2195-06. |
| **Rule 2 (Energy Valve)** | **CONFIRMED** by Rick, but scope grew — a Modbus cable comes with it. Still blocked on B2CA equivalent + which Modbus cable. |
| **Rule 3 (CS34ZB)** | **SECOND OBSERVATION** from 1363's NEXT panel. Cable string now well supported; trigger still one observation. |
| **Rule 4 (WP diverse functies)** | Unchanged. 1363 has no WP rows. |
| **Conflict A (transportpomp)** | **REFRAMED.** 1363 shows `4G6` at 22 kW and `3G2,5` at 0,76 kW for the same device type — probably a load-sizing question (Q18), not a conflict. |
| **Conflict B (ketel)** | Unchanged. 1363's ketel rows use `HHJZ 5X1` + `HCHOZ 2X1`, consistent with Duitslandlaan's split reading rather than the standard's single `2x2x0,8`. Weak support for the validated side. |
| **Conflict C (WP meldingen)** | Unchanged since the 2026-07-30 strengthening. |
| **Conflict D (meter voeding)** | **FOURTH VALUE.** 1363 gives `JOBA STUURSTR HHJZ 4X1 MT`. |
| **Conflict E (warmtewiel)** | Unchanged. No warmtewiel rows in 1363 or 2195-06. |
| **Conflict F (wateroverlast)** | Unchanged. No wateroverlast rows in 1363. |
| **Conflict G (werkschakelaar)** | Unchanged. No werkschakelaar melding rows in 1363. |
| **Conflict H (tracing)** | Unchanged; 1363 has no tracing rows. Possible link to Q18 noted. |
| **Q1 (ws = 0)** | Unchanged. 1363 shows `Totaal ws = 0` on all four panels while individual rows carry ws=1 — a **fifth** project, but the priority stays low since ws does not affect the wire list. |
| **Q2 (sheet-to-panel merge)** | **SECOND OBSERVATION** — 1363's single input produces four panels. See Q19. |
| **Q3 (Naregelingen BOM)** | Unchanged. 1363 has no BOM-material rows. |
| **Q5 (DRAK x B2CA)** | **SHARPENED** by Q17 — the problem may be that fire class is per-cable, not that a third column is missing. |
| **Q6 (point-less rows)** | Unchanged; specific to the Priva layout. 1363 (Kuijpers) has none. |
| **Q7 (bundling)** | Unchanged. 1363 emits one cable per signal, matching the pipeline — so bundling is **not** universal across clients. Mild evidence against a global rule. |
| **Q9 (electrode aantal)** | Unchanged. |
| **Q10 (panel-internal)** | **STRENGTHENED indirectly** — the `overspanningsbeveiliging` finding depends on it (`regelkast` internal, `verdeelkast` wired). |
| **Q11 (no naive tab-2 assertion)** | Unchanged and still correct. |
| **Q12 (tracing panel)** | Unchanged. |
| **Q13 (pump feed cores)** | **POSSIBLY SUBSUMED** by Q18 — if cross-section scales with load, `3G2,5` vs `4G2,5` may be a load question rather than a device-type question. |
| **Section 5 hygiene: CS34ZB/ZC** | **UPGRADED** to a probable config error. |
| **Section 5 hygiene: `RAK SIGN KAB`** | Unchanged, still unconfirmed. |

**Process note.** The `overspanningsbeveiliging` error persisted through two
revisions of this file because new projects were appended without re-testing
existing claims. Every future update should re-run this audit rather than only
adding sections.

---

## Section 9 — Rick's answers, 2026-07-31

### R1 — Energy Valve → 4x0,8 **plus a Modbus cable** (CONFIRMS Rule 2)

Rick confirms the Energy Valve cable is `4x0,8` and that it also carries a
Modbus koppeling.

This **promotes Rule 2** (Section 1) from one observation to confirmed by the
standard. The Modbus half also confirms the territory of Rule 3.

**Still needed before encoding:**
1. **B2CA equivalent** — Rule 2 records this as unknown, and no validated
   project supplies it.
2. **Which Modbus cable** — the standard
   `BMS Cable 2x2x24AWG - R1319 - B2ca s1,d0,a1 Violet HA500`, or the Delta
   Controls `COMM U/UTP CAT6 CS34ZB HA305` variant from Rule 3?

Once those two are answered, Rule 2 can ship as a config-only change.

### R2 — Ruimtetemperatuur → `1x2x0,8` (CONFIRMS existing encoding, but
### CONFLICTS with the 2195-06 `METING_BUS` provisional value)

Rick confirms `1x2x0,8`, matching both the dictionary and the config's existing
`METING_PASSIEF` CCA value `DRAK SIGK CCA 1X2X0,8 2501 MT`. Nothing to change
for normal passive sensors.

**But this contradicts the `METING_BUS` row added on 2026-07-30.** That row's
B2CA value is `DRAK SIGK 1X4X0,8 B2CA HA500`, taken from the 2195-06 manual's
ruimtetemperatuuropnemers, and its CCA value was copied from `METING_ACTIEF`
(`1X4X0,8 2502Q`). Both are `1x4x0,8`, not `1x2x0,8`.

Two possible readings, and we do not know which:
- 2195-06's manual deviates from the standard on these rows, or
- a **bus-connected** sensor (NSB8BTN, no AI) is genuinely a different cable
  from a normal passive sensor

**Follow-up for Rick:** *"2195-06 uses NSB8BTN network sensors with no AI, and
its manual gives them `1x4x0,8`. Is that different from a normal
ruimtetemperatuuropnemer, or should they also be `1x2x0,8`?"*

Until answered, the `METING_BUS` cable values stay marked PROVISIONAL. The
classification fix (10 rows that previously emitted nothing) stands regardless
— only the string is in doubt.

### R3 — Waterpomp "4 x 2" — AMBIGUOUS, do not act

Rick indicated roughly `4 x 2` for waterpomp, with uncertainty on our side
about what was meant. Two very different candidates:

| Reading | Cable | Purpose |
|---|---|---|
| `4G2,5` | `DRAK HULT ... 4G2,5` | 400V power feed — already in config |
| `4x2x0,8` | `DRAK SIG B2CA GY 4X2X0.8 HA500` | shielded signal bundle |

2195-06's manual gives `DRAK SIG B2CA GY 4X2X0.8 HA500` for
"Vuilwaterpomp diverse functies", which favours the second reading — but that
is inference, not confirmation.

**Do not encode.** Ask Rick for the full cable string verbatim.

---

## Section 10 — NEW from project 1363 (Kuijpers, B2CA/JOBA, four panels)

### Q14 — `JOBA STUURSTR HHJZ 5X1 MT` never emitted (20 wires) — **CABLE QUESTION CLOSED 2026-08-18**

**Rick confirms `JOBA ST.STR B2CA HCHJZ 5X1 MT` ≡ `JOBA STUURSTR HHJZ 5X1 MT`.**
The config value was never wrong; the gap was partly a wording artefact.

**But the 20 wires are not simply recovered.** 1363's 45% was computed by hand
transcription before the equivalence was known, so those rows may have been
counted as misses on wording alone. **Re-score 1363 with an equivalence-aware
comparison before assuming the gap is closed.**

The classification half of Q14 is superseded by the pump signal rule
(Section 0d). Original entry follows.

The largest single gap. This is the bedrijf/storing cable, used throughout the
manual: circulatiepomp bedrijf/storing, droge koeler vrijgave/storing, ketel
vrijgave/storing, afzuigventilator vrijgave/bedrijf, brandklep melding,
lichtcontact, noodschakelaar.

The config's `BEDRIJF_STORING` and `VRIJGAVE_STORING` both map to
`JOBA ST.STR B2CA HCHJZ 5X1 MT` — the **ST.STR** variant, not **STUURSTR**.

**Unresolved:** is this a config value error (wrong variant for these types), or
are the rows classifying to a different type entirely? Needs a classification
probe on the 1363 input before deciding. Possibly the single cheapest 20 wires
available.

### Q15 — Panel-topology cables not derivable from I/O (16 wires)

The `NEXT` panel is entirely `Datacommunicatiekabel regelkast RK<nnn>` — 16
rows, one per other regelkast in the building (RK161, RK085, RK072, RK851,
RK062, RK061, RK081, RK861, RK071, RK181–185, RK031, RK021).

**These do not come from I/O rows at all.** They are derived from the panel
topology of the project. Nothing in a functielijst generates them.

Also note the cable is **`COMM U/UTP CAT6 CS34ZB HA305`** — the config's
`COMM_RK_ONDERLING` says **`CS34ZC`**. See Section 5; this is now a **second
observation** for CS34ZB (first was Rule 3, Delta Controls on 7268).

**Ask Rick:** is the RK-onderling cable CS34ZB or CS34ZC? And is the
bus-koppeling panel something Erco always produces, i.e. should the pipeline
generate it from a list of panels?

### Q16 — Smoorklep / omschakelafsluiter → `JOBA STUURSTR HHJZ 10X1 MT` (15 wires)

The manual gives `HHJZ 10X1` to every smoorklep. The input calls the same
devices `Omschakelafsluiter 1 GKW droge koeler (Glycol)` and
`Blokkeerafsluiter 1 transport CO`; the manual calls them `Smoorklep`.

The pipeline emits `JOBA ST.STR B2CA HCHJZ 7X1 MT` ×2 and
`JOBA STSTR B2CA HCHJZ 7X1 MT` ×2 — so a few rows classify as
`KLEP_OD`/`SMOORAFSLUITER` but choose 7X1, and 11 rows miss entirely.

Two separate problems: a **synonym gap** (`omschakelafsluiter`,
`blokkeerafsluiter` → smoorklep) and a **cable-value question** (7X1 vs 10X1).

Note `2_Kabelkeuze` already has `BRANDVENTILATIESCHAKELING` at
`JOBA STUURSTR HHJZ 10X1 MT` with the comment *"Tilburg B2CA: 10X1 — observed
exception"*. So 10X1 exists in the config; it is just not reachable from these
device names.

### Q17 — Feed cables are CCA-labelled inside a B2CA project (10 wires) — **TWO OBSERVATIONS**

1363's manual is B2CA/JOBA throughout for signal cables, but every feed is
written **CCA**:

| Manual feed | Count | Pipeline emitted (B2CA) |
|---|---|---|
| `DRAK HULT CCA 3G2,5 HA500` | 5 | `DRAK HULT B2CA 3G2,5 MT` |
| `DRAK HULT CCA 4G4 MT` | 3 | `DRAK HULT B2CA 4G2,5 MT` |
| `DRAK HULT CCA 4G6 MT` | 2 | `DRAK HULT B2CA 4G2,5 MT` |

**This mirrors 2195-06**, where DRAK-branded signal cables appeared inside a
B2CA project. Two projects now show that **the feed cable's fire class is not
the project's fire class**.

This is a much sharper version of Q5. Combined:
- 2195-06: DRAK signal cables at B2CA
- 1363: CCA feeds inside a B2CA/JOBA project

**Ask Rick:** is the fire class per-cable rather than per-project? If so,
`brandklasse` as a single project-level switch is the wrong model.

### Q18 — Feed cross-section scales with load — **THIRD OBSERVATION 2026-08-18, now self-evidenced**

7222 adds `4G4` (7,5 kW/400V ×4), `5G6` (11 kW/400V ×2) and `5G2,5` (tracing ×6),
none of which exist in `3_Voedingen`.

**More decisive: the reissued dictionary contradicts itself by design.**
`Circulatiepomp voeding` appears as `4g2,5` in six sections and `3g2,5` in
another — same device, same document. Cross-section is load-driven; core count is
phase-driven. This is no longer a hypothesis, and it means Conflicts A, E and H
were never conflicts.

**Unit trap:** 7222's input has `Vermogen = 220` on 400 V transportpompen the
manual annotates as 2,2 kW — the input is in **watts**. Any sizing table must
normalise units first. Same family as Q24.

Original entry follows.

1363's feeds:

| Load | Cable |
|---|---|
| 22 kW / 39,2 A / 400V | `4G6` |
| 11 kW / 20,3 A / 400V | `4G4` |
| 0,4–0,76 kW / 230V | `3G2,5` |
| 0,53 kW / 2,33 A / 230V | `3G2,5` |

`3_Voedingen` has one fixed cable per klasse — `400V_3F_zonder_N` is `4G2,5`
regardless of load. `4G4` and `4G6` do not exist in the config at all.

The pipeline already parses kW/A/V (`_parse_electrical_spec`) and writes them
into `bekabeling naar`, so the data is available; there is simply no sizing
table.

**Ask Rick:** is there a current-to-cross-section table we should encode? This
also bears on Conflict A (transportpomp `4g1,5` vs `4g2,5` — possibly both
correct at different loads).

### Q19 — Multi-panel output (relates to Q2)

1363's manual splits into four panels: RK-ALGMN, RK161, RK861, and `NEXT`
(the bus-koppeling panel). The pipeline was run once with `--rk RK1` and
produced a single list of 86 rows against 160 manual wires.

Per the evaluation convention (Section 8) the **page split does not matter** —
what matters is the set of wires. But note:
- the `NEXT` panel's 16 wires are not derivable from I/O at all (Q15)
- `RK861`'s manual includes a `Signaal gevers subkast externe koppelen op
  RK1.3` section, i.e. a *fifth* panel referenced from within one panel's list

Second observation for **Q2** (sheet-to-panel merge, first seen at Tilburg):
one input can legitimately produce several panels' lists.

---

## Section 11 — Consolidated list of open questions for Rick

Ordered by wires unblocked. Items marked ✱ are new or sharpened as of
2026-07-31; **✦ as of 2026-08-18 (project 7222)**; **◆ as of 2026-08-21
(7-nieuw / 7277)**.

**Send items 17 and 18 first.** They are worth ~270 wires between them and both
answer in a sentence. Then 27 and 28, which are worth ~60 across two projects and
are likewise one-line answers. The rest are structural and better raised once he
replies.

| # | Question | Wires | Project |
|---|---|---|---|
| 1 ✱ | Is fire class **per-cable** rather than per-project? (Q17) | 10+ | 1363, 2195-06 |
| 2 | DRAK × B2CA column: are the DRAK GY cables our CCA entry with the fire class swapped? (Q5.1) | 43 | 2195-06 |
| 3 | Do device meldingen bundle into one multi-core cable, and what sets the core count? (Q7) | ~15 | 2195-06 |
| 4 | B2CA passive temp sensor: `1x2x0,8` or `1x4x0,8` for bus sensors? (Q5.2, R2) | 22 | 2195-06 |
| 5 ✱ | `BEDRIJF_STORING` / `VRIJGAVE_STORING`: STUURSTR HHJZ 5X1 or ST.STR HCHJZ 5X1? (Q14) | 20 | 1363 |
| 6 ✱ | Smoorklep/omschakelafsluiter: 7X1 or 10X1? (Q16) | 15 | 1363 |
| 7 ✱ | RK-onderling cable: CS34ZB or CS34ZC? Should the bus-koppeling panel be generated? (Q15) | 16 | 1363, 7268 |
| 8 ✱ | Feed cross-section vs load — is there a sizing table? (Q18) | 10 | 1363 |
| 9 ✱ | Energy Valve: B2CA equivalent, and which Modbus cable? (R1) | ~8 | 7268 |
| 10 ✱ | Waterpomp "4x2" — full cable string please (R3) | ? | — |
| 11 | `DRAKSIG KAB` vs `RAK SIGN KAB` — correct product name? (Q5.3) | 10 | 2195-06 |
| 12 | `DRAK SIG B2CA GY 4X2X0,8 HA500` — no entry in either column (Q5.4) | 8 | 2195-06 |
| 13 | Brandklep + derden → full signal cable: can this ship? (Rule 1) | — | 7268, 2195-06 |
| 14 | Tracing panel assignment (Q12) | — | Fonkel, 2195-06 |
| 15 | Pump feed core count `3G2,5` vs `4G2,5` (Q13) | 2 | 2195-06 |
| 16 | `Totaal ws = 0` — confirm as convention (Q1) | 0 | four projects |
| 17 ✦ | **Field temperature sensors.** The dictionary gives aanvoer/retour/intrede/uittrede opnemers `1x2x0,8`, and the 2026-08-18 reissue moved drukopnemers to `1x4x0,8` but left the temperature rows. 7222's manual uses `1x4x0,8` for both (131 rows). Missed in the update, or a real difference? | **~190** | 7222 |
| 18 ✦ | **`Levering CWD/W` / `CWD/E` scope.** 85 manual rows are `Kabel levering derde totaan RK` against 2 emitted. But `Dakafvoerkap` carries CWD/W and **does** get two Erco cables, so the marker alone cannot mean derden. What distinguishes them? (Rule 1 territory) | **~83** | 7222 |
| 19 ✦ | **Mixed family inside one panel.** RK1 uses DRAK for the plant but JOBA in the UPS rooms, the meldkamer klimaatplafond zones, and 26 of 61 brandkleppen — same function, split by location. No project-level switch can produce this. (sharpens Q17/Q5) | 57 | 7222 |
| 20 ✦ | **Open/dicht core count.** `+ 2 eindcontacten` → `8X0,8` (×48), `Luchtklepservo` → `6X0,8` (×12), `Dakafvoerkap` → `4X0,8` (×2). Does it track feedback contacts? Note the 67 *modulating* regelafsluiters also take `4X0,8`. | 58 rows | 7222 |
| 21 ✦ | **`SMOORAFSLUITER`.** The reissued dictionary says `7g2,5`; Tilburg's validated manual says `7G1,5`, which is what `2_Kabelkeuze` holds. Which stands? *(deliberately left unchanged)* | — | Tilburg |
| 22 ✦ | **`3_Voedingen` `TRACING`.** CCA cell `5G2,5`, B2CA cell `3G2,5`. Dictionary and 7222 both say `5G2,5` — is the B2CA cell wrong? | ~6 | 7222 |
| 23 ✦ | **Multi-panel doorlussen.** When a cable loops from RK03 to RK02, does it appear on both panel lists or one? (Q19) | — | 7222, 1363 |
| 24 ✦ | **Naregelingen scope.** Is the naregelingen sheet in scope for the pipeline at all? ~700 of 7222's 1443 input rows. (Q3) | ~700 rows | 7222, 7268 |
| 25 ✦ | `Leeswaarde` vs `Verzendwaarde` — read/send point counts (Ketels 24/24). Should `SOFT` be the sum? | — | 7222 |
| 26 ✦ | Six `Detector (5m kabel, 230VAC, d150mm, h65mm)` rows — what do they detect? | 6 rows | 7222 |
| 27 ◆ | **Open/dicht core count — SECOND MANUAL.** 7-nieuw gives every VAV klep and zoneafsluiter (`opensturing/standmelding` = open + close + one feedback) `DRAK CCA GY 6X0,8` ×9; we emit `8X0,8` ×19 against **0** in the manual. 7222 split it three ways: no feedback `4X0,8`, one `6X0,8`, two eindcontacten `8X0,8`. Two cores per signal fits both — but 7222's 67 *modulating* regelafsluiters also take `4X0,8`, so it is not simply signal count. **Is the core count set by the number of feedback contacts?** | **~50** | 7-nieuw, 7222 |
| 28 ◆ | **Default digital signal cable on CCA/DRAK.** 7-nieuw's manual uses `RAK SIGN KAB CCA 4X0,8 HA500` for overwerktimers, vorstthermostaat, brandschakelaars, 3-wegafsluiters, circulatiepomp bedrijf/storing — 14 rows. We emit `DRAK CCA GY 2X0,8` (`MELDING`). Score: `4X0,8` 2 vs 14, `2X0,8` 13 vs 0. **Is `4X0,8` the standard for a simple melding, with `2X0,8` reserved for something narrower?** One cell. | ~12 | 7-nieuw |
| 29 ◆ | **What do bare `klep` and `afsluiter` get?** Both are generic catch-all synonyms pointing at `KLEP_OD` (`8X0,8` / `7X1`), added during the 7222 session on a *priority-safety* argument — they sit below the specific valve patterns so they only catch what falls through — **not** on evidence that those devices are open/dicht with feedback. Is `kogelafsluiter` open/dicht with or without feedback? See QN1 in Section 0e. | — | 7222, 7277 |
| 30 ◆ | **Novectra-supplied meters.** 7-nieuw has four `Kwh meter levering Novectra` rows. The manual gives one the derden text (#2) and **omits the other three entirely**; we emit a cable for all four. Is such a meter ever our cable, and what decides it? Why does WP1's appear and WP2's not — do they daisy-chain? | ~4 | 7-nieuw |
| 31 ◆ | **`400V_3F_zonder_N` on CCA.** `3_Voedingen` holds `DRAK HULT CCA 4X2,5 MT` — the only `X` in an otherwise all-`G` column, so possibly a long-standing typo. 7-nieuw's manual uses `DRAK HULT CCA 5G2,5 MT` on the transportpomp and both EC ventilators, all 400 V. 7277 emits it 4 times. | ~7 | 7-nieuw, 7277 |
| 32 ◆ | **Cross-panel signals.** A row reading `VANUIT <other panel>` marks a signal whose cable belongs to the other panel: 7-nieuw RK1's brandschakelaars (no I/O, `VANUIT RK 2 Sport`) get nothing in the manual, RK2's (DI 2 each) do. Currently handled only incidentally, via the absent I/O. **Should a `VANUIT <panel>` row always produce nothing?** Third project with cross-panel references; relates to Q19/Q2. | — | 7-nieuw, 7222, 1363 |

---

## Section 12 — Score history (honest record)

| Project | Layout | Family | Score | Notes |
|---|---|---|---|---|
| Duitslandlaan | Kuijpers | B2CA/JOBA | 18/18 | locked regression |
| Boerhaave | Coneco | CCA | 15/15 | locked regression |
| Fonkel | Kuijpers | B2CA/JOBA | 18/18 | locked; fixture updated 2026-07-30 (tracing feed) |
| Tilburg (7273) | Coneco | CCA | ~55–65% | blind, not locked |
| 7268 | Append1 | CCA | 48% | blind; was 37% before the feed fix |
| ZRD Vlissingen | client7 | — | 17% | blind; blocked by Rule 1 |
| 2195-06 | Priva | B2CA | 20% | blind; 2% on CCA, 11% on B2CA, 20% after METING_BUS |
| **1363** | **Kuijpers** | **B2CA/JOBA** | **45%** | **blind; 13% on CCA. Score predates the STUURSTR/ST.STR equivalence — re-score** |
| 7267 | Apparatuurlijst | B2CA/JOBA | 71% | blind; hard ceiling 23/24 (Q21) |
| **7222** | **client8** | **B2CA/DRAK** | **33.4% exact / 45.4% spec** | **blind 22.6% (wrong family). First B2CA/DRAK project. 793 wires, 5 panels** |
| **7-nieuw** | **scanned PDF** | **CCA/DRAK** | **42.7% exact / 62.5% spec** | **blind 34.4% / 51.0%. 96 wires, 2 panels. Manual hand-transcribed; all 14 totals reconcile** |
| 7277 | two-row header | CCA/DRAK (aangenomen) | not scored | no manual yet. 141 devices, ingested via a direct CSV builder |

2195-06 forecasts if the DRAK×B2CA column is confirmed: 38% (token swap on GY
cables) or 47% (also tolerating the sensor suffix). Both are forecasts, not
measurements.

---

---

---

## Section 0e — What changed on 2026-08-21 (7-nieuw + 7277)

Two projects. **7-nieuw** (muziekschool + sportcomplex) was validated against its
kabellijst of 23-1-2026: 96 wires over two panels, blind **34.4% exact / 51.0%
spec** → **42.7% / 62.5%** after five fixes. **7277** is a new layout with two
header rows; ingested and run, no manual yet, so not scored.

Four answers from Rick encoded. One helper written earlier this week was found to
have destroyed per-project config values; the merge gate has been 1/3 since.

### Answered by Rick

| # | Answer | Encoded as |
|---|---|---|
| M-bus cable | `DRAK SIGK CCA 1X2X0,8 2501 MT`. M-bus ≠ Modbus, and says nothing about scope | `4_Bus` key renamed `MBUS_DERDEN` → `MBUS` |
| overwerktimer | `1x4x0,8` | `2_Kabelkeuze` `OVERWERKTIMER`, DRAK columns |
| brandschakelaar toevoer + afvoer | ONE cable, `Brandventilatieschakeling`, `8x0,8` | pairing pass + existing type's DRAK cells |
| regelafsluiter | **with** open/dicht `8x0,8` DRAK / `12X1` B2CA JOBA / `10X1` CCA JOBA; **without**, unchanged at `4x0,8` / `5X1` | new type `REGELAFSLUITER_OD` |

### CONFIG — M-bus was a protocol masquerading as a scope

`4_Bus` had a key `MBUS_DERDEN` whose cable was *"Kabel levering derde,
enkelzijdig aansluiten op regelkast Erco"*. `_bus_row` selects it purely on the
protocol string, so **every** M-bus device was assumed third-party regardless of
who supplied it. Renamed to `MBUS` with the real cable; derden scope left to
`derden_flag` / `DERDEN_PAT`, where it belongs.

Config and code must land together — `cfg.bus["MBUS"]` against a config still
saying `MBUS_DERDEN` is a `KeyError`.

**`4_Bus` has only ONE cable column**, so this CCA string is also used on B2CA
projects. Same gap as Q25. No current project affected; logged, not fixed.

*Unresolved:* 7-nieuw's manual treats its five M-bus rows three ways — one derden
text, one BMS cable (relabelled by Rick as MOD-bus), three absent. All the
absent/derden ones say `Kwh meter levering Novectra`. See Section 11 item 30.

### BUG — `OVERWERKTIMER` was inert

The type existed with the right cable but is **not in `sig_priority`**, so it
could never be selected: all four rows fell through to `MELDING` and emitted
`2X0,8`. Added. Rick then changed the value to `1x4x0,8`, which **diverges from
7-nieuw's own manual** (#29, #60-62 = `4X0,8`); encoded on his authority and
recorded as deliberate.

A first edit wrote `DRAK … GY 1X4X0,8`, mixing an unscreened product name (`GY`)
with a screened spec (`1x`). Corrected to the `SIGK … 2502Q` line — the pattern
holds throughout: `GY` never carries a `1x` prefix, `SIGK` never appears without
one.

### BUG — brandschakelaar pairing, and why it is NOT a dedupe

Rick: the two functielijst rows become ONE kabellijst row. Evidence: 7-nieuw RK2
r93+r94 → manual #58.

**Implemented as a standalone pairing pass, deliberately outside
`dedupe_devices`.** The two mechanisms answer different questions:

- `dedupe_devices` — *"is this one device described twice, or two devices with
  similar names?"* Global; its key carries group and name stem so that
  Boerhaave's three heat pumps stay three.
- pairing — *"these two named rows are the two halves of one cable."* Always
  exactly two, always adjacent, no ambiguity to resolve.

A first attempt routed it through `_device_key` plus a rename in `_merge_group`.
That made the merge depend on `rk` and `group`, which are **identical across both
panels** on this input, so all four rows collapsed into one; and the
`_merge_group` rename was the only place in the codebase where a merge changes a
device's name. Reverted. Recorded because it cost two runs.

`_pair_brandventilatie()` now runs in `run()` before `dedupe_devices`, merges an
adjacent `toevoer` → `afvoer` pair in that order, unions the I/O, and **flags an
unmatched half rather than emitting it**.

An earlier config attempt **appended a duplicate `BRANDVENTILATIESCHAKELING`
row** instead of editing the existing one; the loader keeps the first, so the
change silently had no effect. The existing row already had all four family
columns populated — including `JOBA 12X1`, which matches 7222 RK04/05 exactly, so
the "three projects, three values" contradiction recorded in v5 was partly an
artefact of not looking at the config first.

### CONFIG — `REGELAFSLUITER_OD`, and why not `KLEP_OD`

`regelafsluiter open/dicht` (prio 80) repointed from `KLEP_STURING_MELDING` to a
new type carrying Rick's four values.

`KLEP_OD` was **not** reused, because it is also reached by three generic
catch-alls — `klep` (30), `afsluiter` (20), `kogelafsluiter` (40) — added during
the 7222 session on a *priority-safety* argument (they sit below the specific
valve patterns, so they only catch what falls through) rather than on evidence
about the devices. Changing `KLEP_OD`'s JOBA columns would have moved all three.
See QN1.

### BUG — every bus row said "MODbus"

`_bus_row` selects a key and then hardcoded the word `MODbus` in the label, so an
M-bus watermeter read `Hoofdwatermeter MODbus koppeling` while carrying the M-bus
cable, and BACnet devices read MODbus too. Added a `_BUS_LABEL` table so the
suffix follows the key. Cosmetic — cannot change a cable — but it contradicted
the cable string in the same row. *(7277 r151-153)*

### DATA — 7-nieuw: a scanned, hand-annotated PDF

5 pages, transcribed by hand to xlsx. **All fourteen totals** (DI/DO/UI/AI/AO/
FDP/software per panel) reconcile with the PDF's own totals rows — a strong but
not conclusive check, since an error shifting a point between two rows in the
same column would still balance.

Recorded in the workbook's notes sheet: the single `Groep` column split into
Groep/Subgroep/Onderdeel; device names repeated on every function row; three
**struck-through** circulatiepomp rows kept with strikethrough (their datapoints
still count toward the PDF's totals); handwritten `BR Controls` replacing
struck-out `LEVERING DERDEN` on five valves recorded verbatim; a handwritten
marginal `2` on two rows **not** interpreted.

**The RK1/RK2 assignment is inferred, not stated.** Page 1 says `VANUIT RK 2
Sport`, page 5 says `VANUIT RK 1 MUZIEKSCHOOL` — each panel names the other.

**`UI` (Universal Input) has no home in `NORM_COLUMNS`** and was folded into
`AI`. 19 points on RK2.

### DATA — 7277: two header rows, neither sufficient alone

| row 14 *(merged down to r20)* | row 21 |
|---|---|
| Bedrijfmelding, Storingsmelding, Analoge ingang, Digitale uitgang, Analoge uitgang, Verzend waarde, Ontvang waarde, P[kW], I[A], U[V], Sturen, Meten, Fabricaat, Type | I/O check, Omschrijving, Proces code, B, ST, AI, I/O, AU, VW, OW |

Both rows scored **7** in `parse_excel`'s header detection and `max()` returns
the first — so ingest chose row 14, which has no `Omschrijving`, and dropped
every row: **`OK: 0 input rows`**, no flag, exit status 0.

A tiebreak entry in the header map (`I/O check` → `regelkast_spec`, an inert
field) pushed row 21 to 8 and produced 130 rows — but with `fabricaat`, `type`,
`voltage`, `power_kw`, `current_a` and `bus_protocol` **all empty**, because
those columns are named only on row 14. Choosing either header row necessarily
abandons the other half of the sheet.

Worked around by building `normalized.csv` directly from the workbook, reading
both header rows by fixed column index: **141 devices**, fabricaat 89, type 99,
bus_protocol 19, voltage 22, power_kw 17. DI went 6 → 31 (the `B`+`ST` sum), DO
45 → 67.

**The real fix is for `parse_excel` to combine two header rows** — candidate row
where non-empty, row above as fallback. Generic: 7222 had the same shape, and it
would make 7277's clean `P`/`I`/`U` columns reachable (see Q18). Not done: the
merge gate has been red since the config accident below, so an ingest change on a
shared path is unverifiable.

Other notes on this layout. The abbreviation **`I/O` means digitale UITGANG** —
row 14 says so, and a storingsmelding lamp carries its 1 there; the most
misleading label seen so far. There is **no plain digital-input column**: all DI
arrives via `B` and `ST`. Empty cells hold the string `'-'`. `Bedrijfmelding` on
row 14 is missing its `s`. `procescode` is filled on 1 of 141 rows, so ordering
falls back to input order — third project running.

### DATA — two client typos, found by their effect on the collapse

- **`Circultiepomp` ×10** (missing the `a`), sitting directly above and below
  correctly-spelled `Circulatiepomp` rows. Broke the transcription's device
  collapse *and* stopped the rows matching the `circulatiepomp` synonym, so ten
  pumps were classified on their I/O signature alone — and the pump rule looked
  broken when the input was at fault. Normalised via an `ALIASES` map **in our
  derived file only**; the source workbook is untouched.
- **`'Warmtepomp. '`** — trailing dot, nothing after it. The collapse splits on
  `". "` and needs a function after the separator, so the bus row (carrying the
  protocol and VW/OW) never joined its own `Vrijgave`/`Storing`/`Vermogen
  sturing` rows: protocol on one device, I/O on another.

Both fixed in the builder: trailing dots stripped before splitting, and a bare
device row can now **start** a collapse run.

### DATA — collapse rule, second iteration

Merging on `(group, stem)` alone collapsed three separate RADA systems on
7-nieuw into one, because each had a row called `datacomm.`. The rule is now:
merge consecutive rows sharing a stem **until a function name repeats**, at which
point a new device starts.

### BROKEN — `propagate_config.py` destroyed per-project config values

A helper written this week copies the master `kabelconfig.xlsx` over each project
copy and restores only `0_Parameters`, on **the handover's claim that the copies
differ only in that tab**. They do not. v3 recorded project-specific
`2_Kabelkeuze` values for Boerhaave (`SMOORAFSLUITER` → `JOBA STUURSTR HHJZ 7X1`,
`METER_VOEDING_24V` CCA → `JOBA STUURSTR HHJZ 3X1`) which were overwritten.

Gate **1/3 since**: boerhaave 12/14 (7X1 ×0 expected 12; 3X1 ×0 expected 3),
duitslandlaan 16/17 (5X1 ×13 expected 14), fonkel 14/14. The failure was
committed, so every run since has been measured against a broken baseline.

**Not yet restored.** Restore the three copies from the pre-propagation commit,
delete or rewrite the script, and **write down the real per-project differences**
before anything else touches those files.

### New questions

**QN1 — `KLEP_OD` is doing two unrelated jobs.** The confirmed *open/dicht with
feedback* type (`8X0,8`, comment "open/close + feedback(s)", from a device with
two eindcontacten) **and** a catch-all for `klep` / `afsluiter` /
`kogelafsluiter`. `kogelafsluiter` is defensible — a ball valve is physically
two-position. `klep` and `afsluiter` say nothing about open/dicht at all. Its
vagueness currently masks two separate unknowns, since `KLEP_OD` is also where
the core-count question (item 27) will eventually be resolved.

**QN7 — `sig_priority` should come from the config, not the code.** Five
functietypes have now needed the identical one-line code edit before their config
value could ever be used: `POMP_2/3_SIGNALEN`, `KLEP_OD_ZONDER_TERUGMELDING`,
`OVERWERKTIMER`, `BRANDVENTILATIESCHAKELING`, `REGELAFSLUITER_OD`. A type absent
from `sig_priority` is invisible to `emit()` however correct its config row is.

**This breaks the README's promise** that estimators extend device coverage by
editing the config with no Python. Changing a *value* is config-only; adding a
*type* is not. Proposal: a priority column on `2_Kabelkeuze`, read at load time.
Real change to a shared path; wants its own session.

### Strengthened

**`LEVERING DERDEN` does not mean "no cable" — SECOND OBSERVATION.** 7-nieuw
RK2's brandschakelaar pair carries `LEVERING DERDEN` and **does** get a cable;
the RK1 pair carries no such marker and gets none. 7222's `Dakafvoerkap` carries
`Levering CWD/W` and gets two Erco cables. Both point the same way: the marker
describes **who supplies the device, not who runs the cable**. Widening
`DERDEN_PAT` to suppress rows would be wrong. Sharpens Section 11 item 18.

**Q23 — silent-drop mechanisms → FIFTH: header-row ties.** 7277's rows 14 and 21
both scored 7; `max()` returns the first, so ingest chose the row without an
`Omschrijving` and discarded **every** row, reporting `OK: 0 input rows` with no
flag and exit status 0. A run that silently produces nothing looks identical to a
run whose input was empty.

**Q18 — the best data source yet.** 7277 has `P [kW]`, `I [A]` and `U [V]` as
**separate numeric columns**, not free text — cleaner than 7222's ambiguous
`Vermogen` or 1363's mangled decimals. If the sizing table is built, build it
from this project. Reachable only once `parse_excel` combines two header rows.

**Q17 / Q5 — family per cable, THIRD observation.** 7-nieuw is CCA/DRAK
throughout except two `Ruimte RV/temperatuur opnemer` rows which get
`JOBA ST.STR B2CA HCHJZ 5X1 MT` — different family **and** different fire class —
while their sibling rows in the same group get DRAK CCA.

### Process

**A helper that assumed structure it never verified.** `propagate_config.py` was
written against a documented claim without checking the claim. Two rules follow:
do not build a tool on an assumption you have not tested, and use
`git stash push config/` + re-run to separate config-caused gate failures from
code-caused ones — it was what proved the pairing change innocent.

**Check whether a functietype already exists before adding it.** Searching
`1_Synoniemen` for the *device name* does not tell you whether the *type* is
there. `BRANDVENTILATIESCHAKELING` already existed with all four family values;
appending a duplicate row silently did nothing.

## Section 0d — What changed on 2026-08-18 (project 7222 + reissued dictionary)

Project 7222: client8 layout, **B2CA/DRAK** — the first project ever run on that
family combination. 793 manual wires across five panels (RK1 349, RK02 166,
RK03 155, RK04 55, RK05 55) plus a Naregelingen sheet. Manual dated 6-2-2026.

Blind 22.6% → **33.4% exact / 45.4% on conductor specs** after four merged fixes.
Merge gate 3/3 green.

### Shipped

| Change | Bucket | Effect |
|---|---|---|
| `procescode` added to `classify_row`'s match text | BUG | 28 rows classified that previously were not; 11 spec matches |
| `DO` branch in the I/O fallback → `KLEP_OD_ZONDER_TERUGMELDING` | BUG | 2 wires; closes a whole-path blind spot |
| `servomotor` synonym removed | CONFIG | prevented a 13-row regression on 2195-06 |
| Pump signal rule (`POMP_2_SIGNALEN` / `POMP_3_SIGNALEN`) | CONFIG+BUG | 19 wires; `POMP` had no signal rule at all |
| Reissued CCA dictionary: `1,5` → `2,5` | CONFIG | 12 cells; closes Conflicts A, E, H |
| `header_map_client8.xlsx` | CONFIG | new layout supported |

### BUG — `classify_row` was blind to `procescode`

The client8 layout puts the **device name in the tag column** and a part number
in `Omschrijving`:

| `Ref. / Procescode` | `Omschrijving` |
|---|---|
| `Dakafvoerkap (droog)` | `Servomotor Open/Dicht` |
| `Buitenluchtklep` | `GCA126.1E Damper actuator` |
| `Vloertemperatuur` | `Sensor Link cable 10 m with flying leads` |
| `Max. thermostaat` | `RAK-TW.1000HB` |

The match text was `omschrijving + type + opmerking`, so the one word
identifying the device was invisible. Fixed by adding `norm.procescode`.

Verified with a new `classify_diff.py` before merging:

```
duitslandlaan  47 rows -> NO CHANGE
boerhaave      31 rows -> NO CHANGE
fonkel         45 rows -> NO CHANGE
7222          938 rows -> 28 CHANGED  (13 None->KLEP_OD, 12 None->METING_ACTIEF,
                                       3 None->METING_PASSIEF)
```

Strictly additive — **no row that already classified was reclassified on any
project**. The 13 `KLEP_OD` rows are the real gain: DO-only rows, and `DO` was
not in the fallback chain, so they previously emitted nothing.

### BUG — `DO` was invisible to the entire signal path

A device whose only signal is a digital **output** selected no function type and
no cable. `classify.py`'s fallback went `AI → DI → AO`, skipping `DO`; `_ok()`
in `rules.py` gated only on `AI`/`DI`/`AO`.

Evidence: 7222 r144/r145 `Dakafvoerkap (droog)/(nat)`, `Voeding=230`,
`Digital uit=1`. Manual rows 139–142 give each a feed **plus** a `GY 4X0,8`
open/dicht cable; the pipeline emitted only the feed.

Fixed with a `DO` branch mapping to a new `KLEP_OD_ZONDER_TERUGMELDING` type
(`4x0,8`). `KLEP_OD` could not be reused — its comment reads *"open/close +
feedback(s)"* and its value is `8X0,8`, the two-eindcontacten variant.

**Failed intermediate attempt, recorded because it cost three runs:** widening
`_ok()` to accept `DO` for `MELDING`/`VRIJGAVE`/`BEDRIJF_STORING` made every
DO-only row select `BEDRIJF_STORING` (`6X0,8`) and masked the new type.
Reverted. `_ok()` deliberately does **not** accept DO.

**Watch item.** Section 0c records that 7267's `Storing urgent`/`Storing niet
urgent` (DO=1, no DI) correctly get no cable, while 2195-06's `Besturing GBS`
rows (also DO=1) *are* wired. The new branch only fires when the dictionary is
silent, so neither should be affected — but **7267 and 2195-06 are not
fixtures**, so the gate cannot confirm it. Worth a manual check.

### CONFIG — `servomotor` synonym removed

`servomotor → KLEP_STURING_MELDING (70)` was intercepting rows it does not
describe. It names the **actuator**, never the device:

| Project | String | What actually decides the cable |
|---|---|---|
| 7222 | `Dakafvoerkap (droog)` / `Servomotor Open/Dicht` | it is a dakafvoerkap |
| 7222 | `ChangeOver6 Servomotor voor NovoCon S` ×14 | prio 70 beat `temperatuur` (65) |
| 7222 | `NovoCon S, Digitale Servomotor` ×14 | bus device, correct BMS cable |
| 2195-06 | `Brandklepservomotor levring derden` (in `opmerking`) | it is a brandklep |
| 7268 | `E-mechanische servomotor` ×6 | Energy Valve accessory |

On 2195-06 the pattern **ties** with `brandklep` at priority 70 and wins on
length (10 > 9), flipping 13 rows on a project with no fixture.

**New general rule.** Component and attribute nouns — `servomotor`,
`hulpschakelaar`, `aansluitset`, `base`, `module` — must not become device
classes. Same failure as the `DERDEN` primary-hijack fixed in v3, reached from a
different direction. Add future candidates of this shape to the batch, not the
dictionary.

Removing it cost ~30 rows their (wrong) cable; those now flag
`NO CABLE DERIVED` and need review.

### CONFIG + BUG — pump signal rule

`POMP` classified correctly but was **inert**: absent from `sig_priority`, so it
could never select a signal cable. Everything a pump emitted came from its
secondaries, and the symptom differed by project:

- **7222** — `Storing` gives `DI=1`, so `VRIJGAVE` passed `_ok()`, was remapped
  to `MELDING`, and emitted `GY 2X0,8`. Wrong cable, 40 rows.
- **2195-06** — no DI/AO, so nothing passed: `NO CABLE DERIVED` on all five
  pumps.

**Rick, 2026-08-18:** a pump's signal cable follows the **number of signals**,
not the pump type.

| Signals on the row | Cable |
|---|---|
| 2 (vrijgave/storing) | `1x4x0,8` |
| 3 (vrijgave/storing/sturing) | `3x2x0,8` |

Confirmed by the reissued dictionary (nine two-signal pump rows, all
`1x4x0,8`) and by 7222's manual (`Circulatiepomp vrijgave/storing` → `1X4X0,8`
×8; `Transportpomp vrijgave/storing/sturing` → `3X2X0,8` ×32).

Implemented as two functietypes, counted from the I/O columns (`DI`/`DO`/`AO`
non-zero) so it does not depend on how the description is worded, plus both
added to `sig_priority` above `VRIJGAVE`.

**Deliberately pump-specific.** The same dictionary gives a three-signal
`Ketel vrijgave/storing, sturing 0-10V` `1x4x0,8` and a two-signal
`Ventilator Sturing/Storing` `2x2x0,8`. **Do not generalise the count rule.**

Config values are the dictionary's bare specs, identical in all four family
columns — the dictionary is family-agnostic and no verified product string
exists. Consequence: these rows emit `1x4x0,8` where neighbours emit full
product strings, so they match on spec but not on exact string.

**Open sub-question:** 2195-06's five pumps carry no I/O at all, so the count is
0 and they will still emit nothing. If its manual gives them a cable, the count
may need to come from the description instead.

### CONFIG — reissued CCA dictionary (Rick, 2026-08-18)

Every `1,5` cross-section moved to `2,5`: `3g1,5→3g2,5` (7 device types),
`4g1,5→4g2,5` (5), `5g1,5→5g2,5` (3), `7g1,5→7g2,5` (4). Separately, 27 signal
rows moved `2x2x0,8 → 1x4x0,8`, including all nine two-signal pump rows and all
five drukopnemer variants.

Applied to `2_Kabelkeuze`: `BRANDSCHAKELAAR_KETELHUIS` and
`WERKSCHAKELAAR_VOEDING` → `5G2,5`, `WARMTEWIEL_VOEDING` → `3G2,5` (12 cells),
plus a stale `3g1,5` in the `KETEL_VOEDING` comment. `3_Voedingen` needed **no
change**.

`SMOORAFSLUITER` deliberately left at `7G1,5` — that value comes from Tilburg's
**validated manual**, not from the standard. See Section 11 item 21.

Closes Conflicts **A**, **E** and **H**.

### CONFIG — `header_map_client8.xlsx`

17 columns; five rows beyond `DEFAULT_HEADER_MAP`:

| client_header | canonical_field | note |
|---|---|---|
| `Ref. / Procescode` | `procescode` | device tags, not numeric codes — `_prefix` returns 0, so prefix ordering is inert and row order falls back to input order |
| `Fabrikaat` | `fabricaat` | spelling variant; kept in the map, not `_HEADER_ALIASES`, for zero blast radius |
| `Voeding` | `voltage` | bare, not `Voeding (V)` |
| `Digital uit` | `DO` | **typo in the client sheet** — without this row DO reads 0 sheet-wide with no flag |
| `Leeswaarde` | `SOFT` | provisional — see Section 11 item 25 |

`AC / DC` and `Verzendwaarde` deliberately unmapped.

### NOT FIXED — `kabel_B2CA_DRAK` `METING_PASSIEF` (largest open item)

7222 is the first project to exercise the B2CA/DRAK column. After the family fix
the pipeline picks the **right rows** and writes the **wrong string**:

| | emitted | manual |
|---|---|---|
| `METING_PASSIEF` | `DRAK SIGK B2CA 1X2X0,8 2501 MT` ×199 | `DRAK SIGK 1X4X0,8 B2CA HA500` ×220 |

`1X2X0,8` (one pair) vs `1X4X0,8` (one quad) is a real conductor difference.
**~190 wires from one cell** — more than everything merged in this session
combined. Blocked on Section 11 item 17.

### DATA — fourth silent-drop mechanism: duplicate columns

7222's raw input has **26 columns in three repeating blocks** (`Analoog in`,
`Digitaal uit`, `Busprotocol`, `Leeswaarde`, `Verzendwaarde` each 2–3 times).
`parse_excel` uses `cols.setdefault`, so **only the first occurrence of each
field is read** and the rest are discarded with no flag. Extends Q23 from three
mechanisms to four.

The blocks were merged down to 17 columns **in Excel** to get the run through.
That breaks the blind-run contract — the score is not reproducible from the file
the client sent, and the next project from this client arrives 26 columns wide
again.

**Proper fix:** collect every column index per field in `ingest`, sum the
integer I/O fields, first-non-empty for the strings. That also resolves
`Verzendwaarde`, currently dropped entirely.

### DATA — silent drops accounted

1442 data rows → ~970 expected in the normalized table: 175 blank
`Omschrijving`, 297 bare rows treated as group headers. The group-header set
includes preamble text (`Dit betreft de levering van een nieuwe regelkast`,
`- Technische ruimte 4e verdieping`), which can become section names.
**Reinforces Q23's `SKIPPED` flag as the highest-value low-risk item
outstanding.**

### DATA — mixed numeric typing; `Vermogen` units

`Digitaal in` arrives as `int`, the other I/O columns and `Voeding` as `str`
(PDF-extraction artefact, same family as Q24). Harmless — `_num` parses both —
but `voltage` arrives as text, so any arithmetic needs `_fnum`.

`Vermogen = 220` on 400 V transportpompen is almost certainly **watts**. It
lands verbatim in `bekabeling naar` and would corrupt Q18's sizing table.

### ACCEPT — scope

The input is a **1443-row building-wide bill of materials**, not a single-panel
functielijst (previous maximum 160 wires). ~108 UNKNOWN flags remain, dominated
by **Priva Blue ID panel hardware** and **naregelingen** (Comforte CX, Roombus,
NovoCon, Touchpoint One, `Schetsplaat` ×15). A `PANEL_INTERN` synonym block for
the Priva hardware shipped this session — 160 `PANEL-INTERNAL` flags, ~500 fewer
phantom rows.

### New — batched, need a second observation

**Open/dicht core count tracks feedback contacts?** 7222 splits 58 open/dicht
rows three ways: `+ 2 eindcontacten` → `8X0,8` (×48), `Luchtklepservo` →
`6X0,8` (×12), `Dakafvoerkap` → `4X0,8` (×2). Two cores per signal fits — **but**
the 67 *modulating* `24V/0-10V` regelafsluiters also take `4X0,8`, so core count
is not a simple function of signal count across the whole population. The
dictionary gives every valve `4x0,8` and does not model feedback contacts.
Section 11 item 20.

**`Ruimtetemperatuuropnemer` is a distinct type.** 7222 gives it
`DRAKSIG KAB B2CA GY 1X2X0.8 MT` consistently, while `Ruimtevochtopnemer` and
`RuimteCO2opnemer` **in the same rooms** get `1X4X0,8`. This confirms Rick's
July answer (R2) is specific to room **temperature** — not room sensors
generally, and not passive sensors generally. 11 wires, one observation. Also a
second observation for the `DRAKSIG KAB` vs `RAK SIGN KAB` question (Q5.3).

**Bundled vs split multi-signal rows — now contradicted.** 7267 (drycooler) and
2195-06 (radiator) split a DI+AO row into two cables; **7222's transportpomp
bundles three signals into one** `3X2X0,8`. Three projects say split, one says
bundle, and the standard says one cable per row throughout. The pipeline
currently does **neither** — the generic tail selects exactly one `ftype` and
silently discards the other signals; `E_KETEL` is the only branch that splits,
hard-coded from Duitslandlaan. Related to Conflict C.

**Mixed family inside one panel.** RK1 uses DRAK for the plant but JOBA for the
UPS rooms, the three meldkamer klimaatplafond zones, and 26 of 61 brandklep
standmeldingen — same function, split by location. 57 wires (`2X1`, `5X1`,
`7X1`, `12X1`) that no project-level `signaalfamilie` switch can produce.
**Second observation for Q17/Q5**, and it escalates the question from "fire
class per cable" to "**family** per cable, possibly driven by location".

### Confirmed cable equivalences (Rick) — move to `equivalents.csv`

**Equivalent:**
- `DRAK SIGK AFG B2CA 3X2X0,8 MT` ≡ `DRAK KAB AFG B2CA 3X2X0,8 MT`
- `RAK SIGN KAB B2CA 4X0,8 HA500` ≡ `DRAK B2CA GY 4X0,8 MT`
- `JOBA ST.STR B2CA HCHJZ 5X1 MT` ≡ `JOBA STUURSTR HHJZ 5X1 MT` *(closes Q14's
  cable question)*

**NOT equivalent:**
- `1x4x0,8` vs `2x2x0,8` — one screened quad vs two screened pairs
- `1x4x0,8` vs `4x0,8` — screened vs unscreened

Three equivalences surfaced in one session, each **after** a score had already
been computed without it. They belong in a file the scorer reads, not in
conversation. Folds into the `score.py` item.

### Tooling added

- **`classify_diff.py`** — loads `1_Synoniemen`, classifies every row of every
  project, diffs primary functietype before/after an edit. **Required before any
  `1_Synoniemen` or match-text change**, because the merge gate covers only
  three projects and is blind to 2195-06, 1363, 7267, 7268 and 7222.
- **`probe4.py`** — prints `classify_row` output for a synthetic row plus
  `classify.__file__` and the live source of the fallback chain. **Run after any
  classify edit** — see the process note below.
- Scoring is now a scripted multiset diff with a spec-only mode that collapses
  wording variants. `score.py` + a saved `manual.csv` per project is the
  remaining half of that item.

### Process notes

**Counterfactual scores must state their assumptions.** A mid-session estimate
of 66.7% after the family fix was derived by substituting cable strings read off
the **manual**, not from `2_Kabelkeuze`. The actual re-run scored 33.0%; the
entire gap was the `kabel_B2CA_DRAK` column. The estimate answered "if family
**and** config are correct" while being presented as "if family is correct".

**An edit in the editor is not an edit on disk.** VS Code's dirty-write guard
makes autosave a silent no-op once the on-disk mtime diverges from what the
editor loaded. Two `classify.py` changes sat unsaved for hours while three
pipeline runs were scored against code that did not contain them — including the
`procescode` change, which `classify_diff.py` had verified independently and
which was therefore briefly recorded as merged when it was not. **Verify with
`probe4.py` or `git status` before scoring a run.** Prefer scripted patches over
hand edits.

**Propagate from the right master.** A failed gate (`boerhaave` 12/14,
`duitslandlaan` 16/17) was caused by running `propagate_config.py` while the
edited config was still under a different filename — the copies were rebuilt
from the unmodified master. `git stash push config/` + re-run isolates
config-caused failures from code-caused ones in one step.

**`HANDOVER.md` section 3 is wrong** about the `2_Kabelkeuze` column order. The
real order is `functietype, kabel_B2CA_DRAK, kabel_CCA_DRAK, kabel_B2CA_JOBA,
kabel_CCA_JOBA, opmerking`.

## Section 0c — What changed on 2026-08-01

### Shipped

| Change | Effect |
|---|---|
| Four-column `2_Kabelkeuze` + `signaalfamilie` selector | 2195-06: 11% → **47%** |
| `METING_BUS` for NW-sens bus sensors | 2195-06: 96 → 106 cables |
| `_header_protocol` — protocol named in a column header | 7267: 58% → **71%** |
| `PANEL_INTERN` — reset/automaat/netwachter emit nothing | −3 wires 7267, −5 wires 2195-06 |
| Section banners + `bekabeling naar` removed from output | presentation only |
| `DEFAULT_HEADER_MAP` refactor + import assertion | fixed `curfrent_a` typo |

### Closed

**Q10 — panel-internal meldingen. ENCODED.** Second observation on 7267
(`Resetknop`, `Automaat 230V`, `Automaat 24V` — no cable in the manual) alongside
2195-06 (`RS-01`, `IA-01`, `NW-01`). Verified first that no locked project
contains these device names and no existing synonym collides. Now a
`PANEL_INTERN` functietype with a dedicated dispatch branch that flags and
returns. `overspanningsbeveiliging` deliberately excluded — 2195-06 wires the
*verdeelkast* variant and not the *regelkast* one.

**Section 5 hygiene: CS34ZB vs CS34ZC.** Rick: treat as equivalent for scoring.
Config unchanged.

### New — project 7267 (Apparatuurlijst, 24 wires)

**Q20 — supply spec on a separate row from the device it feeds.**
7267 has a row with `Onderdeel = Energiemeter`, `Specificatie = voeding 230V`, no
procescode and no I/O. It meets the group-header condition, is consumed as a
section name, and the voltage is discarded. The energiemeter row below it has a
procescode but its Specificatie says `Kamstrup multical 603` — no voltage.

Costs 1 wire. A carry-forward rule (hold a voltage from a consumed header row,
apply to the next device row without one, consume once) is drafted but **one
observation**, and it would be the only place the pipeline infers a relationship
between adjacent rows. Fix the input instead until a second project shows the same
convention.

**Q21 — a cable whose specification is not in the input at all.**
7267's manual gives the circulatiepomp `DRAK HULT CCA 4X2,5 MT, max 2,2kW`. The
functielijst has no voltage, no kW and no A on that row, and the `Zekering`/`kW`/`A`
columns are empty sheet-wide. Rick supplied it from outside the document.

**This is a different category from every other miss.** It sets a hard ceiling of
23/24 on blind accuracy for this project. Worth checking whether other manuals
contain cables with no derivable specification.

**Q22 — protocol location varies across five structural forms.**
Reviewed all eleven header layouts seen so far:

| Where the protocol lives | Layouts |
|---|---|
| A dedicated `Protocol` column | Coneco ×3 |
| A `Data` column | Kuijpers (Fonkel) |
| The `Databus` column | Kuijpers (1363) — same headers, different content |
| Inside an I/O count column | ZRD |
| A column *header* | 7267 (`modbus RTU`), Append1 (`MODbus-punten`) |
| Free text | Priva, 1363 remarks |

**Mechanism A (column header) is shipped.** Two remain:

- **Mechanism B — free-text extractor**, parallel to `_parse_electrical_spec`,
  reading `opmerking` then `omschrijving` when the column is empty. Would likely
  recover 2195-06's missing BMS row. Not built.
- **Mechanism C — the Kuijpers swap.** `bus_protocol` holds a point count and
  `bus_naam` holds the protocol on 1363, the reverse of Fonkel. Same client, same
  headers, inconsistent filling. Fix: `bus_protocol = bus_naam` when the former
  does not look like a protocol. Currently harmless — `_bus_row` falls through to
  the Modbus RTU default, which is right by luck. Would break on a BACnet/IP
  project. Not built.

**Q23 — three silent-drop mechanisms.**
Rows disappear with no flag in three places, each found this week by counting rows
by hand:

1. **M&R filter** — 45 of 130 named rows on 1363, of which ~14 were real RK861
   devices whose author never filled the column (~22 wires)
2. **Group-header heuristic** — 5 rows on 7267, of which 4 are correctly section
   markers and 1 carries a voltage (Q20)
3. **`emit()` early returns** — the `REGELKAST` case cost 6 pump feeds on 2195-06
   before it was fixed

A `SKIPPED (reason): <name> (source_ref)` line in `flags.txt` would have made all
three visible on the first run. Pure diagnostics, cannot change a cable, cannot
break the gate. **Not built — highest-value low-risk item outstanding.**

**Q24 — decimal commas lost in PDF→Excel extraction (input quality).**
1363's `IO_parsed.xlsx` holds `3060`/`5620` where the source PDF shows
`30,60`/`56,20`. Five of ten rows with power data affected; the five correct ones
arrive as floats, the wrong ones as ints. **Not a pipeline bug** — `_fnum` parses
what it is given.

Harmless today: `power_kw` and `current_a` do not affect cable choice. Would
corrupt Q18's current→cross-section lookup if that is ever built. Worth
spot-checking numeric columns against the source after any PDF extraction.

**Q25 — `feed_cable` still reads two columns.**
`signal_cable` was extended to four (fire class × brand); `feed_cable` still does
`row["kabel_B2CA"] if family == "B2CA" else row["kabel_CCA"]`, because
`3_Voedingen` only has two columns.

That matters because **three projects write feeds as CCA inside a B2CA/JOBA list**
— 7267, 1363, 2195-06. Same evidence as Q17. If Rick confirms fire class is
per-cable, `3_Voedingen` needs the same treatment.

### Strengthened

**Q17 — fire class is per-cable, not per-project. THIRD OBSERVATION.**
7267's manual: `DRAK HULT CCA 3G2,5 HA500` and `DRAK HULT CCA 4X2,5 MT`, in a list
that is otherwise entirely JOBA/B2CA. Same pattern as 1363 and 2195-06. This is
now the best-supported open finding and it reframes Q5: the problem may not be a
missing column but a wrong model.

**Rick's `X ≡ G` equivalence — confirmed in his own document.** 7267's manual
writes `4X2,5` where the config writes `4G2,5`.

**Sturing + storing on one row → two cables. SECOND OBSERVATION.**
7267's drycoolers: `3711DK01` appears twice in the manual —
`Dry-cooler storing` (`JOBA STUURSTR HHOZ 2X1`, unscreened) and
`Dry-cooler sturing` (`JOBA ST.STR B2CA HCHOZ 2X1`, screened). One input row,
DI=1 and AO=1. Identical in shape to 2195-06's radiators, and a cleaner example
because the two cables are visibly different types — exactly what Rick's screening
rule predicts.

**Rick's screening rule (2026-07-31).** Analogue signals normally take screened
cable (`1xNx…`); digital take unscreened (`Nx…`). Holds roughly 9 times in 10.
Stated exception: regelafsluiter and afsluiter always take `4x0,8` unscreened.

**Use as a review prompt, not an assertion.** An invariant wrong 10% of the time
gets disabled. And note `1x4x0,8` is **not** equivalent to `4x0,8` — screened
versus unscreened, analogue versus digital.

**`MELDING` requires DI, not DO.** 7267's `Storing urgent` / `Storing niet urgent`
(DO=1, no DI) are rejected by `_ok()` and the manual gives them no cable — right
outcome. But 2195-06's `Besturing GBS` rows (also DO=1) *are* wired in its manual,
bundled into the pump's `4X2X0.8`. Two projects, opposite correct answers. Worth a
question, not a change.