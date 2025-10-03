# stratfoundry-core-spec

- When you send a service for review, attach a small zip and include the **commit hash** of this spec repo (so I anchor to a specific version).

---

## 3) Immediate next steps (fastest path to a real Delta Testnet trade)

1) **Fill `instrument-resolver` data** for 1–2 Delta testnet symbols you’ll use (tick, step, lot, precision, session).
2) **Point your current synthesis** to produce YAML that validates against `DSL/strategy.schema.json`.
3) Replace your mocked compiler with a minimal real one:
   - YAML→dict,
   - `jsonschema` + semantic checks,
   - build a tiny IR (just enough for one long-only entry/exit + SL/TP/TSL) and save to S3.
4) Add a tiny market-data service (Redis Streams) to emit 1m bars for that symbol.
5) Implement the **Delta testnet** path in your broker-connector with idempotent `client_order_id`.
6) Drop in the **strategy-runner** skeleton (we’ll do this right after you share the first service).

---

If you want, I can also generate a **JIRA-ready** set of epics/stories straight from this spec (copy/paste), or we can start with your **instrument-resolver** zip now and wire it to the capsule.

How to add new tasks (that we can pick up in any future chat)

Create/Update an Epic in the repo

Append to BACKLOG.md under a new or existing EPIC.

If it touches services, add a row/update in SERVICE_MATRIX.md.

Open a GitHub Issue for the task

Title: [STORY] <concise goal> (or [EPIC] / [BUG]).

Label it (epic, story, P0/P1, service:<name>).

Put the content in this template (copy-paste):

## Context
Why this matters now. Link to CAPSULE tag and any ADRs.

## Deliverables
- APIs/Contracts to add or change
- Code paths/files to touch
- Artifacts (schemas, examples, docs)

## Acceptance Criteria
- [ ] Behavior and data shape (inputs/outputs)
- [ ] Latency/SLO (if applicable)
- [ ] Tests that prove it (unit/integration/e2e)

## Dependencies
Upstream schemas/services, data, credentials.

## Test Plan
Exact cases, golden vectors, failure modes.

## Ops/CI
Dashboards, alerts, GH Actions changes (if any).


If the task changes any contract/scheme

Add/modify files under DSL/v*/, IR/v*/, or DEPLOYMENT/v*/.

Add examples in the matching examples/ folder.

Write a short ADR in DECISIONS.md.

Bump the tag in VERSIONS.md and push a git tag (e.g., capsule-v2025.10.15-1).

CI should validate examples—keep it green.

Start (or continue) a chat

Paste this bootstrap (adjust numbers):

Use capsule tag capsule-v2025.10.15-1 from https://github.com/<YOUR_GH>/stratfoundry-core-spec .
Focus on ISSUE #123: “[STORY] Paper trading mode”.
Follow YAML DSL → IR → Runner. Only propose changes compliant with the tagged schemas.


I’ll load that exact tag + the issue details and work within those bounds.

What requires a tag bump vs not

No tag bump needed: internal code changes, new service implementation, performance work, docs that don’t change schemas/contracts.

Tag bump required: any change to DSL/IR/DEPLOYMENT schemas or public contracts in CONTRACTS/.

Example: adding a brand-new task

Task: Add “Portfolio Daily Loss Cap” overlay

Add an EPIC section in BACKLOG.md with stories (overlay lib, runner hook, metrics, e2e tests).

No DSL change (it’s deployment-time policy), so add to DEPLOYMENT/v1/deployment.schema.json:

"portfolio_risk": { "type":"object", "properties": { "daily_loss_cap_pct": {"type":"number","minimum":0} }, "additionalProperties": false }


Include DEPLOYMENT/v1/examples/delta_live_with_loss_cap.yaml.

Add ADR (“Why deployment-level overlay, not DSL”), bump tag, open issue, done.

Lightweight governance so we never drift

CAPSULE.md stays the anchor; only revise via ADR + tag.

SERVICE_MATRIX.md tracks scope/status so we both see what’s next.

CI enforces that examples match schemas and tags.