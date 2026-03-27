import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { getAdminAuth } from "@/lib/firebase/admin";
import { getUser, getTrainingProgressDoc } from "@/lib/firestore/db";
import { loadPillarContent } from "@/lib/content/loadPillar";
import { DayPageClient } from "./DayPageClient";
import type { Timestamp } from "firebase-admin/firestore";
import type { TrainingProgress } from "@/lib/firestore/types";

interface PageProps {
  params: Promise<{ pillar_id: string }>;
}

/** Converts a Firestore Timestamp to ISO string, or null. */
function tsToIso(ts: Timestamp | undefined | null): string | null {
  if (!ts) return null;
  return ts.toDate().toISOString();
}

/** Plain-serialisable version of TrainingProgress (no Timestamps). */
export interface SerializedProgress {
  is_locked: boolean;
  reading_completed_at: string | null;
  practice_completed_at: string | null;
  quiz_completed_at: string | null;
  quiz_passed: boolean;
  quiz_score: number | null;
  build_completed_at: string | null;
}

export default async function DayPage({ params }: PageProps) {
  const { pillar_id } = await params;

  // Auth
  const sessionCookie = (await cookies()).get("__session")?.value;
  if (!sessionCookie) redirect("/");

  let uid: string;
  let userEmail: string;
  try {
    const decoded = await getAdminAuth().verifySessionCookie(sessionCookie, true);
    uid = decoded.uid;
    userEmail = decoded.email ?? "";
  } catch {
    redirect("/");
  }

  // Load pillar content (server-side file read — throws if not found)
  let pillarContent;
  try {
    pillarContent = loadPillarContent(pillar_id);
  } catch {
    // Pillar doesn't exist or content not yet authored
    redirect("/dashboard");
  }

  // Load training progress
  const progress = await getTrainingProgressDoc(uid, pillar_id as import("@/lib/firestore/types").PillarId);
  if (!progress || progress.is_locked) {
    redirect("/dashboard");
  }

  // Check user exists
  const user = await getUser(uid);
  if (!user?.program_started_at) {
    redirect("/onboarding");
  }

  const serializedProgress: SerializedProgress = {
    is_locked: progress.is_locked,
    reading_completed_at: tsToIso((progress as TrainingProgress & { reading_completed_at?: Timestamp }).reading_completed_at),
    practice_completed_at: tsToIso((progress as TrainingProgress & { practice_completed_at?: Timestamp }).practice_completed_at),
    quiz_completed_at: tsToIso((progress as TrainingProgress & { quiz_completed_at?: Timestamp }).quiz_completed_at),
    quiz_passed: progress.quiz_passed ?? false,
    quiz_score: progress.quiz_score ?? null,
    build_completed_at: tsToIso((progress as TrainingProgress & { build_completed_at?: Timestamp }).build_completed_at),
  };

  return (
    <DayPageClient
      pillarContent={pillarContent}
      initialProgress={serializedProgress}
      pillarId={pillar_id}
      uid={uid}
      userEmail={userEmail}
      displayName={user.display_name}
    />
  );
}
