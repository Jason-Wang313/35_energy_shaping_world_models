# Submission Readiness Decision

Decision: workshop-only / strong-revise.

## Why Not Submit-Ready

- Evidence is a one-dimensional toy reaching task.
- The certificate is hand-specified.
- V2 shows the certificate fails under damping mismatch.
- There is no hardware validation, contact-rich simulation, learned model, or uncertainty-aware admissibility.
- There is no direct comparison to passivity-based control, Hamiltonian neural models, or MPC safety filters.

## Why Not Kill

- The planner-facing certificate interface is clear and useful.
- The toy task cleanly shows that prediction RMSE is not enough for controller-facing world models.
- The v2 stress makes the calibration boundary explicit.
- The narrowed claim is defensible as a mechanism note.

## Required Next Work

- Learn conservative storage/dissipation bounds.
- Add uncertainty-aware or robust admissible sets.
- Test in a richer robot control setting.
- Compare against classical and learned energy-structured baselines.
