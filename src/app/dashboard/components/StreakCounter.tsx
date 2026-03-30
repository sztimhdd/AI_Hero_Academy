"use client";

import { useTranslations } from "next-intl";

interface Props {
  streakDays: number;
  lastActiveDate: string | null;
}

function isAtRisk(lastActiveDate: string | null): boolean {
  if (!lastActiveDate) return false;
  const today = new Date().toISOString().slice(0, 10);
  if (lastActiveDate === today) return false;
  return new Date().getHours() >= 20;
}

export function StreakCounter({ streakDays, lastActiveDate }: Props) {
  const t = useTranslations("dashboard");
  const atRisk = isAtRisk(lastActiveDate);
  const today = new Date().toISOString().slice(0, 10);
  const activeToday = lastActiveDate === today;

  return (
    <div className="flex items-center gap-4 rounded-2xl bg-white/5 border border-white/10 px-5 py-4">
      <span className="text-3xl select-none" role="img" aria-label="streak">🔥</span>
      <div>
        <div className="flex items-baseline gap-1">
          <span className="text-2xl font-bold text-white">{streakDays}</span>
          <span className="text-slate-400 text-sm">
            {t("streakDays", { count: streakDays })}
          </span>
        </div>
        {atRisk && !activeToday && (
          <p className="text-amber-400 text-xs mt-0.5">{t("streakAtRisk")}</p>
        )}
        {activeToday && (
          <p className="text-emerald-400 text-xs mt-0.5">{t("streakActiveToday")}</p>
        )}
      </div>
    </div>
  );
}
