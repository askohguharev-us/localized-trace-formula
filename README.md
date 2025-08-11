[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16808989.svg)](https://doi.org/10.5281/zenodo.16808989)

**Latest PDF:** see [Releases → latest](../../releases/latest)

# A Localized Trace Formula (Block 0)

**Status:** Block 0 skeleton finalized — `v0.3.0`  
**PDF:** built by GitHub Actions (see Releases / latest asset)

## What is here
- Title, metadata, abstract (≤200 words), keywords, MSC.
- Sections split into `src/sections/01-intro.tex` and `src/sections/02-preliminaries.tex` and included via `\input`.
- Acknowledgments + Data availability added to ToC.
- arXiv-safe LaTeX stack; vector TikZ; working bibliography.
- Dual license: **CC BY 4.0** (text & figures) + **MIT** (code/scripts). See `LICENSE`, `LICENSE-CC-BY-4.0`, `LICENSE-MIT`.
- `CITATION.cff` with DOI.

## How to build locally
Requirements: TeX Live 2023+ or MiKTeX with `latexmk`.

```bash
latexmk -pdf -interaction=nonstopmode main.tex
