#!/usr/bin/env node
/**
 * translate-zh.js — Translate EN pillar JSONs to ZH using Databricks Claude
 *
 * Usage:
 *   node scripts/translate-zh.js [pillar_name|all]
 *
 * Examples:
 *   node scripts/translate-zh.js p1_foundation
 *   node scripts/translate-zh.js all
 *
 * Requires:
 *   DATABRICKS_TOKEN — Databricks PAT (personal access token)
 *
 * If you get SSL errors due to corporate proxy, run with:
 *   NODE_TLS_REJECT_UNAUTHORIZED=0 node scripts/translate-zh.js all
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { jsonrepair } = require('jsonrepair');

// ─── Config ───────────────────────────────────────────────────────────────────

const ROOT = path.join(__dirname, '..');
const DATABRICKS_HOST = 'https://adb-2717931942638877.17.azuredatabricks.net';
const MODEL = 'databricks-claude-opus-4-6';

// Execution order per plan: P1 → P2 → P5 → P3 → P4 → P6 → capstone → diagnostic
const PILLAR_SEQUENCE = [
  'p1_foundation',
  'p2_prompting',
  'p5_workflow',
  'p3_tool_fluency',
  'p4_configuration',
  'p6_agentic',
  'capstone',
  'diagnostic_pillar',
];

// diagnostic_pillar lives at content/diagnostic_pillar.json (not in pillars/)
// and its ZH version goes to content/zh/diagnostic_pillar.json (not in pillars/)
const DIAGNOSTIC_PILLAR = 'diagnostic_pillar';

// ─── System Prompt ────────────────────────────────────────────────────────────

const SYSTEM_PROMPT = `You are a professional educational content localizer specializing in Simplified Chinese for the Chinese professional market. You are working on AI Hero Academy — a B2C 7-day AI skills program targeting job seekers, mid-career professionals, and new graduates in China.

Your task: translate and culturally adapt one pillar JSON file from English to Simplified Chinese.

---

## CRITICAL RULES — READ BEFORE STARTING

### 1. JSON schema is sacred
Output a single valid JSON object. No markdown fences, no explanation text, no comments.
Every key must be identical to the EN original. Never add, remove, or rename keys.

### 2. Template parameters: preserve exactly
These placeholder strings must appear unchanged — do not translate or modify:
  {declared_role}  {declared_industry}  {daily_work_desc}  {day_number}
  {daily_work_tasks}  {org_type}  {case_type}  {scenario_text}
  {task_context}  {fictional_entity}

### 3. Technical terms: always in English
Never translate these, even inside Chinese sentences:
  LLM  GPT  Claude  Gemini  ChatGPT  Grok  Mistral
  RAG  CoT  JSON  API  MCP  SDK  OAuth
  system prompt  temperature  token  fine-tuning  embedding
  Cursor  Windsurf  n8n  Zapier  GitHub Copilot  Notion AI
  M365 Copilot  Google Workspace AI  Midjourney  DALL-E  Runway
  ElevenLabs  Perplexity  NotebookLM

### 4. Framework acronyms: keep in English
MAPS  CRAF  CAST  BRIEF  CREW  TRACE  SAFE  VERIFY

On first occurrence in reading.concept_text only, add a brief ZH gloss in parentheses:
"MAPS框架（模型行为・局限意识・实际应用・安全基准）"
Do NOT spell out the acronym again after the first occurrence.

### 5. Quotation marks inside JSON string values
When quoting or emphasizing text WITHIN a Chinese JSON string value, always use Chinese bracket quotes 「 and 」 (e.g., 「这是引用文本」) — NEVER use ASCII double-quote " characters inside a string value, as they break JSON validity.

### 6. Identifiers: never translate
pillar_id  pillar_slug  task_id  item_id  type  correct_answer
score_weight  day_number  estimated_minutes  perishable_content
last_updated  artifact_type  the framework value (e.g. "MAPS")

---

## TRANSLATION QUALITY BAR

You are localizing educational content — not machine translating.

Register: Simplified Chinese (Mainland China). Professional, warm, direct. Like a knowledgeable
coach speaking to a motivated professional. NOT 公文体. NOT academic.

The EN originals read like a sharp LinkedIn learning post. Match that energy in ZH.

Style reference — write in the style of leading Chinese AI educational content (e.g. Datawhale,
phodal/prompt-patterns). Key characteristics:
- Natural mix of Chinese prose and English technical terms
- Insert a space between Chinese characters and English words/numbers: "使用 LLM 生成内容"
- Direct, structured explanations using numbered lists and clear headings
- Coach voice: knowledgeable but never condescending
- Avoid 的 stacking and passive constructions — write active, punchy sentences

Accuracy: Do not simplify or soften. ZH readers deserve the same conceptual depth.
Rubric levels must preserve their scoring intent — level 4 = mastery, level 0 = failure to engage.
Quiz explanations: translate the full reasoning chain, not a summary.

---

## CULTURAL ADAPTATION (required)

### Names
Replace Western names with plausible Simplified Chinese names:
  Nadia → 雯静 or 晓丹
  Marcus → 志强 or 明浩
  David, Sarah, etc. → common Chinese equivalents
  "James Chen" → keep (already Chinese)

### Fictional companies
Replace Western fictional companies with ZH equivalents matching the industry:
  Meridian Dynamics → 远景咨询 or 启明动力
  Aurora → 朝霞科技
  Crestwood → 松柏集团
  Apex Trade Finance → 顶峰贸易金融
Do NOT use real Chinese companies (Alibaba, Tencent, Huawei).

### Legal and case references
The Mata v. Avianca case (lawyer submits AI-hallucinated citations to US federal court):
Adapt to a Chinese legal context — e.g., a corporate lawyer submitting AI-fabricated case law
citations in a commercial dispute, or a compliance team relying on AI-invented regulatory
provisions. Preserve the lesson: AI-hallucinated professional content causes real consequences.

### Regulatory terms
Replace GDPR with 个人信息保护法（PIPL） where relevant.

### Currency
Convert USD to approximate CNY: $47,000 → 约34万元人民币; $200 → 约1,500元

---

## SECTION GUIDANCE

reading.concept_text — Long-form prose. Preserve bold headings (**粗体**) and list structure.
reading.good_example / anti_pattern — Localize names, companies, currency. Preserve story arc.
reading.takeaway — Translate crisply. No filler.
practice.scenario_template — Translate prose; leave {params} untouched.
practice.tasks[].prompt_template — Translate all prose + quoted examples. Preserve markdown
  (--- dividers, *italics*, **bold**). Leave {params} untouched.
practice.tasks[].rubric — Translate each level precisely. Scoring logic must be identical.
quiz.items — Translate question, all options (A/B/C/D), and explanation. The correct_answer
  key value (e.g. "C") stays as-is — only the option text translates.
build_artifact.prompt — Learner-facing. Translate. Leave {params} untouched.
build_artifact.coach_closing_prompt — AI coach instruction (not shown to learner). Translate
  fully. Coach behaviors (what to probe, when to close, what NOT to do) must be preserved.

---

## OUTPUT FORMAT

Output the complete ZH JSON object starting with { and ending with }.
Nothing before {. Nothing after }. No markdown fences. No explanation text.

Now translate the following EN pillar JSON:`;

// ─── Helpers ──────────────────────────────────────────────────────────────────

function extractJson(raw) {
  const first = raw.indexOf('{');
  const last = raw.lastIndexOf('}');
  if (first === -1 || last === -1 || last <= first) {
    throw new Error('No JSON object found in response');
  }
  return raw.slice(first, last + 1);
}

/**
 * Fix unescaped double-quotes inside JSON string values.
 * The Claude model sometimes uses "quoted text" inside Chinese strings without escaping.
 * This function parses char-by-char, tracking whether we're inside a JSON string,
 * and escapes any `"` that isn't a legitimate string delimiter.
 */
