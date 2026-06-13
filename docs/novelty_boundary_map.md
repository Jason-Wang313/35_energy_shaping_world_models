# Novelty Boundary Map

## Field box

Robot dynamics learning with world-model style prediction and control.

## Candidate thesis boundary

- Existing world models usually optimize prediction or planning usefulness.
- Existing energy shaping / passivity methods usually assume a hand-specified physical model or a controller-centric view.
- The gap is a learned world model whose *prediction error* is explicitly budgeted by an energy-shaping / passivity certificate.

## 20 hidden assumptions to break

- Assumption 1: Model error can be treated as harmless if rollout loss is low.
- Assumption 2: Prediction and control objectives can be decoupled.
- Assumption 3: A learned dynamics model need not preserve physical energy structure.
- Assumption 4: Stability is mostly a controller-side property.
- Assumption 5: State estimation errors are small enough to ignore.
- Assumption 6: The environment is fully known up to noise.
- Assumption 7: Reward/value objectives capture physical feasibility.
- Assumption 8: Long-horizon rollouts remain credible without structural constraints.
- Assumption 9: Passivity is too conservative for learning-based robotics.
- Assumption 10: Energy shaping only matters for classical model-based control.
- Assumption 11: A generic latent world model can safely stand in for mechanics.
- Assumption 12: Robot dynamics can be learned from arbitrary representation choices.
- Assumption 13: Any learned model error is equivalent for planning purposes.
- Assumption 14: Nonlinear underactuated systems need not be treated specially.
- Assumption 15: A single loss can balance accuracy and stability automatically.
- Assumption 16: Closed-loop rollout error is the only important metric.
- Assumption 17: Physical priors only help with sample efficiency, not safety.
- Assumption 18: The model need not expose a certificate that the controller can use.
- Assumption 19: Prediction horizons can be extended simply by more data.
- Assumption 20: Generalization across contact/regime changes is mostly a scale problem.

## V2 boundary

Inside the claim: controller-facing energy admissibility under calibrated or conservative storage/dissipation models.

Outside the claim: hardware safety guarantees when the true plant dissipates less energy than the certificate assumes.
