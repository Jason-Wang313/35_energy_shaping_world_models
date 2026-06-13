# Hostile Reviewer Response

## Likely Rejection

This is passivity/energy shaping repackaged as a world-model interface, and the safety result depends on a hand-specified certificate that knows the plant damping.

## Honest Response

We agree that passivity and energy shaping are the core prior art. The contribution is narrower: a learned world model used by a planner should expose energy admissibility as an interface, not merely optimize prediction loss or an auxiliary physics prior.

The v2 stress quantifies the limitation. When true damping is reduced to 0.02 but the certificate model remains nominal, model cap violations stay at 0 while real unsafe steps rise to 125 and clean success falls to 0.23. The paper should claim calibrated energy-admissibility interfaces, not hardware safety.

## Required Upgrade For Main-Track Submission

- Learn or estimate conservative storage and damping bounds from data.
- Add uncertainty-aware admissibility sets.
- Test in a contact-rich or multi-body robot simulator.
- Compare against passivity-based control, Hamiltonian neural models, and MPC safety filters.
