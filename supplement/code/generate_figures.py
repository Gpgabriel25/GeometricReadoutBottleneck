#!/usr/bin/env python3
"""
Generate publication-quality figures for the Snapshot Isolation Counting paper.

Reads from the matched-setting results directory and produces PDF/PNG figures.
"""
import argparse
import json
import os
from pathlib import Path

import numpy as np

os.environ["MPLBACKEND"] = "Agg"
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def load_json(path):
    with open(path) as f:
        return json.load(f)


def fig1_is_vs_gen_error(results_dir: Path, output_dir: Path):
    """Figure 1: IS vs generation error scatter + regression."""
    is_data = load_json(results_dir / "is_scores.json")
    gen_answers = load_json(results_dir / "gen_answers.json")

    prompt_is_std = []
    prompt_gen_error = []
    prompt_difficulty = []
    for pid, is_item in is_data.items():
        gen_item = gen_answers.get(pid)
        if gen_item is None:
            continue
        is_val = is_item.get("is_std", is_item.get("IS_std", None))
        if is_val is None:
            continue
        gen_err = abs(gen_item.get("gen_answer", 0) - gen_item.get("true_count", 0))
        prompt_is_std.append(float(is_val))
        prompt_gen_error.append(float(gen_err))
        prompt_difficulty.append(gen_item.get("difficulty", "unknown"))

    is_arr = np.array(prompt_is_std)
    err_arr = np.array(prompt_gen_error)
    diff_arr = np.array(prompt_difficulty)

    fig, ax = plt.subplots(1, 1, figsize=(5, 4))
    colors = {"easy": "#2ecc71", "medium": "#f39c12", "hard": "#e74c3c"}
    for diff in ["easy", "medium", "hard"]:
        mask = diff_arr == diff
        if mask.any():
            ax.scatter(is_arr[mask], err_arr[mask], alpha=0.15, s=8,
                       color=colors.get(diff, "gray"), label=diff, rasterized=True)

    # Regression line
    if len(is_arr) > 2:
        coeffs = np.polyfit(is_arr, err_arr, 1)
        x_line = np.linspace(is_arr.min(), is_arr.max(), 100)
        ax.plot(x_line, np.polyval(coeffs, x_line), "k-", linewidth=1.5,
                label="r=%.3f" % np.corrcoef(is_arr, err_arr)[0, 1])

    ax.set_xlabel("IS(std)", fontsize=11)
    ax.set_ylabel("Generation Error (|predicted - true|)", fontsize=11)
    ax.set_title("IS vs Generation Error (Qwen3-8B, matched setting)", fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(output_dir / "fig1_is_vs_gen_error.pdf", dpi=300)
    fig.savefig(output_dir / "fig1_is_vs_gen_error.png", dpi=150)
    plt.close(fig)
    print("  Figure 1: IS vs generation error scatter saved")


def fig2_is_depth_profile(results_dir: Path, output_dir: Path):
    """Figure 2: IS depth profile for correct vs incorrect examples."""
    dp_correct = np.load(results_dir / "is_depth_profile_correct.npy")
    dp_incorrect = np.load(results_dir / "is_depth_profile_incorrect.npy")
    n_layers = len(dp_correct)
    layers = np.arange(n_layers)
    depth_pct = layers / (n_layers - 1) * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), gridspec_kw={"width_ratios": [2, 1]})

    ax1.plot(depth_pct, dp_correct, "o-", markersize=3, linewidth=1.2, color="#2ecc71", label="Correct")
    ax1.plot(depth_pct, dp_incorrect, "s-", markersize=3, linewidth=1.2, color="#e74c3c", label="Incorrect")
    ax1.set_xlabel("Layer Depth (%)", fontsize=11)
    ax1.set_ylabel("Mean IS(std)", fontsize=11)
    ax1.set_title("IS Depth Profile: Correct vs Incorrect", fontsize=10)
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.2)

    diff = dp_incorrect - dp_correct
    ax2.bar(depth_pct, diff, width=2.5, color=np.where(diff > 0, "#e74c3c", "#2ecc71"), alpha=0.7)
    ax2.axhline(0, color="black", linewidth=0.5)
    ax2.set_xlabel("Layer Depth (%)", fontsize=11)
    ax2.set_ylabel("IS Difference (Incorrect - Correct)", fontsize=11)
    ax2.set_title("IS Gap by Layer", fontsize=10)
    ax2.grid(alpha=0.2)

    fig.tight_layout()
    fig.savefig(output_dir / "fig2_is_depth_profile.pdf", dpi=300)
    fig.savefig(output_dir / "fig2_is_depth_profile.png", dpi=150)
    plt.close(fig)
    print("  Figure 2: IS depth profile saved")


