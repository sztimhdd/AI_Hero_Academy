"use client";

import { en } from "@/lib/i18n/en";

type T = typeof en;

const MOTIVATIONS = [
  { id: "save_time", key: "onboarding.s2.motivation_save_time" },
  { id: "quality",   key: "onboarding.s2.motivation_quality" },
  { id: "career",    key: "onboarding.s2.motivation_career" },
  { id: "explore",   key: "onboarding.s2.motivation_explore" },
] as const;

interface Screen2Props {
  copy: T;
  values: {
    current_ai_usage: string;
    primary_motivation: string;
  };
  onChange: (field: string, value: string) => void;
  onNext: () => void;
  onBack: () => void;
}

export default function Screen2({ copy, values, onChange, onNext, onBack }: Screen2Props) {
  const canProceed = values.current_ai_usage.trim().length >= 10 && values.primary_motivation;

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white">{copy["onboarding.s2.title"]}</h2>

      {/* AI tool usage */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-slate-300">
          {copy["onboarding.s2.tools_label"]}
        </label>
        <textarea
          value={values.current_ai_usage}
          onChange={(e) => onChange("current_ai_usage", e.target.value)}
          placeholder={copy["onboarding.s2.tools_placeholder"]}
          rows={3}
          className="w-full bg-white/10 border border-white/20 text-white placeholder-slate-500 rounded-lg px-3 py-2.5 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Primary motivation */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-slate-300">
          {copy["onboarding.s2.motivation_label"]}
        </label>
        <div className="grid grid-cols-1 gap-2">
          {MOTIVATIONS.map(({ id, key }) => (
            <button
              key={id}
              type="button"
              onClick={() => onChange("primary_motivation", id)}
              className={`text-left px-4 py-3 rounded-xl border transition-all text-sm font-medium ${
                values.primary_motivation === id
                  ? "bg-blue-600 border-blue-500 text-white"
                  : "bg-white/10 border-white/20 text-slate-300 hover:bg-white/20"
              }`}
            >
              {copy[key]}
            </button>
          ))}
        </div>
      </div>

      <div className="flex gap-3">
        <button
          type="button"
          onClick={onBack}
          className="flex-1 py-3 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold transition-colors"
        >
          {copy["onboarding.back"]}
        </button>
        <button
          type="button"
          disabled={!canProceed}
          onClick={onNext}
          className="flex-1 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold transition-colors"
        >
          {copy["onboarding.next"]}
        </button>
      </div>
    </div>
  );
}
