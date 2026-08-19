# -*- coding: utf-8 -*-
"""
stress_test_v2.py — integrated Paper 4 (integrated timeline) joint-analysis module
① four-dimensional joint feasibility probability ② absolute-abatement vs GFI-intensity four quadrants ③ system readiness probability ④ 2040 compliance-cost BO allocation ⑤ J1–J9 joint scenarios
Caliber: main parameter table v1.0 + Paper 1/2/3 interface outputs
"""
import numpy as np
import json

rng = np.random.default_rng(20260803)
N = 100000

# ═══ A. System readiness probability (lag topology, same parameters as the Paper 4 original model) ═══
def trunc_normal(mu, sigma, lo, n):
    x = rng.normal(mu, sigma, n)
    while True:
        m = x < lo
        if not m.any():
            return x
        x[m] = rng.normal(mu, sigma, m.sum())

tau_infra = trunc_normal(5.5, 1.3, 2.0, N)
tau_fleet = trunc_normal(5.0, 1.2, 1.5, N)
tau_gov = rng.triangular(2, 3, 5, N)
T_serial = tau_infra + tau_fleet + tau_gov
T_part = np.maximum(tau_infra, tau_gov) + tau_fleet
T_full = np.maximum(np.maximum(tau_infra, tau_gov), tau_fleet)
W2030, W2040 = 6.4, 16.4   # checkpoint windows counted from 2023.7
print('═══ A. System readiness probability ═══')
readiness = {}
for name, T in [('pure series', T_serial), ('partial parallel', T_part), ('fully parallel', T_full)]:
    p30 = float((T <= W2030).mean()); p40 = float((T <= W2040).mean())
    readiness[name] = dict(mean=float(T.mean()), p2030=p30, p2040=p40,
                           ci=[float(np.percentile(T, 2.5)), float(np.percentile(T, 97.5))])
    print(f'{name}: mean {T.mean():.1f} yr [2.5–97.5%: {np.percentile(T,2.5):.1f}–{np.percentile(T,97.5):.1f}], readiness year ≈{2023.6+T.mean():.1f} | P(before 2030)={p30:.1%} | P(before 2040)={p40:.1%}')

# ═══ B. Four-dimensional joint feasibility probability ═══
# Physical supply (2040, D-Central demand 133.6 Mtoe): electro log-normal (E-Low 3.3 / E-Central 16.9 / E-High 68.6, σ=25% anchor) + bio eligible U(36,60)
ln_med = np.log(16.9)
ln_sig = (np.log(68.6) - np.log(3.3)) / (2 * 1.645)   # with E-Low/E-High as P5/P95
S_electro_2040 = rng.lognormal(ln_med, ln_sig, N)
S_bio_2040 = rng.uniform(36, 60, N)                    # Paper 2 double-eligible ceiling 1.5–2.5 EJ
D_2040 = rng.triangular(78.6, 133.6, 262.4, N)         # D-Low/Central/High
P_phys_2040 = float((S_electro_2040 + S_bio_2040 >= D_2040).mean())
# 2030: demand 15 (5%), electro log-normal (median 0.86, upper-tail weighted 2.6), bio eligible U(7,12)
S_electro_2030 = rng.lognormal(np.log(0.86), (np.log(2.6)-np.log(0.86))/1.645, N)
S_bio_2030 = rng.uniform(7, 12, N)
D_2030 = rng.triangular(9, 15, 30, N)                  # S1-3% / S0-5% / S0-10%
P_phys_2030 = float((S_electro_2030 + S_bio_2030 >= D_2030).mean())
# Environmental eligibility: mixed CI≤94 (F regime compliant / U not); regime probability set as a scenario: P(F)=0.5 base
P_env = 0.5
# Economic affordability: 2040 P[MAC≤RU_high]=1.0; P[MAC≤RU_low]=0.632 (Paper 3); 2030: 0.999/0.001
P_econ_2030, P_econ_2040 = 0.98, 1.0
# Readiness: partial parallel as the base topology
P_ready_2030 = readiness['partial parallel']['p2030']
P_ready_2040 = readiness['partial parallel']['p2040']
P_ready_2030_full = readiness['fully parallel']['p2030']
joint_2030 = P_phys_2030 * P_env * P_econ_2030 * P_ready_2030
joint_2030_full = P_phys_2030 * P_env * P_econ_2030 * P_ready_2030_full
joint_2040 = P_phys_2040 * P_env * P_econ_2040 * P_ready_2040
print('\n═══ B. Four-dimensional joint feasibility probability (independence-assumption base) ═══')
print(f'2030 (partial parallel): physical {P_phys_2030:.1%} × environment {P_env:.0%} × economic {P_econ_2030:.0%} × readiness {P_ready_2030:.1%} = joint {joint_2030:.2%}')
print(f'2030 (fully parallel): readiness replaced by {P_ready_2030_full:.1%} → joint {joint_2030_full:.2%}')
print(f'2040 (partial parallel): physical {P_phys_2040:.1%} × environment {P_env:.0%} × economic {P_econ_2040:.0%} × readiness {P_ready_2040:.1%} = joint {joint_2040:.2%}')
# Copula sensitivity: positive correlation raises the joint tail (robustness of the joint probability to independence is described in text)

