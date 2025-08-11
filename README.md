[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16798535.svg)](https://doi.org/10.5281/zenodo.16798535)

**Latest PDF:** see [Releases → latest](../../releases/latest)

# A Localized Trace Formula (Block 0)

**Status:** Block 0 (front matter + sections split) — `v0.2.0`  
**PDF:** built by GitHub Actions (see Releases / latest artifact)

## What is here
- Title, metadata, abstract (≤200 words), keywords, MSC.
- Author affiliation: *Independent Researcher, Moscow, Russia*.
- Minimal statements kept for reference; main text split into:
  - `src/sections/01-intro.tex`
  - `src/sections/02-preliminaries.tex`
  (included in `main.tex` right after `\tableofcontents` via `\input{...}`).
- Acknowledgments & Data availability now appear in the ToC.
- arXiv-safe LaTeX stack; vector TikZ; working GitHub Actions build.

## How to build locally
Requirements: TeX Live 2023+ or MiKTeX with `latexmk`.

```bash
latexmk -pdf -interaction=nonstopmode main.tex
# clean:
latexmk -c
