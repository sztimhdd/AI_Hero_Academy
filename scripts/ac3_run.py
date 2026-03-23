# -*- coding: utf-8 -*-
"""
AC-3 Regression Test — AI Hero Academy
Runs step-by-step through the full user journey.
"""
import sys
import io
import time
import re
import os

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright

SCREENSHOTS = "/c/tmp/ac3_screenshots"
os.makedirs(SCREENSHOTS, exist_ok=True)

RESULTS = []

def ss(page, name):
    path = f"{SCREENSHOTS}/{name}.png"
    page.screenshot(path=path, full_page=True)
    print(f"  [screenshot] {path}", flush=True)
    return path

def settle(page, timeout=30000):
    """Wait for Streamlit to finish rendering."""
    try:
        page.wait_for_selector('[data-testid="stStatusWidget"]', timeout=2000)
        page.wait_for_selector('[data-testid="stStatusWidget"]', state="hidden", timeout=timeout)
    except:
        pass
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except:
        pass
    time.sleep(1.5)

def check(page, step, path):
    """Run AC-3 checks and record result."""
    try:
        text = page.inner_text("body")
    except:
        text = ""

    issues = []

    # EDC check — standalone word
    edc = re.findall(r'\bEDC\b', text)
    if edc:
        issues.append(f"FAIL: 'EDC' found {len(edc)}x — contexts: {[text[max(0,m.start()-30):m.end()+30] for m in re.finditer(r'\bEDC\b', text)][:3]}")

    # Traceback check
    if "Traceback (most recent call last)" in text:
        issues.append("FAIL: Python traceback visible")
    if "StreamlitAPIException" in text:
        issues.append("FAIL: StreamlitAPIException visible")

    # [object Object] check
    if "[object Object]" in text:
        issues.append("FAIL: [object Object] rendered in content")

    # null check (rendered as literal string)
    if re.search(r'\bnull\b', text):
        null_ctx = re.findall(r'.{0,20}null.{0,20}', text)
        issues.append(f"WARN: 'null' found in content: {null_ctx[:2]}")

    status = "PASS"
    if any(i.startswith("FAIL") for i in issues):
        status = "FAIL"
    elif any(i.startswith("WARN") for i in issues):
        status = "WARN"

    RESULTS.append({"step": step, "status": status, "screenshot": path, "issues": issues})
    print(f"  [CHECK] {status} — {step}", flush=True)
    for i in issues:
        print(f"         {i}", flush=True)
    return status

