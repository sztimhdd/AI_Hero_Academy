"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";

const TYPE_ICONS: Record<string, string> = {
  checklist: "✅",
  prompt_template: "💬",
  system_prompt: "⚙️",
  workflow_doc: "🔄",
  agent_design: "🤖",
};

export interface ArtifactSummary {
  pillar_id: string;
  day_number: number;
  artifact_type: string;
  artifact_title: string;
  artifact_content: string;
  created_at: string;
}

function ArtifactModal({
  artifact,
  onClose,
}: {
  artifact: ArtifactSummary;
  onClose: () => void;
}) {
  const t = useTranslations("common");
  const [copied, setCopied] = useState(false);

  function handleCopy() {
    navigator.clipboard.writeText(artifact.artifact_content).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="w-full max-w-2xl max-h-[80vh] flex flex-col rounded-2xl bg-slate-900 border border-white/10 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between px-5 py-4 border-b border-white/10">
          <div>
            <p className="text-xs text-slate-400">
              {TYPE_ICONS[artifact.artifact_type] ?? "📄"}{" "}
              {artifact.artifact_type.replace(/_/g, " ")} · Day {artifact.day_number}
            </p>
            <h3 className="text-white font-semibold mt-0.5">{artifact.artifact_title}</h3>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleCopy}
              className="text-xs px-3 py-1.5 rounded-lg bg-blue-600/30 hover:bg-blue-600/50 text-blue-300 transition-colors"
            >
              {copied ? t("copied") : t("copy")}
            </button>
            <button
              type="button"
              onClick={onClose}
              className="text-slate-400 hover:text-white p-1"
              aria-label={t("close")}
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <div className="overflow-y-auto p-5">
          <pre className="text-sm text-slate-300 whitespace-pre-wrap font-mono leading-relaxed">
            {artifact.artifact_content}
          </pre>
        </div>
      </div>
    </div>
  );
}

export function ArtifactGallery({ artifacts }: { artifacts: ArtifactSummary[] }) {
  const t = useTranslations("dashboard");
  const [selected, setSelected] = useState<ArtifactSummary | null>(null);

  if (artifacts.length === 0) {
    return (
      <section>
        <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">
          {t("artifactsTitle")}
        </h2>
        <div className="rounded-2xl bg-white/5 border border-white/10 px-5 py-8 text-center">
          <p className="text-slate-500 text-sm">{t("artifactsEmpty")}</p>
        </div>
      </section>
    );
  }

  return (
    <section>
      <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">
        {t("artifactsCount", { count: artifacts.length })}
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {artifacts.map((a) => (
          <button
            key={a.pillar_id}
            type="button"
            onClick={() => setSelected(a)}
            className="text-left rounded-2xl bg-white/5 border border-white/10 hover:border-blue-500/40 hover:bg-white/8 transition-colors p-4 group"
          >
            <div className="flex items-start gap-3">
              <span className="text-2xl">{TYPE_ICONS[a.artifact_type] ?? "📄"}</span>
              <div className="min-w-0">
                <p className="text-xs text-slate-500 mb-0.5">
                  Day {a.day_number} · {a.artifact_type.replace(/_/g, " ")}
                </p>
                <p className="text-sm font-medium text-white truncate">{a.artifact_title}</p>
              </div>
            </div>
            <p className="mt-2 text-xs text-slate-500 group-hover:text-slate-400 text-right">
              {t("artifactViewPrompt")}
            </p>
          </button>
        ))}
      </div>
      {selected && (
        <ArtifactModal artifact={selected} onClose={() => setSelected(null)} />
      )}
    </section>
  );
}
