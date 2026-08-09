const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 1000 } });

  // Reference: Wayback snapshot of the original site
  try {
    await page.goto('https://web.archive.org/web/20250321025801/https://www.purecomp.net/', { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(2500);
    await page.screenshot({ path: 'shot_wayback.png', fullPage: false });
    console.log('WAYBACK OK');
  } catch (e) {
    console.log('WAYBACK FAIL', e.message);
  }

  // Our live Jekyll site
  try {
    await page.goto('https://nate-mina.github.io/puco-py/?v=' + Date.now(), { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'shot_live_restyled.png', fullPage: false });
    console.log('LIVE OK');
  } catch (e) {
    console.log('LIVE FAIL', e.message);
  }

  await browser.close();
})();
