# Reproducibility Checklist

- [x] Main simulator is `scripts/energy_certificate_sim.py`.
- [x] Build script is `scripts/build_pdf.ps1`.
- [x] Main output is `docs/energy_certificate_results.csv`.
- [x] V2 outputs are `docs/energy_damping_mismatch_stress.csv` and `docs/energy_damping_mismatch_stress_table.tex`.
- [x] Paper source is `main.tex`.
- [x] Canonical PDF path is `C:/Users/wangz/Downloads/35.pdf`.
- [x] Local `main.pdf` is removed after canonical copy.
- [x] Visible Desktop PDF copies are absent.

Recommended verification commands:

```powershell
python scripts\energy_certificate_sim.py
python scripts\energy_certificate_sim.py --stress-only
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
```
