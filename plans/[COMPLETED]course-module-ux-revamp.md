# Plan: Course Module Page UX Revamp

**Status**: READY TO IMPLEMENT
**Branch**: `feature/course-module-ux`
**Scope**: `pages/04_Course_Module.py` + `utils/styles.py` — no other pages touched
**Research basis**: Full code audit (04_Course_Module.py 744 lines, styles.py 812 lines) +
Streamlit 1.54.0 native component docs (Context7) + LMS UX research (March 2026) +
2026 enterprise e-learning UX expert review (received March 2026)

---

## Expert Review Findings (March 2026)

| Finding | Expert verdict | Plan action |
|---------|---------------|-------------|
| Overall SaaS layout (sidebar nav + top stepper) is standard and intuitive | ✅ Keep | No change |
| Semantic color system for callout cards (Green/Red/Blue); dark mode fits AI theme | ✅ Keep | No change |
| Linear "Read → Practice → Quiz" progression; primary CTA follows Z-pattern | ✅ Keep | No change |
| **Text line length spans full viewport on wide monitors** — 120–140 chars/line; optimal is 60–80 | ⚠️ Fix | **CM-7 (new)** |
| Typography monotonic; `**bold**` markers in content never render (stripped by `_md()` hack) | ⚠️ Fix | Addressed by **CM-1** (`_md()` removal restores native markdown bold) |
| Step indicator loses visibility when user scrolls; stepper or action bar should be sticky | ⚠️ Consider | **Deferred to Phase 2** — Streamlit has no native sticky; fragile CSS approach |
| Cards feel flat; glassmorphism / subtle gradient overlays would elevate to 2026 standard | ⚠️ Consider | **Deferred to Phase 2** — CSS conflicts with Streamlit internals |
| AI "co-pilot" side panel for in-reading contextual Q&A | 🆕 New feature | **Out of scope** for this revamp |

---

## Current State Audit

### What already works well (keep unchanged)
- `step_progress_strip()` custom component — clear visual stepper
- `st.chat_message()` for practice coach conversation (NX1 fix)
- `st.success/error/info` for reading callouts (NX9 fix)
- `st.metric()` for module score (NX4 fix)
- `st.progress()` for domain score bar (NX5 fix)
- Design token system in `COLORS` dict + `styles.py` — consistent and WCAG AA
- `render_sidebar()` consistent nav (NAV1 fix)

### Issues identified (ordered by impact)

| ID | Sub-view | Issue | Severity |
|----|----------|-------|----------|
| CM-A | All | `section_header()` custom HTML function used for SCENARIO/TASK labels — fragile inner div/hr HTML | MEDIUM |
| CM-B | Overview | Sub-view is sparse: counter + title + tagline + strip + 1 button. No module description, no time estimates, no domain context visible until you scroll down | MEDIUM |
| CM-C | Reading | `_md()` function (line 247) manually converts `\n→<br>` and `**bold**→<strong>` — bypasses native Streamlit markdown rendering; concept text wrapped in a raw `<div class="reading-concept">` | HIGH |
| CM-D | Reading | No reading section numbers or visual hierarchy between CONCEPT → Good Example → Mistake → Takeaway | LOW |
| CM-E | Practice | Warning banner (line 332) is an amber `st.warning()` that appears _before_ the user types anything — creates anxiety before interaction | MEDIUM |
| CM-F | Practice | Scenario box is always fully visible even after 3+ chat turns — pushes conversation down the page requiring scroll | HIGH |
| CM-G | Practice | No 4-task visual progress strip — only text label "TASK 1 OF 4" in the section header | MEDIUM |
| CM-H | Practice | "Skip this task →" and "Complete Practice Early →" secondary actions appear as prominent buttons alongside primary CTAs — confuses learner about the primary path | MEDIUM |
| CM-I | Evaluation | Question counter (line 572) and domain tag (line 597) use raw `st.markdown(unsafe_allow_html=True)` | LOW |
| CM-J | Evaluation | Performance task "Scenario" label (lines 628–635) uses a 6-line raw HTML block for a one-line label | LOW |
| CM-K | Results | Coach note rendered in `aha-card-accent` HTML card (lines 705–712) — custom HTML in an otherwise native-component sub-view | MEDIUM |
| CM-L | Results | "Your skills profile has been updated" is a raw HTML `<div>` (lines 714–717) — should be `st.success()` or `st.caption()` | LOW |
| CM-M | Results | `st.metric()` shows module score but no comparison with the diagnostic baseline score for this domain — learner can't see progress | MEDIUM |
| CM-N | Reading | Text line length spans full viewport width — 120–140 chars/line on wide monitors causes eye strain; expert review confirms 60–80 chars/line is optimal | HIGH |
| CM-P | Reading | Step progress strip loses visibility when user scrolls through long reading content — no sticky context anchor | MEDIUM |

