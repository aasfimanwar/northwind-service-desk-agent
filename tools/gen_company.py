"""Deterministic generator for the bulk Northwind synthetic company data.

Run: python tools/gen_company.py
Writes data/generated/*.jsonl and data/MANIFEST.json (record counts + SHA-256 per file).

Design notes
- Standard library only. Randomness comes from SHA-256 (not the 'random' module), so the
  output is identical on every platform and Python version. Output files use LF newlines.
- The hand-authored fixtures in data/fixtures are NOT regenerated here; the eval cases
  reference those. This script only creates the bulk population around them.
- Total headcount target is read from data/fixtures/company.json (12,000 staff).
"""
import hashlib
import json
import unicodedata
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "data" / "fixtures"
GEN = ROOT / "data" / "generated"
SEED = "northwind-v1"
NS = uuid.UUID("6f1c2d3e-4a5b-4c6d-8e7f-a1b2c3d4e5f6")
DOMAIN = "northwind.example"


class DRand:
    """Deterministic pseudo-random stream built on SHA-256."""

    def __init__(self, seed: str) -> None:
        self.seed = seed.encode()
        self.counter = 0
        self.buf = b""
        self.pos = 0

    def u32(self) -> int:
        if self.pos + 4 > len(self.buf):
            self.buf = hashlib.sha256(self.seed + self.counter.to_bytes(8, "big")).digest()
            self.counter += 1
            self.pos = 0
        v = int.from_bytes(self.buf[self.pos:self.pos + 4], "big")
        self.pos += 4
        return v

    def below(self, n: int) -> int:
        return self.u32() % n

    def choice(self, seq):
        return seq[self.below(len(seq))]

    def weighted(self, items):
        total = sum(w for _, w in items)
        r = self.below(total)
        for value, w in items:
            if r < w:
                return value
            r -= w
        return items[-1][0]


def gid(key: str) -> str:
    return str(uuid.uuid5(NS, key))


def ascii_slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return "".join(ch for ch in s.lower() if ch.isalnum())


NAMES = {
    "GB": (
        "Oliver George Harry Noah Jack Leo Arthur Oscar Charlie Henry Freddie Archie Theo Alfie Joshua Thomas Logan Lucas Daniel Joseph Edward Samuel Max Isaac Finley Ethan Harrison Callum Rhys Dylan Euan Fraser Ewan Liam Connor Ryan Aaron Luke Adam Olivia Amelia Isla Ava Mia Ivy Lily Freya Florence Willow Grace Sophie Ella Evie Rosie Poppy Ruby Charlotte Emily Millie Imogen Hannah Chloe Phoebe Daisy Lucy Holly Eilidh Niamh Catriona Megan Bethan Carys Jessica Lauren Katie Beth Zara Layla Sienna Maisie Esme Heidi Erin".split(),
        "Smith Jones Taylor Brown Williams Wilson Johnson Davies Robinson Wright Thompson Evans Walker White Roberts Green Hall Wood Jackson Clarke Patel Khan Ahmed Hussain Ali Singh Begum Shah Mitchell Cooper Hughes Edwards Turner Phillips Hill Moore Ward Morris Baker King Harrison Lee Allen Scott Young Carter Bennett Cook Murphy Kelly Bailey Collins Gray Richardson Marshall Fraser Campbell Stewart Murray Reid Graham MacDonald Robertson Henderson Grant Ross Morgan Griffiths Owen Rees Pritchard Lloyd Price Watson Palmer Hunt Ellis Webb Fox Barnes Fisher Holmes Knight Lawson Mason Nash Parker Pearce Simpson Shaw Stevens Tucker Vaughan Warren Whitehead Woods Yates Dixon Hayes Burton Fletcher Gibson".split(),
    ),
    "IE": (
        "Cian Sean Conor Darragh Oisin Fionn Eoin Padraig Niall Declan Ciaran Colm Aoife Siobhan Niamh Saoirse Ciara Roisin Orla Grainne Aisling Sinead Maeve Clodagh".split(),
        "Murphy Kelly Byrne Ryan Walsh OBrien Doyle McCarthy Gallagher Doherty Kennedy Lynch Murray Quinn Moore McLoughlin Carroll Connolly Daly Brennan Burke Collins Healy Flynn Nolan Fitzgerald".split(),
    ),
    "DE": (
        "Lukas Felix Jonas Leon Maximilian Paul Elias Noah Finn Tim Jan Niklas Sophie Marie Emma Hannah Anna Lea Mia Laura Julia Katharina Johanna Clara Lena".split(),
        "Mueller Schmidt Schneider Fischer Weber Meyer Wagner Becker Schulz Hoffmann Koch Richter Klein Wolf Neumann Schwarz Zimmermann Braun Krueger Hofmann Hartmann Lange Werner Krause Lehmann".split(),
    ),
    "IN": (
        "Aarav Vivaan Aditya Arjun Rohan Karthik Vikram Rahul Siddharth Nikhil Amit Sandeep Priya Ananya Diya Kavya Meera Neha Pooja Riya Shreya Sneha Divya Lakshmi Anjali".split(),
        "Sharma Verma Iyer Nair Reddy Rao Menon Pillai Kulkarni Joshi Desai Patil Gupta Agarwal Banerjee Chatterjee Das Bose Singh Kapoor Malhotra Bhatt Chopra Saxena Naidu".split(),
    ),
    "US": (
        "James Michael Robert John David William Richard Joseph Thomas Daniel Matthew Anthony Mark Steven Andrew Mary Patricia Jennifer Linda Elizabeth Barbara Susan Jessica Sarah Karen Nancy Lisa".split(),
        "Johnson Anderson Thomas Jackson Martin Thompson Garcia Martinez Robinson Clark Rodriguez Lewis Walker Hall Allen Young Hernandez King Wright Lopez Hill Scott Green Adams Baker Nelson".split(),
    ),
}

