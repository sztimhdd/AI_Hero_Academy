/**
 * scripts/seed-dev.ts
 * Seeds 3 test users into Firestore for local development.
 *
 * Run:  npx tsx scripts/seed-dev.ts
 *
 * Requires .env.local with FIREBASE_ADMIN_* vars set.
 * Does NOT use Firebase client SDK — uses Admin SDK directly.
 *
 * Users:
 *  1. fresh@dev.test      — just signed up, no onboarding
 *  2. day3@dev.test       — mid-program (Day 3, P2 in progress)
 *  3. complete@dev.test   — Day 7 complete, credential issued
 */

import * as dotenv from "dotenv";
dotenv.config({ path: ".env.local" });

import { initializeApp, cert, getApps } from "firebase-admin/app";
import { getFirestore, Timestamp } from "firebase-admin/firestore";
import {
  COLLECTIONS,
  UserProfile,
  DiagnosticSession,
  TrainingProgress,
  Credential,
  PillarId,
  PILLAR_IDS,
} from "../src/lib/firestore/types";

// ── Init ────────────────────────────────────────────────────────────────────

if (!getApps().length) {
  initializeApp({
    credential: cert({
      projectId: process.env.FIREBASE_ADMIN_PROJECT_ID!,
      clientEmail: process.env.FIREBASE_ADMIN_CLIENT_EMAIL!,
      privateKey: process.env.FIREBASE_ADMIN_PRIVATE_KEY?.replace(/\\n/g, "\n"),
    }),
  });
}

const db = getFirestore();

// ── Helpers ─────────────────────────────────────────────────────────────────

function now() { return Timestamp.now(); }
function daysAgo(n: number) {
  return Timestamp.fromMillis(Date.now() - n * 24 * 60 * 60 * 1000);
}

async function seedUser(profile: UserProfile) {
  await db.collection(COLLECTIONS.USER_PROFILES).doc(profile.uid).set(profile);
  console.log(`✓ user_profile: ${profile.uid} (${profile.user_email})`);
}

async function seedDiagnostic(session: DiagnosticSession) {
  await db
    .collection(COLLECTIONS.DIAGNOSTIC_SESSIONS)
    .doc(session.session_id)
    .set(session);
  console.log(`✓ diagnostic_session: ${session.session_id}`);
}

async function seedTrainingProgress(docs: TrainingProgress[]) {
  const batch = db.batch();
  for (const doc of docs) {
    const ref = db
      .collection(COLLECTIONS.TRAINING_PROGRESS)
      .doc(`${doc.uid}_${doc.pillar_id}`);
    batch.set(ref, doc);
  }
  await batch.commit();
  console.log(`✓ training_progress: ${docs.length} docs for uid=${docs[0]?.uid}`);
}

async function seedCredential(cred: Credential) {
  await db
    .collection(COLLECTIONS.CREDENTIALS)
    .doc(`${cred.uid}_${cred.credential_id}`)
    .set(cred);
  console.log(`✓ credential: ${cred.credential_id} for uid=${cred.uid}`);
}

// ── User 1: fresh — signed up, no onboarding ─────────────────────────────────

async function seedFreshUser() {
  const uid = "dev-fresh-001";
  await seedUser({
    uid,
    user_email: "fresh@dev.test",
    display_name: "Fresh User",
    profile_photo_url: "",
    auth_provider: "google",
    lang: "en",
    streak_days: 0,
    created_at: now(),
  });
  // No diagnostic, no training progress — middleware will route to /onboarding
}

// ── User 2: day3 — mid-program, P2 unlocked ──────────────────────────────────

