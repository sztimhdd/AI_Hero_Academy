import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { getUser, getLatestDiagnosticSession } from "@/lib/firestore/db";
import type { Timestamp } from "firebase-admin/firestore";
import type { DiagnosticSession } from "@/lib/firestore/types";
import { ProfileClient } from "./ProfileClient";
import { NextIntlClientProvider } from "next-intl";

function serializeDiagnostic(d: DiagnosticSession) {
  const ts = (t: Timestamp) => t.toDate().toISOString();
  return {
    pillar_scores: d.pillar_scores as Record<string, number>,
    overall_score: d.overall_score,
    completed_at: ts(d.completed_at),
  };
}

export default async function ProfilePage() {
  const jar = await cookies();

  let uid: string;
  try {
    const auth = await getAuthFromCookies(jar);
    uid = auth.uid;
  } catch {
    redirect("/");
  }

  const user = await getUser(uid);
  if (!user?.program_started_at) redirect("/onboarding");

  const locale = (user.lang ?? "en") as "en" | "zh";
  const messages = (await import(`@/i18n/messages/${locale}.json`)).default;

  const diagnostic = await getLatestDiagnosticSession(uid);

  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      <ProfileClient
        user={{
          display_name: user.display_name,
          declared_role: user.declared_role,
          declared_industry: user.declared_industry,
          streak_days: user.streak_days ?? 0,
        }}
        diagnostic={diagnostic ? serializeDiagnostic(diagnostic) : null}
        diagnosticHistory={diagnostic ? [serializeDiagnostic(diagnostic)] : []}
      />
    </NextIntlClientProvider>
  );
}
