# Validation — Fonkel Breda (PR 20267276-2600214)
**Client layout:** Kuijpers · **Family:** B2CA / JOBA · **Panels:** RK071 + a "Tracing" sub-panel
**Compared:** blind output ↔ `PR20267276-2600214_Kabellijst.pdf` (10-7-2026, Rick van Deurzen)
**Status:** diffed, NOT yet locked as a regression — input file not yet supplied.

## Score
| Metric | Result |
|---|---|
| Rows in manual (RK071) | 61 (3 feeds + 58 cables) + Tracing panel (1 feed + 2 cables) |
| Rows correct | ~54 / 61 |
| **Blind score** | **~89%** |

Best blind result so far. Structurally a near-twin of Duitslandlaan, and it
reused everything Duitslandlaan taught: **zero cable-knowledge errors.** All
seven misses are structural.

## What matched
Every cable string and both families: buffer temps `HCHOZ 2X1`, druk/flow/
drukverschil `HCHJZ 5X1`, energiemeter voeding + MODbus, `Via aansluitsnoer` ×4,
transportpompen `4G2,5` + kW/A/V string, circ.pompen `3G2,5`, regelafsluiters
`STSTR 7X1`, Korex trio (voeding + storing + bus), E-ketel split
(vrijgave/storing 5X1 **+ separate** sturing 2X1), TSA temps ×4, brandmelding,
`doorlussen` chain behaviour.

## Diff — bucketed

| # | Manual | Blind output | Bucket | Action |
|---|---|---|---|---|
| 1 | 1 Regelkast row | 2 Regelkast rows (input has two RK rows) | **BUG** | dedup: at most one RK row |
| 2 | 1 "Warmtepomp" feed row (hoofd+secundair bundled) | 2 feed rows | **BUG** | bundle multi-feed devices |
| 3 | 1 bedrijfsmeldingen 12X1 | 2 (consequence of #2) | **BUG** | falls out of #2 |
| 4 | `Totaal derden = 1` | 2 | **BUG** | consequence of #1 |
| 5 | `Circulaite pomp 2` present (rows 59-60) | missing | **BUG** | duplicate procescode `091CP_21` collision |
| 6 | Groups: Warmtepomp / Buffervat GKW / Buffervat CV / Korex / Transport GKW / Transport CV / Deelstroomfilter / Elektrische ketel CV-MT | `proces 000`, `proces 071`, `proces 081` + junk (`TSA PN16`, `safety kit`, `Deelstroomfilter Deel-SEP GKW`) | **PARAM/structural** | **batched** — see below |
| 7 | `Buiten TR` on LT-CV buffer temps | `in TR` | **PARAM** | third location value; needs rule or review field |
| 8 | Separate "Tracing" panel (own Voedingen, `derden=0`, 2 cables) | folded into main list | **structural** | **batched** — see below |
| 9 | `Totaal ws = 0` (while 8 rows show ws=1) | 8 | **ASK** | **do not encode** |

## Acted on now (BUG)
- #1 Regelkast dedup — universally true, nothing to break
- #2/#3 Multi-feed bundling — Duitslandlaan has the identical WP pattern and its
  manual also bundles; its 18/18 currently passes only because the fixture
  pre-bundles. This fix makes the raw path match the reviewed path — fixes two
  projects at once.
- #5 Missing pump — a real bug regardless of house standard. Needs the input file
  to debug rather than guess.

## Batched (needs a 2nd observation before designing)
- **#6 Group naming.** The risk: Boerhaave's groups come *from the input*
  (`Warmtepomp 1/2/3`) and match its manual exactly — 15/15 passes today. Fonkel's
  input groups are equipment names, not house sections. Any design must satisfy
  *both* "input groups are authoritative" and "input groups are wrong". That is a
  design question, not a fix.
- **#8 Tracing sub-panel.** A panel with no RK code. Touches `run_per_rk`, which
  both regressions exercise. Pairs naturally with #6 — both are "how does a list
  split into sections/panels". Design once, with real data.

## Questions for the estimator (ASK)
- **`Totaal ws` = 0 while the ws column holds 8 entries.** Duitslandlaan showed
  the same with 10. Two projects, same contradiction → intentional or a template
  default, but *unexplained*. Encoding "always 0" would be inventing a rule from
  an artifact. **Needs Rick's answer.**

## Blocked on
`input.xlsx` — the functielijst that produced this. Without it, #5 and #6 are
guesswork.
