# Sprint 4: B2C Program Completion
**Track:** B (Engineering)
**Depends on:** Sprint 3 (core learning loop), Sprint 1 capstone content (for E9)
**Estimated effort:** L

---

## Objective

Complete the full 7-day program experience: learner dashboard, Day 7 capstone challenge, credential issuance, and full EN/ZH bilingual parity. After this sprint, the product is end-to-end launchable: a learner can onboard, complete 7 days of AI-coached practice, pass the capstone, earn a shareable credential, and use the app in either English or Chinese.

---

## What Gets Built

**1. Dashboard + Streak Mechanics (E7)**

Route: `/dashboard` — authenticated home page after onboarding.

Components:
- **7-day arc timeline:** Day 0–7 cards with locked/available/in-progress/complete states. Active day = "Continue Day N" button.
- **Pillar badges:** 6 SVG badges. Grayscale = locked, colored = complete. Click → pillar name, score, artifact preview.
- **Streak counter:** `streak_days` from `user_profiles` with flame icon. "At risk" nudge if day not started by 20:00 local (client-side, no push notification yet).
- **Build artifact gallery:** Card grid from `build_artifacts`. Each card: type icon, title, day. "View/Copy" opens modal.
- **Profile pill:** display name, OAuth avatar, EN/ZH language toggle, logout.
- **Gap map delta:** before/after gap score comparison shown only after Day 7 capstone complete.

Streak update: `POST /api/streak/update` on session start — compares `last_active_date` to today, writes updated `streak_days` + `last_active_date`.

**2. Day 7 Capstone (E9)**

Route: `/day/capstone` — distinct experience, more immersive than daily modules.

Flow:
1. **Intro:** "Use your own AI tools during this challenge." Estimated time per task. "Begin" CTA.
2. **Challenge (4 mixed-input tasks):**
   - Tasks 1–2: Text input + streaming coach (same engine as Sprint 3, system prompt references all 6 pillars)
   - Task 3: MCQ cluster (3 items, no coach — assessment mode)
   - Task 4: File upload (screenshot of AI-generated output) → GCS signed URL → Gemini vision scoring via `/api/capstone/score-upload`
3. **Results:**
   - PASS (≥2.5/4.0): Celebration → calls `/api/credential/issue` → redirects to `/credential`
   - FAIL: Score breakdown + "Retake" CTA (no retry limit)

API routes:
- `POST /api/capstone/upload-url` — returns GCS signed URL for direct browser upload
- `POST /api/capstone/score-upload` — Gemini multimodal vision scores the screenshot analysis
- `POST /api/capstone/score` — aggregates all task scores, writes `training_progress/capstone`, triggers credential on pass

**3. Credential Generation (E8)**

Triggered by capstone pass. Route: `POST /api/credential/issue`.

Generates and stores in GCS bucket `ai-hero-academy-credentials/{user_email}/`:
- **Open Badge PNG** — SVG template → `sharp` PNG → Open Badges 3.0 metadata embedded
- **PDF certificate** — rendered via `puppeteer` on Cloud Run (learner name, date, score, pillar breakdown)
- **LinkedIn deep link** — `linkedin.com/profile/add?...` pre-composed with issuer, credential name, issue date, credential ID
- **Social share card** — 1200×630px PNG for LinkedIn/WeChat sharing

Credential page `/credential`: badge display, PDF download, LinkedIn add button, social share (LinkedIn, WeChat, copy link). `credentials` Firestore doc written with all asset URLs.

**4. EN/ZH i18n Port (E10)**

Makes the entire app bilingual using `next-intl`.

- Configure `next-intl` with EN + ZH locales
- Wire all hardcoded EN strings in TSX to `t('key')` calls
- New key namespaces: `onboarding.*`, `module.*`, `dashboard.*`, `credential.*`, `capstone.*`
- Language toggle in header: writes `user_profiles.lang` → used by coach engine to stream in ZH
- ZH coach language instruction: keep AI technical terms in EN (LLM, GPT, API, JSON, system prompt, temperature, tool names)
- Batch translate EN → ZH via Gemini Pro; spot-check 10%; test at 375px for layout overflow

---

## Acceptance Criteria

