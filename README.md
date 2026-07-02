# Geometric Readout Bottleneck

> Code and data for the paper **"The Right Answer, the Wrong Direction: Why Transformers Fail at Counting and How to Fix It"**

Transformers fail at counting not because they can't represent counts, but because the output pathway can't route the answer. Linear probes recover counts at $R^2>0.99$ from every layer, yet the count-encoding direction is nearly orthogonal to the output head's digit rows ($|\cos| \leq 0.032$). We trace this to a geometric readout bottleneck, localize it with a 9-row output-head repair, and resolve it with LoRA Q/V attention routing.

- Paper PDF (full, 26 pages): [`paper/main.pdf`](paper/main.pdf)
- arXiv: [arxiv.org/abs/2605.03258](https://arxiv.org/abs/2605.03258)
- NeurIPS 2026 submission (9 pages, anonymized): [`paper/main_neurips.pdf`](paper/main_neurips.pdf)
- arXiv metadata (title, abstract, class codes): [`paper/arxiv_metadata.md`](paper/arxiv_metadata.md)
- Supplement guide: [`supplement/README.md`](supplement/README.md)

## What's in the paper, and where it lives in this repo

| Paper element | Producing script(s) | Data file |
|---|---|---|
| **Fig. 1** — Pipeline / bottleneck schematic | `supplement/code/generate_pipeline.py` | `supplement/figures/pipeline.pdf` (via `paper/figures/`) |
| **Fig. 2** — Probe $R^2$ vs. layer depth | `supplement/code/generate_figures.py` | probe diagnostics in phase 113/119 outputs |
| **Fig. 3** — Probe–readout gap | `supplement/code/generate_figures.py` | `supplement/figures/fig3_probe_r2_gap.pdf` |
| **Fig. 4** — Logit-lens rank profile | `supplement/code/run_phase119c_logitlens.py` → `generate_figures.py` | `supplement/results/results_phase119c_logitlens.json` |
| **Tab. 1** — Unified evaluation (headline methods) | `run_phase112_*`, `run_phase118_*`, `run_phase122_*` | `results_phase112_fullvocab_all_tasks.json`, `results_phase118_lora_generation.json`, `results_phase122_cot.json` |
| **Tab. 2** — Probe $R^2$ by layer | probe scripts in supplement | embedded in phase 113/119 mechanism outputs |
| **Tab. 3** — 9-row repair / LoRA summary | `run_phase112_fullvocab_all_tasks.py`, `run_phase118_lora_generation.py` | `results_phase112_fullvocab_all_tasks.json`, `results_phase118_lora_generation.json` |
| **Tab. 4** — Logit-lens digit rank | `run_phase119c_logitlens.py` | `results_phase119c_logitlens.json` |
| **Tab. 5** — LoRA locus ablation | `run_phase124_lora_variants.py` | `results_phase124_lora_variants.json` |
| **App.** — Hidden diversity / norm rescaling | `run_phase113_hidden_diversity.py`, `run_phase116_norm_rescaling.py` | `results_phase113_hidden_diversity.json`, `results_phase116_norm_rescaling.json` |
| **App.** — Multi-seed LoRA + CoT ceiling | `run_phase121_extra_seeds.py`, `run_phase125_m4_m7.py` | `results_phase121_extra_seeds.json`, `results_phase125_m4_m7.json` |

All script paths above are under `supplement/code/`; all JSON paths under `supplement/results/`.

## Reproduce the headline numbers

```bash
cd supplement/code
python data_generation.py
python run_phase112_fullvocab_all_tasks.py    # 9-row repair (Tab. 1)
python run_phase118_lora_generation.py        # LoRA Q/V generation (Tab. 1)
python run_phase122_cot.py                    # CoT baseline (Tab. 1)
python run_phase119c_logitlens.py             # Logit-lens ranks (Fig. 4 / Tab. 4)
python run_phase124_lora_variants.py          # LoRA locus ablation (Tab. 5)
```

Archived JSON for every primary row is already in `supplement/results/`. See [`supplement/README.md`](supplement/README.md) for the full phase map and expected ranges.

### Key numbers

| Experiment | Metric | Result |
|-----------|--------|--------|
| Probe $R^2$ | Layer 2+ | >0.99 |
| 9-row repair | Constrained | 60.7–100.0% |
| LoRA Q/V generation | 5 seeds | 83.1% ± 7.2% |
| CoT baseline | Few-shot | 20.2% ± 1.9% |

## Repository layout

```
paper/                  LaTeX source, PDFs, figures, checklist
supplement/
  code/                 16 experiment scripts (PyTorch)
  results/              14 primary result JSONs
  figures/              Paper figures (PDF + PNG)
README.md
LICENSE
```

## Citation

```bibtex
@misc{garcia2026rightanswerwrongdirection,
  title         = {The Right Answer, the Wrong Direction: Why Transformers Fail at Counting and How to Fix It},
  author        = {Garcia, Gabriel},
  year          = {2026},
  eprint        = {2605.03258},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CL},
  url           = {https://arxiv.org/abs/2605.03258},
}
```

## License

- Code: MIT (`LICENSE`).
- Paper PDF, LaTeX source, and figures: CC BY 4.0 (`LICENSE`).

## Contact

Gabriel Garcia — gpgabriel25@gmail.com — Independent researcher.
