#!/usr/bin/env python3
import sys, os, glob, yaml

def load_yaml(p):
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def extract_id(item):
    # поддерживаем два формата:
    # 1) {"id": "C1", ...}
    # 2) {"C1": "..."} или {"C1": {...}}
    if isinstance(item, dict):
        if "id" in item and isinstance(item["id"], (str, int)):
            return str(item["id"])
        if len(item) == 1:
            k = next(iter(item.keys()))
            if isinstance(k, (str, int)):
                return str(k)
    return None

def collect_local_ids(godel_dir):
    ids = set()
    for path in sorted(glob.glob(os.path.join(godel_dir, "*.yaml"))):
        y = load_yaml(path)
        for key in ("definitions", "claims", "goals"):
            for it in y.get(key, []) or []:
                _id = extract_id(it)
                if _id:
                    ids.add(_id)
    return ids

def flatten_nodes(layers):
    nodes = []
    for _, arr in (layers or {}).items():
        if not arr: 
            continue
        for v in arr:
            if isinstance(v, (str, int)):
                nodes.append(str(v))
    return nodes

def is_external(node):
    # Внешние узлы: ссылки на другие блоки, например "@block0:A1"
    return isinstance(node, str) and node.startswith("@")

def main():
    if len(sys.argv) < 3:
        print("Usage: metafractal_check.py <godel_dir> <meta_dir>")
        sys.exit(2)

    godel_dir = sys.argv[1]
    meta_dir  = sys.argv[2]

    # 1) Соберём локальные ID из Gödel-файлов
    local_ids = collect_local_ids(godel_dir)

    # 2) Возьмём первый *.meta.yaml в meta_dir
    meta_files = sorted(glob.glob(os.path.join(meta_dir, "*.meta.yaml")))
    if not meta_files:
        print("ERROR: no .meta.yaml files found in", meta_dir)
        sys.exit(2)
    meta_path = meta_files[0]
    meta = load_yaml(meta_path)

    layers = meta.get("layers", {})
    edges  = meta.get("edges", []) or []

    meta_nodes = flatten_nodes(layers)

    # 3) Проверки
    errors = 0
    kinds  = {}

    # 3a) все узлы (кроме внешних) должны существовать среди local_ids
    for n in meta_nodes:
        if is_external(n):
            continue
        if n not in local_ids:
            errors += 1
            kinds["unknown_local_id"] = kinds.get("unknown_local_id", 0) + 1

    # 3b) все рёбра должны ссылаться на объявленные в layers узлы
    node_set = set(meta_nodes)
    for e in edges:
        if not (isinstance(e, list) and len(e) == 2):
            errors += 1
            kinds["bad_edge_format"] = kinds.get("bad_edge_format", 0) + 1
            continue
        u, v = map(str, e)
        for x in (u, v):
            if is_external(x):
                continue
            if x not in node_set:
                errors += 1
                kinds["edge_to_unknown_node"] = kinds.get("edge_to_unknown_node", 0) + 1

    summary = {
        "meta_file": os.path.basename(meta_path),
        "layers": len(layers),
        "nodes": len(meta_nodes),
        "edges": len(edges),
        "local_ids": sorted(local_ids),
        "errors": errors,
    }
    print("METAFRACTAL SUMMARY:", summary)
    if errors:
        print("ERROR KINDS:", kinds)
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
