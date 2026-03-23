# -*- coding: utf-8 -*-
"""
AC-3 Regression Test for AI Hero Academy
Tests the full user journey from Diagnostic through Module 1 Results.
Checks for: no "EDC" text, no empty fields, no None/null, no tracebacks.
"""
import sys
import io
import time
import re
import os
from playwright.sync_api import sync_playwright, Page, expect

# Force UTF-8 output to avoid Windows cp1252 encoding errors
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCREENSHOTS_DIR = "/c/tmp/ac3_screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

RESULTS = []

def screenshot(page: Page, name: str):
    path = f"{SCREENSHOTS_DIR}/{name}.png"
    page.screenshot(path=path, full_page=True)
    return path

def check_page(page: Page, step_name: str, screenshot_path: str):
    """Run all AC-3 checks on the current page state."""
    content = page.content()
    text = page.inner_text("body") if page.locator("body").count() > 0 else content

    issues = []

    # Check 1: No "EDC" text
    # Look for EDC as standalone text (not part of another word like "HEDGE" or "CODEC")
    edc_matches = re.findall(r'\bEDC\b', text)
    if edc_matches:
        issues.append(f"FAIL - Found 'EDC' text ({len(edc_matches)} occurrences): {edc_matches[:3]}")

    # Check 2: No Python tracebacks
    if "Traceback (most recent call last)" in content:
        issues.append("FAIL - Python traceback visible in page")
    if "StreamlitAPIException" in content:
        issues.append("FAIL - StreamlitAPIException visible")

    # Check 3: No None/null/[object Object] rendered as content
    # We check in the visible text specifically
    if re.search(r'\bNone\b', text) and "NoneType" not in text:
        # Allow "None" if it's part of Python error messages, but flag standalone
        none_contexts = re.findall(r'.{0,20}None.{0,20}', text)
        # Filter out common false positives
        bad_none = [c for c in none_contexts if not any(x in c for x in ['NoneType', 'or None', 'if None', '= None', 'is None', 'not None', 'Optional'])]
        if bad_none:
            issues.append(f"WARN - 'None' rendered in content: {bad_none[:2]}")

    if "[object Object]" in text:
        issues.append("FAIL - '[object Object]' rendered in content")

    # Check 4: No empty content fields (blank scenario text, reading cards, questions)
    # Look for suspicious empty sections — elements with no text content
    empty_headers = page.locator("h1:empty, h2:empty, h3:empty").count()
    if empty_headers > 0:
        issues.append(f"WARN - {empty_headers} empty header elements found")

    if issues:
        status = "FAIL" if any(i.startswith("FAIL") for i in issues) else "WARN"
        RESULTS.append({
            "step": step_name,
            "status": status,
            "screenshot": screenshot_path,
            "issues": issues
        })
    else:
        RESULTS.append({
            "step": step_name,
            "status": "PASS",
            "screenshot": screenshot_path,
            "issues": []
        })

def wait_for_streamlit(page: Page, timeout=30000):
    """Wait for Streamlit to finish loading."""
    # Wait for the running indicator to disappear
    try:
        page.wait_for_selector('[data-testid="stStatusWidget"]', timeout=3000)
        page.wait_for_selector('[data-testid="stStatusWidget"]', state="hidden", timeout=timeout)
    except:
        pass
    # Also wait for network to be idle
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except:
        pass
    time.sleep(1.5)

