# Claims

1. Robot world models used by controllers need an action-level physical contract, not only next-state predictions.
2. The proposed contract is an energy-certificate interface: next state, storage estimate, and admissible action set.
3. Energy as a model interface is different from energy as a training loss because a planner can query the former at decision time.
4. Hamiltonian and port-Hamiltonian structure are useful but not identical to a controller-facing admissibility query.
5. In the v3 deterministic suite, one-step RMSE is essentially decoupled from unsafe closed-loop steps.
6. Calibrated, residual, robust, and uncertainty-aware certificates reduce unsafe steps relative to prediction-only and overconfident interfaces.
7. Overconfident certificates are a central negative result: a certificate can fail badly if damping, payload, contact, latency, or cap calibration is optimistic.
8. The result is not a hardware guarantee, not a formal passivity theorem, and not a learned-neural benchmark.
