import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { Timestamp } from "firebase-admin/firestore";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { getUser, getLearnerModel, createCoachSession } from "@/lib/firestore/db";
import { loadPillarContent } from "@/lib/content/loadPillar";
import { assembleCoachPrompt } from "@/lib/coach/assembler";
import type { PillarId } from "@/lib/firestore/types";

export async function POST(req: NextRequest) {
  const sessionCookie = (await cookies()).get("__session")?.value;
  if (!sessionCookie) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  let uid: string;
  let userEmail: string;
  try {
    const auth = await getAuthFromCookies(await cookies());
    uid = auth.uid;
    userEmail = auth.email;
  } catch {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { pillar_id } = await req.json();
  if (!pillar_id) {
    return NextResponse.json({ error: "pillar_id required" }, { status: 400 });
  }

  // Load pillar content
  let pillarContent;
  try {
    pillarContent = loadPillarContent(pillar_id);
  } catch {
    return NextResponse.json({ error: "Pillar not available" }, { status: 404 });
  }

  // Load user profile and learner model in parallel
  const [profile, learnerModel] = await Promise.all([
    getUser(uid),
    getLearnerModel(uid),
  ]);

  if (!profile) {
    return NextResponse.json({ error: "Profile not found" }, { status: 404 });
  }

  // Assemble the system prompt
  const systemPrompt = assembleCoachPrompt(
    pillarContent.practice.coach_system_prompt_template,
    profile,
    learnerModel
  );

  const roleContext = `${profile.declared_role ?? "professional"} in ${profile.declared_industry ?? "their industry"}`;

  // Create the coach session doc (with extra fields stored schema-lessly)
  const sessionId = await createCoachSession({
    uid,
    user_email: userEmail,
    pillar_id: pillar_id as PillarId,
    day_number: pillarContent.day_number,
    role_context: roleContext,
    transcript: [],
    turn_count: 0,
    created_at: Timestamp.now(),
    // Extra fields (beyond CoachSession type) stored schema-lessly
    ...({ system_prompt: systemPrompt, task_turn_counts: {} } as object),
  } as Parameters<typeof createCoachSession>[0]);

  return NextResponse.json({ session_id: sessionId });
}
