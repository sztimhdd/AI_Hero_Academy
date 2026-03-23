# -*- coding: utf-8 -*-
"""
AC-3 Regression Test FINAL — AI Hero Academy
Properly navigates the actual Streamlit app flow.
"""
import sys, io, time, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright

SS = "/c/tmp/ac3_screenshots"
os.makedirs(SS, exist_ok=True)

RESULTS = []

def log(msg): print(msg, flush=True)

def ss(page, name):
    path = f"{SS}/{name}.png"
    page.screenshot(path=path, full_page=True)
    log(f"  [screenshot] {path}")
    return path

def settle(page, timeout=25000):
    try:
        page.wait_for_selector('[data-testid="stStatusWidget"]', timeout=2000)
        page.wait_for_selector('[data-testid="stStatusWidget"]', state="hidden", timeout=timeout)
    except: pass
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except: pass
    time.sleep(1.0)

def body(page):
    try: return page.inner_text("body")
    except: return ""

def check_edc(page, step, path):
    """Run AC-3 checks: no EDC, no traceback, no null/[object Object]."""
    txt = body(page)
    issues = []

    edc = list(re.finditer(r'\bEDC\b', txt))
    if edc:
        snippets = [txt[max(0, m.start()-40):m.end()+40].replace('\n',' ') for m in edc[:3]]
        issues.append(f"FAIL: 'EDC' found {len(edc)}x — context: {snippets}")

    # Traceback detection — Streamlit renders as "Traceback:" (no parentheses) in error box
    if "Traceback (most recent call last)" in txt or re.search(r'Traceback:\s*\nFile', txt, re.M):
        issues.append("FAIL: Python traceback visible in UI")
    if "ModuleNotFoundError" in txt:
        issues.append("FAIL: ModuleNotFoundError visible in UI")
    if "StreamlitAPIException" in txt:
        issues.append("FAIL: StreamlitAPIException in UI")
    if "[object Object]" in txt:
        issues.append("FAIL: [object Object] rendered in content")

    status = "FAIL" if any(i.startswith("FAIL") for i in issues) else "PASS"
    RESULTS.append({"step": step, "status": status, "screenshot": path, "issues": issues})
    log(f"  [CHECK {status}] {step}")
    for i in issues: log(f"         {i}")
    return status

def click_btn_by_text(page, text_exact, timeout=8000):
    """Click button with exact text match."""
    btns = page.locator('[data-testid="stButton"] button')
    for i in range(btns.count()):
        btn = btns.nth(i)
        try:
            t = btn.inner_text().strip()
            if t == text_exact and btn.is_visible():
                btn.click(timeout=timeout)
                log(f"  Clicked: '{t}'")
                return True
        except: pass
    return False

def click_btn_pattern(page, pattern, exclude_pattern=None, timeout=8000):
    """Click first visible+enabled button matching regex pattern."""
    btns = page.locator('[data-testid="stButton"] button')
    regex = re.compile(pattern, re.I)
    for i in range(btns.count()):
        btn = btns.nth(i)
        try:
            t = btn.inner_text().strip()
            if regex.search(t) and btn.is_visible():
                if exclude_pattern and re.search(exclude_pattern, t, re.I):
                    continue
                if btn.is_enabled():
                    btn.click(timeout=timeout)
                    log(f"  Clicked: '{t}'")
                    return t
        except: pass
    return None

def select_first_radio(page):
    """Click the first option label in a Streamlit radio group."""
    # stRadio labels: label 0 = question label, labels 1+ = answer options
    labels = page.locator('[data-testid="stRadio"] label')
    if labels.count() > 1:
        try:
            labels.nth(1).click()  # Click first option (A)
            time.sleep(0.4)
            return True
        except: pass
    return False

