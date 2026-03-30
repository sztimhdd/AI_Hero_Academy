/**
 * GET /api/credential/cert?uid=xxx
 * Streams a PDF certificate using @react-pdf/renderer.
 */
import { NextRequest } from "next/server";
import { getCredential } from "@/lib/firestore/db";
import { Document, Page, Text, View, StyleSheet, renderToBuffer } from "@react-pdf/renderer";

export const runtime = "nodejs";

const styles = StyleSheet.create({
  page: {
    backgroundColor: "#0f172a",
    padding: 60,
    fontFamily: "Helvetica",
  },
  header: {
    borderBottom: "1pt solid #334155",
    paddingBottom: 24,
    marginBottom: 32,
  },
  academy: {
    fontSize: 10,
    color: "#818cf8",
    letterSpacing: 3,
    textTransform: "uppercase",
    marginBottom: 8,
  },
  title: {
    fontSize: 32,
    fontWeight: "bold",
    color: "#ffffff",
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 32,
    fontWeight: "bold",
    color: "#a5b4fc",
  },
  certifies: {
    fontSize: 12,
    color: "#64748b",
    marginBottom: 8,
  },
  name: {
    fontSize: 28,
    color: "#e2e8f0",
    fontWeight: "bold",
    marginBottom: 4,
  },
  description: {
    fontSize: 12,
    color: "#94a3b8",
    lineHeight: 1.6,
    marginBottom: 32,
  },
  grid: {
    flexDirection: "row",
    gap: 12,
    marginBottom: 32,
  },
  pillarBox: {
    flex: 1,
    backgroundColor: "#1e293b",
    borderRadius: 6,
    padding: 10,
    alignItems: "center",
  },
  pillarLabel: {
    fontSize: 10,
    color: "#64748b",
    textTransform: "uppercase",
    marginBottom: 4,
  },
  pillarScore: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#818cf8",
  },
  footer: {
    flexDirection: "row",
    justifyContent: "space-between",
    borderTop: "1pt solid #334155",
    paddingTop: 16,
  },
  footerLabel: {
    fontSize: 9,
    color: "#64748b",
    textTransform: "uppercase",
    letterSpacing: 1,
    marginBottom: 4,
  },
  footerValue: {
    fontSize: 13,
    color: "#e2e8f0",
    fontWeight: "bold",
  },
  overallBox: {
    backgroundColor: "#1e3a2a",
    borderRadius: 8,
    padding: "12 20",
    marginBottom: 32,
    flexDirection: "row",
    alignItems: "center",
    gap: 16,
  },
  overallLabel: {
    fontSize: 11,
    color: "#64748b",
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  overallScore: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#4ade80",
  },
});


export async function GET(req: NextRequest) {
  const uid = req.nextUrl.searchParams.get("uid");
  if (!uid) return new Response("uid required", { status: 400 });

  const credential = await getCredential(uid);
  if (!credential) return new Response("Credential not found", { status: 404 });

  const issuedDate = credential.issued_at.toDate().toLocaleDateString("en-US", {
    year: "numeric", month: "long", day: "numeric",
  });

  const displayName = credential.display_name;
  const overallScore = credential.overall_score;
  const pillarScores = credential.pillar_scores as unknown as Record<string, number>;
  const credentialId = credential.credential_id;
  const pillars = ["p1", "p2", "p3", "p4", "p5", "p6"];

  const pdfBuffer = await renderToBuffer(
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (<Document>
      <Page size="A4" orientation="landscape" style={styles.page}>
        <View style={styles.header}>
          <Text style={styles.academy}>AI Hero Academy</Text>
          <Text style={styles.title}>AI-Supercharged</Text>
          <Text style={styles.subtitle}>Intermediate Certificate</Text>
        </View>
        <Text style={styles.certifies}>This certifies that</Text>
        <Text style={styles.name}>{displayName}</Text>
        <Text style={styles.description}>
          has successfully completed the 7-day AI Hero Academy program, demonstrating
          competency across all six AI skill pillars: Foundations, Precision Prompting,
          Tool Fluency, AI Configuration, AI Workflows, and Agentic Systems.
        </Text>
        <View style={styles.overallBox}>
          <View>
            <Text style={styles.overallLabel}>Overall Score</Text>
            <Text style={styles.overallScore}>{overallScore.toFixed(1)} / 4.0</Text>
          </View>
        </View>
        <View style={styles.grid}>
          {pillars.map((p) => (
            <View key={p} style={styles.pillarBox}>
              <Text style={styles.pillarLabel}>{p.toUpperCase()}</Text>
              <Text style={styles.pillarScore}>{(pillarScores[p] ?? 0)}/2</Text>
            </View>
          ))}
        </View>
        <View style={styles.footer}>
          <View>
            <Text style={styles.footerLabel}>Issue Date</Text>
            <Text style={styles.footerValue}>{issuedDate}</Text>
          </View>
          <View>
            <Text style={styles.footerLabel}>Credential ID</Text>
            <Text style={styles.footerValue}>{credentialId}</Text>
          </View>
          <View>
            <Text style={styles.footerLabel}>Issuer</Text>
            <Text style={styles.footerValue}>AI Hero Academy</Text>
          </View>
        </View>
      </Page>
    </Document>) as Parameters<typeof renderToBuffer>[0]
  );

  return new Response(pdfBuffer as unknown as BodyInit, {
    headers: {
      "Content-Type": "application/pdf",
      "Content-Disposition": `attachment; filename="ai-hero-academy-certificate.pdf"`,
      "Cache-Control": "public, max-age=86400",
    },
  });
}
