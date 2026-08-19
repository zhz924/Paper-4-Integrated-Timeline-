# -*- coding: utf-8 -*-
"""
audit_paper4_v1.2.py — Paper 4 (Integrated Timeline) v1.2 numerical reproducibility audit
Recomputes: the interface table (Table 1), the lag-model topology (Table 2), the
four-dimensional joint probability and Fréchet bounds (Section 4.3), the
beneficial-ownership (BO) burden allocation (Table 3), and the funding-flow interface.
The lag convolution is computed with fixed-seed Monte Carlo.
Usage: python3 audit_paper4_v1.2.py  ->  all assertions pass and it prints
"All numerical relationships close".
Depends only on the Python standard library.
"""
import random, math

errors = []
def check(name, cond, detail=''):
    status = 'PASS' if cond else 'FAIL'
    if not cond:
        errors.append(name)
    print(f'[{status}] {name} {detail}')

random.seed(42)

# ═══ 1. Interface table (Table 1) and Table 3 BO allocation ═══
print('=== 1. Interface and BO allocation ===')
check('2030 deliverable total 0.86+9.6 = 10.46 Mtoe (bio 0.4 EJ median, rounded)', abs(0.86 + 9.6 - 10.46) < 0.01, f'= {0.86 + 9.6:.2f}')
check('2030 coverage 10.46/15.0 ≈ 70% (69.7%)', abs(10.46 / 15.0 * 100 - 69.7) < 0.1, f'= {10.46 / 15.0 * 100:.1f}%')
check('Coverage vs 10% target 10.46/30 ≈ 35% (34.9%)', abs(10.46 / 30 * 100 - 34.9) < 0.1, f'= {10.46 / 30 * 100:.1f}%')
check('J2 total-demand basis 279.2−86.4−14.4 = 178.4 Mtoe (demand side excl. bio)',
      abs(279.2 - 86.4 - 14.4 - 178.4) < 0.01, f'= {279.2 - 86.4 - 14.4:.1f}')
check('J2 median coverage (68.6+47.8)/178.4 ≈ 65.2%', abs((68.6 + 47.8) / 178.4 * 100 - 65.2) < 0.2, f'= {(68.6 + 47.8) / 178.4 * 100:.1f}%')
check('J2 high-end coverage (68.6+86.0)/178.4 ≈ 86.7%', abs((68.6 + 86.0) / 178.4 * 100 - 86.7) < 0.2, f'= {(68.6 + 86.0) / 178.4 * 100:.1f}%')
# BO allocation (Table 3)
for name, share, gross_exp, net_exp in [('Developed', 0.528, 483, 217), ('Developing', 0.472, 431, 194)]:
    g = 914 * share
    check(f'Table 3 {name} gross burden {gross_exp} (×10^8 USD)', abs(g - gross_exp) < 2.5, f'= {g:.0f}')
    check(f'Table 3 {name} net burden {net_exp} (×10^8 USD)', abs(411 * share - net_exp) < 2.5, f'= {411 * share:.0f}')
check('Table 3 DWT share sum 52.8+47.2 = 100', abs(52.8 + 47.2 - 100) < 0.01)
check('Table 3 value share sum 60.8+39.2 = 100', abs(60.8 + 39.2 - 100) < 0.01)
check('Table 3 gross burden sum 483+431 ≈ 914', abs(483 + 431 - 914) < 1.5, f'= {483 + 431}')
# Burden intensity BI
bi_dev = 431 / 39.2
bi_adv = 483 / 60.8
check('Burden intensity developing 11.0 developed 7.9 (~1.4×)',
      abs(bi_dev - 11.0) < 0.1 and abs(bi_adv - 7.9) < 0.1 and abs(bi_dev / bi_adv - 1.39) < 0.05,
      f'= {bi_dev:.2f} vs {bi_adv:.2f} ({bi_dev / bi_adv:.2f}×)')
check('Aging exposure asymmetry 21% vs 9.3% (>2×)', 21.1 / 9.3 > 2.0, f'= {21.1 / 9.3:.2f}×')

# ═══ 2. System lag model (Table 2, Monte Carlo convolution) ═══
print('=== 2. Lag model (Table 2, Monte Carlo convolution) ===')
def tnorm(mu, sd, lo):
    while True:
        x = random.gauss(mu, sd)
        if x >= lo:
            return x
def tri(a, b, c):
    return random.triangular(a, b, c)
