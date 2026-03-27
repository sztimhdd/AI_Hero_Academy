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
function db() {
  // Calling getAdminAuth() ensures the admin app is initialized first
  getAdminAuth();
  return getFirestore();
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
    .orderBy("completed_at", "desc")
    .limit(1)
    .get();
  if (snap.empty) return null;
  return snap.docs[0].data() as DiagnosticSession;
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
  const snap = await db()
    .collection(COLLECTIONS.TRAINING_PROGRESS)
    .where("uid", "==", uid)
    .orderBy("sequence_order")
    .get();
  return snap.docs.map((d) => d.data() as TrainingProgress);
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
