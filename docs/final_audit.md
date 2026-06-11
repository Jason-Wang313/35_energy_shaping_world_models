# Final Audit

Status: recovered manually after child attempt 2 exited before manuscript generation.

## Literature inputs

- `docs/related_work_matrix.csv`: retained from the child literature sweep.
- `docs/literature_map.md`: reports 1007 raw papers, 300 serious-skim candidates, and 250 deep-read candidates.
- Hostile clusters: passivity and energy-shaping control, Hamiltonian/port-Hamiltonian neural dynamics, and embodied world models for robot planning/manipulation.

## Recovered contribution

The paper frames energy certificates as a controller-facing world-model interface rather than an auxiliary training regularizer.

## Reproducible local experiment

- Script: `scripts/energy_certificate_sim.py`
- Results: `docs\energy_certificate_results.csv`
- Episodes: 60
- Horizon per episode: 120
- Energy cap: 0.9

## Result summary

- black_box: RMSE=0.0145, model_cap_violations=1433, unsafe_steps=2545, clean_success=0.00, final_error=0.017
- hamiltonian: RMSE=0.0058, model_cap_violations=406, unsafe_steps=1231, clean_success=0.00, final_error=0.497
- certificate: RMSE=0.0009, model_cap_violations=0, unsafe_steps=0, clean_success=1.00, final_error=0.003

PDF was compiled with pdflatex during recovery and copied to Downloads/Desktop as `35.pdf`.