def get_tabs(page):
    tabs = page.locator('button[role="tab"]')
    return {tabs.nth(i).inner_text().strip(): tabs.nth(i) for i in range(tabs.count())}

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-dev-shm-usage"])
        ctx = browser.new_context(viewport={"width": 1400, "height": 900})
        page = ctx.new_page()

        print("=" * 60, flush=True)
        print("AC-3 REGRESSION TEST", flush=True)
        print("=" * 60, flush=True)

        # ─── STEP 1: Initial page load ───────────────────────────────
        print("\n[STEP 1] Load http://localhost:8501", flush=True)
        page.goto("http://localhost:8501", wait_until="domcontentloaded")
        settle(page)
        path1 = ss(page, "01_initial_load")
        body = page.inner_text("body")
        print(f"  Page title: {page.title()}", flush=True)
        print(f"  Body snippet: {body[:250].replace(chr(10), ' ')}", flush=True)
        check(page, "Step 1 - Initial Load (Diagnostic Page)", path1)

        # Verify it's the Diagnostic page
        if "Diagnostic" not in body and "diagnostic" not in body.lower():
            print("  WARNING: Not on Diagnostic page as expected!", flush=True)

        # ─── STEP 2: Complete 12-question diagnostic ─────────────────
        print("\n[STEP 2] Complete the diagnostic (answering questions)...", flush=True)

        q_count = 0
        for attempt in range(40):
            settle(page, timeout=60000)
            body = page.inner_text("body")

            # Done condition: Skills Profile loaded
            if any(x in body for x in ["Skills Profile", "Your AI Skills Profile", "Gap Map", "skill gap"]):
                print(f"  Diagnostic completed after {q_count} questions", flush=True)
                break

            # Done: Home page
            if "Module 1" in body and "Start" in body:
                print(f"  Navigated to Home page after {q_count} questions", flush=True)
                break

            # Find radio buttons and select one
            radios = page.locator('input[type="radio"]')
            if radios.count() > 0:
                # Select the first option that isn't already selected
                for ri in range(radios.count()):
                    if not radios.nth(ri).is_checked():
                        try:
                            radios.nth(ri).check(force=True)
                            time.sleep(0.3)
                            break
                        except:
                            pass

            # Find textarea (written response questions)
            textarea = page.locator('textarea').first
            if textarea.count() > 0 and textarea.is_visible():
                try:
                    current_val = textarea.input_value()
                    if not current_val.strip():
                        textarea.fill("I would use AI tools responsibly by verifying outputs and protecting client confidentiality.")
                        time.sleep(0.3)
                except:
                    pass

            # Find and click the primary action button
            clicked = False
            for btn_text_pat in [r'Next|Submit|Continue|Done|Finish', r'.*']:
                btns = page.locator('[data-testid="stButton"] button')
                for bi in range(btns.count()):
                    btn = btns.nth(bi)
                    try:
                        btext = btn.inner_text().strip()
                        if btext and btn.is_visible() and btn.is_enabled():
                            if re.search(btn_text_pat, btext, re.I):
                                if 'back' not in btext.lower() and 'prev' not in btext.lower():
                                    btn.click()
                                    q_count += 1
                                    print(f"  Clicked '{btext}' (attempt {attempt+1})", flush=True)
                                    clicked = True
                                    break
                    except:
                        pass
                if clicked:
                    break

            if not clicked:
                print(f"  Attempt {attempt+1}: no clickable button found, body: {body[:150].replace(chr(10), ' ')}", flush=True)
                if attempt > 5:
                    # Take diagnostic screenshot and move on
                    ss(page, f"02_stuck_{attempt}")
                    break

        settle(page, timeout=60000)
        path2 = ss(page, "02_after_diagnostic")
        body = page.inner_text("body")
        print(f"  Post-diagnostic body: {body[:300].replace(chr(10), ' ')}", flush=True)
        check(page, "Step 2 - After Diagnostic", path2)

        # ─── STEP 3: Navigate to Home → Module 1 → Overview ──────────
        print("\n[STEP 3] Navigate to Module 1 Overview...", flush=True)
        settle(page)
        body = page.inner_text("body")

        # If on Skills Profile, look for "Go to Home" or "Start Learning"
        start_btns = page.locator('[data-testid="stButton"] button').filter(
            has_text=re.compile(r'Home|Start Learning|Begin|Module 1|Go to', re.I)
        )
        if start_btns.count() > 0:
            btn_text = start_btns.first.inner_text()
            print(f"  Clicking '{btn_text}'", flush=True)
            start_btns.first.click()
            settle(page, timeout=30000)

        # Check if we're now on Home, look for Module 1
        body = page.inner_text("body")
        mod1_btn = page.locator('[data-testid="stButton"] button').filter(
            has_text=re.compile(r'Module 1|Start|Open', re.I)
        )
        if mod1_btn.count() > 0:
            print(f"  Clicking Module 1 / Start button: '{mod1_btn.first.inner_text()}'", flush=True)
            mod1_btn.first.click()
            settle(page, timeout=30000)

        body = page.inner_text("body")
        print(f"  Body after navigation: {body[:300].replace(chr(10), ' ')}", flush=True)

        # Ensure we're on Overview tab (should be default)
        tabs = get_tabs(page)
        print(f"  Available tabs: {list(tabs.keys())}", flush=True)
        if "Overview" in tabs:
            tabs["Overview"].click()
            settle(page)

        path3 = ss(page, "03_module1_overview")
        check(page, "Step 3 - Module 1 Overview", path3)

        # ─── STEP 4: Reading tab → Concept section ───────────────────
        print("\n[STEP 4] Reading tab...", flush=True)
        tabs = get_tabs(page)
        reading_key = next((k for k in tabs if 'read' in k.lower()), None)
        if reading_key:
            print(f"  Clicking tab: '{reading_key}'", flush=True)
            tabs[reading_key].click()
            settle(page)
        else:
            print(f"  No Reading tab found. Tabs: {list(tabs.keys())}", flush=True)

        body = page.inner_text("body")
        print(f"  Reading content length: {len(body)}", flush=True)
        print(f"  Reading content snippet: {body[:400].replace(chr(10), ' ')}", flush=True)

        # Check for empty reading content
        extra_issues = []
        if len(body.strip()) < 300:
            extra_issues.append("FAIL: Reading content appears empty (< 300 chars)")

        path4 = ss(page, "04_reading_concept")
        check(page, "Step 4 - Reading Tab / Concept Section", path4)
        if extra_issues:
            RESULTS[-1]['issues'].extend(extra_issues)
            RESULTS[-1]['status'] = "FAIL"
            for i in extra_issues:
                print(f"  {i}", flush=True)

        # ─── STEP 5: Practice tab → Task 1 → submit response ─────────
        print("\n[STEP 5] Practice tab — Task 1...", flush=True)
        tabs = get_tabs(page)
        practice_key = next((k for k in tabs if 'pract' in k.lower()), None)
        if practice_key:
            print(f"  Clicking tab: '{practice_key}'", flush=True)
            tabs[practice_key].click()
            settle(page)
        else:
            print(f"  No Practice tab found. Tabs: {list(tabs.keys())}", flush=True)

        body = page.inner_text("body")
        print(f"  Practice page snippet: {body[:400].replace(chr(10), ' ')}", flush=True)

        # Fill textarea
        textarea = page.locator('textarea').first
        if textarea.count() > 0 and textarea.is_visible():
            textarea.fill("I would use the SAFE method to check the prompt")
            print("  Filled Task 1 response", flush=True)
            time.sleep(0.5)
        else:
            print("  WARNING: No textarea found for Practice", flush=True)

        # Click Send button
        send_btn = page.locator('[data-testid="stButton"] button').filter(
            has_text=re.compile(r'Send|Submit|Reply|Go', re.I)
        )
        if send_btn.count() > 0:
            print(f"  Clicking '{send_btn.first.inner_text()}'", flush=True)
            send_btn.first.click()
        else:
            # Try any primary button
            all_btns = page.locator('[data-testid="stButton"] button')
            print(f"  Buttons available: {[all_btns.nth(i).inner_text() for i in range(min(all_btns.count(), 5))]}", flush=True)
            if all_btns.count() > 0:
                all_btns.first.click()

        print("  Waiting for AI coach response...", flush=True)
        # AI response takes several seconds
        settle(page, timeout=90000)
        time.sleep(4)
        settle(page, timeout=30000)

        body = page.inner_text("body")
        print(f"  Post-response snippet: {body[:400].replace(chr(10), ' ')}", flush=True)
        path5 = ss(page, "05_practice_coach_reply")
        check(page, "Step 5 - Practice Tab / Coach Reply", path5)

        # ─── STEP 6: Evaluation tab → answer all 4 → Results ─────────
        print("\n[STEP 6] Evaluation tab...", flush=True)
        tabs = get_tabs(page)
        print(f"  Available tabs: {list(tabs.keys())}", flush=True)
        eval_key = next((k for k in tabs if any(x in k.lower() for x in ['eval', 'quiz', 'assess', 'test'])), None)
        if eval_key:
            print(f"  Clicking tab: '{eval_key}'", flush=True)
            tabs[eval_key].click()
            settle(page)
        else:
            print(f"  No Evaluation tab found.", flush=True)

        body = page.inner_text("body")
        print(f"  Eval page snippet: {body[:400].replace(chr(10), ' ')}", flush=True)

        # Answer MCQ questions
        print("  Answering evaluation MCQs...", flush=True)
        for q_attempt in range(20):
            settle(page)
            body = page.inner_text("body")

            # Check if we've reached Results
            if any(x in body for x in ["Results", "Your Score", "Coach Note", "Module Complete", "Well done"]):
                print(f"  Results page reached after {q_attempt} answer attempts", flush=True)
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
                        except:
                            pass

            # Fill textarea if present (performance task)
            textarea = page.locator('textarea').first
            if textarea.count() > 0 and textarea.is_visible():
                current = textarea.input_value()
                if not current.strip():
                    textarea.fill("I would carefully review the AI output for accuracy, verify all facts against reliable sources, check for any confidential client information, and only share with the client after human review and approval.")
                    time.sleep(0.3)

            # Click Next/Submit
            clicked = False
            for btn_text_pat in [r'Submit|Finish|Complete|Done', r'Next|Continue', r'.*']:
                btns = page.locator('[data-testid="stButton"] button')
                for bi in range(btns.count()):
                    btn = btns.nth(bi)
                    try:
                        btext = btn.inner_text().strip()
                        if btext and btn.is_visible() and btn.is_enabled():
                            if re.search(btn_text_pat, btext, re.I):
                                if 'back' not in btext.lower():
                                    btn.click()
                                    print(f"  Clicked '{btext}' (q_attempt {q_attempt+1})", flush=True)
                                    clicked = True
                                    # Wait longer for submit (AI scoring)
                                    if re.search(r'Submit|Finish|Complete', btext, re.I):
                                        print("  Waiting for AI evaluation scoring...", flush=True)
                                        settle(page, timeout=120000)
                                        time.sleep(5)
                                    break
                    except:
                        pass
                if clicked:
                    break

            if not clicked:
                print(f"  q_attempt {q_attempt+1}: no button to click", flush=True)

        settle(page, timeout=30000)
        body = page.inner_text("body")
        print(f"  Results page snippet: {body[:500].replace(chr(10), ' ')}", flush=True)
        path6 = ss(page, "06_evaluation_results")
        check(page, "Step 6 - Evaluation Results", path6)

        browser.close()

    # ─── FINAL SUMMARY ───────────────────────────────────────────────
    print("\n" + "=" * 60, flush=True)
    print("AC-3 REGRESSION TEST SUMMARY", flush=True)
    print("=" * 60, flush=True)

    all_ok = True
    for r in RESULTS:
        print(f"\n[{r['status']}] {r['step']}", flush=True)
        print(f"       {r['screenshot']}", flush=True)
        for issue in r['issues']:
            print(f"       {issue}", flush=True)
        if r['status'] == "FAIL":
            all_ok = False

    print("\n" + "=" * 60, flush=True)
    fails = [r for r in RESULTS if r['status'] == "FAIL"]
    warns = [r for r in RESULTS if r['status'] == "WARN"]
    if all_ok:
        print(f"OVERALL: PASS ({len(warns)} warning(s))", flush=True)
    else:
        print(f"OVERALL: FAIL — {len(fails)} failure(s), {len(warns)} warning(s)", flush=True)
    print("=" * 60, flush=True)
    print(f"Screenshots: {SCREENSHOTS}", flush=True)

if __name__ == "__main__":
    run()