def fig3_probe_r2_and_gap(results_dir: Path, output_dir: Path, gen_accuracy: float):
    """Figure 3: Probe R² by layer + generation accuracy gap."""
    probe = load_json(results_dir / "probe_results.json")
    layers_data = probe["layers"]
    n_layers = len(layers_data)
    layer_ids = list(range(n_layers))
    r2_vals = [layers_data[str(i)]["r2"] for i in layer_ids]
    easy_r2 = [layers_data[str(i)]["easy_r2"] for i in layer_ids]
    depth_pct = [i / (n_layers - 1) * 100 for i in layer_ids]

    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    ax.plot(depth_pct, r2_vals, "o-", markersize=3, linewidth=1.2, color="#3498db", label="Probe R² (all)")
    ax.plot(depth_pct, easy_r2, "s-", markersize=3, linewidth=1.2, color="#9b59b6", label="Probe R² (easy)")
    ax.axhline(gen_accuracy, color="#e74c3c", linestyle="--", linewidth=1.5,
               label="Next-token digit accuracy (%.1f%%)" % (gen_accuracy * 100))
    ax.fill_between(depth_pct, gen_accuracy, r2_vals, alpha=0.1, color="#e74c3c")
    ax.set_xlabel("Layer Depth (%)", fontsize=11)
    ax.set_ylabel("Probe R² / Accuracy", fontsize=11)
    ax.set_title("Representation-Output Gap (Qwen3-8B)", fontsize=10)
    ax.set_ylim(0.3, 1.02)
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(output_dir / "fig3_probe_r2_gap.pdf", dpi=300)
    fig.savefig(output_dir / "fig3_probe_r2_gap.png", dpi=150)
    plt.close(fig)
    print("  Figure 3: Probe R² and representation-output gap saved")


def fig4_baseline_comparison(results_dir: Path, output_dir: Path):
    """Figure 4: Predictor comparison bar chart (IS vs baselines)."""
    gen = load_json(results_dir / "phase0gen_results.json")
    b = load_json(results_dir / "phase0b_results.json")

    predictors = ["IS(std)", "true_count", "n_tokens"]
    gen_r_vals = [
        gen.get("IS_std_gen_error_r", 0),
        gen.get("true_count_gen_error_r", 0),
        gen.get("n_tokens_gen_error_r", 0),
    ]
    gen_auroc_vals = [
        gen.get("IS_std_gen_error_AUROC", b.get("auroc_std", 0)),
        gen.get("true_count_gen_error_AUROC", b.get("true_count_auroc", 0)),
        gen.get("n_tokens_gen_error_AUROC", b.get("n_tokens_auroc", 0)),
    ]

    x = np.arange(len(predictors))
    width = 0.35
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

    bars1 = ax1.bar(x, gen_r_vals, width, color=["#3498db", "#2ecc71", "#f39c12"])
    ax1.set_ylabel("Pearson r with Generation Error", fontsize=10)
    ax1.set_title("Predictor → Gen Error Correlation", fontsize=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels(predictors, fontsize=9)
    ax1.set_ylim(0, 1.0)
    for bar, val in zip(bars1, gen_r_vals):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                 "%.3f" % val, ha="center", fontsize=8)
    ax1.grid(axis="y", alpha=0.2)

    bars2 = ax2.bar(x, gen_auroc_vals, width, color=["#3498db", "#2ecc71", "#f39c12"])
    ax2.set_ylabel("AUROC (Gen Failure Prediction)", fontsize=10)
    ax2.set_title("Failure Prediction AUROC", fontsize=10)
    ax2.set_xticks(x)
    ax2.set_xticklabels(predictors, fontsize=9)
    ax2.set_ylim(0.4, 1.0)
    ax2.axhline(0.5, color="gray", linestyle=":", linewidth=0.8, label="chance")
    for bar, val in zip(bars2, gen_auroc_vals):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                 "%.3f" % val, ha="center", fontsize=8)
    ax2.grid(axis="y", alpha=0.2)

    fig.tight_layout()
    fig.savefig(output_dir / "fig4_baseline_comparison.pdf", dpi=300)
    fig.savefig(output_dir / "fig4_baseline_comparison.png", dpi=150)
    plt.close(fig)
    print("  Figure 4: Baseline comparison saved")


