# B2C Demo UAT Report

**Date:** 2026-03-30 (re-run after fix sprint)
**Tester:** Claude Code (automated Playwright)
**Environment:** Production — Cloud Run `ai-hero-academy-b2c` (project `banded-totality-485901`, region `us-central1`)
**Demo URL:** `https://ai-hero-academy-b2c-r5uua4chza-uc.a.run.app/demo?t=07b731f4f039ff5740d366e909b84f8e`
**Branch:** `main` @ `d6c7979`

---

## Executive Summary

| Personas Tested | PASS | FAIL | WARN |
|----------------|------|------|------|
| 5              | 5    | 0    | 0    |

**Overall: RELEASE-GATE READY** — all 5 personas pass, 0 JS console errors, share card renders correctly.

---

## Fixes Applied This Session

| # | Issue (from prior UAT) | Fix | Commit |
|---|----------------------|-----|--------|
| 1 | Share card 503 — Satori `clipPath`/emoji crash killed container | Replaced with `borderRadius: 50%`, merged text+expression template literals, forced `await img.arrayBuffer()` inside try/catch | `f85b3d8` |
| 2 | Build artifacts empty for `day3`/`day6` personas | Seeded `b2c_build_artifacts` collection in `demo-login` route | `f85b3d8` |
| 3 | Dashboard loads in wrong language (stale `NEXT_LOCALE` cookie) | Dashboard now reads locale from Firestore `user.lang` instead of cookie | `d6c7979` |

---

## Persona Results

### 1. `onboarding` → `/onboarding` ✅ PASS

**Redirect:** Demo page → `/onboarding` ✅
**Auth:** Session cookie set, middleware allows through ✅

**Onboarding flow (all 4 screens verified):**

| Screen | Status | Notes |
|--------|--------|-------|
| Screen 1 — Work Context | ✅ | Role, industry, daily work fields render; validation works |
| Screen 2 — AI Journey | ✅ | AI usage + motivation form, Next button enables on complete |
| Screen 3 — Quick Diagnostic | ✅ | 5 MCQ + 1 open-text AI question rendered |
| Screen 4 — Gap Map | ✅ | Gemini scoring completes; 6 domain scores displayed (Overall: 92, Ethics & Risk: 50 lowest); "Start Day 1" CTA present |

**Console errors:** 0

---

### 2. `day1` → `/day/p1` ✅ PASS

**Redirect:** Demo page → `/day/p1` ✅

**Day page state:**
- Reading tab active, full content rendered ✅
- Practice, Quiz, Build tabs locked ✅

**Console errors:** 0

---

### 3. `day3` → `/dashboard` ✅ PASS

**Redirect:** Demo page → `/dashboard` ✅

**Dashboard state:**
- 3-day streak displayed ✅
- Days 1–3 marked complete ✅
- Day 4 shown as next available ("Start") ✅
- Days 5–7 locked ✅
- Pillar Badges section visible ✅
- **Build Artifacts (3)** — all 3 artifacts shown ✅ (was empty in prior UAT)
- **Language: English** (with cleared cookies) ✅ (was showing Chinese in prior run due to stale cookie — fixed)

**Console errors:** 0

---

### 4. `day6` → `/dashboard` ✅ PASS

**Redirect:** Demo page → `/dashboard` ✅

**Dashboard state:**
- 6-day streak displayed ✅
- Days 1–6 all marked complete ✅
- Capstone (Day 7) shown as "Start" ✅
- All 6 pillar badges visible ✅
- **Build Artifacts (6)** — all 6 artifacts shown ✅ (was empty in prior UAT)

**Console errors:** 0

---

### 5. `credential` → `/credential` ✅ PASS

**Redirect:** Demo page → `/credential` ✅

**Credential page content:**
- "Congratulations, Demo User!" heading ✅
- Overall score: 3.8/4.0 ✅
- All 6 pillar scores: 2/2 ✅
- LinkedIn, PDF, Copy Link, Back to Dashboard buttons all present ✅

**Share Card Image:**
- Renders correctly as inline PNG ✅
- `GET /api/credential/share-card?uid=demo-credential` → `200 OK`, `image/png` ✅
- Card shows: AI circle badge, "AI-Supercharged Intermediate", "Demo User", "Score: 3.8/4.0", all P1–P6 pillar scores ✅

**Console errors:** 0

---

## Release Gate

| Check | Status |
|-------|--------|
| All 5 personas reachable via demo URL | ✅ |
| Auth + session cookie flow | ✅ |
| Onboarding 4-screen flow end-to-end | ✅ |
| Gemini diagnostic scoring | ✅ |
| Gap Map renders with real scores | ✅ |
| Day page content renders | ✅ |
| Dashboard streak + progress | ✅ |
| Build Artifacts populated for day3/day6 | ✅ |
| Credential page renders with scores | ✅ |
| Share card image loads (200 OK, image/png) | ✅ |
| Dashboard loads in correct language (Firestore lang) | ✅ |
| Zero JS console errors per persona | ✅ |

**RELEASE-GATE READY.**
