const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const BASE_URL = 'https://ai-hero-academy-387141525919.northamerica-northeast1.run.app';
const SCREENSHOTS_DIR = path.join(__dirname, 'uat_screenshots');

if (!fs.existsSync(SCREENSHOTS_DIR)) {
  fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });
}

const PROFILES = [
  { id: '3a', label: 'Fresh user → Welcome page', expected: 'Welcome' },
  { id: '3b', label: 'RM at Diagnostic → Diagnostic page', expected: 'Diagnostic' },
  { id: '3c', label: 'UW, Module 1 complete → Home/Training', expected: 'Home' },
  { id: '3d', label: 'AN, all modules complete → Home/Training', expected: 'Home' },
  { id: '3e', label: 'MK, Module 3 in progress → Home/Training', expected: 'Home' },
];

function getToken() {
  const tokenFile = path.join(__dirname, 'uat_token.txt');
  if (fs.existsSync(tokenFile)) {
    return fs.readFileSync(tokenFile, 'utf8').trim();
  }
  throw new Error('Token file not found. Run get_token.py first.');
}

async function waitForStreamlitReady(page, timeout = 90000) {
  // Wait for Streamlit to finish the loading skeleton and render actual content
  // Streamlit removes the loading skeleton and renders stMarkdownContainer or stBlock elements
  console.log('Waiting for Streamlit content to render...');

  try {
    // Wait for network to be mostly idle
    await page.waitForLoadState('networkidle', { timeout: 60000 });
    console.log('Network idle reached');
  } catch (e) {
    console.log('Network idle timeout, continuing...');
  }

  // Wait for Streamlit app container with actual content (not loading skeleton)
  // The loading skeletons have class 'stSkeleton'; wait until they're gone or real content appears
  try {
    await page.waitForFunction(() => {
      // Check if there's text content in the Streamlit main area
      const mainArea = document.querySelector('[data-testid="stMain"]') || document.querySelector('.main') || document.body;
      const text = mainArea ? mainArea.innerText.trim() : '';
      return text.length > 50; // Wait until there's meaningful text
    }, { timeout: timeout });
    console.log('Content appeared in main area');
  } catch (e) {
    console.log('Timeout waiting for content, taking screenshot anyway...');
  }

  // Additional buffer for full render
  await page.waitForTimeout(3000);
}

