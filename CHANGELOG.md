# Changelog
## v0.6.0 — Metafractal checks online + Block 1 scaffolding polish (2025-08-12)
**Added**
- Metafractal CI: private meta repo + public lint runner; green checks on push.
- Minimal public checker (`scripts/metafractal_check.py`) with local/externals split.

**Changed**
- Block 1 YAML: normalized local IDs (C1, C2, C3, C4, D1, main-thm).
- LaTeX metadata bumped to v0.6.0.

**Infrastructure**
- `.github/workflows/metafractal.yml` wired to `META_TOKEN` and private meta.
## v0.5.0 — Kernel fix + stability
- Kernel section cleaned and stabilized.
- Projector scaffolding kept.
- Gödel YAML checks green for Block 0/1.
- DOI: 10.5281/zenodo.16810648.
## v0.5.0 — Kernel fix + stability (Block 1 skeleton)
- Fix: symmetric localized kernel definition in §3 (added `\chi_Y(y)`).
- New: labels `\label{def:KR}`, `\label{lem:schwartz-thick}`, `\label{def:TR}`, `\label{lem:stability}`, `\label{thm:main}`.
- Text: clarified cross-references to §2.2/§2.3.
- Notation: $\varepsilon(\theta,\beta)=\min\{\theta,1-1/(2\beta)\}$.

## v0.5.0 — Kernel fix + labels + stability (Block 1 skeleton)
- Fix: symmetric localized kernel definition in §3 (added `\chi_Y(y)`).
- New: labels `\label{def:KR}`, `\label{lem:schwartz-thick}`, `\label{def:TR}`, `\label{lem:stability}`, `\label{thm:main}`.
- Text: replaced ambiguous “§??” cross-references by §2.2/§2.3.
- Notation: clarified $\varepsilon(\theta,\beta)=\min\{\theta,1-1/(2\beta)\}$.
## [v0.2.0] - 2025-08-11
### Added
- Section files: `sections/01-intro.tex`, `sections/02-preliminaries.tex`
- Long-form CC BY 4.0 (LICENSE-CC-BY-4.0)
- Dual-license note (LICENSE) and MIT for workflows (LICENSE-MIT)
- Valid `CITATION.cff` with preferred-citation

### Changed
- TOC anchors for unnumbered sections
- README: links to Releases and DOI

### Fixed
- Names/affiliation metadata, CFF validation
