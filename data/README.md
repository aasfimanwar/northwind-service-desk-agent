# Synthetic company data

Northwind Ltd is fictional. Domain `northwind.example` (reserved TLD). Synthetic clock: 2026-12-01T09:00:00Z.

- `fixtures/`: hand-authored people, groups, sites, devices, sign-in events, HR overrides and known tickets that the eval cases rely on.
- `generated/`: about 12,000 staff of bulk population, built by `python tools/gen_company.py`. Not committed (gitignored).
- `MANIFEST.json`: record counts and SHA-256 per generated file. CI regenerates the data and fails if a hash differs, which proves the generator is deterministic across machines.

The generator uses SHA-256 as its random source and writes LF newlines, so output does not depend on Python version or operating system.

Known simplifications: manager chains are layered by bucket (department and country) rather than modelled on a real org; generated devices and sign-ins are not used by the eval cases.
