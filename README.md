# stratfoundry-core-spec

Source-of-truth specs for StratFoundry core: **YAML Strategy DSL → IR → Engine (Runner)**.  
First target: **Delta Exchange Testnet**. This repo anchors all future chats, issues, and service work.

---

## Contents

- **CAPSULE.md** — the project “anchor” (mission, NFRs, happy path).
- **DSL/v1/** — Strategy DSL schema + examples (YAML in, validated by JSON Schema).
- **IR/v1/** — Internal Representation schema for the engine.
- **CONTRACTS/** — Public contracts (`order_intent.json`, `execution_report.json`).
- **ENDPOINTS/** — Public OpenAPI surface (ui-gateway).
- **scripts/** — CI helper scripts (e.g., YAML validation).
- **SERVICE_MATRIX.md** — Services vs. requirements, status, and order of work.
- **BACKLOG.md** — Epics → stories → tasks.
- **DECISIONS.md** — ADRs (design decisions with rationale).
- **VERSIONS.md** — Capsule/spec tags and dates.

---

## Quickstart

### 1) Local validation (Python 3.11)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_examples.py
```

- Validates all YAML examples under `DSL/v1/examples/` against `DSL/v1/strategy.schema.json`.
- Uses **YAML 1.2** (ruamel.yaml) so keys like `on/off/yes/no` remain strings (no YAML 1.1 boolean surprises).

### 2) CI

GitHub Actions runs schema validation on every push and PR. If CI fails:
- Read the log — the validator prints YAML line/column context and schema paths.
- Keep examples under `DSL/v1/examples/`.
- Stick to plain quotes and spaces (YAML forbids tabs).

### 3) Helpful local tools

```bash
pip install yamllint jsonschema
yamllint DSL/v1/examples/*.yaml
```

---

## Using this repo to work with ChatGPT

**Paste this in any new chat to lock context:**

```
Use context capsule SF-CORE-2025-10-03 from:
https://github.com/mamidipalli/stratfoundry-core-spec/tree/<TAG>

Today’s task: <one-liner, e.g., “review instrument-resolver zip v20251004”>.
Follow YAML DSL → IR → Runner architecture. Use schemas/contracts in this repo.
Only propose changes compliant with the capsule/tag.
```

> Replace `<TAG>` with a real tag (see **Versioning & Tags**). This prevents design drift across threads.

---

## Versioning & Tags

- Schemas and contracts are versioned under `DSL/v*/`, `IR/v*/`, `CONTRACTS/v*/` (and `DEPLOYMENT/v*/` when added).
- Tags (e.g., `capsule-v2025.10.03-1`) mark stable checkpoints you can reference in chats and issues.

**When to bump a tag**

- **Required:** Any change to **DSL/IR/DEPLOYMENT** schemas or public **CONTRACTS**.
- **Not required:** App code changes, refactors, performance work, internal docs that don’t alter contracts.

**Create a tag**

```bash
git tag capsule-vYYYY.MM.DD[-N]
git push --tags
```

Update **VERSIONS.md** with each tag.

---

## How to add a new task/feature

1) Add an entry in **BACKLOG.md** (under an existing EPIC or create a new one).
2) Open a GitHub Issue with this structure:

```
[STORY] <concise goal>

Context
- Capsule tag: <tag>
- Why now / links to ADR(s)

Deliverables
- APIs/Contracts to add/change
- Files to touch (schemas/examples/docs)

Acceptance Criteria
- Behavior & data shapes
- SLO/latency (if any)
- Tests (unit/integration/e2e)

Dependencies
- Upstream/downstream services, creds, data

Test Plan
- Exact cases, golden vectors, failure modes

Ops/CI
- Dashboards, alerts, Actions changes (if any)
```

3) **If contracts/schemas change**:
   - Update the relevant schema under `*/v*/`.
   - Add/adjust examples in `*/v*/examples/`.
   - Write an ADR in **DECISIONS.md**.
   - Bump tag in **VERSIONS.md** and push the tag.

---

## Strategy DSL (YAML)

Keep *strategy logic only* in DSL (indicators, signals, risk, orders).  
Run-mode, subscriber config, and broker account belong in **deployment configs** (a separate schema will live under `DEPLOYMENT/`).

**Example (abridged):**

```yaml
name: Eternal Breakout Long
version: 1.0.0
universe:
  - symbol: BTCUSDTPERP
    venue: DELTA
    asset_class: crypto_perp
data:
  timeframes: [1m, 5m, 15m]
  warmup_bars: 300
  session: { timezone: "UTC", trading_days: "MON-FRI" }
indicators:
  - { id: ema20, fn: EMA, on: close@5m, args: { period: 20 } }
  - { id: rsi14, fn: RSI, on: close@5m, args: { period: 14 } }
signals:
  entry_long:
    all:
      - { ">": { lhs: close@5m, rhs: ema20 } }
      - { ">": { lhs: rsi14, rhs: 55 } }
      - { ">": { lhs: close@1m, rhs: prev_high@15m } }
orders:
  entry: { side: BUY, type: LIMIT, price: "last - 0.05%_of_last", qty: risk_based }
  sl:    { type: STOP,  price: "entry - 0.50%_of_entry" }
  tp:    { type: LIMIT, price: "entry + 0.80%_of_entry", oco_with: sl }
  tsl:   { type: TRAIL_PERCENT, trail: 0.35, activation: "profit >= 0.40%" }
execution:
  broker: DELTA
  time_in_force: DAY
  reduce_only: false
risk:
  capital_per_trade: { type: percent_equity, value: 1.0 }
  max_daily_trades: 2
  max_concurrent_positions: 1
```

Notes:
- YAML 1.2 loader ensures `on/off/yes/no` aren’t auto-booleans.
- Inline maps `{ ... }` are fine; keep commas between pairs.

---

## Contributing workflow (for app repos too)

1) Branch → edit schemas/examples/docs.  
2) Run local validation.  
3) If changing contracts: write ADR, bump tag.  
4) Open PR; CI must be green.  
5) Merge and tag.  
6) In downstream services, pin to the new tag (or publish a tiny `sf_spec` package with these schemas and depend on a specific version).

---

## FAQ / Troubleshooting

**YAML parse error in CI**  
- Check for a missing `:` after a key, missing commas in inline `{}` maps, or tabs (YAML forbids tabs).
- Use block style for lists/objects while iterating.

**Schema error “Additional properties are not allowed”**  
- Your YAML contains a field not permitted by the schema (e.g., adding `oco_with` before the schema allowed it). Update the schema or fix the YAML.

**How to start a new chat without losing context?**  
- Paste the **Bootstrap snippet** with a real **tag**. That locks us both to the same specs.

---

## License

(Add your preferred license: MIT, Apache-2.0, etc.)

---

## Next steps

- Tag the repository with your next stable checkpoint (e.g., `capsule-v2025.10.03-1`).
- Open the first review issue for **instrument-resolver** and attach its code zip.
- Start a new chat with the Bootstrap snippet + issue link. We’ll proceed service-by-service to Delta Testnet trading.