async function testProfile(browser, token, profile) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`Testing profile: ${profile.id} — ${profile.label}`);
  console.log('='.repeat(60));

  const context = await browser.newContext({
    extraHTTPHeaders: {
      'Authorization': `Bearer ${token}`
    },
    viewport: { width: 1280, height: 900 }
  });
  const page = await context.newPage();

  const url = `${BASE_URL}/?demo=true&profile=${profile.id}`;
  console.log(`Navigating to: ${url}`);

  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
    await waitForStreamlitReady(page);

    // Take screenshot
    const screenshotPath = path.join(SCREENSHOTS_DIR, `profile_${profile.id}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    console.log(`Screenshot saved: ${screenshotPath}`);

    // Get page title
    const title = await page.title();
    console.log(`Page title: "${title}"`);

    // Get full page text content from body
    const bodyText = await page.evaluate(() => {
      // Try main content area first
      const main = document.querySelector('[data-testid="stMain"]') ||
                   document.querySelector('.main') ||
                   document.body;
      return main ? main.innerText : document.body.innerText;
    });

    const fullBodyText = await page.evaluate(() => document.body.innerText);

    console.log(`Content length (main): ${bodyText.length} chars`);
    console.log(`Content length (full): ${fullBodyText.length} chars`);

    // Check for "Databricks" text
    const hasDatabricks = fullBodyText.toLowerCase().includes('databricks');
    console.log(`Contains "Databricks": ${hasDatabricks ? 'YES (FAIL!)' : 'No (OK)'}`);

    // Check for Demo Mode selector in sidebar
    const hasDemoMode = fullBodyText.toLowerCase().includes('demo mode') ||
                        fullBodyText.toLowerCase().includes('demo profile') ||
                        fullBodyText.includes('3a') || fullBodyText.includes('3b') ||
                        fullBodyText.includes('3c') || fullBodyText.includes('3d') ||
                        fullBodyText.includes('3e');
    console.log(`Demo Mode / profile indicator in sidebar: ${hasDemoMode ? 'Yes' : 'NOT FOUND'}`);

    // Detect current page/view
    const lower = fullBodyText.toLowerCase();

    // Welcome page indicators
    const isWelcomeRoleSelect = (lower.includes('relationship manager') && lower.includes('underwriter') && lower.includes('analyst') && !lower.includes('module 1')) ||
                                 lower.includes('select your role') || lower.includes('get started') ||
                                 lower.includes('edc internal') || lower.includes('ai skills platform');
    // Diagnostic page indicators
    const isDiagnostic = (lower.includes('diagnostic') && !lower.includes('module')) ||
                          lower.includes('question 1 of') || lower.includes('start diagnostic');
    // Skills Profile page indicators
    const isSkillsProfile = (lower.includes('skills profile') || lower.includes('skill profile')) &&
                             !lower.includes('module 1') && !lower.includes('my training');
    // Home page indicators
    const isHome = lower.includes('my training') ||
                   (lower.includes('module 1') && lower.includes('module 2')) ||
                   (lower.includes('course') && lower.includes('unlock'));

    let detectedPage = 'Unknown';
    if (isHome) detectedPage = 'Home/Training';
    else if (isSkillsProfile) detectedPage = 'Skills Profile';
    else if (isDiagnostic) detectedPage = 'Diagnostic';
    else if (isWelcomeRoleSelect) detectedPage = 'Welcome';

    console.log(`Detected page: ${detectedPage}`);
    console.log(`Expected page: ${profile.expected}`);

    // Profile-specific checks
    if (profile.id === '3a') {
      const hasEyebrow = fullBodyText.includes('EDC INTERNAL · AI SKILLS PLATFORM') ||
                         fullBodyText.includes('EDC INTERNAL') || fullBodyText.includes('AI SKILLS PLATFORM');
      console.log(`Eyebrow "EDC INTERNAL · AI SKILLS PLATFORM": ${hasEyebrow ? 'Present (OK)' : 'NOT FOUND'}`);
    }

    if (['3c', '3d', '3e'].includes(profile.id)) {
      const hasUW = lower.includes('underwriter') || lower.includes('uw ');
      const hasAN = lower.includes('analyst');
      const hasMK = lower.includes('marketing') || lower.includes('marketer');
      if (profile.id === '3c') console.log(`UW role content visible: ${hasUW ? 'Yes (OK)' : 'Not detected'}`);
      if (profile.id === '3d') console.log(`AN role content visible: ${hasAN ? 'Yes (OK)' : 'Not detected'}`);
      if (profile.id === '3e') console.log(`MK role content visible: ${hasMK ? 'Yes (OK)' : 'Not detected'}`);
    }

    // Print text excerpt
    const textToShow = fullBodyText || bodyText;
    console.log('\n--- Full page text excerpt (first 1200 chars) ---');
    console.log(textToShow.substring(0, 1200));
    console.log('---');

    // Pass/fail verdict
    let passed = false;
    if (profile.expected === 'Welcome' && detectedPage === 'Welcome') passed = true;
    if (profile.expected === 'Diagnostic' && detectedPage === 'Diagnostic') passed = true;
    if (profile.expected === 'Home' && detectedPage === 'Home/Training') passed = true;

    console.log(`\nRESULT: ${passed ? '✓ PASS' : '✗ FAIL (got: ' + detectedPage + ')'}`);

  } catch (err) {
    console.error(`Error testing profile ${profile.id}:`, err.message);
  } finally {
    await context.close();
  }
}

(async () => {
  const token = getToken();
  console.log('Got auth token, length:', token.length);

  const browser = await chromium.launch({ headless: true });

  for (const profile of PROFILES) {
    await testProfile(browser, token, profile);
  }

  await browser.close();
  console.log('\n\nAll profiles tested. Screenshots in: ' + SCREENSHOTS_DIR);
})();
