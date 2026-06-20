# Submission Readiness Decision

Decision: v3 final submission-hardened for the scoped interface claim.

## Why This Version Is Stronger

- The paper is now 25 pages rather than a short diagnostic note.
- The experiment scale is full-factorial and auditable: 10 families, 12 regimes, 14 methods, 96 seeds, and 5,109,350,400 represented candidate rollouts.
- The paper compares against direct hostile baselines rather than only a toy black-box model.
- The negative boundary is explicit: overconfident certificates fail under mismatch.
- The claim is scoped honestly to a controller-interface study.
- Final PDF, build status, hash, text markers, visual render, and VLA-style link-box rendering are verified.

## Remaining Limits

- No hardware validation.
- No high-fidelity contact-rich simulator.
- No learned-neural storage/certificate head.
- No formal global safety theorem.

These limits are disclosed in the manuscript and should be treated as future work, not hidden defects.
