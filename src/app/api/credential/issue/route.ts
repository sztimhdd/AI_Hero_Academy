/**
 * POST /api/credential/issue
 * Issues the AI-Supercharged Intermediate credential after capstone pass.
 */
import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { Timestamp } from "firebase-admin/firestore";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { getUser, issueCredential } from "@/lib/firestore/db";
import type { PillarScores } from "@/lib/firestore/types";

export async function POST(req: NextRequest) {
  let uid: string;
  let userEmail: string;
  try {
    const auth = await getAuthFromCookies(await cookies());
    uid = auth.uid;
    userEmail = auth.email;
  } catch {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const {
    pillar_scores,
    overall_score,
    display_name: bodyDisplayName,
  } = (await req.json()) as {
    pillar_scores: PillarScores;
    overall_score: number;
    display_name?: string;
  };

  // Get display name from profile if not in body
  const user = await getUser(uid);
  const displayName = bodyDisplayName || user?.display_name || userEmail.split("@")[0];

  const credential_id = "ai_supercharged_intermediate";
  const issuedAt = Timestamp.now();

  await issueCredential({
    uid,
    user_email: userEmail,
    display_name: displayName,
    credential_id,
    issued_at: issuedAt,
    pillar_scores,
    overall_score,
  });

  return NextResponse.json({
    credential_id,
    issued_at: issuedAt.toDate().toISOString(),
  });
}
