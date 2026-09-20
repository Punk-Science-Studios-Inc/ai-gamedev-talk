// Render every slide to PNG for review: node tools/shoot.mjs [out-dir] [--frags]
// Uses the Playwright Chromium already on this machine.
import { fileURLToPath } from 'node:url';
// playwright is not installed in this folder; borrow the copy from a sibling project unless PW_DIR says otherwise
const pwDir = process.env.PW_DIR || 'C:/Users/darry/projects/oneill/node_modules/playwright';
const { chromium } = await import('file:///' + pwDir.replace(/\\/g, '/') + '/index.mjs');
import path from 'node:path';
import fs from 'node:fs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const out = path.resolve(process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : path.join(root, 'renders'));
const withFrags = process.argv.includes('--frags');
fs.mkdirSync(out, { recursive: true });

const exe = process.env.CHROME || 'C:/Users/darry/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe';
const browser = await chromium.launch({ executablePath: exe, headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on('console', m => { if (m.type() === 'error') console.log('console.error:', m.text()); });
page.on('pageerror', e => console.log('pageerror:', e.message));
await page.goto('file:///' + path.join(root, 'index.html').replace(/\\/g, '/') + '#1', { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
const n = await page.evaluate(() => document.querySelectorAll('.slide').length);
for (let k = 1; k <= n; k++) {
  await page.evaluate(k => { location.hash = '#' + k; }, k);
  await page.waitForTimeout(250);
  if (withFrags) await page.evaluate(() => document.querySelectorAll('.slide.active .frag').forEach(f => f.classList.add('on')));
  await page.waitForTimeout(250);
  await page.screenshot({ path: path.join(out, `slide-${String(k).padStart(2, '0')}.png`) });
}
await browser.close();
console.log(`${n} slides rendered to ${out}`);
