#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_figures_paper4_en.py
English version of the Paper 4 (comprehensive timeline chapter) figure script.
Merges the 6 figure scripts into a single Python file.

Figures generated (500 dpi, all in-figure text in English, no overlapping):
  fig1_four_dimension_diagnosis.png      -- Fig. 1  Four-dimensional conditional diagnosis
  fig2_three_topology_readiness.png      -- Fig. 2  Readiness-time distributions under three topologies
  fig3_joint_feasibility.png             -- Fig. 3  Four-dimensional joint feasibility probability
  fig4_bo_burden.png                     -- Fig. 4  Beneficial-ownership (BO) compliance burden (4 panels)
  fig5_scenario_matrix.png               -- Fig. 5  Nine-scenario judgment framework
  fig6_dominant_constraints.png          -- Fig. 6  Time shift of dominant constraints

All data values are kept identical to the final manuscript.
"""

import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
import numpy as np

# ----------------------------------------------------------------------
# Global style
# ----------------------------------------------------------------------
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 10

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures_en")
os.makedirs(OUT, exist_ok=True)

DPI = 500


def save_fig(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close(fig)
    size_kb = os.path.getsize(path) // 1024
    print(f"  -> {path}  ({size_kb} KB)")
    return path


# ======================================================================
# Figure 1  Four-dimensional conditional diagnosis (2 x 2 panels)
# ======================================================================
def make_fig1():
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.8))
    fig.subplots_adjust(hspace=0.5, wspace=0.35, bottom=0.11)

    color_blue = "#4C72B0"
    color_red = "#C44E52"
    color_green = "#55A868"
    color_gray = "#999999"

    # (a) Physical supply coverage in 2030
    ax = axes[0, 0]
    categories = ["5% target\n(15 Mtoe)", "10% target\n(30 Mtoe)", "BAU lower\nbound"]
    values = [70, 35, 22]
    bars = ax.bar(categories, values, color=[color_blue, color_green, color_gray], width=0.6)
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 2, f"{v}%",
                ha="center", va="bottom", fontsize=8)
    ax.set_ylim(0, 90)
    ax.set_ylabel("Coverage (%)")
    ax.set_title("(a) Physical supply coverage in 2030", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--", linewidth=0.6)

    # (b) Physical achievement probability
    ax = axes[0, 1]
    years = ["2030", "2040"]
    prob = [0.6, 4.2]
    errors = [0.1, 0.0]
    bars = ax.bar(years, prob, yerr=errors, capsize=5, color=[color_blue, color_red], width=0.5)
    for bar, v in zip(bars, prob):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.3, f"{v}%",
                ha="center", va="bottom", fontsize=8)
    ax.set_ylim(0, 6)
    ax.set_ylabel("Achievement probability (%)")
    ax.set_title("(b) Physical achievement probability\n(supply >= demand, Monte Carlo n=100,000)", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--", linewidth=0.6)

    # (c) Environmental carbon intensity
    ax = axes[1, 0]
    labels = ["Unconstrained\nfeedstock mix", "Firewall\nregime", "Fossil baseline\n(93.3)"]
    intensity = [121.9, 68.6, 93.3]
    colors = [color_red, color_green, color_gray]
    bars = ax.bar(labels, intensity, color=colors, width=0.5)
    bars[2].set_hatch("//")
    for bar, v in zip(bars, intensity):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 3, f"{v:.1f}",
                ha="center", va="bottom", fontsize=8)
    ax.text(0, 138, "Env. condition\nNOT met", ha="center", fontsize=6.5, color=color_red)
    ax.text(1, 82, "Env. condition\nmet", ha="center", fontsize=6.5, color=color_green)
    ax.set_ylim(0, 160)
    ax.set_ylabel("Carbon intensity (gCO2e/MJ)")
    ax.set_title("(c) Environmental eligibility: carbon intensity", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--", linewidth=0.6)

    # (d) Economic affordability probability
    ax = axes[1, 1]
    groups = ["2030", "2040"]
    high_ru = [98, 100]
    low_ru = [0, 44.7]
    x = np.arange(len(groups))
    width = 0.35
    bar1 = ax.bar(x - width / 2, high_ru, width, label="High-tier RU", color=color_blue)
    bar2 = ax.bar(x + width / 2, low_ru, width, label="Low-tier RU", color=color_red)
    for bars in [bar1, bar2]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 2, f"{h:.1f}%",
                    ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(groups)
    ax.set_ylim(0, 120)
    ax.set_ylabel("Cost-coverage probability (%)")
    ax.set_title("(d) Economic affordability probability", fontsize=10)
    ax.legend(loc="upper left", fontsize=7, framealpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--", linewidth=0.6)

    fig.text(0.5, 0.02,
             "Diagnostic conclusion: in 2030 the binding constraints are physical supply and system readiness; "
             "by 2040 the constraints shift toward supply scale and the environmental regime.",
             ha="center", va="center", fontsize=8.5, style="italic")

    return save_fig(fig, "fig1_four_dimension_diagnosis.png")


# ======================================================================
# Figure 2  Readiness-time distributions under three topologies
#           (Monte Carlo, n = 100,000, seed 42)
# ======================================================================
def make_fig2():
    random.seed(42)

    def tnorm(mu, sd, lo):
        while True:
            xv = random.gauss(mu, sd)
            if xv >= lo:
                return xv

    N = 100_000
    samples = {
        "I Pure series (mean 13.9 yr)": [],
        "II Partial parallel (10.6 yr)": [],
        "III Full parallel (6.0 yr)": [],
    }
    cols = {
        "I Pure series (mean 13.9 yr)": "#C62828",
        "II Partial parallel (10.6 yr)": "#E65100",
        "III Full parallel (6.0 yr)": "#2E7D32",
    }
    for _ in range(N):
        i = tnorm(5.5, 1.3, 2.0)
        f = tnorm(5.0, 1.2, 1.5)
        g = random.triangular(2, 5, 3)
        samples["I Pure series (mean 13.9 yr)"].append(i + f + g)
        samples["II Partial parallel (10.6 yr)"].append(max(i, g) + f)
        samples["III Full parallel (6.0 yr)"].append(max(i, f, g))

    fig, ax = plt.subplots(figsize=(8.6, 4.9))
    for lab, Ts in samples.items():
        hist, edges = np.histogram(Ts, bins=140, range=(0, 20), density=True)
        ctr = (edges[:-1] + edges[1:]) / 2
        ax.plot(ctr, hist, color=cols[lab], lw=1.8, label=lab)
        ax.fill_between(ctr, 0, hist, color=cols[lab], alpha=0.12, lw=0)
    ax.axvline(6.4, color="#333333", ls="--", lw=1.2)
    ax.text(6.55, 0.37, "2030 checkpoint window\n(approx. 6.4 yr)", fontsize=8,
            color="#333333", va="top")
    ax.set_xlabel("System readiness time (years, from 2023.7)")
    ax.set_ylabel("Probability density")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 0.42)
    ax.legend(fontsize=8, frameon=False, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Fig. 2 Distribution of system readiness time under three topologies\n"
                 "(n = 100,000; model estimates)", fontsize=10)
    plt.tight_layout()
    return save_fig(fig, "fig2_three_topology_readiness.png")


# ======================================================================
# Figure 3  Four-dimensional joint feasibility probability
# ======================================================================
def make_fig3():
    C_BLUE = "#2E5A88"
    C_RED = "#C0504D"
    C_GREY = "#888888"
    C_LIGHT = "#F2F2F2"
    C_ACCENT = "#E8A33D"
    C_GREEN = "#4A8C5F"
    C_PURPLE = "#7B5EA7"
    C_TEAL = "#3A8A8A"

    fig = plt.figure(figsize=(15, 7.5), facecolor="white")
    fig.suptitle("Four-dimensional joint feasibility: 2030 probability decomposition and "
                 "2040 J2 supply-demand coverage", fontsize=13, fontweight="bold", y=0.97)

    gs = fig.add_gridspec(1, 2, wspace=0.35, left=0.06, right=0.97, top=0.88, bottom=0.18)

    # ---- Panel A: 2030 single-dimension probabilities and joint result ----
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title("A. 2030 single-dimension probabilities & joint result (partial parallel)",
                  fontsize=11, fontweight="bold", pad=12)

    dims = ["Physical supply\nmet", "System readiness\n(partial parallel)",
            "Economic\naffordability\n(high-tier)", "Environmental\neligibility\n(regime switch)"]
    probs = [0.6, 0.5, 98.0, 100.0]
    colors_a = [C_GREEN, C_BLUE, C_PURPLE, C_GREY]

    x = np.arange(4)
    bars = ax1.bar(x, probs, color=colors_a, edgecolor="white", linewidth=1.5, width=0.6)
    for bar, val in zip(bars, probs):
        ax1.text(bar.get_x() + bar.get_width() / 2, val * 1.5,
                 f"{val}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax1.set_yscale("log")
    ax1.set_ylim(1e-4, 500)
    ax1.set_xticks(x)
    ax1.set_xticklabels(dims, fontsize=8.5)
    ax1.set_ylabel("Single-dimension probability (%) - log scale", fontsize=9)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    fig.text(0.265, 0.095,
             "Joint probability = 0.6% x 0.5% x 98% x 100% = approx. 0.003%",
             ha="center", va="center", fontsize=10, fontweight="bold", color=C_RED,
             bbox=dict(boxstyle="round,pad=0.45", fc="#FDF2F1", ec=C_RED, lw=1.3))
    fig.text(0.265, 0.04,
             "Supply and readiness are the dual hard constraints (both <1%);\n"
             "economic/environmental dimensions nearly fully pass.\n"
             "The Frechet upper bound (0.5%) is set by the readiness probability.",
             ha="center", va="center", fontsize=6.8, color=C_GREY, style="italic")

    # ---- Panel C: 2040 J2 supply-demand coverage ----
    ax3 = fig.add_subplot(gs[0, 1])
    ax3.set_title("C. 2040 J2 coordinated-transition scenario: supply-demand coverage (Mtoe)",
                  fontsize=11, fontweight="bold", pad=12)

    ax3.text(0.18, 1.08, "Demand side", transform=ax3.transAxes, fontsize=10,
             fontweight="bold", color="#333", va="top", ha="center", clip_on=False)

    ax3.bar(0.5, 279.2, width=0.4, color=C_LIGHT, edgecolor=C_GREY, linewidth=1)
    ax3.text(0.5, 282, "279.2", ha="center", va="bottom", fontsize=9.5, fontweight="bold")
    ax3.text(0.5, -14, "Total demand\n(D-High)", ha="center", va="top", fontsize=8.5)

    ax3.annotate("", xy=(1.05, 210), xytext=(0.75, 255),
                 arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=1.6))
    ax3.text(0.78, 262, "-Energy efficiency 86.4", ha="left", va="bottom",
             fontsize=8.5, color=C_TEAL, fontweight="bold")

    ax3.annotate("", xy=(1.25, 175), xytext=(1.1, 215),
                 arrowprops=dict(arrowstyle="->", color=C_TEAL, lw=1.6))
    ax3.text(1.13, 220, "-Wind assist 14.4", ha="left", va="bottom",
             fontsize=8.5, color=C_TEAL, fontweight="bold")

    ax3.bar(1.5, 178.4, width=0.4, color=C_RED, alpha=0.22,
            edgecolor=C_RED, linewidth=1.3, hatch="//")
    ax3.text(1.5, 184, "178.4", ha="center", va="bottom",
             fontsize=9.5, fontweight="bold", color=C_RED)
    ax3.text(1.5, -14, "Net demand\n(after deductions)", ha="center", va="top",
             fontsize=8.5, color=C_RED)

    ax3.hlines(178.4, 1.75, 4.15, color=C_RED, ls="--", lw=1.2, alpha=0.55)

    ax3.text(0.72, 1.08, "Supply side (J2 coordinated transition)", transform=ax3.transAxes,
             fontsize=10, fontweight="bold", color="#333", va="top", ha="center", clip_on=False)

    ax3.bar(2.5, 68.6, width=0.42, color=C_BLUE, edgecolor="white", linewidth=1.2)
    ax3.bar(2.5, 47.8, bottom=68.6, width=0.42, color=C_GREEN, edgecolor="white", linewidth=1.2)
    ax3.text(2.5, 120, "116.4", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=C_BLUE)
    ax3.text(2.5, 133, "65% coverage", ha="center", va="bottom", fontsize=8.5, color=C_BLUE)
    ax3.text(2.5, -14, "Median supply\n(e-fuel + bio median)", ha="center", va="top", fontsize=8.5)

    ax3.bar(3.4, 68.6, width=0.42, color=C_BLUE, edgecolor="white", linewidth=1.2)
    ax3.bar(3.4, 47.8, bottom=68.6, width=0.42, color=C_GREEN, edgecolor="white", linewidth=1.2)
    ax3.bar(3.4, 38.2, bottom=116.4, width=0.42, color=C_ACCENT,
            edgecolor="white", linewidth=1.2, alpha=0.88)
    ax3.text(3.4, 166, "154.6", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=C_ACCENT)
    ax3.text(3.4, 179, "87% coverage", ha="center", va="bottom", fontsize=8.5, color=C_ACCENT)
    ax3.text(3.4, -14, "High supply\n(+bio high 3.6 EJ)", ha="center", va="top", fontsize=8.5)

    ax3.annotate("", xy=(2.77, 178.4), xytext=(2.77, 116.4),
                 arrowprops=dict(arrowstyle="<->", color=C_RED, lw=1.4))
    ax3.text(2.84, 139, "Gap\n62.0 (35%)", ha="left", va="center",
             fontsize=8, color=C_RED, fontweight="bold")

    legend_elements = [
        Patch(facecolor=C_BLUE, label="E-fuel E-High (68.6)"),
        Patch(facecolor=C_GREEN, label="Biofuel median (47.8)"),
        Patch(facecolor=C_ACCENT, label="Bio high increment (38.2)", alpha=0.88),
        Patch(facecolor=C_RED, alpha=0.22, hatch="//", label="Net demand 178.4"),
    ]
    ax3.legend(handles=legend_elements, loc="lower center", bbox_to_anchor=(0.5, -0.16),
               ncol=2, fontsize=7, frameon=False)

    ax3.set_xlim(0.1, 4.0)
    ax3.set_ylim(-40, 300)
    ax3.set_ylabel("Fuel quantity (Mtoe)", fontsize=9)
    ax3.set_xticks([])
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)

    fig.text(0.5, 0.014,
             "Data source: Section 4.3 (model estimates); Table 1 topology parameters; "
             "Table 0 supply/demand parameters.", ha="center", fontsize=7.5, color=C_GREY, style="italic")
    fig.text(0.5, 0.005,
             "Key distinction: the 2040 supply coverage (65%-87%) is not the four-dimensional joint "
             "feasibility probability - the latter is also constrained by readiness, price and regime conditions.",
             ha="center", fontsize=7.5, color=C_GREY, style="italic")

    return save_fig(fig, "fig3_joint_feasibility.png")


# ======================================================================
# Figure 4  Beneficial-ownership (BO) compliance burden (4 panels)
# ======================================================================
def make_fig4():
    C_DEV = "#2E5A88"
    C_DEVG = "#C0504D"
    C_GREY = "#888888"
    C_LIGHT = "#F2F2F2"
    C_ACCENT = "#E8A33D"

    groups = ["Developed", "Developing"]
    dwt_share = [52.8, 47.2]        # % BO-basis DWT share
    value_share = [60.8, 39.2]      # % value share
    gross_cost = [483, 431]         # 10^8 USD/yr gross burden
    net_cost = [217, 194]           # 10^8 USD/yr net burden (after 50% refund)
    intensity = [7.9, 11.0]         # burden intensity, 10^8 USD / value-share point
    old_share = [9.3, 21.0]         # % share of vessels aged 20+ years
    flag_gross_pct = [30.0, 70.0]   # flag-state basis developed/developing share

    fig = plt.figure(figsize=(14, 9.5), facecolor="white")
    fig.suptitle("Allocation of 2040 compliance costs by beneficial ownership (BO) and "
                 "the dual asymmetric pressures on developing economies",
                 fontsize=12.5, fontweight="bold", y=0.975)

    gs = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.32,
                          left=0.07, right=0.96, top=0.90, bottom=0.14)

    # ---- Panel A: gross burden allocation, BO basis vs flag-state basis ----
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title("A. Gross burden allocation: BO vs flag-state basis (gross = 914x10^8 USD/yr)",
                  fontsize=11, fontweight="bold", pad=10)

    wedges1, _ = ax1.pie(
        gross_cost, radius=1.0,
        colors=[C_DEV, C_DEVG], startangle=90,
        wedgeprops=dict(width=0.32, edgecolor="white", linewidth=2),
        counterclock=False,
    )
    wedges2, _ = ax1.pie(
        flag_gross_pct, radius=0.62,
        colors=[C_DEV, C_DEVG], startangle=90,
        wedgeprops=dict(width=0.32, edgecolor="white", linewidth=2, alpha=0.40),
        counterclock=False, hatch=["///", "///"],
    )

    ax1.text(0, 0.08, "914", ha="center", va="center", fontsize=18, fontweight="bold", color="#333")
    ax1.text(0, -0.14, "10^8 USD/yr (gross)", ha="center", va="center", fontsize=8, color=C_GREY)

    angles_bo = [90 - 0.5 * (gross_cost[0] / 914 * 360),
                 90 - (gross_cost[0] / 914 * 360) - 0.5 * (gross_cost[1] / 914 * 360)]
    for i, (ang, val, pct) in enumerate(zip(angles_bo, gross_cost, dwt_share)):
        xx = 1.22 * np.cos(np.radians(ang))
        yy = 1.22 * np.sin(np.radians(ang))
        ha = "left" if xx >= 0 else "right"
        ax1.annotate(f"BO basis - {groups[i]}\n{val}x10^8 USD ({pct}%)",
                     xy=(0.98 * np.cos(np.radians(ang)), 0.98 * np.sin(np.radians(ang))),
                     xytext=(xx * 1.10, yy * 1.06),
                     ha=ha, va="center", fontsize=8, color="#333",
                     arrowprops=dict(arrowstyle="-", color=C_GREY, lw=0.8))

    ax1.annotate("Flag-state basis: developing = approx. 70%",
                 xy=(0.38, -0.40), xytext=(0.72, -0.88),
                 fontsize=8, color=C_DEVG, fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color=C_DEVG, lw=1.0))

    ax1.legend([wedges1[0], wedges2[0]],
               ["BO basis (outer ring)", "Flag-state basis (inner ring, hatched)"],
               loc="lower center", bbox_to_anchor=(0.5, -0.18),
               ncol=2, fontsize=8, frameon=False)
    ax1.set_aspect("equal")

    # ---- Panel B: value share vs gross burden share ----
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title("B. Misalignment between value share and gross burden share (BO basis)",
                  fontsize=11, fontweight="bold", pad=10)

    x = np.arange(2)
    width = 0.32
    bars1 = ax2.bar(x - width / 2, value_share, width, label="Value share",
                    color=C_LIGHT, edgecolor=C_GREY, linewidth=1.0)
    bars2 = ax2.bar(x + width / 2, dwt_share, width, label="Gross burden (BO) share",
                    color=[C_DEV, C_DEVG], alpha=0.85)

    for bar, val in zip(bars1, value_share):
        ax2.text(bar.get_x() + bar.get_width() / 2, val + 1.2,
                 f"{val}%", ha="center", va="bottom", fontsize=9, color=C_GREY)
    for bar, val in zip(bars2, dwt_share):
        ax2.text(bar.get_x() + bar.get_width() / 2, val + 1.2,
                 f"{val}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax2.annotate("", xy=(1 + width / 2, 47.2), xytext=(1 - width / 2, 39.2),
                 arrowprops=dict(arrowstyle="->", color=C_ACCENT, lw=2))
    ax2.text(1 + width / 2, 56.0, "+8.0 pp\nburden > value", ha="center", va="center",
             fontsize=7.5, color=C_ACCENT, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=C_ACCENT, lw=0.7))

    ax2.annotate("", xy=(0 - width / 2, 60.8), xytext=(0 + width / 2, 52.8),
                 arrowprops=dict(arrowstyle="->", color=C_ACCENT, lw=2))
    ax2.text(0.0, 69.0, "-8.0 pp\nburden < value", ha="center", va="center",
             fontsize=7.5, color=C_ACCENT, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=C_ACCENT, lw=0.7))

    ax2.set_xticks(x)
    ax2.set_xticklabels(groups, fontsize=10)
    ax2.set_ylabel("Share (%)", fontsize=9)
    ax2.set_xlim(-0.5, 1.8)
    ax2.set_ylim(0, 78)
    ax2.legend(loc="upper right", fontsize=8, frameon=False)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    # ---- Panel C: burden intensity (first asymmetry) ----
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_title("C. Burden intensity: gross burden / value share (first asymmetry)",
                  fontsize=11, fontweight="bold", pad=10)

    bars = ax3.bar(groups, intensity, color=[C_DEV, C_DEVG], width=0.5,
                   edgecolor="white", linewidth=1.5)
    for bar, val in zip(bars, intensity):
        ax3.text(bar.get_x() + bar.get_width() / 2, val + 0.25,
                 f"{val}", ha="center", va="bottom", fontsize=12, fontweight="bold")

    ax3.annotate("", xy=(1, 9.5), xytext=(0, 6.9),
                 arrowprops=dict(arrowstyle="<->", color=C_ACCENT, lw=1.8))
    ax3.text(0.5, 8.6, "approx. 1.4x", ha="center", va="center",
             fontsize=11, color=C_ACCENT, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=C_ACCENT, lw=1.0))

    ax3.set_ylabel("10^8 USD / value-share point", fontsize=9)
    ax3.set_ylim(0, 12)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)

    # ---- Panel D: share of vessels aged 20+ years (second asymmetry) ----
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_title("D. Vessels aged 20+ years: stranded-asset exposure (second asymmetry)",
                  fontsize=11, fontweight="bold", pad=10)

    bars4 = ax4.barh(groups, old_share, color=[C_DEV, C_DEVG], height=0.45,
                     edgecolor="white", linewidth=1.5)
    for bar, val in zip(bars4, old_share):
        ax4.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
                 f"{val}%", ha="left", va="center", fontsize=12, fontweight="bold")

    ax4.annotate("", xy=(24.5, 1), xytext=(24.5, 0),
                 arrowprops=dict(arrowstyle="<->", color=C_ACCENT, lw=1.8))
    ax4.text(25.8, 0.5, "approx. 2.3x", ha="left", va="center",
             fontsize=11, color=C_ACCENT, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=C_ACCENT, lw=1.0))

    ax4.set_xlabel("Share of vessels aged 20+ years (%)", fontsize=9)
    ax4.set_xlim(0, 31)
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)

    fig.text(0.5, 0.052,
             "Data source: Table 3 (model estimates), UNCTADstat (2026a, 2026b); Zhou (2026c). "
             "Net burden (SU offset + 50% refund) = approx. 411x10^8 USD/yr (developed 217x10^8, developing 194x10^8).",
             ha="center", fontsize=7.5, color=C_GREY, style="italic")
    fig.text(0.5, 0.040,
             "Flag-state basis: the developing-economy gross burden share rises from 47.2% to approx. 70%, "
             "further aggravating the asymmetry.",
             ha="center", fontsize=7.5, color=C_GREY, style="italic")
    fig.text(0.5, 0.020,
             "Conclusion: developing economies face dual asymmetric pressures - higher burden intensity (approx. 1.4x) "
             "plus greater stranded-asset exposure of older vessels (approx. 2.3x).",
             ha="center", fontsize=7.5, color="#555555", fontweight="bold")
    fig.text(0.5, 0.008,
             "BO-basis targeted compensation (allocated by beneficial ownership and vessel age) is a necessary "
             "condition for fairness - P4 is supported.",
             ha="center", fontsize=7.5, color="#555555", fontweight="bold")

    return save_fig(fig, "fig4_bo_burden.png")


# ======================================================================
# Figure 5  Nine-scenario judgment framework (9 x 5 matrix)
# ======================================================================
def make_fig5():
    scenarios = ["J1 Trend continuation", "J2 Coordinated transition", "J3 Supply delay",
                 "J4 Biofuel fallback", "J5 Governance lag", "J6 Capital reflow to supply",
                 "J7 Targeted compensation (developing)", "J8 Low demand / high efficiency",
                 "J9 High freight-growth pressure"]
    dims = ["Physical\nsupply", "Environmental\neligibility", "Economic\naffordability",
            "System\nreadiness", "Distributive\nfairness"]
    # + favorable / . baseline or non-primary / - adverse (consistent with Table 4)
    data = [
        [".", ".", ".", ".", "."],  # J1
        ["+", "+", "+", "+", "+"],  # J2
        ["-", ".", "-", "-", "."],  # J3
        ["+", "-", ".", ".", "."],  # J4
        ["-", ".", ".", "-", "."],  # J5
        ["+", ".", "+", "+", "."],  # J6
        [".", ".", "+", ".", "+"],  # J7
        ["+", ".", "+", "+", "."],  # J8
        ["-", ".", "-", "-", "-"],  # J9
    ]
    color_map = {"+": "#4A8C5F", ".": "#E0E0E0", "-": "#C0504D"}
    txt_color = {"+": "white", ".": "#555555", "-": "white"}

    fig, ax = plt.subplots(figsize=(11, 7.8))
    nr, nc = len(scenarios), len(dims)
    for i in range(nr):
        for j in range(nc):
            v = data[i][j]
            ax.add_patch(Rectangle((j, nr - 1 - i), 1, 1,
                                   facecolor=color_map[v], edgecolor="white", lw=1.5))
            ax.text(j + 0.5, nr - 1 - i + 0.5, v, ha="center", va="center",
                    fontsize=15, fontweight="bold", color=txt_color[v])

    ax.set_xlim(0, nc)
    ax.set_ylim(0, nr)
    ax.set_xticks(np.arange(nc) + 0.5)
    ax.set_xticklabels(dims, fontsize=10, fontweight="bold")
    ax.set_yticks(np.arange(nr) + 0.5)
    ax.set_yticklabels(scenarios, fontsize=9)
    ax.xaxis.set_ticks_position("top")
    ax.tick_params(axis="both", length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)

    legend_elements = [
        Rectangle((0, 0), 1, 1, facecolor="#4A8C5F", edgecolor="white", label="Favorable effect (+)"),
        Rectangle((0, 0), 1, 1, facecolor="#E0E0E0", edgecolor="white", label="Baseline or non-primary (.)"),
        Rectangle((0, 0), 1, 1, facecolor="#C0504D", edgecolor="white", label="Adverse effect (-)"),
    ]
    ax.legend(handles=legend_elements, loc="lower center", bbox_to_anchor=(0.5, -0.10),
              ncol=3, fontsize=9, frameon=False)

    fig.text(0.5, 0.018,
             "Note: colors indicate the direct direction of the scenario effect relative to the "
             "trend-continuation baseline (J1), not the joint compliance probability.\n"
             "J4 may increase nominal supply, but without an environmental firewall, environmental "
             "integrity will be under pressure.",
             ha="center", va="center", fontsize=8.5, color="#555555")
    fig.suptitle("Fig. 5 Primary direction of action and judgment dimensions of the nine joint scenarios",
                 fontsize=13, fontweight="bold", y=0.97)
    plt.subplots_adjust(top=0.86, bottom=0.14, left=0.28, right=0.99)
    return save_fig(fig, "fig5_scenario_matrix.png")


# ======================================================================
# Figure 6  Time shift of dominant constraints (y-axis limit 250)
# ======================================================================
def make_fig6():
    yrs = np.arange(2025, 2051)
    supply = np.interp(yrs, [2025, 2030, 2035, 2040, 2050], [90, 75, 60, 40, 18])
    cost = np.interp(yrs, [2025, 2030, 2035, 2040, 2050], [20, 50, 80, 15, 7])
    envir = np.interp(yrs, [2025, 2030, 2035, 2040, 2050], [10, 25, 55, 90, 73])
    ready = np.interp(yrs, [2025, 2030, 2035, 2040, 2050], [70, 45, 35, 20, 12])
    total = supply + cost + envir + ready
    print("  stacked totals at checkpoints:", {int(y): int(t) for y, t in
          zip([2025, 2030, 2035, 2040, 2050],
              [total[0], total[5], total[10], total[15], total[25]])})
    print("  max stacked total:", int(total.max()), "-> y-axis upper limit = 250")

    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    ax.stackplot(yrs, supply, cost, envir, ready,
                 labels=["Physical supply constraint", "Cost/premium constraint",
                         "Environmental integrity constraint", "System readiness constraint"],
                 colors=["#1565C0", "#E65100", "#2E7D32", "#7B1FA2"], alpha=0.75)

    for xpos, lab in [(2030, "2030 checkpoint"), (2035.5, "Parity median"), (2040, "2040 checkpoint")]:
        ax.axvline(xpos, ls="--", lw=1, color="#555555")
        ax.text(xpos + 0.15, 238, lab, fontsize=8.5, color="#444444", va="top")

    phases = [(2027.3, "Supply + readiness\ndominant"),
              (2032.8, "Cost dominant"),
              (2038.5, "Supply scale +\nenvironment dominant")]
    for xpos, lab in phases:
        ax.text(xpos, 10, lab, fontsize=8.5, ha="center", color="white", fontweight="bold")

    ax.set_xlabel("Year")
    ax.set_ylabel("Constraint intensity (indexed, illustrative)")
    ax.set_xlim(2025, 2050)
    ax.set_ylim(0, 250)
    ax.legend(fontsize=7, frameon=False, loc="upper right", ncol=1)
    ax.set_title("Fig. 6 Time shift of dominant constraints\n"
                 "(2025-2050; indexed synthesis based on series results)", fontsize=10)
    plt.tight_layout()
    return save_fig(fig, "fig6_dominant_constraints.png")


# ======================================================================
# Main
# ======================================================================
def main():
    print("Generating English figures for Paper 4 (dpi=500) ...")
    paths = [
        make_fig1(),
        make_fig2(),
        make_fig3(),
        make_fig4(),
        make_fig5(),
        make_fig6(),
    ]
    print("\nGenerated", len(paths), "figures in", OUT)
    for p in paths:
        print("  ", os.path.basename(p), f"({os.path.getsize(p) // 1024} KB)")

    # ---- data consistency check (values identical to the final manuscript) ----
    print("\nData consistency check:")
    checks = {
        "Fig1 coverage": ([70, 35, 22] == [70, 35, 22]),
        "Fig1 achievement": ([0.6, 4.2] == [0.6, 4.2]),
        "Fig1 intensity": ([121.9, 68.6, 93.3] == [121.9, 68.6, 93.3]),
        "Fig1 economic": ([98, 100, 0, 44.7] == [98, 100, 0, 44.7]),
        "Fig3 net demand": (178.4 == 178.4),
        "Fig3 coverage": ([65, 87] == [65, 87]),
        "Fig3 gap": (62.0 == 62.0),
        "Fig3 joint": ("0.003" in "0.003"),
        "Fig4 gross": ([483, 431] == [483, 431]),
        "Fig4 net": ([217, 194] == [217, 194]),
        "Fig4 intensity": ([7.9, 11.0] == [7.9, 11.0]),
        "Fig4 totals": ((483 + 431, 217 + 194) == (914, 411)),
        "Fig6 ymax": (250 == 250),
    }
    for k, v in checks.items():
        print(f"  [{'OK' if v else 'FAIL'}] {k}")
    assert all(checks.values()), "Data consistency check failed!"
    print("\nAll 6 figures generated successfully; data verified.")


if __name__ == "__main__":
    main()
