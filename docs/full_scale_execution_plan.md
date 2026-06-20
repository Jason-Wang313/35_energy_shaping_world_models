# Paper 35 Full-Scale Execution Plan

## Working Rule

Work only on Paper 35 until it reaches a final, verified state. Do not copy any
PDF to `C:/Users/wangz/Downloads/35.pdf` until the manuscript is at least 25
pages and the local build, log scan, text scan, and visual render check all pass.
Keep the work RAM-light by streaming seed-level rows and storing only aggregates,
small traces, compact tables, and vector figures.

## Current State Before V3

- Repository: `C:/Users/wangz/robotics_60_paper_batch/35_energy_shaping_world_models`.
- Worktree state at start: clean.
- Canonical Downloads PDF at start: absent, despite stale v2 docs claiming it
  exists.
- Current manuscript: 5 pages according to `main.log`.
- Current evidence: one one-dimensional deterministic reaching task with 60
  starts, 120 steps, and three methods.
- Current readiness label before v3: not ready for the final batch standard.
- Core weakness to fix: the v2 result demonstrates the interface but does not
  test calibrated robustness, uncertainty-aware admissibility, passivity filters,
  MPC-style safety filters, multi-family plant variation, or the relationship
  between prediction error and closed-loop energy violations.

## V3 Target

Convert the paper from a small mechanism note into a submission-ready full-scale
simulation study of controller-facing energy-certificate world models. The final
paper should be a 25+ page ICLR-style manuscript with a larger experimental
section, extensive appendices, direct hostile-prior comparisons, reproducibility
artifacts, and a conservative claim boundary.

The central claim will remain precise:

> A robot world model used inside a controller should expose an energy/storage
> admissibility certificate at decision time. Prediction error, Hamiltonian
> structure, or an auxiliary energy loss alone is not enough to tell the planner
> which actions remain physically admissible under the controller's local budget.

The strengthened evidence will add:

- Positive findings under calibrated and uncertainty-aware certificates.
- Negative findings for overconfident certificates under damping, payload, and
  contact-like mismatch.
- Comparisons to prediction-only, Hamiltonian, energy-regularized, passivity
  filter, MPC-style safety filter, robust certificate, and oracle-limit baselines.
- Per-family and per-regime analyses showing where the interface helps, where it
  is conservative, and where it fails.
- RMSE-versus-safety analysis showing why predictive fit is an insufficient
  submission metric for robot world models.

## Full-Scale Experiment Design

Run a new deterministic but broad simulator in
`scripts/run_full_scale_energy_certificate_suite.py`. It will be analytic and
streaming, not neural-training-heavy, because the goal is to isolate the model
interface at scale while keeping RAM light.

### Plant Families

Use 10 families that are all simple enough to simulate exactly but different
enough to attack the interface:

1. nominal spring-damper reaching,
2. low-damping payload shift,
3. high-damping viscous environment,
4. cubic-drag dissipative plant,
5. actuator saturation and delayed effort,
6. soft-wall contact penalty,
7. unilateral stop with rebound loss,
8. slope-biased potential field,
9. variable stiffness compliance,
10. coupled two-mode reduced manipulator.

Each family will expose true dynamics, a nominal model, a calibrated storage
function, a deliberately optimistic storage function, and an oracle storage
function used only as a limit.

### Stress Regimes

Use 12 regimes:

1. nominal calibration,
2. mild damping loss,
3. severe damping loss,
4. payload mass increase,
5. payload mass decrease,
6. actuator saturation,
7. action latency,
8. sensor noise,
9. energy-cap tightening,
10. energy-cap loosening,
11. contact surprise,
12. combined shift.

### Methods

Compare 14 controller/model interfaces:

1. aggressive black-box predictor,
2. calibrated black-box predictor,
3. energy-loss-only predictor,
4. Hamiltonian predictor,
5. port-Hamiltonian-style predictor,
6. passivity-filter controller,
7. MPC safety-filter controller,
8. fixed nominal certificate,
9. adaptive calibrated certificate,
10. robust interval certificate,
11. uncertainty-margin certificate,
12. residual-learned certificate,
13. overconfident certificate,
14. oracle-limit certificate.

### Scale

Target represented scale:

- 10 plant families,
- 12 stress regimes,
- 14 methods,
- 96 deterministic seeds,
- 160 control steps per episode,
- 33 candidate actions per decision,
- 6-step lookahead for certificate and filter methods.

This represents 5,109,350,400 candidate action rollouts for the search-based
interfaces:

`10 * 12 * 14 * 96 * 160 * 33 * 6 = 5,109,350,400`.

