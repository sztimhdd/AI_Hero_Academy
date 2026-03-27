# Kickstart: Sprint 4 — B2C Program Completion
**Full plan:** `plans/b2c-s4-program-completion-plan.md`

---

## What to Read First

1. `plans/b2c-s4-program-completion-plan.md` — full spec for all 4 components
2. `plans/b2c-transformation-roadmap.md` §1.4 (credential model), §1.6 (engagement mechanics), §1.3 (capstone format)
3. `TDD.md` §1 (credentials collection, GCS)
4. `content/pillars/capstone.json` — capstone content (must exist from Sprint 1)

**Prerequisites:** Sprint 3 complete (quiz score route exists — capstone + credential trigger from it). Sprint 1 capstone content complete.

---

## What to Build

Build in dependency order: dashboard → capstone → credential → i18n.

**Dashboard (`/dashboard`):** 5 components — arc timeline, pillar badges, streak counter, artifact gallery, profile pill. Streak update API. Mobile-responsive at 375px.

**Capstone (`/day/capstone`):** 3-screen flow (intro → challenge → results). 4 mixed-input tasks. GCS signed URL for file upload. Gemini multimodal vision scoring.

**Credential (`POST /api/credential/issue`):** 4 assets to GCS. Open Badge PNG (`sharp`), PDF (`puppeteer`), LinkedIn deep link, social share card 1200×630px. `/credential` page.

**i18n (`next-intl`):** Configure locales, wire all strings to `t('key')`, translate to ZH, wire language toggle to Firestore `lang` field, update coach language instruction.

---

## Non-Negotiable Rules

- GCS for credential assets — not Firestore blobs, not base64 inline
- File upload is GCS signed URL direct from browser — not proxied through Next.js server
- Gemini multimodal for vision scoring — not any third-party vision API
- `next-intl` for i18n — not `next-i18next`
- AI technical terms stay in EN in ZH copy: LLM, GPT, Claude, API, JSON, system prompt, temperature
- LinkedIn deep link format: `linkedin.com/profile/add?startTask=CERTIFICATION_NAME&...`
- No hard time limit on capstone — 15 min is a design ceiling, not a server timeout

---

## Success Criteria (Done When)

- [ ] `/dashboard` all 5 components working, mobile-responsive ✅
- [ ] `/day/capstone` all 4 task types complete end-to-end ✅
- [ ] File upload → GCS → vision score → aggregated capstone score ✅
- [ ] Capstone PASS → credential issued → `/credential` page shows all 4 assets ✅
- [ ] Open Badge PNG + PDF + LinkedIn deep link + social card all accessible ✅
- [ ] Language toggle switches full UI EN ↔ ZH ✅
- [ ] Coach streams in ZH when `lang = "zh"` ✅
- [ ] No ZH text overflow at 375px ✅
