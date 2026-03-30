# UAT.md — AI Hero Academy MVP
## End-to-End User Acceptance Testing Specification
**Version**: 3.0 | March 2026

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 3.3 | 2026-03-23 | Baseline eval harness added: `.claude/evals/baseline-uat.md` — 41 checks, 9 personas (all 4 roles + en/zh), 38/41 release gate; reset script extended to support `--role an` |
| 3.2 | 2026-03-23 | Master-session model: Section 7 rewritten as direct-execution instructions (not copy-paste prompts); Section 1.1 corrected (removed non-existent `browser_scroll`; added `browser_evaluate` for JS scroll); Section 2.1 updated with server health check and startup sequence; Section 7.4 added for atom-path Home UAT |
| 3.1 | 2026-03-23 | Phase 3 automated UAT added (Section 9): `tests/uat_phase3.js` — 34/34 checks pass; demo personas 3a–3f via `?demo=true&profile=X`; note on F1 validation mechanism (post-click, not disabled button) |
| 3.0 | 2026-03 | Phase 3 intake form; remove Databricks Delta checks (app uses Firestore); fix Welcome page flow; add PM role (UAT-18); add Group E smoke test; branding pre-flight; fix --role an availability |
| 2.0 | 2026-03 | Added Group D state variants, UW/AN/MK smoke tests |
| 1.0 | 2026-02 | Initial spec |

---

## Purpose

This document is the authoritative test specification for the AI Hero Academy MVP UAT. It is intended to be read and executed by a dedicated **Claude Code UAT Agent** using the Playwright MCP browser control tools — against either a **locally running instance** or the **live Cloud Run deployment**.

**Data layer:** The app persists to **Google Cloud Firestore** (GCP project `banded-totality-485901`). There are no Databricks Delta tables to query. Write verification is performed via UI state transitions — if the app navigates to the next expected page, the write succeeded.

---

## 0. Deployment & CI/CD

### 0.1 CI/CD Pipeline

Pushes to `main` trigger `.github/workflows/deploy.yml` (GitHub Actions):

```
git push origin main
  → GitHub Actions: build & deploy job
  → google-github-actions/auth@v2  (credentials_json: GCP_SA_KEY secret)
  → gcloud auth configure-docker us-central1-docker.pkg.dev
  → docker build  --build-arg NEXT_PUBLIC_FIREBASE_* (from GitHub Secrets)
  → docker push   us-central1-docker.pkg.dev/banded-totality-485901/ai-hero-academy/b2c:{sha}
  → gcloud run services delete ai-hero-academy-b2c  (clears stale secret-ref env vars)
  → google-github-actions/deploy-cloudrun@v2
      service:  ai-hero-academy-b2c
      region:   us-central1
      flags:    --allow-unauthenticated --port=8080 --memory=1Gi --min-instances=0 --max-instances=3
      env_vars: FIREBASE_ADMIN_PROJECT_ID, FIREBASE_ADMIN_CLIENT_EMAIL,
                FIREBASE_ADMIN_PRIVATE_KEY, GEMINI_API_KEY, DEMO_TOKEN
```

