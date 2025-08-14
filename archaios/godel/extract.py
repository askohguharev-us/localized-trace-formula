# -*- coding: utf-8 -*-
"""
Простой извлекатель «графа ссылок» из LaTeX.
Сканирует src/**/*.tex, тащит \label{..} и \ref/\eqref{..},
пишет ancillary/godel_graph.json (и не падает, если ничего не найдено).
"""
from __future__ import annotations
import os, re, json, glob, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]  # .../localized-trace-formula
SRC  = ROOT / "src"
OUTD = ROOT / "ancillary"
OUTD.mkdir(parents=True, exist_ok=True)
OUT_JSON = OUTD / "godel_graph.json"

tex_files = sorted(glob.glob(str(SRC / "**" / "*.tex"), recursive=True))
labels = {}
refs   = []
dups   = set()

lab_re  = re.compile(r"\\label\{([^}]+)\}")
ref_re  = re.compile(r"\\(?:ref|eqref)\{([^}]+)\}")

for path in tex_files:
    try:
        txt = pathlib.Path(path).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    # метим все label'ы
    for m in lab_re.finditer(txt):
        lab = m.group(1).strip()
        if lab in labels:
            dups.add(lab)
        else:
            labels[lab] = {"file": os.path.relpath(path, ROOT)}

    # собираем ссылки
    for m in ref_re.finditer(txt):
        lab = m.group(1).strip()
        refs.append({"file": os.path.relpath(path, ROOT), "label": lab})

# метрики
dangling = [r for r in refs if r["label"] not in labels]
stats = {
    "timestamp": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
    "files_scanned": len(tex_files),
    "labels": len(labels),
    "refs": len(refs),
    "duplicate_labels": sorted(list(dups)),
    "dangling_refs": len(dangling),
}

graph = {
    "version": "godel-graph-0.1",
    "stats": stats,
    "labels": [{"id": k, **v} for k, v in labels.items()],
    "refs": refs,
}

OUT_JSON.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[godel:extract] wrote {OUT_JSON} (files={len(tex_files)}, labels={len(labels)}, refs={len(refs)})")
