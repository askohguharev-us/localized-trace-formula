# Gödel Layer (MVP) – schema

Artifacts:
- ancillary/godel_graph.json    # entities + edges
- ancillary/godel_report.csv    # issues table
- ancillary/godel_report.md     # human summary

Entity = { id, kind, title, file, line, hash }
  kind ∈ {definition, lemma, proposition, theorem, corollary, remark}
Edge   = { from, to, file, line, context }

Issues (CSV):
  severity ∈ {error, warn, info}
  code ∈ {BROKEN_REF, MISSING_PROOF, CYCLE, ORPHAN_ENTITY, ORPHAN_REF}
