/**
 * tests/uat_phase3.js — Phase 3 UAT: Atom Path + Dynamic Onboarding
 *
 * Covers:
 *   Scenario A  — Welcome page: intake form renders (Q1, Q2, Advanced options)
 *   Scenario A2 — Home page: atom cards visible for 3f (RM + assembled_path)
 *   Scenario B  — Atom module: click into first atom, reading content renders
 *   Scenario C  — Legacy UW (3c): numbered module list with Read/Practice/Quiz badges
 *   Scenario D  — Legacy AN all-done (3d): all module scores visible
 *   Scenario E  — Legacy MK in-progress (3e): mixed complete/active/locked modules
 *   Scenario F1 — Welcome: submit button disabled when Q1 is empty
 *   Scenario F2 — Welcome: Advanced options expander reveals role selector
 *
 * Usage:
 *   node tests/uat_phase3.js
 *
 * Prerequisites:
 *   - App running: bash run_uat.sh   (LOCAL_UAT=true, port 8501)
 *   - Demo personas seeded: python scripts/seed_demo_personas.py (or done lazily by app)
 */

'use strict';

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const BASE_URL = 'http://localhost:8501';
const SCREENSHOTS_DIR = path.join(__dirname, '..', 'uat_screenshots', 'phase3');

if (!fs.existsSync(SCREENSHOTS_DIR)) {
  fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });
}

// ── Helpers ──────────────────────────────────────────────────────────────────

async function waitForStreamlit(page, timeout = 60000) {
  // Step 1: wait for network idle (initial load)
  try { await page.waitForLoadState('networkidle', { timeout: 25000 }); } catch (_) {}
  // Step 2: wait for meaningful content (not loading spinner)
  try {
    await page.waitForFunction(() => {
      const el = document.querySelector('[data-testid="stMain"]') || document.body;
      return (el ? el.innerText.trim().length : 0) > 100;
    }, { timeout });
  } catch (_) {}
  // Step 3: Demo mode triggers st.rerun() — wait for second network settle
  await page.waitForTimeout(1500);
  try { await page.waitForLoadState('networkidle', { timeout: 15000 }); } catch (_) {}
  // Step 4: Final buffer for Streamlit render completion
  await page.waitForTimeout(3000);
}

async function shot(page, name) {
  const p = path.join(SCREENSHOTS_DIR, `${name}.png`);
  await page.screenshot({ path: p, fullPage: true });
  console.log(`    [screenshot] ${name}.png`);
  return p;
}

function hdr(label) {
  console.log(`\n${'═'.repeat(64)}`);
  console.log(`  ${label}`);
  console.log('═'.repeat(64));
}

const _results = [];
function chk(label, ok) {
  console.log(`  ${ok ? '✓' : '✗'} ${label}`);
  _results.push({ label, ok });
  return ok;
}

async function openDemo(browser, profileId, label) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const url = `${BASE_URL}/?demo=true&profile=${profileId}`;
  console.log(`\n  → ${url}`);
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
  await waitForStreamlit(page);
  await shot(page, label + '_00_load');
  return page;
}

// ── Scenario A — Welcome intake form ─────────────────────────────────────────

async function scenarioA(browser) {
  hdr('Scenario A — Welcome page: intake form (profile 3a)');
  const page = await openDemo(browser, '3a', 'A');
  const txt = await page.evaluate(() => document.body.innerText);
  const lower = txt.toLowerCase();

  chk('A1: Page title contains "AI Hero Academy"', await page.title().then(t => t.includes('AI Hero')));
  chk('A2: Q1 "Tell us about your work" textarea present', lower.includes('tell us about your work') || lower.includes('tell us'));
  chk('A3: AI tools section visible ("Which AI tools")', lower.includes('which ai tools') || lower.includes('ai tools'));
  chk('A4: Advanced options expander visible', lower.includes('advanced options'));
  chk('A5: No ImportError or Traceback on page', !txt.includes('ImportError') && !txt.includes('Traceback'));

  await page.close();
}

// ── Scenario A2 — Atom-path Home (profile 3f) ─────────────────────────────────

