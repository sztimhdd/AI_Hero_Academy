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
type StepKey = "reading" | "practice" | "quiz" | "build";

function getDayState(p: ProgressSummary): DayState {
  if (p.is_locked) return "locked";
  if (p.build_completed_at) return "complete";
  if (p.reading_completed_at || p.practice_completed_at || p.quiz_completed_at)
    return "in_progress";
  return "available";
}

function getStepDone(p: ProgressSummary, key: StepKey): boolean {
  switch (key) {
    case "reading":  return !!p.reading_completed_at;
    case "practice": return !!p.practice_completed_at;
    case "quiz":     return !!p.quiz_passed;
    case "build":    return !!p.build_completed_at;
  }
}

const STEPS: { key: StepKey; label: string }[] = [
  { key: "reading",  label: "Read" },
  { key: "practice", label: "Prac" },
  { key: "quiz",     label: "Quiz" },
  { key: "build",    label: "Build" },
];

/* ─── Per-state styling maps ──────────────────────────────────────── */

const CARD_BG: Record<DayState, string> = {
  locked:
    "border-white/8 bg-slate-900/50",
  available:
    "border-blue-500/35 bg-gradient-to-br from-blue-950/50 to-slate-900/70 hover:border-blue-400/55 hover:shadow-lg hover:shadow-blue-900/25 transition-all duration-200",
  in_progress:
    "border-amber-500/40 bg-gradient-to-br from-amber-950/30 to-slate-900/70 hover:border-amber-400/55 hover:shadow-lg hover:shadow-amber-900/20 transition-all duration-200",
  complete:
    "border-emerald-500/25 bg-gradient-to-br from-emerald-950/25 to-slate-900/70 hover:shadow-lg hover:shadow-emerald-900/15 transition-all duration-200",
};

const ACCENT_BAR: Record<DayState, string> = {
  locked:      "bg-slate-700/50",
  available:   "bg-gradient-to-r from-blue-500 to-indigo-500",
  in_progress: "bg-gradient-to-r from-amber-500 to-orange-400",
  complete:    "bg-gradient-to-r from-emerald-500 to-teal-400",
};

const PROGRESS_FILL: Record<DayState, string> = {
  locked:      "bg-slate-600/50",
  available:   "bg-gradient-to-r from-blue-500 to-indigo-400",
  in_progress: "bg-gradient-to-r from-amber-500 to-orange-400",
  complete:    "bg-gradient-to-r from-emerald-500 to-teal-400",
};

const STATE_BADGE: Record<DayState, string> = {
  locked:      "bg-white/5 text-slate-500",
  available:   "bg-blue-500/15 border border-blue-500/35 text-blue-300",
  in_progress: "bg-amber-500/15 border border-amber-500/35 text-amber-300",
  complete:    "bg-emerald-500/10 border border-emerald-500/30 text-emerald-400",
};

const DAY_NUM_WATERMARK: Record<DayState, string> = {
  locked:      "text-slate-700/30",
  available:   "text-blue-800/35",
  in_progress: "text-amber-800/35",
  complete:    "text-emerald-800/30",
};

/** Maps completedSteps (0–4) to a Tailwind width class. */
const PROGRESS_WIDTH: Record<number, string> = {
  0: "w-0",
  1: "w-1/4",
  2: "w-1/2",
  3: "w-3/4",
  4: "w-full",
};

/** Maps card index (0–6) to a CSS delay class defined in globals.css. */
const ANIM_DELAY_CLS = [
  "daycard-delay-0",
  "daycard-delay-1",
  "daycard-delay-2",
  "daycard-delay-3",
  "daycard-delay-4",
  "daycard-delay-5",
  "daycard-delay-6",
];

const PILLAR_COLOR: Record<DayState, string> = {
  locked:      "text-slate-500",
  available:   "text-white",
  in_progress: "text-white",
  complete:    "text-slate-100",
};

/* ─── Individual Day Card ─────────────────────────────────────────── */

