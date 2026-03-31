"use client";

import { useState } from "react";
import type { PillarReadingContent } from "@/lib/content/loadPillar";

// ── Types ──────────────────────────────────────────────────────────────────────

interface BriefItem { letter: string; name: string; desc: string }
interface Section { title: string; items: string[] }
interface Parsed {
  intro: string[];
  briefIntro: string[];
  briefItems: BriefItem[];
  sections: Section[];
}

// ── Parser ─────────────────────────────────────────────────────────────────────

function parseConcept(text: string): Parsed {
  const blocks = text.split(/\n\n+/).map((b) => b.trim()).filter(Boolean);
  const out: Parsed = { intro: [], briefIntro: [], briefItems: [], sections: [] };
  let phase: "intro" | "brief" | "adv" = "intro";
  let cur: Section | null = null;

  for (const b of blocks) {
    if (/^\*\*[^*\n]+\*\*$/.test(b)) {
      const title = b.slice(2, -2);
      if (title === "The BRIEF Framework") { phase = "brief"; continue; }
      phase = "adv";
      if (cur) out.sections.push(cur);
      cur = { title, items: [] };
      continue;
    }
    const bm = b.match(/^- \*\*([A-Z]) — ([^*]+)\*\*: ([\s\S]+)/);
    if (bm && phase === "brief") {
      out.briefItems.push({ letter: bm[1], name: bm[2], desc: bm[3] });
      continue;
    }
    if (phase === "intro") out.intro.push(b);
    else if (phase === "brief") out.briefIntro.push(b);
    else if (phase === "adv" && cur) cur.items.push(b);
  }
  if (cur) out.sections.push(cur);
  return out;
}

// ── Inline markdown ────────────────────────────────────────────────────────────

