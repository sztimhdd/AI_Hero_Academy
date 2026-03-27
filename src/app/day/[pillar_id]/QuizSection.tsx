"use client";

import { useState } from "react";
import type { PillarQuiz, QuizItem } from "@/lib/content/loadPillar";

interface Props {
  quiz: PillarQuiz;
  pillarId: string;
  alreadyPassed: boolean;
  onPass: () => void;
}

interface QuizResult {
  pass: boolean;
  score: number;
  max_score: number;
  fail_guidance?: string;
  hints?: Array<{ item_id: string; hint: string }>;
  next_pillar_id?: string;
}

function McqItem({
  item,
  selected,
  onSelect,
  hint,
  disabled,
}: {
  item: QuizItem;
  selected: string;
  onSelect: (v: string) => void;
  hint?: string;
  disabled: boolean;
}) {
  return (
    <div className="space-y-3">
      <p className="text-slate-200 text-[15px] font-medium">{item.question}</p>
      <div className="space-y-2">
        {Object.entries(item.options ?? {}).map(([key, text]) => (
          <button
            key={key}
            onClick={() => !disabled && onSelect(key)}
            disabled={disabled}
            className={[
              "w-full text-left rounded-xl border px-4 py-3 text-sm transition-colors",
              selected === key
                ? "bg-blue-600/30 border-blue-500/60 text-blue-100"
                : "bg-white/5 border-white/10 text-slate-300 hover:bg-white/10 hover:border-white/20",
              disabled ? "cursor-default" : "cursor-pointer",
            ].join(" ")}
          >
            <span className="font-semibold mr-2">{key}.</span>
            {text}
          </button>
        ))}
      </div>
      {hint && (
        <div className="bg-amber-950/30 border border-amber-700/30 rounded-lg px-4 py-3 text-amber-300 text-sm">
          💡 {hint}
        </div>
      )}
    </div>
  );
}

function OpenItem({
  item,
  value,
  onChange,
  disabled,
}: {
  item: QuizItem;
  value: string;
  onChange: (v: string) => void;
  disabled: boolean;
}) {
  return (
    <div className="space-y-3">
      <p className="text-slate-200 text-[15px] font-medium">{item.question}</p>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="Write your response here (2–3 sentences)…"
        rows={4}
        className="w-full bg-slate-900/60 border border-white/10 rounded-xl px-4 py-3 text-slate-200 text-sm placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500/50 resize-y disabled:opacity-50"
      />
    </div>
  );
}

