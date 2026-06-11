# Energy-Certificate World Models for Robot Control

This repository contains a recovered ICLR-style manuscript for paper 35 in the robotics 60-paper batch.

## Artifacts

- `main.tex` and `main.pdf`: paper source and compiled PDF.
- `docs/related_work_matrix.csv`: 1007-row automated literature landscape.
- `docs/energy_certificate_results.csv`: deterministic toy control results.
- `scripts/energy_certificate_sim.py`: standalone simulation used in the paper.
- `docs/final_audit.md`: recovery/build audit.

## Main local result

The energy-certificate interface has 0 model energy-cap violations, 0 unsafe closed-loop steps, and clean success rate 1.00 over 60 deterministic starts.
