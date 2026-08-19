# Paper 4 (Integrated Timeline) — Reproducibility Package v1.2

**Paper title:** Under what conditions does the IMO decarbonization timeline hold?
A joint stress test of supply, cost, environmental integrity and system readiness

**Author:** Zhou Haizhong (Beijiang Maritime Safety Administration, P.R. China)

This package reproduces the core numerical results and figures of Paper 4
(the Integrated Timeline paper). The scripts are English translations of the
original Chinese reproducibility package; **all numbers, formulas and logic are
unchanged** — only comments, print output, assertion descriptions, figure
labels and file names have been translated into English.

## Contents

```
Paper4_Reproducibility/
├── README.md                          # this file
├── audit_paper4_v1.2.py               # numerical reproducibility audit (33 assertions)
├── stress_test_v2.py                  # CORE MODEL: joint feasibility + GFI quadrants + BO
├── make_fig1_diagnosis.py             # Fig. 1 four-dimensional condition diagnosis
├── make_figures_p4_v1_1.py            # Fig. 2 system-readiness time distribution
├── make_fig3_joint_feasibility.py     # Fig. 3 four-dimensional joint feasibility
├── make_fig4_bo_burden.py             # Fig. 4 BO-burden allocation (4-panel complex)
├── make_fig5_scenario_matrix.py       # Fig. 5 joint-scenario decision matrix
├── make_fig6_dominant_constraint.py   # Fig. 6 dominant-constraint time shift (v2)
└── figures/
    ├── fig1_diagnosis.png
    ├── fig2_readiness_distribution.png
    ├── fig3_joint_feasibility.png
    ├── fig4_BO_burden.png
    ├── fig5_scenario_matrix.png
    └── fig6_dominant_constraint.png
```

## Figures

The package ships six figures, all rendered at **500 dpi**:

| Fig. | Output file | Script |
|------|-------------|--------|
| 1 | `figures/fig1_diagnosis.png` | `make_fig1_diagnosis.py` |
| 2 | `figures/fig2_readiness_distribution.png` | `make_figures_p4_v1_1.py` |
| 3 | `figures/fig3_joint_feasibility.png` | `make_fig3_joint_feasibility.py` |
| 4 | `figures/fig4_BO_burden.png` | `make_fig4_bo_burden.py` |
| 5 | `figures/fig5_scenario_matrix.png` | `make_fig5_scenario_matrix.py` |
| 6 | `figures/fig6_dominant_constraint.png` | `make_fig6_dominant_constraint.py` |

- **Fig. 1 — Four-dimensional condition diagnosis** (2×2 panel): (a) 2030 physical-supply
  coverage (5% target 70%, 10% target 35%, BAU lower bound 22%); (b) physical-attainment
  probability (2030 = 0.6% with 95% CI 0.5–0.7%, 2040 = 4.2%); (c) environmental
  carbon-intensity comparison (unconstrained 121.9 vs firewall 68.6 vs fossil baseline
  93.3 gCO₂e/MJ); (d) economic-affordability probability (high-RU 98%/100% and low-RU
  0%/44.7% for 2030/2040).
- **Fig. 2 — System-readiness time distribution** under the three lag topologies
  (Monte Carlo, n = 100,000, seed 42): series (mean 13.9 yr), partial-parallel (10.6 yr),
  fully-parallel (6.0 yr).
- **Fig. 3 — Four-dimensional joint feasibility**: 2030 single-dimension probabilities
  and joint result (0.6% × 0.5% × 98% × 100% ≈ 0.003%; Fréchet upper bound 0.5%), and
  2040 J2 supply–demand coverage (net demand 178.4 Mtoe; median coverage 65%, high-bound
  87%, gap 62.0 Mtoe / 35%).
- **Fig. 4 — Beneficial-ownership (BO) burden allocation** (4-panel complex version):
  (A) gross-burden allocation basis comparison, BO vs flag-state (total gross ≈ 914 ×10^8
  USD/yr: developed 483, developing 431); (B) value share vs gross-burden share mismatch
  (±8.0 pp); (C) burden intensity developing 11.0 vs developed 7.9 (≈1.4×);
  (D) 20+ yr vessel-age share developing 21.0% vs developed 9.3% (≈2.3×); net burden
  (after 50% rebate) totals ≈ 411 ×10^8 USD/yr (developed 217, developing 194).
- **Fig. 5 — Joint-scenario decision matrix**: dominant action directions of the J1–J9
  scenarios across the five decision dimensions (physical supply, environmental
  eligibility, economic affordability, system readiness, distributional equity).
- **Fig. 6 — Dominant-constraint time shift** (2025–2050, indexed stacked-area
  schematic; v2 with y-axis upper limit raised to 250).

## Scripts

- **`audit_paper4_v1.2.py`** — Numerical reproducibility audit. Recomputes:
  - the interface table (Table 1);
  - the lag-model topology (Table 2) via fixed-seed Monte Carlo convolution of the
    three subsystem lag distributions;
  - the four-dimensional joint probability and Fréchet bounds (Section 4.3);
  - the beneficial-ownership (BO) burden allocation (Table 3);
  - the funding-flow interface (gross/net burden and rebate compression).
  All 33 assertions must pass; on success the script prints
  `=== All numerical relationships close ✓ ===`. Depends only on the Python
  standard library.

- **`stress_test_v2.py`** — **Core model (joint analysis, n = 100,000, seed 20260803).**
  Generates the system-readiness probabilities under the three lag topologies, the
  four-dimensional joint feasibility probabilities, the absolute-abatement vs GFI-intensity
  quadrants (2008 baseline 1,018 MtCO₂e), the 2040 compliance-cost beneficial-ownership
  allocation (gross 91.4 bn USD), and the J1–J9 joint-scenario matrix directly from the
  parameters and the Paper 1/2/3 interface outputs. Requires `numpy`.

