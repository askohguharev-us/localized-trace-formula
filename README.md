[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16837383.svg)](https://doi.org/10.5281/zenodo.16837383)
[![Release](https://img.shields.io/github/v/release/askoghuharev-us/localized-trace-formula?display_name=tag)](../../releases/latest)
[![ARCHAIOS publish](https://github.com/askoghuharev-us/archaios-core-private/actions/workflows/archaios-publish.yml/badge.svg)](https://github.com/askoghuharev-us/archaios-core-private/actions/workflows/archaios-publish.yml)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](LICENSE-MIT)
[![Content License: CC BY 4.0](https://img.shields.io/badge/Content%20License-CC%20BY%204.0-lightgrey.svg)](LICENSE-CC-BY-4.0)

**Latest PDF:** see [Releases → latest](../../releases/latest)

# A Localized Trace Formula (Block 0)

**Status:** Block 0 — research preprint (active).  
**PDF:** built by GitHub Actions (see Releases / latest artifact).

## What is here
- Title, metadata, abstract (≤200 words), keywords, MSC.
- Author affiliation: *Independent Researcher, Moscow, Russia*.
- Core sections (§§1–6), appendices, arXiv-safe LaTeX stack, vector TikZ.

## ARCHAIOS assessment (public flavor only)
- Human-readable: [`ARCHAIOS-REPORTS/public.md`](ARCHAIOS-REPORTS/public.md)  
- Machine: JSON [`ancillary/archaios-public.json`](ancillary/archaios-public.json) •
  CSV [`ancillary/archaios-public.csv`](ancillary/archaios-public.csv)

> **Policy:** Public flavor contains *metrics only*.  
> No proprietary methodology or recommendations are published here.

## Build locally
Requires TeX Live 2023+ (or MiKTeX) with `latexmk`.

```bash
make pdf          # build to build/main.pdf
# or
cd src && latexmk -pdf -interaction=nonstopmode main.tex
