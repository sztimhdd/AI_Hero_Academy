/**
 * GET /api/credential/badge?uid=xxx
 * Generates a 600×600 Open Badge PNG using Next.js ImageResponse (Satori).
 */
import { ImageResponse } from "next/og";
import { NextRequest } from "next/server";
import { getCredential } from "@/lib/firestore/db";

export const runtime = "nodejs";

export async function GET(req: NextRequest) {
  const uid = req.nextUrl.searchParams.get("uid");
  if (!uid) return new Response("uid required", { status: 400 });

  const credential = await getCredential(uid);
  if (!credential) return new Response("Credential not found", { status: 404 });

  const issuedDate = credential.issued_at.toDate().toLocaleDateString("en-US", {
    year: "numeric", month: "long", day: "numeric",
  });
  const scoreText = `${credential.overall_score.toFixed(1)} / 4.0`;

  const img = new ImageResponse(
    (
      <div
        style={{
          width: 600,
          height: 600,
          background: "linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          fontFamily: "system-ui, sans-serif",
          color: "white",
          padding: 40,
          gap: 24,
        }}
      >
        {/* Hex badge shape */}
        <div
          style={{
            width: 180,
            height: 180,
            background: "linear-gradient(135deg, #4f46e5, #7c3aed)",
            clipPath: "polygon(50% 0%, 93% 25%, 93% 75%, 50% 100%, 7% 75%, 7% 25%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexDirection: "column",
          }}
        >
          <div style={{ fontSize: 64, lineHeight: 1 }}>🏆</div>
        </div>

        {/* Title */}
        <div style={{ textAlign: "center", display: "flex", flexDirection: "column", gap: 8 }}>
          <div style={{ fontSize: 13, color: "#818cf8", letterSpacing: 3, textTransform: "uppercase" }}>
            AI Hero Academy
          </div>
          <div style={{ fontSize: 28, fontWeight: 800, color: "white", lineHeight: 1.2 }}>
            AI-Supercharged
          </div>
          <div style={{ fontSize: 28, fontWeight: 800, color: "#a5b4fc", lineHeight: 1.2 }}>
            Intermediate
          </div>
        </div>

        {/* Learner name */}
        <div style={{ fontSize: 20, color: "#e2e8f0", fontWeight: 600 }}>
          {credential.display_name}
        </div>

        {/* Score + date */}
        <div style={{ display: "flex", gap: 32, alignItems: "center" }}>
          <div style={{ textAlign: "center", display: "flex", flexDirection: "column", gap: 4 }}>
            <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }}>Score</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: "#4ade80" }}>{scoreText}</div>
          </div>
          <div style={{ width: 1, height: 40, background: "#334155" }} />
          <div style={{ textAlign: "center", display: "flex", flexDirection: "column", gap: 4 }}>
            <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }}>Issued</div>
            <div style={{ fontSize: 14, color: "#94a3b8" }}>{issuedDate}</div>
          </div>
        </div>
      </div>
    ),
    {
      width: 600,
      height: 600,
    }
  );

  // Cache for 24h
  return new Response(img.body, {
    headers: {
      "Content-Type": "image/png",
      "Cache-Control": "public, max-age=86400",
    },
  });
}
