# StratFoundry Core Capsule — SF-CORE-2025-10-03 (v2025.10.03)

**Mission (Core only):** Plain-English strategy → YAML DSL → Validate → Compile to IR → Deploy → Run on an engine that places/manages orders (entry, SL, TSL, TP) → Exit per rules. First broker: **Delta Exchange Testnet**; architecture must remain broker-agnostic.

**Non-negotiables / NFRs**
- YAML in, validated by a **JSON Schema** (deterministic; no code-gen per strategy).
- Engine interprets IR for many strategies and many subscribers (fan-out at execution).
- Idempotent **OrderIntent** + transactional outbox; typed rounding (tick/lot/precision).
- Latency SLO: bar-close→decision **p95 ≤ 50ms**; order ACK **p95 ≤ 250ms**.
- Deterministic indicators/expressions; TSL is a one-way ratchet.

**Happy Path**
1) Synthesis makes **YAML** (schema-constrained).
2) Validator + Semantic checks normalize.
3) Compiler emits **IR** (JSON/msgpack) with indicator DAG + typed AST.
4) Deployment passes IR to **Strategy Runner** (engine).
5) Runner consumes bars, evaluates signals, submits orders via **broker-connector**.

**Services Matrix (pointer)**
See `SERVICE_MATRIX.md`. All designs in this repo are the source of truth.

**Chat bootstrap (paste this in any new ChatGPT thread)**
> Use context capsule **SF-CORE-2025-10-03** from https://github.com/mamidipalli/stratfoundry-core-spec.git .  
> Follow CAPSULE.md and the YAML DSL → IR → Runner pipeline.  
> Today’s task: <one-liner>.  
> Only propose changes that comply with CAPSULE & schemas here.

