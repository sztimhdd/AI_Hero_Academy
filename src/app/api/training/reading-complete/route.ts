import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { Timestamp } from "firebase-admin/firestore";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { upsertTrainingProgress } from "@/lib/firestore/db";
import type { PillarId } from "@/lib/firestore/types";

export async function POST(req: NextRequest) {
  let uid: string;
  try {
    const auth = await getAuthFromCookies(await cookies());
    uid = auth.uid;
  } catch {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { pillar_id } = await req.json();
  if (!pillar_id) {
    return NextResponse.json({ error: "pillar_id required" }, { status: 400 });
  }

  await upsertTrainingProgress(uid, pillar_id as PillarId, {
    reading_completed_at: Timestamp.now(),
  });

  return NextResponse.json({ ok: true });
}