def fill_first_textarea(page, text):
    """Fill the first visible textarea and trigger Streamlit rerun via blur."""
    for ta in page.locator('textarea').all():
        if ta.is_visible():
            try:
                if not ta.input_value().strip():
                    ta.click()
                    time.sleep(0.2)
                    page.keyboard.type(text)
                    time.sleep(0.3)
                    # Blur the textarea to trigger Streamlit's on_change / rerun
                    # Clicking the page header is reliable for this
                    try:
                        page.locator('h1, h2, h3').first.click()
                    except:
                        page.keyboard.press('Tab')
                    time.sleep(2.0)  # Wait for Streamlit rerun
                    return True
            except: pass
    return False

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
        ctx = browser.new_context(viewport={"width": 1400, "height": 900})
        page = ctx.new_page()

        log("=" * 60)
        log("AC-3 REGRESSION TEST — AI Hero Academy")
        log("=" * 60)

        # ─── STEP 1: Load app ────────────────────────────────────────────
        log("\n[STEP 1] Navigate to http://localhost:8501")
        page.goto("http://localhost:8501", wait_until="domcontentloaded")
        settle(page)

        path1 = ss(page, "01_initial")
        b = body(page)
        log(f"  Title: {page.title()}")
        log(f"  Body snippet: {b[:250].replace(chr(10),' ')}")

        # Confirm we're on Diagnostic orientation screen
        if "Diagnostic" not in page.title():
            log(f"  WARNING: Expected Diagnostic page, got: {page.title()}")
            log(f"  Hint: Reset user with: python scripts/reset_uat_user.py --role rm")
        check_edc(page, "Step 1 - Initial Load (Diagnostic Page)", path1)

        # ─── STEP 2: Complete 6-question diagnostic ──────────────────────
        log("\n[STEP 2] Completing 6-question diagnostic...")

        # Click orientation "Start Assessment →"
        click_btn_pattern(page, r'Start Assessment')
        settle(page)

        questions_done = 0
        for attempt in range(25):
            settle(page, timeout=90000)
            b = body(page)

            # Completion detection — Skills Profile or scoring spinner done
            current_title = page.title()
            if any(x in current_title for x in ["Skills Profile", "Home", "Course Module"]):
                log(f"  Diagnostic complete — navigated to: {current_title}")
                break
            if any(x in b for x in ["Your AI Skills Profile", "Gap Map", "domain score", "Skills Profile",
                                     "ModuleNotFoundError"]):
                log(f"  Diagnostic complete (post-diagnostic page detected)")
                break

            # Check which question we're on
            q_match = re.search(r'Question\s+(\d+)\s+of\s+(\d+)', b, re.I)
            if q_match:
                qnum = int(q_match.group(1))
                qtotal = int(q_match.group(2))
                log(f"  Q{qnum}/{qtotal}")
            else:
                log(f"  Attempt {attempt+1}: body snippet: {b[:80].replace(chr(10),' ')}")

            # Select radio option if present (MCQ)
            selected = select_first_radio(page)

            # Fill textarea if present (prompt_sandbox / micro_task)
            if not selected:
                filled = fill_first_textarea(page,
                    "I would carefully verify all AI-generated outputs against reliable sources, "
                    "ensure no confidential client information is included in prompts, and apply "
                    "critical judgment before using or sharing any AI-produced content.")
                if filled:
                    log("  Filled textarea response")

            # Now click the advance button
            # Try in order: "Submit & Continue →", "Submit →", "Next →"
            advanced = False
            for pat in [r'Submit\s*&\s*Continue', r'Submit\s*→', r'Next\s*→', r'Next$']:
                result = click_btn_pattern(page, pat, exclude_pattern=r'Exit|Back')
                if result:
                    questions_done += 1
                    advanced = True
                    # After Submit & Continue (last question), wait for AI scoring (30-60s)
                    if 'Continue' in result:
                        log("  Waiting for AI diagnostic scoring (may take 30-60s)...")
                        settle(page, timeout=120000)
                        time.sleep(5)  # Extra buffer
                    break

            if not advanced:
                b2 = body(page)
                all_btns = page.locator('[data-testid="stButton"] button')
                btn_texts = [all_btns.nth(i).inner_text() for i in range(all_btns.count())]
                log(f"  No advance button found; buttons: {btn_texts}")
                # Check if we might be waiting for AI scoring
                if any(x in b2 for x in ["Analysing", "Analyzing", "Building your", "gap map", "spinner"]):
                    log("  Waiting for AI scoring spinner...")
                    settle(page, timeout=120000)
                    time.sleep(5)

        settle(page, timeout=90000)
        path2 = ss(page, "02_after_diagnostic")
        b = body(page)
        log(f"  Post-diagnostic: {b[:300].replace(chr(10),' ')}")
        check_edc(page, "Step 2 - After Diagnostic (12 questions answered)", path2)

        # ─── STEP 3: Skills Profile → Home → Module 1 Overview ──────────
        log("\n[STEP 3] Skills Profile → Home → Module 1 Overview...")
        settle(page)
        b = body(page)

        # From Skills Profile, find the CTA to go to Home/Courses
        for pat in [r'Go to My Courses', r'View My Courses', r'Start Learning', r'Home', r'My Courses']:
            r = click_btn_pattern(page, pat)
            if r:
                settle(page, timeout=30000)
                break

        b = body(page)
        log(f"  After Skills Profile CTA: {b[:200].replace(chr(10),' ')}")

        # On Home page, click Start Module 1
        for pat in [r'Start Module 1', r'Start Module', r'Begin']:
            r = click_btn_pattern(page, pat)
            if r:
                settle(page, timeout=30000)
                log(f"  Navigated to: {r}")
                break

        b = body(page)
        log(f"  After module nav: {b[:200].replace(chr(10),' ')}")

        # Check if on reading; navigate to overview via Back if possible
        if any(x in b for x in ["Concept", "Example", "Pitfall", "Takeaway", "Read"]) and "Start Reading" not in b:
            # Might be directly in reading — navigate back to overview
            r = click_btn_pattern(page, r'← Overview|Overview|Back to Overview')
            if r:
                settle(page)

        path3 = ss(page, "03_module1_overview")
        b = body(page)
        log(f"  Module overview content: {b[:300].replace(chr(10),' ')}")
        check_edc(page, "Step 3 - Module 1 Overview", path3)

        # Verify not empty
        if len(b.strip()) < 100:
            RESULTS[-1]['status'] = "FAIL"
            RESULTS[-1]['issues'].append("FAIL: Module overview appears empty")

        # ─── STEP 4: Reading section ─────────────────────────────────────
        log("\n[STEP 4] Reading section...")

        # Click "Start Reading →" from Overview
        r = click_btn_pattern(page, r'Start Reading')
        if r:
            settle(page)
        else:
            # Already on reading from Home navigation
            log("  Already on reading or navigated directly")

        b = body(page)
        log(f"  Reading content length: {len(b)}")
        log(f"  Reading snippet: {b[:400].replace(chr(10),' ')}")

        # Verify reading has content
        reading_issues = []
        if len(b.strip()) < 300:
            reading_issues.append("FAIL: Reading content very short (< 300 chars)")
        # Check for section labels
        has_section = any(x in b for x in ["Concept", "concept", "Overview", "What is", "Introduction"])
        if not has_section:
            reading_issues.append("WARN: No recognizable reading section (Concept/Example) visible")

        path4 = ss(page, "04_reading_concept")
        check_edc(page, "Step 4 - Reading Tab / Concept Section", path4)
        if reading_issues:
            RESULTS[-1]['issues'].extend(reading_issues)
            if any(i.startswith("FAIL") for i in reading_issues):
                RESULTS[-1]['status'] = "FAIL"
            for i in reading_issues: log(f"  {i}")

        # ─── STEP 5: Practice section ─────────────────────────────────────
        log("\n[STEP 5] Practice section...")

        # Navigate through all reading sections to reach practice
        # Reading has 4 sections: Concept → Example → Pitfall → Takeaway
        # Each section has a "Next →" or "→ Next" button
        for nav_attempt in range(8):
            settle(page)
            b = body(page)

            # Check if we're on practice
            if any(x in b for x in ["Task 1", "task 1", "AI Coach", "Practice Coach", "your response"]):
                log(f"  Practice section reached after {nav_attempt} navigation steps")
                break

            # Check for "Continue to Practice" or similar CTA
            r = click_btn_pattern(page, r'Continue to Practice|Start Practice')
            if r:
                settle(page)
                break

            # Navigate to next reading section
            r = click_btn_pattern(page, r'Next\s*[→→]|→\s*Next|Next Section', exclude_pattern=r'Question|Question next')
            if r:
                settle(page)
                log(f"  Reading navigation: {r}")
                continue

            # Try "Takeaway" as final section
            # After Takeaway, there should be a "Continue to Practice" button
            log(f"  nav_attempt {nav_attempt}: no navigation found in reading")
            log(f"  Body: {b[:100].replace(chr(10),' ')}")
            break

        # If not on practice yet, check for the practice CTA button
        b = body(page)
        if not any(x in b for x in ["Task", "task", "coach", "Coach"]):
            # Try direct practice CTA from wherever we are
            for pat in [r'Continue to Practice', r'Practice', r'Start Practice']:
                r = click_btn_pattern(page, pat, exclude_pattern=r'Exit|Back|Overview')
                if r:
                    settle(page)
                    b = body(page)
                    break

        b = body(page)
        log(f"  Practice page content: {b[:400].replace(chr(10),' ')}")

        # Submit Task 1 response
        practice_text = "I would use the SAFE method to check the prompt"

        filled = fill_first_textarea(page, practice_text)
        if filled:
            log("  Filled Task 1 response")
        else:
            log("  WARNING: No textarea found for Practice Task 1")

        # Click Send/Submit button
        r = click_btn_pattern(page, r'^Send$|^Submit$|^Send Response$|^Reply$')
        if not r:
            # Try any non-exit button
            btns = page.locator('[data-testid="stButton"] button')
            btn_texts = []
            for i in range(btns.count()):
                try:
                    t = btns.nth(i).inner_text().strip()
                    btn_texts.append(t)
                except: pass
            log(f"  Available buttons: {btn_texts}")
            for i in range(btns.count()):
                btn = btns.nth(i)
                try:
                    t = btn.inner_text().strip()
                    if t and btn.is_visible() and btn.is_enabled():
                        if not any(x in t.lower() for x in ['exit', 'back', 'overview', '← ']):
                            btn.click()
                            log(f"  Clicked fallback: '{t}'")
                            break
                except: pass

        log("  Waiting for AI coach response (up to 60s)...")
        settle(page, timeout=90000)
        time.sleep(3)
        settle(page, timeout=30000)

        b = body(page)
        log(f"  Post-reply body: {b[:400].replace(chr(10),' ')}")
        path5 = ss(page, "05_practice_coach_reply")
        check_edc(page, "Step 5 - Practice Tab / Coach Reply", path5)

        # ─── STEP 6: Evaluation section ──────────────────────────────────
        log("\n[STEP 6] Evaluation section...")

        # Navigate to evaluation
        b = body(page)
        log(f"  Current page before eval nav: {b[:150].replace(chr(10),' ')}")

        # Try "Take Quiz →" or "Skip to Quiz" or evaluation nav
        for pat in [r'Take Quiz', r'Skip to Quiz', r'Evaluation', r'Quiz']:
            r = click_btn_pattern(page, pat, exclude_pattern=r'Exit|Back')
            if r:
                settle(page)
                log(f"  Navigated to eval: '{r}'")
                break

        b = body(page)
        log(f"  Eval page: {b[:300].replace(chr(10),' ')}")

        # If not on evaluation, try via overview → Take Quiz
        if not any(x in b for x in ["Question", "Quiz", "Choose your answer", "Evaluation"]):
            log("  Not on evaluation, trying via Overview...")
            r = click_btn_pattern(page, r'← Overview|Overview')
            if r:
                settle(page)
            for pat in [r'Take Quiz', r'Continue Practice']:
                r = click_btn_pattern(page, pat)
                if r:
                    settle(page)
                    break

        # Answer evaluation questions (3 MCQ + 1 performance task)
        log("  Answering evaluation questions...")
        eval_submitted = False
        for q_attempt in range(25):
            settle(page, timeout=60000)
            b = body(page)

            # Results detection
            if any(x in b for x in ["Results", "Your Score", "Coach Note", "Module Complete",
                                     "You scored", "Well done", "module result"]):
                log(f"  Results reached after {q_attempt} eval answer attempts")
                eval_submitted = True
                break

            # Select radio
            selected = select_first_radio(page)
            if selected:
                log(f"  Q{q_attempt+1}: selected radio option")

            # Fill textarea (performance task Q4)
            filled = fill_first_textarea(page,
                "I would carefully review all AI-generated content for factual accuracy, "
                "verify claims against reliable authoritative sources, check that no confidential "
                "client information was inadvertently included, and ensure the tone and format "
                "is appropriate before sharing with the client.")
            if filled:
                log(f"  Q{q_attempt+1}: filled textarea")

            # Click Next or Submit
            advanced = False
            for pat in [r'^Submit\s*(Evaluation|Quiz|Assessment|→)?$', r'^Submit$', r'^Finish$',
                         r'^Next\s*→?$', r'^Next\s+Question']:
                result = click_btn_pattern(page, pat, exclude_pattern=r'Exit|Back|Overview')
                if result:
                    advanced = True
                    # Wait longer for AI scoring
                    if re.search(r'submit|finish', result, re.I):
                        log("  Waiting for AI scoring (up to 90s)...")
                        settle(page, timeout=120000)
                        time.sleep(6)
                    break

            if not advanced:
                btn_texts = []
                btns = page.locator('[data-testid="stButton"] button')
                for i in range(btns.count()):
                    try: btn_texts.append(btns.nth(i).inner_text().strip())
                    except: pass
                log(f"  q_attempt {q_attempt+1}: no advance; buttons={btn_texts}; body={b[:80].replace(chr(10),' ')}")
                if q_attempt > 8:
                    ss(page, f"06_eval_stuck_{q_attempt}")
                    break

        settle(page, timeout=30000)
        b = body(page)
        log(f"  Final results content: {b[:500].replace(chr(10),' ')}")
        path6 = ss(page, "06_evaluation_results")
        check_edc(page, "Step 6 - Evaluation Results", path6)

        # Extra check: verify results has content
        if not eval_submitted and not any(x in b for x in ["Score", "Result", "Coach"]):
            RESULTS[-1]['issues'].append("WARN: Results page content not confirmed")

        browser.close()

    # ─── FINAL SUMMARY ───────────────────────────────────────────────
    log("\n" + "=" * 60)
    log("AC-3 REGRESSION TEST — FINAL SUMMARY")
    log("=" * 60)

    all_ok = True
    for r in RESULTS:
        log(f"\n[{r['status']}] {r['step']}")
        log(f"       Screenshot: {r['screenshot']}")
        for issue in r['issues']:
            log(f"       {issue}")
        if r['status'] == "FAIL":
            all_ok = False

    log("\n" + "=" * 60)
    fails = [r for r in RESULTS if r['status'] == "FAIL"]
    warns = [r for r in RESULTS if r['status'] == "WARN"]
    log(f"OVERALL: {'PASS' if all_ok else 'FAIL'} — {len(fails)} failure(s), {len(warns)} warning(s)")
    log("=" * 60)
    log(f"Screenshots: {SS}")

if __name__ == "__main__":
    run()
