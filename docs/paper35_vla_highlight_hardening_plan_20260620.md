# Paper35 VLA Highlight Hardening Plan

Date: 2026-06-20

## Objective

Make `C:/Users/wangz/Downloads/35.pdf` visually match the VLA-v4 role model's PDF link-box behavior while preserving the already-final 25-page submission content:

- internal equation/table/figure links use red one-point boxes;
- citation and URL links use green one-point boxes when those link types exist;
- no cyan URL boxes remain;
- the final PDF is rebuilt, rendered, inspected, copied only to Downloads, and leaves no local `main.pdf`.

## Plan-Start Evidence

Baseline artifact:

- Canonical PDF: `C:/Users/wangz/Downloads/35.pdf`
- Pages: 25
- Size: 377,741 bytes
- SHA256: `013579C68D8D4C834207DAEF12F523DE6D630EA0C79FC6EF4E23E682AF28727D`
- Local `main.pdf`: absent
- Repository state: clean against `origin/master`

Baseline link inventory from the current Downloads PDF:

- Link pages: `[(3, 2), (5, 1), (6, 1), (7, 1), (8, 1), (12, 1), (15, 1)]`
- Border colors: red = 8
- Border width: `(0, 0, 1)` for all 8 link annotations
- Cyan links: 0
- Green links: 0

Source finding:

- `main.tex` is a single-root manuscript at repository root.
- The preamble currently uses plain `\usepackage{hyperref}` with no VLA-style `\hypersetup`.
- The manuscript contains internal `\ref` links and `\path` text, but no `\cite`, `\citep`, `\citet`, `\url`, or `\href` commands. Therefore the final PDF is expected to contain red internal reference boxes only; green citation/URL boxes are configured for consistency but should not be forced by adding cosmetic links.

Baseline visual render:

- Rendered affected pages 3, 5, 6, 7, 8, 12, and 15 into `C:/Users/wangz/highlight_box_hardening/tmp/pdfs/paper35_before`.
- Visual samples show crisp red boxes around internal references, with no cyan boxes.

## Role-Model Target

Use the same explicit hyperref policy as the visible VLA-v4 role model:

```tex
\usepackage{hyperref}
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 1},
  citebordercolor={0 1 0},
  linkbordercolor={1 0 0},
  urlbordercolor={0 1 0}
}
```

## Execution Plan

1. Add the role-model `\hypersetup` immediately after `\usepackage{hyperref}` in `main.tex`.
2. Rebuild with `scripts/build_pdf.ps1`, which copies the final PDF to Downloads and removes local `main.pdf`.
3. Recompute page count, SHA256, annotation colors, border widths, and local artifact status.
4. Render the affected link pages from the rebuilt Downloads PDF into `tmp/pdfs/paper35_after`.
5. Visually inspect every affected page against the VLA role model:
   - red boxes remain crisp and aligned around internal references;
   - no cyan boxes appear;
   - green link behavior is configured but not artificially introduced where the paper has no cite/url links;
   - no layout drift, clipped text, overfull boxes, or broken tables appear.
6. Update README/status/audit/version metadata with the new hash and visual-hardening result.
7. Scan LaTeX logs for fatal errors, undefined references, rerun warnings, and overfull boxes.
8. Remove Paper35 temp renders, leaving only the shared role-model render directory.
9. Stage only Paper35 source and metadata files, commit, push, and verify a clean repository.

## Non-Goals

- Do not add fake citations, URLs, or content merely to create green boxes.
- Do not alter experiment results, claims, figures, tables, or page-count target.
- Do not leave intermediate PDFs or render folders in the repository or temp area.

## Final QA Result

- Final PDF: `C:/Users/wangz/Downloads/35.pdf`
- Pages: 25
- Size: 377,741 bytes
- SHA256: `E4B9C4A3F3FAD4AA99B9549EF07A1F95CC3606419755C784171C7B58FA057B12`
- Link pages: `[(3, 2), (5, 1), (6, 1), (7, 1), (8, 1), (12, 1), (15, 1)]`
- Annotation colors: red = 8, green = 0, cyan = 0
- Border widths: `(0, 0, 1)` for all 8 link annotations
- Visual QA: affected pages rendered from the rebuilt Downloads PDF and inspected. Red boxes are crisp and aligned; no layout drift or cyan boxes appear. Green cite/url boxes are configured by policy but absent because the manuscript has no cite/url link annotations.
- Local `main.pdf`: absent after canonical build
