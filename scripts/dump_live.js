const { chromium } = require('playwright');
const fs = require('fs');

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
    // Dump the full <body> innerHTML of the RENDERED live site
    const body = await page.evaluate(() => document.body.innerHTML);
    fs.writeFileSync('live_home.html', body);
    console.log('LIVE DOM SAVED bytes=', body.length);
    // Also save the <main> content only (the role=main wrapper)
    const main = await page.evaluate(() => {
      const m = document.querySelector('[role="main"]');
      return m ? m.outerHTML : '';
    });
    fs.writeFileSync('live_home_main.html', main);
    console.log('LIVE MAIN SAVED bytes=', main.length);
  } catch (e) {
    console.log('FAIL', e.message.split('\n')[0]);
  }
  await browser.close();
})();
