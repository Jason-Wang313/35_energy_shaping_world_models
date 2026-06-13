# Energy-Certificate World Models for Robot Control

This repository contains a recovered ICLR-style manuscript for paper 35 in the robotics 60-paper batch.

## Artifacts

- `main.tex`: paper source.
- `C:/Users/wangz/Downloads/35.pdf`: canonical compiled PDF.
- `docs/related_work_matrix.csv`: 1007-row automated literature landscape.
- `docs/energy_certificate_results.csv`: deterministic toy control results.
- `docs/energy_damping_mismatch_stress.csv`: v2 damping-calibration stress.
- `scripts/energy_certificate_sim.py`: standalone simulation used in the paper.
- `scripts/build_pdf.ps1`: builds the PDF, copies it to Downloads, and removes local `main.pdf`.
- `docs/final_audit.md`: recovery/build audit.

## Main local result

The energy-certificate interface has 0 model energy-cap violations, 0 unsafe closed-loop steps, and clean success rate 1.00 over 60 deterministic starts.

## V2 boundary

When true damping is reduced to 0.02 while the certificate model remains nominal, model cap violations remain 0 but real unsafe steps rise to 125 and clean success falls to 0.23.
