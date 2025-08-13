# Changelog
All notable changes to this project will be documented in this file.
We (loosely) follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and semantic-ish versioning for the “Block 0” preprint line.

---

## [Unreleased] – v0.7.1
**Planned**
- Refresh ARCHAIOS public report to point to **v0.7.0 DOI** and current release tag.
- Compliance note terminology: ensure *all* metric names are in English
  (`KPD, KGD, KSD, KSR, KFZ, KKA`) with no Cyrillic leftovers.
- Minor prose polish in §§5–6 after proof pass.

---

## v0.7.0 — Chapters 5–6 + Appendix A; ancillary package (2025-08-13)
**Added**
- **Section 5** (Microlocal construction) and **Section 6** (Geometric term)
  — full text; placeholders removed.
- **Appendix A (Effective volume)**, with proper `\appendix` handling.
- **Ancillary package** under `ancillary/`:
  - `archaios_public_report.json`, `archaios_public_report.csv`
    (public ARCHAIOS metrics),
  - `ARCHAIOS-COMPLIANCE-NOTE.md` (arXiv compliance note).
- README badges and sections:
  Zenodo DOI badge, Release badge, ARCHAIOS publish badge,
  links to ancillary JSON/CSV, and build instructions.
- `CITATION.cff` updated:
  version **v0.7.0**, date `2025-08-13`,
  DOI **10.5281/zenodo.16837383**, preferred citation with
  **Alexander Stepanovich Kozhukharev**.

**Changed**
- `src/main.tex`: enabled `\appendix` and moved ARCHAIOS material *out* of the
  main paper (ancillary-only), fixed duplicated appendix headings in ToC.
- Cross-references and labels across §§2–4 made consistent
  (`lem:time-local`, projector/commutator lemmas, geometric term proposition).
- README wording and links refreshed to match the new structure.

**Fixed**
- **Build:** resolved `latexmk` exit 12 (missing labels/dup titles);
  appendix duplication removed.
- **Publish workflow:** fixed “repository not found / 404” by
  normalizing `owner/repo`, adding a quick API 200-check, and sanitizing inputs.

**Infrastructure**
- `archaios-publish` workflow matured:
  JSON/CSV derived from `ARCHAIOS-REPORTS/public.md`,
  uploaded as artifact and published into target repo’s `ancillary/`.
- Makefile: `make pdf` builds into `build/main.pdf`.

**Notes**
- Current public CSV/JSON may still reference the **v0.6.0** DOI/tag;
  this will be refreshed in **v0.7.1** after the metrics regeneration run.

---

## v0.6.0 — Metafractal checks online + Block 1 scaffolding polish (2025-08-12)
**Added**
- Metafractal CI: private meta repo + public lint runner; green checks on push.
- Minimal public checker (`scripts/metafractal_check.py`) with local/externals split.

**Changed**
- Block 1 YAML: normalized local IDs (C1, C2, C3, C4, D1, main-thm).
- LaTeX metadata bumped to v0.6.0.

**Infrastructure**
- `.github/workflows/metafractal.yml` wired to `META_TOKEN` and private meta.

---

## v0.5.0 — Kernel fix + stability (2025-08-11)
**Changed**
- Kernel section cleaned and stabilized; projector scaffolding kept.
- Gödel YAML checks green for Block 0/1.
- Clarified cross-references and notation in §§2–3.
- DOI maintained: 10.5281/zenodo.16810648 (historic).

---

## [v0.2.0] — 2025-08-11
**Added**
- Section files: `sections/01-intro.tex`, `sections/02-preliminaries.tex`.
- Long-form CC BY 4.0 (`LICENSE-CC-BY-4.0`).
- Dual-license note (`LICENSE`) and MIT for workflows (`LICENSE-MIT`).
- Valid `CITATION.cff` with preferred-citation.

**Changed**
- TOC anchors for unnumbered sections.
- README: links to Releases and DOI.

**Fixed**
- Names/affiliation metadata, CFF validation.

---

## Legend
- **ARCHAIOS metrics (public flavor):** metrics only (no recommendations):
  `KPD, KGD, KSD, KSR, KFZ, KKA, composite, conf`.

[Unreleased]: ../../compare/v0.7.0...HEAD
[v0.2.0]: ../../releases/tag/v0.2.0
