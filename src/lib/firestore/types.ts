import { Timestamp } from "firebase-admin/firestore";

// ── Collection name constants ──────────────────────────────────────────────────
// Prefixed b2c_ to avoid collision with legacy Streamlit collections in shared DB.
export const COLLECTIONS = {
  USER_PROFILES: "b2c_user_profiles",
  DIAGNOSTIC_SESSIONS: "b2c_diagnostic_sessions",
  TRAINING_PROGRESS: "b2c_training_progress",
  COACH_SESSIONS: "b2c_coach_sessions",
  LEARNER_MODEL: "b2c_learner_model",
  BUILD_ARTIFACTS: "b2c_build_artifacts",
  CREDENTIALS: "b2c_credentials",
  AI_CALL_LOG: "b2c_ai_call_log",
} as const;

// ── 1. UserProfile ─────────────────────────────────────────────────────────────
// Document ID: uid (Firebase Auth UID)
export interface UserProfile {
  uid: string;
  user_email: string;
  display_name: string;
  profile_photo_url: string;
  auth_provider: "google" | "linkedin" | "facebook" | string;
  lang: "en" | "zh";
  // Set during onboarding Screen 1
  declared_role?: string;
  declared_industry?: string;
  daily_work_desc?: string;
  // Set during onboarding Screen 2
  current_ai_usage?: string;
  primary_motivation?: "save_time" | "quality" | "career" | "explore";
  // Set on onboarding completion
  program_started_at?: Timestamp;
  // Activity tracking
  streak_days: number;
  last_active_date?: string; // ISO date string "YYYY-MM-DD"
  created_at: Timestamp;
}

// ── 2. DiagnosticSession ───────────────────────────────────────────────────────
// Document ID: auto-generated
export interface DiagnosticSession {
  session_id: string;
  uid: string;
  user_email: string;
  completed_at: Timestamp;
  pillar_scores: PillarScores; // {p1: 0-100, p2: 0-100, ..., p6: 0-100}
  overall_score: number;
  item_scores: Record<string, number>; // question_id → score
  session_number: number; // 1 = baseline, 2+ = re-assessment
  ai_question_used?: string; // the personalized question text (if Gemini generated)
  ai_question_answer?: string; // learner's free-text answer
}

// ── 3. TrainingProgress ────────────────────────────────────────────────────────
// Document ID: {uid}_{pillar_id}  e.g. "abc123_p1"
export interface TrainingProgress {
  uid: string;
  user_email: string;
  pillar_id: PillarId; // "p1" | "p2" | ... | "p6" | "capstone"
  day_number: number; // 1-7
  sequence_order: number; // for rendering order
  is_locked: boolean;
  reading_completed_at?: Timestamp;
  practice_completed_at?: Timestamp;
  quiz_completed_at?: Timestamp;
  quiz_score?: number;
  quiz_passed?: boolean;
  build_artifact?: string; // the artifact the learner produced
  build_completed_at?: Timestamp;
  pillar_score_after?: number;
}

// ── 4. CoachSession ────────────────────────────────────────────────────────────
// Document ID: auto-generated
export interface CoachSession {
  session_id: string;
  uid: string;
  user_email: string;
  pillar_id: PillarId;
  day_number: number;
  role_context: string; // injected at session start from UserProfile
  transcript: CoachTurn[];
  turn_count: number;
  created_at: Timestamp;
}

export interface CoachTurn {
  role: "user" | "assistant";
  content: string;
  timestamp: Timestamp;
}

// ── 5. LearnerModel ────────────────────────────────────────────────────────────
// Document ID: uid
// Updated by synthesis agent after each day's completion.
export interface LearnerModel {
  uid: string;
  user_email: string;
  natural_strengths: string[];
  recurring_gaps: string[];
  mental_model_notes: string;
  preferred_framing: "examples" | "challenge" | "abstract" | "concrete";
  memorable_quotes: string[]; // verbatim from coach transcripts
  daily_summaries: Partial<Record<PillarId, string>>;
  last_updated: Timestamp;
}

// ── 6. BuildArtifact ──────────────────────────────────────────────────────────
// Document ID: {uid}_{pillar_id}
export interface BuildArtifact {
  uid: string;
  user_email: string;
  pillar_id: PillarId;
  day_number: number;
  artifact_type:
    | "checklist"
    | "prompt_template"
    | "system_prompt"
    | "workflow_doc"
    | "agent_design";
  artifact_title: string;
  artifact_content: string; // markdown / plain text
  created_at: Timestamp;
  updated_at: Timestamp;
}

// ── 7. Credential ─────────────────────────────────────────────────────────────
// Document ID: {uid}_{credential_id}
export interface Credential {
  uid: string;
  user_email: string;
  display_name: string; // for badge/PDF rendering
  credential_id: string; // e.g. "ai_supercharged_intermediate"
  issued_at: Timestamp;
  pillar_scores: PillarScores;
  overall_score: number;
}

// ── 8. AiCallLog ──────────────────────────────────────────────────────────────
// Document ID: auto-generated
export interface AiCallLog {
  log_id: string;
  uid: string;
  user_email: string;
  model: string; // e.g. "gemini-2.0-flash"
  prompt_tokens: number;
  completion_tokens: number;
  latency_ms: number;
  route: string; // API route that made the call
  created_at: Timestamp;
}

// ── Shared value types ────────────────────────────────────────────────────────
export type PillarId = "p1" | "p2" | "p3" | "p4" | "p5" | "p6" | "capstone";
export type PillarScores = Record<"p1" | "p2" | "p3" | "p4" | "p5" | "p6", number>;

export const PILLAR_IDS: PillarId[] = ["p1", "p2", "p3", "p4", "p5", "p6"];
