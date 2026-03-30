"use client";

import { useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";

const PERSONAS = [
  {
    id: "onboarding",
    label: "New User",
    day: "Pre-Day 1",
    description: "Just signed up. Walks through the 4-screen onboarding and diagnostic.",
    icon: "👋",
    color: "border-slate-500/50 bg-slate-800/40 hover:border-slate-400/70",
    badge: "text-slate-300",
  },
  {
    id: "day1",
    label: "Day 1 — Reading",
    day: "Day 1",
    description: "Program just started. Reading tab open, Practice locked, streak at 1.",
    icon: "📖",
    color: "border-blue-500/50 bg-blue-900/20 hover:border-blue-400/70",
    badge: "text-blue-300",
  },
  {
    id: "day3",
    label: "Mid-Program",
    day: "Day 3 Complete",
    description: "Days 1–3 done. Dashboard shows progress arc, badges earned, artifacts saved.",
    icon: "⚡",
    color: "border-amber-500/50 bg-amber-900/20 hover:border-amber-400/70",
    badge: "text-amber-300",
  },
  {
    id: "day6",
    label: "Pre-Capstone",
    day: "Day 6 Complete",
    description: "Days 1–6 done. Capstone challenge available. Full dashboard with all badges.",
    icon: "🎯",
    color: "border-purple-500/50 bg-purple-900/20 hover:border-purple-400/70",
    badge: "text-purple-300",
  },
  {
    id: "credential",
    label: "Graduate",
    day: "Program Complete",
    description: "All 7 days and capstone done. Credential page with shareable badge and PDF.",
    icon: "🏆",
    color: "border-emerald-500/50 bg-emerald-900/20 hover:border-emerald-400/70",
    badge: "text-emerald-300",
  },
] as const;

function DemoContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("t") ?? "";
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  if (!token) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 flex items-center justify-center px-4">
        <div className="text-center space-y-3">
          <div className="text-4xl">🔒</div>
          <p className="text-slate-400">Demo link required. Please use the link provided.</p>
        </div>
      </div>
    );
  }

  async function handlePersona(personaId: string) {
    setLoading(personaId);
    setError(null);
    try {
      const res = await fetch("/api/auth/demo-login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ persona: personaId, token }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error ?? "Something went wrong");
        return;
      }
      router.push(data.redirect);
    } catch {
      setError("Connection error — please try again");
    } finally {
      setLoading(null);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 px-4 py-12">
      <div className="max-w-2xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <p className="text-xs font-semibold text-blue-400 uppercase tracking-widest">Private Beta</p>
          <h1 className="text-3xl font-bold text-white">AI Hero Academy</h1>
          <p className="text-slate-400 text-sm">
            Choose a persona to explore the learner journey at any stage.
          </p>
        </div>

        {error && (
          <div className="bg-red-950/40 border border-red-700/40 rounded-xl px-4 py-3 text-red-300 text-sm text-center">
            {error}
          </div>
        )}

        {/* Persona cards */}
        <div className="space-y-3">
          {PERSONAS.map((p) => (
            <button
              key={p.id}
              type="button"
              onClick={() => handlePersona(p.id)}
              disabled={loading !== null}
              className={[
                "w-full text-left rounded-2xl border px-5 py-4 transition-all duration-150",
                "disabled:opacity-50 disabled:cursor-not-allowed",
                p.color,
              ].join(" ")}
            >
              <div className="flex items-center gap-4">
                <span className="text-2xl flex-none">{p.icon}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-0.5">
                    <span className="text-white font-semibold text-sm">{p.label}</span>
                    <span className={`text-xs font-medium ${p.badge}`}>{p.day}</span>
                  </div>
                  <p className="text-slate-400 text-xs leading-relaxed">{p.description}</p>
                </div>
                {loading === p.id ? (
                  <span className="text-slate-400 animate-pulse text-sm flex-none">Loading…</span>
                ) : (
                  <span className="text-slate-600 text-sm flex-none">→</span>
                )}
              </div>
            </button>
          ))}
        </div>

        <p className="text-center text-xs text-slate-600">
          Demo sessions expire after 2 hours · Data is reset on each selection
        </p>
      </div>
    </div>
  );
}

export default function DemoPage() {
  return (
    <Suspense>
      <DemoContent />
    </Suspense>
  );
}