def click_and_wait(page: Page, selector: str, timeout=10000):
    """Click an element and wait for Streamlit to settle."""
    page.locator(selector).first.click(timeout=timeout)
    wait_for_streamlit(page)

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()

        print("=" * 60)
        print("AC-3 REGRESSION TEST — AI Hero Academy")
        print("=" * 60)

        # ── STEP 1: Navigate to app ──────────────────────────────────
        print("\n[Step 1] Navigating to http://localhost:8501...")
        page.goto("http://localhost:8501", wait_until="domcontentloaded")
        wait_for_streamlit(page)
        path = screenshot(page, "01_home_page")

        # Verify we're on Diagnostic page (user was reset to RM with no diagnostic)
        body_text = page.inner_text("body")
        print(f"  Page title area: {body_text[:200]}")
        check_page(page, "Step 1 - App Home / Diagnostic Page", path)
        print(f"  → {RESULTS[-1]['status']} | Screenshot: {path}")
        if RESULTS[-1]['issues']:
            for issue in RESULTS[-1]['issues']:
                print(f"     {issue}")

        # ── STEP 2: Complete 12-question diagnostic ──────────────────
        print("\n[Step 2] Completing 12-question diagnostic...")

        # Check if we're on the Diagnostic page
        if "Diagnostic" not in body_text and "diagnostic" not in body_text.lower():
            print("  WARNING: May not be on Diagnostic page. Current content snippet:")
            print(f"  {body_text[:500]}")

        questions_answered = 0
        max_attempts = 20

        for attempt in range(max_attempts):
            # Wait for radio buttons to appear
            time.sleep(1)
            wait_for_streamlit(page)

            body_text = page.inner_text("body")

            # Check if we're done with diagnostic (Skills Profile loaded)
            if any(x in body_text for x in ["Skills Profile", "Gap Map", "Your AI Skills", "Domain Score"]):
                print(f"  Diagnostic complete after {questions_answered} questions answered")
                break

            # Look for radio button options
            radio_buttons = page.locator('input[type="radio"]')
            radio_count = radio_buttons.count()

            if radio_count > 0:
                # Click first available radio (first option)
                try:
                    # Use the label associated with the first radio
                    first_radio_label = page.locator('label').filter(has=page.locator('input[type="radio"]')).first
                    if first_radio_label.count() > 0:
                        first_radio_label.click()
                    else:
                        radio_buttons.first.click()
                    time.sleep(0.5)
                except Exception as e:
                    print(f"  Radio click error: {e}")

            # Look for Next/Submit button
            next_btn = page.locator('button').filter(has_text=re.compile(r'Next|Submit|Continue', re.I))
            if next_btn.count() > 0:
                try:
                    next_btn.first.click()
                    questions_answered += 1
                    print(f"  Answered question {questions_answered}")
                    wait_for_streamlit(page, timeout=45000)
                except Exception as e:
                    print(f"  Button click error: {e}")
                    time.sleep(2)
            else:
                # Try clicking any stButton
                st_buttons = page.locator('[data-testid="stButton"] button')
                if st_buttons.count() > 0:
                    btn_texts = [st_buttons.nth(i).inner_text() for i in range(min(st_buttons.count(), 5))]
                    print(f"  Available buttons: {btn_texts}")
                    # Click the first non-Back button
                    for i in range(st_buttons.count()):
                        btn_text = st_buttons.nth(i).inner_text()
                        if btn_text.strip() and 'back' not in btn_text.lower():
                            st_buttons.nth(i).click()
                            questions_answered += 1
                            print(f"  Clicked '{btn_text}' (question {questions_answered})")
                            wait_for_streamlit(page, timeout=45000)
                            break
                else:
                    print(f"  Attempt {attempt+1}: No buttons found, waiting...")
                    time.sleep(2)

                    # If we've been stuck for a while with no progress, take diagnostic screenshot
                    if attempt > 5 and questions_answered == 0:
                        stuck_path = screenshot(page, f"02_stuck_{attempt}")
                        print(f"  Stuck screenshot: {stuck_path}")
                        print(f"  Body snippet: {body_text[:300]}")
                        break

        path = screenshot(page, "02_after_diagnostic")
        body_text = page.inner_text("body")
        check_page(page, "Step 2 - After Diagnostic (12 questions)", path)
        print(f"  → {RESULTS[-1]['status']} | Screenshot: {path}")
        if RESULTS[-1]['issues']:
            for issue in RESULTS[-1]['issues']:
                print(f"     {issue}")
        print(f"  Page content snippet: {body_text[:300]}")

        # ── STEP 3: Skills Profile → Home → Module 1 → Overview ─────
        print("\n[Step 3] Navigating to Home → Module 1 → Overview...")

        # First, navigate to Home if we have a sidebar navigation
        wait_for_streamlit(page)
        body_text = page.inner_text("body")

        # Look for Home button/link
        home_link = page.locator('a, button').filter(has_text=re.compile(r'^Home$', re.I))
        if home_link.count() > 0:
            home_link.first.click()
            wait_for_streamlit(page)
            print("  Clicked Home")
        else:
            print("  No Home link found, may already be on Skills Profile")

        # Look for "Start Learning" or module 1 button
        start_btn = page.locator('button, a').filter(has_text=re.compile(r'Start Learning|Module 1|Begin', re.I))
        if start_btn.count() > 0:
            start_btn.first.click()
            wait_for_streamlit(page)
            print("  Clicked Start Learning / Module 1")

        path = screenshot(page, "03_module1_overview")
        body_text = page.inner_text("body")
        check_page(page, "Step 3 - Module 1 Overview", path)
        print(f"  → {RESULTS[-1]['status']} | Screenshot: {path}")
        if RESULTS[-1]['issues']:
            for issue in RESULTS[-1]['issues']:
                print(f"     {issue}")
        print(f"  Page content snippet: {body_text[:300]}")

        # ── STEP 4: Reading tab → Concept section ───────────────────
        print("\n[Step 4] Navigating to Reading tab...")

        # Click Reading tab
        reading_tab = page.locator('[data-testid="stTab"], button[role="tab"]').filter(has_text=re.compile(r'Reading', re.I))
        if reading_tab.count() > 0:
            reading_tab.first.click()
            wait_for_streamlit(page)
            print("  Clicked Reading tab")
        else:
            # Try finding tab by text
            all_tabs = page.locator('button[role="tab"]')
            tab_count = all_tabs.count()
            print(f"  Found {tab_count} tabs")
            for i in range(tab_count):
                tab_text = all_tabs.nth(i).inner_text()
                print(f"    Tab {i}: {tab_text}")
                if 'read' in tab_text.lower():
                    all_tabs.nth(i).click()
                    wait_for_streamlit(page)
                    print(f"  Clicked tab: {tab_text}")
                    break

        # Scroll to Concept section if it exists
        concept = page.locator('text=Concept').first
        if concept.count() > 0:
            concept.scroll_into_view_if_needed()

        path = screenshot(page, "04_reading_concept")
        body_text = page.inner_text("body")
        check_page(page, "Step 4 - Reading Tab / Concept Section", path)
        print(f"  → {RESULTS[-1]['status']} | Screenshot: {path}")
        if RESULTS[-1]['issues']:
            for issue in RESULTS[-1]['issues']:
                print(f"     {issue}")

        # Check for empty reading content
        if len(body_text.strip()) < 200:
            RESULTS[-1]['status'] = "FAIL"
            RESULTS[-1]['issues'].append("FAIL - Reading content appears empty (< 200 chars)")
            print("  FAIL - Reading content appears empty")

        print(f"  Content length: {len(body_text)} chars")

        # ── STEP 5: Practice tab → Task 1 response ──────────────────
        print("\n[Step 5] Navigating to Practice tab and submitting Task 1...")

        practice_tab = page.locator('button[role="tab"]').filter(has_text=re.compile(r'Practice', re.I))
        if practice_tab.count() > 0:
            practice_tab.first.click()
            wait_for_streamlit(page)
            print("  Clicked Practice tab")

        # Wait for the task to appear and find the text area
        time.sleep(2)
        wait_for_streamlit(page)

        body_text = page.inner_text("body")
        print(f"  Practice page snippet: {body_text[:400]}")

        # Find textarea and type response
        textarea = page.locator('textarea').first
        if textarea.count() > 0:
            textarea.click()
            textarea.fill("I would use the SAFE method to check the prompt")
            print("  Filled in Task 1 response")
            time.sleep(0.5)
        else:
            print("  WARNING: No textarea found for Practice")

        # Click Send/Submit button
        send_btn = page.locator('button').filter(has_text=re.compile(r'Send|Submit|Reply', re.I))
        if send_btn.count() > 0:
            send_btn.first.click()
            print("  Clicked Send button")
            # Wait for AI coach response (may take several seconds)
            wait_for_streamlit(page, timeout=60000)
            time.sleep(3)  # Extra wait for AI response
            wait_for_streamlit(page, timeout=30000)
        else:
            # Try the stButton
            st_buttons = page.locator('[data-testid="stButton"] button')
            btn_count = st_buttons.count()
            if btn_count > 0:
                btn_texts = [st_buttons.nth(i).inner_text() for i in range(min(btn_count, 5))]
                print(f"  Available buttons: {btn_texts}")
                st_buttons.first.click()
                wait_for_streamlit(page, timeout=60000)
                time.sleep(3)
                wait_for_streamlit(page, timeout=30000)

        path = screenshot(page, "05_practice_coach_reply")
        body_text = page.inner_text("body")
        check_page(page, "Step 5 - Practice Tab / Coach Reply", path)
        print(f"  → {RESULTS[-1]['status']} | Screenshot: {path}")
        if RESULTS[-1]['issues']:
            for issue in RESULTS[-1]['issues']:
                print(f"     {issue}")
        print(f"  Content snippet: {body_text[:400]}")

        # ── STEP 6: Evaluation tab → answer all 4 questions → Results ─
        print("\n[Step 6] Navigating to Evaluation tab...")

        eval_tab = page.locator('button[role="tab"]').filter(has_text=re.compile(r'Eval|Quiz|Assessment', re.I))
        if eval_tab.count() > 0:
            eval_tab.first.click()
            wait_for_streamlit(page)
            print("  Clicked Evaluation tab")
        else:
            # Try to navigate to it
            all_tabs = page.locator('button[role="tab"]')
            tab_count = all_tabs.count()
            print(f"  Found {tab_count} tabs for evaluation step")
            for i in range(tab_count):
                tab_text = all_tabs.nth(i).inner_text()
                print(f"    Tab {i}: {tab_text}")
                if any(x in tab_text.lower() for x in ['eval', 'quiz', 'assess', 'test']):
                    all_tabs.nth(i).click()
                    wait_for_streamlit(page)
                    print(f"  Clicked: {tab_text}")
                    break

        time.sleep(2)
        wait_for_streamlit(page)

        # Answer all questions (MCQs)
        print("  Answering evaluation questions...")
        for q_num in range(1, 5):
            radio_buttons = page.locator('input[type="radio"]')
            radio_count = radio_buttons.count()

            if radio_count > 0:
                # Click first option for each question
                try:
                    labels = page.locator('label').filter(has=page.locator('input[type="radio"]'))
                    if labels.count() > 0:
                        labels.first.click()
                        time.sleep(0.5)
                except Exception as e:
                    print(f"  Q{q_num} radio error: {e}")

            # Click Next if available, otherwise continue
            next_btn = page.locator('button').filter(has_text=re.compile(r'Next|Continue', re.I))
            if next_btn.count() > 0:
                next_btn.first.click()
                wait_for_streamlit(page)
                print(f"  Answered Q{q_num}")

        # Now fill in the performance task (last question - likely a textarea)
        textarea = page.locator('textarea').first
        if textarea.count() > 0:
            textarea.click()
            textarea.fill("I would carefully review the AI-generated content for accuracy, check all facts against verified sources, and ensure no confidential client information was included before sharing with the client.")
            print("  Filled performance task response")
            time.sleep(0.5)

        # Submit the evaluation
        submit_btn = page.locator('button').filter(has_text=re.compile(r'Submit|Finish|Complete', re.I))
        if submit_btn.count() > 0:
            submit_btn.first.click()
            print("  Clicked Submit")
            # Wait for AI scoring (takes longer)
            wait_for_streamlit(page, timeout=90000)
            time.sleep(5)
            wait_for_streamlit(page, timeout=30000)
        else:
            st_buttons = page.locator('[data-testid="stButton"] button')
            if st_buttons.count() > 0:
                btn_texts = [st_buttons.nth(i).inner_text() for i in range(min(st_buttons.count(), 5))]
                print(f"  Available buttons for submit: {btn_texts}")
                # Look for submit-like button
                for i in range(st_buttons.count()):
                    btn_text = st_buttons.nth(i).inner_text().lower()
                    if any(x in btn_text for x in ['submit', 'finish', 'complete', 'evaluate']):
                        st_buttons.nth(i).click()
                        wait_for_streamlit(page, timeout=90000)
                        time.sleep(5)
                        wait_for_streamlit(page, timeout=30000)
                        print(f"  Clicked: {btn_text}")
                        break

        path = screenshot(page, "06_evaluation_results")
        body_text = page.inner_text("body")
        check_page(page, "Step 6 - Evaluation Results", path)
        print(f"  → {RESULTS[-1]['status']} | Screenshot: {path}")
        if RESULTS[-1]['issues']:
            for issue in RESULTS[-1]['issues']:
                print(f"     {issue}")
        print(f"  Results content snippet: {body_text[:500]}")

        browser.close()

    # ── FINAL SUMMARY ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("AC-3 REGRESSION TEST SUMMARY")
    print("=" * 60)

    all_pass = True
    for r in RESULTS:
        status_icon = "PASS" if r['status'] == "PASS" else ("WARN" if r['status'] == "WARN" else "FAIL")
        print(f"\n[{status_icon}] {r['step']}")
        print(f"       Screenshot: {r['screenshot']}")
        if r['issues']:
            for issue in r['issues']:
                print(f"       {issue}")
            if r['status'] == "FAIL":
                all_pass = False

    print("\n" + "=" * 60)
    if all_pass:
        print("OVERALL: PASS — No critical failures detected")
    else:
        fails = [r for r in RESULTS if r['status'] == "FAIL"]
        print(f"OVERALL: FAIL — {len(fails)} step(s) failed")
    print("=" * 60)
    print(f"\nScreenshots saved to: {SCREENSHOTS_DIR}")

if __name__ == "__main__":
    run_test()