1. `/dashboard` renders all 5 components (arc, badges, streak, gallery, profile pill) ✅
2. Day arc shows correct lock/unlock states from `training_progress` ✅
3. Streak counter increments on daily session start ✅
4. Build artifact gallery shows all saved artifacts ✅
5. `/day/capstone`: all 4 task types render and submit ✅
6. File upload: GCS signed URL → browser direct upload → vision score returned ✅
7. Capstone PASS → `/api/credential/issue` called → `/credential` page shown ✅
8. Capstone FAIL → score breakdown + retake CTA ✅
9. Open Badge PNG generated and accessible at stable GCS URL ✅
10. PDF certificate downloadable ✅
11. LinkedIn deep link pre-composed and correct format ✅
12. Social share card 1200×630px generated ✅
13. Language toggle switches EN ↔ ZH across all pages ✅
14. `user_profiles.lang` written on language change ✅
15. Coach streams in ZH when `lang = "zh"` ✅
16. No text overflow in ZH at 375px mobile ✅
17. AI technical terms kept in EN within ZH copy ✅

## UAT Checkpoint

**Type: Full end-to-end launch UAT (Playwright MCP, remote Cloud Run) — release gate**

This is the launch UAT. All tests run against the deployed Cloud Run URL. Pass = cleared for public launch.

**Part A — Dashboard (Playwright MCP, remote)**
```
Persona: seed user with Days 1–3 complete (scripts/seed-dev.ts Day3 fixture)

UAT-S4-1:  /dashboard renders all 5 components
UAT-S4-2:  Day arc: Days 1–3 complete, Day 4 available, Days 5–7 locked
UAT-S4-3:  Streak counter shows correct value from user_profiles.streak_days
UAT-S4-4:  Build artifact gallery shows artifacts from Days 1–3
UAT-S4-5:  Language toggle switches EN ↔ ZH across all dashboard text
```

**Part B — Capstone (Playwright MCP, remote)**
```
Persona: seed user with Days 1–6 complete (scripts/seed-dev.ts Day6 fixture)

UAT-S4-6:  /day/capstone intro screen renders with "Begin" CTA
UAT-S4-7:  Task 1 text input + streaming coach response works
UAT-S4-8:  Task 3 MCQ cluster: all 3 items render, selections recorded
UAT-S4-9:  Task 4 file upload: GCS signed URL returned, browser upload succeeds
UAT-S4-10: Gemini vision score returned within 30s for uploaded screenshot
UAT-S4-11: Capstone PASS (≥2.5) → /api/credential/issue called → /credential redirect
UAT-S4-12: Capstone FAIL (<2.5) → score breakdown shown + retake CTA present
```

**Part C — Credential (Playwright MCP, remote)**
```
UAT-S4-13: /credential page renders badge, PDF link, LinkedIn button, share card
UAT-S4-14: PDF certificate URL is accessible (HTTP 200)
UAT-S4-15: LinkedIn deep link has correct format (startTask=CERTIFICATION_NAME)
UAT-S4-16: Social share card image URL is accessible (HTTP 200, 1200×630px)
```

**Part D — ZH parity (Playwright MCP, remote)**
```
UAT-S4-17: All /dashboard strings render in ZH when lang=zh (no EN bleed)
UAT-S4-18: /day/p1 coach streams ZH response when lang=zh
UAT-S4-19: No text overflow at 375px viewport in ZH (screenshot check)
UAT-S4-20: AI technical terms (LLM, API, JSON, temperature) kept in EN within ZH copy
```

**Part E — Legacy Streamlit final regression (Playwright MCP, local port 8501)**
Run `.claude/evals/baseline-uat.md` — must pass **38/41**.
This is the final legacy check before public launch. G2a or G4 failure blocks launch.

**Release gate: 18/20 B2C tests + 38/41 legacy tests.**
Any failure in UAT-S4-11 (credential issue), UAT-S4-9 (file upload), or UAT-S4-18 (ZH coach) blocks launch regardless of total score.

## Key Constraints

- GCS for all credential assets — not Firestore, not CDN-less
- Gemini multimodal for vision scoring — no third-party vision API
- LinkedIn deep link standard format (same as Google, Coursera, Credly)
- `next-intl` for i18n — not `next-i18next`
- No traditional Chinese (ZH-TW), no WeChat OAuth, no push notifications this sprint

## Out of Scope

- ZH translation of pillar content JSON (future content sprint)
- Push notifications / streak reminders (post-MVP)
- Manager/employer dashboard (B2B feature, permanently out of scope)
- Credential verification endpoint (post-MVP)
