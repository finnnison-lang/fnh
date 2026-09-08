/* FNH v2 — interactions */
(() => {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, fine = matchMedia('(pointer: fine)').matches;
  const hasGsap = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);
  const META = { de: { title: 'FNH · Finn Hafemann — Film, Foto, AI & Design aus Stuttgart', desc: 'Finn Hafemann, Filmemacher, Fotograf und Designer aus der Region Stuttgart. Echte Kamera trifft generative KI: Nürburgring 24h, OdyssAI 2028, Island, Miniatur-Katastrophen.' }, en: { title: 'FNH · Finn Hafemann — Film, Photo, AI & Design from Stuttgart', desc: 'Finn Hafemann, filmmaker, photographer and designer from the Stuttgart region. Real cameras meet generative AI: Nürburgring 24h, OdyssAI 2028, Iceland, miniature disasters.' } };
  let lang = 'de'; try { lang = localStorage.getItem('fnh-lang') || ((navigator.language || 'de').toLowerCase().startsWith('de') ? 'de' : 'en'); } catch (e) {}
  function applyLang(l) {
    lang = l; document.documentElement.lang = l;
    $$('[data-en]').forEach(el => { if (el.dataset.de === undefined) el.dataset.de = el.innerHTML; el.innerHTML = l === 'en' ? el.dataset.en : el.dataset.de; });
    $$('[data-en-alt]').forEach(el => { if (el.dataset.deAlt === undefined) el.dataset.deAlt = el.getAttribute('alt') || ''; el.setAttribute('alt', l === 'en' ? el.dataset.enAlt : el.dataset.deAlt); });
    document.title = META[l].title; const md = $('meta[name="description"]'); if (md) md.content = META[l].desc;
    $$('[data-lang-toggle]').forEach(b => b.textContent = l === 'en' ? 'DE' : 'EN');
    try { localStorage.setItem('fnh-lang', l); } catch (e) {}
    rebuildSplits();
  }
  $$('[data-lang-toggle]').forEach(b => b.addEventListener('click', () => applyLang(lang === 'en' ? 'de' : 'en')));
  /* word splits */
  function rebuildSplits() {
    $$('[data-split]').forEach(el => {
      if (el._tw) { el._tw.scrollTrigger && el._tw.scrollTrigger.kill(); el._tw.kill(); el._tw = null; }
      const parts = []; el.childNodes.forEach(n => {
        if (n.nodeType === 3) n.textContent.split(/\s+/).filter(Boolean).forEach(w => parts.push(`<span class="w"><span>${w}</span></span>`));
        else if (n.nodeType === 1) n.textContent.split(/\s+/).filter(Boolean).forEach(w => parts.push(`<span class="w"><span class="${n.className}">${w}</span></span>`));
      });
      el.innerHTML = parts.join(' ');
      if (reduce || !hasGsap) return;
      const inner = $$('.w > span', el); gsap.set(inner, { yPercent: 110 });
      el._tw = gsap.to(inner, { yPercent: 0, duration: 1.1, ease: 'power4.out', stagger: 0.03, scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
    });
    hasGsap && ScrollTrigger.refresh();
  }
  /* smooth scroll */
  let lenis = null;
  if (!reduce && typeof Lenis !== 'undefined' && hasGsap) { lenis = new Lenis({ lerp: 0.08, smoothWheel: true }); lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
  applyLang(lang);
  const scrollTo = t => { const el = typeof t === 'string' ? $(t) : t; if (!el) return; lenis ? lenis.scrollTo(el, { duration: 1.6 }) : el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }); };
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => { const id = a.getAttribute('href'); if (id.length < 2 || a.dataset.modal !== undefined) return; e.preventDefault(); closeMenu(); scrollTo(id); }));
  /* menu */
  const burger = $('.burger'), menu = $('#menu');
  function closeMenu() { menu.classList.remove('is-open'); burger.textContent = burger.dataset.open; document.body.classList.remove('is-locked'); lenis && lenis.start(); }
  burger.dataset.open = burger.textContent;
  burger.addEventListener('click', () => { const open = !menu.classList.contains('is-open'); if (!open) return closeMenu(); menu.classList.add('is-open'); burger.textContent = lang === 'en' ? 'Close' : 'Schließen'; document.body.classList.add('is-locked'); lenis && lenis.stop(); });
  if (hasGsap && !reduce) gsap.to('.progress', { scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: 0.3 } });
  /* cursor */
  if (fine && !reduce && hasGsap) {
    const cur = $('.cursor'), label = $('.cursor__label'); let x = 0, y = 0, rx = 0, ry = 0;
    addEventListener('pointermove', e => { x = e.clientX; y = e.clientY; cur.classList.add('is-on'); }, { passive: true });
    document.addEventListener('mouseleave', () => cur.classList.remove('is-on'));
    gsap.ticker.add(() => { rx += (x - rx) * 0.22; ry += (y - ry) * 0.22; cur.style.transform = `translate3d(${rx}px,${ry}px,0)`; });
    $$('[data-cursor]').forEach(el => { el.addEventListener('mouseenter', () => { label.textContent = lang === 'en' && el.dataset.cursorEn ? el.dataset.cursorEn : el.dataset.cursor; cur.classList.add('is-hover'); }); el.addEventListener('mouseleave', () => cur.classList.remove('is-hover')); });
  }
  /* hero */
  const hero = $('#hero'), hv = $('.hero__video');
  if (hv) { const attach = () => { $$('source[data-src]', hv).forEach(s => s.src = s.dataset.src); hv.load(); hv.play().then(() => hv.parentElement.classList.add('is-live')).catch(() => {}); }; if (reduce) hv.removeAttribute('autoplay'); else if (document.readyState === 'complete') attach(); else addEventListener('load', () => setTimeout(attach, 150)); }
  if (hasGsap && !reduce && hero) {
    gsap.from('.hero__title .l > span', { yPercent: 110, duration: 1.4, ease: 'power4.out', stagger: 0.12, delay: 0.3 });
    gsap.from(['.hero__kicker', '.hero__side', '.hero__foot'], { opacity: 0, y: 16, duration: 1.2, ease: 'power3.out', stagger: 0.1, delay: 0.9 });
    gsap.fromTo('.hero__media', { scale: 1.08 }, { scale: 1, duration: 2.4, ease: 'power2.out' });
    gsap.timeline({ scrollTrigger: { trigger: hero, start: 'top top', end: '+=70%', pin: true, scrub: true, anticipatePin: 1 } })
      .fromTo('.hero__media', { scale: 1, filter: 'brightness(1)' }, { scale: 1.08, filter: 'brightness(0.25)', ease: 'none', immediateRender: false }, 0)
      .fromTo('.hero__title .l > span', { yPercent: 0, opacity: 1 }, { yPercent: -40, opacity: 0, stagger: 0.04, ease: 'none', immediateRender: false }, 0)
      .fromTo(['.hero__kicker', '.hero__side', '.hero__foot'], { opacity: 1, y: 0 }, { opacity: 0, y: -20, ease: 'none', immediateRender: false }, 0);
  }
  /* journey */
  const chapters = $$('.ch'); const N = chapters.length;
  const playOnly = i => chapters.forEach((c, k) => { const v = $('video', c); if (!v) return; if (k === i) { if (!v.src && $('source[data-src]', v)) { $$('source[data-src]', v).forEach(s => s.src = s.dataset.src); v.load(); } v.play().then(() => c.classList.add('is-live')).catch(() => {}); } else { v.pause(); c.classList.remove('is-live'); } });
  const counter = $('.journey__count'), bars = $$('.journey__bars i'), nextLab = $('.journey__next');
  const setActive = i => { counter && (counter.textContent = `( ${String(i + 1).padStart(2, '0')} / ${String(N).padStart(2, '0')} )`); bars.forEach((b, k) => b.classList.toggle('is-on', k <= i)); if (nextLab) { const nx = chapters[i + 1]; nextLab.textContent = nx ? (lang === 'en' ? 'Next: ' : 'Nächstes Kapitel: ') + (lang === 'en' ? nx.dataset.titleEn : nx.dataset.title) : (lang === 'en' ? 'All works below' : 'Alle Arbeiten weiter unten'); } playOnly(i); };
  if (N && hasGsap && !reduce) {
    const HOLD = 0.55, TR = 0.45; chapters.forEach((c, i) => { if (i) gsap.set(c, { clipPath: 'inset(100% 0 0 0)' }); });
    const tl = gsap.timeline({ scrollTrigger: { trigger: '.journey', start: 'top top', end: () => '+=' + ((N - 1) + HOLD + 0.4) * innerHeight, pin: '.journey__pin', scrub: 0.6, anticipatePin: 1, invalidateOnRefresh: true, onUpdate: self => { const t = self.progress * ((N - 1) + HOLD + 0.4); const a = Math.min(N - 1, Math.max(0, Math.floor(t + (1 - HOLD)))); if (a !== tl._active) { tl._active = a; setActive(a); } }, onEnter: () => setActive(0), onEnterBack: () => setActive(tl._active || 0) } });
    for (let i = 1; i < N; i++) {
      const s = (i - 1) + HOLD, prev = chapters[i - 1], cur = chapters[i];
      tl.to($('.ch__media', prev), { scale: 0.9, filter: 'brightness(0.35)', duration: TR, ease: 'none' }, s)
        .to($('.ch__text', prev), { y: -70, opacity: 0, duration: TR * 0.7, ease: 'none' }, s)
        .fromTo(cur, { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: TR, ease: 'none' }, s)
        .fromTo($('.ch__media', cur), { scale: 1.18 }, { scale: 1, duration: TR, ease: 'none' }, s)
        .fromTo($('.ch__text', cur), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: TR * 0.8, ease: 'none' }, s + TR * 0.25);
    }
    tl.to({}, { duration: HOLD + 0.4 });
    setActive(0);
  } else if (N) { setActive(0); chapters.forEach((c, i) => playOnly(i)); }
  /* reveals */
  if (hasGsap && !reduce) {
    $$('[data-reveal]').forEach(el => gsap.from(el, { y: 30, opacity: 0, duration: 1.2, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 90%', once: true } }));
    $$('.row').forEach((r, i) => gsap.from(r, { y: 24, opacity: 0, duration: 0.9, ease: 'power3.out', scrollTrigger: { trigger: r, start: 'top 95%', once: true } }));
    const ai = $('.about__img img'); ai && gsap.fromTo(ai, { y: '-14%' }, { y: '0%', ease: 'none', scrollTrigger: { trigger: '.about__img', start: 'top bottom', end: 'bottom top', scrub: true } });
    gsap.matchMedia().add('(min-width: 900px)', () => {
      const track = $('.strip__track'); if (!track) return; const dist = () => track.scrollWidth - innerWidth;
      gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: { trigger: '.strip__pin', start: 'top top', end: () => '+=' + dist(), pin: true, scrub: 0.5, invalidateOnRefresh: true, anticipatePin: 1 } });
      $$('.pic img').forEach(img => gsap.fromTo(img, { xPercent: -6 }, { xPercent: 6, ease: 'none', scrollTrigger: { trigger: '.strip__pin', start: 'top top', end: () => '+=' + dist(), scrub: true } }));
    });
  }
  /* lightbox */
  const lb = $('#lightbox'), lbBody = $('.lb__body'), lbCap = $('.lb__cap'); let lastFocus = null;
  function openLightbox({ type, src, poster, title, vertical }) { lastFocus = document.activeElement; lbBody.innerHTML = ''; if (type === 'video') { const v = document.createElement('video'); v.src = src; v.controls = true; v.autoplay = true; v.playsInline = true; if (poster) v.poster = poster; if (vertical) v.classList.add('is-vertical'); lbBody.appendChild(v); } else { const i = new Image(); i.src = src; i.alt = title || ''; lbBody.appendChild(i); } lbCap.textContent = title || ''; lb.classList.add('is-open'); document.body.classList.add('is-locked'); lenis && lenis.stop(); $('.lb__close').focus(); }
  function closeLightbox() { const v = $('video', lbBody); if (v) { v.pause(); v.removeAttribute('src'); v.load(); } lb.classList.remove('is-open'); lbBody.innerHTML = ''; document.body.classList.remove('is-locked'); lenis && lenis.start(); lastFocus && lastFocus.focus && lastFocus.focus(); }
  $('.lb__close').addEventListener('click', closeLightbox); lb.addEventListener('click', e => { if (e.target === lb || e.target === lbBody) closeLightbox(); });
  const activate = (el, fn) => { el.addEventListener('click', fn); el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fn(); } }); };
  const T = el => (lang === 'en' && el.dataset.titleEn) ? el.dataset.titleEn : el.dataset.title;
  $$('[data-open-video]').forEach(el => activate(el, () => openLightbox({ type: 'video', src: el.dataset.openVideo, poster: el.dataset.poster, title: T(el), vertical: el.dataset.vertical === '1' })));
  $$('[data-open-image]').forEach(el => activate(el, () => openLightbox({ type: 'image', src: el.dataset.openImage, title: T(el) })));
  /* index: filters + hover preview */
  $$('.chip').forEach(ch => ch.addEventListener('click', () => { const f = ch.dataset.filter; $$('.chip').forEach(c => c.classList.toggle('is-active', c === ch)); $$('.row').forEach(r => r.classList.toggle('is-hidden', f !== 'all' && r.dataset.cat !== f)); hasGsap && ScrollTrigger.refresh(); }));
  const pv = $('.preview'), pvImg = $('.preview img');
  if (pv && fine && !reduce) { let px = 0, py = 0, tx = 0, ty = 0; addEventListener('pointermove', e => { tx = e.clientX + 160; ty = e.clientY; }, { passive: true }); gsap.ticker.add(() => { px += (tx - px) * 0.12; py += (ty - py) * 0.12; pv.style.left = px + 'px'; pv.style.top = py + 'px'; });
    $$('.row').forEach(r => { r.addEventListener('mouseenter', () => { pvImg.src = r.dataset.poster; pv.classList.toggle('is-v', r.dataset.vertical === '1'); pv.classList.add('is-on'); }); r.addEventListener('mouseleave', () => pv.classList.remove('is-on')); }); }
  /* modals */
  $$('[data-modal]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); const m = $('#modal-' + a.dataset.modal); if (!m) return; lastFocus = a; m.classList.add('is-open'); document.body.classList.add('is-locked'); lenis && lenis.stop(); $('.modal__close', m).focus(); }));
  const closeModals = () => { $$('.modal.is-open').forEach(m => m.classList.remove('is-open')); if (!lb.classList.contains('is-open')) { document.body.classList.remove('is-locked'); lenis && lenis.start(); } };
  $$('[data-modal-close]').forEach(b => b.addEventListener('click', closeModals)); $$('.modal').forEach(m => m.addEventListener('click', e => { if (e.target === m) closeModals(); }));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { if (lb.classList.contains('is-open')) closeLightbox(); closeModals(); if (menu.classList.contains('is-open')) closeMenu(); } });
  addEventListener('load', () => hasGsap && ScrollTrigger.refresh()); document.fonts && document.fonts.ready.then(() => hasGsap && ScrollTrigger.refresh());
})();
