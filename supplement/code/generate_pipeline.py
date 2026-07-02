#!/usr/bin/env python3
"""Generate the pipeline figure used in the paper."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float
    text: str
    face: str
    edge: str

    @property
    def cx(self) -> float:
        return self.x + self.w / 2.0

    @property
    def cy(self) -> float:
        return self.y + self.h / 2.0


def draw_box(ax: plt.Axes, box: Box, fontsize: int = 14) -> None:
    patch = FancyBboxPatch(
        (box.x, box.y),
        box.w,
        box.h,
        boxstyle="round,pad=0.02,rounding_size=0.16",
        linewidth=2.2,
        edgecolor=box.edge,
        facecolor=box.face,
    )
    ax.add_patch(patch)
    ax.text(
        box.cx,
        box.cy,
        box.text,
        ha="center",
        va="center",
        fontsize=fontsize,
        family="DejaVu Sans",
    )


def draw_arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str = "#4D4D4D",
    lw: float = 2.4,
    mutation_scale: float = 18.0,
) -> None:
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=mutation_scale,
        linewidth=lw,
        color=color,
        shrinkA=0.0,
        shrinkB=0.0,
        connectionstyle="arc3,rad=0.0",
        joinstyle="miter",
        capstyle="round",
    )
    ax.add_patch(arrow)


def build_pipeline_figure(output_pdf: Path, output_png: Path) -> None:
    fig, ax = plt.subplots(figsize=(13.5, 9.5))
    ax.set_xlim(0.0, 14.0)
    ax.set_ylim(0.0, 10.0)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    left_boxes = [
        Box(1.3, 7.25, 4.1, 0.86, "Residual Stream", "#D9E7D9", "#6FA35E"),
        Box(0.95, 5.85, 4.8, 1.0, "Probe decodes count\n(R^2 ~ 1.0)", "#D4DFEF", "#678CC0"),
        Box(1.05, 4.05, 4.6, 1.05, "lm_head misaligned\n(|cos| <= 0.032)", "#F1D2D2", "#B44E4E"),
        Box(1.30, 2.45, 4.1, 0.92, "Wrong digit", "#F6E2C7", "#D89200"),
    ]

    right_boxes = [
        Box(7.70, 6.95, 4.65, 1.26, "9-row repair\n(36K params)", "#D9E7D9", "#6FA35E"),
        Box(7.70, 5.10, 4.65, 1.26, "LoRA Q/V\n(7.7M params)", "#D4DFEF", "#678CC0"),
        Box(7.70, 3.25, 4.65, 1.26, "DPS\n(diagnostic)", "#E7DCEE", "#8A68A2"),
    ]

    for box in left_boxes:
        draw_box(ax, box, fontsize=21 if box is left_boxes[0] else 22 if box is left_boxes[3] else 21)

    for box in right_boxes:
        draw_box(ax, box, fontsize=20)

    ax.text(
        10.0,
        8.75,
        "Interventions",
        ha="center",
        va="center",
        fontsize=28,
        fontweight="bold",
        family="DejaVu Sans",
    )

    # Vertical left-pipeline arrows.
    for top_box, lower_box in zip(left_boxes[:-1], left_boxes[1:]):
        start = (top_box.cx, top_box.y)
        end = (lower_box.cx, lower_box.y + lower_box.h)
        draw_arrow(ax, start, end, lw=3.0, mutation_scale=20)

    # Three rightward connectors: short stems from red box edge, then diagonal fan-out.
    source_box = left_boxes[2]
    source_y = [
        source_box.y + source_box.h * 0.76,
        source_box.y + source_box.h * 0.50,
        source_box.y + source_box.h * 0.24,
    ]
    source_x = source_box.x + source_box.w
    stem_len = 0.70
    stem_color = "#7F7F7F"

    for sy, target_box in zip(source_y, right_boxes):
        sx2 = source_x + stem_len
        ax.plot([source_x, sx2], [sy, sy], color=stem_color, linewidth=3.0, solid_capstyle="round")
        target = (target_box.x, target_box.cy)
        draw_arrow(ax, (sx2, sy), target, color=stem_color, lw=3.0, mutation_scale=21)

    # Small source dots reinforce that each connector starts at the red box edge.
    ax.scatter([source_x] * 3, source_y, s=46, color=stem_color, zorder=5)

    fig.tight_layout(pad=0.4)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_pdf, dpi=300, bbox_inches="tight", pad_inches=0.03)
    fig.savefig(output_png, dpi=300, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    output_dir = repo_root / "paper" / "figures"
    build_pipeline_figure(output_dir / "pipeline.pdf", output_dir / "pipeline.png")
    print(f"Saved {output_dir / 'pipeline.pdf'}")
    print(f"Saved {output_dir / 'pipeline.png'}")


if __name__ == "__main__":
    main()