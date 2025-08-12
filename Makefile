# Root Makefile for building PDF and arXiv bundle

SRC_DIR   := src
SECT_DIR  := $(SRC_DIR)/sections
OUT       := build
PDF       := $(OUT)/main.pdf

TEX_MAIN  := $(SRC_DIR)/main.tex
SECTIONS  := $(SECT_DIR)/01-intro.tex \
             $(SECT_DIR)/02-preliminaries.tex \
             $(SECT_DIR)/03-kernel.tex \
             $(SECT_DIR)/04-projector.tex

FIGS_DIR  := figs
VERSION   ?= 0.3.1

LATEXMK   := latexmk
LATEXFLAGS := -pdf -interaction=nonstopmode

.PHONY: all pdf clean distclean anc-pack help

all: pdf

$(OUT):
	@mkdir -p $(OUT)

pdf: $(OUT) $(TEX_MAIN) $(SECTIONS)
	@cd $(SRC_DIR) && $(LATEXMK) $(LATEXFLAGS) main.tex
	@mkdir -p $(OUT)
	@cp $(SRC_DIR)/main.pdf $(PDF)
	@echo "PDF -> $(PDF)"

clean:
	-@cd $(SRC_DIR) 2>/dev/null && $(LATEXMK) -C || true
	-@rm -rf $(OUT)

distclean: clean
	-@rm -rf dist

# -------- arXiv ancillary pack (создаёт dist/arxiv-src.zip)
anc-pack:
	@echo ">> Building arXiv source with anc/"
	@rm -rf dist/arxiv-src && mkdir -p dist/arxiv-src/anc
	# исходники статьи
	@rsync -a --exclude '.git' --exclude '.github' --exclude 'dist' \
	      --exclude 'ARCHAIOS-REPORTS' --exclude 'ancillary' \
	      ./ dist/arxiv-src/
	# ancillary (переименуем README в ARCHAIOS_README.md)
	@cp -f ancillary/archaios_public_report.json dist/arxiv-src/anc/ 2>/dev/null || true
	@cp -f ancillary/archaios_public_report.csv  dist/arxiv-src/anc/ 2>/dev/null || true
	@cp -f ancillary/README.md                   dist/arxiv-src/anc/ARCHAIOS_README.md 2>/dev/null || true
	@cd dist && zip -rq arxiv-src.zip arxiv-src
	@echo ">> Done: dist/arxiv-src.zip"

help:
	@echo "Targets:"
	@echo "  pdf        - build $(PDF)"
	@echo "  anc-pack   - make arXiv bundle with anc/ (dist/arxiv-src.zip)"
	@echo "  clean      - clean LaTeX intermediates"
	@echo "  distclean  - clean + remove dist/"
