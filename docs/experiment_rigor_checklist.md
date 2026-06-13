# Experiment Rigor Checklist

- [x] Main simulator is `scripts/energy_certificate_sim.py`.
- [x] Main run uses 60 deterministic starts and 120 control steps each.
- [x] Baselines include black-box, Hamiltonian-style, and energy-certificate interfaces.
- [x] Main metrics include RMSE, model cap violations, unsafe steps, clean success, return, and final error.
- [x] V2 stress attacks damping calibration.
- [x] Negative boundary is explicit: at true damping 0.02, model cap violations remain 0 but real unsafe steps rise to 125.
- [ ] No hardware validation.
- [ ] No learned neural model trained from data.
- [ ] No contact-rich or multi-body simulator.
- [ ] No uncertainty-aware certificate.

Decision: mechanism evidence only; terminal state is workshop-only / strong-revise.
