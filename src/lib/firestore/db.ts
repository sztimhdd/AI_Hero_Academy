/**
 * Firestore CRUD helpers — server-side only (uses firebase-admin).
 * Never import this file in client components.
 */
import { getFirestore, Timestamp, FieldValue } from "firebase-admin/firestore";
import { getAdminAuth } from "@/lib/firebase/admin";
import {
  COLLECTIONS,
  UserProfile,
  DiagnosticSession,
  TrainingProgress,
  CoachSession,
  CoachTurn,
  LearnerModel,
  BuildArtifact,
  Credential,
  AiCallLog,
  PillarId,
  PILLAR_IDS,
} from "./types";

// Lazy Firestore instance — mirrors admin.ts lazy pattern
let _db: ReturnType<typeof getFirestore> | null = null;
function db() {
  if (_db) return _db;
  // Calling getAdminAuth() ensures the admin app is initialized first
  getAdminAuth();
  _db = getFirestore();
  // preferRest: true — use HTTP/1.1 REST instead of gRPC.
  // Required when a corporate TLS proxy blocks gRPC (HTTP/2 ALPN).
  // Wrapped in try-catch: in dev, HMR resets the module but the Firestore
  // singleton persists, so settings() may already have been called.
  try {
    _db.settings({ preferRest: true });
  } catch {
    // Already initialized — preferRest is already set, safe to ignore.
  }
  return _db;
}

// ── UserProfile ────────────────────────────────────────────────────────────────

export async function getUser(uid: string): Promise<UserProfile | null> {
  const snap = await db().collection(COLLECTIONS.USER_PROFILES).doc(uid).get();
  return snap.exists ? (snap.data() as UserProfile) : null;
}

export async function createUser(profile: UserProfile): Promise<void> {
  await db()
    .collection(COLLECTIONS.USER_PROFILES)
    .doc(profile.uid)
    .set(profile);
}

export async function upsertUser(
  uid: string,
  fields: Partial<UserProfile>
): Promise<void> {
  await db()
    .collection(COLLECTIONS.USER_PROFILES)
    .doc(uid)
    .set(fields, { merge: true });
}

// ── DiagnosticSession ──────────────────────────────────────────────────────────

export async function createDiagnosticSession(
  session: Omit<DiagnosticSession, "session_id">
): Promise<string> {
  const ref = db().collection(COLLECTIONS.DIAGNOSTIC_SESSIONS).doc();
  const withId: DiagnosticSession = { ...session, session_id: ref.id };
  await ref.set(withId);
  return ref.id;
}

export async function getLatestDiagnosticSession(
  uid: string
): Promise<DiagnosticSession | null> {
  const snap = await db()
    .collection(COLLECTIONS.DIAGNOSTIC_SESSIONS)
    .where("uid", "==", uid)
    .get();
  if (snap.empty) return null;
  const docs = snap.docs.map((d) => d.data() as DiagnosticSession);
  docs.sort((a, b) => b.completed_at.toMillis() - a.completed_at.toMillis());
  return docs[0];
}

// ── TrainingProgress ──────────────────────────────────────────────────────────

export async function upsertTrainingProgress(
  uid: string,
  pillarId: PillarId,
  fields: Partial<TrainingProgress>
): Promise<void> {
  const docId = `${uid}_${pillarId}`;
  await db()
    .collection(COLLECTIONS.TRAINING_PROGRESS)
    .doc(docId)
    .set(fields, { merge: true });
}

export async function getTrainingProgress(
  uid: string
): Promise<TrainingProgress[]> {
  // Fetch by known doc IDs to avoid requiring a composite index on (uid, sequence_order).
  const pillarOrder: PillarId[] = ["p1", "p2", "p3", "p4", "p5", "p6", "capstone"];
  const refs = pillarOrder.map((p) =>
    db().collection(COLLECTIONS.TRAINING_PROGRESS).doc(`${uid}_${p}`)
  );
  const snaps = await db().getAll(...refs);
  return snaps
    .filter((s) => s.exists)
    .map((s) => s.data() as TrainingProgress);
}

