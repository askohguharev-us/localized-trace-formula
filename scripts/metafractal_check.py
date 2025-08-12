#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metafractal sanity-check for Archaios meta files.

Usage (from repo root):
    python scripts/metafractal_check.py archaios/godel archaios/metafractal
The script will scan all *.meta.yaml files inside the meta-dir.

What it checks (minimal public version):
  1) Syntax/shape of meta: required keys, list types, edges format.
  2) Local-vs-external nodes:
     - Local IDs = items from layers other than 'Axioms' (e.g., Defs/Claims/Goal/...).
     - External refs must start with '@' (e.g., "@block0:A1").
     - If a non-@ name appears that is NOT declared as a local ID, it is an error.
  3) Edge endpoints must be either a declared local ID or an external ref ('@...').

This file intentionally does NOT load private rules or the full Archaios engine.
It only performs a safe public lint that reveals nothing about the internal method.
"""

from __future__ import annotations

import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

try:
    import yaml  # PyYAML
except Exception as e:
    print("FATAL: PyYAML is required. Install with 'pip install pyyaml'.")
    raise


# ---------- helpers ----------

def load_yaml(fp: Path) -> Any:
    with fp.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_external(name: str) -> bool:
    """External references are written as '@blockK:ID' (we only check the '@')."""
    return isinstance(name, str) and name.startswith("@")

# ---------- core logic ----------

def flatten_nodes(layers: Dict[str, Any]) -> List[str]:
    """Collect all node names from layer lists (strings only)."""
    nodes: List[str] = []
    for _layer_name, lst in (layers or {}).items():
        if lst is None:
            continue
        if not isinstance(lst, list):
            continue
        for item in lst:
            if isinstance(item, str):
                nodes.append(item.strip())
    return nodes


def local_ids_from_layers(layers: Dict[str, Any]) -> List[str]:
    """
    By convention in the public lint:
      - 'Axioms' layer contains only external references, so it doesn't contribute local IDs.
      - All OTHER layers contribute local IDs (e.g., 'Defs', 'Claims', 'Lemmas', 'Goal', etc.).
    """
    locals_list: List[str] = []
    for lname, lst in (layers or {}).items():
        if lname.lower() == "axioms":
            # Do not add Axioms to locals: they should be written as @blockX:Ak
            continue
        if not isinstance(lst, list):
            continue
        for item in lst:
            if isinstance(item, str) and not is_external(item):
                locals_list.append(item.strip())
    return locals_list


def check_meta_file(meta_fp: Path) -> Tuple[int, Dict[str, int]]:
    """
    Returns: (errors_count, error_kinds)
    """
    data = load_yaml(meta_fp)
    errors = 0
    kinds: Dict[str, int] = {}

    # basic shape
    if not isinstance(data, dict):
        print(f"{meta_fp}: ERROR meta must be a mapping/dict.")
        return 1, {"bad_shape": 1}

    layers = data.get("layers")
    edges = data.get("edges")

    if not isinstance(layers, dict):
        print(f"{meta_fp}: ERROR 'layers' must be a mapping.")
        return 1, {"missing_layers": 1}

    if edges is None:
        edges = []
    if not isinstance(edges, list):
        print(f"{meta_fp}: ERROR 'edges' must be a list.")
        return 1, {"bad_edges": 1}

    # gather nodes
    meta_nodes: List[str] = flatten_nodes(layers)
    local_ids: List[str] = local_ids_from_layers(layers)

    # Check edge shapes
    bad_edge_shape = 0
    for e in edges:
        if not (isinstance(e, (list, tuple)) and len(e) == 2 and
                all(isinstance(x, str) for x in e)):
            bad_edge_shape += 1
    if bad_edge_shape:
        errors += bad_edge_shape
        kinds["bad_edge_shape"] = bad_edge_shape

    # Find unknown locals:
    # any node or edge endpoint that is NOT external and NOT in local_ids.
    local_set: Set[str] = set(local_ids)
    unknown_locals: Set[str] = set()

    # from nodes listed in layers
    for n in meta_nodes:
        if not is_external(n) and n not in local_set:
            unknown_locals.add(n)

    # from edges endpoints
    for a, b in [tuple(e) for e in edges if isinstance(e, (list, tuple)) and len(e) == 2]:
        if not is_external(a) and a not in local_set:
            unknown_locals.add(a)
        if not is_external(b) and b not in local_set:
            unknown_locals.add(b)

    if unknown_locals:
        cnt = len(unknown_locals)
        errors += cnt
        kinds["unknown_local_id"] = cnt
        print("UNKNOWN LOCAL IDS:", sorted(unknown_locals))

    # Summary
    print(
        "METAFRACTAL SUMMARY:",
        {
            "meta_file": meta_fp.name,
            "layers": len(layers),
            "nodes": len(meta_nodes),
            "edges": len(edges),
            "local_ids": local_ids,
            "errors": errors,
        }
    )

    return errors, kinds


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage:\n  python scripts/metafractal_check.py <godel_dir> <meta_dir>")
        # godel_dir is currently unused in the public lint (kept for future).
        return 2

    godel_dir = Path(sys.argv[1]).resolve()
    meta_dir = Path(sys.argv[2]).resolve()

    if not meta_dir.exists():
        print(f"ERROR: meta_dir not found: {meta_dir}")
        return 2

    meta_files = sorted(meta_dir.glob("*.meta.yaml"))
    if not meta_files:
        print(f"ERROR: no *.meta.yaml files in {meta_dir}")
        return 2

    total_errors = 0
    aggregate: Dict[str, int] = {}

    for mf in meta_files:
        print(f"\n--- Checking {mf} ---")
        errs, kinds = check_meta_file(mf)
        total_errors += errs
        for k, v in kinds.items():
            aggregate[k] = aggregate.get(k, 0) + v

    if total_errors:
        print("ERROR KINDS:", aggregate)
        return 1

    print("\nOK: metafractal checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
