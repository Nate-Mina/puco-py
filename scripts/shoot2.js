const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 1100 } });

  // 1) The REAL current purecomp.net (needs JS to render)
  try {
    await page.goto('https://www.purecomp.net/', { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(3500);
    await page.screenshot({ path: 'ref_real.png', fullPage: false });
    console.log('REAL OK');
  } catch (e) {
    console.log('REAL FAIL', e.message);
  }

  // 2) Wayback snapshot as a second reference (no toolbar clip)
  try {
    await page.goto('https://web.archive.org/web/20250321025801/https://www.purecomp.net/', { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(3000);
    // clip removes the ~46px Wayback toolbar
    await page.screenshot({ path: 'ref_wayback.png', fullPage: false, clip: { x: 0, y: 46, width: 1280, height: 1054 } });
    console.log('WAYBACK OK');
  } catch (e) {
    console.log('WAYBACK FAIL', e.message);
  }

  // 3) Our live Jekyll site
  try {
    await page.goto('https://nate-mina.github.io/puco-py/?v=' + Date.now(), { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'ref_live.png', fullPage: false });
    console.log('LIVE OK');
  } catch (e) {
    console.log('LIVE FAIL', e.message);
  }

  await browser.close();
})();
