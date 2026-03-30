/**
 * POST /api/auth/demo-login
 *
 * Private beta demo mode. Seeds Firestore with a pre-built persona and sets
 * a demo session cookie so stakeholders can walk through the full UX without
 * creating a real account.
 *
 * Protected by DEMO_TOKEN env var — only works when that secret is configured.
 * Safe to deploy to production; returns 404 when DEMO_TOKEN is absent.
 */
import { NextResponse } from "next/server";
import { Timestamp } from "firebase-admin/firestore";
import { getFirestore } from "firebase-admin/firestore";
import { getAdminAuth } from "@/lib/firebase/admin";
import { COLLECTIONS } from "@/lib/firestore/types";

export const dynamic = "force-dynamic";

const PERSONAS = ["onboarding", "day1", "day3", "day6", "credential"] as const;
type Persona = typeof PERSONAS[number];

const PERSONA_UIDS: Record<Persona, string> = {
  onboarding: "demo-onboarding",
  day1:       "demo-day1",
  day3:       "demo-day3",
  day6:       "demo-day6",
  credential: "demo-credential",
};

const PERSONA_REDIRECTS: Record<Persona, string> = {
  onboarding: "/onboarding",
  day1:       "/day/p1",
  day3:       "/dashboard",
  day6:       "/dashboard",
  credential: "/credential",
};

export async function POST(req: Request) {
  if (!process.env.DEMO_TOKEN) {
    return NextResponse.json({ error: "Not available" }, { status: 404 });
  }

  const { persona, token } = await req.json() as { persona?: string; token?: string };

  if (token !== process.env.DEMO_TOKEN) {
    return NextResponse.json({ error: "Invalid token" }, { status: 403 });
  }

  if (!persona || !PERSONAS.includes(persona as Persona)) {
    return NextResponse.json(
      { error: `Invalid persona. Choose: ${PERSONAS.join(", ")}` },
      { status: 400 }
    );
  }

  const p = persona as Persona;
  const uid = PERSONA_UIDS[p];
  const email = `${uid}@demo.ai-hero.academy`;

  try {
    try { getAdminAuth(); } catch { /* initialise Admin SDK */ }
    const db = getFirestore();
    const pillars = ["p1", "p2", "p3", "p4", "p5", "p6", "capstone"] as const;
    const now = Timestamp.now();
    const batch = db.batch();

    // ── User profile ──────────────────────────────────────────────────────────
    const profileRef = db.collection(COLLECTIONS.USER_PROFILES).doc(uid);
    const baseProfile = {
      uid,
      user_email: email,
      display_name: "Demo User",
      profile_photo_url: "",
      auth_provider: "demo",
      lang: "en",
      declared_role: "Product Manager",
      declared_industry: "Technology",
      daily_work_desc: "I coordinate cross-functional teams, write product specs, and lead stakeholder meetings.",
      current_ai_usage: "Occasionally use ChatGPT for writing",
      primary_motivation: "save_time",
      streak_days: p === "onboarding" ? 0 : p === "day1" ? 1 : p === "day3" ? 3 : 6,
      last_active_date: new Date().toISOString().slice(0, 10),
      created_at: now,
    };

    if (p === "onboarding") {
      // No program_started_at → middleware sends to /onboarding
      batch.set(profileRef, baseProfile);
    } else {
      batch.set(profileRef, {
        ...baseProfile,
        program_started_at: now,
      });
    }

    // ── Training progress ─────────────────────────────────────────────────────
    const completedCount: Record<Persona, number> = {
      onboarding: 0,
      day1:       0,  // p1 available but not yet started
      day3:       3,
      day6:       6,
      credential: 6,
    };
    const daysComplete = completedCount[p];

    if (p !== "onboarding") {
      pillars.forEach((pillarId, idx) => {
        const ref = db.collection(COLLECTIONS.TRAINING_PROGRESS).doc(`${uid}_${pillarId}`);
        const daysBack = Timestamp.fromMillis(Date.now() - (daysComplete - 1 - Math.min(idx, daysComplete - 1)) * 86400000);
        const isDone = idx < daysComplete;
        batch.set(ref, {
          uid,
          user_email: email,
          pillar_id: pillarId,
          day_number: idx + 1,
          sequence_order: idx,
          is_locked: !isDone && idx !== daysComplete,
          reading_completed_at: isDone ? daysBack : null,
          practice_completed_at: isDone ? daysBack : null,
          quiz_completed_at: isDone ? daysBack : null,
          quiz_score: isDone ? 85 : null,
          quiz_passed: isDone ? true : null,
          build_completed_at: isDone ? daysBack : null,
          pillar_score_after: isDone ? 2 : null,
        });
      });
    }

    // ── Credential (credential persona only) ─────────────────────────────────
    if (p === "credential") {
      const credRef = db.collection(COLLECTIONS.CREDENTIALS).doc(`${uid}_ai_supercharged_intermediate`);
      batch.set(credRef, {
        uid,
        user_email: email,
        display_name: "Demo User",
        credential_id: "ai_supercharged_intermediate",
        issued_at: now,
        pillar_scores: { p1: 2, p2: 2, p3: 2, p4: 2, p5: 2, p6: 2 },
        overall_score: 3.8,
      });
    }

    await batch.commit();
  } catch (err) {
    console.error("Demo seed error:", err);
    // Proceed with cookie even if Firestore seed fails
  }

  const redirect = PERSONA_REDIRECTS[p];
  const expiresIn = 2 * 60 * 60; // 2-hour demo sessions
  const res = NextResponse.json({ ok: true, persona: p, redirect });

  res.cookies.set("__session", "demo-bypass", {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: expiresIn,
    path: "/",
  });
  res.cookies.set("__demo_uid", PERSONA_UIDS[p], {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: expiresIn,
    path: "/",
  });

  return res;
}
