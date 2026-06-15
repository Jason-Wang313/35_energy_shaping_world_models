# Experiment Rigor Checklist

- [x] Main full-scale runner is `scripts/run_full_scale_energy_certificate_suite.py`.
- [x] Runner streams seed rows and keeps RAM usage light.
- [x] Families: 10.
- [x] Regimes: 12.
- [x] Methods: 14.
- [x] Seeds per cell: 96.
- [x] Seed rows: 161,280.
- [x] Aggregate rows: 1,680.
- [x] Represented candidate rollouts: 5,109,350,400.
- [x] Baselines include black-box, calibrated black-box, energy-loss-only, Hamiltonian, port-Hamiltonian, passivity filter, MPC safety filter, certificate variants, overconfident certificate, and oracle limit.
- [x] Metrics include RMSE, model cap violations, actual unsafe steps, clean success, return, final error, admitted action fraction, energy margin, and action effort.
- [x] Negative controls include overconfident certificates and combined-shift regimes.
- [x] Figures and LaTeX tables are generated from results artifacts.
- [x] Final manuscript is 25 pages.
- [x] No hardware claim is made.
- [x] No learned-neural training claim is made.

Decision: v3 is submission-hardened for the scoped interface claim.
