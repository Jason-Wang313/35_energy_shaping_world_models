# Hostile Reviewer Response

The strongest response is to keep the claim narrow and evidence-rich.

1. The paper does not claim to invent passivity or Hamiltonian dynamics. It claims that a learned world model used by a controller should expose the energy admissibility query at decision time.
2. The v3 suite includes hostile baselines: Hamiltonian predictor, port-Hamiltonian predictor, passivity filter, MPC safety filter, fixed certificate, robust certificate, uncertainty-margin certificate, overconfident certificate, and oracle limit.
3. Prediction error is tested directly and is not a reliable proxy for unsafe closed-loop behavior in the suite.
4. The overconfident certificate is a negative control showing that certificates require conservative calibration.
5. The deterministic suite is justified as an interface study; hardware and learned-neural validation are future work.

The reviewer should judge the paper as a controller-interface contribution, not as a hardware safety paper.
