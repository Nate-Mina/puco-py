const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 1100 } });

  // Block slow third-party embeds that prevent 'load' from firing on the live site
  await page.route('**/*', (route) => {
    const u = route.request().url();
    if (u.includes('allmylinks.com') || u.includes('beacons.ai') || u.includes('googleusercontent.com/embeds') || u.includes('doubleclick') || u.includes('google-analytics')) {
      return route.abort();
    }
    return route.continue();
  });

  // 1) Try the REAL live site (abort heavy embeds so it can finish)
  try {
    await page.goto('https://www.purecomp.net/', { waitUntil: 'load', timeout: 45000 });
    await page.waitForTimeout(4000);
    await page.screenshot({ path: 'ref_real.png', fullPage: false });
    console.log('REAL OK');
  } catch (e) {
    console.log('REAL FAIL', e.message.split('\n')[0]);
  }

  // 2) Newest Wayback snapshot
  try {
    await page.goto('https://web.archive.org/web/2026/https://www.purecomp.net/', { waitUntil: 'load', timeout: 45000 });
    await page.waitForTimeout(3500);
    await page.screenshot({ path: 'ref_wayback_new.png', fullPage: false, clip: { x: 0, y: 46, width: 1280, height: 1054 } });
    console.log('WAYBACK_NEW OK');
  } catch (e) {
    console.log('WAYBACK_NEW FAIL', e.message.split('\n')[0]);
  }

  await browser.close();
})();
