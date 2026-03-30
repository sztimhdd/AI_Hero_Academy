import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { updateStreak } from "@/lib/firestore/db";

export async function POST() {
  try {
    const auth = await getAuthFromCookies(await cookies());
    await updateStreak(auth.uid);
    return NextResponse.json({ ok: true });
  } catch {
    // Non-critical — never block the UI
    return NextResponse.json({ ok: false }, { status: 200 });
  }
}