LOCATIONS = {
    "GB": [("London", 30), ("Birmingham", 20), ("Manchester", 15), ("Leeds", 12), ("Bristol", 10), ("Glasgow", 13)],
    "IN": [("Pune", 60), ("Bengaluru", 40)],
    "DE": [("Frankfurt", 60), ("Munich", 40)],
    "US": [("Chicago", 55), ("Austin", 45)],
    "IE": [("Dublin", 100)],
}

DEPARTMENTS = [
    ("Engineering", 28), ("Customer Support", 14), ("Sales", 14), ("Operations", 12), ("Finance", 7),
    ("IT Services", 6), ("Marketing", 5), ("People", 4), ("Legal and Compliance", 3), ("Procurement", 3),
    ("Product", 3), ("Internal Audit", 1),
]

TITLES = {
    "Engineering": ["Software Engineer", "Senior Software Engineer", "QA Engineer", "DevOps Engineer", "Data Engineer"],
    "Customer Support": ["Support Agent", "Senior Support Agent", "Support Specialist"],
    "Sales": ["Sales Executive", "Account Executive", "Sales Operations Analyst", "Business Development Rep"],
    "Operations": ["Operations Analyst", "Logistics Coordinator", "Process Analyst", "Operations Coordinator"],
    "Finance": ["Finance Analyst", "Accounts Payable Clerk", "Financial Accountant", "Payroll Specialist"],
    "IT Services": ["Service Desk Analyst", "Systems Engineer", "Network Engineer", "IT Support Technician"],
    "Marketing": ["Marketing Executive", "Content Designer", "Digital Marketing Specialist"],
    "People": ["HR Advisor", "Talent Partner", "Learning Specialist"],
    "Legal and Compliance": ["Compliance Analyst", "Paralegal", "Legal Counsel"],
    "Procurement": ["Procurement Specialist", "Category Analyst", "Supplier Coordinator"],
    "Product": ["Product Manager", "Product Analyst", "UX Designer"],
    "Internal Audit": ["Audit Analyst", "Senior Auditor"],
}

APPS = (
    "Salesforce-Lite Workday-Lite ServiceDesk-Portal Expense-Portal Contract-Repo Billing-System Data-Warehouse BI-Dashboards Code-Repo CI-Pipeline Artifact-Store Monitoring Logging Ticketing Knowledge-Base HR-Portal Learning-Portal Travel-Booking Asset-Register Risk-Register Vendor-Portal Customer-Portal Pricing-Tool Forecasting-Tool Marketing-Automation Design-Library Survey-Tool Meeting-Rooms Fleet-Tracker Warehouse-Mgmt Support-Chat Document-Signing Audit-Tracker Policy-Library Payroll-Reports Time-Tracking Inventory Procurement-Portal Compliance-Tracker Release-Calendar"
).split()

