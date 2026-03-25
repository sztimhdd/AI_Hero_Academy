#!/usr/bin/env python3
"""
Translate AI Hero Academy content files from English to Simplified Chinese.

Uses the Andrew Ng reflection workflow (translate → reflect → improve) with:
- databricks-claude-sonnet-4-6 at temperature 0.3 / 0.1 / 0.2 per step
- Domain glossary for consistent terminology
- RAG style reference injected into every prompt

Writes translated files to content/zh/{filename}.
For content/i18n/zh.json, overwrites in place.

Usage:
    python scripts/translate_content.py              # all files
    python scripts/translate_content.py --file courses
    python scripts/translate_content.py --dry-run    # print to stdout
    python scripts/translate_content.py --role rm    # filter to one role
"""

import argparse
import json
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Corporate SSL proxy re-signs TLS certs — disable verification for local dev
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests as _requests
_orig_send = _requests.adapters.HTTPAdapter.send
def _patched_send(self, *a, **kw):
    kw["verify"] = False
    return _orig_send(self, *a, **kw)
_requests.adapters.HTTPAdapter.send = _patched_send

from databricks.sdk import WorkspaceClient
from databricks.sdk.config import Config
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole
from tenacity import retry, wait_random_exponential, stop_after_attempt

CONTENT_DIR = Path(__file__).parent.parent / "content"
ZH_DIR = CONTENT_DIR / "zh"
SONNET_ENDPOINT = "databricks-claude-sonnet-4-6"

# ---------------------------------------------------------------------------
# Style reference (RAG)
# ---------------------------------------------------------------------------

_REF_PATH = Path(__file__).parent.parent / "references" / "zh-translation-reference.md"
_REF_DOC = _REF_PATH.read_text(encoding="utf-8")[:3000] if _REF_PATH.exists() else ""

# ---------------------------------------------------------------------------
# Domain glossary
# ---------------------------------------------------------------------------

GLOSSARY = """
# App-specific terms (always use these exactly, no variation)

## Learning platform UI
- "gap map" → "差距图谱"
- "skills profile" → "技能档案"
- "diagnostic" / "skill diagnostic" → "技能测评"
- "AI coach" → "AI辅导员"
- "learning path" → "学习路径"
- "course module" → "学习模块"
- "reading" (sub-module) → "精读"
- "practice" (sub-module) → "实战练习"
- "evaluation" / "quiz" → "综合评估"
- "prompt sandbox" → "提示词沙盒"
- "overview" (module section) → "模块概览"
- "results" (module section) → "评估结果"
- "score" / "scoring" → "评分"
- "domain score" → "领域得分"
- "overall score" → "综合得分"

## Skill level labels (exact match required)
- "Champion" → "卓越级"
- "Proficient" → "精通级"
- "Practitioner" → "实践级"
- "Explorer" → "探索级"
- "Unaware" → "认知前级"

## Six learning domains
- "responsible AI" → "负责任AI"
- "strategic prompting" → "战略性提示"
- "critical evaluation" → "批判性评估"
- "relationship intelligence" → "关系洞察"
- "data decision" → "数据决策"
- "augmented communication" → "增强沟通"

## Job roles
- "relationship manager" / "RM" → "客户经理"
- "underwriter" / "UW" → "核保专员"
- "analyst" / "AN" → "业务分析师"
- "marketing advisor" / "MK" → "市场顾问"
- "project manager" / "PM" → "项目经理"
- "learner" → "学习者"

# AI/technology terms (standard Chinese industry usage from reference materials)

## Core AI concepts
- "large language model" / "LLM" → "大语言模型"
- "prompt engineering" → "提示工程"
- "prompt" (noun) → "提示词"
- "prompt" (verb, as in "to prompt the AI") → "向AI提问" / "引导AI"
- "chain-of-thought" / "CoT" → "思维链"
- "zero-shot" → "零样本"
- "few-shot" → "少样本"
- "fine-tuning" → "微调"
- "in-context learning" → "上下文学习"
- "retrieval-augmented generation" / "RAG" → "检索增强生成"
- "instruction following" → "指令遵循"
- "self-consistency" → "自我一致性"
- "hallucination" → "幻觉"
- "token" (AI token) → "令牌" (keep "token" in technical contexts)
- "context window" → "上下文窗口"
- "temperature" (AI parameter) → "温度参数"
- "inference" (AI inference) → "推理"
- "embedding" → "嵌入向量"
- "knowledge base" → "知识库"

## AI usage patterns
- "AI-assisted" → "AI辅助"
- "AI-generated" → "AI生成"
- "AI tools" → "AI工具"
- "generative AI" → "生成式AI"
- "AI application" → "AI应用"
- "use case" → "应用场景" (not "用例")
- "workflow" → "工作流程"
- "automation" → "自动化"
- "responsible AI use" → "负责任地使用AI"
- "AI governance" → "AI治理"
- "bias" (AI bias) → "偏见" / "偏差"

## Training/learning terms
- "scenario" → "情景" / "场景"
- "rubric" → "评分标准"
- "criterion" / "criteria" → "评估标准"
- "performance task" → "实战任务"
- "micro-task" → "微任务"
- "skill" → "技能"
- "competency" → "能力"
- "capability" → "能力"
- "assessment" → "评估"
- "feedback" → "反馈"
- "coach note" → "辅导建议"
- "best practice" → "最佳实践"
- "anti-pattern" → "反面案例" / "错误模式"
- "good example" → "正面案例"
- "takeaway" → "核心要点"
- "real use case" → "实际应用场景"

# Financial services terms

- "export finance" → "出口金融"
- "financial institution" → "金融机构"
- "relationship manager" → "客户经理"
- "client" / "customer" → "客户"
- "due diligence" → "尽职调查"
- "risk assessment" → "风险评估"
- "compliance" → "合规"
- "stakeholder" → "利益相关方"
- "credit analysis" → "信贷分析"
- "underwriting" → "核保"
- "portfolio" → "投资组合" / "业务组合"
- "transaction" → "交易"
- "deal" (financial deal) → "业务" / "项目"
- "pitch" → "方案陈述"
- "briefing" → "情况简报"
"""