---

## Proposed UX Improvements

### Task CM-1 — Reading sub-view: remove `_md()` hack; render concept natively

**File**: `pages/04_Course_Module.py` (lines 247–252)

**Problem**: The `_md()` function does manual HTML escaping that conflicts with native markdown and silently breaks for edge cases (e.g. nested bold, links, code blocks).

**Fix**:
1. Delete the `_md()` helper function (lines 247–249)
2. Replace the `<div class="reading-concept">` block with native `st.markdown()`:

```python
# BEFORE:
st.markdown(f'<div class="reading-concept">{_md(reading.get("concept_text",""))}</div>', unsafe_allow_html=True)

# AFTER:
concept_text = reading.get("concept_text", "")
if concept_text:
    with st.container(border=True):
        st.markdown(concept_text)
```

3. Remove `.reading-concept` CSS block from `utils/styles.py` (lines 459–465)

**Why `st.container(border=True)`**: Provides visual framing consistent with the rest of the card design system, without custom CSS.

---

### Task CM-2 — Practice sub-view: collapse scenario after first reply; add task progress strip

**File**: `pages/04_Course_Module.py` (practice section ~lines 294–450)

**Problem CM-F**: Scenario text (often 200–400 chars) stays fully expanded throughout the conversation, pushing the chat history down. After the first coach reply the learner has already read the scenario.

**Fix**: Wrap the scenario in `st.expander()` that auto-collapses once the conversation begins:

```python
scenario_started = len(messages) > 0
with st.expander("📋 Scenario", expanded=(not scenario_started)):
    st.markdown(scenario_html)  # replace the scenario-box div (keep CSS for inner content)
```

**Problem CM-G**: No visual task progress strip.

**Fix**: Render a 4-step strip above the current task text using the existing `step_progress_strip()` helper:

```python
# Build 4-item task progress for step strip
task_steps = []
for t in range(4):
    if t < task_idx:
        state = "done"
    elif t == task_idx:
        state = "current"
    else:
        state = "pending"
    task_steps.append({"label": f"Task {t+1}", "state": state})
step_progress_strip(task_steps)
```

Place this strip immediately after `section_header("SCENARIO")` and before the task instruction text.

**Problem CM-H**: Secondary action buttons clutter the primary path.

**Fix**: Move "Skip this task →" and "Complete Practice Early →" into a `st.popover()`:

```python
# Existing primary CTA (keep as-is):
if st.button("Next Task →", key="p_next", type="primary"):
    ...

# Secondary actions moved into popover:
with st.popover("⋯ More options"):
    if task_idx < 3:
        if st.button("Skip this task", key="p_skip_pop"):
            ...
    if st.button("Complete Practice Early", key="p_early_pop"):
        ...
```

**Problem CM-E**: Warning banner shown before any interaction.

**Fix**: Demote to `st.caption()` with an icon — less alarming, still informative:

```python
# BEFORE:
st.warning("⚠️ Navigating away via the sidebar or breadcrumb will end your session "
           "without saving your practice conversation.")

# AFTER:
st.caption("ℹ️ Navigating away will end this practice session. "
           "Use **Complete Practice →** to save your progress.")
```

---

### Task CM-3 — Results sub-view: native coach note card; score delta; native update confirmation

**File**: `pages/04_Course_Module.py` (results section ~lines 656–743)

**Problem CM-K**: Coach note in `aha-card-accent` HTML card.

**Fix**: Replace with `st.container(border=True)` + styled caption:

```python
# BEFORE (lines 704–712):
if coach_note:
    st.markdown(f"""
<div class="aha-card-accent">
  <div class="coach-header"><span>🤖</span><span class="coach-label">AI Coach Note</span></div>
  <div ...>{coach_note}</div>
</div>""", unsafe_allow_html=True)

# AFTER:
if coach_note:
    with st.container(border=True):
        st.caption("🤖 AI COACH NOTE")
        st.markdown(coach_note)
```

Remove `aha-card-accent` coach-specific inner CSS once this is the only remaining use. (The card class is still used elsewhere — check before removing.)

**Problem CM-L**: "Skills profile has been updated" raw HTML div.

