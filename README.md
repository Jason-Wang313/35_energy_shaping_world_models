# Energy-Certificate World Models for Robot Control

Status: v3 final full-scale submission-hardened artifact.

## Final PDF

- Canonical PDF: `C:/Users/wangz/Downloads/35.pdf`
- Pages: 25
- Size: 377,741 bytes
- SHA256: `013579C68D8D4C834207DAEF12F523DE6D630EA0C79FC6EF4E23E682AF28727D`
- Local `main.pdf`: absent after canonical build
- Build status: complete
- Visual render: checked from final Downloads PDF

## V3 Scale

- 10 plant families
- 12 stress regimes
- 14 model/controller interfaces
- 96 seeds per cell
- 160 represented control steps
- 33 candidate actions
- 6-step lookahead
- 5,109,350,400 represented candidate rollouts
- 161,280 seed-level rows
- 1,680 aggregate rows

## Main Finding

The v3 deterministic suite supports a scoped interface claim: robot world models
used inside controllers should expose controller-facing energy admissibility, not
only next-state predictions. One-step RMSE is essentially decoupled from unsafe
closed-loop steps in the suite, while calibrated, residual, robust, and
uncertainty-aware certificate interfaces reduce unsafe steps relative to
prediction-only, energy-loss-only, and overconfident interfaces.

## Key Artifacts

- `main.tex`: v3 final manuscript source.
- `scripts/run_full_scale_energy_certificate_suite.py`: RAM-light full-scale suite.
- `results/full_scale/seed_metrics.csv`: seed-level results.
- `results/full_scale/aggregate_metrics.csv`: aggregate results.
- `results/full_scale/experiment_summary.json`: summary numbers.
- `results/full_scale/validation.json`: final PDF and build validation.
- `figures/full_scale/*.pdf`: generated figures.
- `scripts/build_pdf.ps1`: canonical build/export script.
