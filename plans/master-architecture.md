# Master Architecture — AI Hero Academy
## Competency-Based Learning Infrastructure

> Status: **LIVING DOCUMENT** — updated as architectural decisions are made
> Last updated: 2026-03-24

---

## Vision

> Every employee, regardless of role or job title, receives a personalized AI skills
> training path built from their actual work context — not from which bucket we put them in.

The platform evolves through three content maturity phases. Roles are scaffolding
to bootstrap content, not a permanent architectural constraint.

---

## Three-Phase Content Maturity Model

```
Phase 1 — Role-seeded          Phase 2 — Atomic              Phase 3 — Fully Atomic
(complete)                      (current)                     (target)
──────────────────────          ──────────────────────        ──────────────────────
Roles → content factory         Roles → atom pool             No roles at runtime
Role-specific scenarios         fill_scenario() injects       JD/LinkedIn → intake
Role-gated diagnosis            Diagnosis still broken        Diagnosis fully atomic
Role-gated path                 assemble_path() works         Everything assembled
Hard to extend to               New roles = new atoms         Any job title served
  new roles                       (not new courses)
```

**We are currently transitioning Phase 2 → Phase 3.**

The atom pool and path assembler are Phase 3 infrastructure.
The diagnostic and intake are Phase 1 holdouts.

---

## What "Competency-Based" Means Here

The unit of delivery is a **skill behavior**, not a course or a role.

Each atom teaches one observable AI behavior (e.g., "verify AI output before forwarding").
The behavior is universal. The scenario wrapper adapts to the user's context at runtime.
The diagnostic measures whether the user demonstrates the behavior — not whether they
know the right answer for their job title.

This aligns with:
- **McKinsey skills-based workforce approach** (2024): define required skills, not credentials
- **Situational Judgment Test design principles**: competency measured independently of scenario context
- **Holistic AI literacy matrix** (ScienceDirect 2024): generic layer (universal) + domain-specific layer (personalized)

---

## Current State Assessment (2026-03-24)

### What is already Phase 3

| Component | Status | Notes |
|-----------|--------|-------|
| `assemble_path()` | ✅ Fully atomic | Role-agnostic selection by domain score + tag match |
| `fill_scenario()` | ✅ Atomic | Runtime role injection via `{placeholder}` tokens |
| Atom `capability_tags` | ✅ Atomic | Universal behavior keywords, not role-specific |
| Atom `coach_system_prompt_template` | ✅ Atomic | Uses `{role}`, `{organisation}`, `{domain}` — no hardcoding |
| Eval loader (`04_Course_Module.py`) | ✅ Atomic | Inline eval branch added Phase 4 |

### What is still Phase 1 / Phase 2

| Component | Status | Problem |
|-----------|--------|---------|
| `diagnostic_items.json` | ❌ Phase 1 | `role_id`-gated + hardcoded `scenario_text` |
| `01_Diagnostic.py` | ❌ Phase 1 | Loads items by `role_id`; invalid for unknown roles |
| `00_Welcome.py` intake parse | ⚠️ Phase 2 | Extracts 3 fields; role_id inferred by keyword matching |
| `data_decision` atom reading content | ⚠️ Phase 2 | Role-variant concept_text has role-specific scenarios |

### Dry-Run Validation (2026-03-24)

Four EDC JDs tested against the current atom pool assuming a de-roled diagnostic:

| Role | Persona Match | Domain Coverage | Diagnostic Valid? |
|------|--------------|----------------|-------------------|
| Credit Insurance Underwriter | ✅ UW exists | ~70% | ✅ (known role) |
| Investment Analyst | ❌ Wrong persona (data vs. finance) | ~55% | ❌ |
| Sr. Technical Advisor | ❌ No persona | ~35% | ❌ |
| Junior SPF Associate | ❌ No persona | ~80% if de-roled | ❌ |

**Conclusion:** The atoms are at critical mass for domain coverage. The diagnostic is the bottleneck.

---

## Atom Library Status (post Phase 4)

**20 canonical atoms across 7 domains.**

| Domain | Count | Universal | Role-variant |
|--------|-------|-----------|--------------|
| `responsible_ai` | 2 | `safe_framework`, `ai_tool_governance` | — |
| `strategic_prompting` | 2 | `craf_framework`, `iterative_refinement` | — |
| `critical_eval` | 2 | `verify_framework`, `hallucination_patterns` | — |
| `augmented_comm` | 2 | `surface_workflow`, `email_message_drafting` | — |
| `relationship_intel` | 6 | `meeting_intelligence` | rm, uw, an, mk, pm |
| `data_decision` | 5 | *(Phase 5 adds 1 universal)* | rm, uw, an, mk, pm |
| `capstone` | 1 | `end_to_end_workflow` | — |

