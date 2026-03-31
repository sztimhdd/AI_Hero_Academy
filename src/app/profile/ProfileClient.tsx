"use client";

import Link from "next/link";
import { useTranslations } from "next-intl";

export interface DiagnosticSummary {
  pillar_scores: Record<string, number>; // p1–p6, values 0–100
  overall_score: number;
  completed_at: string; // ISO string
}

export interface UserProfileSummary {
  display_name: string;
  declared_role?: string;
  declared_industry?: string;
  streak_days: number;
}

interface Props {
  user: UserProfileSummary;
  diagnostic: DiagnosticSummary | null;
  diagnosticHistory: DiagnosticSummary[];
}

// ── Radar chart ────────────────────────────────────────────────────────────────

const PILLAR_ORDER = ["p1", "p2", "p3", "p4", "p5", "p6"] as const;

function radarPoint(angle: number, r: number, cx: number, cy: number) {
  const x = cx + r * Math.cos(angle - Math.PI / 2);
  const y = cy + r * Math.sin(angle - Math.PI / 2);
  return { x, y };
}

function RadarChart({
  scores,
  labels,
}: {
  scores: Record<string, number>;
  labels: Record<string, string>;
}) {
  const size = 260;
  const cx = size / 2;
  const cy = size / 2;
  const maxR = 90;
  const n = PILLAR_ORDER.length;
  const angleStep = (2 * Math.PI) / n;

  // Grid rings at 25%, 50%, 75%, 100%
  const rings = [0.25, 0.5, 0.75, 1];

  // Score polygon points
  const scorePoints = PILLAR_ORDER.map((id, i) => {
    const raw = scores[id] ?? 0;
    const r = (Math.min(raw, 100) / 100) * maxR;
    const { x, y } = radarPoint(angleStep * i, r, cx, cy);
    return `${x},${y}`;
  }).join(" ");

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="w-full max-w-xs mx-auto" role="img" aria-label="Radar chart">
      {/* Grid rings */}
      {rings.map((ratio) => {
        const pts = PILLAR_ORDER.map((_, i) => {
          const { x, y } = radarPoint(angleStep * i, maxR * ratio, cx, cy);
          return `${x},${y}`;
        }).join(" ");
        return (
          <polygon
            key={ratio}
            points={pts}
            fill="none"
            stroke="#334155"
            strokeWidth="1"
          />
        );
      })}

      {/* Axes */}
      {PILLAR_ORDER.map((_, i) => {
        const { x, y } = radarPoint(angleStep * i, maxR, cx, cy);
        return <line key={i} x1={cx} y1={cy} x2={x} y2={y} stroke="#334155" strokeWidth="1" />;
      })}

      {/* Score polygon */}
      <polygon
        points={scorePoints}
        fill="#14b8a633"
        stroke="#14b8a6"
        strokeWidth="2"
        strokeLinejoin="round"
      />

      {/* Score dots */}
      {PILLAR_ORDER.map((id, i) => {
        const raw = scores[id] ?? 0;
        const r = (Math.min(raw, 100) / 100) * maxR;
        const { x, y } = radarPoint(angleStep * i, r, cx, cy);
        return <circle key={id} cx={x} cy={y} r={4} fill="#14b8a6" />;
      })}

      {/* Axis labels */}
      {PILLAR_ORDER.map((id, i) => {
        const labelR = maxR + 18;
        const { x, y } = radarPoint(angleStep * i, labelR, cx, cy);
        const anchor =
          Math.abs(x - cx) < 5 ? "middle" : x < cx ? "end" : "start";
        return (
          <text
            key={id}
            x={x}
            y={y + 4}
            textAnchor={anchor}
            fontSize="10"
            fill="#94a3b8"
            fontFamily="system-ui, sans-serif"
          >
            {labels[id]}
          </text>
        );
      })}
    </svg>
  );
}

// ── Gap map helpers ─────────────────────────────────────────────────────────

function gapTier(score: number): "critical" | "needs_work" | "on_track" {
  if (score < 40) return "critical";
  if (score < 70) return "needs_work";
  return "on_track";
}

const TIER_STYLES = {
  critical: "bg-red-500/10 text-red-400 border-red-500/30",
  needs_work: "bg-amber-500/10 text-amber-400 border-amber-500/30",
  on_track: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
};

// ── Level label ─────────────────────────────────────────────────────────────

function scoreToLevel(overall: number): string {
  if (overall >= 3.5) return "Expert";
  if (overall >= 2.5) return "Advanced";
  if (overall >= 1.5) return "Practitioner";
  return "Beginner";
}

// ── Main component ───────────────────────────────────────────────────────────

