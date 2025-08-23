# ==== PDF ====
BUILD=build
SRC=src/main.tex
SECTIONS=src/sections/*.tex
APPENDICES=src/appendices/*.tex

pdf: $(BUILD)/paper.pdf
$(BUILD)/paper.pdf: $(SRC) $(SECTIONS) $(APPENDICES) src/references.bib
	@mkdir -p $(BUILD)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=$(BUILD) $(SRC)

clean:
	latexmk -C -outdir=$(BUILD)
	rm -rf $(BUILD) arxiv.tar.gz public-src

# ==== Ancillary ====
ancillary:
	python3 scripts/metafractal_check.py --out ancillary/archaios_public_report.json --csv ancillary/archaios_public_report.csv || true
	python3 archaios/godel/extract.py --in src --out ancillary/godel_graph.json || true
	python3 archaios/godel/check.py   --in archaios/godel --out ancillary/godel_report.csv --md ancillary/godel_report.md || true

# ==== Публичная редакция (арxiv) ====
PUBLIC_TAG ?= PUBLIC
redact:
	@rm -rf public-src && mkdir -p public-src/sections public-src/appendices
	python3 scripts/redact.py --tag $(PUBLIC_TAG) --in src/sections    --out public-src/sections
	python3 scripts/redact.py --tag $(PUBLIC_TAG) --in src/appendices  --out public-src/appendices
	cp src/main.tex public-src/main.tex
	cp src/references.bib public-src/references.bib

# ==== arXiv bundle ====
arxiv: redact
	tar -czf arxiv.tar.gz -C public-src .

# ==== всё для релиза ====
release: pdf ancillary arxiv
	@echo "Artifacts ready: $(BUILD)/paper.pdf, ancillary/*, arxiv.tar.gz"
