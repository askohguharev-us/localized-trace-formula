# -*- coding: utf-8 -*-
import json, pathlib, csv, sys
INP = pathlib.Path("ancillary/godel_graph.json")
RCSV = pathlib.Path("ancillary/godel_report.csv")
RMD  = pathlib.Path("ancillary/godel_report.md")

g = json.loads(INP.read_text(encoding="utf-8"))
ids = {e["id"] for e in g["entities"]}
by_id = {e["id"]: e for e in g["entities"]}

issues = []

# 1) broken refs / orphan refs
for r in g["refs"]:
    if r["to"] not in ids:
        issues.append(["error","BROKEN_REF",r["file"],r["line"],f"ref → {r['to']} not found"])

# 2) missing proof: for theorem/lemma without 'proof' following (heuristic via next entity gap)
#   Assume proof resides between this entity and next entity in same file
by_file = {}
for e in g["entities"]:
    by_file.setdefault(e["file"], []).append(e)
for f,lst in by_file.items():
    lst.sort(key=lambda x: x["line"])
    text = pathlib.Path(f).read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    for i,e in enumerate(lst):
        if e["kind"] in ("theorem","lemma","proposition"):
            endline = lst[i+1]["line"]-1 if i+1<len(lst) else len(lines)
            segment = "\n".join(lines[e["line"]-1:endline])
            if "\\begin{proof}" not in segment:
                issues.append(["warn","MISSING_PROOF",f,e["line"],f"{e['id']} has no proof block"])

# 3) dependency cycles (very rough: build edges only between known ids)
adj = {i:set() for i in ids}
for r in g["refs"]:
    if r["from"] in ids and r["to"] in ids:
        adj[r["from"]].add(r["to"])

visited, stack = set(), set()
def dfs(u):
    visited.add(u); stack.add(u)
    for v in adj[u]:
        if v not in visited and dfs(v): return True
        if v in stack:
            issues.append(["error","CYCLE","-",0,f"{u} → {v}"])
            return True
    stack.remove(u); return False

for i in ids:
    if i not in visited: dfs(i)

# 4) orphan entities (never referenced, informational)
refed = {r["to"] for r in g["refs"] if r["to"] in ids}
for i in ids - refed:
    issues.append(["info","ORPHAN_ENTITY",by_id[i]["file"],by_id[i]["line"],i])

# write CSV
RCSV.parent.mkdir(parents=True, exist_ok=True)
with RCSV.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["severity","code","file","line","detail"])
    w.writerows(issues)

# write MD summary
errs = sum(1 for x in issues if x[0]=="error")
warns = sum(1 for x in issues if x[0]=="warn")
md = []
md.append("# Gödel Validation Report (MVP)\n")
md.append(f"- Entities: **{len(ids)}**; Refs: **{len(g['refs'])}**")
md.append(f"- Errors: **{errs}**, Warnings: **{warns}**\n")
if errs:
    md.append("## Errors")
    for s,c,f,l,d in issues:
        if s=="error": md.append(f"- **{c}** @ `{f}:{l}` — {d}")
if warns:
    md.append("\n## Warnings")
    for s,c,f,l,d in issues:
        if s=="warn": md.append(f"- **{c}** @ `{f}:{l}` — {d}")
RMD.write_text("\n".join(md), encoding="utf-8")

# fail build if errors
if errs>0:
    print("Gödel check: errors present"); sys.exit(1)
print("Gödel check: OK")
