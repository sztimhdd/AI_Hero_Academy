import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { saveBuildArtifact } from "@/lib/firestore/db";
import { loadPillarContent } from "@/lib/content/loadPillar";
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

  const {
    pillar_id,
    artifact_content,
  }: {
    pillar_id: PillarId;
    artifact_content: string;
  } = await req.json();

  if (!pillar_id || artifact_content === undefined) {
    return NextResponse.json({ error: "pillar_id and artifact_content required" }, { status: 400 });
  }

  const pillarContent = loadPillarContent(pillar_id);
  const { artifact_type, artifact_name } = pillarContent.build_artifact;

  await saveBuildArtifact(uid, pillar_id, {
    user_email: userEmail,
    day_number: pillarContent.day_number,
    artifact_type: artifact_type as "checklist" | "prompt_template" | "system_prompt" | "workflow_doc" | "agent_design",
    artifact_title: artifact_name,
    artifact_content,
  });

  return NextResponse.json({ ok: true });
}
