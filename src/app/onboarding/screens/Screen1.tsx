"use client";

import { en } from "@/lib/i18n/en";

type T = typeof en;

const ROLES = [
  "Marketer", "Product Manager", "Engineer / Developer", "Designer",
  "Teacher / Educator", "HR / People Ops", "Operations", "Finance / Analyst",
  "Consultant", "Executive / Leader", "Sales", "Other",
];

const INDUSTRIES = [
  "Technology", "Healthcare", "Finance / Banking", "Education",
  "Retail / E-commerce", "Manufacturing", "Consulting", "Government / Public Sector",
  "Media / Entertainment", "Non-profit", "Other",
];

interface Screen1Props {
  copy: T;
  values: {
    declared_role: string;
    declared_industry: string;
    daily_work_desc: string;
  };
  onChange: (field: string, value: string) => void;
  onNext: () => void;
}

export default function Screen1({ copy, values, onChange, onNext }: Screen1Props) {
  const canProceed =
    values.declared_role.trim() &&
    values.declared_industry.trim() &&
    values.daily_work_desc.trim().length >= 20;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">{copy["onboarding.s1.title"]}</h2>
      </div>

      {/* Role */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-slate-300">
          {copy["onboarding.s1.role_label"]}
        </label>
        <select
          value={values.declared_role}
          onChange={(e) => onChange("declared_role", e.target.value)}
          className="w-full bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="" className="bg-slate-900">{copy["onboarding.s1.role_placeholder"]}</option>
          {ROLES.map((r) => (
            <option key={r} value={r.toLowerCase().replace(/\s*\/.*/, "").replace(/\s+/g, "_")} className="bg-slate-900">
              {r}
            </option>
          ))}
        </select>
      </div>

      {/* Industry */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-slate-300">
          {copy["onboarding.s1.industry_label"]}
        </label>
        <select
          value={values.declared_industry}
          onChange={(e) => onChange("declared_industry", e.target.value)}
          className="w-full bg-white/10 border border-white/20 text-white rounded-lg px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="" className="bg-slate-900">{copy["onboarding.s1.industry_placeholder"]}</option>
          {INDUSTRIES.map((i) => (
            <option key={i} value={i.toLowerCase().replace(/\s*\/.*/, "").replace(/\s+/g, "_")} className="bg-slate-900">
              {i}
            </option>
          ))}
        </select>
      </div>

      {/* Daily work */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-slate-300">
          {copy["onboarding.s1.daily_work_label"]}
        </label>
        <textarea
          value={values.daily_work_desc}
          onChange={(e) => onChange("daily_work_desc", e.target.value)}
          placeholder={copy["onboarding.s1.daily_work_placeholder"]}
          rows={4}
          className="w-full bg-white/10 border border-white/20 text-white placeholder-slate-500 rounded-lg px-3 py-2.5 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <p className="text-xs text-slate-500 text-right">
          {values.daily_work_desc.length < 20
            ? `${20 - values.daily_work_desc.length} more characters needed`
            : "✓"}
        </p>
      </div>

      <button
        type="button"
        disabled={!canProceed}
        onClick={onNext}
        className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold transition-colors"
      >
        {copy["onboarding.next"]}
      </button>
    </div>
  );
}
