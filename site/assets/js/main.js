/* FNH — Finn Hafemann · interactions */
(() => {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = window.matchMedia('(pointer: fine)').matches;
  const hasGsap = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);

  /* ---------- language ---------- */
  const META = {
    de: { title: 'FNH · Finn Hafemann — Film, Foto, AI & Design aus Stuttgart', desc: 'FNH Studios: Finn Hafemann, Filmemacher, Fotograf und Designer aus der Region Stuttgart. Echte Kamera trifft generative KI. Miniatur-Katastrophen, Porträts, Island, Packaging.' },
    en: { title: 'FNH · Finn Hafemann — Film, Photo, AI & Design from Stuttgart', desc: 'FNH Studios: Finn Hafemann, filmmaker, photographer and designer from the Stuttgart region. Real cameras meet generative AI. Miniature disasters, portraits, Iceland, packaging.' }
  };
  const LANG_KEY = 'fnh-lang';
  let lang = 'de';
  try { lang = localStorage.getItem(LANG_KEY) || ((navigator.language || 'de').toLowerCase().startsWith('de') ? 'de' : 'en'); } catch (e) {}
  const t = (de, en) => (lang === 'en' ? en : de);

  function applyLang(l) {
    lang = l;
    document.documentElement.lang = l;
    $$('[data-en]').forEach(el => { if (el.dataset.de === undefined) el.dataset.de = el.innerHTML; el.innerHTML = l === 'en' ? el.dataset.en : el.dataset.de; });
    $$('[data-en-alt]').forEach(el => { if (el.dataset.deAlt === undefined) el.dataset.deAlt = el.getAttribute('alt') || ''; el.setAttribute('alt', l === 'en' ? el.dataset.enAlt : el.dataset.deAlt); });
    $$('[data-en-label]').forEach(el => { if (el.dataset.deLabel === undefined) el.dataset.deLabel = el.getAttribute('aria-label') || ''; el.setAttribute('aria-label', l === 'en' ? el.dataset.enLabel : el.dataset.deLabel); });
    document.title = META[l].title;
    const md = $('meta[name="description"]'); if (md) md.content = META[l].desc;
    $$('[data-lang-toggle]').forEach(b => { b.textContent = l === 'en' ? 'DE' : 'EN'; });
    try { localStorage.setItem(LANG_KEY, l); } catch (e) {}
    rebuildSplits();
  }
  $$('[data-lang-toggle]').forEach(b => b.addEventListener('click', () => applyLang(lang === 'en' ? 'de' : 'en')));

  /* ---------- word splits ---------- */
  function splitWords(el) {
    const text = el.textContent.trim();
    el.innerHTML = text.split(/\s+/).map(w => `<span class="w"><span>${w}</span></span>`).join(' ');
  }
  function rebuildSplits() {
    $$('[data-split]').forEach(el => {
      if (el._tw) { el._tw.scrollTrigger && el._tw.scrollTrigger.kill(); el._tw.kill(); el._tw = null; }
      splitWords(el);
      if (reduce || !hasGsap) return;
      const inner = $$('.w > span', el);
      gsap.set(inner, { yPercent: 110 });
      el._tw = gsap.to(inner, { yPercent: 0, duration: 1, ease: 'power4.out', stagger: 0.04, scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
    });
    if (hasGsap) ScrollTrigger.refresh();
  }

  /* ---------- smooth scroll ---------- */
  let lenis = null;
  if (!reduce && typeof Lenis !== 'undefined' && hasGsap) {
    lenis = new Lenis({ lerp: 0.085, smoothWheel: true, wheelMultiplier: 1 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(time => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  function scrollTo(target) {
    const el = typeof target === 'string' ? $(target) : target;
    if (!el) return;
    if (lenis) lenis.scrollTo(el, { offset: 0, duration: 1.4 });
    else el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
  }
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    if (id.length < 2 || a.dataset.modal !== undefined) return;
    e.preventDefault(); closeMenu(); scrollTo(id);
  }));

  /* ---------- nav / menu ---------- */
  const nav = $('#nav'), burger = $('.burger'), menu = $('#menu');
  const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 40);
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  function closeMenu() { menu.classList.remove('is-open'); burger.classList.remove('is-open'); burger.setAttribute('aria-expanded', 'false'); document.body.classList.remove('is-locked'); lenis && lenis.start(); }
  burger.addEventListener('click', () => {
    const open = !menu.classList.contains('is-open');
    menu.classList.toggle('is-open', open); burger.classList.toggle('is-open', open); burger.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('is-locked', open); if (lenis) open ? lenis.stop() : lenis.start();
  });

  /* ---------- progress bar ---------- */
  if (hasGsap && !reduce) gsap.to('.progress', { scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: 0.3 } });

  /* ---------- cursor ---------- */
  if (fine && !reduce && hasGsap) {
    const cur = $('.cursor'), label = $('.cursor__label');
    let x = 0, y = 0, rx = 0, ry = 0;
    window.addEventListener('pointermove', e => { x = e.clientX; y = e.clientY; cur.classList.add('is-on'); }, { passive: true });
    document.addEventListener('mouseleave', () => cur.classList.remove('is-on'));
    gsap.ticker.add(() => { rx += (x - rx) * 0.2; ry += (y - ry) * 0.2; cur.style.transform = `translate3d(${rx}px,${ry}px,0)`; });
    const bind = el => {
      el.addEventListener('mouseenter', () => { label.textContent = lang === 'en' && el.dataset.cursorEn ? el.dataset.cursorEn : el.dataset.cursor; cur.classList.add('is-hover'); });
      el.addEventListener('mouseleave', () => cur.classList.remove('is-hover'));
    };
    $$('[data-cursor]').forEach(bind);
  }

  /* ---------- hero ---------- */
  const hero = $('#hero'), heroVideo = $('.hero__video');
  if (heroVideo) {
    /* sources attach after load so the poster wins LCP and the loop streams in behind it */
    const attach = () => { $$('source[data-src]', heroVideo).forEach(s => { s.src = s.dataset.src; }); heroVideo.load(); heroVideo.play().catch(() => {}); };
    if (reduce) heroVideo.removeAttribute('autoplay');
    else if (document.readyState === 'complete') attach();
    else window.addEventListener('load', () => setTimeout(attach, 120));
  }
  const tc = $('.hud__tc');
  if (tc) {
    const pad = n => String(n).padStart(2, '0'); const t0 = performance.now();
    setInterval(() => { const s = (performance.now() - t0) / 1000; tc.textContent = `TC ${pad(Math.floor(s / 3600))}:${pad(Math.floor(s / 60) % 60)}:${pad(Math.floor(s) % 60)}:${pad(Math.floor((s % 1) * 25))}`; }, 40);
  }
  if (hasGsap && !reduce && hero) {
    gsap.from('.hero__title .ch', { yPercent: 120, duration: 1.3, ease: 'power4.out', stagger: 0.08, delay: 0.15 });
    gsap.from('[data-reveal-hero]', { y: 24, opacity: 0, duration: 1, ease: 'power3.out', stagger: 0.1, delay: 0.7 });
    gsap.from('.hud', { opacity: 0, duration: 1.2, delay: 1 });
    gsap.timeline({ scrollTrigger: { trigger: hero, start: 'top top', end: '+=110%', pin: true, scrub: true, anticipatePin: 1 } })
      .to('.hero__media', { scale: 0.8, borderRadius: 28, ease: 'none' }, 0)
      .to('.hero__title', { yPercent: -35, opacity: 0, ease: 'none' }, 0)
      .to(['.hero__row', '.hero__kicker', '.hud', '.hero__scroll'], { opacity: 0, y: -24, ease: 'none', stagger: 0 }, 0);
  }

  /* ---------- generic reveals + parallax ---------- */
  if (hasGsap && !reduce) {
    $$('[data-reveal]').forEach(el => gsap.from(el, { y: 36, opacity: 0, duration: 1.1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 90%', once: true } }));
    $$('[data-speed]').forEach(el => {
      const s = parseFloat(el.dataset.speed) || 1; const scope = el.closest('[data-parallax-scope]') || el; const amp = 220;
      gsap.fromTo(el, { y: (s - 1) * amp }, { y: -(s - 1) * amp, ease: 'none', scrollTrigger: { trigger: scope, start: 'top bottom', end: 'bottom top', scrub: true, invalidateOnRefresh: true } });
    });
  }

  /* ---------- disciplines: horizontal pin ---------- */
  if (hasGsap) {
    const mm = gsap.matchMedia();
    mm.add('(min-width: 900px) and (prefers-reduced-motion: no-preference)', () => {
      const track = $('.disc__track'); if (!track) return;
      const dist = () => track.scrollWidth - window.innerWidth;
      gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: { trigger: '#disciplines', start: 'top top', end: () => '+=' + dist(), pin: true, scrub: true, invalidateOnRefresh: true, anticipatePin: 1 } });
      $$('.disc__bg img').forEach(img => gsap.fromTo(img, { xPercent: -6 }, { xPercent: 6, ease: 'none', scrollTrigger: { trigger: '#disciplines', start: 'top top', end: () => '+=' + dist(), scrub: true } }));
    });
    /* reel wall columns drift at three speeds */
    mm.add('(min-width: 600px) and (prefers-reduced-motion: no-preference)', () => {
      const wall = $('[data-wall]'); if (!wall) return;
      [-0.16, 0.1, -0.24].forEach((v, i) => {
        const col = $(`.wall__col:nth-child(${i + 1})`, wall); if (!col) return;
        gsap.fromTo(col, { y: () => -v * window.innerHeight * 0.5 }, { y: () => v * window.innerHeight * 0.5, ease: 'none', scrollTrigger: { trigger: wall, start: 'top bottom', end: 'bottom top', scrub: true, invalidateOnRefresh: true } });
      });
    });
    mm.add('(prefers-reduced-motion: no-preference)', () => {
      $$('[data-filmreveal]').forEach(el => gsap.fromTo(el, { clipPath: 'inset(0 100% 0 0 round 12px)' }, { clipPath: 'inset(0 0% 0 0 round 12px)', duration: 1.3, ease: 'power4.inOut', scrollTrigger: { trigger: el, start: 'top 85%', once: true } }));
    });
  }

  /* ---------- lightbox ---------- */
  const lb = $('#lightbox'), lbBody = $('.lb__body'), lbCap = $('.lb__cap');
  let lastFocus = null;
  function openLightbox({ type, src, poster, title, vertical }) {
    lastFocus = document.activeElement; lbBody.innerHTML = '';
    if (type === 'video') {
      const v = document.createElement('video'); v.src = src; v.controls = true; v.autoplay = true; v.playsInline = true; if (poster) v.poster = poster; if (vertical) v.classList.add('is-vertical'); lbBody.appendChild(v);
    } else { const i = new Image(); i.src = src; i.alt = title || ''; lbBody.appendChild(i); }
    lbCap.textContent = title || ''; lb.classList.add('is-open'); document.body.classList.add('is-locked'); lenis && lenis.stop(); $('.lb__close').focus();
  }
  function closeLightbox() {
    const v = $('video', lbBody); if (v) { v.pause(); v.removeAttribute('src'); v.load(); }
    lb.classList.remove('is-open'); lbBody.innerHTML = ''; document.body.classList.remove('is-locked'); lenis && lenis.start(); lastFocus && lastFocus.focus && lastFocus.focus();
  }
  $('.lb__close').addEventListener('click', closeLightbox);
  lb.addEventListener('click', e => { if (e.target === lb || e.target === lbBody) closeLightbox(); });
  const activate = (el, fn) => { el.addEventListener('click', fn); el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fn(); } }); };

  /* ---------- reel wall clips ---------- */
  const playClip = (c, v) => v.play().then(() => c.classList.add('is-playing')).catch(() => {});
  const stopClip = (c, v) => { v.pause(); c.classList.remove('is-playing'); };
  const clips = $$('.clip');
  clips.forEach(c => {
    const v = $('video', c);
    if (fine) { c.addEventListener('mouseenter', () => playClip(c, v)); c.addEventListener('mouseleave', () => stopClip(c, v)); }
    activate(c, () => openLightbox({ type: 'video', src: c.dataset.src, poster: c.dataset.poster, title: lang === 'en' ? c.dataset.titleEn : c.dataset.title, vertical: true }));
  });
  if (!fine && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { const c = e.target, v = $('video', c); e.intersectionRatio >= 0.6 ? playClip(c, v) : stopClip(c, v); }), { threshold: [0, 0.6, 1] });
    clips.forEach(c => io.observe(c));
  }

  /* ---------- films ---------- */
  $$('.film-row').forEach(row => {
    const media = $('.film-row__media', row), v = $('video', media);
    if ('IntersectionObserver' in window && !reduce) {
      new IntersectionObserver(es => es.forEach(e => { e.isIntersecting ? v.play().then(() => media.classList.add('is-playing')).catch(() => {}) : (v.pause(), media.classList.remove('is-playing')); }), { threshold: 0.35 }).observe(media);
    }
    activate(row, () => openLightbox({ type: 'video', src: row.dataset.src, poster: row.dataset.poster, title: row.dataset.title }));
  });

  /* ---------- photos ---------- */
  $$('.chip').forEach(ch => ch.addEventListener('click', () => {
    const f = ch.dataset.filter; $$('.chip').forEach(c => c.classList.toggle('is-active', c === ch));
    $$('.ph').forEach(p => p.classList.toggle('is-hidden', f !== 'all' && p.dataset.cat !== f));
    hasGsap && ScrollTrigger.refresh();
  }));
  $$('.ph').forEach(p => activate(p, () => openLightbox({ type: 'image', src: p.dataset.full, title: lang === 'en' ? p.dataset.titleEn : p.dataset.title })));

  /* ---------- design tilt ---------- */
  $$('.dcard').forEach(card => {
    const inner = $('.dcard__inner', card);
    if (fine && !reduce) {
      card.addEventListener('pointermove', e => { const r = card.getBoundingClientRect(); const px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5; inner.style.transform = `rotateX(${-py * 10}deg) rotateY(${px * 12}deg) translateZ(6px)`; });
      card.addEventListener('pointerleave', () => { inner.style.transform = ''; });
    }
    activate(card, () => openLightbox({ type: 'image', src: card.dataset.full, title: card.dataset.title }));
  });

  /* ---------- compare sliders ---------- */
  $$('[data-cmp]').forEach(c => {
    const after = $('.cmp__after', c), handle = $('.cmp__handle', c); let pos = 100, drag = false, touched = false, st = null;
    const set = p => { pos = Math.max(0, Math.min(100, p)); after.style.clipPath = `inset(0 0 0 ${pos}%)`; handle.style.left = pos + '%'; };
    const move = e => { const r = c.getBoundingClientRect(); set(((e.clientX - r.left) / r.width) * 100); };
    c.addEventListener('pointerdown', e => { drag = true; touched = true; st && st.kill(); c.setPointerCapture(e.pointerId); move(e); });
    c.addEventListener('pointermove', e => drag && move(e));
    c.addEventListener('pointerup', () => { drag = false; }); c.addEventListener('pointercancel', () => { drag = false; });
    c.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') set(pos - 4); if (e.key === 'ArrowRight') set(pos + 4); });
    c.tabIndex = 0;
    if (hasGsap && !reduce) { const o = { p: 100 }; st = gsap.to(o, { p: 50, ease: 'none', scrollTrigger: { trigger: c, start: 'top 85%', end: 'top 25%', scrub: true, onUpdate: () => !touched && set(o.p) } }).scrollTrigger; }
    else set(50);
  });

  /* ---------- legal modals ---------- */
  $$('[data-modal]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); const m = $('#modal-' + a.dataset.modal); if (!m) return; lastFocus = a; m.classList.add('is-open'); document.body.classList.add('is-locked'); lenis && lenis.stop(); $('.modal__close', m).focus(); }));
  const closeModals = () => { $$('.modal.is-open').forEach(m => m.classList.remove('is-open')); if (!lb.classList.contains('is-open')) { document.body.classList.remove('is-locked'); lenis && lenis.start(); } lastFocus && lastFocus.focus && lastFocus.focus(); };
  $$('[data-modal-close]').forEach(b => b.addEventListener('click', closeModals));
  $$('.modal').forEach(m => m.addEventListener('click', e => { if (e.target === m) closeModals(); }));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { if (lb.classList.contains('is-open')) closeLightbox(); closeModals(); if (menu.classList.contains('is-open')) closeMenu(); } });

  /* ---------- boot ---------- */
  applyLang(lang);
  window.addEventListener('load', () => hasGsap && ScrollTrigger.refresh());
  document.fonts && document.fonts.ready.then(() => hasGsap && ScrollTrigger.refresh());
})();
