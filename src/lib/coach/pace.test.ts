import { describe, it, expect } from "vitest";
import {
  TURN_BUDGET,
  MASTERY_TOKEN,
  isTurnBlocked,
  hasMasterySignal,
  makeTaskCompleteEvent,
  stripMasteryToken,
  formatSseEvent,
} from "./pace";

describe("PACE — isTurnBlocked (3-question budget)", () => {
  it("allows turn when count is 0 (Q1 not yet used)", () => {
    expect(isTurnBlocked(0)).toBe(false);
  });

  it("allows turn when count is 1 (Q2 not yet used)", () => {
    expect(isTurnBlocked(1)).toBe(false);
  });

  it("allows turn when count is 2 (Q3 not yet used)", () => {
    expect(isTurnBlocked(2)).toBe(false);
  });

  it("blocks Q4 — turn count equals TURN_BUDGET (3)", () => {
    expect(isTurnBlocked(TURN_BUDGET)).toBe(true);
  });

  it("blocks any turn beyond the budget", () => {
    expect(isTurnBlocked(4)).toBe(true);
    expect(isTurnBlocked(10)).toBe(true);
  });

  it("TURN_BUDGET constant is 3", () => {
    expect(TURN_BUDGET).toBe(3);
  });
});

describe("PACE — hasMasterySignal (early exit detection)", () => {
  it("returns true when response ends with mastery token on its own line", () => {
    const response =
      "That's exactly it — you caught the pattern most people miss.\n[[TASK_COMPLETE]]";
    expect(hasMasterySignal(response)).toBe(true);
  });

  it("returns true when mastery token appears inline", () => {
    expect(hasMasterySignal("Great work! [[TASK_COMPLETE]] You're done.")).toBe(true);
  });

  it("returns false when response contains no mastery token", () => {
    expect(hasMasterySignal("Good try. Think a bit deeper about the second scenario.")).toBe(
      false
    );
  });

  it("returns false for empty string", () => {
    expect(hasMasterySignal("")).toBe(false);
  });

  it("MASTERY_TOKEN constant is [[TASK_COMPLETE]]", () => {
    expect(MASTERY_TOKEN).toBe("[[TASK_COMPLETE]]");
  });
});

describe("PACE — makeTaskCompleteEvent", () => {
  it("emits budget_exhausted event with correct shape", () => {
    const event = makeTaskCompleteEvent("budget_exhausted", "p1_t1");
    expect(event.type).toBe("task_complete");
    expect(event.reason).toBe("budget_exhausted");
    expect(event.taskId).toBe("p1_t1");
  });

  it("emits mastery_early_exit event with correct shape", () => {
    const event = makeTaskCompleteEvent("mastery_early_exit", "p1_t3");
    expect(event.type).toBe("task_complete");
    expect(event.reason).toBe("mastery_early_exit");
    expect(event.taskId).toBe("p1_t3");
  });

  it("event has no content field", () => {
    const event = makeTaskCompleteEvent("budget_exhausted", "p1_t1");
    expect(event.content).toBeUndefined();
  });
});

describe("PACE — stripMasteryToken", () => {
  it("removes the mastery token from the end of a response", () => {
    const raw = "Nice work! You nailed it.\n[[TASK_COMPLETE]]";
    expect(stripMasteryToken(raw)).toBe("Nice work! You nailed it.");
  });

  it("leaves responses without the token unchanged", () => {
    const clean = "Think about the third scenario.";
    expect(stripMasteryToken(clean)).toBe(clean);
  });
});

describe("PACE — formatSseEvent", () => {
  it("serialises a text event to SSE wire format", () => {
    const wire = formatSseEvent({ type: "text", content: "Hello" });
    expect(wire).toBe('data: {"type":"text","content":"Hello"}\n\n');
  });

  it("serialises a task_complete event to SSE wire format", () => {
    const wire = formatSseEvent({
      type: "task_complete",
      reason: "budget_exhausted",
      taskId: "p1_t2",
    });
    expect(wire).toContain('"type":"task_complete"');
    expect(wire).toContain('"reason":"budget_exhausted"');
    expect(wire).toContain('"taskId":"p1_t2"');
    expect(wire).toMatch(/\n\n$/);
  });
});