**Fix**:
```python
# BEFORE (lines 714–717):
st.markdown("""<div style="...">✓ Your skills profile has been updated.</div>""", unsafe_allow_html=True)

# AFTER:
st.success("✓ Your skills profile has been updated.")
```

**Problem CM-M**: `st.metric()` shows score without baseline comparison.

**Fix**: Retrieve the diagnostic domain score for this module's primary_domain and compute a delta:

```python
# After loading result_score, also fetch diagnostic baseline:
diag_row = query_one(
    f"SELECT domain_scores FROM {CATALOG}.learner.diagnostic_sessions "
    f"WHERE user_email = ? AND completed_at IS NOT NULL "
    f"ORDER BY completed_at DESC LIMIT 1",
    [user_email],
)
diag_domain_scores = {}
if diag_row:
    try:
        diag_domain_scores = json.loads(diag_row.get("domain_scores") or "{}")
    except Exception:
        pass
diag_baseline = diag_domain_scores.get(primary_domain)

# Then render metric with delta:
delta_str = None
if diag_baseline is not None:
    try:
        delta_val = rs - float(diag_baseline)
        delta_str = f"{delta_val:+.1f} vs. diagnostic"
    except (TypeError, ValueError):
        pass

st.metric(label=course_title, value=f"{rs:.1f} / 4.0", delta=delta_str)
```

