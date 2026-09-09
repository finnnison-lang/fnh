/* FNH v3 — interactions */
(() => {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, fine = matchMedia('(pointer: fine)').matches;
  const hasGsap = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined'; if (hasGsap) gsap.registerPlugin(ScrollTrigger);
  const META = { de: { title: 'FNH · Finn Hafemann — Film, Foto, AI & Design aus Stuttgart', desc: 'Finn Hafemann, Filmemacher, Fotograf und Designer aus der Region Stuttgart. Echte Kamera trifft generative KI: Nürburgring 24h, OdyssAI 2028, Island, Kuppelkino.' }, en: { title: 'FNH · Finn Hafemann — Film, Photo, AI & Design from Stuttgart', desc: 'Finn Hafemann, filmmaker, photographer and designer from the Stuttgart region. Real cameras meet generative AI: Nürburgring 24h, OdyssAI 2028, Iceland, dome cinema.' } };
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
  function rebuildSplits() {
    $$('[data-split]').forEach(el => {
      if (el._tw) { el._tw.scrollTrigger && el._tw.scrollTrigger.kill(); el._tw.kill(); el._tw = null; }
      const words = el.textContent.trim().split(/\s+/); el.innerHTML = words.map(w => `<span class="w"><span>${w}</span></span>`).join(' ');
      if (reduce || !hasGsap) return;
      const inner = $$('.w > span', el); gsap.set(inner, { yPercent: 110 });
      el._tw = gsap.to(inner, { yPercent: 0, duration: 1, ease: 'power4.out', stagger: 0.025, scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
    });
    hasGsap && ScrollTrigger.refresh();
  }
  let lenis = null;
  if (!reduce && typeof Lenis !== 'undefined' && hasGsap) { lenis = new Lenis({ lerp: 0.085, smoothWheel: true }); lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
  applyLang(lang);
  const scrollTo = t => { const el = typeof t === 'string' ? $(t) : t; if (!el) return; lenis ? lenis.scrollTo(el, { duration: 1.5 }) : el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }); };
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => { const id = a.getAttribute('href'); if (id.length < 2 || a.dataset.modal !== undefined) return; e.preventDefault(); closeMenu(); scrollTo(id); }));
  const burger = $('.burger'), menu = $('#menu'); burger.dataset.open = burger.textContent;
  function closeMenu() { menu.classList.remove('is-open'); burger.textContent = lang === 'en' ? 'Menu' : 'Menü'; document.body.classList.remove('is-locked'); lenis && lenis.start(); }
  burger.addEventListener('click', () => { if (menu.classList.contains('is-open')) return closeMenu(); menu.classList.add('is-open'); burger.textContent = lang === 'en' ? 'Close' : 'Schließen'; document.body.classList.add('is-locked'); lenis && lenis.stop(); });
  if (hasGsap && !reduce) gsap.to('.progress', { scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: 0.3 } });
  const nav = $('.nav'); let lastY = 0;
  const onScroll = () => { const y = window.scrollY; if (y > 140 && y > lastY + 4) nav.classList.add('nav--hidden'); else if (y < lastY - 4 || y < 140) nav.classList.remove('nav--hidden'); lastY = y; };
  addEventListener('scroll', onScroll, { passive: true });
  const darkSecs = $$('.dark, .reel');
  const setNavTheme = () => { const y = 36; const onDark = darkSecs.some(s => { const r = s.getBoundingClientRect(); return r.top <= y && r.bottom > y; }); nav.classList.toggle('nav--dark', onDark); };
  addEventListener('scroll', setNavTheme, { passive: true }); setNavTheme();
  if (fine && !reduce && hasGsap) {
    const cur = $('.cursor'), label = $('.cursor__label'); let x = 0, y = 0, rx = 0, ry = 0;
    addEventListener('pointermove', e => { x = e.clientX; y = e.clientY; cur.classList.add('is-on'); }, { passive: true }); document.addEventListener('mouseleave', () => cur.classList.remove('is-on'));
    gsap.ticker.add(() => { rx += (x - rx) * 0.22; ry += (y - ry) * 0.22; cur.style.transform = `translate3d(${rx}px,${ry}px,0)`; });
    $$('[data-cursor]').forEach(el => { el.addEventListener('mouseenter', () => { label.textContent = lang === 'en' && el.dataset.cursorEn ? el.dataset.cursorEn : el.dataset.cursor; cur.classList.add('is-hover'); }); el.addEventListener('mouseleave', () => cur.classList.remove('is-hover')); });
  }
  /* hero */
  if (hasGsap && !reduce) {
    gsap.from('.hero__logo', { yPercent: 18, opacity: 0, duration: 1.6, ease: 'power4.out', delay: 0.2 });
    gsap.from(['.hero__kicker', '.hero__foot'], { opacity: 0, y: 12, duration: 1.1, ease: 'power3.out', stagger: 0.12, delay: 0.9 });
    gsap.fromTo('.hero__logo', { y: 0, opacity: 1 }, { y: -120, opacity: 0.15, ease: 'none', immediateRender: false, scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom top', scrub: true } });
  }
  /* videos: attach lazily + play in view */
  const attach = v => { if (v.dataset.ready) return; $$('source[data-src]', v).forEach(s => s.src = s.dataset.src); v.load(); v.dataset.ready = '1'; };
  const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(en => { const wrap = en.target, v = $('video', wrap); if (!v) return; if (en.isIntersecting) { attach(v); v.play().then(() => wrap.classList.add('is-live')).catch(() => {}); } else { v.pause(); wrap.classList.remove('is-live'); } }), { threshold: 0.25 }) : null;
  $$('.reel').forEach(r => { if (reduce) return; io && io.observe(r); if (hasGsap) gsap.fromTo($('.reel__media', r), { scale: 1.12 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: r, start: 'top bottom', end: 'top top', scrub: true } }); });
  /* tiles */
  const tiles = $$('.tile');
  tiles.forEach(t => { const v = $('video', t); if (fine) { t.addEventListener('mouseenter', () => { attach(v); v.play().then(() => t.classList.add('is-playing')).catch(() => {}); }); t.addEventListener('mouseleave', () => { v.pause(); t.classList.remove('is-playing'); }); } });
  if (!fine && 'IntersectionObserver' in window) { const tio = new IntersectionObserver(es => es.forEach(en => { const t = en.target, v = $('video', t); if (en.intersectionRatio >= 0.6) { attach(v); v.play().then(() => t.classList.add('is-playing')).catch(() => {}); } else { v.pause(); t.classList.remove('is-playing'); } }), { threshold: [0, 0.6] }); tiles.forEach(t => tio.observe(t)); }
  /* reveals + parallax */
  if (hasGsap && !reduce) {
    $$('[data-reveal]').forEach(el => gsap.from(el, { y: 28, opacity: 0, duration: 1.1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 92%', once: true } }));
    $$('.tile, .pic').forEach(el => gsap.from(el, { y: 40, opacity: 0, duration: 1.2, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 94%', once: true } }));
    const rowsEl = $('.rows'); rowsEl && gsap.from('.rows .row', { opacity: 0, y: 10, duration: .6, ease: 'power2.out', stagger: 0.025, scrollTrigger: { trigger: rowsEl, start: 'top 85%', once: true } });
    gsap.matchMedia().add('(min-width: 900px)', () => {
      $$('[data-speed]').forEach(el => { const s = parseFloat(el.dataset.speed) || 1, amp = 160; gsap.fromTo(el, { y: (s - 1) * amp }, { y: -(s - 1) * amp, ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true, invalidateOnRefresh: true } }); });
    });
    const si = $('.studio__img img'); si && gsap.fromTo(si, { y: '-12%' }, { y: '0%', ease: 'none', scrollTrigger: { trigger: '.studio__img', start: 'top bottom', end: 'bottom top', scrub: true } });
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
  /* index */
  $$('.chip').forEach(ch => ch.addEventListener('click', () => { const f = ch.dataset.filter; $$('.chip').forEach(c => c.classList.toggle('is-active', c === ch)); $$('.row').forEach(r => r.classList.toggle('is-hidden', f !== 'all' && r.dataset.cat !== f)); $('.rows').classList.remove('is-collapsed'); const sa = $('.showall'); sa && (sa.hidden = true); hasGsap && ScrollTrigger.refresh(); }));
  const sa = $('.showall'); sa && sa.addEventListener('click', () => { const rows = $('.rows'); const c = rows.classList.toggle('is-collapsed'); sa.textContent = c ? (lang === 'en' ? sa.dataset.moreEn : sa.dataset.more) : (lang === 'en' ? sa.dataset.lessEn : sa.dataset.less); hasGsap && ScrollTrigger.refresh(); if (c) scrollTo('#index'); });
  const pv = $('.preview'), pvImg = $('.preview img');
  if (pv && fine && !reduce) { let px = 0, py = 0, tx = 0, ty = 0; addEventListener('pointermove', e => { tx = e.clientX + 150; ty = e.clientY; }, { passive: true }); gsap.ticker.add(() => { px += (tx - px) * 0.12; py += (ty - py) * 0.12; pv.style.left = px + 'px'; pv.style.top = py + 'px'; }); $$('.row').forEach(r => { r.addEventListener('mouseenter', () => { pvImg.src = r.dataset.poster; pv.classList.toggle('is-v', r.dataset.vertical === '1'); pv.classList.add('is-on'); }); r.addEventListener('mouseleave', () => pv.classList.remove('is-on')); }); }
  /* modals */
  $$('[data-modal]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); const m = $('#modal-' + a.dataset.modal); if (!m) return; lastFocus = a; m.classList.add('is-open'); document.body.classList.add('is-locked'); lenis && lenis.stop(); $('.modal__close', m).focus(); }));
  const closeModals = () => { $$('.modal.is-open').forEach(m => m.classList.remove('is-open')); if (!lb.classList.contains('is-open')) { document.body.classList.remove('is-locked'); lenis && lenis.start(); } };
  $$('[data-modal-close]').forEach(b => b.addEventListener('click', closeModals)); $$('.modal').forEach(m => m.addEventListener('click', e => { if (e.target === m) closeModals(); }));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { if (lb.classList.contains('is-open')) closeLightbox(); closeModals(); if (menu.classList.contains('is-open')) closeMenu(); } });
  addEventListener('load', () => hasGsap && ScrollTrigger.refresh()); document.fonts && document.fonts.ready.then(() => hasGsap && ScrollTrigger.refresh());
})();
