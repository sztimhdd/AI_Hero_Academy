# -*- coding: utf-8 -*-
"""
AC-3 Regression Test v2 — AI Hero Academy
Properly navigates the actual app flow with correct button targeting.
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
    time.sleep(1.2)

def body(page):
    try:
        return page.inner_text("body")
    except:
        return ""

def check(page, step, path):
    txt = body(page)
    issues = []

    edc = list(re.finditer(r'\bEDC\b', txt))
    if edc:
        snippets = [txt[max(0, m.start()-30):m.end()+30].replace('\n',' ') for m in edc[:3]]
        issues.append(f"FAIL: 'EDC' found {len(edc)} time(s): {snippets}")

    if "Traceback (most recent call last)" in txt:
        issues.append("FAIL: Python traceback visible")
    if "StreamlitAPIException" in txt:
        issues.append("FAIL: StreamlitAPIException visible")
    if "[object Object]" in txt:
        issues.append("FAIL: [object Object] in content")

    status = "FAIL" if any(i.startswith("FAIL") for i in issues) else ("WARN" if issues else "PASS")
    RESULTS.append({"step": step, "status": status, "screenshot": path, "issues": issues})
    log(f"  [CHECK {status}] {step}")
    for i in issues: log(f"         {i}")
    return status

def click_btn(page, text_re, timeout=10000, exact=False):
    """Click the first visible button matching text_re, return its text or None."""
    btns = page.locator('[data-testid="stButton"] button')
    pattern = re.compile(text_re, re.I)
    for i in range(btns.count()):
        btn = btns.nth(i)
        try:
            t = btn.inner_text().strip()
            if pattern.search(t) and btn.is_visible() and btn.is_enabled():
                btn.click(timeout=timeout)
                log(f"  Clicked: '{t}'")
                return t
        except: pass
    return None

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
        ctx = browser.new_context(viewport={"width": 1400, "height": 900})
        page = ctx.new_page()

        log("=" * 60)
        log("AC-3 REGRESSION TEST v2 — AI Hero Academy")
        log("=" * 60)

        # ── STEP 1: Initial page load ──────────────────────────────────
        log("\n[STEP 1] http://localhost:8501")
        page.goto("http://localhost:8501", wait_until="domcontentloaded")
        settle(page)
        path1 = ss(page, "01_initial")
        b = body(page)
        log(f"  Title: {page.title()}")
        log(f"  Body: {b[:250].replace(chr(10),' ')}")
        check(page, "Step 1 - Initial Load (Diagnostic Page)", path1)

        # Confirm Diagnostic orientation screen
        assert "Diagnostic" in b or "diagnostic" in b.lower(), "Expected Diagnostic page"

        # ── STEP 2: Diagnostic — click Start Assessment ─────────────────
        log("\n[STEP 2] Completing diagnostic (6 questions)...")
        # Click the orientation "Start Assessment →" button
        result = click_btn(page, r'^Start Assessment')
        if result:
            settle(page)
        else:
            log("  WARNING: 'Start Assessment' button not found")

        # Now answer 6 questions
        q_answered = 0
        for attempt in range(30):
            settle(page, timeout=90000)
            b = body(page)

            # Completion detection
            if any(x in b for x in ["Skills Profile", "Your AI Skills", "Gap Map", "skill gap", "domain score"]):
                log(f"  Diagnostic complete after {q_answered} questions answered")
                break
            if "Skills Profile" in page.title():
                log(f"  Skills Profile loaded")
                break

            # Check question number to track progress
            q_match = re.search(r'Question\s+(\d+)\s+of\s+(\d+)', b)
            if q_match:
                q_num = int(q_match.group(1))
                q_total = int(q_match.group(2))
                log(f"  On question {q_num}/{q_total}")
            else:
                log(f"  Body snippet: {b[:100].replace(chr(10),' ')}")

            # Select radio option if present
            radios = page.locator('input[type="radio"]')
            if radios.count() > 0:
                for ri in range(radios.count()):
                    if not radios.nth(ri).is_checked():
                        try:
                            radios.nth(ri).check(force=True)
                            time.sleep(0.3)
                            break
                        except: pass

            # Fill textarea if present (prompt_sandbox / micro_task questions)
            for ta in page.locator('textarea').all():
                if ta.is_visible():
                    try:
                        if not ta.input_value().strip():
                            ta.fill("I would use AI tools carefully by verifying all outputs against reliable sources before sharing with clients, and I would never include confidential client information in AI prompts.")
                            time.sleep(0.3)
                    except: pass
                    break

            # Click the primary action button — specifically NOT "← Exit"
            # Buttons in order of preference: "Submit & Continue", "Submit →", "Next →"
            clicked = None
            for pat in [r'^Submit\s*[&→]', r'^Next\s*[→]', r'^Submit\s*→']:
                clicked = click_btn(page, pat)
                if clicked:
                    q_answered += 1
                    break

            if not clicked:
                # Fall through: click any primary button that is not Exit/Back
                btns = page.locator('[data-testid="stButton"] button[kind="primary"], [data-testid="stButton"] button[data-testid="baseButton-primary"]')
                if btns.count() > 0:
                    t = btns.first.inner_text().strip()
                    if 'exit' not in t.lower() and 'back' not in t.lower():
                        btns.first.click()
                        q_answered += 1
                        log(f"  Clicked primary button: '{t}'")
                        clicked = t

            if not clicked:
                log(f"  Attempt {attempt+1}: no action button found")
                if attempt >= 5:
                    ss(page, f"02_stuck_{attempt}")
                    break

        settle(page, timeout=90000)
        path2 = ss(page, "02_after_diagnostic")
        b = body(page)
        log(f"  Post-diagnostic: {b[:300].replace(chr(10),' ')}")
        check(page, "Step 2 - After Diagnostic (Skills Profile)", path2)

        # ── STEP 3: Skills Profile → Home → Module 1 → Overview ────────
        log("\n[STEP 3] Navigate Skills Profile → Home → Module 1 Overview...")
        settle(page)

        # From Skills Profile, click "Go to My Courses" or "Home" or similar CTA
        for pat in [r'Go to My Courses', r'Start Learning', r'View Courses', r'Home', r'Begin']:
            r = click_btn(page, pat)
            if r:
                settle(page, timeout=30000)
                break

        b = body(page)
        log(f"  After Skills Profile CTA: {b[:250].replace(chr(10),' ')}")

        # On Home page, click "Start Module 1 →"
        for pat in [r'Start Module 1', r'Start Module', r'Module 1']:
            r = click_btn(page, pat)
            if r:
                settle(page, timeout=30000)
                log(f"  Navigated to module: {r}")
                break

        b = body(page)
        log(f"  After module click: {b[:250].replace(chr(10),' ')}")

        # Now on Course Module page — navigate to Overview sub-view
        # The module may start directly on Reading; check what sub-view we're on
        # Look for the "← Overview" back link or overview buttons
        for pat in [r'Overview', r'← Overview', r'Back to Overview']:
            r = click_btn(page, pat)
            if r:
                settle(page)
                break

        path3 = ss(page, "03_module1_overview")
        b = body(page)
        log(f"  Overview page: {b[:300].replace(chr(10),' ')}")
        check(page, "Step 3 - Module 1 Overview", path3)

        # ── STEP 4: Reading tab ─────────────────────────────────────────
        log("\n[STEP 4] Reading section...")
        # Click "Start Reading →" from overview
        r = click_btn(page, r'Start Reading|Continue Reading|Read')
        if r:
            settle(page)

        b = body(page)
        log(f"  Reading content length: {len(b)}")
        log(f"  Reading snippet: {b[:400].replace(chr(10),' ')}")

        # Check for empty content
        extra = []
        if len(b.strip()) < 300:
            extra.append("FAIL: Reading content appears empty (< 300 chars)")

        # Check for empty concept sections
        if "Concept" in b and len(b) < 500:
            extra.append("WARN: Very little reading content after Concept label")

        path4 = ss(page, "04_reading")
        check(page, "Step 4 - Reading Tab / Concept Section", path4)
        if extra:
            RESULTS[-1]['issues'].extend(extra)
            RESULTS[-1]['status'] = "FAIL" if any(e.startswith("FAIL") for e in extra) else RESULTS[-1]['status']
            for e in extra: log(f"  {e}")

        # ── STEP 5: Practice section ────────────────────────────────────
        log("\n[STEP 5] Practice section...")

        # From Reading, find "Start Practice" or navigate through sections
        # First complete the reading by going through all 4 sections (Concept → Example → Pitfall → Takeaway)
        log("  Navigating through reading sections to reach Practice...")
        for section_nav_attempt in range(8):
            b = body(page)
            # If we hit practice section
            if any(x in b for x in ["Task 1", "Practice Coach", "AI Coach", "coach"]):
                log(f"  Reached Practice after {section_nav_attempt} section navigations")
                break
            # Check for Continue to Practice button
            r = click_btn(page, r'Continue to Practice|Start Practice|Practice')
            if r:
                settle(page)
                break
            # Navigate through reading sections with Next button
            r = click_btn(page, r'Next\s*[→→]|Next Section|Takeaway|Example|Pitfall')
            if r:
                settle(page)
            else:
                # Try to find any forward-navigation button
                r = click_btn(page, r'Next|Continue|Proceed')
                if r:
                    settle(page)
                    log(f"  Navigation click: {r}")
                else:
                    log(f"  Section attempt {section_nav_attempt+1}: no nav button, body: {b[:100].replace(chr(10),' ')}")
                    break

        # If still on reading, navigate to practice via overview back-nav pattern
        b = body(page)
        if not any(x in b for x in ["Task 1", "task 1", "Practice Coach", "coach"]):
            # Try clicking to next section or finish reading
            log("  Attempting to reach practice via reading completion...")
            for _ in range(5):
                settle(page)
                r = click_btn(page, r'Takeaway|Continue|Finish Reading|Start Practice|Practice')
                if r:
                    settle(page)
                    b = body(page)
                    if any(x in b for x in ["Task 1", "Practice", "coach"]):
                        break

        b = body(page)
        log(f"  Practice page body: {b[:400].replace(chr(10),' ')}")

        # Fill textarea and send response to Task 1
        ta = page.locator('textarea').first
        if ta.count() > 0 and ta.is_visible():
            ta.fill("I would use the SAFE method to check the prompt")
            log("  Filled Task 1 response")
            time.sleep(0.5)
        else:
            log("  WARNING: No textarea found for Practice")

        # Click Send
        r = click_btn(page, r'^Send$|^Submit$|^Reply$|Send Response')
        if not r:
            # Fallback: click any primary button that's not Exit/Back
            btns = page.locator('[data-testid="stButton"] button')
            for i in range(btns.count()):
                btn = btns.nth(i)
                t = btn.inner_text().strip()
                if t and btn.is_visible() and btn.is_enabled():
                    if not any(x in t.lower() for x in ['exit', 'back', 'overview']):
                        btn.click()
                        log(f"  Clicked fallback button: '{t}'")
                        break

        log("  Waiting for AI coach response (~15s)...")
        settle(page, timeout=60000)
        time.sleep(3)
        settle(page, timeout=30000)

        b = body(page)
        log(f"  Post-coach reply: {b[:400].replace(chr(10),' ')}")
        path5 = ss(page, "05_practice_coach_reply")
        check(page, "Step 5 - Practice Tab / Coach Reply", path5)

        # ── STEP 6: Evaluation section ──────────────────────────────────
        log("\n[STEP 6] Evaluation section...")

        # Navigate to evaluation — may be via "Skip to Quiz", "Take Quiz", or after completing practice
        b = body(page)

        # Try to find evaluation navigation
        for pat in [r'Take Quiz|Skip to Quiz|Evaluation|Quiz|Assessment']:
            r = click_btn(page, pat)
            if r:
                settle(page)
                log(f"  Navigated to eval: {r}")
                break

        # If practice isn't done yet, we might need to complete it
        # For the test we can navigate directly via the overview
        b = body(page)
        if not any(x in b for x in ["Question", "Quiz", "Evaluation", "MCQ", "Choose your answer"]):
            log("  Not on evaluation page, attempting via Overview → Take Quiz path")
            # Go back to overview
            r = click_btn(page, r'← Overview|Overview|Back')
            if r:
                settle(page)
            r = click_btn(page, r'Take Quiz|Continue Practice|Quiz')
            if r:
                settle(page)

        b = body(page)
        log(f"  Eval page: {b[:400].replace(chr(10),' ')}")

        # Answer evaluation questions
        log("  Answering evaluation questions...")
        for q_attempt in range(25):
            settle(page, timeout=60000)
            b = body(page)

            # Check for results page
            if any(x in b for x in ["Results", "Your Score", "Coach Note", "Module Complete",
                                     "Well done", "module_score", "You scored"]):
                log(f"  Results reached after {q_attempt} eval attempts")
                break

            # Select radio
            radios = page.locator('input[type="radio"]')
            if radios.count() > 0:
                for ri in range(radios.count()):
                    if not radios.nth(ri).is_checked():
                        try:
                            radios.nth(ri).check(force=True)
                            time.sleep(0.3)
                            break
                        except: pass

            # Fill textarea
            for ta in page.locator('textarea').all():
                if ta.is_visible():
                    try:
                        if not ta.input_value().strip():
                            ta.fill("I would carefully review the AI output for accuracy, verify all facts against reliable sources, check for any confidential client information, and only share with the client after human review and approval.")
                            time.sleep(0.3)
                    except: pass
                    break

            # Click next/submit — prioritize Submit
            clicked = False
            for pat in [r'^Submit\s*(Evaluation|Quiz|Assessment|→|$)', r'^Submit$', r'^Finish$', r'^Next\s*→?$', r'^Next\s+Question']:
                r = click_btn(page, pat)
                if r:
                    clicked = True
                    # Wait longer for AI scoring on Submit
                    if re.search(r'submit|finish', r, re.I):
                        log("  Waiting for AI scoring (~30s)...")
                        settle(page, timeout=120000)
                        time.sleep(5)
                    break

            if not clicked:
                log(f"  q_attempt {q_attempt+1}: no eval button; body: {b[:100].replace(chr(10),' ')}")
                if q_attempt > 8:
                    ss(page, f"06_eval_stuck_{q_attempt}")
                    break

        settle(page, timeout=30000)
        b = body(page)
        log(f"  Final results page: {b[:500].replace(chr(10),' ')}")
        path6 = ss(page, "06_evaluation_results")
        check(page, "Step 6 - Evaluation Results", path6)

        browser.close()

    # ── SUMMARY ──────────────────────────────────────────────────────
    log("\n" + "=" * 60)
    log("AC-3 REGRESSION TEST SUMMARY")
    log("=" * 60)
    all_ok = True
    for r in RESULTS:
        log(f"\n[{r['status']}] {r['step']}")
        log(f"       {r['screenshot']}")
        for i in r['issues']:
            log(f"       {i}")
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