# ---------------------------------------------------------------------------
# Base system prompt (shared across all 3 steps)
# ---------------------------------------------------------------------------

BASE_SYSTEM = """You are a professional Simplified Chinese (简体中文) translator \
for corporate AI training materials in financial services.

Rules:
1. Translate ONLY the text fields specified. Return valid JSON with the same structure.
2. Keep ALL JSON keys, IDs, booleans, numbers, and scoring weights in English as-is.
3. Framework acronyms (SAFE, CRAF, VERIFY, TRACE, STAKE): keep in English.
4. Fictional company names (Meridian, Aurora, Crestwood, Apex, Maple, Northern): keep in English.
5. {placeholder} variables: preserve exactly as-is.
6. Use natural Mainland Chinese business register — avoid literal word-for-word translation.
7. CRITICAL: When quoting a word or phrase within Chinese text, use 「」 or （） instead of " " — never use ASCII double-quote characters inside a JSON string value, as they break JSON.
8. Return ONLY valid JSON — no markdown fences, no commentary."""

# Compact glossary injected into user prompts (not system prompt, to avoid confusion)
GLOSSARY_COMPACT = """Key terms (always use these, no variation):
gap map=差距图谱, skills profile=技能档案, diagnostic=技能测评, AI coach=AI辅导员,
learning path=学习路径, prompt sandbox=提示词沙盒, evaluation=综合评估,
course module=学习模块, domain score=领域得分,
Champion=卓越级, Proficient=精通级, Practitioner=实践级, Explorer=探索级, Unaware=认知前级,
responsible AI=负责任AI, strategic prompting=战略性提示, critical evaluation=批判性评估,
relationship intelligence=关系洞察, data decision=数据决策, augmented communication=增强沟通,
relationship manager=客户经理, underwriter=核保专员, analyst=业务分析师,
marketing advisor=市场顾问, LLM=大语言模型, prompt=提示词, scenario=场景,
rubric=评分标准, use case=应用场景, best practice=最佳实践, anti-pattern=反面案例"""

