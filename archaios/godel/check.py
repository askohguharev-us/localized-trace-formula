# -*- coding: utf-8 -*-
"""
Мини-проверки по godel_graph.json и отчёты в CSV/MD.
Не валит workflow при отсутствии данных — выдаёт пустой отчёт.
"""
from __future__ import annotations
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUTD = ROOT / "ancillary"
OUT_JSON = OUTD / "godel_graph.json"
OUT_CSV  = OUTD / "godel_report.csv"
OUT_MD   = OUTD / "godel_report.md"
OUTD.mkdir(parents=True, exist_ok=True)

graph = {"stats": {}, "labels": [], "refs": []}
if OUT_JSON.exists():
    graph = json.loads(OUT_JSON.read_text(encoding="utf-8"))

stats = graph.get("stats", {})
labels = {n["id"] for n in graph.get("labels", [])}
refs   = graph.get("refs", [])

dangling = [r for r in refs if r.get("label") not in labels]
dup_list = stats.get("duplicate_labels", [])

rows = []
rows.append(["check", "status", "details"])
rows.append(["no_dangling_refs", "PASS" if not dangling else "FAIL", f"count={len(dangling)}"])
rows.append(["no_duplicate_labels", "PASS" if not dup_list else "FAIL", f"dups={len(dup_list)}"])
rows.append(["basic_density", "INFO", f"labels={len(labels)}, refs={len(refs)}"])

with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)

md = [
    "# Gödel layer report",
    "",
    f"*files*={stats.get('files_scanned',0)}, *labels*={len(labels)}, *refs*={len(refs)}",
    "",
    "| Check | Status | Details |",
    "|---|---|---|",
]
for r in rows[1:]:
    md.append(f"| {r[0]} | {r[1]} | {r[2]} |")
OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

print(f"[godel:check] wrote {OUT_CSV.name} & {OUT_MD.name}")
