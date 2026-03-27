"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { en } from "@/lib/i18n/en";
import { zh } from "@/lib/i18n/zh";
import { PillarScores } from "@/lib/firestore/types";
import Screen1 from "./screens/Screen1";
import Screen2 from "./screens/Screen2";
import Screen3 from "./screens/Screen3";
import Screen4 from "./screens/Screen4";

type Lang = "en" | "zh";
type T = typeof en;

const STORAGE_KEY = "onboarding_state";
const TOTAL_SCREENS = 4;

interface OnboardingState {
  screen: number;
  lang: Lang;
  declared_role: string;
  declared_industry: string;
  daily_work_desc: string;
  current_ai_usage: string;
  primary_motivation: string;
  mcq_answers: Record<string, string>;
  ai_question_text: string;
  ai_question_answer: string;
  pillar_scores: PillarScores | null;
  overall_score: number;
}

const INITIAL_STATE: OnboardingState = {
  screen: 1,
  lang: "en",
  declared_role: "",
  declared_industry: "",
  daily_work_desc: "",
  current_ai_usage: "",
  primary_motivation: "",
  mcq_answers: {},
  ai_question_text: "",
  ai_question_answer: "",
  pillar_scores: null,
  overall_score: 0,
};

function loadState(): OnboardingState {
  if (typeof window === "undefined") return INITIAL_STATE;
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    return raw ? { ...INITIAL_STATE, ...JSON.parse(raw) } : INITIAL_STATE;
  } catch {
    return INITIAL_STATE;
  }
}

function saveState(state: OnboardingState) {
  if (typeof window === "undefined") return;
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

export default function OnboardingPage() {
  const [state, setState] = useState<OnboardingState>(INITIAL_STATE);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Rehydrate from sessionStorage on mount (partial-save resume)
  useEffect(() => {
    setState(loadState());
  }, []);

  const copy: T = state.lang === "en" ? en : (zh as unknown as T);

  function update(field: string, value: unknown) {
    setState((prev) => {
      const next = { ...prev, [field]: value };
      saveState(next);
      return next;
    });
  }

  function goTo(screen: number) {
    setState((prev) => {
      const next = { ...prev, screen };
      saveState(next);
      return next;
    });
  }

  // Screen 3 → Screen 4: POST to /api/diagnostic/score
  async function handleDiagnosticSubmit() {
    setSubmitting(true);
    setError(null);
    try {
      const res = await fetch("/api/diagnostic/score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          declared_role: state.declared_role,
          declared_industry: state.declared_industry,
          daily_work_desc: state.daily_work_desc,
          current_ai_usage: state.current_ai_usage,
          primary_motivation: state.primary_motivation,
          mcq_answers: state.mcq_answers,
          ai_question_text: state.ai_question_text,
          ai_question_answer: state.ai_question_answer,
        }),
      });

      if (!res.ok) throw new Error("Scoring failed");

      const data = await res.json();
      setState((prev) => {
        const next = {
          ...prev,
          screen: 4,
          pillar_scores: data.pillar_scores,
          overall_score: data.overall_score,
        };
        saveState(next);
        return next;
      });
    } catch {
      setError(copy["common.error"]);
    } finally {
      setSubmitting(false);
    }
  }

  // Screen 4 CTA → go to dashboard
  function handleStart() {
    sessionStorage.removeItem(STORAGE_KEY);
    router.push("/dashboard");
  }

  const progressPct = ((state.screen - 1) / (TOTAL_SCREENS - 1)) * 100;

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 flex flex-col items-center justify-start px-4 py-8">
      {/* Lang toggle */}
      <div className="w-full max-w-lg flex justify-between items-center mb-6">
        <span className="text-slate-400 text-sm">
          {copy["onboarding.step"]
            .replace("{current}", String(state.screen))
            .replace("{total}", String(TOTAL_SCREENS))}
        </span>
        <button
          type="button"
          onClick={() => update("lang", state.lang === "en" ? "zh" : "en")}
          className="text-sm text-slate-400 hover:text-white transition-colors"
        >
          {copy["landing.lang_toggle"]}
        </button>
      </div>

      {/* Progress bar */}
      <div className="w-full max-w-lg mb-8">
        <div className="h-1 bg-white/10 rounded-full overflow-hidden">
          <div
            className="h-full bg-blue-500 rounded-full transition-all duration-500"
            style={{ width: `${progressPct}%` }}
          />
        </div>
      </div>

      <div className="w-full max-w-lg">
        {error && (
          <div className="mb-4 px-4 py-3 bg-red-500/20 border border-red-500/40 rounded-xl text-red-300 text-sm">
            {error}
          </div>
        )}

        {state.screen === 1 && (
          <Screen1
            copy={copy}
            values={{
              declared_role: state.declared_role,
              declared_industry: state.declared_industry,
              daily_work_desc: state.daily_work_desc,
            }}
            onChange={update}
            onNext={() => goTo(2)}
          />
        )}

        {state.screen === 2 && (
          <Screen2
            copy={copy}
            values={{
              current_ai_usage: state.current_ai_usage,
              primary_motivation: state.primary_motivation,
            }}
            onChange={update}
            onNext={() => goTo(3)}
            onBack={() => goTo(1)}
          />
        )}

        {state.screen === 3 && (
          <Screen3
            copy={copy}
            profile={{
              declared_role: state.declared_role,
              declared_industry: state.declared_industry,
              daily_work_desc: state.daily_work_desc,
            }}
            values={{
              mcq_answers: state.mcq_answers,
              ai_question_text: state.ai_question_text,
              ai_question_answer: state.ai_question_answer,
            }}
            onChange={update}
            onNext={handleDiagnosticSubmit}
            onBack={() => goTo(2)}
          />
        )}

        {state.screen === 4 && state.pillar_scores && (
          <Screen4
            copy={copy}
            pillarScores={state.pillar_scores}
            onStart={handleStart}
            loading={submitting}
          />
        )}
      </div>
    </main>
  );
}
