// Minimal offline slide engine. No dependencies.
// Keys: ArrowRight / PageDown / Space / Enter = next step; ArrowLeft / PageUp / Backspace = previous;
// Home / End; F = fullscreen; B or . = black screen; O = overview; Escape = leave overview.
// Microsoft presentation clickers send PageDown / PageUp (and sometimes F5 / B / period), all handled here.
(() => {
  const slides = Array.from(document.querySelectorAll('.slide'));
  const counter = document.getElementById('counter');
  let i = 0;

  const hashIndex = () => {
    const n = parseInt(location.hash.replace('#', ''), 10);
    return Number.isFinite(n) && n >= 1 && n <= slides.length ? n - 1 : 0;
  };

  function fragments(s) { return Array.from(s.querySelectorAll('.frag')); }

  function show(n, { fromEnd = false } = {}) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach((s, k) => {
      s.classList.toggle('active', k === i);
      s.classList.toggle('past', k < i);
    });
    const fr = fragments(slides[i]);
    fr.forEach(f => f.classList.toggle('on', fromEnd));
    history.replaceState(null, '', '#' + (i + 1));
    if (counter) counter.textContent = `${i + 1} / ${slides.length}`;
    document.body.dataset.slide = slides[i].id || String(i + 1);
    // pause any video on other slides, play autoplay video on this one
    document.querySelectorAll('video').forEach(v => { if (!slides[i].contains(v)) v.pause(); });
    slides[i].querySelectorAll('video[data-autoplay]').forEach(v => v.play().catch(() => {}));
  }

  function next() {
    const fr = fragments(slides[i]).filter(f => !f.classList.contains('on'));
    if (fr.length) { fr[0].classList.add('on'); return; }
    if (i < slides.length - 1) show(i + 1);
  }
  function prev() {
    const on = fragments(slides[i]).filter(f => f.classList.contains('on'));
    if (on.length) { on[on.length - 1].classList.remove('on'); return; }
    if (i > 0) show(i - 1, { fromEnd: true });
  }

  function toggleBlack() { document.body.classList.toggle('black'); }
  function toggleOverview() { document.body.classList.toggle('overview'); }
  function fullscreen() {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
    else document.exitFullscreen?.();
  }

  document.addEventListener('keydown', e => {
    if (e.target && ['INPUT', 'TEXTAREA'].includes(e.target.tagName)) return;
    switch (e.key) {
      case 'ArrowRight': case 'PageDown': case ' ': case 'Enter': case 'ArrowDown':
        e.preventDefault();
        if (document.body.classList.contains('overview')) { show(i + 1); } else next();
        break;
      case 'ArrowLeft': case 'PageUp': case 'Backspace': case 'ArrowUp':
        e.preventDefault(); if (document.body.classList.contains('overview')) { show(i - 1); } else prev(); break;
      case 'Home': e.preventDefault(); show(0); break;
      case 'End': e.preventDefault(); show(slides.length - 1); break;
      case 'f': case 'F': fullscreen(); break;
      case 'F5': e.preventDefault(); fullscreen(); break;
      case 'b': case 'B': case '.': toggleBlack(); break;
      case 'o': case 'O': toggleOverview(); break;
      case 'Escape': document.body.classList.remove('overview', 'black'); break;
    }
  });

  // Overview: click a slide to jump to it
  document.addEventListener('click', e => {
    if (!document.body.classList.contains('overview')) return;
    const s = e.target.closest('.slide');
    if (s) { show(slides.indexOf(s)); document.body.classList.remove('overview'); }
  });

  // Touch swipe for a tablet
  let tx = null;
  document.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', e => {
    if (tx === null) return;
    const dx = e.changedTouches[0].clientX - tx; tx = null;
    if (Math.abs(dx) > 60) (dx < 0 ? next() : prev());
  });

  window.addEventListener('hashchange', () => show(hashIndex()));

  // Scale the 1920x1080 stage to the window, letterboxed
  function fit() {
    const stage = document.getElementById('stage');
    if (!stage) return;
    const s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    stage.style.transform = `translate(-50%, -50%) scale(${s})`;
  }
  window.addEventListener('resize', fit);
  fit();
  show(hashIndex());
})();
