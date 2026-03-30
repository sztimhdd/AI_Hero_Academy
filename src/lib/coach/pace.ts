/**
 * PACE enforcement — pure functions only.
 * No Firebase, no Next.js imports. Unit-testable in isolation.
 *
 * The 3-question budget per task is enforced here.
 * Q4 is blocked server-side by isTurnBlocked(), not just in system prompts.
 */

import type { CoachStreamEvent, TaskCompleteReason, TaskId } from "./types";

/** Hard ceiling: 3 questions per task (Q1 open, Q2 adaptive, Q3 synthesis). */
export const TURN_BUDGET = 3;

/**
 * Special token the coach model must emit at the end of its response
 * when it closes a task early due to mastery.
 * Appended to the system prompt by assembler.ts.
 */
export const MASTERY_TOKEN = "[[TASK_COMPLETE]]";

/**
 * Returns true when the current task's turn count has reached or exceeded
 * the budget — meaning the next user message should be blocked.
 *
 * @param taskTurnCount  Number of turns ALREADY used for this task.
 */
export function isTurnBlocked(taskTurnCount: number): boolean {
  return taskTurnCount >= TURN_BUDGET;
}

/**
 * Returns true when the coach model's response contains the mastery token,
 * indicating the task's learning objective has been met before Q3.
 */
export function hasMasterySignal(response: string): boolean {
  return response.includes(MASTERY_TOKEN);
}

/**
 * Constructs a task_complete SSE event payload.
 */
export function makeTaskCompleteEvent(
  reason: TaskCompleteReason,
  taskId: TaskId
): CoachStreamEvent {
  return { type: "task_complete", reason, taskId };
}

/**
 * Removes the mastery token (and any trailing newline) from a coach response
 * before it is forwarded to the client.
 */
export function stripMasteryToken(response: string): string {
  return response.replace(MASTERY_TOKEN, "").trimEnd();
}

/**
 * Serialises a CoachStreamEvent to the SSE wire format.
 * e.g.  data: {"type":"text","content":"Hello"}\n\n
 */
export function formatSseEvent(event: CoachStreamEvent): string {
  return `data: ${JSON.stringify(event)}\n\n`;
}
