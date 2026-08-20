import json, sys
from pathlib import Path

REQUIRED = ["case_identity", "representation", "fact_timeline", "evidence_status", "procedure_status", "open_issues", "workflow_outputs"]

def main(path):
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    missing = [k for k in REQUIRED if k not in data]
    errors = []
    if missing:
        errors.append("missing keys: " + ", ".join(missing))
    for event in data.get("fact_timeline", []):
        if not event.get("event_id") or not event.get("event") or not event.get("status"):
            errors.append(f"invalid timeline event: {event!r}")
        if event.get("date") is None and not event.get("date_precision"):
            errors.append(f"unknown date lacks date_precision: {event.get('event_id')}")
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))

