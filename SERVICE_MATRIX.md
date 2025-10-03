
Services vs Requirements Matrix
#	Service	Status	Keep / Change	Key Actions (next)
1	ui-gateway	Active	Keep	Add routes for synth/validate/compile/deploy/preview/backtest
2	synthesis	Active	Change	YAML-constrained prompting + inline schema validation
3	validator	Active	Merge→lib	Move logic to strategy_dsl lib; keep thin API wrapper
4	compiler	Active	Change	Real YAML→IR (DAG/AST), bind instruments, emit IR hash
5	sim-preview	Active	Change	Use IR + evaluator; no mock math
6	spec-store (registry)	Active	Change	Add registry metadata (symbols, TFs, broker)
7	instrument-resolver	Active	Change	Expand for Delta testnet constraints first
8	broker-connector	Active	Change	Delta testnet adapter with idempotent COID + OCO emu
9	llm-proxy	Active	Keep	Schema-aware decoding; YAML only
10	deployment-manager	Active	Change	Actor scheduling; warmup prefetch of bars
11	strategy-media	Active	Defer	Optional enrichment; out of P0 scope
12	strategy-runner	NEW	Add	Engine actors, SL/TSL/TP, idempotent intents
13	signal-evaluator	NEW	Add	Deterministic indicators + typed exprs
14	market-data	NEW	Add	Minimal Redis Streams bars for Delta testnet
15	backtester	NEW	Add	Same runner with sim clock

Implementation Order (to first real trade on Delta testnet)

instrument-resolver (Delta), 2) strategy_dsl lib, 3) compiler (real),

signal-evaluator (lib), 5) market-data (1m/5m bars), 6) broker-connector (Delta),

strategy-runner (engine), 8) deployment-manager warmup,

synthesis (YAML strict), 10) sim-preview (IR), 11) spec-store registry, 12) backtester.