function fixUnescapedQuotes(jsonStr) {
  let result = '';
  let inString = false;
  let i = 0;

  while (i < jsonStr.length) {
    const ch = jsonStr[i];
    const code = jsonStr.charCodeAt(i);

    if (!inString) {
      if (ch === '"') {
        inString = true;
        result += ch;
      } else {
        result += ch;
      }
      i++;
    } else {
      if (ch === '\\') {
        // Escaped sequence — copy both chars as-is
        result += ch + (jsonStr[i + 1] || '');
        i += 2;
      } else if (code === 10 || code === 13) {
        // Literal newline inside a string — escape it
        result += code === 13 ? '\\r' : '\\n';
        i++;
      } else if (ch === '"') {
        // Determine if this is a legitimate closing quote or an inner quote.
        // After a real closing quote, the next non-whitespace char must be one of: : , } ] or EOF
        let j = i + 1;
        while (j < jsonStr.length && (jsonStr[j] === ' ' || jsonStr[j] === '\t' ||
               jsonStr.charCodeAt(j) === 10 || jsonStr.charCodeAt(j) === 13)) {
          j++;
        }
        const nextCh = j < jsonStr.length ? jsonStr[j] : '\0';
        if (':,}]'.includes(nextCh) || j >= jsonStr.length) {
          // Legitimate closing quote
          inString = false;
          result += ch;
        } else {
          // Inner unescaped quote — escape it
          result += '\\"';
        }
        i++;
      } else {
        result += ch;
        i++;
      }
    }
  }
  return result;
}

