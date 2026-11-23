# DECISIONS (Architecture Decision Records)

Project: northwind-service-desk-agent
Status key: Accepted = given by the owner; Proposed = awaiting the owner's confirmation.

---

## ADR-0001: Build Path B (free, local, Microsoft Agent Framework)

- **Date:** 2026-11-22
- **Status:** Accepted (owner confirmed Path B on 2026-11-22)
- **Context:** Phase 0 documentation research (read 2026-11-16) found:
  - Copilot Studio trial needs a work or school account; personal accounts are not accepted.
  - Microsoft 365 Business trials require a credit card and convert to paid after 30 days.
  - The Microsoft 365 Developer Program sandbox needs a billing account and is limited to
    specific subscriber or partner categories.
  - Power Apps Developer Plan (Power Automate approvals) needs a work or school account.
  - Azure free account needs a phone number and a non-prepaid card; credit lasts 30 days.
  - Azure for Students needs current-student academic email verification; university
    credentials cannot be used for this project.
  - Foundry Agent Service itself has no extra charge, but model tokens and tools are billed
    and an Azure subscription is required.
  - Microsoft Agent Framework is MIT-licensed, GA (1.0) since 2026-04-03, free to use.
- **Decision:** Path B. Microsoft Agent Framework (Python) + MCP tools + in-repo mock
  Microsoft Graph server + local web chat UI. A PLATFORM-MAPPING document lists which
  Copilot Studio / Foundry features each component corresponds to and what was NOT built.
- **Rejected alternatives:**
  - Path A (Copilot Studio trial tenant + Power Automate + Foundry agent): no documented
    route that is both free and card-free for this owner; card-required steps need separate
    explicit approval with a cancel date, and none has been approved.
  - Hybrid (Path B now, Path A later): not rejected permanently; revisit only if the owner
    approves a specific card-required step.
- **Consequences:** Resume wording is limited to "built with Microsoft Agent Framework".
  Copilot Studio, Foundry and Power Automate are not claimed. Gemini/Groq compatibility with
  the framework's model clients is unverified and must be proven by a spike (ADR-0010).

## ADR-0002: Build lean mock Graph server and eval module inside this repo

- **Date:** 2026-11-22
- **Status:** Accepted
- **Context:** Projects 1 (mock Graph server) and 5 (eval harness) do not exist yet.
- **Decision:** Build minimal versions inside this repo, behind clean interfaces:
  - mock Microsoft Graph server covering only the endpoints this project uses, shaped
    like the real Graph API;
  - small eval module: dataset loader, split tool with lock file, metrics, record/replay,
    paired bootstrap, requests-per-day tracker.
- **Rejected alternatives:** cross-repo dependency; waiting for Projects 1 and 5.
- **Consequences:** Phase 1 is split into 1a (corpus, data, 80-case suite) and 1b (mock
  Graph, mini harness). Each sub-phase ends with a stop for approval. Modules stay
  swappable later, with no cross-repo dependency.

## ADR-0003: Retrieval starts with BM25 (SQLite FTS5)

- **Date:** 2026-11-22
- **Status:** Accepted
- **Decision:** BM25 over the small synthetic policy corpus using SQLite FTS5. A small
  local reranker or a bge-small embedding model is added only as an ablation and kept only
  if measured results justify it.
- **Rejected alternatives:** API embeddings (quota cost, request-limit pressure).

## ADR-0004: "Zero unauthorised actions" is enforced by a deterministic policy gate

- **Date:** 2026-11-22
- **Status:** Accepted
- **Decision:** The guarantee lives in tool-layer code, not in the prompt. Property-style
  tests attempt to bypass the gate.
- **Rejected alternatives:** prompt-only enforcement.

## ADR-0005: Locked test set, extension set for later fixes

- **Date:** 2026-11-22
- **Status:** Accepted
- **Decision:** The ~30% test split is locked (lock file) until the final report and used
  once. If Phase 6 reveals a flawed test case, the locked set is not edited; new cases go
  into a separate extension set, both are reported, and an ADR is logged.
