const { chromium } = require('playwright');
const { PNG } = require('pngjs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 1000 } });
  await page.route('**/*', (route) => {
    const u = route.request().url();
    if (u.includes('allmylinks.com') || u.includes('beacons.ai') || u.includes('googleusercontent.com/embeds') || u.includes('doubleclick') || u.includes('google-analytics')) {
      return route.abort();
    }
    return route.continue();
  });

  async function shot(url, file, full=false) {
    await page.goto(url, { waitUntil: 'load', timeout: 45000 });
    await page.waitForTimeout(full ? 4000 : 2000);
    await page.screenshot({ path: file, fullPage: full });
  }

  try { await shot('https://www.purecomp.net/', 'cmp_real.png'); console.log('real done'); } catch(e){ console.log('real fail', e.message.split('\n')[0]); }
  try { await shot('https://nate-mina.github.io/puco-py/?v='+Date.now(), 'cmp_live.png'); console.log('live done'); } catch(e){ console.log('live fail', e.message.split('\n')[0]); }

  await browser.close();
})();
