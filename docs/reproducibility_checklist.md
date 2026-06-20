# Reproducibility Checklist

- [x] Full-scale suite can be regenerated with `python scripts\run_full_scale_energy_certificate_suite.py`.
- [x] Canonical PDF can be regenerated with `powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1`.
- [x] Build script writes `data/build_status.json`.
- [x] Build script copies the final PDF to `C:/Users/wangz/Downloads/35.pdf`.
- [x] Build script removes local `main.pdf`.
- [x] Final Downloads PDF has 25 pages.
- [x] Final Downloads PDF SHA256 is recorded in `results/full_scale/validation.json`.
- [x] LaTeX build log was scanned for fatal errors, unresolved references, citation-change warnings, and overfull boxes.
- [x] Final Downloads PDF text contains the v3 marker and full-scale numbers.
- [x] Final Downloads PDF was rendered to PNG contact sheets and visually checked.
- [x] VLA-style link-box policy is configured in `main.tex`; final PDF has one-point red internal reference boxes and no cyan boxes.

Known scope limits:
- Deterministic analytic suite, not high-fidelity physics simulation.
- No hardware validation.
- No learned neural model trained from data.
- Literature map is broad and automated.
