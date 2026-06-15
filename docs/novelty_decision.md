# Novelty Decision

Chosen direction: energy certificates as a controller-facing world-model interface.

The strongest novelty claim is architectural. The model does not merely predict a next state or receive an energy regularizer during training. It exposes a storage estimate and admissible action set that a planner can query at decision time.

Boundary against prior work:
- Passivity and energy shaping provide the control language, not the complete learned-model interface.
- Hamiltonian and port-Hamiltonian neural models provide useful structure, but not necessarily an action-level admissibility contract.
- MPC and safety filters can consume the certificate, but they do not replace the need for the world model to expose physical budget information.

V3 evidence supports this novelty boundary through direct hostile baselines and stress regimes.
