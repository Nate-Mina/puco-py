const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 1200 } });

  // Collect all image responses from the live site
  const images = {};
  page.on('response', (resp) => {
    const ct = resp.headers()['content-type'] || '';
    const u = resp.url();
    if (ct.startsWith('image/') && u.includes('googleusercontent.com')) {
      resp.body().then((b) => { images[u] = b; }).catch(() => {});
    }
  });

  try {
    await page.goto('https://www.purecomp.net/', { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(5000);
  } catch (e) {
    console.log('goto fail', e.message.split('\n')[0]);
  }

  console.log('captured image responses:', Object.keys(images).length);
  // Save them with index
  let i = 0;
  for (const [u, buf] of Object.entries(images)) {
    const fn = `recovered_img_${i}.png`;
    fs.writeFileSync(fn, buf);
    console.log(i, fn, buf.length, u.slice(0, 70));
    i++;
  }
  await browser.close();
})();
