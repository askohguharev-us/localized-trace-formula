#!/usr/bin/env python3
import sys, os, yaml, glob
import networkx as nx

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def iter_ids(obj):
    if isinstance(obj, dict):
        if "id" in obj and isinstance(obj["id"], str):
            yield obj["id"]
        for v in obj.values():
            yield from iter_ids(v)
    elif isinstance(obj, list):
        for x in obj:
            yield from iter_ids(x)

def normalize(node):
    return str(node).strip()

def collect_godel_ids(godel_dir):
    known = set()
    files = sorted(glob.glob(os.path.join(godel_dir, "block*.godel.yaml")))
    for p in files:
        try:
            data = load_yaml(p)
            for id_ in iter_ids(data):
                known.add(normalize(id_))
        except Exception:
            pass
    return known

def check_meta(meta_path, known_ids):
    data = load_yaml(meta_path)
    errors = []

    for k in ["version", "block", "layers", "edges"]:
        if k not in data:
            errors.append(f"missing_key:{k}")

    layers = data.get("layers", {})
    edges  = data.get("edges", [])

    layer_nodes = []
    layer_index = {}
    for i, (lname, ids) in enumerate(layers.items()):
        if not isinstance(ids, list):
            errors.append(f"bad_layer_list:{lname}")
            continue
        for x in ids:
            x = normalize(x)
            layer_nodes.append(x)
            layer_index[x] = i

    G = nx.DiGraph()
    G.add_nodes_from(layer_nodes)
    for e in edges:
        if not (isinstance(e, list) and len(e) == 2):
            errors.append("bad_edge_format")
            continue
        u, v = normalize(e[0]), normalize(e[1])
        if u not in layer_index:
            errors.append(f"edge_unknown_src:{u}")
        if v not in layer_index:
            errors.append(f"edge_unknown_dst:{v}")
        G.add_edge(u, v)
        if u in layer_index and v in layer_index:
            if layer_index[u] > layer_index[v]:
                errors.append(f"layer_violation:{u}->{v}")

    try:
        _ = list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        errors.append("cycle_detected")

    for x in layer_nodes:
        if not x.startswith("@") and x not in known_ids:
            errors.append(f"unknown_local_id:{x}")

    summary = {
        "meta_file": os.path.basename(meta_path),
        "layers": len(layers),
        "nodes": len(layer_nodes),
        "edges": len(edges),
        "errors": len(errors),
    }
    print("METAFRACTAL SUMMARY:", summary)
    if errors:
        kinds = {}
        for e in errors:
            k = e.split(":")[0]
            kinds[k] = kinds.get(k, 0) + 1
        print("ERROR KINDS:", kinds)

    return len(errors) == 0

def main():
    if len(sys.argv) != 3:
        print("Usage: metafractal_check.py <godel_dir> <meta_dir>")
        sys.exit(2)
    godel_dir, meta_dir = sys.argv[1], sys.argv[2]
    known_ids = collect_godel_ids(godel_dir)

    ok_all = True
    for meta_path in sorted(glob.glob(os.path.join(meta_dir, "block*.meta.yaml"))):
        ok = check_meta(meta_path, known_ids)
        ok_all = ok_all and ok
    sys.exit(0 if ok_all else 1)

if __name__ == "__main__":
    main()
