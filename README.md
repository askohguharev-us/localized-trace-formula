[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16810648.svg)](https://doi.org/10.5281/zenodo.16810648)
[![Release](https://img.shields.io/github/v/release/askohguharev-us/localized-trace-formula?display_name=tag)](../../releases/latest)
[![ARCHAIOS publish](https://github.com/askohguharev-us/archaios-core-private/actions/workflows/archaios.yml/badge.svg)](https://github.com/askohguharev-us/archaios-core-private/actions/workflows/archaios.yml)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](LICENSE-MIT)
[![Content License: CC BY 4.0](https://img.shields.io/badge/Content%20License-CC%20BY%204.0-lightgrey.svg)](LICENSE-CC-BY-4.0)

**Latest PDF:** see [Releases → latest](../../releases/latest)

# A Localized Trace Formula (Block 0)

**Status:** Block 0 finalized — `v0.3.0`  
**PDF:** built by GitHub Actions (see Releases / latest artifact)

## What is here
- Title, metadata, abstract (≤200 words), keywords, MSC.
- Author affiliation: *Independent Researcher, Moscow, Russia*.
- Minimal statements for reference (Block 0).
- arXiv-safe LaTeX stack; vector TikZ; working CI.

## ARCHAIOS assessment (public flavor)
Public, non-proprietary metrics for this block:

- Human-readable: [`ARCHAIOS-REPORTS/public.md`](ARCHAIOS-REPORTS/public.md)
- Machine-readable:  
  JSON — [`ancillary/archaios_public_report.json`](ancillary/archaios_public_report.json)  
  CSV — [`ancillary/archaios_public_report.csv`](ancillary/archaios_public_report.csv)

> Public flavor = metrics only (no recommendations).  
> Fields: `KPD, KGD, KSD, KSR, KFZ, KKA, composite, conf`.

## How to build locally
Requirements: TeX Live 2023+ (or MiKTeX) with `latexmk`.

```bash
# Option A (recommended)
make pdf          # uses the root Makefile → builds into build/main.pdf

# Option B (manual)
cd src
latexmk -pdf -interaction=nonstopmode main.tex
