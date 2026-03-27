# CLAUDE.md — Branch: b2c-nextjs

> **This is the B2C Next.js branch.** The Streamlit app no longer exists here.
> Legacy app lives on `main`. Do not reintroduce Python, Streamlit, or legacy Firestore patterns.
> See `BRANCH.md` for full branch context, architecture decisions, and acceptance criteria.

---

## Development Environment

**Node:** v21 (v20 LTS preferred for production Docker)
**Package manager:** npm

```bash
npm install          # install deps
npm run dev          # local dev server → http://localhost:3000
npm run build        # production build
npm run lint         # ESLint
```

Copy `.env.example` → `.env.local` and fill in Firebase + Gemini values before running.

---

## Project Overview

**AI Hero Academy B2C** — personal AI transformation platform. 7-day program, 6 AI skill pillars, AI coaching, shareable credential. Full product spec: `plans/b2c-transformation-roadmap.md`.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15 App Router, React Server Components, TypeScript |
| Styling | Tailwind CSS v4 |
| Auth | Firebase Authentication (Google + LinkedIn OIDC + Facebook) |
| Session | HTTP-only cookie backed by Firebase Admin JWT |
| Database | Google Cloud Firestore (`banded-totality-485901`) |
| AI | Google Gemini 2.0 Flash (via `src/app/api/` routes only) |
| Deploy | Docker → GCP Artifact Registry → Cloud Run |

## File Structure (target state after Sprint 2)

```
src/
  app/
    page.tsx                          # Landing / login
    dashboard/page.tsx                # Post-onboarding stub
    onboarding/
      page.tsx                        # 4-screen flow
      screens/
        Screen1.tsx                   # Role + industry + daily work
        Screen2.tsx                   # AI usage + motivation
        Screen3.tsx                   # Diagnostic (5 MCQ + 1 AI question)
        Screen4.tsx                   # Gap map + Start Day 1 CTA
    api/
      auth/
        session/route.ts              # POST: ID token → session cookie
        logout/route.ts               # POST: clear cookie
      diagnostic/
        generate-question/route.ts    # POST: Gemini → personalized question
        score/route.ts                # POST: score + write Firestore
  lib/
    firebase/
      client.ts                       # Firebase client SDK init
      admin.ts                        # Firebase Admin SDK init
    firestore/
      types.ts                        # 8 TypeScript interfaces
      db.ts                           # CRUD helpers
  lib/i18n/
    en.ts                             # English copy
    zh.ts                             # Chinese copy (placeholder OK for Sprint 2)
  middleware.ts                       # Auth guard
content/
  i18n/
    en.json                           # Legacy EN copy (seed reference)
    zh.json                           # Legacy ZH copy (seed reference)
firestore.rules                       # Firestore security rules
scripts/
  seed-dev.ts                         # 3 test users
Dockerfile                            # Multi-stage: node:20-alpine → standalone
.github/workflows/deploy.yml          # GitHub Actions → Cloud Run
```

## Remote Environment

| Resource | Value |
|----------|-------|
| GCP Project | `banded-totality-485901` |
| Cloud Run service | `ai-hero-academy-b2c` (new — don't touch `ai-hero-academy`) |
| Firestore | default database (shared with legacy) |
| Gemini model | `gemini-2.0-flash` |
| GitHub repo | `https://github.com/sztimhdd/AI_Hero_Academy` |

## Key Constraints (Non-Negotiable)

- **App Router only** — no Pages Router
- **HTTP-only cookies** — no localStorage, no sessionStorage for auth tokens
- **Firebase Auth only** — no NextAuth, no custom JWT
- **Flat Firestore collections** — no subcollections
- **Gemini from API routes only** — `GEMINI_API_KEY` never in client bundle
- **Cloud Run only** — no Vercel; `next.config.ts` must have `output: "standalone"`
- **Do not modify legacy Firestore collections** — `user_profiles`, `diagnostic_sessions`, `gap_maps`, `training_progress`, `coach_sessions`, `ai_call_log` are owned by the Streamlit app on `main`

## Firestore Collections (B2C — New)

All defined in `src/lib/firestore/types.ts`. Full schemas in `plans/b2c-transformation-roadmap.md` §3.1:

- `b2c_user_profiles`
- `b2c_diagnostic_sessions`
- `b2c_training_progress`
- `b2c_coach_sessions`
- `b2c_learner_model`
- `b2c_build_artifacts`
- `b2c_credentials`
- `b2c_ai_call_log`

> Prefixed `b2c_` to avoid any collision with legacy collections in the shared Firestore database.

## Auth Flow

```
User clicks "Sign in with Google"
  → Firebase client SDK triggers OAuth popup
  → Firebase returns ID token (JWT) to browser
  → Browser POSTs ID token to /api/auth/session
  → Server verifies token with firebase-admin
  → Server sets __session HTTP-only cookie (7-day expiry)
  → Browser redirected to /onboarding or /dashboard
```

`middleware.ts` reads `__session` cookie on every request:
- No cookie → allow through to `/` only; redirect all other routes to `/`
- Valid cookie → allow through; redirect `/` to `/dashboard` (or `/onboarding` if no `program_started_at`)

## Verification Checklist

Before marking any task complete:

- `npm run build` passes with no type errors
- `npm run lint` passes
- Changed routes navigable in browser (`npm run dev`)
- For Firestore writes: verify in GCP Firestore console (project `banded-totality-485901`)
- For auth changes: test sign-in + sign-out flow end-to-end
- For onboarding changes: verify all 4 screens and partial-save resume behavior

## Lessons Learned

> Append after any correction or unexpected failure.

- **2026-03-27** — `create-next-app` refuses to scaffold into a non-empty directory. Workaround: scaffold to `/tmp`, then copy files into repo. This is a one-time bootstrap — do not re-run `create-next-app` in the project root.
