# Kickstart: Sprint 5 — UX Audit & Redesign
**Full plan:** `plans/b2c-s5-ux-audit-redesign-plan.md`

---

## What to Read First

1. `plans/b2c-s5-ux-audit-redesign-plan.md` — full spec: screen inventory, issue severity definitions, e-learning UX patterns, UAT
2. `~/.claude/skills/ui-ux-pro-max/` — full skill: 10-category priority framework, priority 1–5 are launch-gate criteria
3. `.claude/evals/baseline-uat.md` — legacy regression suite (must pass 38/41 at end of sprint)
4. `scripts/seed-dev.ts` — seed fixtures needed for audit (Day3, Day6, post-pass)

**Prerequisites:** Sprint 4 complete. All 15 screens exist and are functional. `npm run build` green. Cloud Run deployed.

---

## What to Build

Build in strict phase order — do NOT start E13 before HITL backlog approval.

**E11 — Playwright Audit Sweep**
Automated screenshot of all 15 screens × 3 viewports (375/768/1440px). Console error capture. A11y snapshot. Touch target size check (< 44×44px flagged). Output: `ux-audit/screenshots/` + `ux-audit/audit-report.md` with per-screen severity tags.

Seed requirements: Day3 fixture (V6–V10), Day6 fixture (V11–V13), post-pass credential fixture (V14), ZH Day3 fixture (V15).

**E12 — ui-ux-pro-max Evaluation & HITL Backlog**
Run ui-ux-pro-max skill against every screenshot. Evaluate priority 1–5 for CRITICAL/HIGH. Priority 6–10 produce MEDIUM only. Write `ux-audit/issue-backlog.md`.

**HITL gate**: Present backlog to user. Get approval before any implementation. Document approved severity in backlog header.

**E13 — Redesign & Implement**
Implement all CRITICAL and HIGH issues. MEDIUM if < 2h estimate. Max 3 HITL rounds per screen. Before/after screenshot pair per fix. No backend changes.

Key e-learning UX patterns to apply:
- Reading: content hierarchy landmarks, example/anti-pattern distinguished, `max-width: 72ch`
- Coach chat: distinct bubbles, streaming indicator, task progress above-fold, ≥ 44px input
- Quiz: progressive disclosure, ≥ 44px MCQ options, non-color-only selected state, per-question feedback
- Dashboard: icon + color + label for arc states (not color-only), helpful empty states

**E14 — ZH Mobile Parity**
375px pass on all redesigned screens in Chinese. No overflow, CJK font stack, AI terms in EN, touch targets ≥ 44px.

---

## Non-Negotiable Rules

- ui-ux-pro-max skill for every severity rating — no gut-feel calls
- HITL approval gates E12 → E13 — no implementation without signed-off backlog
- Before/after Playwright screenshots for every fix — committed to `ux-audit/screenshots/`
- Max 3 HITL rounds per screen — take the best approved design
- No new features, no backend changes, no schema changes
- ZH copy: no new machine translation — adapt from existing patterns
- `npm run build` + `npm run lint` green before marking any task done

---

## Success Criteria (Done When)

- [ ] `ux-audit/audit-report.md` committed with all 15 screens severity-tagged ✅
- [ ] `ux-audit/issue-backlog.md` committed and HITL-approved ✅
- [ ] Re-audit confirms 0 CRITICAL issues ✅
- [ ] Re-audit confirms 0 HIGH issues ✅
- [ ] Before/after screenshots committed for all fixed issues ✅
- [ ] ZH 375px: no overflow on any redesigned screen ✅
- [ ] Legacy baseline-uat.md: 38/41 ✅
- [ ] UAT-S5 19/19 pass ✅
