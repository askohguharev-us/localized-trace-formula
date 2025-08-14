# -*- coding: utf-8 -*-
import re, os, json, hashlib, pathlib

SRC_DIR = pathlib.Path("src")
OUT_JSON = pathlib.Path("ancillary/godel_graph.json")
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

# environments to capture
KINDS = ["definition","lemma","proposition","theorem","corollary","remark"]

env_re = re.compile(
    r"\\begin\{(" + "|".join(KINDS) + r")\}([\s\S]*?)\\end\{\1\}",
    re.M
)
label_re = re.compile(r"\\label\{([^\}]+)\}")
title_re = re.compile(r"\\(begin\{.*?\}|textbf|emph)\{(.*?)\}")
ref_re = re.compile(r"\\ref\{([^\}]+)\}")

def norm_text(s: str) -> str:
    s = re.sub(r"%.*", "", s)              # drop comments
    s = re.sub(r"\\cite\{.*?\}", "", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^\}]*\})*", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

entities = []
edges = []

for tex in SRC_DIR.rglob("*.tex"):
    txt = tex.read_text(encoding="utf-8", errors="ignore")
    # entities
    for m in env_re.finditer(txt):
        kind = m.group(1)
        block = m.group(2)
        # label inside the block
        lab = label_re.search(block)
        if not lab:  # allow unlabeled but mark with synthetic id
            eid = f"{kind}:{tex.name}:{m.start()}"
        else:
            eid = lab.group(1)
        # poor man's title: first bold/emph or first sentence
        title = ""
        t = title_re.search(block)
        title = t.group(2) if t else norm_text(block)[:120]
        h = sha256(norm_text(block)[:1000])
        # line number
        line = txt[:m.start()].count("\n") + 1
        entities.append({
            "id": eid, "kind": kind, "title": title,
            "file": str(tex), "line": line, "hash": h
        })
    # refs (global, we’ll bind source later by nearest env)
    for m in ref_re.finditer(txt):
        rid = m.group(1)
        line = txt[:m.start()].count("\n") + 1
        edges.append({
            "from": None, "to": rid, "file": str(tex), "line": line,
            "context": "ref"
        })

# map refs to nearest preceding entity in the same file (heuristic)
by_file = {}
for e in entities:
    by_file.setdefault(e["file"], []).append(e)
for lst in by_file.values():
    lst.sort(key=lambda x: x["line"])

for ed in edges:
    lst = by_file.get(ed["file"], [])
    prev = [e for e in lst if e["line"] <= ed["line"]]
    ed["from"] = prev[-1]["id"] if prev else "(doc)"

graph = {"entities": entities, "refs": edges}
OUT_JSON.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT_JSON}")
