import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { Timestamp } from "firebase-admin/firestore";
import { getAdminAuth } from "@/lib/firebase/admin";
import { getCoachSession, completeCoachSession, upsertTrainingProgress } from "@/lib/firestore/db";
import type { PillarId } from "@/lib/firestore/types";
import type { CoachMessage } from "@/lib/coach/types";

export async function POST(req: NextRequest) {
  const sessionCookie = (await cookies()).get("__session")?.value;
  if (!sessionCookie) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  let uid: string;
  try {
    const decoded = await getAdminAuth().verifySessionCookie(sessionCookie, true);
    uid = decoded.uid;
  } catch {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const {
    session_id,
    pillar_id,
    conversation,
  }: {
    session_id: string;
    pillar_id: PillarId;
    conversation: CoachMessage[];
  } = await req.json();

  if (!session_id || !pillar_id || !conversation) {
    return NextResponse.json({ error: "session_id, pillar_id and conversation required" }, { status: 400 });
  }

  // Verify the session belongs to this user
  const sessionDoc = await getCoachSession(session_id);
  if (!sessionDoc || sessionDoc.uid !== uid) {
    return NextResponse.json({ error: "Session not found" }, { status: 404 });
  }

  const now = Timestamp.now();

  // Write transcript and mark practice complete in parallel
  await Promise.all([
    completeCoachSession(
      session_id,
      conversation.map((m) => ({ role: m.role, content: m.content })),
      now
    ),
    upsertTrainingProgress(uid, pillar_id, {
      practice_completed_at: now,
    }),
  ]);

  return NextResponse.json({ ok: true });
}
