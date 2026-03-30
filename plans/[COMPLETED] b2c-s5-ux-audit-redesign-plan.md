# Sprint 5: UX Audit & Redesign
**Track:** B (Design × Engineering)
**Depends on:** Sprint 4 complete (all 15 screens exist and are functional)
**Estimated effort:** M

---

## Objective

Systematic UI/UX quality pass across all 15 post-S4 screens before public launch. Uses Playwright to screenshot every screen at three viewports, ui-ux-pro-max to evaluate each screen against its 10-category priority framework, and a HITL redesign loop to resolve all CRITICAL and HIGH severity issues. Outcome: 0 CRITICAL defects, 0 HIGH defects, and a documented MEDIUM backlog for post-launch. Does not introduce new features — UI/UX only.

---

## Screen Inventory (15 views)

| # | Route | View |
|---|-------|------|
| V1 | `/` | Landing / sign-in |
| V2 | `/onboarding` | Screen 1 — Role + industry + daily work |
| V3 | `/onboarding` | Screen 2 — AI usage + motivation |
| V4 | `/onboarding` | Screen 3 — Diagnostic (5 MCQ + 1 AI question) |
| V5 | `/onboarding` | Screen 4 — Gap map + Start Day 1 CTA |
| V6 | `/dashboard` | Day arc + pillar badges + streak + artifact gallery + profile pill |
| V7 | `/day/[pillar_id]` | Reading tab |
| V8 | `/day/[pillar_id]` | Practice tab (PACE coach chat) |
| V9 | `/day/[pillar_id]` | Quiz tab (3 MCQ + 1 open) |
| V10 | `/day/[pillar_id]` | Build tab (artifact editor) |
| V11 | `/day/capstone` | Capstone intro screen |
| V12 | `/day/capstone` | Capstone challenge (4 task types) |
| V13 | `/day/capstone` | Capstone results (PASS + FAIL states) |
| V14 | `/credential` | Badge + PDF link + LinkedIn button + share card |
| V15 | ZH parity | V6 + V8 + V9 at 375px in Chinese |

---

## What Gets Built

**1. Playwright Audit Sweep (E11)**

Automated Playwright sweep capturing evidence for every screen before any redesign work begins. All screenshots saved to `ux-audit/screenshots/`. Audit report written to `ux-audit/audit-report.md`.

Per screen, capture:
- Screenshots at 375px, 768px, 1440px viewport width
- `browser_console_messages` — flag any `[error]` entries
- `browser_snapshot` — accessibility tree for a11y checks (focus order, aria-labels, heading hierarchy)
- Touch target size scan: any interactive element with bounding box `< 44×44px` flagged

Seed users required:
- V1–V5: fresh unauthenticated session
- V6–V10: `scripts/seed-dev.ts` Day 3 fixture (Days 1–3 complete, Day 4 available)
- V11–V13: Day 6 fixture (Days 1–6 complete)
- V14: post-capstone-pass fixture (credential issued)
- V15: Day 3 fixture + `lang=zh` set in `b2c_user_profiles`

Output per screen: `V{N}-{view-name}-{viewport}.png`, console log, a11y snapshot.

**2. ui-ux-pro-max Evaluation & Issue Backlog (E12)**

Each screen evaluated against ui-ux-pro-max's 10-category priority framework. Evaluation focused on priority tiers 1–5 (Accessibility → Touch → Performance → Style → Layout/Responsive) as launch-gate criteria. Tiers 6–10 produce MEDIUM backlog items only.

Severity definitions:
- **CRITICAL** — blocks task completion, crashes, 0 WCAG AA contrast, no keyboard nav, completely broken layout
- **HIGH** — poor e-learning UX pattern, touch target < 44px, broken ZH at 375px, coach chat unreadable, quiz feedback absent, missing loading/error states
- **MEDIUM** — improvement opportunity; does not block use; documented for post-launch