Monitor builds: [GitHub Actions](https://github.com/sztimhdd/AI_Hero_Academy/actions)

Build typically completes in 5–8 minutes. The job uses `concurrency: deploy-production` — concurrent pushes cancel the older run.

**Required GitHub Secrets:**

| Secret | Purpose |
|--------|---------|
| `GCP_SA_KEY` | Service account JSON key for `google-github-actions/auth@v2` |
| `NEXT_PUBLIC_FIREBASE_API_KEY` | Firebase client SDK (build-time `--build-arg`) |
| `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` | Firebase client SDK |
| `NEXT_PUBLIC_FIREBASE_APP_ID` | Firebase client SDK |
| `NEXT_PUBLIC_APP_URL` | Canonical app URL injected at build |
| `FIREBASE_ADMIN_CLIENT_EMAIL` | Firebase Admin SDK (runtime `env_vars`) |
| `FIREBASE_ADMIN_PRIVATE_KEY` | Firebase Admin SDK |
| `GEMINI_API_KEY` | Gemini API calls from API routes |
| `DEMO_TOKEN` | Private beta `/demo?t=TOKEN` route |

### 0.2 Two UAT Modes

| Mode | URL | When to use |
|------|-----|-------------|
| **Local** | `http://localhost:3000` | Dev iteration, mid-feature testing |
| **Remote (Cloud Run)** | `$(gcloud run services describe ai-hero-academy-b2c --region us-central1 --format "value(status.url)")` | Pre-release gate, post-deploy smoke test |

**Local startup:**

```bash
npm run dev   # Next.js dev server → http://localhost:3000
```

Then seed test personas if not already present:

```bash
npx ts-node scripts/seed-dev.ts
```

**Remote UAT — get the URL first:**

```bash
SERVICE_URL=$(gcloud run services describe ai-hero-academy-b2c \
  --region us-central1 --project banded-totality-485901 \
  --format "value(status.url)")
echo "$SERVICE_URL"
```

Then navigate Playwright:

```javascript
mcp__playwright__browser_navigate(url=SERVICE_URL)
mcp__playwright__browser_wait_for(text="AI Hero", time=20)
```

> **Cold start warning:** Cloud Run scales to zero when idle. First request after an idle period takes 10–20 seconds. Always use `browser_wait_for(time=20)` before interacting on remote.

### 0.3 Post-Deploy Smoke Test

After any push to `main`, verify the deployment before running Tier 2 UAT:

```bash
SERVICE_URL=$(gcloud run services describe ai-hero-academy-b2c \
  --region us-central1 --project banded-totality-485901 \
  --format "value(status.url)")

# Landing page loads
curl -sf "$SERVICE_URL" -o /dev/null -w "%{http_code}\n" && echo "T-CR-0 PASS" || echo "T-CR-0 FAIL"

# API health (session endpoint returns 401 without cookie — that's correct)
curl -sf "$SERVICE_URL/api/auth/session" -o /dev/null -w "%{http_code}\n"
# Expected: 401 or 405 (not 500 — server is up and routing)

# Tier 3 — share card (Linux/Cloud Run only, font rendering):
curl -sf "$SERVICE_URL/api/credential/share-card?uid=dev-complete-004" \
  -o /dev/null -w "%{http_code} %{content_type}\n" && echo "T-CR-1 PASS" || echo "T-CR-1 FAIL"
```

Or via Playwright:

```javascript
mcp__playwright__browser_navigate(url=SERVICE_URL)
mcp__playwright__browser_wait_for(text="AI Hero", time=20)
mcp__playwright__browser_take_screenshot(filename="post_deploy_smoke.png", type="png")
```

Landing page renders → deployment succeeded. Hangs or 500 errors → check [GitHub Actions logs](https://github.com/sztimhdd/AI_Hero_Academy/actions).

### 0.4 Dev Login (LOCAL_DEV only)

The app exposes `/api/auth/dev-login` and `/api/auth/demo-login` when `LOCAL_DEV=true` (set in `.env.local`). These routes are **blocked in production** (Cloud Run does not set `LOCAL_DEV`).

Dev personas seeded by `scripts/seed-dev.ts`:

| Email | State |
|-------|-------|
| `day1@dev.test` | Fresh — no onboarding complete |
| `day3@dev.test` | Days 1–3 done |
| `day6@dev.test` | Days 1–6 done, capstone unlocked |
| `complete@dev.test` | Graduated — credential issued |

---

## 1. Agent Instructions

### 1.1 Tools Required

| Tool | Key Parameters | Purpose |
|------|----------------|---------|
| `mcp__playwright__browser_navigate` | `url` | Open a URL in the current tab |
| `mcp__playwright__browser_navigate_back` | — | Go back to the previous page |
| `mcp__playwright__browser_snapshot` | `selector` (optional CSS scope), `filename` (optional save to file) | Capture accessibility tree — **always call before acting** |
| `mcp__playwright__browser_click` | `ref`, `element` (description), `button`, `doubleClick` | Click by `ref` from snapshot |
| `mcp__playwright__browser_type` | `ref`, `element`, `text`, `slowly`, `submit` | Type into a single input |
| `mcp__playwright__browser_fill_form` | `fields: [{name, ref, type, value}]` — types: `textbox`, `radio`, `checkbox`, `combobox`, `slider` | **Preferred for multi-field forms** — fills all in one call |
| `mcp__playwright__browser_select_option` | `ref`, `element`, `values` (array) | Select dropdown values |
| `mcp__playwright__browser_press_key` | `key` (e.g., `Enter`, `Tab`, `Escape`) | Send keyboard events |
| `mcp__playwright__browser_wait_for` | `text`, `textGone`, `time` (seconds) — mutually exclusive | Wait for text to appear/disappear or a fixed delay |
| `mcp__playwright__browser_take_screenshot` | `filename`, `fullPage` (boolean), `ref`/`element` for element crop | Capture screenshot; `fullPage: true` captures full scrollable page |
| `mcp__playwright__browser_evaluate` | `function` (JS string) | Execute JS in page — use for scrolling (see below) |
| `mcp__playwright__browser_resize` | `width`, `height` | Set viewport; always `1280×800` for this project |
| `mcp__playwright__browser_hover` | `ref`, `element` | Hover over element (triggers tooltips, expanders) |
| `mcp__playwright__browser_drag` | `startRef`, `startElement`, `endRef`, `endElement` | Drag and drop |
| `mcp__playwright__browser_handle_dialog` | `accept` (bool), `promptText` | Accept or dismiss alert/confirm/prompt dialogs |
| `mcp__playwright__browser_network_requests` | `includeStatic` (bool, default false), `filename` | Inspect API calls — use to debug failed AI calls (filter to non-static) |
| `mcp__playwright__browser_console_messages` | — | Read browser console for JS errors |
| `mcp__playwright__browser_tabs` | `action`: `list`/`new`/`close`/`select`, `index` | Manage browser tabs |
| `mcp__playwright__browser_close` | — | Close the browser page |
| `mcp__playwright__browser_file_upload` | `paths` (array of absolute paths) | Upload files via file input elements |
| `mcp__playwright__browser_install` | — | Install Chromium if missing (run once if browser not found) |

> **No `browser_scroll` tool exists.** Use `browser_evaluate` to scroll:
> ```javascript
> // Scroll the main Streamlit content area down
> () => window.scrollBy(0, 500)
> // Or target the specific scrollable container
> () => document.querySelector('[data-testid="stMain"]').scrollTop += 500
> ```

> **Snapshot mode is `incremental` by default.** The server only returns changed nodes after each interaction. After any Streamlit rerender, call `browser_snapshot` again — all `ref` values from the previous snapshot are stale and must not be reused.

> **Note:** The app uses Firestore, not Databricks Delta tables. Do NOT attempt SQL queries
> against `mdlg_ai_shared.*` — that catalog does not contain app data. All write verification
> is done via UI state transitions (see Section 1.4).

### 1.2 How to Interact with Streamlit

Streamlit rerenders the full DOM on every interaction. The Playwright MCP snapshot mode is **incremental by default** — after any rerender, the server returns only changed nodes. This means **all `ref` values from the previous snapshot are stale and must be discarded**.

Follow this pattern for every interaction:

1. **Call `browser_snapshot` first** to get the current accessibility tree and `ref` values
2. **Use the `ref` value** from the snapshot to target `browser_click` / `browser_type` — never guess refs
3. **After any click that triggers a rerender**, call `browser_wait_for` (text to appear or `textGone` for spinners), then call `browser_snapshot` again before the next action
4. **For multi-field forms** (e.g., the Welcome page Q1 + Q2), prefer `browser_fill_form` over multiple sequential `browser_type` calls:

```python
browser_fill_form(fields=[
  {"name": "Q1 work description", "ref": "<ref>", "type": "textbox",
   "value": "I'm a Relationship Manager..."},
  {"name": "Q2 AI tools multi-select", "ref": "<ref>", "type": "combobox",
   "value": "Microsoft Copilot (M365 — Word, Excel, Teams, Outlook)"}
])
```

5. **To scope a snapshot to the main content area** (reduces token volume on Streamlit pages with long sidebars):

```python
browser_snapshot(selector="[data-testid='stMain']")
```

6. **To scroll** (no `browser_scroll` tool exists — use `browser_evaluate`):

```python
browser_evaluate(function="() => window.scrollBy(0, 600)")
```

### 1.3 Handling Loading States

The app shows loading spinners during AI calls (scoring, gap map, coach responses). These can take 5–60 seconds depending on the call type.

```text
Diagnostic scoring + gap map:   up to 60 seconds
Module evaluation scoring:      up to 45 seconds
AI coach response (one turn):   up to 15 seconds
Course creation (Build Course): up to 30 seconds
Intake profile parse (Welcome): up to 15 seconds
Page navigation/load:           up to 10 seconds
```

Pattern to wait for AI loading to complete:

```python
browser_wait_for(textGone="Analyzing", time=60)   # diagnostic scoring
browser_wait_for(textGone="Scoring",   time=45)   # evaluation scoring
browser_wait_for(textGone="Building",  time=30)   # course creation
browser_wait_for(textGone="Personalizing", time=15)  # intake parse
```

> **`time` is in seconds, not milliseconds.** The `browser_wait_for` tool accepts `time` as a number of seconds (e.g., `time=60`), not milliseconds.

If a loading state does not clear within the timeout: take a screenshot, mark the step as FAIL, and continue to the next scenario if possible.

**Debugging a stuck or failed AI call:**

If a spinner never clears or an `st.error` box appears, use `browser_network_requests` to inspect what the app actually sent:

```python
# Get all non-static requests (XHR, websocket, API calls) since page load
browser_network_requests(includeStatic=False)
```

Look for requests to the Gemini/serving endpoint that returned a non-2xx status or timed out. Also check:

```python
browser_console_messages()   # JS errors or Streamlit websocket failures
```

### 1.4 Firestore State Verification

The app persists to Firestore. Direct SQL queries are not possible. Use these verification patterns instead:

**Pattern 1 — Page navigation proves write.** If the app successfully navigates to the next page (e.g., Diagnostic after profile creation, Skills Profile after diagnostic), the required Firestore write succeeded. The app reads Firestore on every page load and will throw an error or stay on the current page if a write failed.

**Pattern 2 — Reset script re-read.** After running `python scripts/reset_uat_user.py`, the script reads Firestore to confirm the seeded state. If the reset command completes without error, the prior writes are confirmed intact.

**Pattern 3 — Explicit navigation check.** After a write, navigate away and back to the page that reads that data. If the data appears correctly (e.g., score is visible, gap map has bullets), the write is confirmed.

> **When in doubt:** Navigate back to the page that reads the data (Home, Skills Profile) and confirm it loads without error. This is the functional equivalent of a SELECT query.

### 1.5 AI Call Assertions

The app makes real LLM calls to **Google Gemini API** (`gemini-2.0-flash`). **Do NOT assert specific AI-generated text content** — it varies per call. Assert only:
- That the UI transitioned to the expected state (new heading, score visible, next section loaded)
- That structural elements appear (score is a number, gap map has bullets, coach replied)

### 1.6 Failure Handling

If a step fails:
1. Call `browser_take_screenshot` immediately and note the filename
2. Log the failure as `[FAIL] UAT-NN: Step N — description of what was expected vs. what was seen`
3. Continue to the next scenario if the failure is not a blocking dependency
4. At the end, list all failures in a summary

### 1.7 Viewport

Set the viewport to 1280×800 before starting:
```
browser_resize(width=1280, height=800)
```

---

## 2. Pre-Test Setup

### 2.1 Start the App

**Step 1 — Check if already running:**

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8501/
```

If the response is `200`, the server is already up — skip to Step 3. If it returns nothing or an error, proceed to Step 2.

**Step 2 — Start the server:**

```bash
bash run_uat.sh &
```

Then poll until it responds:

```bash
# Wait up to 30 seconds for the server to be ready
for i in $(seq 1 15); do
  code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8501/ 2>/dev/null)
  [ "$code" = "200" ] && echo "Server ready" && break
  sleep 2
done
```

**Step 3 — Verify with Playwright:**

```python
mcp__playwright__browser_resize(width=1280, height=800)
mcp__playwright__browser_navigate(url="http://localhost:8501")
mcp__playwright__browser_snapshot()
```

Expected: A page loads without Python traceback or red Streamlit error box. The exact page depends on the test user's Firestore state.

### 2.2 Test User Setup

The test user email is set in `.env` as `DEV_USER_EMAIL`. The default value in `.env.example` is `uat-test@example.com`. Check your `.env` for the actual value before running any scenario.

All reset commands operate on the `DEV_USER_EMAIL` address only — no other users are affected.

### 2.3 Reset Command Reference

Each test group has its own independent pre-condition. Run the matching reset command before starting that group — **you do not need to run prior groups**.

| Group | Reset Command | Starting State | Scenarios |
|-------|--------------|----------------|-----------|
| **A** | `python scripts/reset_uat_user.py` | No profile; Welcome page | UAT-01 |
| **B** | `python scripts/reset_uat_user.py --role rm` | RM profile seeded; Diagnostic page | UAT-02, UAT-03 |
| **C** | `python scripts/reset_uat_user.py --profile course-built` | RM + diagnostic + course built, Module 1 not started; Home page | UAT-04 through UAT-12 |
| **D** | See each scenario's pre-conditions | Various | UAT-13 through UAT-18 |
| **E** | See each persona's pre-conditions | Various | Persona smoke tests |

> **`--role` availability:** `--role` accepts `rm`, `uw`, `mk`. There is no `--role an` —
> for Analyst and PM smoke tests (UAT-14, UAT-18), use the full-wipe reset and create the
> profile via the Welcome page in the test itself.

---

## 3. Pre-Flight Global Checks

Run these before beginning any test group. They must all pass before continuing.

### 3.1 App Health Check

1. Navigate to `http://localhost:8501`
2. Assert: Page loads within 10 seconds (no timeout, no server error)
3. Assert: No Python traceback visible on the page
4. Assert: No Streamlit red error box (`st.error`) from a system-level failure

### 3.2 Branding Check

The app must not display organization-specific branding. After navigating to `http://localhost:8501`:

1. Assert: The text **"EDC"** does NOT appear anywhere on the visible page
2. Assert: The text **"EDC Internal"** does NOT appear anywhere
3. Assert: The text **"your EDC environment"** does NOT appear
4. Assert: The text **"AI Hero Academy"** IS visible (correct product name)

> **Why this matters:** This check caught a production-bound branding leak found in the
> 2026-03 UAT run. Run it on every page that renders visible text, not just Welcome.

### 3.3 Common Checks (apply to every page under test)

For every key screenshot in every scenario, assert:
- No "EDC" text visible anywhere on screen
- No empty fields rendering `None`, `null`, `undefined`, or `[]` as visible text
- No Python traceback or Streamlit error box (red background box with stack trace)
- Page fully renders within 10 seconds of navigation

---

## 4. Test Scenarios

> **Independent groups**: Each group has its own reset command. A UAT runner can start
> at any group without running prior groups. Within a group, scenarios run in order.

---

### Group A — Onboarding

**Reset before this group:** `python scripts/reset_uat_user.py`

**Starting state:** No docs in Firestore `user_profiles` for the test user. App opens on Welcome page.

---

#### UAT-01: Welcome Page — New RM User Onboarding (Phase 3 Intake Form)

**Purpose:** Verify a brand-new user can land on the Welcome page, fill in the intake form (Q1 role description + Q2 AI tools), submit, and navigate to the Diagnostic. The role dropdown is in the **Advanced Options expander** — not the main flow.

**Pre-conditions:** Test user has no Firestore `user_profiles` doc (confirmed by Group A reset).

**Steps:**

1. Navigate to `http://localhost:8501`
2. Assert: Text "AI Hero Academy" is visible on the page
3. Assert: Pre-flight branding check passes (no "EDC" text)
4. Assert: A multi-line text area (Q1) is visible with label "Tell us about your work" or equivalent
5. Assert: A multi-select widget (Q2) for AI tools is visible below Q1
6. Assert: The CTA button ("Start My Diagnostic" or equivalent) is visible
7. Type into the Q1 text area: `I'm a Relationship Manager at a financial institution. Every day I prepare client briefings, draft meeting agendas, and write follow-up emails. If AI could do ONE thing to make my work easier, it would be to summarize CRM notes and draft first-cut client proposals automatically.`
8. In the Q2 multi-select, select at least one AI tool option (e.g., "Microsoft Copilot (M365 — Word, Excel, Teams, Outlook)")
9. Expand the **"Advanced options (demo / admin)"** expander
10. Locate the role selector dropdown inside the expander
11. Select **"Relationship Manager"** from the role dropdown (ensures predictable role_id = `rm`)
12. Confirm the display name field shows a reasonable default (email prefix or name)
13. Collapse the expander (or leave it open — either is valid)
14. Click the CTA button ("Start My Diagnostic")
15. Assert: A loading spinner appears ("Personalizing your journey..." or equivalent)
16. Wait for spinner to disappear (timeout: **15 seconds**)
17. Assert: The page transitions — Diagnostic content is visible (orientation screen or "Question 1 of 18" counter appears)

**State Verification:** The page transition to Diagnostic confirms the Firestore `user_profiles` write succeeded. (The app reads this doc on every load; it would stay on Welcome if the write failed.)

---

### Group B — Diagnostic Journey

**Reset before this group:** `python scripts/reset_uat_user.py --role rm`

**Starting state:** `user_profiles` doc exists (role=rm). App opens on Diagnostic page. Skips UAT-01 onboarding.

---

#### UAT-02: Diagnostic — Complete RM 18-Question Assessment

**Purpose:** Complete all 18 diagnostic questions across 6 domains and verify that AI scoring runs and produces a completed session with a gap map.

**Pre-conditions:** Group B reset complete. User is on the Diagnostic page.

**Steps:**

1. Assert: An orientation screen is visible (contains text about the number of questions or time estimate)
2. Click the orientation CTA button to begin the diagnostic
3. For each question **N = 1 to 18**, repeat:
   a. Assert: A question counter text is visible (e.g., "Question N of 18" or "N / 18")
   b. Assert: A domain label/tag is visible on the question
   c. **If the question shows radio buttons (MCQ):**
      - Select the first radio option (option A)
      - Click "Next" button
   d. **If the question shows a text area (prompt sandbox or micro-task):**
      - Click into the text area
      - Type: `This is a UAT test response. I would structure my prompt with clear context about the client situation, specify the desired output format, include relevant constraints such as data safety rules, and ask for a specific deliverable.`
      - Click the "Submit" button
   e. Wait for the next question to appear before continuing
4. After submitting question 18:
   - Assert: A loading indicator or spinner appears (text like "Analyzing" or a spinner component)
   - Wait for loading to complete (`browser_wait_for textGone` on loading text, timeout: **60 seconds**)
5. Assert: The page has transitioned to the Skills Profile ("Your AI Skills Profile" is visible, OR a numeric score is displayed)

**State Verification:**
- Skills Profile rendered → `diagnostic_sessions` write confirmed
- Gap map bullets visible → `gap_maps` write confirmed

---

#### UAT-03: Skills Profile — Scores, Gap Map, Build Course

**Purpose:** Verify the Skills Profile page renders domain scores, a gap map narrative, and assessment history; then confirm the "Build My Training Course" action creates 7 training progress records and navigates to Home.

**Pre-conditions:** Follows UAT-02. User is on the Skills Profile page.

**Steps:**

1. Assert: Heading "Your AI Skills Profile" is visible
2. Assert: An overall score value is visible (a decimal number)
3. Assert: A level label is visible and is one of: `Unaware`, `Explorer`, `Practitioner`, `Proficient`, `Champion`
4. Assert: Domain scores section is rendered (at least one domain name is visible with a score)
5. Assert: A section titled "Your Gap Map" or equivalent heading is present
6. Assert: At least **3 gap bullets** are visible under the gap map section
7. Assert: No gap bullet renders `None`, `null`, or empty text
8. Assert: An assessment history section or table is visible with at least 1 data row
9. Assert: A "Build My Training Course" button is visible (course has not yet been built)
10. Assert: A "Retake Diagnostic" button is visible
11. Click "Build My Training Course"
12. Assert: A loading state appears (spinner or "Building" text)
13. Wait for loading to complete (timeout: **30 seconds**)
14. Assert: Page has navigated to the Home dashboard ("Welcome back" is visible)

**State Verification:** 7 module cards visible on Home → 7 `training_progress` writes confirmed.

---

### Group C — Full Module Journey

**Reset before this group:** `python scripts/reset_uat_user.py --profile course-built`

**Starting state:** RM profile + completed diagnostic + gap map + 7 `training_progress` docs seeded (Module 1 unlocked, Modules 2–7 locked). App opens on Home dashboard. Skips UAT-01 through UAT-03.

---

#### UAT-04: Home Dashboard — Module List and Lock State

**Purpose:** Verify the Home dashboard displays the personalized module list, with Module 1 unlocked and Modules 2–7 locked, and the summary card shows the user's score.

**Pre-conditions:** Group C reset complete. User is on the Home page.

**Steps:**

1. Assert: A greeting with the user's name is visible (or "Welcome back" text)
2. Assert: A summary card shows a numeric overall score and a level label
3. Assert: Exactly **7 module cards** are listed (numbered 01 through 07)
4. Assert: Module 1 has an actionable CTA button (e.g., "Start Module", "Start Reading", or similar — not a lock icon or disabled state)
5. Assert: At least one of Modules 2–7 shows a locked state (lock icon, "locked" text, or a disabled/greyed appearance)
6. Assert: A link or button to "View Skills Profile" or "View Full Profile" is present in the summary card area

---

#### UAT-05: Module 1 — Overview Sub-view

**Purpose:** Verify the Course Module overview sub-view renders the module title, step progress strip, and context-aware CTA before any sub-modules are completed.

**Pre-conditions:** Follows UAT-04. User is on the Home page.

**Steps:**

1. Click the CTA button on **Module 1** (the first unlocked module card)
2. Assert: A module number (e.g., "01") and module title text are visible
3. Assert: A step progress strip is visible showing at least the labels "Reading", "Practice", and "Quiz" (or equivalent abbreviations)
4. Assert: The primary CTA button text is "Start Reading" (or equivalent — reading has not yet been completed)
5. Note the module title text for reference in UAT-10 (to confirm Module 2 has a different title)

---

#### UAT-06: Module 1 — Reading Sub-view

**Purpose:** Verify the reading content renders correctly with segmented pill tab navigation, all 4 section tabs are accessible, and completing reading on the Takeaway tab advances to Practice.

**Pre-conditions:** Follows UAT-05. User is on the Module 1 overview.

**Steps:**

1. Click the "Start Reading" CTA button
2. Assert: A segmented pill tab control is visible with 4 tabs: "Concept", "Example", "Pitfall", "Takeaway"
3. Assert: The "Concept" tab is selected by default and concept text is visible in the content area
4. Click the "Example" tab
5. Assert: Example content is visible (a green/success styled box with "Good example" label)
6. Click the "Pitfall" tab
7. Assert: Pitfall content is visible (a yellow/warning styled box with "Common mistake" label)
8. Click the "Takeaway" tab
9. Assert: Takeaway content is visible (an info styled box with "Key takeaway" label)
10. Assert: A "Mark Reading Complete →" button is visible on the Takeaway tab
11. Assert: No "Mark Reading Complete" button appears when on the Concept tab (click back to Concept to verify)
12. Return to "Takeaway" tab and click "Mark Reading Complete →"
13. Assert: The UI transitions to the Practice sub-view — a "Scenario" label or "Task 1 of 4" text becomes visible

**State Verification:** Practice sub-view loaded → `reading_completed_at` write confirmed. (Navigate back to Module Overview — Reading step shows as completed in the progress strip.)

---

#### UAT-07: Module 1 — Practice Sub-view (AI Coach)

**Purpose:** Verify the AI coach practice flow: the scenario panel renders, tasks advance sequentially, the coach responds to user input, and completing all 4 tasks enables the "Complete Practice" action.

**Pre-conditions:** Follows UAT-06. User is on the Practice sub-view.

**Steps:**

1. Assert: A "Scenario" label and scenario description text are visible at the top of the page
2. Assert: A "Task 1 of 4" indicator (or "Task 1") is visible
3. Assert: A text input or chat input field is present and interactable
4. Type into the input field: `I would start by reviewing the CRM notes and then craft a prompt with relevant context about the client's industry, recent interactions, and the specific output format I need from Copilot.`
5. Submit the response (click the submit button, or press Enter if it is a chat input)
6. Wait for the coach response to appear (timeout: **15 seconds**)
7. Assert: A coach reply message is visible in the conversation area (at least one message with the coach avatar or label)
8. Assert: A turn counter is visible (text like "Turn 1 of 15" or "Turn 2")
9. Locate and click the "Next Task" button (or equivalent advance button)
10. Assert: "Task 2 of 4" is now visible
11. Type into the input: `For this task, I would verify the AI-generated output against the original CRM data before sending it to the client, checking each factual claim against the source notes.`
12. Submit and wait for coach response (timeout: **15 seconds**)
13. Assert: Coach responds with a new message
14. Click "Next Task" to advance to Task 3
15. Assert: "Task 3 of 4" is visible
16. Type: `I would use only anonymized, fictional data in my Copilot prompts to comply with our data safety policy, keeping all real client information out of the AI tool.`
17. Submit and wait for coach response (timeout: **15 seconds**)
18. Assert: Coach responds
19. Click "Next Task" to advance to Task 4
20. Assert: "Task 4 of 4" is visible
21. Type: `For the final task, I would chain multiple Copilot steps: first generate a draft, then verify key facts, then refine the prompt to improve the output before using it in the final deliverable.`
22. Submit and wait for coach response (timeout: **15 seconds**)
23. Assert: Coach responds
24. Assert: A "Complete Practice" button (or equivalent) is now visible
25. Click "Complete Practice"
26. Assert: The UI transitions to the Evaluation sub-view (quiz questions appear, e.g., "Question 1 of 4" or "Quiz" heading)

**State Verification:** Evaluation sub-view loaded → `coach_sessions` and `practice_completed_at` writes confirmed.

---

#### UAT-08: Module 1 — Evaluation Quiz

**Purpose:** Verify the 4-question quiz (3 MCQ + 1 performance task) renders correctly, AI scoring runs after final submission, and the results sub-view is reached.

**Pre-conditions:** Follows UAT-07. User is on the Evaluation sub-view.

**Steps:**

1. Assert: A quiz header or question counter is visible (e.g., "Question 1 of 4" or "Quiz")
2. **For Question 1 (MCQ):**
   a. Assert: Radio button options are visible
   b. Select the first available radio option
   c. Click the "Next" button
   d. Wait for Question 2 to load
3. **For Question 2 (MCQ):**
   a. Assert: Radio button options are visible
   b. Select the first available radio option
   c. Click the "Next" button
   d. Wait for Question 3 to load
4. **For Question 3 (MCQ):**
   a. Assert: Radio button options are visible
   b. Select the first available radio option
   c. Click the "Next" button
   d. Wait for Question 4 to load
5. **For Question 4 (performance task):**
   a. Assert: A text input area is visible (not radio buttons)
   b. Type: `I would first identify the key claims in the AI-generated summary, then verify each one against the original source data in CRM and meeting notes. Only after confirming accuracy would I include the content in the client report, and I would add a note that the draft was AI-assisted and human-reviewed.`
   c. Click the final "Submit" button
6. Assert: A loading state appears ("Scoring" text or spinner visible)
7. Wait for loading to complete (timeout: **45 seconds**)
8. Assert: The Results sub-view is now displayed — a module score value is visible (a decimal number)

**State Verification:**
- Results sub-view with score → `evaluation_score` and `evaluation_completed_at` writes confirmed
- Navigate to Home: Module 2 shows as unlocked (not locked) → `is_locked=false` write confirmed
- Navigate to Skills Profile: gap map has new bullets → post-evaluation `gap_maps` write confirmed

---

#### UAT-09: Module 1 — Results Sub-view

**Purpose:** Verify the results page shows the module score, an AI-generated coach note, and navigation CTAs for proceeding to Module 2.

**Pre-conditions:** Follows UAT-08. User is on the Results sub-view.

**Steps:**

1. Assert: A module score is visible (a decimal number between 0.0 and 4.0)
2. Assert: A coach note / feedback text block is visible (a non-empty text paragraph — content will vary; assert it is not empty)
3. Assert: A CTA button to proceed to Module 2 is visible (text like "Start Module 2", "Next Module", or "Go to Module 2")
4. Click the "Start Module 2" CTA button
5. Assert: The Module 2 overview sub-view loads — a module title different from Module 1's title is visible, and the step progress strip shows all stages as "not started" or "pending"

---

#### UAT-10: Module 2 — Unlock and Reading Start Verification

**Purpose:** Confirm Module 2 is properly unlocked, has distinct content from Module 1, and navigating back to Home correctly reflects Module 1 as completed.

**Pre-conditions:** Follows UAT-09. User is on Module 2 overview.

**Steps:**

1. Assert: Module 2's title text is different from the Module 1 title noted in UAT-05
2. Assert: The step progress strip shows Reading, Practice, and Quiz all as "not started" or "pending" (none completed yet)
3. Assert: The primary CTA button says "Start Reading" (or equivalent)
4. Click "Start Reading"
5. Assert: Reading content loads — segmented control is visible with 4 tabs; concept text visible on Concept tab
6. Assert: The reading content text is visually different from Module 1's reading content (distinct topic)
7. Navigate back to the Home dashboard (use the sidebar navigation or "Back to Dashboard" link)
8. Assert: Module 1's card on the Home page shows a completed state — a score value is displayed next to or within the Module 1 card
9. Assert: Module 2's card on the Home page shows an active/in-progress state — it has a CTA button (not locked)
10. Assert: Modules 3–7 remain locked

---

#### UAT-11: Skills Profile — Post-Training Score Update

**Purpose:** Verify that the Skills Profile page reflects updated domain scores after Module 1 evaluation, with the assessment history showing at least the initial diagnostic and the post-evaluation update.

**Pre-conditions:** Follows UAT-10.

**Steps:**

1. Navigate to the Skills Profile page (use sidebar link "Skills Profile" or the "View Full Skills Profile" link from Home)
2. Assert: "Your AI Skills Profile" heading is visible
3. Assert: The overall score value is visible
4. Assert: The assessment history section or table shows at least **2 rows** (the initial diagnostic row plus any subsequent update), OR the domain scores reflect non-zero values consistent with the prior evaluation updates
5. Assert: The gap map section still has bullets (at least 3 visible)

---

#### UAT-12: Retake Diagnostic — Progress Preservation

**Purpose:** Verify that starting a diagnostic retake works correctly, and that navigating away without completing it does NOT wipe prior training progress.

**Pre-conditions:** Follows UAT-11. User is on the Skills Profile page.

**Steps:**

1. Assert: The "Retake Diagnostic" button is visible on the Skills Profile page
2. Click "Retake Diagnostic"
3. Assert: The Diagnostic page loads — an orientation screen or "Question 1 of 18" counter is visible
4. If on the orientation screen, click through to begin the diagnostic
5. Assert: Question 1 is visible with radio buttons or a text input
6. Answer Question 1 (select any radio option for MCQ, or type a short response for text input)
7. Assert: Question 2 loads (the question counter advances — confirms partial diagnostic works)
8. Navigate back to the Home page **without completing** the diagnostic (use sidebar navigation — click "Home")
9. Assert: The Home page shows Module 1 with a **completed** state and its score (prior progress was NOT wiped)
10. Assert: Module 2 still shows as **unlocked** (is_locked = false)

**State Verification:** Module 1 still shows completed score → `training_progress` doc was NOT overwritten by the abandoned retake.

---

### Group D — State Variants and New Coverage

Each scenario in this group has its own independent reset command in its pre-conditions.

---

#### UAT-13: UW Role Smoke Test — Welcome and Diagnostic Start

**Purpose:** Verify that the Underwriter role is selectable via the Advanced Options expander and that a UW user can begin the diagnostic flow.

**Pre-conditions:** Run `python scripts/reset_uat_user.py` to wipe the test user before this scenario.

**Steps:**

1. Run `python scripts/reset_uat_user.py`
2. Navigate to `http://localhost:8501`
3. Assert: The Welcome page loads
4. Assert: "AI Hero Academy" text is visible
5. Assert: Pre-flight branding check passes (no "EDC" text)
6. Assert: The Q1 text area is visible
7. Type into Q1: `I'm an underwriter reviewing loan applications and assessing risk. I analyze financial statements and credit reports daily. If AI could help, I'd want it to flag unusual patterns in financial data automatically.`
8. Expand the **"Advanced options (demo / admin)"** expander
9. Locate the role selector dropdown inside the expander
10. Assert: **"Underwriter"** is present as a selectable option
11. Select "Underwriter" from the dropdown
12. Collapse the expander
13. Click the CTA button ("Start My Diagnostic")
14. Wait for spinner to disappear (timeout: **15 seconds**)
15. Assert: The Diagnostic page loads (question counter or orientation screen visible)
16. If on an orientation screen, click through to begin
17. Assert: Question 1 is visible with a domain label/tag
18. Answer Question 1 (select any radio option or type a short response)
19. Assert: Question 2 loads successfully (confirms UW diagnostic flow is functional)

**State Verification:** Diagnostic page → profile created with `role_id = 'uw'` confirmed.

---

#### UAT-14: AN Role Smoke Test — Welcome and Diagnostic Start

**Purpose:** Verify that the Analyst role is selectable via the Advanced Options expander and that an AN user can begin the diagnostic flow.

> **Note:** `--role an` is NOT available in the reset script. Always use full-wipe reset for this scenario.

**Pre-conditions:** Run `python scripts/reset_uat_user.py` to wipe the test user before this scenario.

**Steps:**

1. Run `python scripts/reset_uat_user.py`
2. Navigate to `http://localhost:8501`
3. Assert: The Welcome page loads
4. Assert: "AI Hero Academy" text is visible
5. Assert: Pre-flight branding check passes (no "EDC" text)
6. Type into Q1: `I'm a data analyst building dashboards and running ad-hoc SQL queries to support business decisions. If AI could help, I'd want it to generate first-draft SQL from plain English descriptions of what I need.`
7. Expand the **"Advanced options (demo / admin)"** expander
8. Locate the role selector dropdown inside the expander
9. Assert: **"Analyst"** is present as a selectable option
10. Select "Analyst" from the dropdown
11. Click the CTA button
12. Wait for spinner to disappear (timeout: **15 seconds**)
13. Assert: The Diagnostic page loads
14. If on an orientation screen, click through to begin
15. Assert: Question 1 is visible with a domain label/tag
16. Answer Question 1 (select any radio option or type a short response)
17. Assert: Question 2 loads successfully (confirms AN diagnostic flow is functional)

**State Verification:** Diagnostic page → profile created with `role_id = 'an'` confirmed.

---

#### UAT-15: Home Dashboard — All Modules Complete

**Purpose:** Verify the Home dashboard and Skills Profile render correctly when all 7 modules are complete.

**Pre-conditions:** Run `python scripts/reset_uat_user.py --profile all-done` before this scenario.

**Steps:**

1. Run `python scripts/reset_uat_user.py --profile all-done`
2. Navigate to `http://localhost:8501`
3. Assert: The Home dashboard loads (not Welcome or Diagnostic)
4. Assert: **All 7 module cards** are visible
5. Assert: Each module card shows a completed state — a score value is displayed on or near each card, OR a checkmark / "Complete" label is visible
6. Assert: **No module cards show a locked state** (no lock icons, no "locked" text on any of the 7 cards)
7. Assert: None of the 7 module CTAs say "Start Module" — CTAs should reflect already-completed state (e.g., "Review", "View Results", or similar)
8. Navigate to the Skills Profile page
9. Assert: "Your AI Skills Profile" heading is visible
10. Assert: The overall score value is ≥ 3.0 (seeded evaluation scores produce Proficient-level average)
11. Assert: At least one domain label shows "Proficient" or "Champion"
12. Assert: Gap map bullets are present (at least 3 visible — seeded from fixture data)
13. Assert: Assessment history section shows at least 1 row
14. Navigate back to Home and click on any completed module card
15. Assert: The module overview loads without error; step progress strip shows all 3 sub-modules as completed

---

#### UAT-16: Completed Module — Direct Results Navigation

**Purpose:** Verify that navigating to a module completed in a prior session shows the correct context-aware CTA and renders the Results sub-view without re-triggering AI scoring.

**Pre-conditions:** Run `python scripts/reset_uat_user.py --profile m1-done` before this scenario.

**Steps:**

1. Run `python scripts/reset_uat_user.py --profile m1-done`
2. Navigate to `http://localhost:8501`
3. Assert: The Home dashboard loads
4. Assert: Module 1 shows a completed state (score visible, or "Complete" label)
5. Assert: Module 2 shows an active/unlocked state (CTA is enabled, not locked)
6. Click on the Module 1 card
7. Assert: The Module 1 overview sub-view loads
8. Assert: The step progress strip shows all 3 sub-modules (Reading, Practice, Quiz) as **completed**
9. Assert: The primary CTA does **NOT** say "Start Reading" — it should reflect completion (e.g., "View Results", "Review", or "Go to Results")
10. Click the CTA to navigate to the Results sub-view
11. Assert: The Results sub-view loads
12. Assert: A module score value is visible (a decimal number between 0.0 and 4.0; should be near 2.8 from seeded data)
13. Assert: A coach note text block is visible and non-empty
14. Assert: **No loading spinner appeared** during navigation to Results (results load instantly from DB, no AI call re-triggered)
15. Navigate back to Home via the sidebar or link
16. Assert: Module 2 still shows as unlocked (state undisturbed by visiting Module 1)

---

#### UAT-17: MK Role Smoke Test — Welcome and Diagnostic Start

**Purpose:** Verify that the Marketing/Comms Advisor role is selectable via the Advanced Options expander and that an MK user can begin the diagnostic flow.

**Pre-conditions:** Run `python scripts/reset_uat_user.py` to wipe the test user before this scenario.

**Steps:**

1. Run `python scripts/reset_uat_user.py`
2. Navigate to `http://localhost:8501`
3. Assert: The Welcome page loads
4. Assert: "AI Hero Academy" text is visible
5. Assert: Pre-flight branding check passes (no "EDC" text)
6. Type into Q1: `I'm a marketing and communications advisor writing content, managing social channels, and coordinating internal communications. If AI could do one thing for me, it would be to generate a first draft of any communication from a brief.`
7. Expand the **"Advanced options (demo / admin)"** expander
8. Locate the role selector dropdown inside the expander
9. Assert: **"Marketing/Comms Advisor"** is present as a selectable option
10. Select "Marketing/Comms Advisor" from the dropdown
11. Click the CTA button
12. Wait for spinner to disappear (timeout: **15 seconds**)
13. Assert: The Diagnostic page loads (question counter or orientation screen visible)
14. If on an orientation screen, click through to begin
15. Assert: Question 1 is visible with a domain label/tag
16. Answer Question 1 (select any radio option or type a short response)
17. Assert: Question 2 loads successfully (confirms MK diagnostic flow is functional)

---

#### UAT-18: PM Role Smoke Test — Welcome and Diagnostic Start

**Purpose:** Verify that the Project Manager role is selectable via the Advanced Options expander and that a PM user can begin the diagnostic flow.

> **Note:** `--role pm` is NOT available in the reset script. Always use full-wipe reset for this scenario.

**Pre-conditions:** Run `python scripts/reset_uat_user.py` to wipe the test user before this scenario.

**Steps:**

1. Run `python scripts/reset_uat_user.py`
2. Navigate to `http://localhost:8501`
3. Assert: The Welcome page loads
4. Assert: "AI Hero Academy" text is visible
5. Assert: Pre-flight branding check passes (no "EDC" text)
6. Type into Q1: `I'm a project manager coordinating cross-functional teams, managing project timelines, and producing status reports. If AI could help, I'd want it to draft project status updates and risk logs from my rough notes automatically.`
7. Expand the **"Advanced options (demo / admin)"** expander
8. Locate the role selector dropdown inside the expander
9. Assert: **"Project Manager"** is present as a selectable option
10. Select "Project Manager" from the dropdown
11. Click the CTA button
12. Wait for spinner to disappear (timeout: **15 seconds**)
13. Assert: The Diagnostic page loads
14. If on an orientation screen, click through to begin
15. Assert: Question 1 is visible with a domain label/tag
16. Answer Question 1 (select any radio option or type a short response)
17. Assert: Question 2 loads successfully (confirms PM diagnostic flow is functional)

---

### Group E — 5-Persona Smoke Test (Quick Regression)

Use this group for a fast pre-deploy sanity check. Run each persona independently. The goal is to confirm routing, rendering, and no-traceback — not to exercise the full flow.

**How to use:** Run each persona in order. Each has its own reset command. Take a screenshot of the key page for each. Total runtime: ~10 minutes.

---

#### Persona 1: Fresh User → Welcome Page

**Reset:** `python scripts/reset_uat_user.py`

**Steps:**
1. Navigate to `http://localhost:8501`
2. Take screenshot
3. Assert: Welcome page renders (Q1 text area visible)
4. Assert: Pre-flight branding check passes (no "EDC" text)
5. Assert: No Python traceback or Streamlit error box

---

#### Persona 2: RM Post-Diagnostic → Skills Profile

**Reset:** `python scripts/reset_uat_user.py --role rm --diag`

**Steps:**
1. Navigate to `http://localhost:8501`
2. Take screenshot
3. Assert: Skills Profile page renders ("Your AI Skills Profile" heading visible)
4. Assert: Domain scores are visible with numeric values (not `None` or `null`)
5. Assert: Gap map section has at least 3 bullets
6. Assert: No Python traceback or Streamlit error box

---

#### Persona 3: RM Module 1 Unlocked → Home + Module Entry

**Reset:** `python scripts/reset_uat_user.py --profile course-built`

**Steps:**
1. Navigate to `http://localhost:8501`
2. Take screenshot
3. Assert: Home page shows module sequence (at least 7 cards)
4. Assert: Module 1 is unlocked/clickable (has a CTA button)
5. Click Module 1 CTA
6. Take screenshot
7. Assert: Module 1 Overview renders (module title and progress strip visible)
8. Assert: No Python traceback or Streamlit error box

---

#### Persona 4: RM Module 1 Complete → Home Completed State

**Reset:** `python scripts/reset_uat_user.py --profile m1-done`

**Steps:**
1. Navigate to `http://localhost:8501`
2. Take screenshot
3. Assert: Module 1 shows completed state (score visible on card)
4. Assert: Module 2 is unlocked (CTA button visible, no lock icon)
5. Assert: No Python traceback or Streamlit error box

---

#### Persona 5: RM All Modules Done → Home All-Complete State

**Reset:** `python scripts/reset_uat_user.py --profile all-done`

**Steps:**
1. Navigate to `http://localhost:8501`
2. Take screenshot
3. Assert: All 7 modules show completed state
4. Assert: Overall score visible (numeric value ≥ 3.0)
5. Assert: No module shows locked state
6. Assert: No Python traceback or Streamlit error box

---

## 5. Pass/Fail Criteria

### PASS — All of the following must be true:

- [ ] Pre-flight branding check passes on all pages tested (no "EDC" text visible)
- [ ] UAT-01 through UAT-12 completed without unhandled Python exceptions or error messages on the happy path
- [ ] UAT-13 UW smoke test confirms "Underwriter" is in the Advanced Options role selector
- [ ] UAT-14 AN smoke test confirms "Analyst" is in the Advanced Options role selector
- [ ] UAT-17 MK smoke test confirms "Marketing/Comms Advisor" is in the Advanced Options role selector
- [ ] UAT-18 PM smoke test confirms "Project Manager" is in the Advanced Options role selector
- [ ] UAT-15: Home shows all 7 module cards as complete with no locked state; Skills Profile shows Proficient-level score (≥ 3.0)
- [ ] UAT-16: Module 1 overview CTA reflects completion (not "Start Reading"); Results load without spinner
- [ ] Module 2 shows as unlocked after Module 1 evaluation completes (UAT-08 state verification)
- [ ] No Streamlit error box (red `st.error`) appeared for a system-level error during normal usage
- [ ] No `None`, `null`, `undefined`, or `[]` rendered as visible text on any page

### FAIL — Any one of the following triggers an overall FAIL:

- [ ] "EDC" text appears anywhere on screen during any scenario
- [ ] App shows an unhandled Python exception traceback on any happy path step
- [ ] A loading state (Analyzing / Scoring / Building / Personalizing) does not resolve within the stated timeout
- [ ] Module 2 remains locked after Module 1 evaluation completes
- [ ] "Underwriter" is missing from the role selector in the Advanced Options expander
- [ ] "Analyst" is missing from the role selector in the Advanced Options expander
- [ ] "Marketing/Comms Advisor" is missing from the role selector in the Advanced Options expander
- [ ] "Project Manager" is missing from the role selector in the Advanced Options expander
- [ ] Navigating away from a partial retake diagnostic wipes completed module progress
- [ ] UAT-15: Any module card shows a locked state or "Start Module" CTA with `--profile all-done` seeded
- [ ] UAT-16: Module 1 overview shows "Start Reading" CTA after `--profile m1-done` seed (context-aware CTA not working)
- [ ] UAT-16: A loading spinner appears when navigating to Results of an already-completed module (AI scoring re-triggered)
- [ ] Gap map renders with `None` or empty bullet text
- [ ] Welcome page CTA is blocked when Q1 has valid text (regression in form validation)

---

## 6. Known Limitations / Out of Scope

| Limitation | Reason |
|-----------|--------|
| AI coach text content is NOT asserted | LLM outputs vary per call |
| Modules 3–7 are not fully tested end-to-end | Structurally identical to Module 1; covered by pattern |
| Exact gap map bullet text is not asserted | AI-generated; varies per call |
| Mobile / responsive layout not tested | Desktop-first MVP (1280×800) |
| Manager dashboard not tested | Does not exist in MVP scope |
| UW/AN/MK/PM full module journey not tested | Smoke tests confirm onboarding; RM module journey covers the pattern |
| Error/failure path scenarios not tested | Graceful error messages tested only by inspection |
| Firestore writes not queried directly | App uses GCP Firestore — no SQL query layer; verification is via UI state transitions |
| Role inference via Q1 LLM parse not tested for edge cases | UAT uses Advanced Options expander for explicit role selection to ensure deterministic test outcomes |

---

## 7. Running UAT from the Master Session

> **Baseline eval harness**: The authoritative test matrix (41 checks, 9 personas, 38/41 release gate) lives at `.claude/evals/baseline-uat.md`. Read it before starting any baseline run.
>
> **Architecture note:** UAT is executed directly in the main Claude Code session — NOT in a
> sub-agent or a new session. The Playwright MCP tools (`mcp__playwright__browser_*`) are only
> available to the main session agent; the Databricks proxy strips `tool_reference` blocks before
> sub-agents can discover them. All browser calls must happen here.

### 7.1 Pre-run Checklist

Before issuing any UAT run command, verify all of the following in this session:

1. **Server health** — confirm `http://localhost:8501` returns HTTP 200:

   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://localhost:8501/
   ```

   If not `200`, start the server per Section 2.1 and wait for it to respond.

2. **Viewport set** — issue once per session before any navigation:

   ```python
   mcp__playwright__browser_resize(width=1280, height=800)
   ```

3. **Screenshot folder** — create a dated folder for this run's screenshots:

   ```bash
   git_sha=$(git rev-parse --short HEAD)
   mkdir -p tests/$(date +%Y-%m-%d)-${git_sha}
   echo "Screenshot dir: tests/$(date +%Y-%m-%d)-${git_sha}"
   ```

4. **MCP constraint reminder** — never delegate `mcp__playwright__*` calls to sub-agents; call them
   all directly in this session.

---

### 7.2 Full Suite (Groups A–D + E, all 18 scenarios)

Trigger a full UAT run by sending this instruction in the current session:

```
Execute the full UAT suite defined in UAT.md.

RULES:
- You are already in the master UAT session — call all mcp__playwright__browser_* tools directly.
  Never delegate them to sub-agents.
- Data layer is Firestore, NOT Databricks. Do NOT run SQL queries against mdlg_ai_shared.*.
  Write verification is via UI state transitions (Section 1.4).
- --role reset accepts: rm, uw, mk only. For AN and PM, use full-wipe reset.
- Every browser interaction: snapshot → get ref → act → wait_for.
- On failure: screenshot immediately, log [FAIL] UAT-NN: Step N — expected X, got Y, continue.
- Do NOT assert specific AI-generated text — only assert UI state and structural elements.

SEQUENCE:
1. Run pre-flight checks (Section 3).
2. Group A — reset: python scripts/reset_uat_user.py → run UAT-01.
3. Group B — reset: python scripts/reset_uat_user.py --role rm → run UAT-02, UAT-03.
4. Group C — reset: python scripts/reset_uat_user.py --profile course-built → run UAT-04 through UAT-12.
5. Group D — each scenario has its own reset (see Section 4) → run UAT-13 through UAT-18.
6. Group E — each persona has its own reset → run all 5 personas.

OUTPUT: Fill in and print the Test Execution Summary (Section 8) when all scenarios complete.
```

---

### 7.3 Quick Smoke Test (Group E — 5 personas, ~10 min)

```
Execute Group E (5-Persona Smoke Test) from UAT.md Section 4.

RULES:
- Call all mcp__playwright__browser_* tools directly in this session — not via sub-agents.
- Viewport must be 1280×800.

For EVERY persona in order:
1. Run its reset command (python scripts/reset_uat_user.py [options]).
2. Navigate to http://localhost:8501.
3. Take a screenshot — save to tests/<date>-<sha>/<persona-id>.png.
4. Assert: no "EDC" text, no Python traceback, no None/null rendered as visible text.
5. Assert the persona-specific conditions from UAT.md Section 4 Group E.

REPORT FORMAT (print after all 5):
| Persona | Reset cmd | Key page | Screenshot | Pass/Fail | Issues |

Flag issues with: exact page, element ref, observed vs expected. Do NOT fix — document only.
```

---

### 7.4 Atom-Path Home Smoke Test

For the atom-path Home branch (demo persona `3f` or reset `--profile course-built` with assembled path):

```
Execute atom-path Home checks using demo persona 3f.

1. mcp__playwright__browser_navigate(url="http://localhost:8501/?demo=true&profile=3f")
2. mcp__playwright__browser_snapshot()
3. Assert: domain badges are visible (not Read/Practice/Quiz sub-badges)
4. Assert: modules numbered 01–07 are present
5. Assert: "Start Module 1 →" CTA is visible and clickable
6. Click "Start Module 1 →"
7. Assert: reading content page loads (Concept/Example/Pitfall/Takeaway tabs visible)
8. Assert: no Python traceback, no EDC text, no None/null
```

---

### 7.5 Targeted Single Group

To run one group without re-running others, issue:

```
Execute only Group C (UAT-04 through UAT-12) from UAT.md.
Reset first: python scripts/reset_uat_user.py --profile course-built
Run pre-flight Section 3 checks, then proceed with UAT-04.
Call all mcp__playwright__browser_* tools directly — not via sub-agents.
```

Replace `Group C` / `UAT-04 through UAT-12` / reset command with the target group's values from Section 2.3.

---

## 8. Test Execution Summary Template

```
UAT Execution Date: ___________
App version / Git commit: ___________
Test user email: (from DEV_USER_EMAIL in .env)

PRE-FLIGHT:
Branding check (no EDC text): PASS / FAIL
App health check: PASS / FAIL

SCENARIO RESULTS:
-- Group A: Onboarding --
UAT-01: PASS / FAIL — notes

-- Group B: Diagnostic Journey --
UAT-02: PASS / FAIL — notes
UAT-03: PASS / FAIL — notes

-- Group C: Full Module Journey --
UAT-04: PASS / FAIL — notes
UAT-05: PASS / FAIL — notes
UAT-06: PASS / FAIL — notes
UAT-07: PASS / FAIL — notes
UAT-08: PASS / FAIL — notes
UAT-09: PASS / FAIL — notes
UAT-10: PASS / FAIL — notes
UAT-11: PASS / FAIL — notes
UAT-12: PASS / FAIL — notes

-- Group D: State Variants --
UAT-13: PASS / FAIL — notes
UAT-14: PASS / FAIL — notes
UAT-15: PASS / FAIL — notes
UAT-16: PASS / FAIL — notes
UAT-17: PASS / FAIL — notes
UAT-18: PASS / FAIL — notes

-- Group E: Persona Smoke Test --
Persona 1 (Fresh):     PASS / FAIL — screenshot:
Persona 2 (Post-diag): PASS / FAIL — screenshot:
Persona 3 (M1 unlock): PASS / FAIL — screenshot:
Persona 4 (M1 done):   PASS / FAIL — screenshot:
Persona 5 (All done):  PASS / FAIL — screenshot:

OVERALL RESULT: PASS / FAIL

FAILURES REQUIRING INVESTIGATION:
- [list any FAILs with screenshot references and reproduction steps]
```

---

## 9. Phase 3 Automated UAT — Results (2026-03-23)

### 9.1 Overview

Phase 3 automated UAT is covered by `tests/uat_phase3.js` — a self-contained Node.js Playwright script that exercises the demo persona infrastructure (`?demo=true&profile=<id>`) rather than the `reset_uat_user.py` workflow. It runs without the Playwright MCP server; any machine with Node.js and `playwright` npm installed can execute it.

**Run command:**
```bash
node tests/uat_phase3.js
```

**Prerequisites:**
- App running: `bash run_uat.sh` (port 8501, `LOCAL_UAT=true`)
- Demo personas auto-seeded on first navigation (handled by `utils/demo.py`)

**Result: 34/34 checks pass (81 s)**

Screenshots saved to `uat_screenshots/phase3/`.

---

### 9.2 Demo Persona Reference

| Profile ID | Label | Email | Purpose |
|-----------|-------|-------|---------|
| `3a` | Fresh user | `demo-fresh@demo.local` | Welcome page — intake form, validation |
| `3b` | RM at Diagnostic | `demo-rm-diag@demo.local` | Diagnostic start state |
| `3c` | UW, Module 1 complete | `demo-uw-m1@demo.local` | Legacy Home — Read/Practice/Quiz badges |
| `3d` | AN, all modules done | `demo-an-all@demo.local` | Legacy Home — all 7 scores visible |
| `3e` | MK, Module 3 in progress | `demo-mk-m3@demo.local` | Legacy Home — mixed states (2 of 7) |
| `3f` | RM, atom path | `demo-rm-atom@demo.local` | Atom-path Home — domain badges, Start Module |

Navigate to any persona: `http://localhost:8501/?demo=true&profile=<id>`

---

### 9.3 Scenario Results

| Scenario | Checks | Description | Result |
|----------|--------|-------------|--------|
| **A** | 5/5 | Welcome page: Q1 textarea, Q2 AI tools, Advanced options expander, no errors | ✅ PASS |
| **A2** | 6/6 | Atom-path Home (3f): domain badges visible, numbered 01–07, no legacy Read/Practice/Quiz | ✅ PASS |
| **B** | 4/4 | Click "Start Module 1 →" on atom-path Home → reading content page renders | ✅ PASS |
| **C** | 6/6 | Legacy UW Home (3c): Read/Practice/Quiz badges, Module 1 completed, locked modules present | ✅ PASS |
| **D** | 5/5 | Legacy AN Home (3d): "7 of 7" complete, ≥5 score values visible, no locked modules | ✅ PASS |
| **E** | 5/5 | Legacy MK Home (3e): mixed complete/active/locked, "2 of 7" visible | ✅ PASS |
| **F1** | 1/1 | Submit with empty Q1 → `st.error("Please describe your work before starting.")` appears | ✅ PASS |
| **F2** | 2/2 | Advanced options expander click → role selector options visible | ✅ PASS |
| **TOTAL** | **34/34** | | ✅ **ALL PASS** |

---

### 9.4 Key Implementation Notes (for future UAT runs)

**F1 validation — post-click, not disabled button:**
The "Start My Diagnostic" button on the Welcome page is **always enabled**. Empty Q1 validation fires *after* the button is clicked, via `st.error(t("welcome.error_q1_empty", _lang))`. The error text is `"Please describe your work before starting."`. Do NOT test `isDisabled()` — test for the error message appearing after a click.

**Atom-path vs legacy branch:**
The Home page branches on `get_assembled_path(user_email)`:
- Present → atom cards (domain badges, Start/Continue/Review buttons, no Read/Practice/Quiz badges)
- Absent → legacy numbered module list (Read/Practice/Quiz sub-badges, lock icons)

**Demo mode seeding:**
`ensure_demo_seeded(profile_id)` in `utils/demo.py` sets `_DEMO_SEED_IN_PROGRESS = True` before writing to Firestore, bypassing the `_is_demo_mode()` guard that would otherwise suppress DML. Seeding is idempotent — it wipes and re-seeds on each navigation to `?demo=true&profile=<id>`.

**Streamlit hot-reload warning:**
Editing `utils/demo.py` while Streamlit is running can cause a stale module cache leading to `ImportError` on the next page load. Always restart the Streamlit process after editing any file in `utils/`.
