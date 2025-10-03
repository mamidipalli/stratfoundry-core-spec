
Versions

- CAPSULE SF-CORE-2025-10-03 — v2025.10.03 (initial)

- capsule-v2025.10.03-2 — Schema & tooling
  - DSL schema updated to draft 2020-12 **$defs** (replaced deprecated `definitions`)
  - Orders schema allows `oco_with` (for TP/SL brackets)
  - CI switched to **YAML 1.2** parsing (ruamel.yaml) to avoid `on/off/yes/no` boolean pitfalls
  - Example YAMLs validated via GitHub Actions

- capsule-v2025.10.03-3 — Docs & bootstrap
  - **CAPSULE.md** clarified (stable capsule name, bootstrap instructions)
  - **README.md** added with Quickstart, Versioning/Tags, and usage with ChatGPT
  - No changes to DSL/IR/CONTRACTS schemas (code can continue pinning `-2` if desired)
