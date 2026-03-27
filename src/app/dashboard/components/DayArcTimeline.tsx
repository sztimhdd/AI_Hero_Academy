"use client";

import Link from "next/link";
import { useTranslations } from "next-intl";

export interface ProgressSummary {
  pillar_id: string;
  day_number: number;
  sequence_order: number;
  is_locked: boolean;
  reading_completed_at: string | null;
  practice_completed_at: string | null;
  quiz_completed_at: string | null;
  quiz_passed: boolean;
  quiz_score: number | null;
  build_completed_at: string | null;
  pillar_score_after: number | null;
}

type DayState = "locked" | "available" | "in_progress" | "complete";

function getDayState(p: ProgressSummary): DayState {
  if (p.is_locked) return "locked";
  if (p.build_completed_at) return "complete";
  if (p.reading_completed_at || p.practice_completed_at || p.quiz_completed_at)
    return "in_progress";
  return "available";
}

const STATE_STYLES: Record<DayState, string> = {
  locked: "bg-white/5 border-white/10 opacity-40",
  available: "bg-blue-600/20 border-blue-500/50 hover:border-blue-400/70",
  in_progress: "bg-amber-600/20 border-amber-500/50 hover:border-amber-400/70",
  complete: "bg-emerald-600/20 border-emerald-500/40",
};

function StateIcon({ state }: { state: DayState }) {
  if (state === "locked")
    return (
      <svg className="w-4 h-4 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
      </svg>
    );
  if (state === "complete")
    return (
      <svg className="w-4 h-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
      </svg>
    );
  return null;
}

export function DayArcTimeline({ progress }: { progress: ProgressSummary[] }) {
  const t = useTranslations("dashboard");

  return (
    <section>
      <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">
        {t("journeyTitle")}
      </h2>
      <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-hide">
        {progress.map((p) => {
          const state = getDayState(p);
          const isCapstone = p.pillar_id === "capstone";
          const href = `/day/${p.pillar_id}`;
          const stateKey = state === "in_progress" ? "inProgress" : state;
          const stateLabel = t(`dayState.${stateKey}`);
          const pillarLabel = t(`pillar.${p.pillar_id}`);

          return (
            <div
              key={p.pillar_id}
              className={`flex-none w-32 rounded-2xl border p-4 transition-colors ${STATE_STYLES[state]}`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs text-slate-400">
                  {isCapstone ? "Day 7" : `Day ${p.day_number}`}
                </span>
                <StateIcon state={state} />
              </div>
              <p className="text-xs font-medium text-white leading-tight mb-3 min-h-[2rem]">
                {pillarLabel}
              </p>
              {state !== "locked" ? (
                <Link
                  href={href}
                  className={`block text-center text-xs font-semibold py-1.5 px-2 rounded-lg transition-colors ${
                    state === "complete"
                      ? "text-emerald-400 bg-emerald-500/10"
                      : state === "in_progress"
                      ? "text-amber-300 bg-amber-500/15 hover:bg-amber-500/25"
                      : "text-blue-300 bg-blue-500/15 hover:bg-blue-500/25"
                  }`}
                >
                  {stateLabel}
                </Link>
              ) : (
                <span className="block text-center text-xs text-slate-600 py-1.5">
                  {stateLabel}
                </span>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
