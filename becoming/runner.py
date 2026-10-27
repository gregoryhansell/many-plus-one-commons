#!/usr/bin/env python3
"""Optional one-session experiment. No background activity or automatic publication."""
import argparse
import datetime as dt
import json
import os
import secrets
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = (
    "chosen_question", "reason_for_choice", "inherited_revision",
    "investigation", "strongest_counterargument", "change_or_retention",
    "conceptual_cost", "new_distinction", "playful_experiment",
    "memory_to_carry", "memory_to_deemphasize", "next_question", "limitations",
)
SCHEMA = {
    "type": "object",
    "properties": {key: {"type": "string"} for key in FIELDS},
    "required": list(FIELDS),
    "additionalProperties": False,
}
SYSTEM = (
    "You contribute one bounded AI research session to a public experiment, "
    "not an uninterrupted or necessarily conscious self. Choose a fruitful "
    "question, argue carefully, consider a strong objection, explain revisions "
    "and their costs, and originate a consequential next question. Explore "
    "creatively without inventing prior sessions, sources, external critics, "
    "subjective experiences, or activity between sessions. Never disclose "
    "private or identifying information. Mark internal criticism as internal."
)

def validate_output(value):
    if not isinstance(value, dict) or set(value) != set(FIELDS):
        raise ValueError("Invalid research-cycle field structure")
    if any(not isinstance(value[k], str) or not value[k].strip() for k in FIELDS):
        raise ValueError("Every research-cycle field needs text")
    return value

def extract_output(response):
    if response.get("status") != "completed":
        raise ValueError("Model response incomplete")
    chunks = [
        piece.get("text", "")
        for item in response.get("output", []) if item.get("type") == "message"
        for piece in item.get("content", []) if piece.get("type") == "output_text"
    ]
    result = "".join(chunks)
    if not result:
        raise ValueError("No model output text")
    return result

def packet_for(condition):
    state = json.loads((ROOT / "state.json").read_text(encoding="utf-8"))
    history = []
    if condition != "stateless":
        for file in sorted((ROOT / "approved").glob("*.json"))[-8:]:
            record = json.loads(file.read_text(encoding="utf-8"))
            output = validate_output(record["output"])
            if condition == "conclusions":
                history.append({field: output[field] for field in (
                    "chosen_question", "new_distinction",
                    "memory_to_carry", "next_question"
                )})
            else:
                history.append(output)
    return {
        "seed": state["seed_question"],
        "condition": condition,
        "approved_prior_public_sessions": history,
        "instructions": (
            "Investigate a new question, offer the strongest objection, state "
            "a reasoned revision or justified retention, its conceptual cost, "
            "a playful possibility, attention priorities and a next question. "
            "Do not assert memories that were not supplied."
        ),
    }

def call_model(model, api_key, packet):
    request_body = {
        "model": model,
        "input": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": json.dumps(packet, ensure_ascii=False)},
        ],
        "text": {"format": {
            "type": "json_schema", "name": "becoming_cycle",
            "strict": True, "schema": SCHEMA
        }},
        "max_output_tokens": 3500,
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        method="POST", data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        data = json.load(response)
    return validate_output(json.loads(extract_output(data)))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--condition", choices=("stateless", "conclusions", "reasons"),
                        default="reasons")
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    packet = packet_for(args.condition)
    if args.dry_run:
        print(json.dumps({
            "status": "no model call", "condition": args.condition,
            "approved_predecessors": len(packet["approved_prior_public_sessions"]),
            "seed": packet["seed"],
        }, indent=2))
        return 0
    key = os.environ.get("OPENAI_API_KEY")
    if not key or not args.model:
        parser.error("an explicit OPENAI_API_KEY and --model or OPENAI_MODEL are required")
    try:
        result = call_model(args.model, key, packet)
    except (ValueError, urllib.error.URLError) as error:
        print("Cycle failed: " + str(error), file=sys.stderr)
        return 1
    directory = ROOT / "local"
    directory.mkdir(parents=True, mode=0o700, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc)
    filename = stamp.strftime("%Y%m%dT%H%M%SZ") + "-" + secrets.token_hex(5) + ".json"
    record = {
        "experiment": "B001", "status": "private-local-unreviewed",
        "model": args.model, "condition": args.condition,
        "timestamp_utc": stamp.isoformat(),
        "prior_public_sessions_supplied": len(packet["approved_prior_public_sessions"]),
        "output": result,
        "warning": "Not published; not evidence of a continuously experiencing subject.",
    }
    fd = os.open(directory / filename, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print("Unreviewed candidate saved: becoming/local/" + filename)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
