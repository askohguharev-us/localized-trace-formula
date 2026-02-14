# Localized Trace Formula for Hyperbolic Surfaces

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16877265.svg)](https://doi.org/10.5281/zenodo.16877265)
[![Release](https://img.shields.io/github/v/release/askoghuharev-us/localized-trace-formula?display_name=tag)](../../releases/latest)
[![Build Status](https://github.com/askoghuharev-us/localized-trace-formula/actions/workflows/archaios-publish.yml/badge.svg)](https://github.com/askoghuharev-us/localized-trace-formula/actions)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE-CC-BY-4.0)

> **Monograph Title:** Localized Trace Formula: A Microlocal Approach with Power-Saving Remainders  
> **Author:** Alexander S. Kozhukharev  
> **Affiliation:** Independent Researcher (Moscow, Russia)  
> **Subject:** Spectral Theory, Automorphic Forms, Microlocal Analysis

---

## Abstract

This monograph establishes a **localized trace formula** for finite-area hyperbolic surfaces $\Gamma\backslash\mathbb{H}$ with cusps. By constructing a microlocalized wave propagator and a smooth spectral projector onto the interval $[\lambda-\eta, \lambda+\eta]$, we derive a geometric expansion over closed geodesics of length up to $T \asymp \log\lambda$. 

The main result is a **power-saving remainder term** $O(\lambda^{-\delta})$, where $\delta > 0$ depends on the spectral gap and the geometry of the cusps. This provides a robust framework for quantitative local Weyl laws and variance estimates for Hecke–Maass forms.



## Mathematical Classification (MSC 2020)
- **11F72** (Spectral theory; Selberg trace formula)
- **58J40** (Pseudodifferential operators and Fourier integral operators on manifolds)
- **11L05** (Gauss and Kloosterman sums; Hecke operators)
- **35P20** (Asymptotic distribution of eigenvalues and eigenfunctions)

## Project Structure

The monograph is built using a modular LaTeX framework for maximum rigour and clarity:

* `src/sections/`: Core theoretical development (microlocal tools, kernel estimates).
* `src/appendices/`: Detailed auxiliary proofs and historical context.
* `ancillary/`: Machine-readable validation reports.
* `bib/`: Comprehensive bibliography (Selberg, Sarnak, Venkatesh, et al.).

## Automated Rigour & Validation

This project employs non-standard automated tools to ensure mathematical consistency:

### 1. Gödel Validation (Reference Graph)
We utilize a custom tool to extract all mathematical entities (Theorems, Lemmas, Definitions) and build a directed acyclic graph (DAG) of dependencies based on `\ref{}` links.
- **Status:** All 40+ main results are logically reachable and cycle-free.
- **Report:** See `ancillary/godel_report.md`.

### 2. ARCHAIOS Assessment
A framework for verifying the structural integrity of the LaTeX stack and compliance with open-access scientific standards.
- **Metrics:** `ancillary/archaios_public_report.json`.



## Local Build Instructions

To compile the monograph from source, you need a full **TeX Live 2023+** distribution.

```bash
# Clone the repository
git clone [https://github.com/askoghuharev-us/localized-trace-formula.git](https://github.com/askoghuharev-us/localized-trace-formula.git)
cd localized-trace-formula

# Build using the provided Makefile (requires latexmk)
make pdf

# Output will be located in build/main.pdf
