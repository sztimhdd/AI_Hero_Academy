# UX Audit Report — Sprint 5
**Date:** 2026-03-27
**Auditor:** Playwright MCP + ui-ux-pro-max evaluation
**Scope:** 15 views × 3 viewports (375 / 768 / 1440px)
**Build:** Sprint 4 final (`npm run build` green after seed-dev.ts type fix)

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 1 |
| HIGH | 9 |
| MEDIUM | 7 |

**CRITICAL** issues block task completion and must be fixed before any UAT pass is possible.
**HIGH** issues degrade the core e-learning UX patterns and must be resolved before launch.
**MEDIUM** issues are documented for post-launch or low-effort opportunistic fixes.

---

## Console Errors Captured

| Screen | Error | Severity |
|--------|-------|----------|
| V4 — Onboarding S3 | `POST /api/diagnostic/generate-question → 500` (Gemini API key) | HIGH |
| V4 — Onboarding S3 | `POST /api/diagnostic/score → 401` (UAT bypass not applied) | CRITICAL |
| V14 — Credential | `GET /api/credential/share-card → ERR_EMPTY_RESPONSE` | HIGH |
| V14 — Credential | `Image without width/height props` warning | MEDIUM |

---

## Per-Screen Findings

### V1 — Landing / Sign-in
**375px / 768px / 1440px**
Screenshots: `V1-landing-375.png`, `V1-landing-768.png`, `V1-landing-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| — | Layout | OK | Content centred, no overflow |
| — | Touch | MEDIUM | Language toggle "中文" is text-only, no icon; 375px touch area acceptable |
| — | A11y | OK | Buttons have visible labels and role=button |

---

### V2 — Onboarding Screen 1 (Role + industry + daily work)
**375px / 768px / 1440px**
Screenshots: `V2-onboarding-s1-375.png`, `V2-onboarding-s1-768.png`, `V2-onboarding-s1-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| — | Touch | OK | Select dropdowns and textarea are full-width |
| — | Progress | MEDIUM | "Step 1 of 4" is plain text, no visual progress bar |
| — | Layout | OK | CTA "Next →" visible above fold at 375px |
| — | A11y | OK | Labels properly associated with controls |

---

### V3 — Onboarding Screen 2 (AI usage + motivation)
**375px / 768px / 1440px**
Screenshots: `V3-onboarding-s2-375.png`, `V3-onboarding-s2-768.png`, `V3-onboarding-s2-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| — | Touch | OK | Motivation buttons are full-width, ≥ 44px height |
| — | Layout | OK | Back + Next both visible, no overflow |
| — | A11y | OK | Motivation buttons have clear text labels |

---

### V4 — Onboarding Screen 3 (Diagnostic — 5 MCQ + 1 AI question)
**375px / 768px / 1440px**
Screenshots: `V4-onboarding-s3-375.png`, `V4-onboarding-s3-768.png`, `V4-onboarding-s3-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| C-01 | Auth / Error | **CRITICAL** | `POST /api/diagnostic/score` returns 401 in LOCAL_UAT mode — route bypasses `getAuthFromCookies()` and calls `verifySessionCookie()` directly. "Something went wrong. Please try again." shown. S4 gap map is completely unreachable. |
| H-01 | Error State | **HIGH** | `POST /api/diagnostic/generate-question` returns 500 (Gemini key unavailable in UAT). Fallback question renders but the API error appears in console. No visible loading/error indicator to the user. |
| — | Touch | OK | MCQ option buttons are full-width ≥ 44px height |
| — | Cognitive | MEDIUM | All 5 MCQ questions + 1 open question shown simultaneously — no progressive disclosure; long scroll on 375px |

---

### V5 — Onboarding Screen 4 (Gap map + Start Day 1 CTA)
**Status:** Unreachable due to C-01 (score API 401).
Screenshots taken reflect error state.

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| C-01 | Blocked | **CRITICAL** | Cannot reach S4 until C-01 is fixed. No gap map renders. No Start Day 1 CTA visible. |

---

