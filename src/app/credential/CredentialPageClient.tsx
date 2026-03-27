"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";

interface Props {
  uid: string;
  displayName: string;
  overallScore: number;
  pillarScores: Record<string, number>;
  issuedDate: string;
  credentialId: string;
  linkedInUrl: string;
  appUrl: string;
}

const PILLAR_LABELS: Record<string, string> = {
  p1: "AI Foundations",
  p2: "Precision Prompting",
  p3: "Tool Fluency",
  p4: "AI Configuration",
  p5: "AI Workflows",
  p6: "Agentic Systems",
};

export function CredentialPageClient({
  uid,
  displayName,
  overallScore,
  pillarScores,
  issuedDate,
  credentialId,
  linkedInUrl,
  appUrl,
}: Props) {
  const [copied, setCopied] = useState(false);

  const badgeUrl = `/api/credential/badge?uid=${uid}`;
  const certUrl = `/api/credential/cert?uid=${uid}`;
  const shareCardUrl = `/api/credential/share-card?uid=${uid}`;
  const sharePageUrl = `${appUrl}/credential`;

  function handleCopyLink() {
    navigator.clipboard.writeText(sharePageUrl).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900">
      <div className="max-w-2xl mx-auto px-4 py-12 space-y-10">
        {/* Hero */}
        <div className="text-center space-y-3">
          <div className="text-5xl">🏆</div>
          <h1 className="text-3xl font-bold text-white">Congratulations, {displayName}!</h1>
          <p className="text-slate-400">You&apos;ve earned the AI&#8209;Supercharged Intermediate credential.</p>
        </div>

        {/* Badge + score */}
        <div className="bg-white/5 border border-white/10 rounded-2xl p-6 flex flex-col sm:flex-row items-center gap-6">
          <Image
            src={badgeUrl}
            alt="AI-Supercharged Intermediate badge"
            width={160}
            height={160}
            className="rounded-xl"
            unoptimized
          />
          <div className="space-y-3 text-center sm:text-left">
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider">Credential</p>
              <p className="text-xl font-bold text-white">AI-Supercharged Intermediate</p>
              <p className="text-xs text-indigo-400 mt-0.5">AI Hero Academy · {issuedDate}</p>
            </div>
            <div className="flex items-center gap-3 justify-center sm:justify-start">
              <div className="bg-emerald-900/30 border border-emerald-600/30 rounded-lg px-4 py-2 text-center">
                <p className="text-xs text-slate-500">Overall Score</p>
                <p className="text-2xl font-bold text-emerald-400">{overallScore.toFixed(1)}<span className="text-sm text-slate-500 ml-0.5">/4.0</span></p>
              </div>
            </div>
          </div>
        </div>

        {/* Pillar breakdown */}
        <section>
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Pillar Scores</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {(["p1", "p2", "p3", "p4", "p5", "p6"] as const).map((p) => {
              const score = pillarScores[p] ?? 0;
              return (
                <div
                  key={p}
                  className={`rounded-xl border p-4 text-center ${score >= 1 ? "bg-indigo-900/20 border-indigo-600/30" : "bg-white/5 border-white/10"}`}
                >
                  <p className="text-xs text-slate-500 mb-1">{PILLAR_LABELS[p]}</p>
                  <p className={`text-xl font-bold ${score >= 1 ? "text-indigo-300" : "text-slate-500"}`}>
                    {score}/2
                  </p>
                </div>
              );
            })}
          </div>
        </section>

        {/* Social share card preview */}
        <section>
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Share Card</h2>
          <div className="rounded-2xl overflow-hidden border border-white/10">
            <Image
              src={shareCardUrl}
              alt="Share card"
              width={1200}
              height={630}
              className="w-full h-auto"
              unoptimized
            />
          </div>
        </section>

        {/* Actions */}
        <section>
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Share &amp; Download</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {/* LinkedIn */}
            <a
              href={linkedInUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-3 bg-[#0a66c2] hover:bg-[#004182] text-white font-semibold py-3 px-5 rounded-xl transition-colors"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
              </svg>
              Add to LinkedIn
            </a>

            {/* Download PDF */}
            <a
              href={certUrl}
              download="ai-hero-academy-certificate.pdf"
              className="flex items-center justify-center gap-3 bg-white/10 hover:bg-white/15 text-white font-semibold py-3 px-5 rounded-xl transition-colors border border-white/10"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download PDF
            </a>

            {/* Copy link */}
            <button
              type="button"
              onClick={handleCopyLink}
              className="flex items-center justify-center gap-3 bg-white/10 hover:bg-white/15 text-white font-semibold py-3 px-5 rounded-xl transition-colors border border-white/10"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              {copied ? "Copied!" : "Copy Link"}
            </button>

            {/* Dashboard */}
            <Link
              href="/dashboard"
              className="flex items-center justify-center gap-3 bg-indigo-600/30 hover:bg-indigo-600/50 text-indigo-200 font-semibold py-3 px-5 rounded-xl transition-colors border border-indigo-500/30"
            >
              ← Back to Dashboard
            </Link>
          </div>
        </section>

        {/* Credential ID */}
        <p className="text-center text-xs text-slate-600">
          Credential ID: {credentialId} · Issued {issuedDate}
        </p>
      </div>
    </main>
  );
}
