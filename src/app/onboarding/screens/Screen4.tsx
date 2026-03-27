"use client";

import { en } from "@/lib/i18n/en";
import { PillarScores } from "@/lib/firestore/types";

type T = typeof en;

const PILLAR_KEYS = [
  { id: "p1", labelKey: "onboarding.s4.pillar.p1" },
  { id: "p2", labelKey: "onboarding.s4.pillar.p2" },
  { id: "p3", labelKey: "onboarding.s4.pillar.p3" },
  { id: "p4", labelKey: "onboarding.s4.pillar.p4" },
  { id: "p5", labelKey: "onboarding.s4.pillar.p5" },
  { id: "p6", labelKey: "onboarding.s4.pillar.p6" },
] as const;

interface Screen4Props {
  copy: T;
  pillarScores: PillarScores;
  onStart: () => void;
  loading: boolean;
}

function scoreColor(score: number): string {
  if (score >= 80) return "bg-emerald-500";
  if (score >= 55) return "bg-blue-500";
  if (score >= 35) return "bg-amber-500";
  return "bg-red-500";
}

function scoreLabel(score: number): string {
  if (score >= 80) return "Strong";
  if (score >= 55) return "Developing";
  if (score >= 35) return "Early";
  return "Beginner";
}

export default function Screen4({ copy, pillarScores, onStart, loading }: Screen4Props) {
  const overall = Math.round(
    Object.values(pillarScores).reduce((a, b) => a + b, 0) / 6
  );

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">{copy["onboarding.s4.title"]}</h2>
        <p className="text-slate-400 text-sm mt-1">{copy["onboarding.s4.subtitle"]}</p>
      </div>

      {/* Overall score */}
      <div className="bg-white/10 rounded-2xl p-5 text-center border border-white/10">
        <div className="text-5xl font-bold text-white">{overall}</div>
        <div className="text-slate-400 text-sm mt-1">Overall AI Readiness Score</div>
        <div className="text-blue-400 font-medium mt-1">{scoreLabel(overall)}</div>
      </div>

      {/* Pillar bars */}
      <div className="space-y-3">
        {PILLAR_KEYS.map(({ id, labelKey }) => {
          const score = pillarScores[id as keyof PillarScores];
          return (
            <div key={id} className="space-y-1">
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-300">{copy[labelKey]}</span>
                <span className="text-sm font-mono text-white">{score}</span>
              </div>
              <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${scoreColor(score)}`}
                  style={{ width: `${score}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      <p className="text-slate-400 text-xs text-center leading-relaxed">
        Your 7-day program is personalised to close these gaps. Day 1 starts with your lowest-scoring pillar.
      </p>

      <button
        type="button"
        disabled={loading}
        onClick={onStart}
        className="w-full py-4 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed text-white font-bold text-lg transition-colors"
      >
        {loading ? copy["common.loading"] : copy["onboarding.s4.cta"]}
      </button>
    </div>
  );
}