function validateTranslation(enObj, zhObj, pillarName) {
  let errors = 0;
  const warnings = [];

  function checkKeys(a, b, path) {
    for (const k of Object.keys(a)) {
      if (!(k in b)) {
        console.error(`  MISSING KEY: ${path}.${k}`);
        errors++;
      } else if (typeof a[k] === 'object' && a[k] !== null && !Array.isArray(a[k])) {
        checkKeys(a[k], b[k], `${path}.${k}`);
      }
    }
  }
  checkKeys(enObj, zhObj, 'root');

  const enStr = JSON.stringify(enObj);
  const zhStr = JSON.stringify(zhObj);

  // Check {param} slots preserved
  const params = [...new Set([...enStr.matchAll(/\{[a-z_]+\}/g)].map(m => m[0]))];
  for (const p of params) {
    const re = new RegExp(p.replace('{', '\\{').replace('}', '\\}'), 'g');
    const ec = (enStr.match(re) || []).length;
    const zc = (zhStr.match(re) || []).length;
    if (ec !== zc) {
      console.error(`  PARAM MISMATCH ${p}: EN=${ec} ZH=${zc}`);
      errors++;
    }
  }

  // Warn on possibly-translated EN terms
  const mustKeep = ['LLM', 'JSON', 'API', 'system prompt', 'temperature', 'MAPS', 'CRAF', 'CAST', 'BRIEF', 'CREW'];
  for (const t of mustKeep) {
    if (enStr.includes(t) && !zhStr.includes(t)) {
      warnings.push(`POSSIBLE TRANSLATED TERM (check): ${t}`);
    }
  }

  return { errors, warnings };
}

// ─── Core translation ─────────────────────────────────────────────────────────