function DayCard({
  p,
  idx,
  isCapstone,
}: {
  p: ProgressSummary;
  idx: number;
  isCapstone: boolean;
}) {
  const t = useTranslations("dashboard");
  const state = getDayState(p);
  const stateKey = state === "in_progress" ? "inProgress" : state;
  const stateLabel = t(`dayState.${stateKey}`);
  const pillarLabel = t(`pillar.${p.pillar_id}`);
  const dayLabel = isCapstone ? "Day 7" : `Day ${p.day_number}`;
  const completedSteps = STEPS.filter((s) => getStepDone(p, s.key)).length;

  const stateIcon =
    state === "locked"      ? "🔒" :
    state === "complete"    ? "✓"  :
    state === "in_progress" ? "↻"  : "▶";

  const inner = (
    <div
      className={[
        "relative rounded-2xl border overflow-hidden",
        CARD_BG[state],
        isCapstone ? "flex flex-row" : "flex flex-col",
      ].join(" ")}
    >
      {/* Accent bar — top strip for regular cards, left ribbon for capstone */}
      <div
        className={[
          "shrink-0",
          isCapstone ? "w-1" : "h-[3px] w-full",
          ACCENT_BAR[state],
        ].join(" ")}
      />

      {/* Card body */}
      <div
        className={[
          "relative flex flex-col gap-3 p-4",
          isCapstone ? "flex-1 sm:flex-row sm:items-center sm:gap-8" : "",
        ].join(" ")}
      >
        {/* Large day-number watermark */}
        <span
          aria-hidden="true"
          className={[
            "absolute top-1.5 right-3 font-black leading-none pointer-events-none select-none",
            isCapstone ? "text-7xl sm:text-8xl" : "text-5xl",
            DAY_NUM_WATERMARK[state],
          ].join(" ")}
        >
          {isCapstone ? "7" : p.day_number}
        </span>

        {/* Top row: day label + state badge */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-[10px] font-bold uppercase tracking-[0.12em] text-slate-500">
            {dayLabel}
          </span>
          <span
            className={[
              "inline-flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded-full",
              STATE_BADGE[state],
            ].join(" ")}
          >
            {/* Pulsing live-dot for active day */}
            {state === "in_progress" && (
              <span className="relative flex h-1.5 w-1.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-amber-500" />
              </span>
            )}
            {stateIcon} {stateLabel}
          </span>
        </div>

        {/* Pillar name */}
        <p
          className={[
            "font-semibold leading-snug pr-10",
            isCapstone ? "text-base sm:text-lg" : "text-sm",
            PILLAR_COLOR[state],
          ].join(" ")}
        >
          {pillarLabel}
        </p>

        {/* 4-step module pills — hidden for capstone to reduce noise */}
        {!isCapstone && (
          <div className="flex gap-1 flex-wrap">
            {STEPS.map((step) => {
              const done = getStepDone(p, step.key);
              const cls =
                state === "locked"
                  ? "border-white/6 text-slate-700"
                  : done
                  ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-400"
                  : "border-white/10 text-slate-500";
              return (
                <span
                  key={step.key}
                  className={[
                    "text-[9px] font-medium px-1.5 py-0.5 rounded border",
                    cls,
                  ].join(" ")}
                >
                  {done ? "✓" : "·"} {step.label}
                </span>
              );
            })}
            {/* Quiz score badge */}
            {p.quiz_score !== null && state !== "locked" && (
              <span className="ml-auto text-[9px] font-medium px-1.5 py-0.5 rounded border border-violet-500/30 bg-violet-500/10 text-violet-300">
                {p.quiz_score}%
              </span>
            )}
          </div>
        )}

        {/* Progress bar + fraction label */}
        {state !== "locked" && (
          <div className={isCapstone ? "sm:w-48 flex-none" : ""}>
            <div className="flex items-center justify-between mb-1">
              <span className="text-[9px] text-slate-500">
                {completedSteps} / 4
              </span>
              {isCapstone && p.quiz_score !== null && (
                <span className="text-[9px] font-medium text-violet-400">
                  {p.quiz_score}%
                </span>
              )}
            </div>
            <div className="h-1 rounded-full bg-white/8 overflow-hidden">
              <div
                className={[
                  "h-full rounded-full",
                  PROGRESS_FILL[state],
                  PROGRESS_WIDTH[completedSteps] ?? "w-0",
                ].join(" ")}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );

  const delayCls = ANIM_DELAY_CLS[idx] ?? "daycard-delay-0";

  if (state === "locked") {
    return (
      <div className={`daycard-enter ${delayCls} opacity-50`}>
        {inner}
      </div>
    );
  }

  return (
    <Link
      href={`/day/${p.pillar_id}`}
      className={`block daycard-enter ${delayCls}`}
    >
      {inner}
    </Link>
  );
}

/* ─── Timeline container ──────────────────────────────────────────── */

export function DayArcTimeline({ progress }: { progress: ProgressSummary[] }) {
  const t = useTranslations("dashboard");

  const regular = progress.filter((p) => p.pillar_id !== "capstone");
  const capstone = progress.find((p) => p.pillar_id === "capstone");

  return (
    <section>
      <h2 className="text-[11px] font-bold text-slate-400 uppercase tracking-[0.15em] mb-4">
        {t("journeyTitle")}
      </h2>

      {/* 3-column grid for Days 1–6 */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-3">
        {regular.map((p, idx) => (
          <DayCard key={p.pillar_id} p={p} idx={idx} isCapstone={false} />
        ))}
      </div>

      {/* Capstone — full-width banner */}
      {capstone && (
        <DayCard p={capstone} idx={regular.length} isCapstone />
      )}
    </section>
  );
}
