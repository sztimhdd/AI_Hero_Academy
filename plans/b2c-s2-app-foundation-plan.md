# Sprint 2: B2C App Foundation
**Track:** B (Engineering)
**Depends on:** Nothing in Track B. Runs in parallel with Sprint 1.
**Estimated effort:** M

---

## Objective

Bootstrap the Next.js B2C application: scaffold, Firebase Authentication, Firestore schema with TypeScript types, and the onboarding flow. This sprint produces a deployed, authenticated shell where a new user can sign in, complete onboarding (4 screens including the AI-generated diagnostic), and land on a dashboard stub. It is the foundation every subsequent engineering sprint builds on.

---

## What Gets Built

**1. Next.js App Scaffold + Firebase Auth (E1)**
- Next.js 15 App Router, TypeScript, Tailwind CSS, deployed to Cloud Run
- Firebase Authentication: Google OAuth + LinkedIn OAuth (OIDC) + Facebook OAuth
- Auth flow: OAuth → Firebase JWT → HTTP-only session cookie → server-side validation via `firebase-admin`
- Middleware: unauthenticated → `/`, authenticated away from `/`
- Landing page `/`: social login buttons + EN/ZH static toggle
- CI/CD: GitHub Actions → Artifact Registry → Cloud Run on push to `main`

**2. Firestore Schema + TypeScript Types (E2)**
- `src/lib/firestore/types.ts` — interfaces for all 8 collections: `UserProfile`, `DiagnosticSession`, `TrainingProgress`, `CoachSession`, `LearnerModel`, `BuildArtifact`, `Credential`, `AiCallLog`
- `src/lib/firestore/db.ts` — CRUD helpers: `getUser`, `createUser`, `upsertTrainingProgress`, `appendCoachTurn`, `upsertLearnerModel`, `saveBuildArtifact`, `issueCredential`
- Firestore security rules: users can only read/write their own documents
- Dev seed script: 3 test users (fresh / Day 3 in-progress / Day 7 complete)
- Legacy Streamlit app remains untouched — no existing Firestore documents modified

**3. Onboarding Flow (E3)**
- Route: `/onboarding` — 4 screens, unskippable for new users
  - **Screen 1:** declared role (select + free-text), declared industry (select), daily work desc (textarea)
  - **Screen 2:** current AI tool usage (textarea) + primary motivation (4 options)
  - **Screen 3:** 5 MCQ diagnostic from `content/diagnostic_pillar.json` + 1 AI-generated personalized open question (Gemini Flash via `/api/diagnostic/generate-question`, static fallback)
  - **Screen 4:** 6-pillar gap map visualization + "Start Day 1" CTA
- On completion: writes `user_profiles` (all declared fields + `program_started_at`), `diagnostic_sessions` (`pillar_scores`), `training_progress/p1` (`is_locked: false`)
- Partial save: screen position preserved in session; refresh resumes from last screen

---

## Acceptance Criteria

1. Sign in with Google → Firestore `user_profiles` doc created → authenticated session active ✅
2. New user without `program_started_at` → routed to `/onboarding`, cannot reach dashboard ✅
3. All 4 onboarding screens render and are navigable ✅
4. AI-generated diagnostic question returned within 3 seconds, or static fallback shown ✅
5. Onboarding completion writes all required Firestore documents ✅
6. `training_progress/p1` unlocked (`is_locked: false`); P2–P6 locked ✅
7. Gap map visualization renders with 6 pillar scores ✅
8. `docker build` + `gcloud run deploy` succeed; app accessible at Cloud Run URL ✅
9. GitHub Actions deploys on push to `main` ✅
10. Firestore security rules: user A cannot read user B's documents ✅
11. Legacy Streamlit app passes smoke test after security rules update ✅
12. EN + ZH copy present on all screens (ZH may be placeholder until Sprint 4) ✅

## UAT Checkpoint

**Type: Remote Playwright smoke test (Cloud Run) + legacy regression (local)**

Run after `gcloud run deploy` succeeds and CI/CD is green.

**Part A — B2C smoke test (Playwright MCP, remote)**
```
Target: https://ai-hero-academy-387141525919.northamerica-northeast1.run.app
(replace with new Next.js Cloud Run URL once deployed)

UAT-S2-1: Landing page renders — login buttons visible, EN/ZH toggle present
UAT-S2-2: Google OAuth sign-in completes → user_profiles doc created in Firestore
UAT-S2-3: New user → routed to /onboarding (cannot reach /dashboard directly)
UAT-S2-4: All 4 onboarding screens render and advance correctly
UAT-S2-5: AI-generated diagnostic question appears within 5s, or static fallback shown
UAT-S2-6: Onboarding completion → /dashboard stub renders
UAT-S2-7: Firestore: training_progress/p1 is_locked=false; p2–p6 is_locked=true
UAT-S2-8: Unauthenticated /dashboard → redirects to /
UAT-S2-9: User A cannot access User B's Firestore documents (test with 2 test accounts)
```
Gate: 8/9 pass (UAT-S2-9 can be deferred to security review sprint if infeasible in smoke test).

**Part B — Legacy Streamlit regression (Playwright MCP, local)**
```bash
bash run_uat.sh   # start legacy app on port 8501
```
Run `.claude/evals/baseline-uat.md` — must pass **38/41** (existing gate).
Any failure in G2a (RM diagnostic) or G4 (module flow) **blocks this sprint**.
Purpose: Firestore security rules update in E2 must not break the legacy app.

## Key Constraints

- Firebase Auth only — no other auth provider
- App Router only — no Pages Router
- HTTP-only cookies for session — no localStorage
- Flat Firestore collections — no subcollections
- GCP project `banded-totality-485901` — existing project

## Out of Scope

- Coach engine and daily module (Sprint 3)
- Dashboard full implementation (Sprint 4)
- Full ZH i18n system (Sprint 4)
- WeChat OAuth (post-MVP)
