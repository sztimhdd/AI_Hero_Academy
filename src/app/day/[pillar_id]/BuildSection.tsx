"use client";

import { useState } from "react";
import type { BuildArtifactConfig } from "@/lib/content/loadPillar";

interface Props {
  pillarId: string;
  artifactConfig: BuildArtifactConfig;
  initialArtifact: string;
}

export function BuildSection({ pillarId, artifactConfig, initialArtifact }: Props) {
  const [content, setContent] = useState(initialArtifact);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  async function handleSave() {
    if (!content.trim()) return;
    setSaving(true);
    setSaved(false);
    try {
      await fetch("/api/build/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          pillar_id: pillarId,
          artifact_content: content,
        }),
      });
      setSaved(true);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-6 pb-8">
      <div>
        <h2 className="text-white text-lg font-semibold mb-1">
          {artifactConfig.artifact_name}
        </h2>
        <p className="text-slate-400 text-sm leading-relaxed">
          {artifactConfig.artifact_description}
        </p>
      </div>

      <div className="bg-blue-950/20 border border-blue-700/20 rounded-xl p-5">
        <p className="text-blue-300 text-sm font-medium mb-3">Your prompt</p>
        <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">
          {artifactConfig.prompt
            .replace(/{declared_role}/g, "your role")
            .replace(/{declared_industry}/g, "your industry")}
        </p>
      </div>

      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Write your artifact here…"
        rows={12}
        className="w-full bg-slate-900/60 border border-white/10 rounded-xl px-4 py-4 text-slate-200 text-sm placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500/50 resize-y"
      />

      <div className="flex items-center gap-4">
        <button
          onClick={handleSave}
          disabled={saving || !content.trim()}
          className="bg-green-600 hover:bg-green-500 disabled:opacity-50 text-white font-semibold px-8 py-3 rounded-xl transition-colors"
        >
          {saving ? "Saving…" : "Save to My Toolkit"}
        </button>
        {saved && (
          <span className="text-green-400 text-sm flex items-center gap-1.5">
            <span>✓</span>
            Saved to your AI Toolkit
          </span>
        )}
      </div>
    </div>
  );
}