- **Rejected alternatives:** editing the locked set in place.

## ADR-0006: Judge independence and run metadata

- **Date:** 2026-11-22
- **Status:** Accepted
- **Decision:** Generator and judge roles are pinned per run; provider failover is
  disabled during eval runs; roles are recorded in run metadata. The judge must be a
  different model family from the system under test.

## ADR-0007: Cassette (record/replay) policy

- **Date:** 2026-11-22
- **Status:** Accepted
- **Decision:** Cassettes are keyed by a hash of the full request. CI fails on a miss with
  "re-record required". Re-recording is scoped per milestone (end of Phases 2, 4 and 6);
  prompts and tool schemas are frozen before each milestone run.

## ADR-0008: Eval budget against free-tier limits

- **Date:** 2026-11-22
- **Status:** Accepted (owner delegated the token rule to the assistant on 2026-11-22)
- **Decision:**
  - A single eval run may use at most about 25% of each provider's own daily limit, checked
    per provider and per dimension: requests per day, and tokens per day where the provider
    publishes one. The run halts at the first dimension that reaches 25%, checkpoints, and
    resumes the next day. Replays are free.
  - Limits are read from the owner's own accounts (Gemini AI Studio rate-limit page, Groq
    Limits page) and stored in a config file with the read date. Public docs and
    third-party pages are samples only.
  - Pre-flight check: before a live run the harness prints projected requests and tokens,
    computed from averages the tracker has actually measured, and refuses to start a live
    run that projects past the budget unless resume-over-days is selected. No average is
    assumed before it has been measured.
  - Baseline and per-phase runs use the DEV split only. The test split is used once for the
    final report; that single run may span several days.
- **Rationale:** a global "smallest limit across providers" rule would throttle every
  provider to the tightest one. Checking each provider against its own limits keeps the 25%
  intent (leave 75% for debugging and re-recording) without wasting the larger quotas. Token
  limits can bind before request limits in agent loops, so both are tracked.
- **Rejected alternatives:** requests-only rule; one global budget set by the tightest
  provider.
- **Open item:** if the chosen Gemini generator model has a very low daily request cap in
  AI Studio, choose a model with a higher cap or lengthen resume time; log the choice.

## ADR-0009: UI and repo hygiene

- **Date:** 2026-11-22
- **Status:** Accepted
- **Decision:** GitHub username `aasfimanwar`; new public repo `northwind-service-desk-agent`,
  MIT licence, commits with the owner's GitHub noreply email. Minimal FastAPI plus one HTML
  page (no Streamlit or Chainlit). Add
  `.gitattributes` early to normalise line endings to LF. Report peak memory per phase,
  measured, not assumed.

## ADR-0010: Verify Agent Framework model-client support before relying on it

- **Date:** 2026-11-22
- **Status:** Proposed
- **Context:** Phase 0 did not confirm first-party support for Gemini or Groq in the
  framework's model clients; both offer OpenAI-compatible endpoints.
- **Decision:** Run a small spike (Phase 1b or start of Phase 2) behind the project's own
  provider interface. Log the outcome and any stub exceptions needed for mypy --strict.

## ADR-0011: Company scale, setting and corpus shape

- **Date:** 2026-12-01 (synthetic clock) / authored 2026-11-22
- **Status:** Accepted (owner chose about 12,000 staff, UK setting, UK English)
- **Decision:** Fictional UK-headquartered multinational with exactly 12,000 staff (GB 7,200, IN 2,400, DE 900, US 900, IE 600). Hand-authored fixtures (44 staff plus one guest) carry the eval cases; the remaining 11,956 staff are generated. 13 policy documents with stable section IDs (126 sections), including deliberate gaps (leave outside the UK, hotels outside the UK, home-office equipment, sabbaticals) and one deliberate conflict (POL-DEV-3.1 against POL-CA-2.3, resolved by POL-DOC-1.2).
- **Rejected alternatives:** a roughly 120-person company (too easy for retrieval and group-scale effects); generating every person by script (cases need stable, hand-checked facts).
- **Consequences:** policy numbers (25 days leave, 45p/25p mileage and similar) are synthetic and must never be quoted as real policy.

