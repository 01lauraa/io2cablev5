# Scorecard

Blind-run accuracy per project. **Blind** = untouched input, parameters filled,
nothing fixed to flatter the result. This is the honest measure of where the
rules stand; the post-fix regression score just proves the fix stuck.

---

## Projects

| # | Project | PR | Client layout | Family | Blind score | Regression | Date |
|---|---|---|---|---|---|---|---|
| 1 | Duitslandlaan Zoetermeer | 20267283 | Kuijpers | B2CA / JOBA | **~83%** structural, 24% exact-string | 18/18 ✅ | 2026-07 |
| 2 | Boerhaave Leiden | 20267275.1 | Coneco | CCA / mixed | **~20%** usable (3 causes at once) | 15/15 ✅ | 2026-07 |
| 3 | Fonkel Breda | 20267276 | Kuijpers | B2CA / JOBA | **~89%** (54/61 rows) | 18/18 ✅ | 2026-07 |

## Reading the numbers

**Duitslandlaan ~83%**: one wrong parameter (CCA instead of B2CA) accounted for
~35 of the misses. The rules were mostly right; the *setup* was wrong. Hence
`brandklasse` became mandatory-in-code.

**Boerhaave ~20%**: three independent failures stacked — wrong header map (new
client layout), corrupted input (dead formulas), and house rules never taught to
the config. Each was a one-time cost, not recurring variance. Re-running the same
project today: 15/15.

**Fonkel ~89%**: the best blind result, on a project structurally similar to
Duitslandlaan. All 7 misses were *structural* (grouping, dedup, sub-panel), zero
cable-knowledge errors. This is what the ceiling looks like when the family
parameter is right and the layout is known. After the v4 fixes it reproduces its
manual exactly on sections, feeds, totals and every cable string — the two
remaining deviations are the ws-total ASK and the un-modelled Tracing sub-panel.

## What the trend says

The per-project cost is **front-loaded per client layout and per house standard**,
not per project:

- new client layout → one header-map Excel (~15 min)
- new house-standard strings → ~10 config rows, no code
- new structural pattern → a code change, once

Fonkel needed no new cable knowledge at all — it reused everything Duitslandlaan
taught. That's the pattern to watch: **as layouts and standards accumulate, blind
scores should climb and the work should shift from CONFIG to nothing.**

## Target

Not 100%. The realistic ceiling is ~85–90% mechanical, with the remainder being
genuine human decisions — distances, daisy-chain order, third-party scope,
renovation states. The goal was never unattended generation; it is
**"everything manual" → "approve the exceptions"**.

A rising flag-to-error ratio is a *good* sign: it means the system increasingly
knows what it doesn't know.