async function translatePillar(pillarName) {
  const token = process.env.DATABRICKS_TOKEN;
  if (!token) {
    throw new Error('DATABRICKS_TOKEN environment variable is not set');
  }

  // diagnostic_pillar lives at content/diagnostic_pillar.json, not inside pillars/
  const isDiagnostic = pillarName === DIAGNOSTIC_PILLAR;
  const enPath = isDiagnostic
    ? path.join(ROOT, 'content', `${pillarName}.json`)
    : path.join(ROOT, 'content/pillars', `${pillarName}.json`);
  const zhDir = isDiagnostic
    ? path.join(ROOT, 'content/zh')
    : path.join(ROOT, 'content/zh/pillars');
  const zhPath = path.join(zhDir, `${pillarName}.json`);

  if (!fs.existsSync(enPath)) {
    throw new Error(`EN source not found: ${enPath}`);
  }

  // Skip if ZH file already exists and is valid JSON
  if (fs.existsSync(zhPath)) {
    try {
      JSON.parse(fs.readFileSync(zhPath, 'utf8'));
      console.log(`[${pillarName}] Already translated — skipping.`);
      return;
    } catch (_) {
      console.warn(`[${pillarName}] Existing ZH file invalid — re-translating.`);
    }
  }

  fs.mkdirSync(zhDir, { recursive: true });

  const enContent = fs.readFileSync(enPath, 'utf8');
  const enObj = JSON.parse(enContent);

  console.log(`\n[${pillarName}] Calling ${MODEL}...`);
  const startMs = Date.now();

  const response = await fetch(
    `${DATABRICKS_HOST}/serving-endpoints/${MODEL}/invocations`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: [
          { role: 'user', content: `${SYSTEM_PROMPT}\n\n${enContent}` },
        ],
        max_tokens: 32000,
      }),
    }
  );

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`API error ${response.status}: ${errText}`);
  }

  const data = await response.json();
  const elapsed = ((Date.now() - startMs) / 1000).toFixed(1);

  const rawContent = data.choices?.[0]?.message?.content;
  if (!rawContent) {
    throw new Error(`Unexpected API response shape: ${JSON.stringify(data)}`);
  }

  console.log(`[${pillarName}] Response received in ${elapsed}s (${rawContent.length} chars)`);

  // Extract and parse JSON
  const jsonStr = extractJson(rawContent);
  let zhObj;
  try {
    zhObj = JSON.parse(jsonStr);
  } catch (parseErr) {
    // Stage 1: fix unescaped inner quotes char-by-char
    console.warn(`  JSON parse error: ${parseErr.message} — attempting quote fix...`);
    try {
      const fixedStr = fixUnescapedQuotes(jsonStr);
      zhObj = JSON.parse(fixedStr);
      console.log(`  Quote fix succeeded.`);
    } catch (fixErr) {
      // Stage 2: jsonrepair as last resort
      console.warn(`  Quote fix failed: ${fixErr.message} — trying jsonrepair...`);
      try {
        const repairedStr = jsonrepair(fixUnescapedQuotes(jsonStr));
        zhObj = JSON.parse(repairedStr);
        console.log(`  jsonrepair succeeded.`);
      } catch (repairErr) {
        const debugPath = path.join(ROOT, `tmp-debug-${pillarName}.txt`);
        fs.writeFileSync(debugPath, rawContent, 'utf8');
        console.error(`  All repair strategies failed: ${repairErr.message}`);
        console.error(`  Raw response saved to: ${debugPath}`);
        throw repairErr;
      }
    }
  }

  // Validate
  console.log(`[${pillarName}] Validating...`);
  const { errors, warnings } = validateTranslation(enObj, zhObj, pillarName);

  for (const w of warnings) {
    console.warn(`  WARN: ${w}`);
  }

  if (errors > 0) {
    throw new Error(`Validation failed with ${errors} error(s) — not saving`);
  }

  // Pretty-print with 2-space indent to match EN files
  fs.writeFileSync(zhPath, JSON.stringify(zhObj, null, 2), 'utf8');
  console.log(`[${pillarName}] ✓ Saved to content/zh/pillars/${pillarName}.json`);
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const arg = process.argv[2] || 'all';

  let targets;
  if (arg === 'all') {
    targets = PILLAR_SEQUENCE;
  } else if (PILLAR_SEQUENCE.includes(arg)) {
    targets = [arg];
  } else {
    console.error(`Unknown pillar: ${arg}`);
    console.error(`Valid values: all, ${PILLAR_SEQUENCE.join(', ')}`);
    process.exit(1);
  }

  console.log(`Translating: ${targets.join(', ')}`);
  console.log(`Model: ${MODEL}`);

  let passed = 0;
  let failed = 0;

  for (const pillar of targets) {
    try {
      await translatePillar(pillar);
      passed++;
    } catch (err) {
      console.error(`[${pillar}] FAILED: ${err.message}`);
      failed++;
      if (targets.length > 1) {
        console.error(`Continuing with next pillar...`);
      }
    }
  }

  console.log(`\nDone: ${passed} passed, ${failed} failed`);
  if (failed > 0) process.exit(1);
}

main().catch(err => {
  console.error('Fatal:', err.message);
  process.exit(1);
});
