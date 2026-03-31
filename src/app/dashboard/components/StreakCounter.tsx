"use client";

import { useTranslations } from "next-intl";
import type { ProgressSummary } from "./DayArcTimeline";

interface Props {
  streakDays: number;
  lastActiveDate: string | null;
  progress: ProgressSummary[];
}

const PILLAR_COLORS: Record<string, string> = {
  p1: "#3b82f6",
  p2: "#8b5cf6",
  p3: "#06b6d4",
  p4: "#f59e0b",
  p5: "#10b981",
  p6: "#ef4444",
};

function MiniBadge({ pillarId, complete }: { pillarId: string; complete: boolean }) {
  const color = complete ? (PILLAR_COLORS[pillarId] ?? "#475569") : "#475569";
  const textColor = complete ? "#fff" : "#64748b";
  return (
    <svg viewBox="0 0 80 80" className="w-8 h-8" role="img" aria-label={pillarId.toUpperCase()}>
      <polygon
        points="40,4 74,22 74,58 40,76 6,58 6,22"
        fill={complete ? color + "33" : "#1e293b"}
        stroke={color}
        strokeWidth="2.5"
      />
      <text
        x="40"
        y="47"
        textAnchor="middle"
        fontSize="22"
        fontWeight="700"
        fill={textColor}
        fontFamily="system-ui, sans-serif"
      >
        {pillarId.toUpperCase()}
      </text>
    </svg>
  );
}

function isAtRisk(lastActiveDate: string | null): boolean {
  if (!lastActiveDate) return false;
  const today = new Date().toISOString().slice(0, 10);
  if (lastActiveDate === today) return false;
  return new Date().getHours() >= 20;
}

export function StreakCounter({ streakDays, lastActiveDate, progress }: Props) {
  const t = useTranslations("dashboard");
  const atRisk = isAtRisk(lastActiveDate);
  const today = new Date().toISOString().slice(0, 10);
  const activeToday = lastActiveDate === today;

  const pillars = progress.filter((p) => p.pillar_id !== "capstone");

  return (
    <div className="flex items-center gap-4 rounded-2xl bg-white/5 border border-white/10 px-5 py-4">
      {/* Streak info */}
      <span className="text-3xl select-none flex-shrink-0" role="img" aria-label="streak">🔥</span>
      <div className="flex-shrink-0">
        <div className="flex items-baseline gap-1">
          <span className="text-2xl font-bold text-white">{streakDays}</span>
          <span className="text-slate-400 text-sm">
            {t("streakDays")}
          </span>
        </div>
        {atRisk && !activeToday && (
          <p className="text-amber-400 text-xs mt-0.5">{t("streakAtRisk")}</p>
        )}
        {activeToday && (
          <p className="text-emerald-400 text-xs mt-0.5">{t("streakActiveToday")}</p>
        )}
      </div>

      {/* Pillar mini-badges */}
      {pillars.length > 0 && (
        <div className="ml-auto flex items-center gap-1.5">
          {pillars.map((p) => (
            <MiniBadge
              key={p.pillar_id}
              pillarId={p.pillar_id}
              complete={!!p.build_completed_at}
            />
          ))}
        </div>
      )}
    </div>
  );
}