# ---------------------------------------------------------------------------
# LLM helper
# ---------------------------------------------------------------------------

@retry(wait=wait_random_exponential(min=2, max=20), stop=stop_after_attempt(3))
def _call(w: WorkspaceClient, user_content: str, temp: float) -> str:
    resp = w.serving_endpoints.query(
        name=SONNET_ENDPOINT,
        messages=[
            ChatMessage(role=ChatMessageRole.SYSTEM, content=BASE_SYSTEM),
            ChatMessage(role=ChatMessageRole.USER,
                        content=f"{GLOSSARY_COMPACT}\n\n{user_content}"),
        ],
        temperature=temp,
        max_tokens=8192,
    )
    return resp.choices[0].message.content.strip()


def _strip_fences(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:]).strip()
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0].strip()
    return raw


def _fix_json(raw: str) -> str:
    """Replace unescaped ASCII double-quotes inside JSON string values with 「」."""
    import re
    # Replace " and " curly quotes with Chinese 「 」 (already safe, just normalise)
    raw = raw.replace('\u201c', '「').replace('\u201d', '」')
    return raw


# ---------------------------------------------------------------------------
# Reflection workflow
# ---------------------------------------------------------------------------

def _reflect_improve(w: WorkspaceClient, source_json: str, t1_json: str) -> str:
    """Step 2: critique the initial translation."""
    prompt = f"""Source (English JSON):
<source>
{source_json}
</source>

Initial translation (Chinese JSON):
<translation>
{t1_json}
</translation>

You are a senior Chinese editor reviewing this translation for a corporate AI training \
platform targeting Mainland Chinese financial services professionals.

Evaluate on:
- Accuracy: does it faithfully convey the English meaning?
- Fluency: does it read naturally to a native Mainland Chinese reader?
- Register: appropriately formal (business training, not casual)?
- Glossary: are approved terms used correctly and consistently?
- Idioms: any English idioms translated too literally?

Provide specific, actionable suggestions only. Reference the exact phrases that need \
improvement. Be concise — no general praise."""
    return _call(w, prompt, temp=0.1)


def _improve(w: WorkspaceClient, source_json: str, t1_json: str, critique: str,
             fields: list[str], task_desc: str) -> str:
    """Step 3: apply critique to produce final translation."""
    prompt = f"""Source (English JSON):
<source>
{source_json}
</source>

Initial translation:
<translation>
{t1_json}
</translation>

Editor suggestions:
<suggestions>
{critique}
</suggestions>

Task: {task_desc}
Fields to translate: {', '.join(fields)}

Apply the editor suggestions to produce the final improved translation.
Rules:
- Same JSON structure as the input — same keys, same entry count, same nesting.
- Only edit the translatable text fields; keep all IDs, numbers, booleans unchanged.
- If a suggestion conflicts with the glossary, keep the glossary term.
- Return only valid JSON — no markdown fences, no explanation."""
    return _call(w, prompt, temp=0.2)


