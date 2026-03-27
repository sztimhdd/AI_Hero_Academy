# UX Issue Backlog — Sprint 5
**Generated:** 2026-03-27
**Tool:** ui-ux-pro-max Priority Framework (P1–P5 = launch gate; P6–P10 = MEDIUM only)
**HITL Sign-off:** ✅ APPROVED 2026-03-27 — all CRITICAL and HIGH items implemented in E13. See `plans/b2c-s5-uat-report.md` for verification.

---

## HITL Approval Header

> **Action required:** Review severities below. Promote/demote items or add notes before E13 begins.
> Sign off by replying with "Backlog approved" or listing specific changes.

---

## CRITICAL Issues (1)

| ID | Screen | Category | Severity | Description | Current | Expected | Screenshot |
|----|--------|----------|----------|-------------|---------|----------|------------|
| C-01 | V4 Onboarding S3, V5 S4 | Auth/Error | **CRITICAL** | `/api/diagnostic/score` and `/api/diagnostic/generate-question` call `verifySessionCookie()` directly — they do not use `getAuthFromCookies()` which has the LOCAL_UAT bypass. In UAT mode both routes return 401/500. Clicking "See My Gap Map →" shows "Something went wrong." S4 gap map is completely unreachable. | "Something went wrong. Please try again." error banner; user stuck on S3 | Score route and generate-question route must call `getAuthFromCookies()` (or add their own LOCAL_UAT bypass inline). S4 gap map renders after successful score submission. | `V4-onboarding-s3-375.png` |

---

## HIGH Issues (9)

| ID | Screen | Category | Severity | Description | Current | Expected | Screenshot |
|----|--------|----------|----------|-------------|---------|----------|------------|
| H-01 | V4 S3 | Error State | HIGH | No visible error/loading indicator for AI personalised question generation. Gemini call fails silently (console 500); fallback textarea appears but user sees no explanation. | Textarea appears without explanation | Show "Generating your personalised question…" spinner, or on error show "Using a standard question" notice | `V4-onboarding-s3-375.png` |
| H-02 | V6 Dashboard | Touch | HIGH | Language toggle "EN" button: 41×28px — both width and height below 44px minimum. Unreliable to tap on mobile. | 41×28px | ≥ 44×44px tap target (add padding) | `V6-dashboard-375.png` |
| H-03 | V6 Dashboard | Touch | HIGH | "Sign out" button: 44×16px — height 16px, far below minimum. | 44×16px | ≥ 44px height (add py-3 minimum) | `V6-dashboard-375.png` |
| H-04 | V6 Dashboard | A11y/State | HIGH | Day arc `available` and `in_progress` states use color only. `StateIcon` returns null for both. At 375px in grayscale or for color-blind users, states are indistinguishable. Spec: icon + color + label for all states. | Locked=🔒, Complete=✓, Available=no icon, In-progress=no icon | Available=▶ icon, In-progress=⏳ or ◉ icon (distinct from locked/complete) | `V6-dashboard-375.png` |
| H-05 | V7 Reading | Layout/Readability | HIGH | Reading content `max-width: 896px` (~112ch). At 768px and 1440px lines are excessively long, straining readability. Spec: `max-width: 72ch`. | `max-w-[896px]` on outer container | Add `max-w-[72ch]` or `max-w-prose` to reading content wrapper | `V7-reading-1440.png` |
| H-06 | V7 Reading | A11y | HIGH | "Good Example" / "Anti-Pattern" / "Key Takeaway" sections use `h2` but styled as `text-xs uppercase tracking-widest` — renders as tiny decorative labels, not readable section headings. Accessibility tree shows artifact title as only h2. Section purpose unclear to screen-reader users. | `<h2 class="text-xs font-semibold text-green-400 uppercase tracking-widest">` | Use semantic section labels that are visually readable (e.g. `text-sm font-semibold` + icon prefix ✅ / ❌ / 💡) | `V7-reading-375.png` |
| H-07 | V7, V8 | Touch | HIGH | "← Dashboard" back link: 86×20px (height 20px). Present on every day page. Users reliably miss it on mobile when tapping back. | `<a>` with no padding | Add `py-3 px-2` minimum to expand tap target to ≥ 44px | `V7-reading-375.png` |
| H-08 | V9 Quiz | Cognitive | HIGH | All 4 quiz questions displayed simultaneously — no progressive disclosure. On 375px requires ~3 full screens of scroll. Increases cognitive load and scroll-past risk before Submit. | 4 questions in one scrollable column | Show one question at a time with Next/Previous controls, or show numbered visible question + clear visual separator with sticky question counter | `V9-quiz-375.png` |
| H-09 | V9 Quiz | A11y/State | HIGH | MCQ selected state: `bg-blue-600/30 border-blue-500/60 text-blue-100` — color only, no icon or label. At 375px against dark background the contrast difference is subtle. Fails non-color-only requirement. | Color-only selected highlight | Add `✓` checkmark icon before the selected option key, or "Selected" visually-hidden label + visible border width change | `V9-quiz-375.png` |
| H-10 | V14 Credential | API Error | HIGH | `GET /api/credential/share-card` returns `ERR_EMPTY_RESPONSE`. Share card image box is blank. LinkedIn share button references broken image URL. Breaks the key shareable credential flow. | Blank image box + broken LinkedIn share | Share-card route must return a valid image response (or graceful error with placeholder) | `V14-credential-375.png` |

---

## MEDIUM Issues (7 — post-launch backlog)

| ID | Screen | Category | Description | Estimate |
|----|--------|----------|-------------|----------|
| M-01 | V2–V5 Onboarding | Progress | "Step N of 4" is plain text only — no visual progress bar. Users can't scan overall progress at a glance. | 1h |
| M-02 | V4 S3 Diagnostic | Cognitive | All 5 MCQ + 1 open question shown simultaneously (long scroll at 375px). Same pattern as H-08 but lower impact since it's a one-time onboarding experience. | 2h |
| M-03 | V6 Dashboard | A11y | Streak counter number lacks `aria-label` (e.g. `aria-label="1 day streak"`). Screen reader reads bare "1". | 0.5h |
| M-04 | V7 Reading | Typography | `leading-relaxed` ≈ 1.5 line-height. Spec requires 1.6+ for EN body text. Change to `leading-[1.65]` or `leading-loose`. | 0.5h |
| M-05 | V8 Practice | UX | Send button text "…" during streaming is ambiguous. Replace with "Sending" text or spinner + label. | 0.5h |
| M-06 | V14 Credential | A11y | Badge `<img>` missing `width`/`height` causing Next.js layout shift warning. | 0.5h |
| M-07 | V15 ZH | Typography | ZH body text uses `leading-relaxed` (≈1.5). CJK spec requires 1.8. Add `lang="zh"` aware line-height via Tailwind or CSS var. | 1h |

---

## Issues Out of Scope for E13

Per sprint rules (no new features, no backend changes):
- M-02: Diagnostic progressive disclosure requires content rework — post-launch
- Any new API routes

---

## Implementation Priority for E13

Execute in this order:
1. **C-01** — Auth bypass fix (unblocks V5 and all UAT tests)
2. **H-10** — Share-card API fix (unblocks credential UAT)
3. **H-02 + H-03 + H-07** — Touch targets (same PR, same component area)
4. **H-04** — Day arc state icons (dashboard)
5. **H-08** — Quiz progressive disclosure
6. **H-09** — MCQ selected state icon
7. **H-05** — Reading max-width
8. **H-06** — Reading section heading style
9. **H-01** — Diagnostic AI question loading state
