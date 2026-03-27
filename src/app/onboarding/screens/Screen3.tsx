"use client";

import { useEffect, useState } from "react";
import { en } from "@/lib/i18n/en";
import diagnosticData from "../../../../content/diagnostic_pillar.json";

type T = typeof en;

interface MCQQuestion {
  id: string;
  pillar: string;
  text: string;
  options: { id: string; text: string }[];
}

interface Screen3Props {
  copy: T;
  profile: {
    declared_role: string;
    declared_industry: string;
    daily_work_desc: string;
  };
  values: {
    mcq_answers: Record<string, string>;
    ai_question_text: string;
    ai_question_answer: string;
  };
  onChange: (field: string, value: unknown) => void;
  onNext: () => void;
  onBack: () => void;
}

export default function Screen3({ copy, profile, values, onChange, onNext, onBack }: Screen3Props) {
  const [aiQuestionLoading, setAiQuestionLoading] = useState(false);
  const questions: MCQQuestion[] = diagnosticData.questions;

  // Fetch AI question on mount if not already loaded
  useEffect(() => {
    if (values.ai_question_text) return;
    setAiQuestionLoading(true);

    fetch("/api/diagnostic/generate-question", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(profile),
    })
      .then((r) => r.json())
      .then((data) => onChange("ai_question_text", data.question ?? ""))
      .catch(() => onChange("ai_question_text", copy["onboarding.s3.fallback_question"]))
      .finally(() => setAiQuestionLoading(false));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const allMcqAnswered = questions.every((q) => values.mcq_answers[q.id]);
  const canProceed =
    allMcqAnswered &&
    values.ai_question_answer.trim().length >= 20;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">{copy["onboarding.s3.title"]}</h2>
        <p className="text-slate-400 text-sm mt-1">{copy["onboarding.s3.subtitle"]}</p>
      </div>

      {/* 5 MCQ questions */}
      {questions.map((q, idx) => (
        <div key={q.id} className="space-y-3">
          <p className="text-sm font-medium text-white">
            {idx + 1}. {q.text}
          </p>
          <div className="space-y-2">
            {q.options.map((opt) => (
              <button
                key={opt.id}
                type="button"
                onClick={() =>
                  onChange("mcq_answers", { ...values.mcq_answers, [q.id]: opt.id })
                }
                className={`w-full text-left px-4 py-2.5 rounded-lg border text-sm transition-all ${
                  values.mcq_answers[q.id] === opt.id
                    ? "bg-blue-600 border-blue-500 text-white"
                    : "bg-white/10 border-white/20 text-slate-300 hover:bg-white/20"
                }`}
              >
                <span className="font-mono mr-2 text-slate-400">{opt.id.toUpperCase()}.</span>
                {opt.text}
              </button>
            ))}
          </div>
        </div>
      ))}

      {/* AI-generated open question */}
      <div className="space-y-3 border-t border-white/10 pt-6">
        <p className="text-sm font-medium text-slate-300">
          {copy["onboarding.s3.ai_question_label"]}
        </p>
        {aiQuestionLoading ? (
          <div className="text-slate-400 text-sm animate-pulse">{copy["common.loading"]}</div>
        ) : (
          <p className="text-white text-sm leading-relaxed">
            {values.ai_question_text || copy["onboarding.s3.fallback_question"]}
          </p>
        )}
        <textarea
          value={values.ai_question_answer}
          onChange={(e) => onChange("ai_question_answer", e.target.value)}
          placeholder="Share your thoughts…"
          rows={4}
          className="w-full bg-white/10 border border-white/20 text-white placeholder-slate-500 rounded-lg px-3 py-2.5 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
        <p className="text-xs text-slate-500 text-right">
          {values.ai_question_answer.length < 20
            ? `${20 - values.ai_question_answer.length} more characters needed`
            : "✓"}
        </p>
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
          {copy["onboarding.submit"]}
        </button>
      </div>
    </div>
  );
}
