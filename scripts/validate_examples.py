import sys, json, pathlib
import yaml, jsonschema

ROOT = pathlib.Path(file).resolve().parents[1]
schema = json.loads((ROOT/"DSL/strategy.schema.json").read_text())

ok = True
for ypath in (ROOT/"DSL/examples").glob("*.yaml"):
with open(ypath, "r") as f:
data = yaml.safe_load(f)
try:
jsonschema.validate(data, schema)
print(f"[OK ] {ypath.name}")
except jsonschema.ValidationError as e:
print(f"[ERR] {ypath.name}: {e.message}")
ok = False

sys.exit(0 if ok else 1)
