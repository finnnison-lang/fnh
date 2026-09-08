// Screenshots of the local site at given scroll positions, using headless Chrome via puppeteer-core.
import puppeteer from 'puppeteer-core';
const [,, url, out, w='1440', h='900', ...pos] = process.argv;
const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--no-sandbox','--autoplay-policy=no-user-gesture-required'] });
const page = await browser.newPage(); await page.setViewport({ width: +w, height: +h, deviceScaleFactor: 1 });
await page.goto(url, { waitUntil: 'networkidle2' }); await new Promise(r => setTimeout(r, 2500));
const steps = pos.length ? pos.map(Number) : [0];
for (const p of steps) {
  await page.evaluate(y => window.scrollTo(0, y * innerHeight), p);
  // let lenis + scrolltrigger settle
  await new Promise(r => setTimeout(r, 1800));
  await page.screenshot({ path: `${out}_${String(p).replace('.','_')}.png` });
}
const errors = await page.evaluate(() => window.__errs || []);
await browser.close(); console.log('done', steps.length, 'shots');
