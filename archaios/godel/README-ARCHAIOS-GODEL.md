# ARCHAIOS Gödel-layer (logic verifier)

Purpose
-------
This layer verifies the *logical* structure of a proof block:
assumptions → lemmas → inference steps → main claim, with explicit
dependencies, boundary cases, and constant control. It complements
any Coq-like symbolic checker.

How it works (manual v0.1)
--------------------------
- You maintain one YAML file per block: `<block>.godel.yaml`.
- ARCHAIOS parses it and reports:
  * missing assumptions / hidden hypotheses,
  * circularity in dependencies,
  * boundary cases not covered,
  * constants and parameter domains underspecified.

Status levels
-------------
- draft → review → locked

House rules (no recursion)
--------------------------
- The block cannot validate itself using its own claim.
- Metachecks use a reduced set: (Consistency, Reviewability).
