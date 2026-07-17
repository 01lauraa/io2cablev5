# Validation Protocol

How a new project gets validated and turned into a permanent regression.
Follow this every time; the discipline is what keeps 20 projects from breaking
each other.

---

## The loop

### 1. Run blind (Laura)
Fill in `0_Parameters` for the project. Run the pipeline. **Change nothing** —
no fixing the input, no tweaking config to make the output look better. A blind
run is the only honest measure of where the rules actually stand.

```bash
python -m io2cable.pipeline --config config/kabelconfig_<project>.xlsx \
    --input projects/<project>/input.xlsx \
    --header-map config/header_map_<client>.xlsx \
    --out projects/<project>/out_blind --rk RK01
```

### 2. Hand over four things (Laura → Claude)
Blind-run diagnosis without the input file wastes a round trip every time.
Put all four in `projects/<project>/`:

| File | Why it's needed |
|---|---|
| `input.xlsx` | without it, mismatches can't be traced to a cause |
| `manual.pdf` | the ground truth |
| `out_blind/` | the generated list **and** `flags.txt` |
| `config_used.xlsx` | which parameters produced this |

### 3. Diff and classify (Claude)
Every mismatch goes in exactly one bucket. The bucket determines the risk and
the action:

| Bucket | Meaning | Action | Risk |
|---|---|---|---|
| **BUG** | code contradicts its own rules | fix now | low |
| **CONFIG** | house standard not yet captured | cell edit in kabelconfig | low |
| **PARAM** | project-level choice, not derivable from the I/O list | new parameter + default | medium |
| **DATA** | input broken/ambiguous | review step, no code change | none |
| **ASK** | genuine unknown | question for the estimator | none |
| **ACCEPT** | correct deviation (routing, lengths, chain order) | document in the test | none |

Written up in `projects/<project>/validation.md`.

### 4. Decide what to act on (both)
- **BUG / CONFIG** → do now, they're bounded.
- **PARAM / structural** → **batch them.** One project is not enough signal to
  design against. Wait for the same need in a second or third project.
- **ASK** → never encode a rule from an artifact. Ask first.

Precedent: Fonkel's group-naming problem was held back because Boerhaave's
groups are correct *from the input* while Fonkel's are not. Designing on one
observation would have broken the other project.

### 5. Lock it in (Claude)
- fixture: `projects/<project>/normalized.csv` (post-review canonical rows)
- test: `projects/<project>/test.py` with **documented deviations** in the docstring
- register it in `run_all_tests.py`
- score it in `docs/SCORECARD.md`
- log every change in `docs/CHANGELOG.md` with bucket + source project + the row
  that proved it
- bump `docs/RULES.md` if a rule changed

### 6. Merge gate
**Nothing merges unless every regression passes.**

```bash
python run_all_tests.py
```

---

## Rules of engagement

1. **Never encode a rule from a single observation.** Twice is a pattern; once is
   a coincidence. The `Totaal ws = 0` contradiction has appeared in two projects
   and is *still* unencoded because it's unexplained, not just unobserved.
2. **The blind run is sacred.** Fixing the input first and then measuring tells
   you nothing about the rules.
3. **Regressions are the licence to change things.** The only reason we can say
   "this fix is safe" is that two other projects fail loudly if it isn't.
4. **Config over code.** If a change can be a cell edit, it must be.
5. **Flags are a feature.** A flagged uncertainty beats a confident wrong row.
6. **Provenance per claim.** Every rule in RULES.md cites the project and row
   that established it.

---

## Anatomy of a project folder

```
projects/<name>/
├── input.xlsx        # the client's functielijst (as received)
├── manual.pdf        # the estimator's cable list (ground truth)
├── config_used.xlsx  # parameters for this project
├── out_blind/        # untouched blind-run output + flags.txt
├── normalized.csv    # post-review canonical fixture
├── test.py           # regression, with deviations documented
└── validation.md     # the diff, bucketed
```
