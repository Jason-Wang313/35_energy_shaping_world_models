# Final Audit

1. Chosen thesis: robot world models should expose controller-facing energy certificates, not only next-state predictions.
2. Final version: v3 final full-scale.
3. Final PDF: `C:/Users/wangz/Downloads/35.pdf`.
4. Final pages: 25.
5. Final SHA256: `013579C68D8D4C834207DAEF12F523DE6D630EA0C79FC6EF4E23E682AF28727D`.
6. Local `main.pdf`: absent after canonical build.
7. Build status: complete.
8. Full-scale suite: 10 families, 12 regimes, 14 methods, 96 seeds, 160 represented steps, 33 candidate actions, 6-step lookahead.
9. Represented candidate rollouts: 5,109,350,400.
10. Seed rows: 161,280.
11. Aggregate rows: 1,680.
12. Main positive result: calibrated/residual/robust/uncertainty-aware certificates reduce unsafe steps relative to prediction-only and overconfident methods.
13. Main negative result: overconfident certificates average 55.55 unsafe steps per seed.
14. RMSE-safety result: one-step RMSE is essentially decoupled from unsafe closed-loop steps in the suite.
15. Evidence boundary: deterministic analytic suite only; no hardware and no learned-neural training claim.
16. Visual audit: final Downloads PDF rendered to PNG contact sheets and checked.