export function ProfileClient({ user, diagnostic, diagnosticHistory }: Props) {
  const t = useTranslations("profile");
  const dt = useTranslations("dashboard");

  const radarLabels = PILLAR_ORDER.reduce<Record<string, string>>((acc, id) => {
    acc[id] = t(`radarLabel.${id}`);
    return acc;
  }, {});

  const pillarNames = PILLAR_ORDER.reduce<Record<string, string>>((acc, id) => {
    acc[id] = dt(`pillar.${id}`);
    return acc;
  }, {});

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900">
      <div className="max-w-2xl mx-auto px-4 py-8 space-y-8">

        {/* Back link */}
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-1 text-sm text-slate-400 hover:text-white transition-colors"
        >
          {t("backToDashboard")}
        </Link>

        {/* Header */}
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white">{t("title")}</h1>
          {(user.declared_role || user.declared_industry) && (
            <p className="text-slate-400 text-sm mt-1">
              {user.declared_role && <span>{t("role")}: {user.declared_role}</span>}
              {user.declared_role && user.declared_industry && <span className="mx-2 text-slate-600">·</span>}
              {user.declared_industry && <span>{t("industry")}: {user.declared_industry}</span>}
            </p>
          )}
          {diagnostic && (
            <p className="text-slate-500 text-xs mt-1">
              {t("lastAssessed")}: {new Date(diagnostic.completed_at).toLocaleDateString()}
            </p>
          )}
        </div>

        {!diagnostic ? (
          <p className="text-slate-400 text-sm rounded-2xl bg-white/5 border border-white/10 px-5 py-6">
            {t("noDiagnostic")}
          </p>
        ) : (
          <>
            {/* Overall score card */}
            <div className="rounded-2xl bg-white/5 border border-white/10 px-6 py-5 flex items-center gap-4">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">
                  {t("overallScoreTitle")}
                </p>
                <p className="text-3xl font-bold text-white">
                  {scoreToLevel(diagnostic.overall_score)}
                </p>
                <p className="text-slate-400 text-sm mt-0.5">
                  {diagnostic.overall_score.toFixed(1)} / 4.0
                </p>
              </div>
            </div>

            {/* Radar chart */}
            <section className="rounded-2xl bg-white/5 border border-white/10 px-6 py-6">
              <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
                {t("radarTitle")}
              </h2>
              <RadarChart scores={diagnostic.pillar_scores} labels={radarLabels} />
            </section>

            {/* Gap map */}
            <section>
              <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">
                {t("gapMapTitle")}
              </h2>
              {/* Legend */}
              <div className="flex gap-4 mb-3 text-xs text-slate-400">
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-red-500 inline-block" />
                  {t("gapCritical")}
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block" />
                  {t("gapNeedsWork")}
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block" />
                  {t("gapOnTrack")}
                </span>
              </div>
              <div className="rounded-2xl bg-white/5 border border-white/10 px-4 py-4 space-y-2">
                {PILLAR_ORDER.map((id) => {
                  const score = diagnostic.pillar_scores[id] ?? 0;
                  const tier = gapTier(score);
                  const tierLabel = t(
                    tier === "critical"
                      ? "gapCritical"
                      : tier === "needs_work"
                      ? "gapNeedsWork"
                      : "gapOnTrack"
                  );
                  return (
                    <div key={id} className="flex items-center justify-between gap-3">
                      <span className="text-sm text-slate-300">{pillarNames[id]}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-24 h-1.5 rounded-full bg-slate-700">
                          <div
                            className="h-full rounded-full bg-teal-500"
                            style={{ width: `${Math.min(score, 100)}%` }}
                          />
                        </div>
                        <span
                          className={`text-xs px-2 py-0.5 rounded-full border ${TIER_STYLES[tier]}`}
                        >
                          {tierLabel}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </section>

            {/* Assessment history */}
            {diagnosticHistory.length > 0 && (
              <section>
                <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">
                  {t("historyTitle")}
                </h2>
                <div className="rounded-2xl bg-white/5 border border-white/10 divide-y divide-white/5">
                  {diagnosticHistory.map((d, i) => (
                    <div key={i} className="flex items-center justify-between px-4 py-3">
                      <span className="text-sm text-slate-300">
                        {new Date(d.completed_at).toLocaleDateString()}
                      </span>
                      <span className="text-sm text-white font-medium">
                        {d.overall_score.toFixed(1)} / 4.0
                        <span className="text-slate-500 text-xs ml-1">
                          ({scoreToLevel(d.overall_score)})
                        </span>
                      </span>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </>
        )}
      </div>
    </main>
  );
}
