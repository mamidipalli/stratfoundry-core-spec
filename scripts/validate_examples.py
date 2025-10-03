# scripts/validate_examples.py
import sys
import json
import pathlib

import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Locate the schema (supports versioned or unversioned layout)
schema_path_candidates = [
    ROOT / "DSL" / "v1" / "strategy.schema.json",
    ROOT / "DSL" / "strategy.schema.json",
]
schema_path = next((p for p in schema_path_candidates if p.exists()), None)
if not schema_path:
    print("[ERR] Could not find strategy schema JSON under DSL/ or DSL/v1/")
    sys.exit(1)

schema = json.loads(schema_path.read_text())
validator = Draft202012Validator(schema)

# Collect example YAMLs from both possible locations
example_dirs = [
    ROOT / "DSL" / "v1" / "examples",
    ROOT / "DSL" / "examples",
]
yaml_files = []
for d in example_dirs:
    if d.exists():
        yaml_files.extend(list(d.glob("*.yaml")))
        yaml_files.extend(list(d.glob("*.yml")))

if not yaml_files:
    print("[ERR] No example YAML files found in DSL/examples/ or DSL/v1/examples/")
    sys.exit(1)

ok = True
for ypath in sorted(yaml_files):
    with open(ypath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    if errors:
        print(f"[ERR] {ypath.name}")
        for e in errors[:5]:  # print first few to keep logs readable
            loc = "/".join(map(str, e.path)) or "<root>"
            print(f"      at {loc}: {e.message}")
        if len(errors) > 5:
            print(f"      ... and {len(errors)-5} more")
        ok = False
    else:
        print(f"[OK ] {ypath.name}")

sys.exit(0 if ok else 1)