/**
 * Initializes training progress after onboarding:
 * - p1: unlocked (is_locked: false)
 * - p2–p6 + capstone: locked (is_locked: true)
 */
export async function initTrainingProgress(
  uid: string,
  userEmail: string
): Promise<void> {
  const batch = db().batch();
  const pillarsInOrder: PillarId[] = [
    ...PILLAR_IDS,
    "capstone" as PillarId,
  ];

  pillarsInOrder.forEach((pillarId, idx) => {
    const docId = `${uid}_${pillarId}`;
    const ref = db().collection(COLLECTIONS.TRAINING_PROGRESS).doc(docId);
    const progress: TrainingProgress = {
      uid,
      user_email: userEmail,
      pillar_id: pillarId,
      day_number: idx + 1,
      sequence_order: idx,
      is_locked: idx !== 0, // only p1 is unlocked
    };
    batch.set(ref, progress);
  });

  await batch.commit();
}

// ── CoachSession ───────────────────────────────────────────────────────────────

export async function createCoachSession(
  session: Omit<CoachSession, "session_id">
): Promise<string> {
  const ref = db().collection(COLLECTIONS.COACH_SESSIONS).doc();
  const withId: CoachSession = { ...session, session_id: ref.id };
  await ref.set(withId);
  return ref.id;
}

export async function appendCoachTurn(
  sessionId: string,
  turn: CoachTurn
): Promise<void> {
  const ref = db().collection(COLLECTIONS.COACH_SESSIONS).doc(sessionId);
  await ref.update({
    transcript: FieldValue.arrayUnion(turn),
    turn_count: FieldValue.increment(1),
  });
}

// ── LearnerModel ───────────────────────────────────────────────────────────────

export async function upsertLearnerModel(
  uid: string,
  fields: Partial<LearnerModel>
): Promise<void> {
  await db()
    .collection(COLLECTIONS.LEARNER_MODEL)
    .doc(uid)
    .set({ ...fields, last_updated: Timestamp.now() }, { merge: true });
}

// ── BuildArtifact ─────────────────────────────────────────────────────────────

export async function saveBuildArtifact(
  uid: string,
  pillarId: PillarId,
  artifact: Omit<BuildArtifact, "uid" | "pillar_id" | "created_at" | "updated_at">
): Promise<void> {
  const docId = `${uid}_${pillarId}`;
  const now = Timestamp.now();
  const existing = await db()
    .collection(COLLECTIONS.BUILD_ARTIFACTS)
    .doc(docId)
    .get();

  await db()
    .collection(COLLECTIONS.BUILD_ARTIFACTS)
    .doc(docId)
    .set(
      {
        uid,
        pillar_id: pillarId,
        ...artifact,
        updated_at: now,
        created_at: existing.exists ? existing.data()!.created_at : now,
      },
      { merge: true }
    );
}

// ── Credential ────────────────────────────────────────────────────────────────

export async function issueCredential(
  credential: Credential
): Promise<void> {
  const docId = `${credential.uid}_${credential.credential_id}`;
  await db()
    .collection(COLLECTIONS.CREDENTIALS)
    .doc(docId)
    .set(credential);
}

// ── LearnerModel (read) ────────────────────────────────────────────────────────

export async function getLearnerModel(uid: string): Promise<LearnerModel | null> {
  const snap = await db().collection(COLLECTIONS.LEARNER_MODEL).doc(uid).get();
  return snap.exists ? (snap.data() as LearnerModel) : null;
}

// ── CoachSession (read + update) ───────────────────────────────────────────────

export async function getCoachSession(sessionId: string): Promise<Record<string, unknown> | null> {
  const snap = await db().collection(COLLECTIONS.COACH_SESSIONS).doc(sessionId).get();
  return snap.exists ? snap.data() as Record<string, unknown> : null;
}

/**
 * Atomically increments task_turn_counts[taskId] in the session doc.
 * Returns the NEW count after the increment.
 * Uses a transaction so we can read the new value atomically.
 */
