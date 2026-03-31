"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { DayArcTimeline } from "./components/DayArcTimeline";
import { StreakCounter } from "./components/StreakCounter";
import { ArtifactGallery } from "./components/ArtifactGallery";
import { ProfilePill } from "./components/ProfilePill";
import type { ProgressSummary } from "./components/DayArcTimeline";
import type { ArtifactSummary } from "./components/ArtifactGallery";

interface UserSummary {
  display_name: string;
  profile_photo_url: string;
  streak_days: number;
  last_active_date: string | null;
  lang: "en" | "zh";
}

interface Props {
  uid: string;
  userEmail: string;
  user: UserSummary;
  progress: ProgressSummary[];
  artifacts: ArtifactSummary[];
}

export function DashboardClient({
  uid,
  userEmail,
  user,
  progress,
  artifacts,
}: Props) {
  const t = useTranslations("dashboard");

  // Fire streak update on first render (session start)
  useEffect(() => {
    fetch("/api/streak/update", { method: "POST" }).catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [uid]);

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900">
      <div className="max-w-3xl mx-auto px-4 py-8 space-y-8">
        {/* Header */}
        <ProfilePill
          displayName={user.display_name}
          profilePhotoUrl={user.profile_photo_url}
          lang={user.lang}
          userEmail={userEmail}
        />

        {/* Welcome */}
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white">
            {t("welcomeBack", { name: user.display_name || userEmail.split("@")[0] })}
          </h1>
          <p className="text-slate-400 mt-1 text-sm">{t("subtitle")}</p>
          <Link
            href="/profile"
            className="inline-flex items-center gap-1 text-xs text-teal-400 hover:text-teal-300 mt-2 transition-colors"
          >
            {t("viewSkillsProfile")} →
          </Link>
        </div>

        {/* Streak + Pillar Badges */}
        <StreakCounter
          streakDays={user.streak_days}
          lastActiveDate={user.last_active_date}
          progress={progress}
        />

        {/* 7-Day Arc */}
        <DayArcTimeline progress={progress} />

        {/* Build Artifacts */}
        <ArtifactGallery artifacts={artifacts} />
      </div>
    </main>
  );
}
