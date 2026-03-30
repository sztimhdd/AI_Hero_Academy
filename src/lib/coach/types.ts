/**
 * Types for the AI Coach engine.
 * Pure types — no Firebase imports here so these can be used in both
 * server routes and the pure PACE logic that unit tests exercise.
 */

export type TaskId = string; // e.g. "p1_t1"

export type TaskCompleteReason = "budget_exhausted" | "mastery_early_exit";

export interface CoachStreamEvent {
  type: "text" | "task_complete" | "error";
  content?: string;             // for type: "text"
  reason?: TaskCompleteReason;  // for type: "task_complete"
  taskId?: string;              // for type: "task_complete"
  message?: string;             // for type: "error"
}

/** A single message in the ongoing coach conversation (Gemini role names). */
export interface CoachMessage {
  role: "user" | "model";
  content: string;
}

/**
 * The server-side representation of an active coaching session.
 * Stored in Firestore b2c_coach_sessions with extra fields beyond
 * the base CoachSession interface.
 */
export interface ActiveCoachSession {
  session_id: string;
  uid: string;
  user_email: string;
  pillar_id: string;
  day_number: number;
  role_context: string;
  system_prompt: string;
  task_turn_counts: Record<TaskId, number>;
  transcript: Array<{ role: string; content: string }>;
  turn_count: number;
  created_at: unknown; // Firestore Timestamp — typed as unknown to avoid import
  practice_completed_at?: unknown;
}