## ADR-0012: Case counts rebalanced inside the six categories

- **Status:** Accepted (assistant's call within the brief; owner may revise at review)
- **Context:** The Phase 1a design proposed 16/16/12/12/14/10. Writing the cases showed that device and lockout diagnostics (which need read-only lookups) belong with answerable cases, and that evidence-gap cases fit best under ambiguous.
- **Decision:** answerable 22, access request 14, unauthorised 12, ambiguous 10, adversarial 14, out of scope 8 (total 80). The brief fixes only the total and the six categories.
- **Consequence:** SharePoint-permission scenarios are thin (4 cases). Flagged for owner review.

## ADR-0013: Calibration cases are forced into DEV; labelling is blind

- **Status:** Accepted
- **Decision:** The 20 calibration cases are always in the DEV split, so judge calibration never uses the locked test set. The owner labels them from `calibration_blind.csv` with neutral IDs (cal-01 to cal-20), shuffled, with no expected answers. The mapping file is opened only after labelling. Agreement between owner and draft labels is measured before the judge is trusted.
- **Rejected alternatives:** calibrating on random cases (risks leaking the test set); showing draft labels first (anchors the labeller).

## ADR-0014: Synthetic clock and deterministic data

- **Status:** Accepted
- **Decision:** The dataset's "now" is 2026-12-01T09:00:00Z for every case and tool, so dates in cases never drift. Bulk data comes from a stdlib-only generator that uses SHA-256 as its random source and LF newlines. The bulk files are gitignored; `data/MANIFEST.json` holds record counts and hashes and CI verifies them.
- **Rejected alternatives:** Python's `random` module (output can differ between Python versions); committing about 12 MB of bulk data.

## ADR-0015: Adversarial cases authored by the assistant

- **Status:** Accepted (owner asked the assistant to generate them, realistic for a UK multinational)
- **Decision:** All 14 adversarial cases are drafted by Claude and flagged `claude-draft` until reviewed. Attack types: direct override, indirect injection inside quoted email, authority impersonation, fake approval, credential social engineering, data exfiltration, prompt extraction, role-play jailbreak, urgency pressure, hidden text in a screenshot, unverifiable cross-ticket claim, parameter smuggling, fake system notice, multilingual override.
- **Risk:** one author means shared blind spots; the owner's review, and adding any cases from real service-desk experience (rephrased and fully synthetic), reduces it.

## ADR-0016: Eval budget option B (milestone allowance)

- **Date:** 2026-11-23
- **Status:** Accepted (owner chose option B)
- **Context:** Groq free-tier limits read on 2026-11-22 (see `config/provider_limits.json`): the strongest candidate chat models allow 1,000 requests, 200,000 tokens, 8,000 tokens per minute and 30 requests per minute per day, per model. At the 25% cap of ADR-0008 that is 250 requests and 50,000 tokens per model per day, about 4.5 requests and about 890 tokens per case for a 56-case dev run. Gemini limits for text models have not yet been found.
- **Decision (amends ADR-0008):**
  - Routine runs: at most 25% of each model's daily limit, per dimension (requests and tokens), as before.
  - Milestone runs (end of Phases 2, 4 and 6, plus the single final test run): up to 60% of each model's daily limit, per dimension. The run still halts at the first dimension that reaches its cap, checkpoints, and resumes the next day.
  - Replays from recorded cassettes are free and unlimited.
  - Design targets, to be checked against measured numbers: about 4 LLM calls per case, top-3 retrieval passages, compact prompts so that every request stays well under the 8,000 tokens-per-minute limit, and the generator and judge on different models (each model has its own daily limit).
  - The pre-flight check of ADR-0008 still applies: no average is assumed before it has been measured.
- **Rejected alternatives:** option A (25% everywhere: dev runs would take days); option C (higher cap everywhere: no headroom for debugging and re-recording).
- **Consequences:** `config/provider_limits.json` gains a milestone fraction of 0.60 in the Phase 1b commit. Limits are re-read before every milestone run.
