"use client";

import { useState, useEffect, useRef } from "react";
import type { PracticeTask, BuildArtifactConfig } from "@/lib/content/loadPillar";
import type { CoachMessage } from "@/lib/coach/types";
import type { CoachStreamEvent } from "@/lib/coach/types";

interface Props {
  scenario: string;
  tasks: PracticeTask[];
  buildArtifactConfig: BuildArtifactConfig;
  pillarId: string;
  userEmail: string;
  alreadyCompleted: boolean;
  onComplete: (artifact: string, sessionId: string) => void;
}

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  streaming?: boolean;
}

/** Simple ID generator (client-side only). */
let msgCounter = 0;
function nextId() {
  return `msg-${++msgCounter}`;
}

export function PracticeSection({
  scenario,
  tasks,
  buildArtifactConfig,
  pillarId,
  alreadyCompleted,
  onComplete,
}: Props) {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [sessionError, setSessionError] = useState(false);
  const [currentTaskIdx, setCurrentTaskIdx] = useState(0);
  const [taskTurnCounts, setTaskTurnCounts] = useState<Record<string, number>>({});
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [showArtifactEditor, setShowArtifactEditor] = useState(false);
  const [artifactText, setArtifactText] = useState("");
  const [saving, setSaving] = useState(false);
  const [taskCompletedTasks, setTaskCompletedTasks] = useState<Set<string>>(new Set());

  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const currentTask = tasks[currentTaskIdx];
  const allTasksDone = currentTaskIdx >= tasks.length;

  // Start session on mount
  useEffect(() => {
    if (alreadyCompleted) return;
    fetch("/api/coach/session/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pillar_id: pillarId }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.session_id) setSessionId(data.session_id);
        else setSessionError(true);
      })
      .catch(() => setSessionError(true));
  }, [pillarId, alreadyCompleted]);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage() {
    if (!sessionId || !inputValue.trim() || isStreaming || !currentTask) return;

    const userText = inputValue.trim();
    setInputValue("");
    setIsStreaming(true);

    const userMsg: Message = { id: nextId(), role: "user", content: userText };
    setMessages((prev) => [...prev, userMsg]);

    // Build conversation_history (all past messages for Gemini)
    const conversationHistory: CoachMessage[] = messages
      .concat(userMsg)
      .map((m) => ({ role: m.role === "user" ? "user" : "model", content: m.content }));

    // Add placeholder for streaming assistant message
    const assistantMsgId = nextId();
    setMessages((prev) => [
      ...prev,
      { id: assistantMsgId, role: "assistant", content: "", streaming: true },
    ]);

    try {
      const res = await fetch("/api/coach/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          task_id: currentTask.task_id,
          user_message: userText,
          conversation_history: conversationHistory.slice(0, -1), // exclude the just-added user msg
        }),
      });

      if (!res.body) throw new Error("No stream body");

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let accumulatedContent = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const raw = line.slice(6).trim();
          if (!raw || raw === "[DONE]") continue;

          let event: CoachStreamEvent;
          try {
            event = JSON.parse(raw);
          } catch {
            continue;
          }

          if (event.type === "text" && event.content) {
            accumulatedContent += event.content;
            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantMsgId
                  ? { ...m, content: accumulatedContent, streaming: true }
                  : m
              )
            );
          } else if (event.type === "task_complete" && event.taskId) {
            handleTaskComplete(event.taskId);
          }
        }
      }

      // Finalise the streaming message
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMsgId ? { ...m, streaming: false } : m
        )
      );

      // Track turn count client-side for the "Question N of 3" indicator
      setTaskTurnCounts((prev) => ({
        ...prev,
        [currentTask.task_id]: (prev[currentTask.task_id] ?? 0) + 1,
      }));
    } catch {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMsgId
            ? { ...m, content: "Connection error — please try again.", streaming: false }
            : m
        )
      );
    } finally {
      setIsStreaming(false);
    }
  }

  function handleTaskComplete(taskId: string) {
    setTaskCompletedTasks((prev) => new Set([...prev, taskId]));

    setTimeout(() => {
      const nextIdx = tasks.findIndex((t) => t.task_id === taskId) + 1;
      if (nextIdx >= tasks.length) {
        // All tasks done — show artifact editor
        setShowArtifactEditor(true);
        setCurrentTaskIdx(tasks.length);
      } else {
        setCurrentTaskIdx(nextIdx);
        // Add a coach transition message for the next task
        setMessages((prev) => [
          ...prev,
          {
            id: nextId(),
            role: "assistant",
            content: `─── Moving to Task ${nextIdx + 1}: ${tasks[nextIdx].title} ───`,
            streaming: false,
          },
        ]);
      }
    }, 800);
  }

  async function handleFinishPractice() {
    if (!sessionId) return;
    setSaving(true);

    const conversation: CoachMessage[] = messages
      .filter((m) => !m.content.startsWith("───"))
      .map((m) => ({ role: m.role === "user" ? "user" : "model", content: m.content }));

    try {
      await fetch("/api/coach/session/complete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          pillar_id: pillarId,
          conversation,
        }),
      });
    } finally {
      setSaving(false);
    }

    onComplete(artifactText, sessionId ?? "");
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  const currentTurnCount = currentTask ? (taskTurnCounts[currentTask.task_id] ?? 0) : 0;
  const questionsRemaining = Math.max(0, 3 - currentTurnCount);

  if (alreadyCompleted) {
    return (
      <div className="text-center py-16">
        <div className="text-4xl mb-4">✓</div>
        <p className="text-slate-300 text-lg font-medium">Practice complete</p>
        <p className="text-slate-500 text-sm mt-2">Head to the Quiz to test your understanding.</p>
      </div>
    );
  }

  if (sessionError) {
    return (
      <div className="text-center py-16">
        <p className="text-red-400">Could not start coaching session. Please refresh.</p>
      </div>
    );
  }

  if (!sessionId) {
    return (
      <div className="text-center py-16">
        <div className="text-slate-400 animate-pulse">Starting your AI coach…</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Scenario context card — always visible */}
      <div className="rounded-xl border border-amber-500/25 bg-amber-500/8 p-4">
        <p className="text-xs text-amber-400/80 uppercase tracking-widest font-semibold mb-2">
          Your Scenario
        </p>
        <p className="text-slate-200 text-sm leading-relaxed italic">{scenario}</p>
      </div>

      {/* Task stepper */}
      <div className="flex gap-2 flex-wrap">
        {tasks.map((task, idx) => (
          <div
            key={task.task_id}
            className={[
              "flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border transition-colors",
              idx === currentTaskIdx
                ? "bg-blue-600/30 border-blue-500/60 text-blue-300"
                : taskCompletedTasks.has(task.task_id)
                ? "bg-green-950/30 border-green-700/40 text-green-400"
                : "bg-white/5 border-white/10 text-slate-500",
            ].join(" ")}
          >
            {taskCompletedTasks.has(task.task_id) && <span>✓</span>}
            <span>Task {idx + 1}: {task.title}</span>
          </div>
        ))}
      </div>

      {/* Current task: objective + full prompt (the concrete instructions/content) */}
      {currentTask && !allTasksDone && (
        <div className="border border-white/10 rounded-xl overflow-hidden">
          {/* Header row: objective + turn counter */}
          <div className="bg-white/5 px-4 py-3 flex items-start justify-between gap-4">
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">
                Task {currentTaskIdx + 1} of {tasks.length}
              </p>
              <p className="text-slate-200 text-sm font-medium">{currentTask.learning_objective}</p>
            </div>
            <div className="shrink-0 text-right">
              <p className="text-xs text-slate-500">Questions</p>
              <p className="text-blue-400 font-semibold text-sm">
                {currentTurnCount + 1} of 3
              </p>
              {questionsRemaining === 0 && (
                <p className="text-xs text-amber-400 mt-0.5">Last question</p>
              )}
            </div>
          </div>
          {/* Task prompt — the concrete instructions and sample content to work with */}
          <div className="border-t border-white/8 bg-slate-900/40 px-4 py-3">
            <p className="text-xs text-slate-500 uppercase tracking-widest font-semibold mb-2">
              Task Instructions
            </p>
            <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">
              {currentTask.prompt_template}
            </p>
          </div>
        </div>
      )}

      {/* Artifact editor (post-all-tasks) */}
      {showArtifactEditor && (
        <div className="space-y-4 bg-white/5 border border-white/10 rounded-xl p-6">
          <div>
            <h3 className="text-white font-semibold mb-1">
              {buildArtifactConfig.artifact_name}
            </h3>
            <p className="text-slate-400 text-sm">{buildArtifactConfig.artifact_description}</p>
          </div>
          <textarea
            value={artifactText}
            onChange={(e) => setArtifactText(e.target.value)}
            placeholder={buildArtifactConfig.prompt.slice(0, 120) + "…"}
            rows={8}
            className="w-full bg-slate-900/60 border border-white/10 rounded-lg p-4 text-slate-200 text-sm placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500/50 resize-y"
          />
          <button
            type="button"
            onClick={handleFinishPractice}
            disabled={saving}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-60 text-white font-semibold px-8 py-3 rounded-xl transition-colors"
          >
            {saving ? "Saving…" : "Finish Practice → Take Quiz"}
          </button>
        </div>
      )}

      {/* Chat messages */}
      <div className="space-y-3 min-h-[200px]">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={[
              "rounded-xl px-4 py-3 text-sm leading-relaxed max-w-[90%]",
              msg.role === "user"
                ? "ml-auto bg-blue-600/30 border border-blue-500/30 text-blue-100"
                : msg.content.startsWith("───")
                ? "bg-transparent border-none text-slate-500 text-xs text-center max-w-full"
                : "bg-white/5 border border-white/10 text-slate-200",
            ].join(" ")}
          >
            {msg.content}
            {msg.streaming && (
              <span className="inline-block w-1.5 h-4 bg-blue-400 ml-0.5 animate-pulse align-middle" />
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      {!showArtifactEditor && !allTasksDone && (
        <div className="flex gap-2 items-end">
          <textarea
            ref={textareaRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isStreaming}
            placeholder="Your response… (Enter to send, Shift+Enter for new line)"
            rows={3}
            className="flex-1 bg-slate-900/60 border border-white/10 rounded-xl px-4 py-3 text-slate-200 text-sm placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500/50 resize-none disabled:opacity-50"
          />
          <button
            type="button"
            onClick={sendMessage}
            disabled={isStreaming || !inputValue.trim()}
            className="shrink-0 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white font-medium px-5 py-3 rounded-xl transition-colors h-fit"
          >
            {isStreaming ? "…" : "Send"}
          </button>
        </div>
      )}
    </div>
  );
}
