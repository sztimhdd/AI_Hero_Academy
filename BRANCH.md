# Branch: b2c-nextjs

## Purpose

This branch is the **B2C future state** of AI Hero Academy. The legacy Streamlit app (Python, Cloud Run) has been fully replaced by a Next.js 15 App Router application targeting the same GCP project.

**Do not merge this branch into `main` until Sprint 2 acceptance criteria are fully met.**
**Do not carry any Streamlit code, Python deps, or Streamlit-specific Firestore patterns back into this branch.**

---

## What This Branch Contains

| Path | What it is |
|------|-----------|
| `src/` | Next.js App Router app (TypeScript, Tailwind) |
| `content/i18n/` | EN + ZH copy seeds (carried from legacy; will be extended) |
| `plans/` | Sprint plans + B2C transformation roadmap (read-only reference) |
| `TDD.md` | Technical Design Document v2.0 — B2C stack decisions |
| `CLAUDE.md` | Project instructions for Claude Code on this branch |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15 App Router, React Server Components, TypeScript |
| Styling | Tailwind CSS |
| Auth | Firebase Authentication — Google + LinkedIn (OIDC) + Facebook OAuth |
| Session | HTTP-only cookie (`__session`) backed by Firebase Admin JWT verification |
| Database | Google Cloud Firestore (GCP project `banded-totality-485901`) |
| AI | Google Gemini 2.0 Flash via API routes |
| Deploy | Docker → Artifact Registry → GCP Cloud Run |
| CI/CD | GitHub Actions on push to `b2c-nextjs` (and eventually `main`) |

---

## GCP Project

**Project ID:** `banded-totality-485901`
**Cloud Run service:** `ai-hero-academy-b2c` (new service — legacy `ai-hero-academy` is the Streamlit app, leave it running)
**Firestore database:** default (shared with legacy app — see Firestore safety rules below)

---

## Firestore Safety Rules (Critical)

The legacy Streamlit app writes to these collections via a service account (bypasses security rules):
`user_profiles`, `diagnostic_sessions`, `gap_maps`, `training_progress`, `coach_sessions`, `ai_call_log`

The B2C Next.js app uses **new collection names** for its own documents:
- All 8 B2C collections defined in `src/lib/firestore/types.ts`
- Security rules on B2C collections require `request.auth != null` (Firebase Auth UID)
- **Never rename or restructure the legacy collections above** — the Streamlit app on `main` depends on them

---

## Sprint 2 Build Order

```
Step 1 — Scaffold + Auth        ← YOU ARE HERE
  Firebase client + admin SDK
  /api/auth/session + /api/auth/logout
  Landing page / with OAuth buttons
  middleware.ts auth guard
  Dockerfile + GitHub Actions CI/CD

Step 2 — Firestore Schema
  src/lib/firestore/types.ts     (8 interfaces)
  src/lib/firestore/db.ts        (CRUD helpers)
  firestore.rules
  scripts/seed-dev.ts

Step 3 — Onboarding Flow
  /onboarding (4 screens)
  /api/diagnostic/generate-question
  /api/diagnostic/score
  /dashboard (stub)
```

---

## Environment Variables Required

```bash
# Firebase client SDK (public — safe to expose to browser)
NEXT_PUBLIC_FIREBASE_API_KEY=
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NEXT_PUBLIC_FIREBASE_PROJECT_ID=banded-totality-485901
NEXT_PUBLIC_FIREBASE_APP_ID=

# Firebase Admin SDK (server-only — never expose to browser)
FIREBASE_ADMIN_PROJECT_ID=banded-totality-485901
FIREBASE_ADMIN_CLIENT_EMAIL=
FIREBASE_ADMIN_PRIVATE_KEY=

# Gemini
GEMINI_API_KEY=

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

Copy `.env.example` → `.env.local` and fill in values before running locally.

---

## Key Architecture Decisions (from TDD.md §4.4–4.5)

- **App Router only** — no Pages Router. All routes under `src/app/`.
- **HTTP-only cookies** — Firebase ID token is exchanged server-side for a session cookie. No token ever touches `localStorage`.
- **Flat Firestore collections** — no subcollections. All documents at top level, filtered by `user_email` or `uid`.
- **Server Components by default** — mark `"use client"` only where browser APIs or React hooks are needed.
- **Gemini called from API routes only** — never from client components. API key never exposed to browser.
- **No Vercel** — Cloud Run only. `next.config.ts` uses `output: "standalone"` for Docker.

---

## Acceptance Criteria (Sprint 2 Done-When)

- [ ] Sign in with Google → `user_profiles` doc created in Firestore → session cookie set
- [ ] Unauthenticated request to any protected route → redirected to `/`
- [ ] Authenticated user with no `program_started_at` → redirected to `/onboarding`
- [ ] All 4 onboarding screens render and are navigable
- [ ] AI-generated diagnostic question returned ≤ 3 s, or static fallback shown
- [ ] Onboarding completion writes: `user_profiles`, `diagnostic_sessions`, `training_progress/p1` (unlocked), `training_progress/p2–p6` (locked)
- [ ] Gap map renders with 6 pillar scores
- [ ] `docker build` succeeds; `gcloud run deploy` succeeds
- [ ] GitHub Actions deploys on push to this branch
- [ ] Firestore security rules: user A cannot read user B's documents
- [ ] Legacy Streamlit app smoke test still passes on `main`
- [ ] EN + ZH copy present on all screens (ZH may be placeholder)

---

## Reading Order for New Agents

1. This file (`BRANCH.md`) — branch context and constraints
2. `CLAUDE.md` — project-level Claude Code instructions
3. `TDD.md` §1 (tech stack), §4.4 (Next.js decision), §4.5 (auth model)
4. `plans/b2c-s2-app-foundation-plan.md` — Sprint 2 full spec
5. `plans/b2c-transformation-roadmap.md` §3.1 (Firestore schemas), §1.7 (onboarding / role context)