This adds a DB query only for the Results sub-view (already makes one in `complete_evaluation` — but the fallback path doesn't). Cache in session state after evaluation completes to avoid the round-trip.

---

### Task CM-4 — Evaluation sub-view: replace raw HTML labels with native components

**File**: `pages/04_Course_Module.py` (evaluation section ~lines 456–650)

**Problem CM-I + CM-J**: Minor HTML injections for labels.

**Fix**: Replace the three raw HTML label patterns:

```python
# 1. Question counter (line 572–576) — BEFORE:
st.markdown(f'<div class="question-counter">Module {seq_order} · Quiz · '
            f'Question {min(eval_idx + 1, EVAL_TOTAL)} of {EVAL_TOTAL}</div>',
            unsafe_allow_html=True)
# AFTER:
st.caption(f"MODULE {seq_order}  ·  QUIZ  ·  QUESTION {min(eval_idx + 1, EVAL_TOTAL)} OF {EVAL_TOTAL}")

# 2. Domain tag inline (lines 597–599) — BEFORE:
st.markdown(f'<div class="domain-tag-inline">{DOMAIN_DISPLAY_NAMES.get(...)}</div>',
            unsafe_allow_html=True)
# AFTER (keep visual similar with a formatted caption):
st.caption(f"📍 {DOMAIN_DISPLAY_NAMES.get(primary_domain, primary_domain).upper()}")

# 3. Performance task Scenario label (lines 628–635) — BEFORE: 6-line HTML block
# AFTER:
st.caption("SCENARIO")
```

This removes 3 `unsafe_allow_html=True` calls with zero visual regression.

---

### Task CM-5 — Overview sub-view: add module description and step time hints

**File**: `pages/04_Course_Module.py` (overview section ~lines 192–225)

**Current**: Sparse — counter, title, tagline, step strip, 1 CTA button.

**Fix**: Add a `st.expander("About this module")` showing domain context and estimated step times:

```python
# After step_progress_strip(), before the CTA button:
with st.expander("About this module", expanded=False):
    domain_display = DOMAIN_DISPLAY_NAMES.get(primary_domain, primary_domain)
    st.caption(f"📍 Domain: {domain_display}")
    st.markdown(
        "| Step | Format | Est. time |\n"
        "|------|--------|-----------|\n"
        "| Read | Article + callouts | ~5 min |\n"
        "| Practice | AI coach conversation (4 tasks) | ~10–15 min |\n"
        "| Quiz | 3 MCQ + 1 written response | ~5 min |"
    )
```

This uses native `st.expander` + a markdown table — zero HTML injection.

---

### Task CM-6 — `styles.py` cleanup

**File**: `utils/styles.py`

Remove CSS blocks that are no longer used after tasks CM-1 to CM-5:

| CSS class/selector | Reason for removal |
|--------------------|--------------------|
| `.reading-concept` (lines 459–465) | Replaced by `st.container(border=True)` in CM-1 |
| `.coach-header`, `.coach-label` (lines 447–454) | Replaced by `st.caption()` in CM-3 (verify no other uses first) |

Keep:
- `.scenario-box` — still used in practice (scenario HTML) and evaluation MCQ scenario
- `.question-text` — still used in practice task text and evaluation MCQ question
- `.aha-card-accent`, `.aha-card-warning` etc. — may still be used elsewhere; grep first
- `.domain-tag-inline`, `.question-counter` — removed from evaluation HTML, but check if used in diagnostic page too (`grep -r "domain-tag-inline\|question-counter" pages/`)

---

### Task CM-7 — Reading sub-view: slide-style section navigation (microlearning)

**File**: `pages/04_Course_Module.py` (reading section ~lines 253–287)

**Problems CM-N + CM-D**: All 4 reading sections (Concept, Good Example, Mistake, Takeaway) are shown simultaneously as a scrolling wall of text. This saturates working memory and violates cognitive load theory. Research confirms slide-per-section formats achieve ~80% completion vs. 10–20% for scrolling walls. Text also spans full viewport width (~120–140 chars/line on wide monitors) — optimal is 60–80.

**Fix**: Replace the scroll view with a **session-state index stepper** — one section per slide. Apply a centered column layout to the content area for line-length control.

**New session state key**: `reading_section_idx` (0 = Concept, 1 = Good Example, 2 = Mistake, 3 = Takeaway). Reset to 0 whenever `reading_idx` advances.

**Content field mapping** (verified from `content/reading_content.json`):

> **Data audit result**: Each course has exactly **one** reading item (the JSON is a dict keyed by `course_id`). There is NO multi-item pagination — `reading_idx` is always 0. Navigation is simplified: no "Next Concept →" branch; the last section always shows "Mark Reading Complete →".

> **Field name fix**: `anti_pattern` is the correct field name (not `mistake`). Label can still say "Common Mistake" — label is independent of field name.

| Section idx | Display label | Streamlit component | JSON field |
|-------------|---------------|---------------------|------------|
| 0 | Concept | `st.container(border=True)` + `st.markdown()` | `concept_text` (500–800 words) |
| 1 | Good Example | `st.success()` | `good_example` (200–400 words) |
| 2 | Common Mistake | `st.warning()` | `anti_pattern` (150–300 words) |
| 3 | Key Takeaway | `st.info()` | `takeaway` (20–40 words, punchy) |

Note: `st.warning()` is more appropriate than `st.error()` for anti-patterns — the content is cautionary, not an app error.

```python
# At reading section entry:
if "reading_section_idx" not in st.session_state:
    st.session_state.reading_section_idx = 0

SECTION_TOTAL = 4
section_idx = st.session_state.reading_section_idx

# 4-step section progress strip (reuse step_progress_strip):
section_steps = [
    {"label": lbl, "state": ("done" if i < section_idx else ("current" if i == section_idx else "pending"))}
    for i, lbl in enumerate(["Concept", "Example", "Pitfall", "Takeaway"])
]
step_progress_strip(section_steps)

# Width-constrained content area (one section at a time):
_, content_col, _ = st.columns([1, 4, 1])
with content_col:
    st.caption(f"SECTION {section_idx + 1} OF {SECTION_TOTAL}")
    if section_idx == 0:
        concept_text = reading.get("concept_text", "")
        if concept_text:
            with st.container(border=True):
                st.markdown(concept_text)
    elif section_idx == 1:
        if reading.get("good_example"):
            st.success(f"**Good example** — {reading['good_example']}")
    elif section_idx == 2:
        if reading.get("anti_pattern"):
            st.warning(f"**Common mistake** — {reading['anti_pattern']}")
    elif section_idx == 3:
        if reading.get("takeaway"):
            st.info(f"**Key takeaway** — {reading['takeaway']}")

# Navigation — use on_click= callbacks to avoid stale-state double-render bug.
# One reading item per course: no "Next Concept →" branch needed.
def _section_next():
    st.session_state.reading_section_idx = min(st.session_state.reading_section_idx + 1, SECTION_TOTAL - 1)

def _section_prev():
    st.session_state.reading_section_idx = max(st.session_state.reading_section_idx - 1, 0)

nav_l, _, nav_r = st.columns([1, 6, 1])
with nav_l:
    st.button("← Back", on_click=_section_prev,
              disabled=(section_idx == 0),
              use_container_width=True)
with nav_r:
    if section_idx < SECTION_TOTAL - 1:
        st.button("Next →", on_click=_section_next, type="primary", use_container_width=True)
    else:
        if st.button("Mark Reading Complete →", key="r_complete", type="primary", use_container_width=True):
            pass  # ... existing mark-complete logic (write reading_completed_at, advance sub-view) ...
```

**Why not `st.tabs()`**: Tabs render all labels simultaneously, allowing the learner to skip — breaks sequencing. Session-state stepper enforces progressive reading. (Streamlit GitHub #10748: native `st.stepper()` is on the community roadmap; this is the current standard workaround.)

**Why `on_click=` not inline `if st.button():`**: Avoids the stale-state double-render bug where previous section content persists for one extra render cycle.

**No JSON changes required**: the four content fields (`concept_text`, `good_example`, `anti_pattern`, `takeaway`) already map to four discrete slides. Content is already structured for this pattern.

---

## Implementation Order

```text
CM-1  Reading: remove _md() hack; st.container(border=True) for concept  ← lowest risk, isolated
CM-7  Reading: constrain content width with columns layout                ← additive only, no removals
CM-4  Evaluation: replace 3 HTML label patterns with st.caption()         ← low risk, small changes
CM-5  Overview: add expander with time hints                               ← additive only, no removals
CM-2  Practice: scenario expander + task strip + popover for secondary    ← medium risk, test thoroughly
CM-3  Results: native coach note + success banner + metric delta           ← medium risk, test delta query
CM-6  styles.py: remove dead CSS (after CM-1..CM-7 verified)              ← do last, after UAT
```

---

## Files to Modify

| File | Changes |
|------|---------|
| `pages/04_Course_Module.py` | Tasks CM-1 through CM-5 |
| `utils/styles.py` | Task CM-6: remove dead CSS classes |

**No other files touched.**

---

## Acceptance Checks

- [ ] CM-1: Reading concept text renders markdown bold/italic/code correctly (no `<br>` artifacts); wrapped in border container
- [ ] CM-1: No `_md()` function remains in the file
- [ ] CM-2: Practice scenario auto-collapses after first coach reply; expander label shows "📋 Scenario"
- [ ] CM-2: 4-task step strip shows correct done/current/pending states for each task
- [ ] CM-2: "Skip this task" and "Complete Practice Early" are only accessible via the "⋯ More options" popover
- [ ] CM-2: Warning replaced by `st.caption()` — no amber `st.warning()` before any interaction
- [ ] CM-3: Coach note renders inside `st.container(border=True)` with "🤖 AI COACH NOTE" caption
- [ ] CM-3: "Skills profile updated" shows as `st.success()`
- [ ] CM-3: `st.metric()` shows `delta` value vs. diagnostic domain score (or no delta if diagnostic not available)
- [ ] CM-4: Evaluation question counter shows as `st.caption()` — visually similar to before
- [ ] CM-4: Domain tag shows as `st.caption()` — no HTML injection
- [ ] CM-5: Overview expander exists and shows domain + time estimate table when opened
- [ ] CM-7: Reading shows one section at a time (Concept → Example → Mistake → Takeaway) — no full-page scroll; 4-step strip shows current section
- [ ] CM-7: "Next →" advances through sections; last section of last item shows "Mark Reading Complete →"
- [ ] CM-7: "← Back" navigates backward; disabled on first section of first item
- [ ] CM-7: Content renders in a centered narrow column (`[1, 4, 1]`) — visibly shorter line length on wide monitors
- [ ] CM-6: No `.reading-concept`, `.coach-label` CSS blocks remain if confirmed unused
- [ ] Full UAT: `bash run_uat.sh` — all 14 UAT scenarios pass; no regressions on Diagnostic, Skills Profile, Home pages

---

## Out of Scope

- Replacing `step_progress_strip()` or `section_header()` custom HTML components globally — these are shared across pages; leave for a dedicated refactor
- Changing session-state-based sub-view navigation model — too risky; functional and well-tested
- Adding multimedia (video, audio) to reading content — content architecture change, not UX
- Animated transitions between sub-views — Streamlit does not support CSS transitions on page re-renders
- Adding `st.tabs()` to replace the sub-view state machine — would require all 5 sub-views to render simultaneously, defeating lazy loading; current model is correct
- **Sticky step indicator / sticky action bar** (expert CM-P) — Streamlit has no native sticky support; CSS-only approach (`position: sticky`) is fragile across Streamlit version updates; defer to Phase 2
- **Glassmorphism / gradient overlay cards** (expert feedback) — CSS background-blur conflicts with Streamlit's internal shadow DOM; defer to Phase 2
- **In-reading AI co-pilot side panel** (expert recommendation) — significant new feature requiring a second AI call pattern and sidebar state management; out of scope for this UX revamp