### V6 — Dashboard
**375px / 768px / 1440px**
Screenshots: `V6-dashboard-375.png`, `V6-dashboard-768.png`, `V6-dashboard-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| H-02 | Touch | **HIGH** | Language toggle "EN" button: 41×28px (both dims < 44px). Not tappable on mobile. |
| H-03 | Touch | **HIGH** | "Sign out" button: 44×16px (height 16px — far below 44px minimum). Tapping is unreliable on mobile. |
| H-04 | A11y / State | **HIGH** | Day arc `available` and `in_progress` states use **color only** (blue vs amber). `StateIcon` returns `null` for these states. Spec requires icon + color + label for all 4 states. Only `locked` (padlock) and `complete` (checkmark) have icons. |
| — | A11y | MEDIUM | Streak counter number "1" has no `aria-label` describing what it counts |
| — | Touch | MEDIUM | Day arc timeline CTA links (`py-1.5` = 14px height + padding ≈ 28px total) — below 44px |
| — | Layout | OK | No overflow at 375px; horizontal scroll on arc timeline works |
| — | Empty State | OK | Artifact gallery empty state shows "Complete Day 1 to save your first artifact" ✓ |

---

### V7 — Day Page — Reading Tab
**375px / 768px / 1440px**
Screenshots: `V7-reading-375.png`, `V7-reading-768.png`, `V7-reading-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| H-05 | Layout/Readability | **HIGH** | Reading content `max-width: 896px` (~112ch). Spec requires `max-width: 72ch` for reading column. At 768px+, lines are too long — reduces readability. |
| H-06 | A11y | **HIGH** | "Good Example" and "Anti-Pattern" section headings use `h2` styled as `text-xs uppercase tracking-widest` (tiny decorative label). At 375px the `h2` tags are visually indistinguishable from body text labels. No semantic distinction visible in snapshot — a11y tree shows no `h2` heading for these sections. Reading `h2` is detected as "My Personal AI Tool Selection Checklist" (the artifact title), not section landmarks. |
| — | Touch | HIGH | "← Dashboard" back link: 86×20px (height 20px, < 44px) |
| — | Touch | OK | "Mark as Read" CTA button: `py-3 px-8` ≈ 48px height ✓ |
| — | Content | OK | Good Example (green) / Anti-Pattern (red) are colour + border coded; visually distinct |
| — | A11y | MEDIUM | `leading-relaxed` on body text ≈ 1.5 line-height. Spec wants 1.6+ |

---

### V8 — Day Page — Practice Tab (PACE coach chat)
**375px / 768px / 1440px**
Screenshots: `V8-practice-375.png`, `V8-practice-768.png`, `V8-practice-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| — | Task Progress | OK | "Task N of M" header is rendered (`p.text-xs text-slate-500 uppercase`) ✓ |
| — | Question Budget | OK | "Question N of 3" counter rendered in header panel ✓ |
| — | Streaming | OK | Streaming cursor `animate-pulse` is implemented ✓ |
| — | Bubbles | OK | User vs coach messages visually distinct (blue vs white/5) ✓ |
| — | Touch | OK | Send button `py-3 px-5` ≈ 48px height; textarea `py-3` ≈ accessible |
| H-07 | Touch | **HIGH** | "← Dashboard" back link (also on this page): 86×20px height < 44px |
| — | UX | MEDIUM | Send button text shows "…" during streaming — misleading; should show "Sending" or spinner with label |
| — | UX | MEDIUM | Task transition divider `─── Moving to Task N ───` is pure text with no visual break; at 375px it could be missed |

---

### V9 — Day Page — Quiz Tab
**375px / 768px / 1440px**
Screenshots: `V9-quiz-375.png`, `V9-quiz-768.png`, `V9-quiz-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| H-08 | Cognitive | **HIGH** | All 4 quiz questions shown simultaneously (no progressive disclosure). At 375px this requires ~3 full screens of scroll before reaching Submit. Increases cognitive load and risk of accidental scroll-past. |
| H-09 | A11y / State | **HIGH** | MCQ selected state uses **color only**: `bg-blue-600/30 border-blue-500/60`. No checkmark icon or "Selected" label added. Fails non-color-only requirement. |
| — | Touch | OK | MCQ option buttons `py-3 px-4` ≈ 48px height ✓ |
| — | Feedback | OK | Per-question number labels "Question N of M" rendered ✓ |
| — | Retry | OK | "Try Again" CTA prominent after fail ✓ |
| — | A11y | MEDIUM | Submit button disabled with no tooltip explaining why — user must scroll up to find unanswered question |