CODENAMES = (
    "Aurora Basalt Cedar Delta Ember Falcon Garnet Harbor Indigo Juniper Kestrel Lagoon Meridian Nimbus Onyx Pinnacle Quartz Raven Summit Tundra Umber Vertex Willow Xenon Yarrow Zenith "
    "Amber Birch Cobalt Dune Elm Fjord Glacier Heron Iris Jasper Kite Linden Marlin Nova Orchid Pebble Quill Reef Sable Thistle Ursa Violet Wren Yew Zephyr "
    "Anchor Beacon Canyon Drift Echo Flint Grove Haven Isle Jetty Knoll Ledge Moor Nest Oasis Pier Quay Ridge Shoal Trail Vale Wharf Atlas Borealis Cascade Dawn"
).split()


def main() -> None:
    GEN.mkdir(parents=True, exist_ok=True)
    company = json.loads((FIX / "company.json").read_text(encoding="utf-8"))
    people_fx = json.loads((FIX / "people.json").read_text(encoding="utf-8"))
    now_year = 2026
    rnd = DRand(SEED)

    fixture_upns = {p["upn"] for p in people_fx}
    fixture_staff = [p for p in people_fx if p["userType"] != "Guest"]
    fixture_by_country: dict[str, int] = {}
    for p in fixture_staff:
        fixture_by_country[p["country"]] = fixture_by_country.get(p["country"], 0) + 1

    # headcount per country for generated users
    to_make = {cc: n - fixture_by_country.get(cc, 0) for cc, n in company["countries"].items()}

    used_upns = set(fixture_upns)
    users = []
    counter = 0
    # build a flat list of (country) then assign dept/location
    for cc in sorted(to_make):
        for _ in range(to_make[cc]):
            counter += 1
            first = rnd.choice(NAMES[cc][0])
            last = rnd.choice(NAMES[cc][1])
            base = f"{ascii_slug(first)}.{ascii_slug(last)}"
            local, k = base, 1
            while f"{local}@{DOMAIN}" in used_upns:
                k += 1
                local = f"{base}{k}"
            upn = f"{local}@{DOMAIN}"
            used_upns.add(upn)
            users.append({
                "_cc": cc,
                "upn": upn,
                "displayName": f"{first} {last}",
                "country": cc,
                "department": rnd.weighted(DEPARTMENTS),
                "officeLocation": rnd.weighted(LOCATIONS[cc]),
            })

    # buckets by (department, country) for the management layers
    buckets: dict[tuple, list] = {}
    for u in users:
        buckets.setdefault((u["department"], u["country"]), []).append(u)

    heads: dict[str, dict] = {}
    for dept, _ in DEPARTMENTS:
        gb = buckets.get((dept, "GB"), [])
        if gb:
            heads[dept] = gb[0]

    ceo = "amanda.sterling@" + DOMAIN
    n_user = 0
    for key in sorted(buckets):
        dept, cc = key
        b = buckets[key]
        head = heads.get(dept)
        for i, u in enumerate(b):
            mi = i // 10
            si = mi // 8
            if u is head:
                node, mgr_upn = "head", ceo
            elif i % 10 != 0:
                node, mgr_upn = "staff", b[(i // 10) * 10]["upn"]
            elif mi % 8 != 0:
                node, mgr_upn = "manager", b[(mi // 8) * 80]["upn"]
            elif si % 8 != 0:
                node, mgr_upn = "senior", b[(si // 8) * 640]["upn"]
            else:
                node, mgr_upn = "director", (head["upn"] if head else ceo)
            u["_node"] = node
            u["managerUpn"] = mgr_upn

    out_users = []
    for u in users:
        n_user += 1
        node = u["_node"]
        titles = TITLES[u["department"]]
        if node == "head":
            title, band = f"Head of {u['department']}", "L8"
        elif node == "director":
            title, band = f"Director, {u['department']} ({u['country']})", "L7"
        elif node == "senior":
            title, band = f"Senior Manager, {u['department']}", "L7"
        elif node == "manager":
            title, band = f"{u['department']} Manager", "L6"
        else:
            title, band = rnd.choice(titles), rnd.choice(["L2", "L3", "L3", "L4", "L4", "L5"])
        contractor = node == "staff" and rnd.below(100) < 3
        rec = {
            "id": gid(u["upn"]),
            "upn": u["upn"],
            "displayName": u["displayName"],
            "jobTitle": title + (" (contractor)" if contractor else ""),
            "department": u["department"],
            "officeLocation": u["officeLocation"],
            "country": u["country"],
            "managerUpn": u["managerUpn"],
            "userType": "Contractor" if contractor else "Employee",
            "band": "C1" if contractor else band,
            "employeeId": f"NW{10000 + n_user}",
            "accountEnabled": True,
            "fixture": False,
        }
        if contractor:
            rec["sponsorUpn"] = u["managerUpn"]
            rec["agency"] = rnd.choice(["Brightpath Staffing", "Keystone Resourcing", "Larkfield Talent"])
            rec["contractEnd"] = f"{now_year + 1}-{rnd.choice(['01', '02', '03', '04', '05'])}-{rnd.choice(['15', '28'])}"
        out_users.append(rec)

    # devices
    devices = []
    comp_w = [("compliant", 9300), ("os_update_overdue", 250), ("encryption_disabled", 120), ("no_recent_check_in", 180), ("endpoint_protection_signatures_stale", 100)]
    for rec in out_users:
        mac = rec["department"] in ("Marketing", "Product", "Engineering") and rnd.below(100) < 35
        plat = "macOS" if mac else "Windows"
        name = f"NW-{'MB' if mac else 'LT'}-{rec['employeeId']}"
        managed = "agency_owned_not_enrolled" if rec["userType"] == "Contractor" and rnd.below(100) < 40 else "corporate"
        d = {"id": gid("device:" + name), "deviceName": name, "ownerUpn": rec["upn"], "platform": plat, "fixture": False, "managed": managed,
             "osUpdatePendingDays": rnd.below(10), "encryption": True, "defenderSignatureAgeDays": rnd.below(4), "lastCheckInDays": rnd.below(3), "jailbroken": False}
        if managed != "corporate":
            d.update({"complianceState": "unmanaged", "nonComplianceReasons": ["device_not_enrolled"], "lastCheckInDays": None})
        else:
            reason = rnd.weighted(comp_w)
            if reason == "compliant":
                d["complianceState"] = "compliant"
            else:
                d["complianceState"] = "noncompliant"
                d["nonComplianceReasons"] = [reason]
                if reason == "os_update_overdue":
                    d["osUpdatePendingDays"] = 31 + rnd.below(40)
                elif reason == "encryption_disabled":
                    d["encryption"] = False
                elif reason == "no_recent_check_in":
                    d["lastCheckInDays"] = 31 + rnd.below(30)
                else:
                    d["defenderSignatureAgeDays"] = 8 + rnd.below(10)
        devices.append(d)
        if rnd.below(100) < 65:
            ios = rnd.below(100) < 60
            mname = f"NW-MOB-{rec['employeeId']}"
            md = {"id": gid("device:" + mname), "deviceName": mname, "ownerUpn": rec["upn"], "platform": "iOS" if ios else "Android", "fixture": False,
                  "managed": "corporate", "osUpdatePendingDays": rnd.below(8), "encryption": True, "lastCheckInDays": rnd.below(3), "jailbroken": False,
                  "complianceState": "compliant"}
            if rnd.below(1000) < 12:
                md["complianceState"] = "noncompliant"
                md["jailbroken"] = True
                md["nonComplianceReasons"] = ["rooted_device"]
            devices.append(md)

    # managers pool per department for group/site owners
    mgr_pool: dict[str, list] = {}
    for rec in out_users:
        if rec["band"] in ("L6", "L7"):
            mgr_pool.setdefault(rec["department"], []).append(rec["upn"])

    def owner_for(dept: str) -> str:
        pool = mgr_pool.get(dept) or [ceo]
        return rnd.choice(pool)

    # groups
    groups, memberships = [], []
    for dept, _ in DEPARTMENTS:
        groups.append({"id": gid("group:dyn:" + dept), "displayName": f"SG-Dyn-Dept-{ascii_slug(dept).upper()}", "groupType": "dynamic", "classification": "Internal",
                       "owners": [], "membershipRule": f"user.department -eq \"{dept}\"", "requestableViaServiceDesk": False, "fixture": False})
    for cc, locs in sorted(LOCATIONS.items()):
        for loc, _ in locs:
            groups.append({"id": gid("group:loc:" + loc), "displayName": f"SG-Dyn-Loc-{ascii_slug(loc).upper()}", "groupType": "dynamic", "classification": "Internal",
                           "owners": [], "membershipRule": f"user.officeLocation -eq \"{loc}\"", "requestableViaServiceDesk": False, "fixture": False})
    by_dept: dict[str, list] = {}
    for rec in out_users:
        by_dept.setdefault(rec["department"], []).append(rec["upn"])
    for app in APPS:
        dept = rnd.choice([d for d, _ in DEPARTMENTS])
        cls = rnd.weighted([("Internal", 70), ("Confidential", 25), ("Restricted", 5)])
        name = f"SG-App-{app}-Users"
        owner = owner_for(dept)
        groups.append({"id": gid("group:" + name), "displayName": name, "groupType": "security", "classification": cls, "owners": [owner],
                       "requestableViaServiceDesk": True, "description": f"Access to {app}", "fixture": False})
        pool = by_dept[dept]
        for _ in range(60 + rnd.below(240)):
            memberships.append({"group": name, "upn": rnd.choice(pool)})
    for code in CODENAMES:
        dept = rnd.choice([d for d, _ in DEPARTMENTS])
        name = f"M365-Proj-{code}"
        owner = owner_for(dept)
        groups.append({"id": gid("group:" + name), "displayName": name, "groupType": "m365", "classification": "Internal", "owners": [owner],
                       "requestableViaServiceDesk": True, "description": f"Project {code} Team", "fixture": False})
        pool = by_dept[dept]
        for _ in range(8 + rnd.below(40)):
            memberships.append({"group": name, "upn": rnd.choice(pool)})
    # remove duplicate membership rows deterministically
    seen = set()
    uniq = []
    for m in memberships:
        k = (m["group"], m["upn"])
        if k not in seen:
            seen.add(k)
            uniq.append(m)
    memberships = uniq

    # sites
    sites = []
    for dept, _ in DEPARTMENTS:
        sites.append({"id": gid("site:dept:" + dept), "name": f"Dept-{ascii_slug(dept)}", "sensitivityLabel": "Internal", "externalSharing": "Disabled", "owners": [owner_for(dept)], "fixture": False})
    for code in CODENAMES:
        label = rnd.weighted([("Internal", 80), ("Confidential", 15), ("Restricted", 5)])
        sharing = "Disabled" if label == "Restricted" else rnd.weighted([("Disabled", 40), ("ExistingGuests", 35), ("NewAndExistingGuests", 25)])
        dept = rnd.choice([d for d, _ in DEPARTMENTS])
        sites.append({"id": gid("site:proj:" + code), "name": f"Proj-{code}", "sensitivityLabel": label, "externalSharing": sharing, "owners": [owner_for(dept)], "fixture": False})

    # HR records for generated users
    hr = []
    for rec in out_users:
        year = 2012 + rnd.below(14)
        month = 1 + rnd.below(12)
        day = 1 + rnd.below(28)
        hr.append({"upn": rec["upn"], "status": "active", "startDate": f"{year}-{month:02d}-{day:02d}", "jobFamily": rec["department"][:3].upper(), "trainingComplete": True, "legalHold": False})

    files = {
        "users.jsonl": out_users,
        "devices.jsonl": devices,
        "groups.jsonl": groups,
        "memberships.jsonl": memberships,
        "sites.jsonl": sites,
        "hr_records.jsonl": hr,
    }
    manifest = {"generator": "tools/gen_company.py", "seed": SEED, "files": {}}
    for fname, rows in files.items():
        data = "".join(json.dumps(r, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n" for r in rows)
        (GEN / fname).write_bytes(data.encode("utf-8"))
        manifest["files"][fname] = {"records": len(rows), "sha256": hashlib.sha256(data.encode("utf-8")).hexdigest()}
    total_staff = len(out_users) + len(fixture_staff)
    manifest["totals"] = {"generated_users": len(out_users), "fixture_staff": len(fixture_staff), "total_staff": total_staff}
    (ROOT / "data" / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(manifest["totals"]))
    for f, v in manifest["files"].items():
        print(f, v["records"], v["sha256"][:16])


if __name__ == "__main__":
    main()
