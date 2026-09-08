import puppeteer from 'puppeteer-core';
const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--no-sandbox'] });
const page = await browser.newPage(); await page.setViewport({ width: 1440, height: 900 });
const errs=[]; page.on('pageerror', e => errs.push(e.message)); page.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
await page.goto('http://localhost:4173/', { waitUntil: 'networkidle2' }); await new Promise(r => setTimeout(r, 3000));
const info = await page.evaluate(() => Array.from(document.querySelectorAll('.hero__title .l > span')).map(s => { const r = s.getBoundingClientRect(); const cs = getComputedStyle(s); return { text: s.textContent, x: r.x, y: r.y, w: r.width, h: r.height, tf: cs.transform, op: cs.opacity, font: cs.fontFamily, fs: cs.fontSize, lh: cs.lineHeight, parentH: s.parentElement.getBoundingClientRect().height, parentTop: s.parentElement.getBoundingClientRect().top }; }));
const h1 = await page.evaluate(() => { const r = document.querySelector('.hero__title').getBoundingClientRect(); return { top: r.top, h: r.height, html: document.querySelector('.hero__title').innerHTML.slice(0,300) }; });
const fonts = await page.evaluate(() => Array.from(document.fonts).map(f => f.family + ' ' + f.style + ' ' + f.status));
console.log(JSON.stringify({ info, h1, fonts, errs }, null, 1)); await browser.close();
