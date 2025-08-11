[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16808989.svg)](https://doi.org/10.5281/zenodo.16808989)

**Latest PDF:** see [Releases → latest](../../releases/latest)

# A Localized Trace Formula (Block 0)

**Status:** Block 0 finalized — `v0.3.0`  
**PDF:** built by GitHub Actions (see Releases / latest artifact)

## What is here
- Title, metadata, abstract (≤200 words), keywords, MSC.
- Author affiliation: *Independent Researcher, Moscow, Russia*.
- Minimal statements for reference (Block 0).
- arXiv-safe LaTeX stack; vector TikZ; working CI.

## How to build locally
Requirements: TeX Live 2023+ or MiKTeX with `latexmk`.

```bash
latexmk -pdf -interaction=nonstopmode main.tex