- **`make_fig1_diagnosis.py`** — Generates Fig. 1 (2×2 four-dimensional condition
  diagnosis, 500 dpi). Outputs `figures/fig1_diagnosis.png`. Depends on `numpy` and
  `matplotlib`.

- **`make_figures_p4_v1_1.py`** — Generates Fig. 2 (500 dpi): system-readiness time
  distribution under the three topologies (Monte Carlo, n = 100,000, seed 42).
  Outputs `figures/fig2_readiness_distribution.png`. Depends on `numpy` and
  `matplotlib`.

- **`make_fig3_joint_feasibility.py`** — Generates Fig. 3 (four-dimensional joint
  feasibility, 500 dpi). Outputs `figures/fig3_joint_feasibility.png`. Depends on
  `numpy` and `matplotlib`.

- **`make_fig4_bo_burden.py`** — Generates Fig. 4 (4-panel complex version, 500 dpi):
  gross-burden allocation basis comparison (BO vs flag-state), value-share vs
  gross-burden-share mismatch, burden intensity, and 20+ yr vessel-age (stranded-asset)
  exposure. Outputs `figures/fig4_BO_burden.png`. Depends on `numpy` and `matplotlib`.

- **`make_fig5_scenario_matrix.py`** — Generates Fig. 5 (J1–J9 joint-scenario decision
  matrix, 500 dpi). Outputs `figures/fig5_scenario_matrix.png`. Depends on `numpy` and
  `matplotlib`.

- **`make_fig6_dominant_constraint.py`** — Generates Fig. 6 (dominant-constraint time
  shift, 500 dpi). This is the v2 fix: in the v1.1 figure the stacked total at 2035
  reached 230 (60+80+55+35), exceeding the original y-axis upper limit of 210, so the
  top (system-readiness) layer was clipped; v2 raises the y-axis upper limit to 250 and
  lowers the node labels. Outputs `figures/fig6_dominant_constraint.png`.

**Audit vs. core model.** `audit_paper4_v1.2.py` is the *audit* script: it verifies
the numerical relationships already printed in the paper by recomputing each number
independently and asserting that it matches. `stress_test_v2.py` is the *core-model*
script: it generates the results directly from the parameters and the companion-paper
interfaces. Together they provide complete reproduction — the core model produces the
numbers and the audit confirms that every relation closes.

## Requirements

- Python 3.8+ (developed and tested on Python 3.12)
- `audit_paper4_v1.2.py`: standard library only.
- `stress_test_v2.py`: `numpy` (core-model Monte Carlo, seed 20260803, n = 100,000).
- `make_fig1_diagnosis.py`, `make_figures_p4_v1_1.py`, `make_fig3_joint_feasibility.py`,
  `make_fig4_bo_burden.py`, `make_fig5_scenario_matrix.py` and
  `make_fig6_dominant_constraint.py`: `numpy` and `matplotlib`.

Install dependencies:

```bash
pip install numpy matplotlib
```

## How to run

```bash
# 1) Numerical audit (all 33 assertions must print PASS)
python3 audit_paper4_v1.2.py

# 2) Core model: joint feasibility + GFI quadrants + BO allocation (requires numpy)
python3 stress_test_v2.py

# 3) Regenerate the six figures (outputs to ./figures/)
python3 make_fig1_diagnosis.py
python3 make_figures_p4_v1_1.py      # generates Fig. 2
python3 make_fig3_joint_feasibility.py
python3 make_fig4_bo_burden.py       # generates Fig. 4
python3 make_fig5_scenario_matrix.py
python3 make_fig6_dominant_constraint.py
```

The audit is deterministic (random seed 42), so re-running reproduces Table 2 and
all assertion values exactly.

## Data sources

- **Beneficial-ownership (BO) fleet panel** — UNCTADstat BO panel (2014–2026).
  2026: developed economies hold 52.8% of deadweight tonnage (DWT) and 60.8% of
  fleet value; developing economies hold 47.2% DWT and 39.2% value (two-group basis).
  Aging exposure: ~21% of developing-economy tonnage is aged 20+ years (partial
  subsample basis) vs 9.3% for developed economies.

- **Biofuel deliverable medians** — Ricardo & DNV biofuel medians (IMO, 2024b,
  MEPC 82/INF.8/Add.1, Table 1-2): 2030 = 9.6 Mtoe; 2040 = 47.8 Mtoe (high upper
  bound 86.0 Mtoe).

- **Lag-distribution parameters** (Table 2; start point 2023-07 / MEPC 80):
  - Infrastructure lag τ_infra ~ truncated normal (mean 5.5 yr, sd 1.3 yr, lower bound 2.0 yr)
  - Fleet-response lag τ_fleet ~ truncated normal (mean 5.0 yr, sd 1.2 yr, lower bound 1.5 yr)
  - Multilateral-governance lag τ_gov ~ triangular (2, 5, 3) yr
  - Checkpoint windows: 2030 ≈ 6.4 yr, 2040 ≈ 16.4 yr
  - Monte Carlo: n = 100,000, random seed = 42

- **Other inputs** — the physical-supply, environmental-integrity and economic
  dimensions are standardized outputs of the companion studies (Zhou, 2026a;
  2026b; 2026c). All values used by the audit are hard-coded in
  `audit_paper4_v1.2.py` so the paper can be re-checked from this single file.

## Units

Monetary amounts are expressed in units of 10^8 (hundred million) USD;
e.g. 914 × 10^8 USD = USD 91.4 bn.

## Data availability

Reproducibility package DOI: **10.5281/zenodo.XXXXXXX** *(placeholder — replace
with the assigned Zenodo DOI before submission)*.
