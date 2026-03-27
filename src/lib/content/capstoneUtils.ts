/**
 * Pure utility functions for capstone template filling.
 * No Node.js dependencies — safe for client and server.
 */

export function fillScenario(
  template: string,
  role: string,
  industry: string,
  dailyWork?: string
): string {
  return template
    .replace(/\{declared_role\}/g, role || "professional")
    .replace(/\{declared_industry\}/g, industry || "their industry")
    .replace(/\{daily_work_desc\}/g, dailyWork || "");
}

export function fillSectionPrompt(
  template: string,
  role: string,
  industry: string
): string {
  return template
    .replace(/\{declared_role\}/g, role || "professional")
    .replace(/\{declared_industry\}/g, industry || "their industry");
}
