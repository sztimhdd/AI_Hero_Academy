"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import type { CapstoneContent, CapstoneMcqItem } from "@/lib/content/loadCapstone";
import { fillSectionPrompt } from "@/lib/content/capstoneUtils";
import type { CoachMessage, CoachStreamEvent } from "@/lib/coach/types";

// ── Types ─────────────────────────────────────────────────────────────────────

type Screen = "intro" | "challenge" | "results";
type TaskState = "pending" | "active" | "done";

interface PillarScores {
  p1: number; p2: number; p3: number; p4: number; p5: number; p6: number;
}

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  streaming?: boolean;
}

let msgCounter = 0;
function nextId() { return `cm-${++msgCounter}`; }

// ── Sub-components ────────────────────────────────────────────────────────────

function TaskBadge({ n, total, state }: { n: number; total: number; state: TaskState }) {
  return (
    <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
      state === "active" ? "bg-blue-600/30 border-blue-500/60 text-blue-300" :
      state === "done"   ? "bg-emerald-900/30 border-emerald-700/40 text-emerald-400" :
                           "bg-white/5 border-white/10 text-slate-500"
    }`}>
      {state === "done" && <span>✓</span>}
      <span>Task {n}/{total}</span>
    </div>
  );
}

// Reusable streaming coach (for tasks 1 + 2)
function CoachTask({
  sectionTitle,
  promptText,
  taskId,
  sessionId,
  onDone,
}: {
  sectionTitle: string;
  promptText: string;
  taskId: string;
  sessionId: string;
  onDone: (conversation: CoachMessage[]) => void;
}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [turnCount, setTurnCount] = useState(0);
  const [done, setDone] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage() {
    if (!input.trim() || isStreaming || done) return;
    const userText = input.trim();
    setInput("");
    setIsStreaming(true);

    const userMsg: Message = { id: nextId(), role: "user", content: userText };
    setMessages(prev => [...prev, userMsg]);

    const history: CoachMessage[] = messages
      .concat(userMsg)
      .map(m => ({ role: m.role === "user" ? "user" : "model", content: m.content }));

    const assistantId = nextId();
    setMessages(prev => [...prev, { id: assistantId, role: "assistant", content: "", streaming: true }]);

    try {
      const res = await fetch("/api/coach/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          task_id: taskId,
          user_message: userText,
          conversation_history: history.slice(0, -1),
        }),
      });

      if (!res.body) throw new Error("no body");
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let accumulated = "";

      while (true) {
        const { done: d, value } = await reader.read();
        if (d) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const raw = line.slice(6).trim();
          if (!raw || raw === "[DONE]") continue;
          let event: CoachStreamEvent;
          try { event = JSON.parse(raw); } catch { continue; }

          if (event.type === "text" && event.content) {
            accumulated += event.content;
            setMessages(prev => prev.map(m =>
              m.id === assistantId ? { ...m, content: accumulated, streaming: true } : m
            ));
          } else if (event.type === "task_complete") {
            markDone();
          }
        }
      }
      setMessages(prev => prev.map(m =>
        m.id === assistantId ? { ...m, streaming: false } : m
      ));
      const newCount = turnCount + 1;
      setTurnCount(newCount);
      if (newCount >= 3) markDone();
    } catch {
      setMessages(prev => prev.map(m =>
        m.id === assistantId ? { ...m, content: "Connection error. Please try again.", streaming: false } : m
      ));
    } finally {
      setIsStreaming(false);
    }
  }

  function markDone() {
    setDone(true);
    setMessages(prev => {
      const conv: CoachMessage[] = prev
        .filter(m => !m.content.startsWith("───"))
        .map(m => ({ role: m.role === "user" ? "user" : "model", content: m.content }));
      onDone(conv);
      return prev;
    });
  }

  function handleKey(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  }

  return (
    <div className="space-y-4">
      <div className="bg-blue-950/40 border border-blue-500/20 rounded-xl p-4">
        <p className="text-xs text-blue-400 font-semibold uppercase tracking-wider mb-2">{sectionTitle}</p>
        <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">{promptText}</p>
      </div>

      <div className="space-y-3 min-h-[160px]">
        {messages.map(msg => (
          <div key={msg.id} className={`rounded-xl px-4 py-3 text-sm leading-relaxed max-w-[92%] ${
            msg.role === "user"
              ? "ml-auto bg-blue-600/30 border border-blue-500/30 text-blue-100"
              : "bg-white/5 border border-white/10 text-slate-200"
          }`}>
            {msg.content}
            {msg.streaming && <span className="inline-block w-1.5 h-4 bg-blue-400 ml-0.5 animate-pulse align-middle" />}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {done ? (
        <div className="text-center py-3 text-emerald-400 text-sm font-medium">
          ✓ Section complete — your coach has recorded your response.
        </div>
      ) : (
        <div className="flex gap-2 items-end">
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKey}
            disabled={isStreaming}
            placeholder="Your response… (Enter to send, Shift+Enter for new line)"
            rows={3}
            className="flex-1 bg-slate-900/60 border border-white/10 rounded-xl px-4 py-3 text-slate-200 text-sm placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500/50 resize-none disabled:opacity-50"
          />
          <button
            onClick={sendMessage}
            disabled={isStreaming || !input.trim()}
            className="shrink-0 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white font-medium px-5 py-3 rounded-xl transition-colors h-fit"
          >
            {isStreaming ? "…" : "Send"}
          </button>
        </div>
      )}
    </div>
  );
}

// MCQ cluster (task 3)
function McqCluster({
  items,
  onDone,
}: {
  items: CapstoneMcqItem[];
  onDone: (answers: Record<string, string>, score: number) => void;
}) {
  const [selections, setSelections] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState<Record<string, boolean>>({});

  function submit() {
    const r: Record<string, boolean> = {};
    let correct = 0;
    for (const item of items) {
      const isCorrect = selections[item.item_id] === item.correct_answer;
      r[item.item_id] = isCorrect;
      if (isCorrect) correct++;
    }
    setResults(r);
    setSubmitted(true);
    // Score: correct count / items.length * 2 (maps to 0-2 scale for pillar scoring)
    const score = (correct / items.length) * 2;
    onDone(selections, Math.round(score * 10) / 10);
  }

  return (
    <div className="space-y-6">
      <div className="bg-amber-950/30 border border-amber-500/20 rounded-xl p-4">
        <p className="text-xs text-amber-400 font-semibold uppercase tracking-wider mb-1">Applied Judgment: MCQ Cluster</p>
        <p className="text-slate-400 text-sm">Select the best answer for each scenario. No coach — this is assessment mode.</p>
      </div>

      {items.map((item, idx) => (
        <div key={item.item_id} className="space-y-3">
          <p className="text-slate-200 text-sm font-medium">
            <span className="text-slate-500 mr-2">{idx + 1}.</span>
            {item.question}
          </p>
          <div className="space-y-2">
            {Object.entries(item.options).map(([key, text]) => {
              const selected = selections[item.item_id] === key;
              const correct = submitted && item.correct_answer === key;
              const wrong = submitted && selected && !correct;
              return (
                <button
                  key={key}
                  disabled={submitted}
                  onClick={() => setSelections(prev => ({ ...prev, [item.item_id]: key }))}
                  className={`w-full text-left text-sm px-4 py-3 rounded-xl border transition-colors ${
                    correct   ? "bg-emerald-600/20 border-emerald-500/50 text-emerald-200" :
                    wrong     ? "bg-red-600/20 border-red-500/50 text-red-200" :
                    selected  ? "bg-blue-600/30 border-blue-500/60 text-blue-100" :
                                "bg-white/5 border-white/10 text-slate-300 hover:border-white/20"
                  }`}
                >
                  <span className="font-semibold mr-2">{key}.</span>{text}
                </button>
              );
            })}
          </div>
        </div>
      ))}

      {!submitted ? (
        <button
          onClick={submit}
          disabled={Object.keys(selections).length < items.length}
          className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white font-semibold transition-colors"
        >
          Submit Answers ({Object.keys(selections).length}/{items.length} answered)
        </button>
      ) : (
        <div className="text-center text-emerald-400 text-sm font-medium py-2">
          ✓ Answers recorded — {Object.values(results).filter(Boolean).length}/{items.length} correct.
        </div>
      )}
    </div>
  );
}

// Open design task (task 4)
function OpenDesignTask({
  promptText,
  onDone,
}: {
  promptText: string;
  onDone: (text: string, imageBase64: string | null, mimeType: string | null) => void;
}) {
  const [text, setText] = useState("");
  const [imageBase64, setImageBase64] = useState<string | null>(null);
  const [mimeType, setMimeType] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    const reader = new FileReader();
    reader.onload = () => {
      const dataUrl = reader.result as string;
      // Strip data URL prefix: "data:<mime>;base64,<data>"
      const base64 = dataUrl.split(",")[1];
      setImageBase64(base64);
      setMimeType(file.type);
      setUploading(false);
    };
    reader.readAsDataURL(file);
  }

  function submit() {
    onDone(text, imageBase64, mimeType);
    setSubmitted(true);
  }

  return (
    <div className="space-y-4">
      <div className="bg-purple-950/30 border border-purple-500/20 rounded-xl p-4">
        <p className="text-xs text-purple-400 font-semibold uppercase tracking-wider mb-2">Design Challenge</p>
        <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">{promptText}</p>
      </div>

      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        disabled={submitted}
        placeholder="Paste your design documentation here, or describe your workflow/agent system…"
        rows={8}
        className="w-full bg-slate-900/60 border border-white/10 rounded-xl px-4 py-3 text-slate-200 text-sm placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-purple-500/50 resize-y disabled:opacity-60"
      />

      <div>
        <label htmlFor="cap-upload" className="block text-xs text-slate-500 mb-2">
          Optionally upload a diagram or screenshot of your AI output (PNG, JPG, PDF)
        </label>
        <input
          id="cap-upload"
          type="file"
          accept="image/*,.pdf"
          onChange={handleFile}
          disabled={submitted || uploading}
          className="block text-sm text-slate-400 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:bg-white/10 file:text-slate-300 hover:file:bg-white/15"
        />
        {imageBase64 && (
          <p className="text-emerald-400 text-xs mt-1">✓ File ready for submission</p>
        )}
        {uploading && <p className="text-slate-500 text-xs mt-1">Loading…</p>}
      </div>

      {!submitted ? (
        <button
          onClick={submit}
          disabled={!text.trim()}
          className="w-full py-3 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-40 text-white font-semibold transition-colors"
        >
          Submit Design
        </button>
      ) : (
        <div className="text-center text-emerald-400 text-sm font-medium py-2">
          ✓ Design submitted — scoring in progress…
        </div>
      )}
    </div>
  );
}

// ── Main CapstonePageClient ───────────────────────────────────────────────────

interface Props {
  uid: string;
  userEmail: string;
  displayName: string;
  declaredRole: string;
  declaredIndustry: string;
  scenario: string;
  capstone: CapstoneContent;
  alreadyPassed: boolean;
}

export function CapstonePageClient({
  uid,
  userEmail,
  displayName,
  declaredRole,
  declaredIndustry,
  scenario,
  capstone,
  alreadyPassed,
}: Props) {
  const router = useRouter();
  const [screen, setScreen] = useState<Screen>(alreadyPassed ? "results" : "intro");
  const [activeTask, setActiveTask] = useState(0);
  const [taskStates, setTaskStates] = useState<TaskState[]>(["pending", "pending", "pending", "pending"]);

  // Collected task data
  const [task1Conv, setTask1Conv] = useState<CoachMessage[]>([]);
  const [task2Conv, setTask2Conv] = useState<CoachMessage[]>([]);
  const [mcqAnswers, setMcqAnswers] = useState<Record<string, string>>({});
  const [mcqScore, setMcqScore] = useState(0);
  const [task4Text, setTask4Text] = useState("");
  const [task4ImageBase64, setTask4ImageBase64] = useState<string | null>(null);
  const [task4MimeType, setTask4MimeType] = useState<string | null>(null);

  // Session
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [sessionError, setSessionError] = useState(false);

  // Results
  const [submitting, setSubmitting] = useState(false);
  const [passed, setPassed] = useState(alreadyPassed);
  const [overallScore, setOverallScore] = useState<number | null>(null);
  const [pillarScores, setPillarScores] = useState<PillarScores | null>(null);
  const [failFeedback, setFailFeedback] = useState<string | null>(null);

  const sections = capstone.sections;
  const task1Section = sections[0]!;
  const task2Section = sections[1]!;
  const task3Section = sections[2]!;
  const task4Section = sections[3]!;

  // Start capstone coach session when entering challenge
  useEffect(() => {
    if (screen !== "challenge" || sessionId || sessionError) return;
    fetch("/api/capstone/session/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ uid, userEmail, declaredRole, declaredIndustry }),
    })
      .then(r => r.json())
      .then(d => {
        if (d.session_id) setSessionId(d.session_id);
        else setSessionError(true);
      })
      .catch(() => setSessionError(true));
  }, [screen, sessionId, sessionError, uid, userEmail, declaredRole, declaredIndustry]);

  function markTask(idx: number, state: TaskState) {
    setTaskStates(prev => prev.map((s, i) => i === idx ? state : s));
  }

  function advanceTask(completedIdx: number) {
    markTask(completedIdx, "done");
    const next = completedIdx + 1;
    if (next < 4) {
      setActiveTask(next);
      markTask(next, "active");
    }
  }

  function handleTask1Done(conv: CoachMessage[]) {
    setTask1Conv(conv);
    advanceTask(0);
  }

  function handleTask2Done(conv: CoachMessage[]) {
    setTask2Conv(conv);
    advanceTask(1);
  }

  function handleMcqDone(answers: Record<string, string>, score: number) {
    setMcqAnswers(answers);
    setMcqScore(score);
    advanceTask(2);
  }

  function handleTask4Done(text: string, imgBase64: string | null, mime: string | null) {
    setTask4Text(text);
    setTask4ImageBase64(imgBase64);
    setTask4MimeType(mime);
    markTask(3, "done");
  }

  async function submitCapstone() {
    setSubmitting(true);
    try {
      const body = {
        session_id: sessionId,
        task1_conversation: task1Conv,
        task2_conversation: task2Conv,
        task3_answers: mcqAnswers,
        task3_score: mcqScore,
        task4_text: task4Text,
        task4_image_base64: task4ImageBase64,
        task4_mime_type: task4MimeType,
        declared_role: declaredRole,
        declared_industry: declaredIndustry,
      };
      const res = await fetch("/api/capstone/score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      setPillarScores(data.pillar_scores);
      setOverallScore(data.overall_score);
      setPassed(data.passed);
      setFailFeedback(data.feedback ?? null);
      setScreen("results");

      if (data.passed) {
        // Issue credential
        await fetch("/api/credential/issue", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            pillar_scores: data.pillar_scores,
            overall_score: data.overall_score,
            display_name: displayName,
          }),
        });
        // Redirect to credential page after 2s
        setTimeout(() => router.push("/credential"), 2200);
      }
    } finally {
      setSubmitting(false);
    }
  }

  const allTasksDone = taskStates.every(s => s === "done");

  // ── Intro screen ─────────────────────────────────────────────────────────────
  if (screen === "intro") {
    return (
      <main className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 flex flex-col items-center justify-center px-4 py-12">
        <div className="w-full max-w-2xl space-y-8">
          <div className="text-center space-y-3">
            <div className="text-5xl">🏆</div>
            <h1 className="text-3xl font-bold text-white">{capstone.title}</h1>
            <p className="text-slate-400 text-sm">Day 7 · ~{capstone.estimated_minutes} minutes</p>
          </div>

          <div className="bg-indigo-950/60 border border-indigo-500/20 rounded-2xl p-6">
            <p className="text-xs text-indigo-400 font-semibold uppercase tracking-wider mb-3">Your Scenario</p>
            <p className="text-slate-200 text-sm leading-relaxed">{scenario}</p>
          </div>

          <div className="space-y-3">
            <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">4 Tasks</p>
            {sections.map((s, i) => (
              <div key={s.section_id} className="flex items-start gap-4 bg-white/5 border border-white/10 rounded-xl px-4 py-3">
                <span className="text-slate-500 text-sm font-mono w-6 flex-none">{i + 1}</span>
                <div className="min-w-0">
                  <p className="text-sm font-medium text-white">{s.title}</p>
                  <p className="text-xs text-slate-500 mt-0.5">
                    {s.type === "text_input" ? "AI coach · " : s.type === "mcq_cluster" ? "Assessment · " : "Design + optional upload · "}
                    ~{s.estimated_minutes} min · Pillars: {s.pillars_tested.join(", ").toUpperCase()}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <div className="bg-amber-950/30 border border-amber-500/20 rounded-xl px-4 py-3">
            <p className="text-amber-300 text-sm">
              💡 You are explicitly encouraged to use your own AI tools during this challenge — it tests judgment about <em>when and how</em> to use AI, not recall under pressure.
            </p>
          </div>

          <button
            onClick={() => { setScreen("challenge"); markTask(0, "active"); }}
            className="w-full py-4 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-lg transition-colors shadow-lg shadow-indigo-900/40"
          >
            Begin Challenge →
          </button>
        </div>
      </main>
    );
  }

  // ── Challenge screen ──────────────────────────────────────────────────────────
  if (screen === "challenge") {
    if (sessionError) {
      return (
        <main className="min-h-screen bg-slate-900 flex items-center justify-center">
          <p className="text-red-400">Could not start coaching session. Please refresh.</p>
        </main>
      );
    }
    if (!sessionId) {
      return (
        <main className="min-h-screen bg-slate-900 flex items-center justify-center">
          <p className="text-slate-400 animate-pulse">Starting AI coach…</p>
        </main>
      );
    }

    return (
      <main className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900">
        <div className="max-w-2xl mx-auto px-4 py-8 space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-bold text-white">{capstone.title}</h1>
            <div className="flex gap-2">
              {taskStates.map((state, i) => (
                <TaskBadge key={i} n={i + 1} total={4} state={state} />
              ))}
            </div>
          </div>

          {/* Active task */}
          {activeTask === 0 && taskStates[0] !== "done" && (
            <CoachTask
              sectionTitle={task1Section.title}
              promptText={fillSectionPrompt(task1Section.prompt_template ?? "", declaredRole, declaredIndustry)}
              taskId={task1Section.section_id}
              sessionId={sessionId}
              onDone={handleTask1Done}
            />
          )}

          {(activeTask === 1 || (taskStates[0] === "done" && activeTask >= 1)) && taskStates[1] !== "done" && (
            <CoachTask
              sectionTitle={task2Section.title}
              promptText={fillSectionPrompt(task2Section.prompt_template ?? "", declaredRole, declaredIndustry)}
              taskId={task2Section.section_id}
              sessionId={sessionId}
              onDone={handleTask2Done}
            />
          )}

          {(activeTask === 2 || (taskStates[1] === "done" && activeTask >= 2)) && taskStates[2] !== "done" && (
            <McqCluster
              items={(task3Section.items ?? []) as CapstoneMcqItem[]}
              onDone={handleMcqDone}
            />
          )}

          {(activeTask === 3 || (taskStates[2] === "done" && activeTask >= 3)) && taskStates[3] !== "done" && (
            <OpenDesignTask
              promptText={fillSectionPrompt(task4Section.prompt_template ?? "", declaredRole, declaredIndustry)}
              onDone={handleTask4Done}
            />
          )}

          {/* Submit */}
          {allTasksDone && (
            <div className="bg-indigo-950/50 border border-indigo-500/30 rounded-2xl p-6 text-center space-y-4">
              <p className="text-white font-semibold text-lg">All tasks complete! 🎉</p>
              <p className="text-slate-400 text-sm">Submit your work for AI scoring and credential review.</p>
              <button
                onClick={submitCapstone}
                disabled={submitting}
                className="w-full py-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-60 text-white font-bold text-lg transition-colors"
              >
                {submitting ? "Scoring your work…" : "Submit & Get Results →"}
              </button>
            </div>
          )}
        </div>
      </main>
    );
  }

  // ── Results screen ────────────────────────────────────────────────────────────
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 flex flex-col items-center justify-center px-4 py-12">
      <div className="w-full max-w-2xl space-y-8">
        {passed ? (
          <>
            <div className="text-center space-y-4">
              <div className="text-6xl animate-bounce">🏆</div>
              <h1 className="text-3xl font-bold text-white">You passed!</h1>
              {overallScore !== null && (
                <p className="text-indigo-300 text-lg font-semibold">
                  Score: {overallScore.toFixed(1)} / 4.0
                </p>
              )}
              <p className="text-slate-400 text-sm max-w-md mx-auto">
                You&apos;ve demonstrated real AI skills across all 6 pillars. Your credential is being generated — you&apos;ll be redirected shortly.
              </p>
            </div>

            {pillarScores && (
              <div className="grid grid-cols-3 gap-3">
                {(Object.entries(pillarScores) as [string, number][]).map(([k, v]) => (
                  <div key={k} className="bg-emerald-900/20 border border-emerald-600/30 rounded-xl p-3 text-center">
                    <p className="text-xs text-slate-400 uppercase">{k}</p>
                    <p className="text-emerald-400 font-bold text-lg">{v}/2</p>
                  </div>
                ))}
              </div>
            )}

            <div className="text-center">
              <button
                onClick={() => router.push("/credential")}
                className="px-8 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition-colors"
              >
                View Credential →
              </button>
            </div>
          </>
        ) : (
          <>
            <div className="text-center space-y-4">
              <div className="text-5xl">📊</div>
              <h1 className="text-2xl font-bold text-white">Not quite there yet</h1>
              {overallScore !== null && (
                <p className="text-slate-400">
                  Score: <span className="text-white font-semibold">{overallScore.toFixed(1)}</span> / 4.0 (pass threshold: 2.5)
                </p>
              )}
            </div>

            {failFeedback && (
              <div className="bg-white/5 border border-white/10 rounded-xl p-5">
                <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">{failFeedback}</p>
              </div>
            )}

            {pillarScores && (
              <div className="grid grid-cols-3 gap-3">
                {(Object.entries(pillarScores) as [string, number][]).map(([k, v]) => (
                  <div key={k} className={`border rounded-xl p-3 text-center ${v >= 1 ? "bg-emerald-900/20 border-emerald-600/30" : "bg-red-900/20 border-red-600/30"}`}>
                    <p className="text-xs text-slate-400 uppercase">{k}</p>
                    <p className={`font-bold text-lg ${v >= 1 ? "text-emerald-400" : "text-red-400"}`}>{v}/2</p>
                  </div>
                ))}
              </div>
            )}

            <div className="text-center">
              <button
                onClick={() => { setScreen("intro"); setActiveTask(0); setTaskStates(["pending", "pending", "pending", "pending"]); setSessionId(null); }}
                className="px-8 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold transition-colors"
              >
                Retake Challenge
              </button>
            </div>
          </>
        )}
      </div>
    </main>
  );
}