---

### V10 — Day Page — Build Tab
**375px / 768px / 1440px**
Screenshots: `V10-build-375.png`, `V10-build-768.png`, `V10-build-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| — | Layout | OK | No overflow at any viewport |
| — | Touch | OK | Textarea accessible; submit button ≥ 44px |
| — | A11y | OK | Heading + description present |

---

### V11 — Capstone Intro
**375px / 768px / 1440px**
Screenshots: `V11-capstone-intro-375.png`, `V11-capstone-intro-768.png`, `V11-capstone-intro-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| — | Layout | OK | No overflow; content above fold at 375px |
| — | Touch | OK | CTA buttons ≥ 44px |

---

### V12 — Capstone Challenge
**375px / 768px / 1440px**
Screenshots: `V12-capstone-challenge-375.png`, `V12-capstone-challenge-768.png`, `V12-capstone-challenge-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| — | Layout | OK | Task sections scroll correctly at 375px |
| — | Touch | OK | Input areas accessible |

---

### V13 — Capstone Results
**375px / 768px / 1440px**
Screenshots: `V13-capstone-results-375.png`, `V13-capstone-results-768.png`, `V13-capstone-results-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| — | Layout | OK | Results render without overflow |
| — | CTA | OK | Pass/fail CTAs visible above fold |

---

### V14 — Credential Page
**375px / 768px / 1440px**
Screenshots: `V14-credential-375.png`, `V14-credential-768.png`, `V14-credential-1440.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| H-10 | API Error | **HIGH** | `GET /api/credential/share-card` returns `ERR_EMPTY_RESPONSE`. Share card image fails to load — blank image box shown. LinkedIn share and download flows broken. |
| — | Layout | OK | Badge renders; PDF button visible |
| — | Touch | OK | LinkedIn and download buttons ≥ 44px |
| — | A11y | MEDIUM | Badge `<img>` missing `width`/`height` attributes (Next.js warning) |

---

### V15 — ZH Mobile Parity (375px)
**Screenshots:** `V15-zh-dashboard-375.png`, `V15-zh-practice-375.png`, `V15-zh-quiz-375.png`

| ID | Category | Severity | Finding |
|----|----------|----------|---------|
| — | Overflow | OK | No text overflow on dashboard at 375px ZH |
| — | Font | OK | CJK characters render correctly (system font stack) |
| — | Touch | HIGH | Same as H-02/H-03: EN/Sign out touch targets still < 44px in ZH mode |
| — | AI Terms | OK | LLM, API, JSON, GPT visible in EN within ZH content ✓ |
| — | Line-height | MEDIUM | ZH body text uses `leading-relaxed` (≈1.5). Spec requires 1.8 for CJK body |

---

## Touch Target Summary (375px scan)

| Element | Measured | Pass (≥44×44) |
|---------|----------|----------------|
| Language toggle "EN" | 41×28px | ❌ |
| Sign out button | 44×16px | ❌ height |
| "← Dashboard" back link | 86×20px | ❌ height |
| Day arc CTA links | ~128×28px | ❌ height |
| Unnamed icon button (header) | 32×32px | ❌ |
| MCQ option buttons | ~360×48px | ✅ |
| Quiz Submit button | ~360×48px | ✅ |
| Practice Send button | ~80×48px | ✅ |
| "Mark as Read" CTA | ~200×48px | ✅ |
| Motivation buttons (S2) | ~360×48px | ✅ |

---

## A11y Snapshot Summary

| Check | Result |
|-------|--------|
| Reading tab h2/h3 landmarks | ⚠️ Sections styled as `text-xs` decorative labels; not structural headings |
| Quiz question numbering | ✅ "Question N of M" present |
| Streak aria-label | ❌ Missing |
| Day arc state icon+label | ❌ Available/in-progress: color-only |
| MCQ selected state non-color | ❌ Color-only |
| Credential share card | ❌ Image load fails |