export async function updateCoachSessionTurns(
  sessionId: string,
  taskId: string
): Promise<number> {
  const ref = db().collection(COLLECTIONS.COACH_SESSIONS).doc(sessionId);
  const newCount = await db().runTransaction(async (tx) => {
    const snap = await tx.get(ref);
    const data = snap.data() as Record<string, unknown>;
    const counts = (data.task_turn_counts as Record<string, number>) ?? {};
    const current = counts[taskId] ?? 0;
    const updated = current + 1;
    tx.update(ref, { [`task_turn_counts.${taskId}`]: updated });
    return updated;
  });
  return newCount;
}

/**
 * Writes the full practice transcript and marks practice complete.
 */
export async function completeCoachSession(
  sessionId: string,
  transcript: Array<{ role: string; content: string }>,
  practiceCompletedAt: import("firebase-admin/firestore").Timestamp
): Promise<void> {
  const ref = db().collection(COLLECTIONS.COACH_SESSIONS).doc(sessionId);
  await ref.update({
    transcript,
    turn_count: transcript.length,
    practice_completed_at: practiceCompletedAt,
  });
}

// ── TrainingProgress (single doc) ─────────────────────────────────────────────

export async function getTrainingProgressDoc(
  uid: string,
  pillarId: PillarId
): Promise<TrainingProgress | null> {
  const docId = `${uid}_${pillarId}`;
  const snap = await db().collection(COLLECTIONS.TRAINING_PROGRESS).doc(docId).get();
  return snap.exists ? (snap.data() as TrainingProgress) : null;
}

// ── BuildArtifact (read) ───────────────────────────────────────────────────────

export async function getBuildArtifacts(uid: string): Promise<BuildArtifact[]> {
  const snap = await db()
    .collection(COLLECTIONS.BUILD_ARTIFACTS)
    .where("uid", "==", uid)
    .get();
  return snap.docs
    .map((d) => d.data() as BuildArtifact)
    .sort((a, b) => (a.day_number ?? 0) - (b.day_number ?? 0));
}

// ── Credential (read) ─────────────────────────────────────────────────────────

export async function getCredential(uid: string): Promise<Credential | null> {
  const snap = await db()
    .collection(COLLECTIONS.CREDENTIALS)
    .where("uid", "==", uid)
    .get();
  if (snap.empty) return null;
  // Sort descending by issued_at client-side to avoid composite index requirement
  const docs = snap.docs.map((d) => d.data() as Credential);
  docs.sort((a, b) => b.issued_at.toMillis() - a.issued_at.toMillis());
  return docs[0];
}

// ── UserProfile (lang update) ─────────────────────────────────────────────────

export async function updateUserLang(
  uid: string,
  lang: "en" | "zh"
): Promise<void> {
  await db().collection(COLLECTIONS.USER_PROFILES).doc(uid).update({ lang });
}

// ── Streak update ─────────────────────────────────────────────────────────────

export async function updateStreak(uid: string): Promise<void> {
  const today = new Date().toISOString().slice(0, 10); // "YYYY-MM-DD"
  const snap = await db().collection(COLLECTIONS.USER_PROFILES).doc(uid).get();
  if (!snap.exists) return;
  const data = snap.data() as UserProfile;
  if (data.last_active_date === today) return; // already counted today

  const yesterday = new Date(Date.now() - 86_400_000).toISOString().slice(0, 10);
  const newStreak =
    data.last_active_date === yesterday ? (data.streak_days ?? 0) + 1 : 1;

  await db()
    .collection(COLLECTIONS.USER_PROFILES)
    .doc(uid)
    .update({ streak_days: newStreak, last_active_date: today });
}

// ── AiCallLog ─────────────────────────────────────────────────────────────────

export async function logAiCall(
  entry: Omit<AiCallLog, "log_id" | "created_at">
): Promise<void> {
  const ref = db().collection(COLLECTIONS.AI_CALL_LOG).doc();
  await ref.set({
    ...entry,
    log_id: ref.id,
    created_at: Timestamp.now(),
  });
}