def fig5_phase3b_conditions(phase3b_path: Path, output_dir: Path):
    """Figure 5: Phase 3B per-condition count accuracy (frozen baseline)."""
    d = load_json(phase3b_path)
    per_cond_test = d.get("per_condition_test", {})
    if not per_cond_test:
        print("  Figure 5: SKIPPED (no per-condition test data)")
        return

    conditions = list(per_cond_test.keys())
    accs = [per_cond_test[c]["count_accuracy"] for c in conditions]
    losses = [per_cond_test[c]["count_loss"] for c in conditions]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
    x = np.arange(len(conditions))
    labels = [c.replace("_", "\n") for c in conditions]

    bars1 = ax1.bar(x, [a * 100 for a in accs], color=["#3498db", "#95a5a6", "#f39c12", "#e74c3c"])
    ax1.set_ylabel("Test Count Accuracy (%)", fontsize=10)
    ax1.set_title("Phase 3B Frozen Baseline: No Training Effect", fontsize=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=8)
    for bar, val in zip(bars1, accs):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 "%.1f%%" % (val * 100), ha="center", fontsize=8)
    ax1.set_ylim(0, 100)
    ax1.grid(axis="y", alpha=0.2)

    bars2 = ax2.bar(x, losses, color=["#3498db", "#95a5a6", "#f39c12", "#e74c3c"])
    ax2.set_ylabel("Test Count Loss (CE)", fontsize=10)
    ax2.set_title("Count Loss by Condition", fontsize=10)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=8)
    for bar, val in zip(bars2, losses):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                 "%.3f" % val, ha="center", fontsize=8)
    ax2.grid(axis="y", alpha=0.2)

    fig.tight_layout()
    fig.savefig(output_dir / "fig5_phase3b_conditions.pdf", dpi=300)
    fig.savefig(output_dir / "fig5_phase3b_conditions.png", dpi=150)
    plt.close(fig)
    print("  Figure 5: Phase 3B condition comparison saved")


def main():
    parser = argparse.ArgumentParser(description="Generate paper figures")
    parser.add_argument("--results_dir", default="results/qwen3-8b-instruct-matched")
    parser.add_argument("--phase3b_path",
                        default="results/phase3b_frozen_v3/phase3b_mvp_summary.json")
    parser.add_argument("--output_dir", default="figures")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating figures from %s" % results_dir)

    gen_data = load_json(results_dir / "phase0gen_results.json")
    gen_accuracy = gen_data.get("accuracy", 0.3875)

    fig1_is_vs_gen_error(results_dir, output_dir)
    fig2_is_depth_profile(results_dir, output_dir)
    fig3_probe_r2_and_gap(results_dir, output_dir, gen_accuracy)
    fig4_baseline_comparison(results_dir, output_dir)

    phase3b_path = Path(args.phase3b_path)
    if phase3b_path.exists():
        fig5_phase3b_conditions(phase3b_path, output_dir)
    else:
        print("  Skipping Figure 5 (no Phase 3B results at %s)" % phase3b_path)

    print("All figures saved to %s" % output_dir)


if __name__ == "__main__":
    main()