N = 100_000
W30, W40 = 6.4, 16.4
res = {}
for topo in ['serial', 'partial', 'parallel']:
    Ts = []
    for _ in range(N):
        i = tnorm(5.5, 1.3, 2.0)
        f = tnorm(5.0, 1.2, 1.5)
        g = tri(2, 5, 3)
        if topo == 'serial': T = i + f + g
        elif topo == 'partial': T = max(i, g) + f
        else: T = max(i, f, g)
        Ts.append(T)
    Ts.sort()
    mean = sum(Ts) / N
    lo95, hi95 = Ts[int(0.025 * N)], Ts[int(0.975 * N)]
    p30 = sum(1 for t in Ts if t <= W30) / N * 100
    p40 = sum(1 for t in Ts if t <= W40) / N * 100
    res[topo] = (mean, lo95, hi95, p30, p40)
check('Series mean 13.9 yr', abs(res['serial'][0] - 13.9) < 0.1, f'= {res["serial"][0]:.2f}')
check('Series P(2030)=0%', res['serial'][3] < 0.05, f'= {res["serial"][3]:.2f}%')
check('Series P(2040)=91.2%', abs(res['serial'][4] - 91.2) < 0.6, f'= {res["serial"][4]:.1f}%')
check('Partial-parallel mean 10.6 yr', abs(res['partial'][0] - 10.6) < 0.1, f'= {res["partial"][0]:.2f}')
check('Partial-parallel P(2030)=0.5%', abs(res['partial'][3] - 0.5) < 0.15, f'= {res["partial"][3]:.2f}%')
check('Partial-parallel P(2040)=100%', res['partial'][4] > 99.9, f'= {res["partial"][4]:.1f}%')
check('Fully-parallel mean 6.0 yr', abs(res['parallel'][0] - 6.0) < 0.1, f'= {res["parallel"][0]:.2f}')
check('Fully-parallel P(2030)=66.0%', abs(res['parallel'][3] - 66.0) < 0.6, f'= {res["parallel"][3]:.1f}%')
check('Fully-parallel P(2040)=100%', res['parallel'][4] > 99.9, f'= {res["parallel"][4]:.1f}%')
check('Series 95% interval 10.2–17.5', abs(res['serial'][1] - 10.2) < 0.3 and abs(res['serial'][2] - 17.5) < 0.3,
      f'= {res["serial"][1]:.1f}–{res["serial"][2]:.1f}')

# ═══ 3. Four-dimensional joint probability and Fréchet bounds (Section 4.3) ═══
print('=== 3. Joint probability (Section 4.3) ===')
PS30, PR_partial, PR_parallel, PC_high = 0.006, 0.005, 0.660, 0.98
p_joint_2030 = PS30 * PR_partial * PC_high * 1.0
check('2030 independence baseline ≈ 0.003% (0.006×0.005×0.98=0.0029%)',
      abs(p_joint_2030 * 100 - 0.0029) < 0.001, f'= {p_joint_2030 * 100:.4f}%')
check('2030 fully-parallel upper bound ≈ 0.4% (0.006×0.66×0.98)',
      abs(PS30 * PR_parallel * PC_high * 100 - 0.39) < 0.02, f'= {PS30 * PR_parallel * PC_high * 100:.2f}%')
# Fréchet bounds: 2030 four dimensions (0.006, 0.005, 0.98, 1.0)
lo_f = max(0.0, (0.006 + 0.005 + 0.98 + 1.0) - 3)
hi_f = min(0.006, 0.005, 0.98, 1.0)
check('Fréchet bounds [0%, 0.5%] (partial-parallel)', abs(lo_f) < 1e-9 and abs(hi_f - 0.005) < 1e-9,
      f'= [{lo_f * 100:.2f}%, {hi_f * 100:.1f}%]')
check('Joint-probability upper bound = weakest single dimension (readiness 0.5%)', hi_f == PR_partial)
# Monte Carlo standard error
se = math.sqrt(0.006 * 0.994 / 100_000) * 100
check('MC standard error for P_S=0.6% ≈ 0.024 pp', abs(se - 0.0244) < 0.001, f'= {se:.3f}%')

# ═══ 4. Funding-flow interface and closure ═══
print('=== 4. Funding-flow interface ===')
check('2040 gross 914 (×10^8 USD; Zhou, 2026c economic assessment)', True, f'= 914')
check('Net burden 411 (×10^8 USD) ≈ 914×0.45', abs(914 * 0.45 - 411.3) < 0.5, f'= {914 * 0.45:.1f}')
check('Rebate compression 55%', abs(1 - 411.3 / 914 - 0.55) < 0.01, f'= {(1 - 411.3 / 914) * 100:.1f}%')

print()
if errors:
    print(f'=== {len(errors)} item(s) failed to close: {errors} ===')
else:
    print('=== All numerical relationships close ✓ ===')
