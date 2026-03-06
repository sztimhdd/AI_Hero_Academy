# Course Module UX Revamp — Agent Kickstart Prompt

Copy the section below into a new Claude Code session to implement the UX revamp.

---

## Kickstart Prompt

You are implementing the **Course Module UX Revamp** for the AI Hero Academy Streamlit app.

### Read these files first (in order):

1. `plans/course-module-ux-revamp.md` — full plan with 7 tasks, exact code snippets, and acceptance checks
2. `pages/04_Course_Module.py` — the file you will modify (~744 lines; 5 sub-views: overview/reading/practice/evaluation/results)
3. `utils/styles.py` — design system CSS; you will remove dead CSS classes at the end

### Branch setup (do this first):

```bash
git checkout main && git pull
git checkout -b feature/course-module-ux
```

### What to build (6 tasks, in order):

**CM-1 — Reading sub-view: remove `_md()` hack** (~lines 247–252)
- Delete the `_md()` helper function
- Replace `<div class="reading-concept">{_md(...)}` with:
  ```python
  with st.container(border=True):
      st.markdown(reading.get("concept_text", ""))
  ```
- Remove `.reading-concept` CSS block from `utils/styles.py` (lines ~459–465)

**CM-2 — Practice sub-view** (~lines 294–450)
1. Demote warning banner: replace `st.warning(...)` with `st.caption("ℹ️ Navigating away will end this practice session. Use **Complete Practice →** to save your progress.")`
2. Collapse scenario in expander: replace the scenario-box div with `st.expander("📋 Scenario", expanded=(len(messages)==0))` wrapping the existing `st.markdown(f'<div class="scenario-box">...')`
3. Add 4-step task progress strip immediately after the scenario expander, before the task text:
   ```python
   task_steps = [{"label": f"Task {t+1}", "state": ("done" if t < task_idx else ("current" if t == task_idx else "pending"))} for t in range(4)]
   step_progress_strip(task_steps)
   ```
4. Move secondary actions into `st.popover("⋯ More options")`:
   - "Skip this task" → inside popover only
   - "Complete Practice Early" → inside popover only
   - Keep primary "Next Task →" and "Complete Practice →" as top-level buttons

**CM-3 — Results sub-view** (~lines 656–743)
1. Coach note card: replace `<div class="aha-card-accent">...</div>` HTML block with:
   ```python
   with st.container(border=True):
       st.caption("🤖 AI COACH NOTE")
       st.markdown(coach_note)
   ```
2. Update confirmation: replace raw HTML `<div style="...">✓ Your skills profile...</div>` with `st.success("✓ Your skills profile has been updated.")`
3. Score delta: add a DB query at the top of the results block to get the diagnostic domain baseline, then pass `delta=delta_str` to `st.metric()`. See the plan for exact SQL and delta calculation code.

**CM-4 — Evaluation sub-view: replace HTML labels** (~lines 572–635)
1. Question counter: replace `st.markdown(f'<div class="question-counter">...', unsafe_allow_html=True)` with `st.caption(f"MODULE {seq_order}  ·  QUIZ  ·  QUESTION {min(eval_idx+1, EVAL_TOTAL)} OF {EVAL_TOTAL}")`
2. Domain tag: replace `<div class="domain-tag-inline">` with `st.caption(f"📍 {DOMAIN_DISPLAY_NAMES.get(primary_domain, primary_domain).upper()}")`
3. Performance task Scenario label: replace the 6-line HTML block with `st.caption("SCENARIO")`