Issue backlog written to `ux-audit/issue-backlog.md` with columns: `ID | Screen | Category | Severity | Description | Current behaviour | Expected behaviour | Screenshot ref`.

**HITL gate before E13:** User reviews and approves/promotes/deprioritizes the backlog. Severity changes must be co-signed. No redesign starts without HITL approval on the backlog.

**3. Redesign & Implement (E13)**

Implement all approved CRITICAL and HIGH issues. MEDIUM issues implemented only if estimated < 2h; otherwise logged to post-launch backlog.

E-learning UX patterns to apply where flagged (sourced from industry research):
- **Reading tab:** Content hierarchy with `h2`/`h3` landmarks, `good-example` / `anti-pattern` clearly visually distinguished (color + icon), key takeaway visually prominent, sufficient line-height (1.6+), `max-width: 72ch` for readability column
- **Practice (coach chat):** Message bubbles clearly separated user vs. coach, streaming indicator (typing animation), task progress "Task N of 4" always above-fold, question budget indicator "Question N of 3" visible per task (PACE model — removes anxiety about endless questioning), explicit visual closure moment when task exits early on mastery (brief beat before advancing — learner feels completion, not truncation), bridge statement at task end always visible (one-line coach close linking to what's next — never ends mid-air), input field ≥ 44px touch height, send button always visible (not hidden behind keyboard on mobile)
- **Quiz tab:** One question visible at a time (progressive disclosure) or clearly numbered, MCQ options ≥ 44px tap height, selected state unambiguous (not color-only), score feedback below each question on submit (not only at top), retry CTA visually prominent on fail
- **Dashboard:** Day arc timeline scannable left-to-right, locked/available/complete states use icon + color + label (not color-only), streak counter uses `aria-label`, artifact gallery empty state is helpful ("Complete Day 1 to save your first artifact")
- **Onboarding:** One question per screen (no cognitive overload), progress indicator always visible, back navigation never loses input, CTA always above fold on mobile
- **ZH-specific:** Line-height 1.8 for CJK body text, PingFang SC / Noto Sans SC system stack, no letter-spacing reduction on Chinese, AI technical terms (LLM, API, JSON, GPT, temperature, system prompt) kept in EN

Per fix: before screenshot + code change + after screenshot. Max 3 HITL rounds per screen — accept best approved design and move on.

No backend changes permitted in this sprint. UI components and CSS/Tailwind only.

**4. ZH Mobile Parity Pass (E14)**

Dedicated pass at 375px in Chinese for all redesigned screens. Checks:
- No text overflow or truncation
- Touch targets ≥ 44px on all interactive elements
- CJK font stack renders (not fallback to serif)
- AI technical terms remain in EN within ZH copy
- Language toggle accessible and functional

---

## Acceptance Criteria

1. All 15 screens captured at 375/768/1440px with no unreported console errors ✅
2. `ux-audit/audit-report.md` exists with per-screen severity-tagged findings ✅
3. `ux-audit/issue-backlog.md` exists; all items HITL-reviewed and severity approved ✅
4. 0 CRITICAL issues remain in re-audit run after E13 ✅
5. 0 HIGH issues remain in re-audit run after E13 ✅
6. All MEDIUM issues documented in post-launch backlog ✅
7. Reading tab: content hierarchy landmarks, example/anti-pattern distinguished, `max-width: 72ch` ✅
8. Coach chat: user/coach bubbles distinct, streaming indicator, task + question progress indicators always visible, visual closure on mastery exit ✅
9. Quiz: progressive disclosure or clear numbering, MCQ ≥ 44px, selected state not color-only ✅
10. Dashboard: locked/available/complete uses icon + color + label (not color-only) ✅
11. All interactive elements ≥ 44×44px touch target on mobile ✅
12. ZH at 375px: no overflow on any redesigned screen ✅
13. Before/after Playwright screenshots committed for every fixed issue ✅

---

## UAT Checkpoint

**Type: Visual regression + a11y audit (Playwright MCP, local + remote Cloud Run)**

**Part A — Audit Coverage (Playwright MCP, local)**
```
UAT-S5-1:  All 15 screens screenshot-captured at 375/768/1440px
UAT-S5-2:  No [error] console entries on any screen (console check)
UAT-S5-3:  audit-report.md committed with severity tags on all screens
UAT-S5-4:  issue-backlog.md committed; HITL sign-off noted in backlog header
```

**Part B — CRITICAL / HIGH Resolution (Playwright MCP, local)**
```
Seed: Day3 fixture + Day6 fixture + post-pass credential fixture

UAT-S5-5:  Re-audit: 0 CRITICAL issues flagged by ui-ux-pro-max on any screen
UAT-S5-6:  Re-audit: 0 HIGH issues flagged by ui-ux-pro-max on any screen
UAT-S5-7:  All MEDIUM issues present in post-launch-backlog.md
```

**Part C — E-Learning UX Patterns (Playwright MCP, local)**
```
UAT-S5-8:  Reading tab: content sections have visible h2/h3 landmarks (a11y snapshot)
UAT-S5-9:  Reading tab: good-example and anti-pattern visually distinct at 375px (screenshot)
UAT-S5-10: Coach chat: user vs coach message bubbles visually distinct (screenshot)
UAT-S5-11: Coach chat: "Task N of 4" AND "Question N of 3" indicators both visible without scrolling at 375px
UAT-S5-12: Quiz: MCQ options bounding box ≥ 44px height (evaluate snapshot)
UAT-S5-13: Quiz: selected MCQ state uses icon or label, not color alone (screenshot)
UAT-S5-14: Dashboard: locked/available/complete state uses icon + text (not color-only) (snapshot)
UAT-S5-15: All interactive elements ≥ 44×44px touch target on V6, V8, V9 (evaluate snapshot)
```

**Part D — ZH Mobile Parity (Playwright MCP, local, 375px)**
```
Seed: Day3 fixture with lang=zh

UAT-S5-16: No text overflow on /dashboard at 375px in ZH (screenshot)
UAT-S5-17: No text overflow on /day/[pillar_id] Practice tab at 375px in ZH (screenshot)
UAT-S5-18: No text overflow on /day/[pillar_id] Quiz tab at 375px in ZH (screenshot)
UAT-S5-19: AI technical terms (LLM, API, JSON, temperature) remain EN in ZH copy (snapshot text check)
```

**Part E — Legacy regression (Playwright MCP, local port 8501)**
```
Run .claude/evals/baseline-uat.md — must pass 38/41.
```

**Release gate: 19/19 S5 tests + 38/41 legacy.**
Any failure in UAT-S5-5 (0 CRITICAL) or UAT-S5-6 (0 HIGH) blocks launch regardless of total score.

---

## Key Constraints

- **ui-ux-pro-max skill is mandatory** for every issue evaluation — no gut-feel severity assignments
- **HITL approval required** before implementing any screen redesign (E12 → E13 gate)
- **Max 3 HITL rounds per screen** — accept best approved design, log remainder to backlog
- **Before/after Playwright screenshots** required for every fixed issue — no code-only fixes
- **No new features** — this sprint is UI/UX only; no new API routes, no schema changes
- **No backend changes** — components and CSS/Tailwind only
- **ZH copy:** no new machine translation; adapt from existing ZH map patterns established in vision.html
- All fixes must pass `npm run build` + `npm run lint` before marking complete

---

## Out of Scope

- New features or content changes (Sprint 4 scope)
- Performance optimization / bundle splitting (post-launch sprint)
- Motion / animation system overhaul (post-launch sprint)
- Native mobile app shell
- New language locales beyond EN/ZH
- Credential page visual design iteration (covered by E13 if HIGH issues found)
- Backend or API changes of any kind
