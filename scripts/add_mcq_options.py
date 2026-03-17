"""
add_mcq_options.py — Injects task_modes and task_mcq_options into practice_scenarios.json.

Run from project root:
    .venv/Scripts/python scripts/add_mcq_options.py

Idempotent: safe to re-run; overwrites existing task_modes/task_mcq_options fields.
"""

import json
from pathlib import Path

SCENARIOS_PATH = Path(__file__).parent.parent / "content" / "practice_scenarios.json"

# ── MCQ option data ────────────────────────────────────────────────────────────
# All scenarios share task_modes = ["open", "mcq", "mcq", "mcq"]
# task_mcq_options[0] = null (open task), [1..3] = list of 3 options
# is_best marks the strongest answer the coach will positively reinforce.
# ──────────────────────────────────────────────────────────────────────────────

MCQ_DATA: dict[str, list] = {

    # ── RM ──────────────────────────────────────────────────────────────────
    "rm_c1_responsible_ai": [
        None,
        [
            {"label": "Replace all client-specific figures with directional ranges before prompting", "is_best": True},
            {"label": "Remove the client name only; keep financial figures for accuracy", "is_best": False},
            {"label": "Use a consumer AI tool but delete the chat history afterwards", "is_best": False},
        ],
        [
            {"label": "Rewrite using only sector-level descriptors so no single client is identifiable", "is_best": True},
            {"label": "Keep the geography since it is publicly known information", "is_best": False},
            {"label": "Add a disclaimer that the prompt is for internal use only", "is_best": False},
        ],
        [
            {"label": "Apply all four SAFE steps and add explicit output constraints to the prompt", "is_best": True},
            {"label": "Keep deal size in ranges but retain the client's industry niche", "is_best": False},
            {"label": "Send the prompt to IT for review before using the output client-facing", "is_best": False},
        ],
    ],

    "rm_c2_strategic_prompting": [
        None,
        [
            {"label": "Specify role, context, format, and constraints in one structured prompt", "is_best": True},
            {"label": "Ask the AI to decide the best format for the output", "is_best": False},
            {"label": "Send multiple short prompts and combine the best parts manually", "is_best": False},
        ],
        [
            {"label": "Add explicit output constraints to prevent the AI from inventing figures", "is_best": True},
            {"label": "Tell the AI to use a professional tone and trust its judgment on facts", "is_best": False},
            {"label": "Review the output for tone only; content accuracy is the AI's responsibility", "is_best": False},
        ],
        [
            {"label": "Iterate the prompt by adding missing constraints discovered during review", "is_best": True},
            {"label": "Accept the first output if it looks plausible and meets the word count", "is_best": False},
            {"label": "Ask the AI to self-critique and rewrite its own response", "is_best": False},
        ],
    ],

    "rm_c3_critical_eval": [
        None,
        [
            {"label": "Verify each AI claim against the source documents before using it", "is_best": True},
            {"label": "Flag only figures that differ significantly from your own recollection", "is_best": False},
            {"label": "Accept AI output that includes hedging language like 'approximately'", "is_best": False},
        ],
        [
            {"label": "Treat any unverifiable AI claim as a hallucination until confirmed", "is_best": True},
            {"label": "Ask the AI for its source; accept if it names a plausible document", "is_best": False},
            {"label": "Remove only claims the client is likely to question directly", "is_best": False},
        ],
        [
            {"label": "Replace fabricated content with your own verified language and document the change", "is_best": True},
            {"label": "Send the output with a caveat that figures are AI-generated", "is_best": False},
            {"label": "Re-prompt with stricter instructions and use the next output as-is", "is_best": False},
        ],
    ],

    "rm_c4_relationship_intel": [
        None,
        [
            {"label": "Structure the prompt with specific relationship context and a clear deliverable", "is_best": True},
            {"label": "Describe the client broadly and ask the AI to suggest relationship strategies", "is_best": False},
            {"label": "Feed the AI all CRM notes and ask it to summarise the relationship", "is_best": False},
        ],
        [
            {"label": "Provide only the strategic context the AI needs; omit personal or sensitive detail", "is_best": True},
            {"label": "Include personal details to get a more personalised recommendation", "is_best": False},
            {"label": "Let the AI infer client sentiment from financial data alone", "is_best": False},
        ],
        [
            {"label": "Apply SAFE abstractions to relationship details before prompting, then verify output", "is_best": True},
            {"label": "Share meeting notes verbatim since they are internal documents", "is_best": False},
            {"label": "Ask the AI to generate talking points without providing any background", "is_best": False},
        ],
    ],

    "rm_c5_data_decision": [
        None,
        [
            {"label": "Frame the prompt with decision context, abstracted data, and explicit output format", "is_best": True},
            {"label": "Paste the dashboard screenshot and ask the AI to interpret it", "is_best": False},
            {"label": "Ask the AI to recommend a decision without providing any data", "is_best": False},
        ],
        [
            {"label": "Verify AI-generated insights against the underlying data source", "is_best": True},
            {"label": "Use AI output directly if it aligns with your intuition", "is_best": False},
            {"label": "Ask the AI to flag its own uncertainty; use flagged items only", "is_best": False},
        ],
        [
            {"label": "Treat AI output as a first-pass hypothesis; validate each insight independently", "is_best": True},
            {"label": "Share the AI summary with the client as a supporting exhibit", "is_best": False},
            {"label": "Accept the output if it has no obvious numerical errors", "is_best": False},
        ],
    ],

    "rm_c6_augmented_comm": [
        None,
        [
            {"label": "Provide tone, audience, purpose, and explicit guardrails in the prompt", "is_best": True},
            {"label": "Ask the AI to write the email and apply your own tone afterwards", "is_best": False},
            {"label": "Use the AI draft as-is since it matches professional email conventions", "is_best": False},
        ],
        [
            {"label": "Review AI-drafted communication for accuracy, tone, and confidentiality before sending", "is_best": True},
            {"label": "Send the draft if it passes a spell-check", "is_best": False},
            {"label": "Ask a colleague to review the AI output instead of reviewing it yourself", "is_best": False},
        ],
        [
            {"label": "Constrain the prompt to prevent new claims, then verify every factual statement", "is_best": True},
            {"label": "Tell the AI the email is client-facing; trust it to self-censor sensitive content", "is_best": False},
            {"label": "Remove only the content the client specifically flagged in the last meeting", "is_best": False},
        ],
    ],

    "rm_c7_capstone": [
        None,
        [
            {"label": "Apply SAFE abstractions, specify deliverable and constraints, then verify output", "is_best": True},
            {"label": "Use the most capable AI model to reduce the need for manual verification", "is_best": False},
            {"label": "Complete the workflow faster by skipping the abstraction step for low-risk items", "is_best": False},
        ],
        [
            {"label": "Flag any AI output that cannot be traced to a source document", "is_best": True},
            {"label": "Accept AI outputs that include hedging language as sufficiently cautious", "is_best": False},
            {"label": "Share AI-generated summaries if they match your overall recollection", "is_best": False},
        ],
        [
            {"label": "Treat AI as a drafting assistant requiring full human review before client use", "is_best": True},
            {"label": "Delegate fact-checking to a junior team member to save time", "is_best": False},
            {"label": "Use AI outputs directly for internal documents but review client-facing ones", "is_best": False},
        ],
    ],

    # ── UW ──────────────────────────────────────────────────────────────────
    "uw_c1_responsible_ai": [
        None,
        [
            {"label": "Replace client-specific data with sector-level abstractions before prompting", "is_best": True},
            {"label": "Remove the borrower name only; keep financial ratios for accuracy", "is_best": False},
            {"label": "Use consumer AI tools for analysis but keep outputs off the credit file", "is_best": False},
        ],
        [
            {"label": "Abstract all re-identification signals including geography, deal size, and structure", "is_best": True},
            {"label": "Keep covenants in the prompt since they are standard industry terms", "is_best": False},
            {"label": "Add a prompt instruction telling the AI not to share the data externally", "is_best": False},
        ],
        [
            {"label": "Apply all SAFE steps and add output constraints to prevent AI from inventing figures", "is_best": True},
            {"label": "Retain the borrower's industry niche since it is not personally identifiable", "is_best": False},
            {"label": "Send the abstracted prompt to compliance for pre-approval before use", "is_best": False},
        ],
    ],

    "uw_c2_strategic_prompting": [
        None,
        [
            {"label": "Structure the prompt with role, abstracted context, deliverable, and constraints", "is_best": True},
            {"label": "Ask the AI to decide the analysis approach based on available data", "is_best": False},
            {"label": "Submit multiple short prompts and merge the outputs", "is_best": False},
        ],
        [
            {"label": "Add explicit constraints preventing the AI from generating fictional ratios or covenants", "is_best": True},
            {"label": "Trust the AI to stay within the credit context you have described", "is_best": False},
            {"label": "Instruct the AI to flag any assumptions; accept the flagged output as reviewed", "is_best": False},
        ],
        [
            {"label": "Refine the prompt iteratively, adding constraints each time an issue is found", "is_best": True},
            {"label": "Accept the first plausible output to keep the review process efficient", "is_best": False},
            {"label": "Ask the AI to self-assess its output quality before finalising", "is_best": False},
        ],
    ],

    "uw_c3_critical_eval": [
        None,
        [
            {"label": "Cross-reference every AI-generated figure against the source credit application", "is_best": True},
            {"label": "Flag only figures that differ by more than 10% from your own estimate", "is_best": False},
            {"label": "Accept AI output that includes phrases like 'based on available data'", "is_best": False},
        ],
        [
            {"label": "Treat any AI claim that lacks a traceable source as a potential hallucination", "is_best": True},
            {"label": "Ask the AI to cite its source; use the output if a plausible source is named", "is_best": False},
            {"label": "Remove only the claims most likely to affect the credit decision", "is_best": False},
        ],
        [
            {"label": "Replace all unverifiable AI content with your own validated language", "is_best": True},
            {"label": "Attach the AI output as a supporting exhibit with a caveat note", "is_best": False},
            {"label": "Re-prompt with tighter constraints and accept the revised output", "is_best": False},
        ],
    ],

    "uw_c4_relationship_intel": [
        None,
        [
            {"label": "Provide abstracted borrower context and a clear analytical deliverable", "is_best": True},
            {"label": "Include all covenant details to give the AI full context", "is_best": False},
            {"label": "Ask the AI to infer borrower risk profile from industry benchmarks alone", "is_best": False},
        ],
        [
            {"label": "Limit the prompt to strategic context; exclude personally identifiable borrower details", "is_best": True},
            {"label": "Include the borrower's location since it is publicly registered information", "is_best": False},
            {"label": "Provide the AI with the credit officer's internal risk assessment for context", "is_best": False},
        ],
        [
            {"label": "Abstract relationship details, prompt with constraints, then verify every AI output claim", "is_best": True},
            {"label": "Share internal credit memos since they are not client-facing documents", "is_best": False},
            {"label": "Ask the AI to generate a risk summary without providing any borrower background", "is_best": False},
        ],
    ],

    "uw_c5_data_decision": [
        None,
        [
            {"label": "Frame the prompt with abstracted financial context and a specific analytical question", "is_best": True},
            {"label": "Upload the financial statements directly for the AI to analyse", "is_best": False},
            {"label": "Ask the AI for a credit recommendation without providing any supporting data", "is_best": False},
        ],
        [
            {"label": "Validate AI-generated ratio interpretations against the source financial statements", "is_best": True},
            {"label": "Accept AI ratio analysis if it aligns with your preliminary assessment", "is_best": False},
            {"label": "Ask the AI to highlight its own errors; use the corrected version directly", "is_best": False},
        ],
        [
            {"label": "Treat AI output as a hypothesis that requires independent verification before the credit memo", "is_best": True},
            {"label": "Use AI analysis directly in the credit memo with an AI-generated caveat", "is_best": False},
            {"label": "Accept the output if it falls within standard industry benchmarks", "is_best": False},
        ],
    ],

    "uw_c6_augmented_comm": [
        None,
        [
            {"label": "Specify audience, tone, purpose, and explicit confidentiality constraints in the prompt", "is_best": True},
            {"label": "Ask the AI to write the memo and apply compliance language afterwards", "is_best": False},
            {"label": "Use the AI draft if it matches the standard memo template structure", "is_best": False},
        ],
        [
            {"label": "Review every AI-drafted communication for accuracy, tone, and confidentiality before issuing", "is_best": True},
            {"label": "Send the draft if no obvious factual errors are present", "is_best": False},
            {"label": "Have a junior analyst spot-check the AI output before distribution", "is_best": False},
        ],
        [
            {"label": "Constrain the prompt to prevent fabricated terms, then verify every factual statement", "is_best": True},
            {"label": "Inform the AI the memo is confidential; rely on it to avoid sensitive disclosures", "is_best": False},
            {"label": "Only verify sections of the memo that will be seen by external parties", "is_best": False},
        ],
    ],

    "uw_c7_capstone": [
        None,
        [
            {"label": "Apply SAFE steps, define deliverable and constraints, then verify all AI outputs", "is_best": True},
            {"label": "Use the most capable model to reduce verification effort", "is_best": False},
            {"label": "Skip abstraction for internal-only documents to speed up the workflow", "is_best": False},
        ],
        [
            {"label": "Flag any AI-generated content that cannot be traced to a source document", "is_best": True},
            {"label": "Accept hedged AI language as sufficient evidence of appropriate caution", "is_best": False},
            {"label": "Use AI summaries that match your own recollection of the credit file", "is_best": False},
        ],
        [
            {"label": "Position AI as a drafting assistant requiring full human review before any credit use", "is_best": True},
            {"label": "Delegate AI output verification to the most junior team member", "is_best": False},
            {"label": "Apply full review to external documents; use AI output directly for internal ones", "is_best": False},
        ],
    ],

    # ── AN ──────────────────────────────────────────────────────────────────
    "an_c1_responsible_ai": [
        None,
        [
            {"label": "Abstract all client-specific identifiers and use approved AI environments only", "is_best": True},
            {"label": "Remove the client name; retain financial figures to preserve analytical accuracy", "is_best": False},
            {"label": "Use consumer AI for quick analyses but avoid saving or sharing the outputs", "is_best": False},
        ],
        [
            {"label": "Strip all re-identification signals — company, location, niche deal terms — before prompting", "is_best": True},
            {"label": "Keep sector benchmarks in the prompt since they are publicly available", "is_best": False},
            {"label": "Add a confidentiality disclaimer at the top of the prompt", "is_best": False},
        ],
        [
            {"label": "Apply all four SAFE steps and add output constraints to prevent AI from fabricating data", "is_best": True},
            {"label": "Retain the client's sub-sector since it is less specific than the company name", "is_best": False},
            {"label": "Route the prompt through a manager before using the AI output", "is_best": False},
        ],
    ],

    "an_c2_strategic_prompting": [
        None,
        [
            {"label": "Include role, abstracted context, specific deliverable, and output constraints", "is_best": True},
            {"label": "Let the AI choose the analysis format based on its training", "is_best": False},
            {"label": "Send several narrow prompts and stitch the outputs together manually", "is_best": False},
        ],
        [
            {"label": "Add explicit constraints to prevent the AI from inventing benchmarks or figures", "is_best": True},
            {"label": "Trust the AI to stay factual when you describe the analytical goal clearly", "is_best": False},
            {"label": "Ask the AI to flag its assumptions; approve flagged items as reviewed", "is_best": False},
        ],
        [
            {"label": "Iterate the prompt by tightening constraints each time an issue is discovered", "is_best": True},
            {"label": "Accept the first output that looks structurally sound", "is_best": False},
            {"label": "Ask the AI to critique and rewrite its own response", "is_best": False},
        ],
    ],

    "an_c3_critical_eval": [
        None,
        [
            {"label": "Trace every AI-generated figure back to its source before using it in analysis", "is_best": True},
            {"label": "Flag only figures that differ significantly from your independent estimate", "is_best": False},
            {"label": "Accept AI output that uses hedging language like 'approximately' or 'estimated'", "is_best": False},
        ],
        [
            {"label": "Treat unverifiable AI claims as hallucinations until independently confirmed", "is_best": True},
            {"label": "Ask the AI to name its source; use the output if the source name is plausible", "is_best": False},
            {"label": "Remove only the claims most likely to be challenged in a presentation", "is_best": False},
        ],
        [
            {"label": "Replace all fabricated content with your own verified language and document the substitution", "is_best": True},
            {"label": "Publish AI output with a note that figures are preliminary and subject to change", "is_best": False},
            {"label": "Re-prompt with stricter instructions and publish the next output as verified", "is_best": False},
        ],
    ],

    "an_c4_relationship_intel": [
        None,
        [
            {"label": "Provide abstracted client context and a specific relationship intelligence deliverable", "is_best": True},
            {"label": "Feed all CRM interaction logs to the AI and ask for a relationship summary", "is_best": False},
            {"label": "Ask the AI to infer client priorities from publicly available filings only", "is_best": False},
        ],
        [
            {"label": "Provide only the strategic context needed; exclude personally identifiable details", "is_best": True},
            {"label": "Include names of client contacts to get more targeted recommendations", "is_best": False},
            {"label": "Let the AI infer sentiment from financial results without qualitative context", "is_best": False},
        ],
        [
            {"label": "Abstract relationship data, apply SAFE steps, then verify all AI-generated insights", "is_best": True},
            {"label": "Share meeting notes verbatim because they are marked internal-only", "is_best": False},
            {"label": "Generate relationship insights without providing context to keep the prompt simple", "is_best": False},
        ],
    ],

    "an_c5_data_decision": [
        None,
        [
            {"label": "Provide abstracted data context, a specific analytical question, and an output format", "is_best": True},
            {"label": "Share a screenshot of the dashboard and ask the AI to interpret it", "is_best": False},
            {"label": "Ask for a strategic recommendation without providing any underlying data", "is_best": False},
        ],
        [
            {"label": "Cross-check every AI-generated insight against the source data before presenting", "is_best": True},
            {"label": "Use AI insights directly if they align with your overall view of the data", "is_best": False},
            {"label": "Ask the AI to self-flag uncertain insights; use the rest without review", "is_best": False},
        ],
        [
            {"label": "Treat all AI outputs as hypotheses requiring independent validation before presentation", "is_best": True},
            {"label": "Include AI analysis in client-facing slides with an 'AI-generated' label", "is_best": False},
            {"label": "Accept outputs that fall within widely published industry benchmarks", "is_best": False},
        ],
    ],

    "an_c6_augmented_comm": [
        None,
        [
            {"label": "Specify audience, tone, deliverable, and explicit confidentiality guardrails in the prompt", "is_best": True},
            {"label": "Ask the AI to draft the report and refine the tone yourself afterwards", "is_best": False},
            {"label": "Use the AI draft if it follows the standard report structure", "is_best": False},
        ],
        [
            {"label": "Review AI-drafted communications for accuracy, tone, and confidentiality before sending", "is_best": True},
            {"label": "Send the draft if no critical factual errors are visible on first read", "is_best": False},
            {"label": "Ask a peer to review the AI output before distribution", "is_best": False},
        ],
        [
            {"label": "Constrain the prompt to prevent fabrication, then verify every factual claim", "is_best": True},
            {"label": "Mark the report as AI-drafted to signal that readers should verify claims themselves", "is_best": False},
            {"label": "Only verify sections visible to external stakeholders", "is_best": False},
        ],
    ],

    "an_c7_capstone": [
        None,
        [
            {"label": "Apply SAFE abstractions, define deliverable and constraints, verify all AI outputs", "is_best": True},
            {"label": "Use a more capable model to reduce the need for manual output verification", "is_best": False},
            {"label": "Skip abstraction for internal analysis to accelerate delivery timelines", "is_best": False},
        ],
        [
            {"label": "Flag any AI content that cannot be traced to an authoritative source document", "is_best": True},
            {"label": "Accept hedged AI language as evidence of appropriate analytical caution", "is_best": False},
            {"label": "Use AI outputs that match your own initial reading of the data", "is_best": False},
        ],
        [
            {"label": "Treat AI as a drafting aid requiring complete human validation before any client use", "is_best": True},
            {"label": "Assign AI output verification to the most junior analyst on the team", "is_best": False},
            {"label": "Apply full review to client deliverables; accept AI output for internal documents", "is_best": False},
        ],
    ],

    # ── MK ──────────────────────────────────────────────────────────────────
    "mk_c1_responsible_ai": [
        None,
        [
            {"label": "Specify audience, plain language requirement, length, and a no-fabrication constraint", "is_best": True},
            {"label": "Ask the AI to choose the best format and length for the content type", "is_best": False},
            {"label": "Generate a first draft and refine the constraint later based on the output", "is_best": False},
        ],
        [
            {"label": "Treat any unverifiable AI statistic as a potential hallucination until confirmed", "is_best": True},
            {"label": "Accept statistics the AI presents with a citation, even if unverified", "is_best": False},
            {"label": "Flag only statistics that seem implausibly high or low", "is_best": False},
        ],
        [
            {"label": "Replace fabricated content with verified language and add guardrails to the prompt", "is_best": True},
            {"label": "Publish the content with a note that statistics are AI-generated and may vary", "is_best": False},
            {"label": "Re-prompt with the instruction to avoid statistics and publish the next version", "is_best": False},
        ],
    ],

    "mk_c2_strategic_prompting": [
        None,
        [
            {"label": "Include audience, objective, format, tone, and explicit output constraints in the prompt", "is_best": True},
            {"label": "Let the AI decide the best content strategy based on the product description", "is_best": False},
            {"label": "Use multiple prompts for different content sections and combine them manually", "is_best": False},
        ],
        [
            {"label": "Add constraints preventing the AI from generating claims you cannot verify", "is_best": True},
            {"label": "Trust the AI to stay on-brand when you describe the product accurately", "is_best": False},
            {"label": "Ask the AI to flag its own uncertain claims; accept the rest as verified", "is_best": False},
        ],
        [
            {"label": "Refine the prompt iteratively, tightening constraints each time an issue appears", "is_best": True},
            {"label": "Accept the first output that matches the word count and tone requirements", "is_best": False},
            {"label": "Ask the AI to improve its own draft based on brand guidelines you provide", "is_best": False},
        ],
    ],

    "mk_c3_critical_eval": [
        None,
        [
            {"label": "Cross-reference the AI statistic against the original brief and external sources", "is_best": True},
            {"label": "Accept the statistic since it appears with a plausible source name in the AI output", "is_best": False},
            {"label": "Flag the statistic internally but publish to meet the deadline; correct in a follow-up", "is_best": False},
        ],
        [
            {"label": "Remove the fabricated quote and replace with verified content from the approved brief", "is_best": True},
            {"label": "Keep the quote but change the attribution to a fictional spokesperson", "is_best": False},
            {"label": "Ask the AI to generate a replacement quote that is less likely to be challenged", "is_best": False},
        ],
        [
            {"label": "Remove all confidential project references and add prompt guardrails to prevent recurrence", "is_best": True},
            {"label": "Replace the project code name only; retain the pilot client reference for credibility", "is_best": False},
            {"label": "Publish the content with the pilot reference since it has not been formally announced yet", "is_best": False},
        ],
    ],

    "mk_c4_relationship_intel": [
        None,
        [
            {"label": "Provide abstracted audience insights and a specific messaging deliverable with guardrails", "is_best": True},
            {"label": "Share the full customer research report for the AI to analyse and summarise", "is_best": False},
            {"label": "Ask the AI to infer audience preferences from publicly available competitor content", "is_best": False},
        ],
        [
            {"label": "Include only aggregate audience signals; exclude personally identifiable respondent details", "is_best": True},
            {"label": "Include named customer quotes from research since they add authenticity", "is_best": False},
            {"label": "Let the AI generate audience personas using its own training data as the base", "is_best": False},
        ],
        [
            {"label": "Abstract all audience data, apply SAFE steps, then verify AI messaging against brand guidelines", "is_best": True},
            {"label": "Share verbatim survey responses since they are anonymised at collection", "is_best": False},
            {"label": "Generate messaging without audience context to keep the prompt simple", "is_best": False},
        ],
    ],

    "mk_c5_data_decision": [
        None,
        [
            {"label": "Frame the prompt with abstracted campaign metrics, a specific question, and output format", "is_best": True},
            {"label": "Share the raw analytics export for the AI to identify patterns", "is_best": False},
            {"label": "Ask for content recommendations without providing any performance data", "is_best": False},
        ],
        [
            {"label": "Verify every AI-generated performance insight against the source analytics before presenting", "is_best": True},
            {"label": "Use AI insights directly if they support the narrative you had already planned", "is_best": False},
            {"label": "Ask the AI to self-flag uncertain insights; use the rest without further review", "is_best": False},
        ],
        [
            {"label": "Treat AI outputs as first-pass hypotheses requiring independent validation before use", "is_best": True},
            {"label": "Include AI analysis in client reports with an 'AI-generated' attribution label", "is_best": False},
            {"label": "Accept outputs that fall within industry benchmark ranges without further verification", "is_best": False},
        ],
    ],

    "mk_c6_augmented_comm": [
        None,
        [
            {"label": "Specify channel, audience, tone, objective, and explicit brand and accuracy constraints", "is_best": True},
            {"label": "Ask the AI to generate the content and adjust the brand voice yourself afterwards", "is_best": False},
            {"label": "Use the AI draft if it meets the word count and matches the channel format", "is_best": False},
        ],
        [
            {"label": "Review every AI-drafted communication for accuracy, tone, and compliance before publishing", "is_best": True},
            {"label": "Publish the draft if it passes a grammar check and no obvious errors are present", "is_best": False},
            {"label": "Ask a junior team member to spot-check the AI output before it goes live", "is_best": False},
        ],
        [
            {"label": "Constrain the prompt to prevent fabricated claims, then verify every factual statement", "is_best": True},
            {"label": "Mark the content as AI-generated so audiences understand it may contain inaccuracies", "is_best": False},
            {"label": "Only verify sections that include statistics or named third parties", "is_best": False},
        ],
    ],

    "mk_c7_capstone": [
        None,
        [
            {"label": "Apply SAFE steps, specify deliverable and constraints, verify all AI outputs against sources", "is_best": True},
            {"label": "Use the most capable model available to reduce the need for manual verification", "is_best": False},
            {"label": "Skip confidentiality checks for internal campaign briefs to hit the deadline", "is_best": False},
        ],
        [
            {"label": "Flag any AI-generated content that cannot be traced to an approved source or brief", "is_best": True},
            {"label": "Accept AI language that hedges with phrases like 'research suggests' without further review", "is_best": False},
            {"label": "Use AI outputs that align with your existing campaign narrative", "is_best": False},
        ],
        [
            {"label": "Position AI as a drafting assistant requiring full human review before any public use", "is_best": True},
            {"label": "Delegate AI output verification to the content coordinator to save senior time", "is_best": False},
            {"label": "Apply full review to media-facing content; accept AI output for internal briefs", "is_best": False},
        ],
    ],
}


def main() -> None:
    with open(SCENARIOS_PATH, encoding="utf-8") as f:
        data: dict = json.load(f)

    updated = 0
    missing = []

    for scenario_id, scenario in data.items():
        if scenario_id not in MCQ_DATA:
            missing.append(scenario_id)
            continue

        options = MCQ_DATA[scenario_id]
        scenario["task_modes"] = ["open", "mcq", "mcq", "mcq"]
        scenario["task_mcq_options"] = options
        updated += 1

    if missing:
        print(f"WARNING: no MCQ data for {len(missing)} scenarios: {missing}")

    print(f"Updated {updated} scenarios.")

    with open(SCENARIOS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved → {SCENARIOS_PATH}")


if __name__ == "__main__":
    main()
