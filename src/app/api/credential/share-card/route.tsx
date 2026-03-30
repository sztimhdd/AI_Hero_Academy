/**
 * GET /api/credential/share-card?uid=xxx
 * Generates a 1200×630 social share card PNG using Next.js ImageResponse.
 */
import { ImageResponse } from "next/og";
import { NextRequest } from "next/server";
import { getCredential } from "@/lib/firestore/db";

export const runtime = "nodejs";

export async function GET(req: NextRequest) {
  const uid = req.nextUrl.searchParams.get("uid");
  if (!uid) return new Response("uid required", { status: 400 });

  let credential;
  try {
    credential = await getCredential(uid);
  } catch (err) {
    console.error("share-card: Firestore error", err);
    return new Response("Firestore error", { status: 500 });
  }
  if (!credential) return new Response("Credential not found", { status: 404 });

  const issuedDate = credential.issued_at.toDate().toLocaleDateString("en-US", {
    year: "numeric", month: "long",
  });
  const scoreText = `${credential.overall_score.toFixed(1)}/4.0`;

  const PILLARS = ["P1", "P2", "P3", "P4", "P5", "P6"] as const;
  const pillarScores = credential.pillar_scores;

  try {
  const img = new ImageResponse(
    (
      <div
        style={{
          width: 1200,
          height: 630,
          background: "linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #0c1a3a 100%)",
          display: "flex",
          fontFamily: "system-ui, sans-serif",
          color: "white",
          padding: 64,
          gap: 48,
          alignItems: "center",
        }}
      >
        {/* Left: badge + academy */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 20,
            flexShrink: 0,
          }}
        >
          <div
            style={{
              width: 200,
              height: 200,
              background: "linear-gradient(135deg, #4f46e5, #7c3aed)",
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <div style={{ fontSize: 64, fontWeight: 900, color: "white" }}>AI</div>
          </div>
          <div style={{ fontSize: 16, color: "#818cf8", letterSpacing: 2, textTransform: "uppercase" }}>
            AI Hero Academy
          </div>
        </div>

        {/* Right: text content */}
        <div style={{ display: "flex", flexDirection: "column", gap: 20, flex: 1 }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            <div style={{ fontSize: 48, fontWeight: 900, lineHeight: 1.1, color: "white" }}>
              AI-Supercharged
            </div>
            <div style={{ fontSize: 48, fontWeight: 900, lineHeight: 1.1, color: "#a5b4fc" }}>
              Intermediate
            </div>
          </div>

          <div style={{ fontSize: 24, color: "#e2e8f0" }}>
            {credential.display_name}
          </div>

          <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
            <div
              style={{
                background: "rgba(74, 222, 128, 0.2)",
                border: "1px solid rgba(74, 222, 128, 0.4)",
                borderRadius: 8,
                padding: "8px 20px",
                fontSize: 20,
                fontWeight: 700,
                color: "#4ade80",
              }}
            >
              {`Score: ${scoreText}`}
            </div>
            <div style={{ fontSize: 16, color: "#64748b" }}>{issuedDate}</div>
          </div>

          {/* Pillar scores */}
          <div style={{ display: "flex", gap: 12 }}>
            {PILLARS.map((p) => {
              const key = p.toLowerCase() as keyof typeof pillarScores;
              const score = pillarScores[key] ?? 0;
              return (
                <div
                  key={p}
                  style={{
                    background: score >= 1 ? "rgba(79, 70, 229, 0.13)" : "#1e293b",
                    border: `1px solid ${score >= 1 ? "rgba(79, 70, 229, 0.4)" : "#334155"}`,
                    borderRadius: 8,
                    padding: "6px 12px",
                    textAlign: "center",
                    display: "flex",
                    flexDirection: "column",
                    gap: 2,
                  }}
                >
                  <div style={{ fontSize: 11, color: "#64748b" }}>{p}</div>
                  <div style={{ fontSize: 16, fontWeight: 700, color: score >= 1 ? "#818cf8" : "#475569" }}>
                    {`${score}/2`}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    ),
    { width: 1200, height: 630 }
  );

  // Force Satori rendering to complete inside the try/catch.
  // ImageResponse renders lazily during streaming; awaiting arrayBuffer() here
  // ensures any resvg/Satori crash is caught rather than killing the process.
  const buffer = await img.arrayBuffer();
  return new Response(buffer, { headers: { "Content-Type": "image/png" } });
  } catch (err) {
    console.error("share-card render error:", err);
    return new Response("Share card generation failed", { status: 500 });
  }
}