function InlineMd({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return (
    <>
      {parts.map((p, i) =>
        p.startsWith("**") && p.endsWith("**")
          ? <strong key={i} className="font-semibold text-white">{p.slice(2, -2)}</strong>
          : <span key={i}>{p}</span>
      )}
    </>
  );
}

// ── Design tokens ──────────────────────────────────────────────────────────────

const BRIEF_COLORS = {
  B: { pill: "bg-blue-500/15 border-blue-500/40 text-blue-400",   card: "border-blue-500/20 bg-blue-500/5"    },
  R: { pill: "bg-violet-500/15 border-violet-500/40 text-violet-400", card: "border-violet-500/20 bg-violet-500/5" },
  I: { pill: "bg-amber-500/15 border-amber-500/40 text-amber-400",  card: "border-amber-500/20 bg-amber-500/5"  },
  E: { pill: "bg-emerald-500/15 border-emerald-500/40 text-emerald-400", card: "border-emerald-500/20 bg-emerald-500/5" },
  F: { pill: "bg-rose-500/15 border-rose-500/40 text-rose-400",   card: "border-rose-500/20 bg-rose-500/5"   },
} as const;

const BRIEF_SUMMARIES: Record<string, string> = {
  B: "Standing rules for every interaction",
  R: "Persistent persona and expertise",
  I: "Step-by-step task procedures",
  E: "Handling ambiguity and out-of-scope inputs",
  F: "Output structure, length, and tone",
};

const CHAPTERS = [
  { label: "Concept",    accent: "text-sky-400/80"     },
  { label: "Framework",  accent: "text-violet-400/80"  },
  { label: "Deep Dive",  accent: "text-amber-400/80"   },
  { label: "In Practice",accent: "text-emerald-400/80" },
  { label: "Takeaway",   accent: "text-rose-400/80"    },
];

// ── Shared sub-components ──────────────────────────────────────────────────────

function ChapterHeader({ idx, title, subtitle, centered }: {
  idx: number; title: string; subtitle: string; centered?: boolean;
}) {
  return (
    <div className={`mb-7 ${centered ? "text-center" : ""}`}>
      <p className={`text-[10px] uppercase tracking-widest font-semibold mb-1 ${CHAPTERS[idx].accent}`}>
        Chapter {idx + 1} · {CHAPTERS[idx].label}
      </p>
      <h2 className="text-2xl font-bold text-white leading-tight">{title}</h2>
      <p className="text-slate-400 text-sm mt-1">{subtitle}</p>
    </div>
  );
}

function Body({ text, className = "" }: { text: string; className?: string }) {
  return (
    <p className={`text-slate-300 leading-relaxed text-[15px] ${className}`}>
      <InlineMd text={text} />
    </p>
  );
}

function SectionBlock({ section }: { section: Section }) {
  const [open, setOpen] = useState(true);
  return (
    <div className="border border-white/10 rounded-xl overflow-hidden">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between px-4 py-3 bg-white/4 hover:bg-white/6 transition-colors text-left"
      >
        <span className="text-sm font-semibold text-slate-200">{section.title}</span>
        <svg
          className={`w-4 h-4 text-slate-500 transition-transform duration-200 ${open ? "rotate-180" : ""}`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {open && (
        <div className="px-4 py-4 space-y-3 bg-white/2">
          {section.items.map((item, i) => {
            // Definition bullet: - **Label**: content
            const dm = item.match(/^- \*\*([^*]+)\*\*: ([\s\S]+)/);
            if (dm) {
              return (
                <div key={i} className="bg-white/5 rounded-lg px-3 py-2.5 border border-white/8">
                  <p className="text-amber-300/90 font-semibold text-xs mb-1">{dm[1]}</p>
                  <p className="text-slate-300 text-sm leading-relaxed"><InlineMd text={dm[2]} /></p>
                </div>
              );
            }
            return <Body key={i} text={item} />;
          })}
        </div>
      )}
    </div>
  );
}

// ── Page components ────────────────────────────────────────────────────────────

function PageConcept({ intro }: { intro: string[] }) {
  return (
    <div>
      <ChapterHeader idx={0} title="The Concept" subtitle="The foundation — what you need to know before everything else" />
      {/* Visual before/after */}
      <div className="grid grid-cols-2 gap-3 mb-7">
        <div className="bg-slate-800/50 border border-white/8 rounded-xl p-4">
          <p className="text-[10px] text-slate-500 uppercase tracking-wide mb-2">Without configuration</p>
          <div className="space-y-1 mb-3">
            {["Context...", "Role...", "Format..."].map((l) => (
              <div key={l} className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-red-400/60 shrink-0" />
                <span className="text-xs text-slate-500">{l} <em className="text-red-400/60">every message</em></span>
              </div>
            ))}
          </div>
          <p className="text-[10px] text-red-400/70">Repetitive. Inconsistent.</p>
        </div>
        <div className="bg-blue-500/6 border border-blue-500/20 rounded-xl p-4">
          <p className="text-[10px] text-blue-400/70 uppercase tracking-wide mb-2">With a system prompt</p>
          <div className="space-y-1 mb-3">
            {["Configure once", "AI applies always", "Never repeat"].map((l) => (
              <div key={l} className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-green-400 shrink-0" />
                <span className="text-xs text-slate-300">{l}</span>
              </div>
            ))}
          </div>
          <p className="text-[10px] text-blue-400/70">Persistent. Reliable.</p>
        </div>
      </div>
      <div className="space-y-4">
        {intro.map((p, i) => <Body key={i} text={p} />)}
      </div>
    </div>
  );
}

function PageFramework({ briefIntro, briefItems, sections }: {
  briefIntro: string[];
  briefItems: BriefItem[];
  sections: Section[];
}) {
  const [active, setActive] = useState<string>(briefItems[0]?.letter ?? "");
  const hasBrief = briefItems.length > 0;
  const activeItem = briefItems.find((it) => it.letter === active);
  const half = Math.ceil(sections.length / 2);

  return (
    <div>
      <ChapterHeader
        idx={1}
        title={hasBrief ? "The BRIEF Framework" : "Core Concepts"}
        subtitle={hasBrief ? "Five layers that turn a tool into a configured assistant" : "Key ideas in depth"}
      />
      {hasBrief ? (
        <>
          {briefIntro.map((p, i) => <Body key={i} text={p} className="mb-5" />)}
          {/* Letter tabs */}
          <div className="flex gap-1.5 mb-5">
            {briefItems.map(({ letter }) => {
              const c = BRIEF_COLORS[letter as keyof typeof BRIEF_COLORS];
              const isActive = active === letter;
              return (
                <button
                  key={letter}
                  type="button"
                  onClick={() => setActive(letter)}
                  className={[
                    "flex-1 py-3 rounded-xl border font-bold text-xl transition-all duration-200",
                    isActive
                      ? `${c.pill} scale-[1.06] shadow-lg`
                      : "bg-white/3 border-white/10 text-white/30 hover:text-white/60 hover:bg-white/5",
                  ].join(" ")}
                >
                  {letter}
                </button>
              );
            })}
          </div>
          {/* Active card */}
          {activeItem && (() => {
            const c = BRIEF_COLORS[activeItem.letter as keyof typeof BRIEF_COLORS];
            return (
              <div className={`rounded-xl border ${c.card} p-5`} key={activeItem.letter}>
                <div className="flex items-center gap-3 mb-3">
                  <div className={`w-9 h-9 rounded-lg border flex items-center justify-center font-bold text-sm ${c.pill} shrink-0`}>
                    {activeItem.letter}
                  </div>
                  <div>
                    <p className="font-semibold text-white">{activeItem.letter} — {activeItem.name}</p>
                    <p className="text-xs text-slate-500">{BRIEF_SUMMARIES[activeItem.letter]}</p>
                  </div>
                </div>
                <Body text={activeItem.desc} />
              </div>
            );
          })()}
          {/* Mini index */}
          <div className="mt-5 space-y-1.5">
            {briefItems.map(({ letter, name }) => {
              const c = BRIEF_COLORS[letter as keyof typeof BRIEF_COLORS];
              return (
                <button
                  key={letter}
                  type="button"
                  onClick={() => setActive(letter)}
                  className={[
                    "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg border text-left transition-all",
                    active === letter ? `${c.card}` : "border-transparent hover:bg-white/4",
                  ].join(" ")}
                >
                  <span className={`w-5 h-5 rounded flex items-center justify-center text-xs font-bold border ${c.pill} shrink-0`}>{letter}</span>
                  <span className="text-sm text-slate-300">{letter} — {name}</span>
                  <span className="text-[11px] text-slate-600 ml-auto hidden sm:block">{BRIEF_SUMMARIES[letter]}</span>
                </button>
              );
            })}
          </div>
        </>
      ) : (
        <div className="space-y-4">
          {sections.slice(0, half).map((s) => <SectionBlock key={s.title} section={s} />)}
        </div>
      )}
    </div>
  );
}

function PageDeepDive({ briefItems, sections }: { briefItems: BriefItem[]; sections: Section[] }) {
  const hasBrief = briefItems.length > 0;
  const half = Math.ceil(sections.length / 2);
  const displayed = hasBrief ? sections : sections.slice(half);

  return (
    <div>
      <ChapterHeader idx={2} title="Deep Dive" subtitle="Advanced mechanics and configuration techniques" />
      {displayed.length === 0 ? (
        <p className="text-slate-500 text-sm">No additional content for this section.</p>
      ) : (
        <div className="space-y-4">
          {displayed.map((s) => (
            <div key={s.title}>
              {s.title.includes("Temperature") ? (
                <TemperatureSection section={s} />
              ) : (
                <SectionBlock section={s} />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function TemperatureSection({ section }: { section: Section }) {
  const zones = [
    { range: "0", label: "Structured", sub: "JSON, tables, tool calls", color: "bg-sky-400" },
    { range: "0.2–0.3", label: "Analytical", sub: "Research, review, facts", color: "bg-violet-400" },
    { range: "0.7–0.9", label: "Creative", sub: "Brainstorm, write, ideate", color: "bg-rose-400" },
  ];
  return (
    <div className="border border-white/10 rounded-xl overflow-hidden">
      <div className="px-4 py-3 bg-white/4 border-b border-white/8">
        <p className="text-sm font-semibold text-amber-300/90">{section.title}</p>
      </div>
      <div className="p-4 space-y-4">
        {/* Temperature scale */}
        <div>
          <div className="h-2 rounded-full overflow-hidden mb-2 reading-temp-scale" />
          <div className="grid grid-cols-3 gap-2">
            {zones.map(({ range, label, sub, color }) => (
              <div key={label} className="text-center bg-white/4 rounded-lg p-2.5">
                <div className={`w-2 h-2 rounded-full ${color} mx-auto mb-1.5`} />
                <p className="text-white text-xs font-bold tabular-nums">{range}</p>
                <p className="text-slate-200 text-[11px] font-medium mt-0.5">{label}</p>
                <p className="text-slate-500 text-[10px] mt-0.5 leading-snug">{sub}</p>
              </div>
            ))}
          </div>
        </div>
        {section.items.map((item, i) => {
          const dm = item.match(/^- \*\*([^*]+)\*\*: ([\s\S]+)/);
          if (dm) return null; // already visualised above
          return <Body key={i} text={item} />;
        })}
      </div>
    </div>
  );
}

function PageExamples({ good, bad }: { good: string; bad: string }) {
  const [view, setView] = useState<"good" | "bad">("good");
  return (
    <div>
      <ChapterHeader idx={3} title="In Practice" subtitle="The same concept — applied right, and applied wrong" />
      {/* Toggle */}
      <div className="flex rounded-xl border border-white/10 p-1 mb-5 bg-white/3">
        {(["good", "bad"] as const).map((v) => (
          <button
            key={v}
            type="button"
            onClick={() => setView(v)}
            className={[
              "flex-1 flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg text-sm font-medium transition-all",
              view === v
                ? v === "good"
                  ? "bg-emerald-500/20 border border-emerald-500/30 text-emerald-300"
                  : "bg-red-500/20 border border-red-500/30 text-red-300"
                : "text-slate-500 hover:text-slate-300",
            ].join(" ")}
          >
            {v === "good" ? (
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            ) : (
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            )}
            {v === "good" ? "Success Story" : "Anti-Pattern"}
          </button>
        ))}
      </div>

      {view === "good" ? (
        <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-6 h-6 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center shrink-0">
              <svg className="w-3.5 h-3.5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <p className="text-emerald-400 font-semibold text-sm">BRIEF Applied Correctly</p>
          </div>
          <div className="grid grid-cols-2 gap-2 mb-4">
            <div className="bg-emerald-500/10 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold text-white tabular-nums">95%</p>
              <p className="text-[11px] text-emerald-300/70 mt-0.5">ready on first draft</p>
            </div>
            <div className="bg-emerald-500/10 rounded-lg p-3 text-center">
              <p className="text-2xl font-bold text-white tabular-nums">45m</p>
              <p className="text-[11px] text-emerald-300/70 mt-0.5">saved every week</p>
            </div>
          </div>
          <Body text={good} />
        </div>
      ) : (
        <div className="bg-red-500/5 border border-red-500/20 rounded-xl p-5">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-6 h-6 rounded-full bg-red-500/20 border border-red-500/40 flex items-center justify-center shrink-0">
              <svg className="w-3.5 h-3.5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <p className="text-red-400 font-semibold text-sm">The Anti-Pattern</p>
          </div>
          <div className="bg-red-500/10 rounded-lg p-3 mb-4 border border-red-500/15">
            <p className="text-[10px] text-red-300/60 uppercase tracking-wide mb-1.5">The incomplete prompt</p>
            <p className="text-slate-300 text-sm italic">&ldquo;You are a helpful professional assistant. Be accurate and concise.&rdquo;</p>
          </div>
          <Body text={bad} />
        </div>
      )}
    </div>
  );
}

function PageTakeaway({ takeaway, done, marking, onMark }: {
  takeaway: string; done: boolean; marking: boolean; onMark: () => void;
}) {
  return (
    <div className="text-center">
      <ChapterHeader idx={4} title="Your Key Takeaway" subtitle="Carry this principle into every session" centered />
      {/* BRIEF strip */}
      <div className="flex justify-center gap-2 mb-7">
        {(["B", "R", "I", "E", "F"] as const).map((l) => {
          const c = BRIEF_COLORS[l];
          return (
            <div key={l} className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-lg border ${c.pill}`}>
              {l}
            </div>
          );
        })}
      </div>
      <div className="bg-white/4 border border-white/10 rounded-2xl p-7 mb-8 text-left">
        <p className="text-white text-base leading-relaxed font-medium">
          <InlineMd text={takeaway} />
        </p>
      </div>
      {done ? (
        <div className="flex flex-col items-center gap-2">
          <div className="w-12 h-12 rounded-full bg-green-500/20 border border-green-500/40 flex items-center justify-center mb-1">
            <svg className="w-6 h-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <p className="text-green-400 font-semibold">Reading complete</p>
          <p className="text-slate-500 text-sm">Practice is now unlocked</p>
        </div>
      ) : (
        <button
          type="button"
          onClick={onMark}
          disabled={marking}
          className="reading-cta-btn inline-flex items-center gap-3 px-8 py-4 rounded-xl font-semibold text-white transition-all disabled:opacity-60 shadow-lg shadow-blue-500/20"
        >
          {marking ? (
            <>
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Saving…
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Mark as Read — Unlock Practice
            </>
          )}
        </button>
      )}
    </div>
  );
}

// ── Main component ─────────────────────────────────────────────────────────────

interface Props {
  reading: PillarReadingContent;
  pillarId: string;
  alreadyRead: boolean;
  onComplete: () => void;
}

export function ReadingSection({ reading, pillarId, alreadyRead, onComplete }: Props) {
  const [page, setPage] = useState(0);
  const [dir, setDir] = useState(1);
  const [fading, setFading] = useState(false);
  const [marking, setMarking] = useState(false);
  const [done, setDone] = useState(alreadyRead);

  const parsed = parseConcept(reading.concept_text);

  function navigate(to: number) {
    if (to === page || fading || to < 0 || to >= CHAPTERS.length) return;
    setDir(to > page ? 1 : -1);
    setFading(true);
    setTimeout(() => { setPage(to); setFading(false); }, 180);
  }

  async function markRead() {
    setMarking(true);
    try {
      await fetch("/api/training/reading-complete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pillar_id: pillarId }),
      });
      setDone(true);
      onComplete();
    } finally {
      setMarking(false);
    }
  }

  const pct = ((page + 1) / CHAPTERS.length) * 100;

  return (
    <div className="max-w-2xl mx-auto pb-10">
      {/* Progress bar */}
      <div className="h-px rounded-full overflow-hidden mb-5 bg-white/8">
        <div
          className="reading-progress-fill h-full rounded-full transition-[width] duration-500 ease-out"
          style={{ width: `${pct}%` }}
        />
      </div>

      {/* Chapter stepper */}
      <nav className="flex gap-1 mb-8" aria-label="Reading chapters">
        {CHAPTERS.map(({ label }, i) => {
          const isActive = i === page;
          const isDone = i < page;
          return (
            <button
              key={i}
              type="button"
              onClick={() => navigate(i)}
              className={[
                "flex-1 flex flex-col items-center gap-1.5 py-2.5 rounded-lg border transition-all duration-200",
                isActive ? "bg-white/8 border-white/15" : isDone ? "bg-green-500/6 border-green-500/20 hover:bg-green-500/10" : "border-transparent hover:bg-white/4",
              ].join(" ")}
            >
              <div className="flex items-center justify-center">
                {isDone ? (
                  <svg className="w-3 h-3 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <div className={`w-1.5 h-1.5 rounded-full ${isActive ? "bg-blue-400 scale-125" : "bg-white/15"}`} />
                )}
              </div>
              <span className={`text-[10px] font-medium leading-none ${isActive ? "text-white" : isDone ? "text-green-400" : "text-slate-600"}`}>
                {label}
              </span>
            </button>
          );
        })}
      </nav>

      {/* Page content */}
      <div
        className={[
          "transition-[opacity,transform] duration-[180ms] ease",
          fading ? "opacity-0" : "opacity-100",
          fading ? (dir > 0 ? "translate-x-3" : "-translate-x-3") : "translate-x-0",
        ].join(" ")}
      >
        {page === 0 && <PageConcept intro={parsed.intro} />}
        {page === 1 && <PageFramework briefIntro={parsed.briefIntro} briefItems={parsed.briefItems} sections={parsed.sections} />}
        {page === 2 && <PageDeepDive briefItems={parsed.briefItems} sections={parsed.sections} />}
        {page === 3 && <PageExamples good={reading.good_example} bad={reading.anti_pattern} />}
        {page === 4 && <PageTakeaway takeaway={reading.takeaway} done={done} marking={marking} onMark={markRead} />}
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between mt-10 pt-5 border-t border-white/8">
        <button
          type="button"
          onClick={() => navigate(page - 1)}
          disabled={page === 0}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm text-slate-500 hover:text-slate-200 disabled:opacity-20 disabled:cursor-not-allowed transition-colors rounded-lg"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Previous
        </button>
        <span className="text-xs text-slate-600 tabular-nums">{page + 1} / {CHAPTERS.length}</span>
        {page < CHAPTERS.length - 1 ? (
          <button
            type="button"
            onClick={() => navigate(page + 1)}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold rounded-lg transition-colors"
          >
            Next
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        ) : (
          <div className="w-24" />
        )}
      </div>
    </div>
  );
}
