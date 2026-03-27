# Kickstart: Sprint 2 — B2C App Foundation
**Full plan:** `plans/b2c-s2-app-foundation-plan.md`

---

## What to Read First

1. `plans/b2c-s2-app-foundation-plan.md` — full spec
2. `TDD.md` §1 (NEW TECH STACK, NEW FIRESTORE COLLECTIONS), §4.4 (Next.js decision), §4.5 (Auth model)
3. `plans/b2c-transformation-roadmap.md` §3.1 (Firestore collection schemas), §1.7 (onboarding / role context)

---

## What to Build

Three things in sequence: scaffold → schema → onboarding.

**Step 1 — Scaffold + Auth:**
```bash
npx create-next-app@latest . --typescript --tailwind --app --src-dir
npm install firebase firebase-admin @google-cloud/firestore
```
- Firebase Auth in GCP project `banded-totality-485901`: enable Google + LinkedIn + Facebook providers
- `src/lib/firebase/client.ts` + `admin.ts` + `/api/auth/session` + `/api/auth/logout` + `middleware.ts`
- Landing page `/`: login buttons + static EN/ZH toggle
- `Dockerfile` + `.github/workflows/deploy.yml` → Cloud Run

**Step 2 — Schema:**
- `src/lib/firestore/types.ts` — 8 TypeScript interfaces
- `src/lib/firestore/db.ts` — CRUD helpers
- `firestore.rules` — auth-scoped per-user access
- `scripts/seed-dev.ts` — 3 test users

**Step 3 — Onboarding:**
- `/onboarding` — 4 screens (profile → motivations → diagnostic → gap map)
- `/api/diagnostic/generate-question` — Gemini Flash personalized question
- `/api/diagnostic/score` — scores responses, writes Firestore docs, unlocks P1

---

## Non-Negotiable Rules

- App Router only — no Pages Router
- Firebase Auth only — no other auth library
- HTTP-only cookies for session — no localStorage
- Flat Firestore collections — no subcollections
- Do NOT modify existing Firestore documents (legacy Streamlit app must keep working)
- Do NOT deploy to Vercel — Cloud Run only
- Do NOT skip the security rules update

---

## Success Criteria (Done When)

- [ ] Sign in with Google → `user_profiles` doc in Firestore → session cookie set ✅
- [ ] Unauthenticated → `/`; authenticated → onboarding or dashboard ✅
- [ ] All 4 onboarding screens complete → all Firestore writes verified ✅
- [ ] P1 unlocked; P2–P6 locked after diagnostic ✅
- [ ] `gcloud run deploy` succeeds; GitHub Actions CI/CD green ✅
- [ ] Legacy Streamlit app smoke test still passes ✅
