# Novelty Decision

Chosen direction: a robot world model whose latent prediction updates are constrained by an energy-shaping budget, so that the model can be used for control without silently inventing or absorbing energy.

Why this is stronger than the seed:
- It changes the central mechanism from 'world model plus regularizer' to 'certificate-aware predictive dynamics.'
- It targets the failure mode that matters most in embodied control: physically implausible rollouts that look good in open-loop but destabilize closed-loop execution.
- It is a robotics contribution, not just a representation-learning tweak.

Rejected weaker variants:
- Bigger model or more data.
- Generic uncertainty estimation.
- Standalone benchmark work.
- RL framing.

V2 boundary: proceed only as workshop-only / strong-revise. The damping-mismatch stress shows that the interface can be dangerously optimistic when dissipation is miscalibrated.