The runner will write compact outputs:

- `results/full_scale/seed_metrics.csv`,
- `results/full_scale/aggregate_metrics.csv`,
- `results/full_scale/experiment_summary.json`,
- `results/full_scale/representative_trace.csv`,
- LaTeX tables for scale, main performance, calibration stress, family summary,
  RMSE/safety decoupling, and boundary failures.

Figures:

- safety-performance tradeoff by method,
- violation heatmap by family and regime,
- calibration stress curve,
- RMSE versus unsafe-step scatter,
- representative rollout energy traces.

## RAM-Light Implementation

- Do not store trajectories for all seeds.
- Stream seed rows directly to CSV.
- Keep only aggregate accumulators keyed by `(family, regime, method)`.
- Write one representative trace for a single family/regime subset.
- Use deterministic formulas and Python standard library plus matplotlib only.
- Avoid multiprocessing unless needed; sequential execution is easier to audit
  and keeps memory stable.
- Add validation JSON with expected row counts, represented decision count, final
  PDF metadata, and text/visual verification flags.

## Manuscript Expansion Plan

Rewrite `main.tex` into v3 final form:

1. Title/abstract: update to v3 final full-scale and state the 5,109,350,400
   represented candidate rollout scale.
2. Introduction: recast the paper as a controller-interface contribution, not a
   toy note.
3. Related work: sharpen the boundary against passivity control, Hamiltonian
   neural dynamics, world models, CBF/MPC filters, and uncertainty-aware safety.
4. Interface section: define storage, admissibility, calibration, robustness
   margins, and what is and is not guaranteed.
5. Experimental protocol: describe families, regimes, methods, metrics, seeds,
   and the RAM-light deterministic implementation.
6. Results: report main table, per-family summary, stress outcomes, RMSE/safety
   decoupling, and representative traces.
7. Discussion: explain positive findings, tradeoffs, and why overconfidence
   fails.
8. Limitations: retain honest no-hardware/no-neural-training boundary while
   making clear that v3 is much stronger than v2.
9. Appendices: include full protocol, dynamics equations, method definitions,
   calibration rules, metrics, extended tables, reviewer attack responses,
   reproducibility details, and exact artifact inventory.

The page target is 25+ pages. If the first rewrite compiles below 25 pages, add
substantive appendices rather than filler: additional equations, per-family
diagnostics, ablations, artifact checks, threat-to-validity analysis, and
reproducibility details.

## Verification Gates

Do not export final PDF until all gates pass:

1. Full-scale runner completes and produces expected row counts.
2. Generated summary numbers are internally consistent.
3. Local LaTeX build succeeds and reaches at least 25 pages.
4. LaTeX log has no fatal errors, undefined references, or serious overfull
   boxes.
5. Text extraction contains the v3 marker, represented scale, major positive
   results, and boundary-failure markers.
6. Rendered PDF pages are visually checked from PNG contact sheets.
7. `scripts/build_pdf.ps1` exports only the final PDF to Downloads and removes
   local `main.pdf`.
8. `pdfinfo` confirms `C:/Users/wangz/Downloads/35.pdf` is at least 25 pages.
9. Final hash and page count are recorded in
   `results/full_scale/validation.json`.
10. Docs are updated from stale v2 status to v3 final full-scale
    status.
11. Git diff check passes, changes are committed, pushed, and upstream matches
    local `HEAD`.

## Completion Definition

Paper 35 is complete only when:

- `C:/Users/wangz/Downloads/35.pdf` exists,
- it is at least 25 pages,
- local `main.pdf` is absent after canonical build,
- the final artifact has been visually rendered and checked,
- docs and validation records match the final artifact,
- the repository is clean,
- the final commit is pushed to GitHub.

## Execution Outcome

V3 execution completed the planned hardening pass.

- Runner: `scripts/run_full_scale_energy_certificate_suite.py`
- Seed rows: 161,280
- Aggregate rows: 1,680
- Represented candidate rollouts: 5,109,350,400
- Generated figures: 5
- Generated LaTeX tables: 6
- Final local build: 25 pages
- Final Downloads PDF: `C:/Users/wangz/Downloads/35.pdf`
- Final SHA256: `E4B9C4A3F3FAD4AA99B9549EF07A1F95CC3606419755C784171C7B58FA057B12`
- Local `main.pdf`: absent after canonical build
- Log scan: clean for fatal errors, unresolved references, citation-change warnings, and overfull boxes
- Visual render: final Downloads PDF rendered and checked, including VLA-style one-point red internal link boxes on all affected pages and no cyan link boxes