def _translate_batch(w: WorkspaceClient, batch: dict | list, fields: list[str],
                     task_desc: str, dry_run: bool = False) -> dict | list:
    """Full 3-step reflection workflow for one batch."""
    source_json = json.dumps(batch, ensure_ascii=False, indent=2)

    # Step 1: initial translation (temp=0.3 for natural first draft)
    t1_prompt = f"""Task: {task_desc}
Fields to translate: {', '.join(fields)}

Input JSON:
{source_json}

Translate the specified fields to Simplified Chinese. Return the complete JSON with \
the same structure."""
    t1_raw = _call(w, t1_prompt, temp=0.3)
    t1_json = _fix_json(_strip_fences(t1_raw))

    if dry_run:
        print("\n--- Step 1 (initial) ---")
        print(t1_json[:500])
        return json.loads(t1_json)

    # Step 2: reflect
    critique = _reflect_improve(w, source_json, t1_json)

    # Step 3: improve
    final_raw = _improve(w, source_json, t1_json, critique, fields, task_desc)
    final_json = _fix_json(_strip_fences(final_raw))

    # Parse with fallback to step-1 result if step-3 output is malformed
    try:
        return json.loads(final_json)
    except json.JSONDecodeError:
        # Try extracting first {...} or [...] block
        import re
        m = re.search(r'(\{.*\}|\[.*\])', final_json, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
        # Fall back to step-1 result
        print("  [WARN] step-3 JSON parse failed, using step-1 result", file=sys.stderr)
        return json.loads(t1_json)


# ---------------------------------------------------------------------------
# Output helper
# ---------------------------------------------------------------------------

def _write_or_print(path: Path, data, dry_run: bool):
    if dry_run:
        print(f"\n--- DRY RUN OUTPUT: {path.name} ---")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])
        print("... (truncated)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# File-specific translators
# ---------------------------------------------------------------------------

def translate_roles(w, dry_run, role_filter):
    src = json.loads((CONTENT_DIR / "roles.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in src.items() if not role_filter or k == role_filter}
    print(f"[roles] Translating {len(entries)} entries...")
    translated = _translate_batch(
        w, entries, ["title", "description"],
        "Translate role titles and descriptions.", dry_run,
    )
    result = {**src, **translated}
    _write_or_print(ZH_DIR / "roles.json", result, dry_run)
    print(f"  ✓ roles.json: {len(translated)} entries")


def translate_domains(w, dry_run, role_filter):
    src = json.loads((CONTENT_DIR / "domains.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in src.items()
               if not role_filter or v.get("role_id") == role_filter}
    keys = list(entries.keys())
    result = dict(src)
    print(f"[domains] Translating {len(entries)} entries one at a time...")
    for i, k in enumerate(keys):
        batch = {k: entries[k]}
        translated = _translate_batch(
            w, batch,
            ["title", "description",
             "level_0_label", "level_0_descriptor",
             "level_1_label", "level_1_descriptor",
             "level_2_label", "level_2_descriptor",
             "level_3_label", "level_3_descriptor",
             "level_4_label", "level_4_descriptor"],
            "Translate domain title, description, and all level label/descriptor fields. "
            "Keep domain_id and role_id unchanged.", dry_run,
        )
        result.update(translated)
        print(f"  ✓ {i+1}/{len(keys)}: {k}")
    _write_or_print(ZH_DIR / "domains.json", result, dry_run)
    print(f"  ✓ domains.json complete")


def translate_courses(w, dry_run, role_filter):
    src = json.loads((CONTENT_DIR / "courses.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in src.items()
               if not role_filter or v.get("role_id") == role_filter}
    keys = list(entries.keys())
    result = dict(src)
    print(f"[courses] Translating {len(entries)} entries in batches of 5...")
    for i in range(0, len(keys), 5):
        batch = {k: entries[k] for k in keys[i:i + 5]}
        translated = _translate_batch(
            w, batch,
            ["title", "tagline", "description", "real_use_case"],
            "Translate course titles, taglines, descriptions, and real_use_case fields.", dry_run,
        )
        result.update(translated)
        print(f"  ✓ batch {i // 5 + 1}/{-(-len(keys) // 5)}")
    _write_or_print(ZH_DIR / "courses.json", result, dry_run)
    print(f"  ✓ courses.json complete")


def translate_i18n(w, dry_run, _role_filter):
    src = json.loads((CONTENT_DIR / "i18n" / "zh.json").read_text(encoding="utf-8"))
    cleaned = {k: v.replace(" [ZH]", "").replace("[ZH]", "") for k, v in src.items()}
    print(f"[i18n/zh] Translating {len(cleaned)} UI string keys...")
    prompt = f"""Task: Translate all values in this UI strings dictionary from English to Simplified Chinese.
Extra rules:
- Keep all {{placeholder}} variables exactly as-is (e.g. {{n}}, {{name}}, {{role}}).
- Keep all arrow/icon characters (→, ←, ✓, ⚡, etc.) exactly as-is.
- Button and nav labels should be concise — Chinese is more compact than English.
- Use the approved glossary terms where applicable.

Input JSON:
{json.dumps(cleaned, ensure_ascii=False, indent=2)}

Return the translated JSON with the same keys."""
    t1_raw = _call(w, prompt, temp=0.3)
    t1_json = _strip_fences(t1_raw)
    if not dry_run:
        critique = _reflect_improve(w, json.dumps(cleaned, ensure_ascii=False, indent=2), t1_json)
        final_raw = _improve(
            w, json.dumps(cleaned, ensure_ascii=False, indent=2), t1_json, critique,
            ["all values"], "Translate UI string values.",
        )
        result = json.loads(_strip_fences(final_raw))
    else:
        result = json.loads(t1_json)
        print("\n--- DRY RUN: i18n/zh.json (first 5 keys) ---")
        for k, v in list(result.items())[:5]:
            print(f"  {k}: {v}")
    assert len(result) == len(src), f"Key count mismatch: {len(result)} vs {len(src)}"
    out_path = CONTENT_DIR / "i18n" / "zh.json"
    _write_or_print(out_path, result, dry_run)
    print(f"  ✓ i18n/zh.json: {len(result)} keys")


def translate_diagnostic_items(w, dry_run, role_filter):
    src = json.loads((CONTENT_DIR / "diagnostic_items.json").read_text(encoding="utf-8"))
    items = [i for i in src if not role_filter or i.get("role_id") == role_filter]
    id_to_idx = {item["item_id"]: idx for idx, item in enumerate(src)}
    result = list(src)
    print(f"[diagnostic_items] Translating {len(items)} items in batches of 5...")
    for i in range(0, len(items), 5):
        batch = items[i:i + 5]
        translated = _translate_batch(
            w, batch,
            ["question_text", "scenario_text", "options[].text",
             "scoring_rubric.criteria[].name", "scoring_rubric.criteria[].description"],
            "Translate diagnostic question text, scenario text, MCQ option text, and rubric "
            "criterion names/descriptions. Keep item_id, role_id, domain_id, item_type, "
            "correct_option, display_order, and all numeric scoring values unchanged.",
            dry_run,
        )
        for t_item in translated:
            idx = id_to_idx.get(t_item.get("item_id"))
            if idx is not None:
                result[idx] = t_item
        print(f"  ✓ batch {i // 5 + 1}/{-(-len(items) // 5)}")
    _write_or_print(ZH_DIR / "diagnostic_items.json", result, dry_run)
    print(f"  ✓ diagnostic_items.json complete")


def translate_reading_content(w, dry_run, role_filter):
    src = json.loads((CONTENT_DIR / "reading_content.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in src.items()
               if not role_filter or k.startswith(role_filter + "_")}
    keys = list(entries.keys())
    result = dict(src)
    print(f"[reading_content] Translating {len(entries)} entries in batches of 3...")
    for i in range(0, len(keys), 3):
        batch = {k: entries[k] for k in keys[i:i + 3]}
        translated = _translate_batch(
            w, batch,
            ["concept_text", "good_example", "anti_pattern", "takeaway"],
            "Translate reading content: concept_text, good_example, anti_pattern, takeaway. "
            "These are educational narrative texts — preserve the instructional tone.", dry_run,
        )
        result.update(translated)
        print(f"  ✓ batch {i // 3 + 1}/{-(-len(keys) // 3)}")
    _write_or_print(ZH_DIR / "reading_content.json", result, dry_run)
    print(f"  ✓ reading_content.json complete")


def translate_evaluation_items(w, dry_run, role_filter):
    src = json.loads((CONTENT_DIR / "evaluation_items.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in src.items()
               if not role_filter or k.startswith(role_filter + "_")}
    keys = list(entries.keys())
    result = dict(src)
    print(f"[evaluation_items] Translating {len(entries)} entries in batches of 3...")
    for i in range(0, len(keys), 3):
        batch = {k: entries[k] for k in keys[i:i + 3]}
        translated = _translate_batch(
            w, batch,
            ["scenario_text", "question_text", "options[].label",
             "scoring_rubric.criteria[].name", "scoring_rubric.criteria[].description"],
            "Translate evaluation scenario text, question text, MCQ option labels, and rubric "
            "criterion names/descriptions. Keep item_id, item_type, correct_option, and all "
            "numeric scoring values unchanged.", dry_run,
        )
        result.update(translated)
        print(f"  ✓ batch {i // 3 + 1}/{-(-len(keys) // 3)}")
    _write_or_print(ZH_DIR / "evaluation_items.json", result, dry_run)
    print(f"  ✓ evaluation_items.json complete")


def translate_practice_scenarios(w, dry_run, role_filter):
    src = json.loads((CONTENT_DIR / "practice_scenarios.json").read_text(encoding="utf-8"))
    entries = {k: v for k, v in src.items()
               if not role_filter or k.startswith(role_filter + "_")}
    keys = list(entries.keys())
    result = dict(src)
    print(f"[practice_scenarios] Translating {len(entries)} entries in batches of 2...")
    for i in range(0, len(keys), 2):
        batch = {k: entries[k] for k in keys[i:i + 2]}
        try:
            translated = _translate_batch(
                w, batch,
                ["scenario_text", "task_1_text", "task_2_text", "task_3_text", "task_4_text",
                 "coach_system_prompt", "task_mcq_options[].label"],
                "Translate scenario text, task texts, coach system prompt, and MCQ option labels. "
                "Keep course_id, task_modes, and all structural/numeric fields unchanged.", dry_run,
            )
        except Exception as e:
            print(f"  [WARN] batch {i // 2 + 1} failed ({e}), retrying individually...")
            translated = {}
            for k in keys[i:i + 2]:
                try:
                    single = _translate_batch(
                        w, {k: entries[k]},
                        ["scenario_text", "task_1_text", "task_2_text", "task_3_text",
                         "task_4_text", "coach_system_prompt", "task_mcq_options[].label"],
                        "Translate scenario text, task texts, coach system prompt.", dry_run,
                    )
                    translated.update(single)
                except Exception as e2:
                    print(f"  [ERROR] {k}: {e2}", file=sys.stderr)
        result.update(translated)
        print(f"  ✓ batch {i // 2 + 1}/{-(-len(keys) // 2)}")
    _write_or_print(ZH_DIR / "practice_scenarios.json", result, dry_run)
    print(f"  ✓ practice_scenarios.json complete")


def translate_atomic_modules(w, dry_run, role_filter):
    """Translate user-visible fields of inline atoms in atomic_modules_v2.json.

    Writes _zh suffix variants back in-place (no separate output file).
    Atoms with source_course_ids are skipped — they delegate to reading_content.
    Filterable by domain via --role (reused as domain prefix, e.g. 'responsible_ai').
    """
    atoms_path = CONTENT_DIR / "atomic_modules_v2.json"
    atoms = json.loads(atoms_path.read_text(encoding="utf-8"))

    # Only translate inline atoms (no source_course_ids) that match the filter
    inline_atoms = [
        a for a in atoms
        if not a.get("source_course_ids")
        and (not role_filter or a.get("domain", "").startswith(role_filter))
    ]
    print(f"[atomic_modules] {len(inline_atoms)} inline atoms to translate (of {len(atoms)} total)...")

    # Build atom_id→index map for in-place update
    atom_index = {a["atom_id"]: i for i, a in enumerate(atoms)}

    # Process in batches of 2
    for b in range(0, len(inline_atoms), 2):
        batch_atoms = inline_atoms[b:b + 2]
        # Flatten to a single dict per atom_id: all translatable text fields
        batch: dict = {}
        for a in batch_atoms:
            r = a.get("reading") or {}
            p = a.get("practice") or {}
            tasks = p.get("task_templates") or []
            batch[a["atom_id"]] = {
                "title": a.get("title", ""),
                "concept_text": r.get("concept_text", ""),
                "good_example": r.get("good_example", ""),
                "anti_pattern": r.get("anti_pattern", ""),
                "takeaway": r.get("takeaway", ""),
                "scenario_template": p.get("scenario_template", ""),
                "task_0": tasks[0]["text_template"] if len(tasks) > 0 else "",
                "task_1": tasks[1]["text_template"] if len(tasks) > 1 else "",
                "task_2": tasks[2]["text_template"] if len(tasks) > 2 else "",
                "task_3": tasks[3]["text_template"] if len(tasks) > 3 else "",
            }

        fields = [
            "title", "concept_text", "good_example", "anti_pattern", "takeaway",
            "scenario_template", "task_0", "task_1", "task_2", "task_3",
        ]
        desc = (
            "Translate atom reading content, practice scenario, and task prompts for an "
            "AI skills learning platform. Keep {placeholder} tokens unchanged. "
            "Preserve bold **text** and markdown formatting."
        )
        try:
            translated = _translate_batch(w, batch, fields, desc, dry_run)
        except Exception as e:
            print(f"  [WARN] batch {b // 2 + 1} failed ({e}), retrying individually...")
            translated = {}
            for a in batch_atoms:
                try:
                    single = _translate_batch(w, {a["atom_id"]: batch[a["atom_id"]]}, fields, desc, dry_run)
                    translated.update(single)
                except Exception as e2:
                    print(f"  [ERROR] {a['atom_id']}: {e2}", file=sys.stderr)

        if dry_run:
            print(json.dumps(translated, ensure_ascii=False, indent=2)[:800])
            print("...")
            continue

        # Merge _zh fields back into atoms list
        for a in batch_atoms:
            aid = a["atom_id"]
            if aid not in translated:
                continue
            tr = translated[aid]
            idx = atom_index[aid]
            atoms[idx]["title_zh"] = tr.get("title", "")
            r = atoms[idx].setdefault("reading", {})
            r["concept_text_zh"] = tr.get("concept_text", "")
            r["good_example_zh"] = tr.get("good_example", "")
            r["anti_pattern_zh"] = tr.get("anti_pattern", "")
            r["takeaway_zh"] = tr.get("takeaway", "")
            p = atoms[idx].setdefault("practice", {})
            p["scenario_template_zh"] = tr.get("scenario_template", "")
            task_zh_vals = [tr.get(f"task_{n}", "") for n in range(4)]
            for n, task in enumerate(p.get("task_templates") or []):
                if n < len(task_zh_vals):
                    task["text_template_zh"] = task_zh_vals[n]

        print(f"  batch {b // 2 + 1}/{-(-len(inline_atoms) // 2)} done")

    if not dry_run:
        atoms_path.write_text(json.dumps(atoms, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  atomic_modules_v2.json updated in place")


# ---------------------------------------------------------------------------
# File registry + main
# ---------------------------------------------------------------------------

FILE_MAP = {
    "roles": translate_roles,
    "domains": translate_domains,
    "courses": translate_courses,
    "i18n": translate_i18n,
    "diagnostic_items": translate_diagnostic_items,
    "reading_content": translate_reading_content,
    "evaluation_items": translate_evaluation_items,
    "practice_scenarios": translate_practice_scenarios,
    "atomic_modules": translate_atomic_modules,
}

FILE_ORDER = [
    "roles", "domains", "courses", "i18n",
    "diagnostic_items", "reading_content", "evaluation_items", "practice_scenarios",
    "atomic_modules",
]


def main():
    parser = argparse.ArgumentParser(description="Translate content files to Simplified Chinese")
    parser.add_argument("--file", choices=list(FILE_MAP.keys()), help="Translate only this file")
    parser.add_argument("--dry-run", action="store_true", help="Print output, do not write")
    parser.add_argument("--role", help="Filter to one role (rm, uw, an, mk)")
    args = parser.parse_args()

    w = WorkspaceClient(config=Config(
        host=os.environ.get("DATABRICKS_HOST", "https://adb-2717931942638877.17.azuredatabricks.net"),
        token=os.environ.get("DATABRICKS_TOKEN"),
        auth_type="pat",
        http_timeout_seconds=300,
    ))
    files_to_run = [args.file] if args.file else FILE_ORDER

    for name in files_to_run:
        print(f"\n{'='*60}")
        print(f"Translating: {name}")
        print(f"{'='*60}")
        try:
            FILE_MAP[name](w, args.dry_run, args.role)
        except Exception as e:
            import traceback
            print(f"\n[ERROR] {name}: {e}", file=sys.stderr)
            traceback.print_exc()
            print("Continuing with next file...")

    print("\n\nAll done.")


if __name__ == "__main__":
    main()
