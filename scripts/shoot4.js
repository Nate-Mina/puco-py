const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 1100 } });
  await page.route('**/*', (route) => {
    const u = route.request().url();
    if (u.includes('allmylinks.com') || u.includes('beacons.ai') || u.includes('googleusercontent.com/embeds') || u.includes('doubleclick') || u.includes('google-analytics')) {
      return route.abort();
    }
    return route.continue();
  });

  try {
    await page.goto('https://www.purecomp.net/', { waitUntil: 'load', timeout: 45000 });
    await page.waitForTimeout(4000);
    await page.screenshot({ path: 'ref_real_full.png', fullPage: true });
    console.log('REAL FULL OK');
  } catch (e) {
    console.log('REAL FULL FAIL', e.message.split('\n')[0]);
  }

  try {
    await page.goto('https://web.archive.org/web/20250321025801/https://www.purecomp.net/', { waitUntil: 'load', timeout: 45000 });
    await page.waitForTimeout(3000);
    await page.screenshot({ path: 'ref_wayback_full.png', fullPage: true, clip: { x: 0, y: 0, width: 1280, height: 4000 } });
    console.log('WAYBACK FULL OK');
  } catch (e) {
    console.log('WAYBACK FULL FAIL', e.message.split('\n')[0]);
  }

  try {
    await page.goto('https://nate-mina.github.io/puco-py/?v=' + Date.now(), { waitUntil: 'load', timeout: 45000 });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'ref_live_full.png', fullPage: true });
    console.log('LIVE FULL OK');
  } catch (e) {
    console.log('LIVE FULL FAIL', e.message.split('\n')[0]);
  }

  await browser.close();
})();