export function QuizSection({ quiz, pillarId, alreadyPassed, onPass }: Props) {
  const [mcqAnswers, setMcqAnswers] = useState<Record<string, string>>({});
  const [openAnswer, setOpenAnswer] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<QuizResult | null>(null);

  // If already passed, show the success screen
  if (alreadyPassed) {
    return (
      <div className="text-center py-16 space-y-4">
        <div className="text-5xl">🏅</div>
        <h2 className="text-white text-xl font-semibold">Quiz Passed!</h2>
        <p className="text-slate-400">You've unlocked the Build section. Create your artifact below.</p>
        <button
          onClick={onPass}
          className="bg-green-600 hover:bg-green-500 text-white font-semibold px-8 py-3 rounded-xl transition-colors"
        >
          Go to Build →
        </button>
      </div>
    );
  }

  // Show result screen after submission
  if (result) {
    if (result.pass) {
      return (
        <div className="text-center py-12 space-y-6">
          <div className="text-5xl">🏅</div>
          <div>
            <h2 className="text-white text-2xl font-bold mb-2">Day Badge Earned!</h2>
            <p className="text-slate-400">
              Score: {result.score} / {result.max_score}
            </p>
          </div>
          <button
            onClick={onPass}
            className="bg-green-600 hover:bg-green-500 text-white font-semibold px-8 py-3 rounded-xl transition-colors"
          >
            Continue to Build →
          </button>
        </div>
      );
    }

    // Failed — show hints and retry
    return (
      <div className="space-y-8">
        <div className="bg-amber-950/30 border border-amber-700/30 rounded-xl p-5">
          <p className="text-amber-300 font-semibold mb-1">
            Score: {result.score} / {result.max_score} — not quite there yet
          </p>
          {result.fail_guidance && (
            <p className="text-amber-200/80 text-sm mt-2">{result.fail_guidance}</p>
          )}
        </div>

        {/* Re-render quiz items with hints */}
        <div className="space-y-8">
          {quiz.items.map((item, i) => {
            const hint = result.hints?.find((h) => h.item_id === item.item_id)?.hint;
            return (
              <div key={item.item_id} className="space-y-3">
                <p className="text-xs text-slate-500 uppercase tracking-wide">
                  Question {i + 1} of {quiz.items.length}
                </p>
                {item.type === "mcq" ? (
                  <McqItem
                    item={item}
                    selected={mcqAnswers[item.item_id] ?? ""}
                    onSelect={(v) =>
                      setMcqAnswers((prev) => ({ ...prev, [item.item_id]: v }))
                    }
                    hint={hint}
                    disabled={false}
                  />
                ) : (
                  <OpenItem
                    item={item}
                    value={openAnswer}
                    onChange={setOpenAnswer}
                    disabled={false}
                  />
                )}
              </div>
            );
          })}
        </div>

        <button
          onClick={() => setResult(null)}
          className="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-8 py-3 rounded-xl transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  async function handleSubmit() {
    const mcqItems = quiz.items.filter((i) => i.type === "mcq");
    const openItem = quiz.items.find((i) => i.type === "open_rubric");

    // Require all MCQ answers
    for (const item of mcqItems) {
      if (!mcqAnswers[item.item_id]) return;
    }
    // Require open answer if there's an open question
    if (openItem && !openAnswer.trim()) return;

    setSubmitting(true);
    try {
      const res = await fetch("/api/quiz/score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          pillar_id: pillarId,
          mcq_answers: mcqAnswers,
          open_answer: openAnswer,
        }),
      });
      const data: QuizResult = await res.json();
      setResult(data);
    } finally {
      setSubmitting(false);
    }
  }

  const mcqItems = quiz.items.filter((i) => i.type === "mcq");
  const allMcqAnswered = mcqItems.every((i) => mcqAnswers[i.item_id]);
  const openItem = quiz.items.find((i) => i.type === "open_rubric");
  const canSubmit = allMcqAnswered && (!openItem || openAnswer.trim().length > 0);

  return (
    <div className="space-y-10">
      <div>
        <h2 className="text-white text-lg font-semibold mb-1">Day Quiz</h2>
        <p className="text-slate-400 text-sm">
          {quiz.items.length} questions · Pass score: {quiz.pass_threshold} / {quiz.max_score}
        </p>
      </div>

      {quiz.items.map((item, i) => (
        <div key={item.item_id} className="space-y-3">
          <p className="text-xs text-slate-500 uppercase tracking-wide">
            Question {i + 1} of {quiz.items.length}
          </p>
          {item.type === "mcq" ? (
            <McqItem
              item={item}
              selected={mcqAnswers[item.item_id] ?? ""}
              onSelect={(v) =>
                setMcqAnswers((prev) => ({ ...prev, [item.item_id]: v }))
              }
              hint={undefined}
              disabled={submitting}
            />
          ) : (
            <OpenItem
              item={item}
              value={openAnswer}
              onChange={setOpenAnswer}
              disabled={submitting}
            />
          )}
        </div>
      ))}

      <button
        onClick={handleSubmit}
        disabled={!canSubmit || submitting}
        className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold px-8 py-3 rounded-xl transition-colors"
      >
        {submitting ? "Scoring…" : "Submit Quiz"}
      </button>
    </div>
  );
}
