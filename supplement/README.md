# Supplemental Materials: The Right Answer, the Wrong Direction

This supplement contains code, results, and figures for reproducing the experiments in *"The Right Answer, the Wrong Direction: Why Transformers Fail at Counting and How to Fix It"* (NeurIPS 2026).

## Structure

```
supplement/
├── README.md              # This file
├── main.tex / main.pdf    # Paper source and compiled PDF
├── code/                  # Reproduction scripts (ALL PyTorch)
│   ├── data_generation.py        # Synthetic benchmark generation
│   ├── run_phase112_fullvocab_all_tasks.py  # Fullvocab 9-row repair across 4 tasks (§4)
│   ├── run_phase113_hidden_diversity.py     # Within-count hidden-state variance analysis
│   ├── run_phase114_improved_repair.py      # Improved 9-row repair with Adam optimization
│   ├── run_phase116_norm_rescaling.py       # Norm rescaling ablation
│   ├── run_phase117_lora_fullvocab.py       # LoRA Q/V fullvocab next-token (§5)
│   ├── run_phase118_lora_generation.py      # LoRA Q/V generation mode (§5)
│   ├── run_phase119_lora_mechanism.py       # Pre/post-LoRA probe alignment (§5)
│   ├── run_phase119b_final_layer.py         # Final-layer probe alignment
│   ├── run_phase119c_logitlens.py           # Logit-lens rank pre/post LoRA (§5)
│   ├── run_phase120_multitask_logitlens.py  # Cross-task logit-lens generalisation
│   ├── run_phase121_extra_seeds.py          # 2 extra LoRA seeds (→5-seed result)
│   ├── run_phase122_cot.py                  # CoT baseline (Limitations)
│   ├── run_phase124_lora_variants.py        # LoRA locus ablation (§5)
│   ├── run_phase125_m4_m7.py                # 60% ceiling + multi-seed CoT
│   ├── generate_figures.py                  # Paper figure generation
│   └── generate_pipeline.py                 # Pipeline diagram
├── results/               # JSON result files for each experiment
│   ├── results_phase4_logit_lens.json
│   ├── results_phase112_fullvocab_all_tasks.json
│   ├── results_phase117_lora_fullvocab.json
│   ├── results_phase118_lora_generation.json
│   ├── results_phase119_lora_mechanism.json
│   ├── results_phase119c_logitlens.json
│   ├── results_phase122_cot.json
│   ├── results_phase124_lora_variants.json
│   ├── results_phase125_m4_m7.json
│   └── ... (38 total)
└── figures/               # All paper figures (PDF + PNG)
```

## Reproduction Guide

**Framework note:** All experiments in this paper were run in PyTorch on TPU VM instances (CPU mode). No JAX or TPU-accelerated code is required. The scripts use HuggingFace Transformers and PEFT (LoRA). Models load from HuggingFace Hub with `trust_remote_code=True` for Qwen3.

### Requirements
- Python 3.11+
- PyTorch 2.x
- HuggingFace Transformers, PEFT (LoRA)
- scikit-learn, matplotlib, numpy, scipy
- Qwen3-8B model weights (downloaded automatically from HuggingFace)

### Quick Start

1. **Generate the benchmark data**:
```bash
python code/data_generation.py
```

2. **Run the 9-row repair** (Table 1, core diagnostic in §4):
```bash
python code/run_phase112_fullvocab_all_tasks.py
python code/run_phase113_hidden_diversity.py
```

3. **Run the LoRA Q/V experiments** (Table 1, §5):
```bash
python code/run_phase117_lora_fullvocab.py    # Fullvocab next-token
python code/run_phase118_lora_generation.py   # Generation mode
python code/run_phase119_lora_mechanism.py    # Mechanistic probe analysis
python code/run_phase119c_logitlens.py        # Logit-lens rank
python code/run_phase121_extra_seeds.py       # 5-seed LoRA
```

4. **Run ablations and baselines**:
```bash
python code/run_phase124_lora_variants.py     # LoRA locus ablation
python code/run_phase122_cot.py               # CoT baseline
python code/run_phase125_m4_m7.py             # 60% ceiling + multi-seed CoT
python code/run_phase116_norm_rescaling.py    # Norm rescaling
```

5. **Regenerate figures**:
```bash
python code/generate_figures.py
python code/generate_pipeline.py
```

### Expected Results

| Experiment | Key Metric | Expected Range |
|-----------|------------|----------------|
| Probe R² | Layer 2+ | >0.99 |
| 9-row repair (entity) | Constrained acc | 60.7% ± 3.1% |
| 9-row repair (other tasks) | Constrained acc | 98.0-100% |
| LoRA Q/V generation | 5-seed | 83.1% ± 7.2% |
| CoT baseline | Few-shot | 20.2% ± 1.9% |
| |cos| probe-lm_head | ≤0.032 (all models) |

### Model & Data

- **Qwen3-8B**: `Qwen/Qwen3-8B` from HuggingFace (Apache 2.0)
- **Mistral-7B**: `mistralai/Mistral-7B-v0.1` from HuggingFace
- **Pythia-410M**: `EleutherAI/pythia-410m` from HuggingFace (Apache 2.0)
- **Benchmark**: 4,320 prompts, full-factorial, generated deterministically from scripts

### Protocol Legend

The paper uses three standard evaluation protocols:
- **Digit-restricted next-token**: argmax over digit tokens 1-9 only
- **Full-vocab next-token**: argmax over all 152K tokens
- **Generation**: greedy autoregressive decode, first digit extracted

All primary effect-size claims are tied to the protocol listed in Table 1 (unified evaluation).

## License
Code: MIT License. Paper text and figures: CC BY 4.0.