**Known gap:** `data_decision` has no universal atom. Role-variant reading content
contains role-specific scenarios (analytics dashboards, portfolio analysis) that feel
off for finance/engineering roles. Phase 5 adds `data_decision__universal_analysis`.

---

## Roadmap

### Phase 5 — Role-Agnostic Diagnostic & Intake
> Plan: `plans/phase5-role-agnostic-diagnostic-plan.md`
> Status: PLANNED

**What it fixes:**
- Replaces role-gated MCQ diagnostic with 6 "Bring Your Own Work" open prompts
- Upgrades intake LLM parse from 3 → 6 fields (adds `industry`, `org_type`, `seniority`)
- Removes `role_id` keyword inference from Welcome page
- Adds `data_decision__universal_analysis` atom (21 total)

**Why this before LinkedIn:**
The BYOW diagnostic is self-contained — it generates its own context signal from
user responses. LinkedIn enhances tag matching but is not a prerequisite.

**UX latency:** ~3–8 seconds for BYOW scoring (single batch LLM call, ~1700 tokens).
Model: `gemini-2.0-flash` temperature 0.1.

---

### Phase 6 — LinkedIn Profile Integration
> Status: FUTURE — do not start until Phase 5 UAT passes

**What it adds:**
- LinkedIn OAuth 2.0 login as an alternative to the text input box
- LLM transformation: LinkedIn profile → intake_profile shape Phase 5 defined
- Pre-populates `role_text`, `daily_tasks`, `industry`, `org_type`, `seniority`
- Role selector in Advanced Options becomes truly optional shortcut

**Why after Phase 5:**
Phase 5 defines the intake_profile schema that LinkedIn feeds into.
Build the target format first; wire the source second.

**Architecture decision needed before Phase 6:**
LinkedIn introduces a third identity source alongside `GCP_USER_EMAIL` / `DEV_USER_EMAIL`.
Decision required: LinkedIn as primary identity (replace email) or profile enrichment
layer on top of existing email auth?

---

### Phase 7 — ZH Translations for New Atoms + BYOW Prompts
> Status: FUTURE

- Extend `translate_content.py` to handle `content/diagnostic_prompts.json`
- Translate 5 Phase 4 atoms + `data_decision__universal_analysis` atom content
- ZH versions of BYOW prompts and rubrics

---

### Phase 8 — Engineer / IT / Specialist Role Atoms
> Status: FUTURE

- Add role-variant atoms or universal atoms for technical roles
- `data_decision__technical_analysis` covering engineering data workflows
- `responsible_ai__technical_governance` for regulated technical environments

---

## Design Principles (derived from this architecture)

**1. Separate the behavior from the scenario.**
The competency being measured or taught must be independent of the scenario used
to deliver it. Scenario wraps behavior at runtime via `fill_scenario()`. This is
already true for atoms; it must become true for diagnostic items.

**2. Roles are runtime context, not structural gates.**
`role_id` should only exist in Firestore for legacy compat and display purposes.
No content loading, no item selection, no path assembly should be gated by `role_id`.

**3. The diagnostic must produce valid signal for any job title.**
If domain scores are noise, the entire path downstream is noise. Diagnostic quality
is the highest-leverage investment in the learning experience.

**4. LinkedIn and JD text are interchangeable inputs.**
Both feed the same `intake_profile` shape. The platform should be indifferent to
which one the user provides.

**5. Universal atoms first, role variants as enrichment.**
New domains should start with a universal atom. Role variants add depth but are not
required for the platform to serve that domain.

---

## Non-Goals (permanent)

- Manager dashboards or cohort analytics
- Admin UI for content editing
- Email notifications or badges
- MLflow prompt versioning
- Mobile layout
- Any assessment that requires knowing the user's role to produce valid scores

---

## Key Files

| File | Purpose |
|------|---------|
| `content/atomic_modules_v2.json` | Canonical atom library |
| `utils/path_assembler.py` | `assemble_path()` + `fill_scenario()` |
| `pages/01_Diagnostic.py` | Diagnostic flow (Phase 5 rewrites this) |
| `pages/00_Welcome.py` | Intake form (Phase 5 enriches this) |
| `content/diagnostic_items.json` | Legacy MCQ items (Phase 1 — kept for ZH compat) |
| `content/diagnostic_prompts.json` | BYOW prompts (Phase 5 creates this) |
| `utils/ai.py` | All LLM calls including diagnostic scoring |
| `scripts/generate_atom.py` | Atom generation CLI |
