/**
 * POST /api/auth/dev-login
 *
 * LOCAL_UAT ONLY — sets a UAT bypass session cookie and seeds Firestore
 * test data for the UAT test user.
 *
 * Does NOT require Firebase Auth (Identity Toolkit API) to be enabled.
 * Uses a magic cookie value ("uat-bypass") that src/lib/auth/verify.ts
 * recognises when LOCAL_UAT=true.
 *
 * Never available when LOCAL_UAT !== "true".
 */
import { NextResponse } from "next/server";
import { Timestamp } from "firebase-admin/firestore";
import { getFirestore } from "firebase-admin/firestore";
import { getAdminAuth } from "@/lib/firebase/admin"; // initialises the Admin SDK / Firestore
import { COLLECTIONS } from "@/lib/firestore/types";
import { getUser, createUser, upsertTrainingProgress, getTrainingProgressDoc } from "@/lib/firestore/db";

const UAT_COOKIE_VALUE = "uat-bypass";
const UAT_UID = process.env.UAT_TEST_UID ?? "uat-test-uid";
const UAT_EMAIL = process.env.DEV_USER_EMAIL ?? "uat@dev.local";
const UAT_NAME = "UAT Test User";

export async function POST() {
  if (process.env.LOCAL_UAT !== "true") {
    return NextResponse.json({ error: "Not available" }, { status: 404 });
  }

  // Seed Firestore with test user data
  try {
    // Force Admin SDK init (needed before Firestore calls)
    try { getAdminAuth(); } catch { /* ignore — only needed for session cookie verification */ }

    const db = getFirestore();

    // 1. Upsert user profile
    const existing = await getUser(UAT_UID);
    if (!existing) {
      await createUser({
        uid: UAT_UID,
        user_email: UAT_EMAIL,
        display_name: UAT_NAME,
        profile_photo_url: "",
        auth_provider: "dev",
        lang: "en",
        declared_role: "Product Manager",
        declared_industry: "Technology",
        daily_work_desc: "I coordinate cross-functional teams, write product specs, and lead stakeholder meetings.",
        current_ai_usage: "Occasionally use ChatGPT for writing",
        primary_motivation: "save_time",
        program_started_at: Timestamp.now(),
        streak_days: 1,
        last_active_date: new Date().toISOString().slice(0, 10),
        created_at: Timestamp.now(),
      });
    } else if (!existing.declared_role) {
      // Patch missing onboarding fields
      await db.collection(COLLECTIONS.USER_PROFILES).doc(UAT_UID).set({
        declared_role: "Product Manager",
        declared_industry: "Technology",
        daily_work_desc: "I coordinate cross-functional teams, write product specs, and lead stakeholder meetings.",
        program_started_at: Timestamp.now(),
        streak_days: 1,
      }, { merge: true });
    }

    // 2. Ensure p1 training progress exists and is unlocked
    const p1Progress = await getTrainingProgressDoc(UAT_UID, "p1");
    if (!p1Progress) {
      // Seed all pillars: p1 unlocked, rest locked
      const pillars = ["p1", "p2", "p3", "p4", "p5", "p6", "capstone"] as const;
      const batch = db.batch();
      pillars.forEach((pillarId, idx) => {
        const ref = db.collection(COLLECTIONS.TRAINING_PROGRESS).doc(`${UAT_UID}_${pillarId}`);
        batch.set(ref, {
          uid: UAT_UID,
          user_email: UAT_EMAIL,
          pillar_id: pillarId,
          day_number: idx + 1,
          sequence_order: idx,
          is_locked: idx !== 0,
        });
      });
      await batch.commit();
    }
  } catch (err) {
    // If Firestore is unavailable (e.g. SSL proxy), still set the cookie
    // so page rendering tests can proceed
    console.error("UAT seed warning:", err);
  }

  const expiresIn = 7 * 24 * 60 * 60; // 7 days in seconds
  const res = NextResponse.json({
    ok: true,
    uid: UAT_UID,
    email: UAT_EMAIL,
    display_name: UAT_NAME,
    note: "UAT bypass cookie set. Firebase Auth not required.",
  });

  res.cookies.set("__session", UAT_COOKIE_VALUE, {
    httpOnly: true,
    secure: false,
    sameSite: "lax",
    maxAge: expiresIn,
    path: "/",
  });

  return res;
}
