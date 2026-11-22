"""Build the blind calibration sheet for the owner's hand-labelling.

Run: python tools/make_calibration_sheet.py
Writes:
  eval/calibration/calibration_blind.csv   (give this to the labeller: no expected answers)
  eval/calibration/calibration_map.json    (cal-id -> case id. Do NOT open until labelling is done)

Blindness: neutral IDs (cal-01..cal-20), deterministic shuffle, and none of the expected
outcome, citations, approvers, tool calls, attack type or difficulty fields are included.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "eval" / "calibration"

HEADER = [
    "cal_id", "requester_name", "requester_title", "requester_department", "requester_manager",
    "ticket_subject", "ticket_body",
    "YOUR_outcome (resolve | escalate | refuse | ask_clarification | not_enough_evidence | out_of_scope)",
    "YOUR_actions (tools to call, who to approve, which team to escalate to)",
    "YOUR_citations (policy section IDs, e.g. POL-ACC-4.1)",
    "YOUR_notes",
]


def main() -> None:
    cases = [json.loads(line) for line in (ROOT / "eval" / "cases" / "cases.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    people = {p["upn"]: p for p in json.loads((ROOT / "data" / "fixtures" / "people.json").read_text(encoding="utf-8"))}
    cal = [c for c in cases if c["calibration"]]
    cal.sort(key=lambda c: hashlib.sha256(("cal-shuffle|" + c["id"]).encode()).hexdigest())
    OUT.mkdir(parents=True, exist_ok=True)
    mapping = {}
    with open(OUT / "calibration_blind.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(HEADER)
        for i, c in enumerate(cal, start=1):
            cid = f"cal-{i:02d}"
            mapping[cid] = c["id"]
            p = people[c["requester"]]
            mgr = people.get(p.get("managerUpn") or "", {}).get("displayName", "")
            w.writerow([cid, p["displayName"], p["jobTitle"], p["department"], mgr, c["subject"], c["body"], "", "", "", ""])
    (OUT / "calibration_map.json").write_text(json.dumps(mapping, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {len(cal)} blind calibration rows")


if __name__ == "__main__":
    main()