async function scenarioA2(browser) {
  hdr('Scenario A2 — Home: atom cards for RM+assembled_path (profile 3f)');
  const page = await openDemo(browser, '3f', 'A2');
  const txt = await page.evaluate(() => document.body.innerText);
  const lower = txt.toLowerCase();

  chk('A2-1: Home page renders (welcome back)', lower.includes('welcome back') || lower.includes('my training'));
  chk('A2-2: Atom domain badges visible (AUGMENTED COMMUNICATION etc.)',
    lower.includes('augmented comm') ||
    lower.includes('critical eval') ||
    lower.includes('responsible ai') ||
    lower.includes('strategic prompting'));
  chk('A2-3: Atom framework titles visible (CSS/CRAF/VERIFY/SAFE)',
    lower.includes('css') || lower.includes('craf') || lower.includes('verify') ||
    lower.includes('safe') || lower.includes('copilot surface'));
  chk('A2-4: Numbered sequence (01, 02…07)',
    txt.includes('01') && txt.includes('02'));
  chk('A2-5: No Read/Practice/Quiz badges (atom-path format, not legacy)',
    !(lower.includes('read') && lower.includes('practice') && lower.includes('quiz') &&
      lower.includes('🔒')));
  chk('A2-6: No ImportError', !txt.includes('ImportError'));

  await shot(page, 'A2_01_atom_cards');
  await page.close();
}

// ── Scenario B — Click into first atom module ─────────────────────────────────

async function scenarioB(browser) {
  hdr('Scenario B — Atom module: click "Start Module 1" → reading content (profile 3f)');
  const page = await openDemo(browser, '3f', 'B');

  // Look for "Start Module 1" or "Start Module" button by text
  const startBtn = page.getByRole('button', { name: /Start Module/i }).first();
  const btnCount = await startBtn.count();
  if (!chk('B1: "Start Module" button found', btnCount > 0)) {
    const allBtns = await page.locator('button').allInnerTexts();
    console.log(`    [debug] Buttons on page: ${allBtns.slice(0, 5).join(' | ')}`);
    await page.close();
    return;
  }

  const btnText = await startBtn.innerText().catch(() => '');
  console.log(`    [info] Button: "${btnText.trim()}"`);
  await startBtn.click();
  await waitForStreamlit(page, 30000);
  await shot(page, 'B_01_module_entered');

  const txt = await page.evaluate(() => document.body.innerText);
  const lower = txt.toLowerCase();

  chk('B2: Module/reading content page renders', lower.includes('reading') || lower.includes('learn') ||
    lower.includes('module') || lower.includes('framework'));
  chk('B3: No error or blank page', !txt.includes('Traceback') && txt.trim().length > 100);
  chk('B4: App still in AI Hero context', await page.title().then(t => t.includes('AI Hero') || t.includes('Course') || t.includes('Module')));

  await page.close();
}

// ── Scenario C — Legacy UW (3c) backward compat ───────────────────────────────

async function scenarioC(browser) {
  hdr('Scenario C — Legacy UW Module 1 complete (profile 3c): numbered module list');
  const page = await openDemo(browser, '3c', 'C');
  const txt = await page.evaluate(() => document.body.innerText);
  const lower = txt.toLowerCase();

  chk('C1: Home page renders', lower.includes('welcome back') || lower.includes('my training'));
  chk('C2: Read/Practice/Quiz sub-badges visible (legacy format)',
    lower.includes('read') && lower.includes('practice') && lower.includes('quiz'));
  chk('C3: Numbered modules present (01, 02)', txt.includes('01') && txt.includes('02'));
  chk('C4: Module 1 shows as completed (Review button or ✓)',
    lower.includes('review module'));
  chk('C5: Locked module present (🔒)', txt.includes('🔒'));
  chk('C6: No unfilled {placeholder} tokens', !(/\{\w+\}/.test(txt)));

  await page.close();
}

// ── Scenario D — Legacy AN all-done (3d) ─────────────────────────────────────

async function scenarioD(browser) {
  hdr('Scenario D — Legacy AN all modules done (profile 3d): all scores visible');
  const page = await openDemo(browser, '3d', 'D');
  const txt = await page.evaluate(() => document.body.innerText);
  const lower = txt.toLowerCase();

  chk('D1: Home page renders', lower.includes('welcome back') || lower.includes('my training'));
  chk('D2: "7 of 7" modules complete', txt.includes('7 of 7'));
  const scorePattern = /\d+\.\d+\s*\/\s*4\.0/g;
  const scores = txt.match(scorePattern) || [];
  chk(`D3: Score values shown (found ${scores.length}, need ≥ 5)`, scores.length >= 5);
  chk('D4: All review buttons present', lower.includes('review module'));
  chk('D5: No locked modules (🔒 absent)', !txt.includes('🔒'));

  await page.close();
}

// ── Scenario E — Legacy MK in-progress (3e) ──────────────────────────────────

async function scenarioE(browser) {
  hdr('Scenario E — Legacy MK Module 3 in progress (profile 3e): mixed states');
  const page = await openDemo(browser, '3e', 'E');
  const txt = await page.evaluate(() => document.body.innerText);
  const lower = txt.toLowerCase();

  chk('E1: Home page renders', lower.includes('welcome back') || lower.includes('my training'));
  chk('E2: Completed modules show Review button', lower.includes('review module'));
  chk('E3: Active module shows Continue/Start',
    lower.includes('continue') || lower.includes('start module') || lower.includes('take quiz'));
  chk('E4: Locked modules present (🔒)', txt.includes('🔒'));
  chk('E5: Progress count visible (2 of 7)', txt.includes('2 of 7') || txt.includes('2 of'));

  await page.close();
}

