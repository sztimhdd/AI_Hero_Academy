"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import type { ProgressSummary } from "./DayArcTimeline";

const PILLAR_COLORS: Record<string, string> = {
  p1: "#3b82f6",
  p2: "#8b5cf6",
  p3: "#06b6d4",
  p4: "#f59e0b",
  p5: "#10b981",
  p6: "#ef4444",
};

function PillarBadgeSvg({ pillarId, complete }: { pillarId: string; complete: boolean }) {
  const color = complete ? (PILLAR_COLORS[pillarId] ?? "#475569") : "#475569";
  const textColor = complete ? "#fff" : "#94a3b8";
  const shortLabel = pillarId.toUpperCase();

  return (
    <svg viewBox="0 0 80 80" className="w-full h-full" role="img">
      <polygon
        points="40,4 74,22 74,58 40,76 6,58 6,22"
        fill={complete ? color + "33" : "#1e293b"}
        stroke={color}
        strokeWidth="2"
      />
      <polygon
        points="40,12 68,27 68,53 40,68 12,53 12,27"
        fill="none"
        stroke={color}
        strokeWidth="1"
        opacity="0.4"
      />
      <text
        x="40"
        y="45"
        textAnchor="middle"
        fontSize="18"
        fontWeight="700"
        fill={textColor}
        fontFamily="system-ui, sans-serif"
      >
        {shortLabel}
      </text>
    </svg>
  );
}

function BadgePopover({
  pillarId,
  progress,
  onClose,
}: {
  pillarId: string;
  progress: ProgressSummary;
  onClose: () => void;
}) {
  const t = useTranslations("dashboard");
  const complete = !!progress.build_completed_at;
  const label = t(`pillar.${pillarId}`);

  return (
    <div
      className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-20 w-52 rounded-xl bg-slate-800 border border-white/10 shadow-xl p-4 text-sm"
      onClick={(e) => e.stopPropagation()}
    >
      <button
        type="button"
        onClick={onClose}
        className="absolute top-2 right-2 text-slate-500 hover:text-white"
        aria-label="Close"
      >
        ✕
      </button>
      <p className="font-semibold text-white mb-1">{label}</p>
      {complete ? (
        <>
          <p className="text-emerald-400 text-xs mb-1">✓ {t("badgeComplete")}</p>
          {progress.quiz_score !== null && (
            <p className="text-slate-400 text-xs">
              {t("badgeQuizScore", { score: Math.round(progress.quiz_score * 100) })}
            </p>
          )}
        </>
      ) : progress.is_locked ? (
        <p className="text-slate-500 text-xs">{t("badgeLocked")}</p>
      ) : (
        <p className="text-slate-400 text-xs">{t("badgeInProgress")}</p>
      )}
    </div>
  );
}

export function PillarBadges({ progress }: { progress: ProgressSummary[] }) {
  const t = useTranslations("dashboard");
  const [openId, setOpenId] = useState<string | null>(null);
  const pillars = progress.filter((p) => p.pillar_id !== "capstone");

  return (
    <section>
      <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">
        {t("pillarBadgesTitle")}
      </h2>
      <div className="grid grid-cols-6 gap-3">
        {pillars.map((p) => {
          const complete = !!p.build_completed_at;
          return (
            <div key={p.pillar_id} className="relative flex flex-col items-center">
              <button
                type="button"
                className="w-12 h-12 sm:w-14 sm:h-14 focus:outline-none"
                onClick={() => setOpenId(openId === p.pillar_id ? null : p.pillar_id)}
                aria-label={t(`pillar.${p.pillar_id}`)}
              >
                <PillarBadgeSvg pillarId={p.pillar_id} complete={complete} />
              </button>
              {openId === p.pillar_id && (
                <BadgePopover
                  pillarId={p.pillar_id}
                  progress={p}
                  onClose={() => setOpenId(null)}
                />
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
