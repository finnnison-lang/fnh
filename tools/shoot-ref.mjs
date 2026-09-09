import puppeteer from 'puppeteer-core';
const [url, out, W, H, ...pos] = process.argv.slice(2);
const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required'] });
const page = await browser.newPage(); await page.setViewport({ width: +W, height: +H, deviceScaleFactor: 1 });
await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36');
await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 }); await new Promise(r => setTimeout(r, 5000));
// dismiss any cookie/intro overlays by pressing Escape and clicking through
await page.keyboard.press('Escape');
const total = await page.evaluate(() => document.body.scrollHeight);
console.log('scrollHeight', total);
for (const p of pos) {
  const y = Math.round(+p * +H); await page.evaluate(y => window.scrollTo({ top: y, behavior: 'instant' }), y);
  // nudge scroll for scroll-driven libs
  await page.mouse.wheel({ deltaY: 1 }); await new Promise(r => setTimeout(r, 2500));
  await page.screenshot({ path: `${out}_${String(p).replace('.', '_')}.png` });
}
const info = await page.evaluate(() => ({ fonts: [...new Set([...document.querySelectorAll('h1,h2,h3,p,a,span,li')].map(e=>getComputedStyle(e).fontFamily))].slice(0,5), bg: getComputedStyle(document.body).backgroundColor, color: getComputedStyle(document.body).color, h: document.body.scrollHeight, big: [...document.querySelectorAll('h1,h2')].slice(0,6).map(e=>({t:e.textContent.trim().slice(0,60), fs:getComputedStyle(e).fontSize, fw:getComputedStyle(e).fontWeight, ls:getComputedStyle(e).letterSpacing, lh:getComputedStyle(e).lineHeight})) }));
console.log(JSON.stringify(info)); await browser.close();
