# Claims

1. Learned world models for robots often optimize predictive fit without explicitly controlling the energy behavior of rollouts.
2. Energy-shaping / passivity ideas provide a more actionable structure for robot dynamics than generic latent regularization.
3. If a world model is used for planning or control, its error should be budgeted by a certificate that speaks the language of the controller.
4. A simple toy benchmark should be enough to show that unconstrained rollouts can violate qualitative energy behavior even when prediction loss is competitive.
5. The strongest novelty claim is architectural: the energy certificate becomes part of the model interface, not just an auxiliary loss.
6. V2 narrows the claim to calibrated certificates: when true damping falls to 0.02 while the certificate model remains nominal, model cap violations remain 0 but real unsafe steps rise to 125 and clean success falls to 0.23.
