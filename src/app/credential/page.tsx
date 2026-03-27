import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { getCredential } from "@/lib/firestore/db";
import { CredentialPageClient } from "./CredentialPageClient";

export default async function CredentialPage() {
  let uid: string;
  try {
    const auth = await getAuthFromCookies(await cookies());
    uid = auth.uid;
  } catch {
    redirect("/");
  }

  const credential = await getCredential(uid);
  if (!credential) redirect("/dashboard");

  const appUrl = process.env.NEXT_PUBLIC_APP_URL ?? "https://ai-hero-academy.app";
  const issuedDate = credential.issued_at.toDate().toLocaleDateString("en-US", {
    year: "numeric", month: "long", day: "numeric",
  });
  const issuedYear = credential.issued_at.toDate().getFullYear();
  const issuedMonth = credential.issued_at.toDate().getMonth() + 1; // 1-indexed

  const linkedInUrl =
    `https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME` +
    `&name=AI-Supercharged+Intermediate` +
    `&issueYear=${issuedYear}` +
    `&issueMonth=${issuedMonth}` +
    `&certUrl=${encodeURIComponent(`${appUrl}/credential`)}` +
    `&certId=${encodeURIComponent(credential.credential_id)}`;

  return (
    <CredentialPageClient
      uid={uid}
      displayName={credential.display_name}
      overallScore={credential.overall_score}
      pillarScores={credential.pillar_scores as unknown as Record<string, number>}
      issuedDate={issuedDate}
      credentialId={credential.credential_id}
      linkedInUrl={linkedInUrl}
      appUrl={appUrl}
    />
  );
}