**CM-5 — Overview sub-view: add module description expander** (~line 208, after `step_progress_strip()`)
```python
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

**CM-7 — Reading sub-view: slide-style section navigation** (~lines 253–287, after CM-1)

Replace the scroll view with a one-section-per-slide stepper. Each reading item has 4 sections shown one at a time: Concept → Good Example → Common Mistake → Key Takeaway.

1. Add session state: `reading_section_idx` (int, 0–3). Initialize to 0; reset to 0 whenever `reading_idx` advances.
2. Add a 4-step strip using `step_progress_strip()` with labels `["Concept", "Example", "Mistake", "Takeaway"]`.
3. Render only the current section in a `st.columns([1, 4, 1])` centered content column:
   - `section_idx == 0` → `st.container(border=True)` + `st.markdown(concept_text)` (CM-1 fix)
   - `section_idx == 1` → `st.success("**Good example** — ...")`
   - `section_idx == 2` → `st.error("**Common mistake** — ...")`
   - `section_idx == 3` → `st.info("**Key takeaway** — ...")`
4. Navigation row (outside the column, full-width):
   - Left: `"← Back"` button — `on_click=_section_prev`, `disabled=` when at first section of first item
   - Right: context-aware primary CTA:
     - Not last section → `"Next →"` (advances section_idx)
     - Last section, not last item → `"Next Concept →"` (advances reading_idx + resets section_idx to 0)
     - Last section AND last item → `"Mark Reading Complete →"` (existing complete logic)
5. **Use `on_click=` callbacks** (not `if st.button():`). Inline checks cause a stale-state double-render bug in Streamlit.
6. See `plans/course-module-ux-revamp.md` Task CM-7 for the complete code snippet.

**CM-6 — `utils/styles.py` cleanup (do last)**
- Before removing any CSS, grep to confirm nothing else uses it:
  ```bash
  grep -rn "reading-concept\|coach-label\|coach-header\|domain-tag-inline\|question-counter" pages/ utils/
  ```
- Remove only the CSS blocks confirmed unused:
  - `.reading-concept` (if CM-1 complete and no other uses)
  - `.coach-header`, `.coach-label` (if CM-3 replaces the only remaining use)
  - `.domain-tag-inline`, `.question-counter` (if CM-4 removes all uses — check `pages/01_Diagnostic.py` too)

### Key constraints:

- Only modify `pages/04_Course_Module.py` and `utils/styles.py`
- Do NOT modify any other pages (00 through 03), `utils/auth.py`, `utils/db.py`, or `utils/demo.py`
- Never add `unsafe_allow_html=True` — the goal is to reduce it
- Keep `step_progress_strip()` and `section_header()` functions unchanged in `utils/styles.py` — they are shared and used by other pages
- Keep `.scenario-box` and `.question-text` CSS — still used for practice task text and eval questions
- Keep all `st.success/error/info` callouts in Reading sub-view — these are correct and already native

### Testing after implementation:

```bash
bash run_uat.sh
```

Walk through the full flow:
1. Navigate to Home → click "Start Module 1 →"
2. **Overview**: verify "About this module" expander opens and shows table
3. **Reading**: click "Start Reading →":
   - Verify only the **Concept** section is visible (not a full scroll page)
   - Verify 4-step strip shows "Concept" as current
   - Verify concept text renders markdown correctly (bold, line breaks) in a `border=True` container
   - Verify content is in a centered narrow column (not full viewport width)
   - Click "Next →" → verify "Good Example" section appears; strip advances
   - Click "Next →" twice more → "Common Mistake" → "Key Takeaway"
   - On last concept's last section: verify "Mark Reading Complete →" button appears (not "Next →")
4. **Practice**: click "Continue Practice →":
   - Verify `st.caption()` warning (not amber banner) at top
   - Verify scenario in expander (auto-expanded initially)
   - Type a response → coach replies → verify expander auto-collapses
   - Verify 4-step task strip shows Task 1 as current
   - Verify "Next Task →" is a prominent primary button
   - Click "⋯ More options" → verify Skip and Complete Early are inside
5. **Evaluation**: verify question counter and domain tag are `st.caption()` style
6. **Results**: verify coach note in `st.container(border=True)`, success banner, and metric shows delta

Manual check:
```
python scripts/reset_uat_user.py --role uw --diag
# Navigate to Skills Profile → "Build My Training Course" → proceed to Home → Module 1 → Results
# Verify metric delta shows vs. diagnostic baseline
```

Also run pytest to check no scoring regressions:
```bash
.venv/Scripts/python -m pytest tests/ -q
```

### Commit when done:

```bash
git add pages/04_Course_Module.py utils/styles.py
git commit -m "feat(ux): revamp Course Module page — native components, task strip, score delta"
```

Then ask the user if they want to merge to main or keep the branch for review.

### Acceptance checklist:

- [ ] Reading concept text renders bold/italic/code via `st.markdown()` — no `_md()` function
- [ ] Reading concept wrapped in `st.container(border=True)`
- [ ] Practice warning is `st.caption()` (not amber banner)
- [ ] Practice scenario in `st.expander("📋 Scenario")` — auto-collapses after first reply
- [ ] 4-step task progress strip visible in practice
- [ ] Skip and Complete Early only accessible via `st.popover("⋯ More options")`
- [ ] Results coach note in `st.container(border=True)` with "🤖 AI COACH NOTE" caption
- [ ] Results update confirmation is `st.success()`
- [ ] Results metric shows `delta` vs. diagnostic domain score
- [ ] Evaluation counter and domain tag are `st.caption()` — no `unsafe_allow_html`
- [ ] Overview has "About this module" expander with domain + time table
- [ ] Reading shows one section at a time (Concept → Example → Mistake → Takeaway) — no full-page scroll
- [ ] Reading 4-step strip tracks current section correctly
- [ ] "Next →" / "Next Concept →" / "Mark Reading Complete →" appear at the right steps
- [ ] "← Back" is disabled on first section of first item; works correctly otherwise
- [ ] Reading content is in a centered narrow column — shorter line length on wide monitors
- [ ] `bash run_uat.sh` passes all 14 UAT scenarios
- [ ] No new `unsafe_allow_html=True` calls added anywhere
