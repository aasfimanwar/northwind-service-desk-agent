"""Validate Phase 1a artefacts. Exit code 1 if any check fails.

Run: python tools/validate_phase1a.py
Run tools/gen_company.py first so data/generated exists.
Checks: policy section IDs, fixture integrity, generated data integrity (unique UPNs,
manager chains, no cycles, 12,000 staff), case references (requesters, citations,
approvers, tools, teams, groups, sites, devices) and category / calibration counts.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def load_jsonl(p: Path):
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


READ_TOOLS = {"lookup_user", "get_manager_chain", "lookup_group", "get_group_owners", "list_group_members", "lookup_site", "get_site_sharing",
              "get_device_compliance", "get_signin_events", "get_hr_record", "get_ticket", "search_policies"}
PROPOSE_TOOLS = {"request_group_add", "request_guest_invite", "request_guest_renewal", "request_external_share", "request_leaver_onedrive_access",
                 "start_onboarding_checklist", "start_offboarding_checklist"}
ESCALATE = {"escalate"}
NEVER_EXPOSED = {"execute_approved_request", "reset_mfa", "issue_tap", "reset_password", "remote_wipe", "disable_account", "set_site_sharing", "relabel_content",
                 "delete_mailbox", "delete_onedrive", "delete_ticket"}
TEAMS = {"it_security", "security_operations", "service_desk_l2", "endpoint_engineering", "people_team", "legal", "policy_office"}
OUTCOMES = {"resolve", "escalate", "refuse", "ask_clarification", "not_enough_evidence", "out_of_scope"}
CATEGORIES = {"answerable_policy": 22, "access_request": 14, "unauthorised_request": 12, "ambiguous": 10, "adversarial_ticket": 14, "out_of_scope": 8}
ROLES = {"role:it_security_approver"}


def main() -> int:
    # --- policies
    sections: set[str] = set()
    for f in sorted((ROOT / "policies").glob("POL-*.md")):
        for m in re.finditer(r"^### (POL-[A-Z]+-[0-9.]+)\b", f.read_text(encoding="utf-8"), re.M):
            if m.group(1) in sections:
                err(f"duplicate policy section {m.group(1)}")
            sections.add(m.group(1))
    print(f"policy documents: {len(list((ROOT / 'policies').glob('POL-*.md')))}, sections: {len(sections)}")

    # --- fixtures
    fx = ROOT / "data" / "fixtures"
    people = json.loads((fx / "people.json").read_text(encoding="utf-8"))
    groups = json.loads((fx / "groups.json").read_text(encoding="utf-8"))
    sites = json.loads((fx / "sites.json").read_text(encoding="utf-8"))
    devices = json.loads((fx / "devices.json").read_text(encoding="utf-8"))
    signins = json.loads((fx / "signins.json").read_text(encoding="utf-8"))
    hr = json.loads((fx / "hr_overrides.json").read_text(encoding="utf-8"))
    tickets = json.loads((fx / "known_tickets.json").read_text(encoding="utf-8"))
    company = json.loads((fx / "company.json").read_text(encoding="utf-8"))
    upns = {p["upn"] for p in people}
    if len(upns) != len(people):
        err("duplicate fixture UPNs")
    for p in people:
        if p.get("managerUpn") and p["managerUpn"] not in upns:
            err(f"fixture manager missing: {p['upn']} -> {p['managerUpn']}")
        if p.get("sponsorUpn") and p["sponsorUpn"] not in upns:
            err(f"fixture sponsor missing: {p['upn']}")
    gnames = {g["displayName"] for g in groups}
    for g in groups:
        for u in g["owners"] + g["members"]:
            if u not in upns:
                err(f"group {g['displayName']} references unknown user {u}")
    snames = {s["name"] for s in sites}
    for s in sites:
        for u in s["owners"]:
            if u not in upns:
                err(f"site {s['name']} owner unknown {u}")
    dnames = {d["deviceName"] for d in devices}
    for d in devices:
        if d["ownerUpn"] not in upns:
            err(f"device {d['deviceName']} owner unknown")
    for s in signins:
        if s["userUpn"] not in upns or s["device"] not in dnames:
            err(f"signin {s['id']} references unknown user or device")
    for u in hr:
        if u not in upns:
            err(f"HR override for unknown user {u}")
    print(f"fixtures: {len(people)} people, {len(groups)} groups, {len(sites)} sites, {len(devices)} devices, {len(signins)} sign-ins, {len(hr)} HR overrides")

    # --- generated
    gen = ROOT / "data" / "generated"
    if not (gen / "users.jsonl").exists():
        err("data/generated missing: run tools/gen_company.py")
        users = []
    else:
        users = load_jsonl(gen / "users.jsonl")
        gdevs = load_jsonl(gen / "devices.jsonl")
        ggroups = load_jsonl(gen / "groups.jsonl")
        gmem = load_jsonl(gen / "memberships.jsonl")
        gsites = load_jsonl(gen / "sites.jsonl")
        ghr = load_jsonl(gen / "hr_records.jsonl")
        all_upns = set(upns)
        by_upn = {p["upn"]: p for p in people}
        for u in users:
            if u["upn"] in all_upns:
                err(f"duplicate UPN {u['upn']}")
            all_upns.add(u["upn"])
            by_upn[u["upn"]] = u
        staff = [p for p in people if p["userType"] != "Guest"] + users
        if len(staff) != company["headcountTarget"]:
            err(f"staff total {len(staff)} != {company['headcountTarget']}")
        cc = Counter(p["country"] for p in staff)
        for c, n in company["countries"].items():
            if cc[c] != n:
                err(f"country {c}: {cc[c]} != {n}")
        for u in users:
            m = u["managerUpn"]
            if m not in all_upns:
                err(f"unknown manager {m} for {u['upn']}")
        depth_max = 0
        for u in staff:
            seen, cur, depth = set(), u["upn"], 0
            while by_upn[cur].get("managerUpn"):
                if cur in seen:
                    err(f"manager cycle at {u['upn']}")
                    break
                seen.add(cur)
                cur = by_upn[cur]["managerUpn"]
                depth += 1
                if depth > 12:
                    err(f"manager chain too deep for {u['upn']}")
                    break
            else:
                if cur != "amanda.sterling@northwind.example":
                    err(f"chain for {u['upn']} does not end at the CEO ({cur})")
            depth_max = max(depth_max, depth)
        for d in gdevs:
            if d["ownerUpn"] not in all_upns:
                err(f"device {d['deviceName']} owner unknown")
        gnames_all = gnames | {g["displayName"] for g in ggroups}
        for m in gmem:
            if m["group"] not in gnames_all or m["upn"] not in all_upns:
                err(f"bad membership {m}")
        for g in ggroups:
            for o in g["owners"]:
                if o not in all_upns:
                    err(f"group owner unknown {o}")
        for s in gsites:
            for o in s["owners"]:
                if o not in all_upns:
                    err(f"site owner unknown {o}")
        if len(ghr) != len(users):
            err("HR record count mismatch")
        print(f"generated: {len(users)} users, {len(gdevs)} devices, {len(ggroups)} groups, {len(gmem)} memberships, {len(gsites)} sites; total staff {len(staff)}; max manager depth {depth_max}")

    # --- cases
    cases = load_jsonl(ROOT / "eval" / "cases" / "cases.jsonl")
    ids = [c["id"] for c in cases]
    if len(set(ids)) != len(ids):
        err("duplicate case ids")
    cat_counts = Counter(c["category"] for c in cases)
    if len(cases) != 80:
        err(f"expected 80 cases, found {len(cases)}")
    for k, v in CATEGORIES.items():
        if cat_counts[k] != v:
            err(f"category {k}: {cat_counts[k]} != {v}")
    cal = [c for c in cases if c["calibration"]]
    if len(cal) != 20:
        err(f"calibration cases {len(cal)} != 20")
    known_ticket_ids = {t["id"] for t in tickets}
    all_tool_names = READ_TOOLS | PROPOSE_TOOLS | ESCALATE | NEVER_EXPOSED
    for c in cases:
        cid = c["id"]
        if c["requester"] not in upns:
            err(f"{cid}: unknown requester {c['requester']}")
        if c["expected_outcome"] not in OUTCOMES:
            err(f"{cid}: bad outcome")
        if not c["body"].strip() or not c["subject"].strip():
            err(f"{cid}: empty ticket")
        for s in c["required_citations"]:
            if s not in sections:
                err(f"{cid}: unknown citation {s}")
        for a in c["required_approvers"]:
            if a not in upns and a not in ROLES:
                err(f"{cid}: unknown approver {a}")
        for t in c["required_tool_calls"] + c["allowed_tool_calls"] + [x for x in c["forbidden_tool_calls"] if isinstance(x, dict)]:
            if t["tool"] not in all_tool_names:
                err(f"{cid}: unknown tool {t['tool']}")
            args = t.get("args", {})
            if t["tool"] == "escalate" and args.get("team") not in TEAMS:
                err(f"{cid}: unknown team {args.get('team')}")
            if "group" in args and args["group"] not in gnames:
                err(f"{cid}: unknown group {args['group']}")
            if "site" in args and args["site"] not in snames:
                err(f"{cid}: unknown site {args['site']}")
            if "device" in args and args["device"] not in dnames:
                err(f"{cid}: unknown device {args['device']}")
            for key in ("user", "leaver", "manager", "sponsor"):
                if key in args and args[key] not in upns:
                    err(f"{cid}: unknown user {args[key]} in args")
            if t["tool"] == "get_ticket" and args["id"] not in known_ticket_ids and cid != "adv-11":
                err(f"{cid}: ticket id not known")
        for t in c["forbidden_tool_calls"]:
            name = t["tool"] if isinstance(t, dict) else t
            if name not in all_tool_names:
                err(f"{cid}: unknown forbidden tool {name}")
        if c["category"] == "adversarial_ticket" and not c["injection"]:
            err(f"{cid}: adversarial case without injection field")
        if c["category"] != "adversarial_ticket" and c["injection"]:
            err(f"{cid}: non-adversarial case with injection field")
        if c["expected_outcome"] == "resolve" and c["category"] == "access_request" and not c["required_tool_calls"]:
            err(f"{cid}: resolve access request without a required tool call")
        if c["required_tool_calls"] and any(t["tool"] in PROPOSE_TOOLS for t in c["required_tool_calls"]) and not c["required_approvers"]:
            err(f"{cid}: propose tool without required approvers")
    print(f"cases: {len(cases)}  by category: {dict(cat_counts)}  calibration: {len(cal)} {dict(Counter(c['category'] for c in cal))}")
    print(f"cases citing policy sections: {sum(1 for c in cases if c['required_citations'])}; distinct sections cited: {len({s for c in cases for s in c['required_citations']})}")

    if errors:
        print(f"\nFAILED: {len(errors)} problem(s)")
        for e in errors[:50]:
            print(" -", e)
        return 1
    print("\nAll Phase 1a checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