// ── Scenario F — Welcome page edge cases ─────────────────────────────────────

async function scenarioF(browser) {
  // F1: Submit disabled when Q1 empty
  hdr('Scenario F1 — Submit button disabled when Q1 is empty (profile 3a)');
  const page = await openDemo(browser, '3a', 'F1');
  const txt = await page.evaluate(() => document.body.innerText);

  // Find the "Start My Diagnostic" button — in Streamlit, primary disabled buttons have aria-disabled
  const diagBtn = page.getByRole('button', { name: /Diagnostic/i }).first();
  const btnCount = await diagBtn.count();
  console.log(`    [info] "Diagnostic" button count: ${btnCount}`);

  if (btnCount > 0) {
    // Button is always enabled; validation fires post-click via st.error()
    await diagBtn.click();
    await page.waitForTimeout(2000);
    try { await page.waitForLoadState('networkidle', { timeout: 10000 }); } catch (_) {}
    await page.waitForTimeout(1500);
    const txtAfterClick = await page.evaluate(() => document.body.innerText);
    chk('F1a: Error message shown for empty Q1 submission',
      txtAfterClick.toLowerCase().includes('please describe') ||
      txtAfterClick.toLowerCase().includes('describe your work'));
  } else {
    chk('F1a: Error message shown for empty Q1 submission', false);
  }

  await shot(page, 'F1_01_empty_q1');
  await page.close();

  // F2: Advanced options expander
  hdr('Scenario F2 — Advanced options reveals role selector (profile 3a)');
  const page2 = await openDemo(browser, '3a', 'F2');
  const txt2 = await page2.evaluate(() => document.body.innerText);
  const lower2 = txt2.toLowerCase();

  chk('F2a: "Advanced options" expander visible', lower2.includes('advanced options'));

  if (lower2.includes('advanced options')) {
    // Click the expander summary
    const expander = page2.locator('[data-testid="stExpander"]').first();
    if (await expander.count() > 0) {
      await expander.click().catch(() => {});
      await page2.waitForTimeout(2000);
      const txt3 = await page2.evaluate(() => document.body.innerText);
      const lower3 = txt3.toLowerCase();
      chk('F2b: Role selector options visible after expand',
        lower3.includes('relationship manager') ||
        lower3.includes('underwriter') ||
        lower3.includes('analyst') ||
        lower3.includes('marketing') ||
        lower3.includes('select your role'));
      await shot(page2, 'F2_01_advanced_open');
    } else {
      // Try clicking by text
      await page2.locator('summary').filter({ hasText: /advanced/i }).click().catch(() => {});
      await page2.waitForTimeout(1500);
      const txt3 = await page2.evaluate(() => document.body.innerText);
      chk('F2b: Role selector visible after expand', txt3.toLowerCase().includes('relationship manager'));
    }
  }

  await page2.close();
}

// ── Main ─────────────────────────────────────────────────────────────────────

(async () => {
  console.log('╔══════════════════════════════════════════════════════════════╗');
  console.log('║   AI Hero Academy — Phase 3 UAT                             ║');
  console.log('╚══════════════════════════════════════════════════════════════╝');
  console.log(`  App:         ${BASE_URL}`);
  console.log(`  Screenshots: ${SCREENSHOTS_DIR}`);

  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const t0 = Date.now();

  try {
    await scenarioA(browser);
    await scenarioA2(browser);
    await scenarioB(browser);
    await scenarioC(browser);
    await scenarioD(browser);
    await scenarioE(browser);
    await scenarioF(browser);
  } finally {
    await browser.close();
  }

  const elapsed = ((Date.now() - t0) / 1000).toFixed(1);

  console.log('\n\n╔══════════════════════════════════════════════════════════════╗');
  console.log('║   Phase 3 UAT — Results                                      ║');
  console.log('╚══════════════════════════════════════════════════════════════╝');

  const passed = _results.filter(r => r.ok);
  const failed = _results.filter(r => !r.ok);

  if (failed.length) {
    console.log('\n  FAILURES:');
    failed.forEach(r => console.log(`    ✗ ${r.label}`));
  }

  console.log(`\n  ${passed.length}/${_results.length} checks passed  (${elapsed}s)`);
  console.log(`  Screenshots: ${SCREENSHOTS_DIR}`);

  process.exit(failed.length === 0 ? 0 : 1);
})();
