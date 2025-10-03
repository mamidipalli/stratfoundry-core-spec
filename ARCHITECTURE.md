# Architecture (Core)

```mermaid
flowchart LR
  A[Plain-English Strategy] --> B[Synthesis (LLM→YAML)]
  B --> C[Validator (Schema + Semantics)]
  C --> D[Compiler (YAML→IR)]
  D --> E[Spec/Registry (S3+PG)]
  D --> F[Sim-Preview]
  D --> G[Deployment Manager]
  G --> H[Strategy Runner (Engine Actors)]
  H --> I[Order Router]
  I --> J[Broker Connectors (Delta testnet first)]
  H <-- K[Market Data (bars/ticks)]
  H --> L[Ledger (orders/fills/positions)]
Design tenets: determinism, idempotency, separation of authoring vs. execution, multi-subscriber fan-out.
