"use client";

import { useState } from "react";
import type { PillarReadingContent } from "@/lib/content/loadPillar";

interface Props {
  reading: PillarReadingContent;
  pillarId: string;
  alreadyRead: boolean;
  onComplete: () => void;
}

/** Renders **text** as bold spans (simple inline markdown). */
function InlineMarkdown({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return (
    <>
      {parts.map((part, i) =>
        part.startsWith("**") && part.endsWith("**") ? (
          <strong key={i} className="font-semibold text-white">
            {part.slice(2, -2)}
          </strong>
        ) : (
          <span key={i}>{part}</span>
        )
      )}
    </>
  );
}

function Paragraph({ text }: { text: string }) {
  return (
    <p className="text-slate-300 leading-relaxed text-[15px]">
      <InlineMarkdown text={text} />
    </p>
  );
}

function ConceptText({ text }: { text: string }) {
  const paragraphs = text.split(/\n\n+/);
  return (
    <div className="space-y-4">
      {paragraphs.map((p, i) => (
        <Paragraph key={i} text={p.trim()} />
      ))}
    </div>
  );
}

export function ReadingSection({ reading, pillarId, alreadyRead, onComplete }: Props) {
  const [marking, setMarking] = useState(false);
  const [done, setDone] = useState(alreadyRead);

  async function handleMarkRead() {
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

  return (
    <div className="space-y-10 pb-8 max-w-[72ch]">
      {/* Core concept */}
      <section>
        <ConceptText text={reading.concept_text} />
      </section>

      {/* Good example */}
      <section>
        <h2 className="text-sm font-semibold text-green-400 mb-3 flex items-center gap-2">
          <span aria-hidden="true">✅</span> Good Example
        </h2>
        <div className="bg-green-950/30 border border-green-800/40 rounded-xl p-5">
          <Paragraph text={reading.good_example} />
        </div>
      </section>

      {/* Anti-pattern */}
      <section>
        <h2 className="text-sm font-semibold text-red-400 mb-3 flex items-center gap-2">
          <span aria-hidden="true">❌</span> Anti-Pattern
        </h2>
        <div className="bg-red-950/30 border border-red-800/40 rounded-xl p-5">
          <Paragraph text={reading.anti_pattern} />
        </div>
      </section>

      {/* Takeaway */}
      <section className="bg-blue-950/40 border border-blue-700/30 rounded-xl p-6">
        <h2 className="text-sm font-semibold text-blue-400 mb-2 flex items-center gap-2">
          <span aria-hidden="true">💡</span> Key Takeaway
        </h2>
        <p className="text-white font-medium text-[15px] leading-relaxed">
          <InlineMarkdown text={reading.takeaway} />
        </p>
      </section>

      {/* Mark as read CTA */}
      <div className="pt-2">
        {done ? (
          <div className="flex items-center gap-2 text-green-400">
            <span className="text-lg">✓</span>
            <span className="text-sm font-medium">Reading complete — Practice is unlocked</span>
          </div>
        ) : (
          <button
            onClick={handleMarkRead}
            disabled={marking}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-60 disabled:cursor-wait text-white font-semibold px-8 py-3 rounded-xl transition-colors"
          >
            {marking ? "Saving…" : "Mark as Read → Unlock Practice"}
          </button>
        )}
      </div>
    </div>
  );
}