async function seedDay3User() {
  const uid = "dev-day3-002";
  const started = daysAgo(3);

  await seedUser({
    uid,
    user_email: "day3@dev.test",
    display_name: "Day 3 User",
    profile_photo_url: "",
    auth_provider: "google",
    lang: "en",
    declared_role: "marketer",
    declared_industry: "tech",
    daily_work_desc: "Content strategy, campaign briefs, reporting",
    current_ai_usage: "ChatGPT for copy drafts, occasional image gen",
    primary_motivation: "quality",
    program_started_at: started,
    streak_days: 3,
    last_active_date: new Date().toISOString().slice(0, 10),
    created_at: daysAgo(3),
  });

  await seedDiagnostic({
    session_id: "diag-day3-002",
    uid,
    user_email: "day3@dev.test",
    completed_at: started,
    pillar_scores: { p1: 62, p2: 48, p3: 55, p4: 30, p5: 40, p6: 45 },
    overall_score: 47,
    item_scores: {},
    session_number: 1,
  });

  const pillarsInOrder: PillarId[] = [...PILLAR_IDS, "capstone" as PillarId];
  await seedTrainingProgress(
    pillarsInOrder.map((pillarId, idx) => ({
      uid,
      user_email: "day3@dev.test",
      pillar_id: pillarId,
      day_number: idx + 1,
      sequence_order: idx,
      is_locked: idx > 2, // P1, P2, P3 unlocked; rest locked
      reading_completed_at: idx < 2 ? daysAgo(3 - idx) : undefined,
      practice_completed_at: idx < 2 ? daysAgo(3 - idx) : undefined,
      quiz_completed_at: idx < 2 ? daysAgo(3 - idx) : undefined,
      quiz_score: idx < 2 ? 80 : undefined,
      quiz_passed: idx < 2 ? true : undefined,
    }))
  );
}

// ── User 3: complete — Day 7 done, credential issued ─────────────────────────

async function seedCompleteUser() {
  const uid = "dev-complete-003";
  const started = daysAgo(7);

  await seedUser({
    uid,
    user_email: "complete@dev.test",
    display_name: "Complete User",
    profile_photo_url: "",
    auth_provider: "google",
    lang: "en",
    declared_role: "pm",
    declared_industry: "fintech",
    daily_work_desc: "Sprint planning, stakeholder updates, roadmap",
    current_ai_usage: "Claude for docs, Copilot for code reviews",
    primary_motivation: "career",
    program_started_at: started,
    streak_days: 7,
    last_active_date: new Date().toISOString().slice(0, 10),
    created_at: daysAgo(8),
  });

  const finalScores = { p1: 88, p2: 82, p3: 79, p4: 75, p5: 85, p6: 80 };

  await seedDiagnostic({
    session_id: "diag-complete-003",
    uid,
    user_email: "complete@dev.test",
    completed_at: started,
    pillar_scores: { p1: 55, p2: 50, p3: 48, p4: 42, p5: 52, p6: 44 },
    overall_score: 49,
    item_scores: {},
    session_number: 1,
  });

  const pillarsInOrder: PillarId[] = [...PILLAR_IDS, "capstone" as PillarId];
  await seedTrainingProgress(
    pillarsInOrder.map((pillarId, idx) => ({
      uid,
      user_email: "complete@dev.test",
      pillar_id: pillarId,
      day_number: idx + 1,
      sequence_order: idx,
      is_locked: false,
      reading_completed_at: daysAgo(7 - idx),
      practice_completed_at: daysAgo(7 - idx),
      quiz_completed_at: daysAgo(7 - idx),
      quiz_score: 85,
      quiz_passed: true,
      build_completed_at: daysAgo(7 - idx),
    }))
  );

  await seedCredential({
    uid,
    user_email: "complete@dev.test",
    display_name: "Complete Dev",
    credential_id: "ai_hero_intermediate",
    issued_at: now(),
    pillar_scores: finalScores,
    overall_score:
      Math.round(
        Object.values(finalScores).reduce((a, b) => a + b, 0) /
          Object.values(finalScores).length
      ),
  });
}

// ── Main ────────────────────────────────────────────────────────────────────

async function main() {
  console.log("Seeding dev users into Firestore…\n");
  await seedFreshUser();
  await seedDay3User();
  await seedCompleteUser();
  console.log("\nDone.");
  process.exit(0);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
