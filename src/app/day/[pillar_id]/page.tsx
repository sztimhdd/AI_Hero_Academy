import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { getAuthFromCookies } from "@/lib/auth/verify";
import { getUser, getTrainingProgressDoc } from "@/lib/firestore/db";
import { loadPillarContent } from "@/lib/content/loadPillar";
import { loadCapstoneContent } from "@/lib/content/loadCapstone";
import { fillScenario } from "@/lib/content/capstoneUtils";
import { DayPageClient } from "./DayPageClient";
import { CapstonePageClient } from "./CapstonePageClient";
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
    const auth = await getAuthFromCookies(await cookies());
    uid = auth.uid;
    userEmail = auth.email;
  } catch {
    redirect("/");
  }

  // Load training progress (applies to both regular days and capstone)
  const progress = await getTrainingProgressDoc(
    uid,
    pillar_id as import("@/lib/firestore/types").PillarId
  );
  if (!progress || progress.is_locked) {
    redirect("/dashboard");
  }

  // Check user exists
  const user = await getUser(uid);
  if (!user?.program_started_at) {
    redirect("/onboarding");
  }

  const lang = user.lang ?? "en";

  // ── Capstone branch ─────────────────────────────────────────────────────────
  if (pillar_id === "capstone") {
    const capstone = loadCapstoneContent(lang);
    const scenario = fillScenario(
      capstone.scenario_template,
      user.declared_role ?? "professional",
      user.declared_industry ?? "their industry",
      user.daily_work_desc
    );
    const alreadyPassed = progress.quiz_passed ?? false;

    return (
      <CapstonePageClient
        uid={uid}
        userEmail={userEmail}
        displayName={user.display_name}
        declaredRole={user.declared_role ?? "professional"}
        declaredIndustry={user.declared_industry ?? "their industry"}
        scenario={scenario}
        capstone={capstone}
        alreadyPassed={alreadyPassed}
      />
    );
  }

  // ── Regular day branch ──────────────────────────────────────────────────────
  let pillarContent;
  try {
    pillarContent = loadPillarContent(pillar_id, lang);
  } catch {
    redirect("/dashboard");
  }

  const serializedProgress: SerializedProgress = {
    is_locked: progress.is_locked,
    reading_completed_at: tsToIso(
      (progress as TrainingProgress & { reading_completed_at?: Timestamp })
        .reading_completed_at
    ),
    practice_completed_at: tsToIso(
      (
        progress as TrainingProgress & {
          practice_completed_at?: Timestamp;
        }
      ).practice_completed_at
    ),
    quiz_completed_at: tsToIso(
      (progress as TrainingProgress & { quiz_completed_at?: Timestamp })
        .quiz_completed_at
    ),
    quiz_passed: progress.quiz_passed ?? false,
    quiz_score: progress.quiz_score ?? null,
    build_completed_at: tsToIso(
      (progress as TrainingProgress & { build_completed_at?: Timestamp })
        .build_completed_at
    ),
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
