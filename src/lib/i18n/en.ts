export const en = {
  // Landing page
  "landing.tagline": "Master AI in 7 Days",
  "landing.subtitle":
    "A structured program to transform how you work with AI — from basics to confident, daily practice.",
  "landing.signin_google": "Continue with Google",
  "landing.signin_facebook": "Continue with Facebook",
  "landing.signin_linkedin": "Continue with LinkedIn",
  "landing.terms": "By signing in you agree to our Terms of Service and Privacy Policy.",
  "landing.lang_toggle": "中文",

  // Onboarding
  "onboarding.step": "Step {current} of {total}",
  "onboarding.next": "Next →",
  "onboarding.back": "← Back",
  "onboarding.submit": "See My Gap Map →",
  "onboarding.s1.title": "Tell us about your work",
  "onboarding.s1.role_label": "Your role",
  "onboarding.s1.role_placeholder": "Select your role",
  "onboarding.s1.industry_label": "Your industry",
  "onboarding.s1.industry_placeholder": "Select your industry",
  "onboarding.s1.daily_work_label": "Describe your daily work",
  "onboarding.s1.daily_work_placeholder":
    "What are your main tasks? What takes the most time?",
  "onboarding.s2.title": "Your AI journey so far",
  "onboarding.s2.tools_label": "Which AI tools have you used at work?",
  "onboarding.s2.tools_placeholder": "e.g. ChatGPT for drafting emails, Copilot for code…",
  "onboarding.s2.motivation_label": "What's your primary goal?",
  "onboarding.s2.motivation_save_time": "Save time on repetitive tasks",
  "onboarding.s2.motivation_quality": "Improve the quality of my work",
  "onboarding.s2.motivation_career": "Advance my career",
  "onboarding.s2.motivation_explore": "Explore what AI can do",
  "onboarding.s3.title": "Quick diagnostic",
  "onboarding.s3.subtitle": "5 questions to map your AI skill gaps",
  "onboarding.s3.ai_question_label": "One more — personalized for you",
  "onboarding.s3.fallback_question":
    "Describe a recent work task where AI could have helped. What stopped you from using it?",
  "onboarding.s4.title": "Your AI Gap Map",
  "onboarding.s4.subtitle": "Here's where you stand across 6 core AI skill pillars",
  "onboarding.s4.cta": "Start Day 1 →",
  "onboarding.s4.pillar.p1": "Prompting",
  "onboarding.s4.pillar.p2": "Context & Memory",
  "onboarding.s4.pillar.p3": "Workflow Integration",
  "onboarding.s4.pillar.p4": "Output Evaluation",
  "onboarding.s4.pillar.p5": "Tool Selection",
  "onboarding.s4.pillar.p6": "Ethics & Risk",

  // Dashboard
  "dashboard.title": "Your Learning Journey",
  "dashboard.day": "Day {n}",
  "dashboard.locked": "Locked",

  // Common
  "common.loading": "Loading…",
  "common.error": "Something went wrong. Please try again.",
  "common.signout": "Sign out",
} as const;

export type TranslationKey = keyof typeof en;
