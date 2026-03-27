import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { getAuthFromCookies } from "@/lib/auth/verify";
import {
  getUser,
  getTrainingProgress,
  getBuildArtifacts,
} from "@/lib/firestore/db";
import type { Timestamp } from "firebase-admin/firestore";
import type { TrainingProgress, BuildArtifact } from "@/lib/firestore/types";
import { DashboardClient } from "./DashboardClient";

/** Strips Firestore Timestamps so data is serialisable across the RSC boundary. */
function serializeProgress(p: TrainingProgress) {
  function ts(t: Timestamp | undefined | null): string | null {
    return t ? t.toDate().toISOString() : null;
  }
  return {
    uid: p.uid,
    pillar_id: p.pillar_id,
    day_number: p.day_number,
    sequence_order: p.sequence_order,
    is_locked: p.is_locked,
    reading_completed_at: ts(p.reading_completed_at),
    practice_completed_at: ts(p.practice_completed_at),
    quiz_completed_at: ts(p.quiz_completed_at),
    quiz_score: p.quiz_score ?? null,
    quiz_passed: p.quiz_passed ?? false,
    build_completed_at: ts(p.build_completed_at),
    pillar_score_after: p.pillar_score_after ?? null,
  };
}

function serializeArtifact(a: BuildArtifact) {
  return {
    uid: a.uid,
    pillar_id: a.pillar_id,
    day_number: a.day_number,
    artifact_type: a.artifact_type,
    artifact_title: a.artifact_title,
    artifact_content: a.artifact_content,
    created_at: a.created_at.toDate().toISOString(),
  };
}

export default async function DashboardPage() {
  const jar = await cookies();

  let uid: string;
  let userEmail: string;
  try {
    const auth = await getAuthFromCookies(jar);
    uid = auth.uid;
    userEmail = auth.email;
  } catch {
    redirect("/");
  }

  const user = await getUser(uid);
  if (!user?.program_started_at) redirect("/onboarding");

  const [progressDocs, artifactDocs] = await Promise.all([
    getTrainingProgress(uid),
    getBuildArtifacts(uid),
  ]);

  return (
    <DashboardClient
      uid={uid}
      userEmail={userEmail}
      user={{
        display_name: user.display_name,
        profile_photo_url: user.profile_photo_url,
        streak_days: user.streak_days ?? 0,
        last_active_date: user.last_active_date ?? null,
        lang: user.lang,
      }}
      progress={progressDocs.map(serializeProgress)}
      artifacts={artifactDocs.map(serializeArtifact)}
    />
  );
}
