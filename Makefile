# Root Makefile for building PDF and arXiv bundle

SRC_DIR := src
SECT_DIR := $(SRC_DIR)/sections
OUT     := build
PDF     := $(OUT)/main.pdf

TEX_MAIN := $(SRC_DIR)/main.tex
SECTIONS := $(SECT_DIR)/01-intro.tex \
            $(SECT_DIR)/02-preliminaries.tex \
            $(SECT_DIR)/03-kernel.tex \
            $(SECT_DIR)/04-projector.tex

FIGS_DIR := figs
ARXIV_DIR := arxiv
ARXIV_TGZ := $(ARXIV_DIR)/ltformula-v$(VERSION).tar.gz
VERSION ?= 0.3.1

LATEXMK := latexmk
LATEXFLAGS := -pdf -interaction=nonstopmode -shell-escape -halt-on-error

.PHONY: all pdf clean arxiv distclean

all: pdf

$(OUT):
	mkdir -p $(OUT)

pdf: $(OUT) $(TEX_MAIN) $(SECTIONS)
	cd $(SRC_DIR) && $(LATEXMK) $(LATEXFLAGS) main.tex
	@mkdir -p $(OUT)
	@cp $(SRC_DIR)/main.pdf $(PDF)
	@echo "PDF -> $(PDF)"

clean:
	cd $(SRC_DIR) && $(LATEXMK) -c
	rm -f $(PDF)

distclean: clean
	rm -rf $(OUT) $(ARXIV_DIR)

# ----- arXiv bundle -----
arxiv: pdf
	mkdir -p $(ARXIV_DIR)/src $(ARXIV_DIR)/$(FIGS_DIR)
	cp -a $(SRC_DIR)/*.tex $(ARXIV_DIR)/src/
	cp -a $(SECT_DIR) $(ARXIV_DIR)/src/
	@if [ -d "$(FIGS_DIR)" ]; then cp -a $(FIGS_DIR)/* $(ARXIV_DIR)/$(FIGS_DIR)/ || true; fi
	# licenses and citation
	cp -a LICENSE* $(ARXIV_DIR)/ || true
	cp -a CITATION.cff $(ARXIV_DIR)/ || true
	# pack
	tar -C $(ARXIV_DIR) -czf $(ARXIV_TGZ) .
	@echo "arXiv bundle -> $(ARXIV_TGZ)"
