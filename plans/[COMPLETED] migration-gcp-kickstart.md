# GCP Migration — Phase A Kickstart Prompt

Copy the section below into a new Claude Code session in the migrated project folder.

---

## Kickstart Prompt

You are implementing **Phase A of the GCP migration** for AI Hero Academy:
replacing the Databricks LLM layer (`utils/ai.py`) with Google Gemini API,
so the app runs locally with zero Databricks dependencies for AI calls.

The full migration spec is in `MIGRATION.md`. Read it before touching any code.

**The app data layer (Databricks SQL / Delta tables) is NOT touched in Phase A.**
`utils/db.py`, `utils/auth.py`, and all pages remain unchanged.
Focus exclusively on the LLM swap.

---

### Read these files first (in order)

1. `MIGRATION.md` — full migration spec and phased plan
2. `utils/ai.py` — the file you will replace (understand every function and its callers)
3. `utils/db.py` — understand `_log_call` dependency (used by `ai.py`); do not modify
4. `requirements.txt` — understand current deps; you will edit this
5. `.env.example` — understand current env vars; you will edit this

---

### Branch setup

```bash
git remote set-url origin https://github.com/sztimhdd/AI_Hero_Academy.git
git checkout -b feature/migrate-llm-gemini
```

---

### What to build (Phase A only)

#### MA-1 — Rewrite `utils/ai.py`

Replace the Databricks SDK LLM client with Google Gemini while keeping every
public function signature identical.

**Public API that must not change:**

```python
call_llm(messages: list[dict], temperature: float, user_email: str, call_type: str) -> str
score_diagnostic(responses_with_rubrics: list[dict], user_email: str) -> dict
generate_gap_map(domain_scores: dict, domain_descriptions: dict, user_email: str, source_type: str) -> list[dict]
coach_response(system_prompt: str, conversation: list[dict], user_input: str, user_email: str) -> str
score_evaluation(responses_with_rubrics: list[dict], user_email: str) -> dict
generate_module_coach_note(module_title: str, evaluation_score: float, domain_scores: dict, next_module_title: str | None, user_email: str) -> str
```

**Gemini implementation notes:**

- Use `google-genai` SDK (`pip install google-genai`)
- Model: `gemini-2.0-flash`
- Auth: `GEMINI_API_KEY` env var
- `messages` format is already OpenAI-compatible (`[{"role": "system"|"user"|"assistant", "content": "..."}]`)
  - Gemini separates `system_instruction` from the conversation turns
  - Extract the first `system` message as `system_instruction`; pass the rest as `contents`
- `temperature` maps directly to Gemini's `generation_config`
- Return `response.text` (string) — same as current `resp.choices[0].message.content`

**`_log_call` in Phase A:**

- Replace the Delta SQL INSERT with a Firestore write OR a local JSON append fallback
- Preferred Phase A approach: write to a local `logs/ai_call_log.jsonl` file (one JSON line per call)
- Create `logs/` directory; add `logs/` to `.gitignore`
- Wrap in try/except — never let logging break the main flow

**`_extract_json` and `_score_batch`:** unchanged — copy as-is (no Databricks dependency).

---

#### MA-2 — Update `requirements.txt` and `.env.example`

`requirements.txt`:
- Remove: `databricks-sdk>=0.35.0`
- Add: `google-genai>=1.0.0`

`.env.example`:
- Remove: `DATABRICKS_TOKEN`, `DATABRICKS_WAREHOUSE_ID`, `SERVING_ENDPOINT_NAME`
- Add: `GEMINI_API_KEY=your-key-here`
- Keep: `DEV_USER_EMAIL` (still used by `utils/auth.py`)
- Add comment: `# Phase B will add: GCP_PROJECT_ID, GCP_USER_EMAIL`

**Note**: `utils/db.py` still imports `databricks-sdk` for the data layer.
Do NOT remove `databricks-sdk` from requirements yet — that happens in Phase B.
Add a `# TODO: DATABRICKS_REMOVED — remove after Phase B` comment next to it.

---

#### MA-3 — Verify Phase A locally

```bash
# Install updated requirements
.venv/Scripts/pip install -r requirements.txt

# Set GEMINI_API_KEY in .env (copy from .env.example, fill in real key)
# Set DEV_USER_EMAIL=dev@example.com in .env

# Run the app (data layer will still need Databricks; AI calls will use Gemini)
bash run_uat.sh
```

Spot-check these flows with Playwright MCP (`mcp__playwright__browser_*`):
1. Navigate to `http://localhost:8501`
2. Exercise the diagnostic flow (answer questions, submit)
3. Confirm an AI response appears in the coach practice view
4. Check `logs/ai_call_log.jsonl` — confirm entries are being written
5. Confirm no `databricks.sdk.service.serving` import errors in terminal

If the data layer fails (expected — Databricks SQL still required), that is acceptable.
Phase A is complete when **AI calls succeed** and **no import errors** on the LLM path.

---

### Commit when Phase A is done

```bash
git add utils/ai.py requirements.txt .env.example .gitignore
git commit -m "feat(migrate): replace Databricks LLM with Gemini API (Phase A)"
git push -u origin feature/migrate-llm-gemini
```

Then open a PR against `main` on https://github.com/sztimhdd/AI_Hero_Academy.

---

### Acceptance checklist — Phase A

- [ ] `utils/ai.py` has zero `databricks` imports
- [ ] All 6 public function signatures are unchanged
- [ ] `call_llm()` uses `gemini-2.0-flash` via `google-genai` SDK
- [ ] `GEMINI_API_KEY` env var is the only new auth requirement for AI calls
- [ ] `_log_call()` writes to `logs/ai_call_log.jsonl` (silently ignores failures)
- [ ] `logs/` is in `.gitignore`
- [ ] `requirements.txt` lists `google-genai`; `databricks-sdk` has a `TODO: DATABRICKS_REMOVED` comment
- [ ] App starts without import errors (`bash run_uat.sh`)
- [ ] At least one Gemini API call succeeds end-to-end and is logged

---

### What comes next (do NOT implement in this session)

- **Phase B**: Replace `utils/db.py` with Firestore (`google-cloud-firestore`)
- **Phase C**: `Dockerfile` + Cloud Run deployment
- **Phase D**: GitHub cleanup, remove `databricks.yml` / `app.yml` / `notebooks/`

Full spec for all phases is in `MIGRATION.md`.
