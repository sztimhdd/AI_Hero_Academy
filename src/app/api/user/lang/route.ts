import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { updateUserLang } from "@/lib/firestore/db";

export async function PATCH(req: NextRequest) {
  try {
    const auth = await getAuthFromCookies(await cookies());
    const { lang } = (await req.json()) as { lang: "en" | "zh" };
    if (lang !== "en" && lang !== "zh") {
      return NextResponse.json({ error: "Invalid lang" }, { status: 400 });
    }
    await updateUserLang(auth.uid, lang);
    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error("[/api/user/lang]", err);
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
}
