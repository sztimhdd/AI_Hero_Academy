"use client";

import { useState } from "react";
import type { PillarContent } from "@/lib/content/loadPillar";
import type { SerializedProgress } from "./page";
import { ReadingSection } from "./ReadingSection";
import { PracticeSection } from "./PracticeSection";
import { QuizSection } from "./QuizSection";
import { BuildSection } from "./BuildSection";

type Tab = "reading" | "practice" | "quiz" | "build";

interface Props {
  pillarContent: PillarContent;
  initialProgress: SerializedProgress;
  pillarId: string;
  uid: string;
  userEmail: string;
  displayName: string;
}

function deriveInitialTab(p: SerializedProgress): Tab {
  if (p.quiz_passed) return "build";
  if (p.practice_completed_at) return "quiz";
  if (p.reading_completed_at) return "practice";
  return "reading";
}

export function DayPageClient({
  pillarContent,
  initialProgress,
  pillarId,
  userEmail,
}: Props) {
  const [progress, setProgress] = useState(initialProgress);
  const [activeTab, setActiveTab] = useState<Tab>(deriveInitialTab(initialProgress));
  const [practiceArtifact, setPracticeArtifact] = useState("");

  const tabs: { id: Tab; label: string; locked: boolean }[] = [
    { id: "reading", label: "Reading", locked: false },
    {
      id: "practice",
      label: "Practice",
      locked: !progress.reading_completed_at,
    },
    {
      id: "quiz",
      label: "Quiz",
      locked: !progress.practice_completed_at,
    },
    {
      id: "build",
      label: "Build",
      locked: !progress.quiz_passed,
    },
  ];

  function handleReadingComplete() {
    setProgress((p) => ({ ...p, reading_completed_at: new Date().toISOString() }));
    setActiveTab("practice");
  }

  function handlePracticeComplete(artifact: string) {
    setProgress((p) => ({ ...p, practice_completed_at: new Date().toISOString() }));
    setPracticeArtifact(artifact);
    setActiveTab("quiz");
  }

  function handleQuizPass() {
    setProgress((p) => ({ ...p, quiz_passed: true, quiz_completed_at: new Date().toISOString() }));
    setActiveTab("build");
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900">
      {/* Header */}
      <header className="border-b border-white/10 px-4 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-widest">
              Day {pillarContent.day_number}
            </p>
            <h1 className="text-white font-semibold text-lg leading-tight">
              {pillarContent.pillar_name}
            </h1>
          </div>
          <a href="/dashboard" className="text-slate-500 hover:text-slate-300 text-sm transition-colors">
            ← Dashboard
          </a>
        </div>
      </header>

      {/* Tab nav */}
      <nav className="border-b border-white/10 px-4">
        <div className="max-w-4xl mx-auto flex gap-0">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => !tab.locked && setActiveTab(tab.id)}
              disabled={tab.locked}
              className={[
                "relative px-5 py-3 text-sm font-medium transition-colors border-b-2 -mb-px",
                activeTab === tab.id
                  ? "text-blue-400 border-blue-400"
                  : tab.locked
                  ? "text-slate-600 border-transparent cursor-not-allowed"
                  : "text-slate-400 hover:text-slate-200 border-transparent",
              ].join(" ")}
            >
              {tab.label}
              {tab.locked && (
                <span className="ml-1.5 text-xs">🔒</span>
              )}
              {tab.id === "reading" && progress.reading_completed_at && (
                <span className="ml-1.5 text-green-400 text-xs">✓</span>
              )}
              {tab.id === "practice" && progress.practice_completed_at && (
                <span className="ml-1.5 text-green-400 text-xs">✓</span>
              )}
              {tab.id === "quiz" && progress.quiz_passed && (
                <span className="ml-1.5 text-green-400 text-xs">✓</span>
              )}
            </button>
          ))}
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        {activeTab === "reading" && (
          <ReadingSection
            reading={pillarContent.reading}
            pillarId={pillarId}
            alreadyRead={!!progress.reading_completed_at}
            onComplete={handleReadingComplete}
          />
        )}
        {activeTab === "practice" && (
          <PracticeSection
            tasks={pillarContent.practice.tasks}
            buildArtifactConfig={pillarContent.build_artifact}
            pillarId={pillarId}
            userEmail={userEmail}
            alreadyCompleted={!!progress.practice_completed_at}
            onComplete={handlePracticeComplete}
          />
        )}
        {activeTab === "quiz" && (
          <QuizSection
            quiz={pillarContent.quiz}
            pillarId={pillarId}
            alreadyPassed={progress.quiz_passed}
            onPass={handleQuizPass}
          />
        )}
        {activeTab === "build" && (
          <BuildSection
            pillarId={pillarId}
            artifactConfig={pillarContent.build_artifact}
            initialArtifact={practiceArtifact}
          />
        )}
      </main>
    </div>
  );
}
