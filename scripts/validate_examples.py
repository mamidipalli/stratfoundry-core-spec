# scripts/validate_examples.py
import sys, json, pathlib, textwrap
import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
schema_path = next((p for p in [
    ROOT/"DSL/v1/strategy.schema.json",
    ROOT/"DSL/strategy.schema.json"
] if p.exists()), None)
if not schema_path:
    print("[ERR] Missing DSL schema"); sys.exit(1)

schema = json.loads(schema_path.read_text())
validator = Draft202012Validator(schema)

example_dirs = [ROOT/"DSL/v1/examples", ROOT/"DSL/examples"]
yaml_files = [p for d in example_dirs if d.exists() for p in d.glob("*.y*ml")]
if not yaml_files:
    print("[ERR] No example YAML files found"); sys.exit(1)

def show_context(path: pathlib.Path, line: int, span: int = 3):
    lines = path.read_text().splitlines()
    start = max(0, line - span - 1)
    end = min(len(lines), line + span)
    block = "\n".join(f"{i+1:>4}: {lines[i]}" for i in range(start, end))
    print(textwrap.dedent(block))

ok = True
for ypath in sorted(yaml_files):
    try:
        with open(ypath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"[YAML ERR] {ypath}")
        if hasattr(e, 'problem_mark') and e.problem_mark:
            print(f"  at line {e.problem_mark.line+1}, column {e.problem_mark.column+1}")
            show_context(ypath, e.problem_mark.line+1)
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
