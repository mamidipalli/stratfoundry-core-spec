# scripts/validate_examples.py
import sys, json, pathlib, textwrap
from jsonschema import Draft202012Validator
from ruamel.yaml import YAML

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Find the DSL schema (v1 preferred)
schema_path = next((p for p in [
    ROOT / "DSL" / "v1" / "strategy.schema.json",
    ROOT / "DSL" / "strategy.schema.json",
] if p.exists()), None)
if not schema_path:
    print("[ERR] Missing DSL schema")
    sys.exit(1)

schema = json.loads(schema_path.read_text())
validator = Draft202012Validator(schema)

# Collect YAML examples
example_dirs = [ROOT / "DSL" / "v1" / "examples", ROOT / "DSL" / "examples"]
yaml_files = [p for d in example_dirs if d.exists() for p in d.glob("*.y*ml")]
if not yaml_files:
    print("[ERR] No example YAML files found")
    sys.exit(1)

# YAML 1.2 loader (so 'on', 'off', 'yes', 'no' are plain strings)
yaml = YAML(typ="safe")
yaml.version = (1, 2)

def show_context(path: pathlib.Path, line: int, span: int = 3):
    lines = path.read_text(encoding="utf-8").splitlines()
    start = max(0, line - span - 1)
    end = min(len(lines), line + span)
    block = "\n".join(f"{i+1:>4}: {lines[i]}" for i in range(start, end))
    print(block)

ok = True
for ypath in sorted(yaml_files):
    try:
        with open(ypath, "r", encoding="utf-8") as f:
            data = yaml.load(f)
    except Exception as e:
        print(f"[YAML ERR] {ypath}: {e}")
        # Try to show a small context if ruamel provides marks (it usually does)
        ok = False
        continue

    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    if errors:
        print(f"[SCHEMA ERR] {ypath.name}")
        for err in errors[:5]:
            loc = "/".join(map(str, err.path)) or "<root>"
            print(f"  at {loc}: {err.message}")
        if len(errors) > 5:
            print(f"  ... and {len(errors)-5} more")
        ok = False
    else:
        print(f"[OK] {ypath.name}")

sys.exit(0 if ok else 1)