# ═══ C. Absolute-abatement vs GFI-intensity four quadrants ═══
print('\n═══ C. GFI four tiers × energy scenarios: absolute emissions and checkpoints (2008 baseline 1,018 MtCO₂e, −70%→305.4) ═══')
F_REF, F_FOSSIL, F_ZNZ = 94.0, 93.3, 10.0
EJ_PER_MTOE = 0.041868
BASE2008 = 1018.0
gfi_levels = {'lax 50%': 0.50, 'central 57%': 0.57, 'strict 65%': 0.65, 'checkpoint-compatible 76%': 0.7574}
energy_scen = {'320 Mtoe (base)': 320, '300 Mtoe (efficiency improvement)': 300, '280 Mtoe (strong efficiency)': 280}
quad = {}
for ename, mtoe in energy_scen.items():
    PJ = mtoe * EJ_PER_MTOE * 1000
    for gname, g in gfi_levels.items():
        target_int = F_REF * (1 - g)                      # GFI target intensity
        # energy substitution rate required to hit target_int (fossil 93.3 / ZNZ 10 mix)
        x = (F_FOSSIL - target_int) / (F_FOSSIL - F_ZNZ)
        x = min(max(x, 0), 1)
        emis = PJ * ((1 - x) * F_FOSSIL + x * F_ZNZ) / 1000
        abs_ok = emis <= BASE2008 * 0.30
        red = 1 - emis / BASE2008
        quad[(ename, gname)] = dict(emis=round(emis, 1), reduction=round(red * 100, 1), abs_ok=abs_ok)
        mark = '✅ both targets met' if abs_ok else '⚠️ GFI met but absolute target missed'
        print(f'{ename} × {gname}: target intensity {target_int:.1f} gCO₂e/MJ → substitution rate {x:.0%} → emissions {emis:.0f} Mt (vs 2008 −{red*100:.0f}%) → {mark}')

# ═══ D. 2040 compliance-cost beneficial-ownership allocation ═══
print('\n═══ D. 2040 compliance-cost beneficial-ownership allocation ═══')
RU_2040_GROSS = 91.4   # billion USD (Paper 3 Table 6)
RU_2040_NET = 41.1     # after 50% fund rebate
bo = {
    'developed economies': dict(dwt=0.528, value=0.608),
    'developing economies (excl. China)': dict(dwt=0.265, value=0.218),
    'China': dict(dwt=0.207, value=0.174),
}
for k, v in bo.items():
    print(f'{k}: gross burden by DWT share {v["dwt"]:.1%} = {RU_2040_GROSS*v["dwt"]:.1f} billion USD/yr (net {RU_2040_NET*v["dwt"]:.1f})')
print('Aged-ship exposure: developing economies 20+ yr tonnage share 21.1% vs developed economies 9.3% (Paper 4 original result)')
print('Unit burden intensity: developing economies (excl. China) DWT share 26.5% vs fleet-value share 21.8% — low-value tonnage bears a relatively higher burden')

# ═══ E. J1–J9 joint-scenario judgment ═══
print('\n═══ E. Joint-scenario judgment matrix ═══')
scen = [
    ('J1 continuation trend', 'E-Central', 'weak-medium', 'medium tier', 'partial parallel', '2030✗ / 2040✗ (physical gap + nominal compliance risk)'),
    ('J2 coordinated transition', 'E-High', 'strict F', 'high tier', 'fully parallel', '2030 marginal ✗ / 2040✓ (conditional achievement)'),
    ('J3 supply delay', 'E-Low', 'strict F', 'medium tier', 'partial parallel', '2030✗ / 2040✗ (hard physical constraint)'),
    ('J4 biofuel backstop', 'E-Low', 'weak U', 'medium tier', 'partial parallel', '2030✗ / 2040 nominal✓ actual✗ (net-emission-increase risk)'),
    ('J5 governance lag', 'E-Central', 'strict F', 'medium tier', 'series', '2030✗ / 2040 marginal (readiness tail risk)'),
    ('J6 fund recycling to supply side', 'E-Central→High', 'strict F', 'high tier', 'partial parallel', '2040✓ probability significantly increased'),
    ('J7 targeted compensation for developing economies', 'E-Central', 'strict F', 'medium tier', 'partial parallel', 'joint feasibility same as J1, distributive equity improved'),
    ('J8 low demand/high efficiency', 'E-Central', 'strict F', 'medium tier', 'partial parallel', '2040✓ (gap narrows to below 65–78% under D-Low)'),
    ('J9 high freight-growth pressure', 'E-Central', 'medium', 'medium tier', 'partial parallel', '2040✗ (demand uplift worsens the gap)'),
]
for row in scen:
    print(' | '.join(row))

json.dump(dict(readiness=readiness, P_phys_2030=P_phys_2030, P_phys_2040=P_phys_2040,
               joint_2030=joint_2030, joint_2030_full=joint_2030_full, joint_2040=joint_2040,
               quad={f'{k[0]}×{k[1]}': v for k, v in quad.items()}),
          open('/sandbox/workspace/integration_task/code/stress_v2_results.json', 'w'), ensure_ascii=False, indent=1)
print('\nsaved stress_v2_results.json')
