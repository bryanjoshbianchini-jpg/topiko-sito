// Oggetti 3D legati allo scorrimento: si entra nella macchina fotografica e nel computer.
// I fotogrammi si caricano solo quando la sezione si avvicina. Con movimento ridotto o rete lenta resta l'ultima immagine.
(() => {
  const sezioni = [...document.querySelectorAll('[data-entra]')];
  if (!sezioni.length) return;
  const fermo = matchMedia('(prefers-reduced-motion:reduce)').matches;
  const rete = navigator.connection;
  const lenta = rete && (rete.saveData || /(^|-)2g|3g/.test(rete.effectiveType || ''));

  sezioni.forEach(sez => {
    const [cartella, totale] = sez.dataset.entra.split(':');
    const N = +totale, canvas = sez.querySelector('canvas'), ctx = canvas.getContext('2d'), testo = sez.querySelector('.entra-testo');
    const telefono = () => innerWidth < 760;
    const suffisso = telefono() ? '-m' : '';
    const src = i => `${cartella}${suffisso}/f_${String(i + 1).padStart(3, '0')}.webp`;
    const passo = telefono() ? 2 : 1;
    const imgs = new Array(N);
    const carica = i => {
      if (imgs[i]) return imgs[i];
      const im = imgs[i] = new Image();
      im.decoding = 'async'; im.src = src(i);
      im.onload = () => { sporco = true; sveglia(); };
      return im;
    };
    let prog = 0, cur = 0, sporco = true, visibile = false, inCorso = false, avviato = false;

    const vicino = f => {
      for (let d = 0; d < N; d++) for (const j of [f - d, f + d]) {
        const im = imgs[j]; if (im && im.complete && im.naturalWidth) return im;
      }
      return null;
    };
    const misura = () => {
      const d = Math.min(devicePixelRatio || 1, 1.5);
      canvas.width = Math.round(canvas.clientWidth * d); canvas.height = Math.round(canvas.clientHeight * d);
      sporco = true; sveglia();
    };
    const disegna = () => {
      const im = vicino(Math.round(cur));
      if (!im) return false;
      const w = canvas.width, h = canvas.height, iw = im.naturalWidth, ih = im.naturalHeight;
      // da telefono l'oggetto parte intero e alla fine l'immagine riempie lo schermo
      const copre = Math.max(w / iw, h / ih), dentro = Math.min(copre, Math.min(w / iw, h / ih) * 1.45);
      const t = cur / (N - 1), k = t * t * t;
      const s = dentro + (copre - dentro) * k;
      const dw = iw * s, dh = ih * s;
      ctx.fillStyle = '#0D0A12'; ctx.fillRect(0, 0, w, h);
      ctx.drawImage(im, (w - dw) / 2, (h - dh) / 2, dw, dh);
      return true;
    };
    const aggiornaTesto = () => {
      const q = Math.min(1, Math.max(0, (prog - .84) / .1));
      testo.style.opacity = q;
      testo.style.transform = `translateY(${(1 - q) * 28}px)`;
      testo.style.pointerEvents = q > .5 ? 'auto' : 'none';
      testo.setAttribute('aria-hidden', q > .5 ? 'false' : 'true');
    };
    function sveglia() { if (!inCorso && visibile) { inCorso = true; requestAnimationFrame(giro); } }
    function giro() {
      const meta = Math.min(prog / .9, 1) * (N - 1);
      const prima = cur;
      cur += (meta - cur) * .16;
      if (Math.abs(meta - cur) < .01) cur = meta;
      if (cur !== prima || sporco) sporco = !disegna();
      if (cur === meta && !sporco) { inCorso = false; return; }
      requestAnimationFrame(giro);
    }
    const leggiScorrimento = () => {
      const r = sez.getBoundingClientRect(), corsa = sez.offsetHeight - innerHeight;
      prog = corsa > 0 ? Math.min(1, Math.max(0, -r.top / corsa)) : 1;
      aggiornaTesto(); sveglia();
    };
    const avvia = () => {
      if (avviato) return; avviato = true;
      if (fermo || lenta) { sez.classList.add('ferma'); carica(N - 1); cur = N - 1; prog = 1; misura(); aggiornaTesto(); return; }
      carica(0);
      let i = passo;
      const prossimo = () => { for (let k = 0; k < 5 && i < N; k++, i += passo) carica(i); if (i < N) setTimeout(prossimo, 90); else carica(N - 1); };
      prossimo();
      addEventListener('scroll', leggiScorrimento, {passive: true});
      leggiScorrimento();
    };
    new IntersectionObserver(es => {
      visibile = es[0].isIntersecting;
      if (visibile) { avvia(); misura(); }
    }, {rootMargin: '120% 0px'}).observe(sez);
    addEventListener('resize', () => { if (avviato) { misura(); if (!fermo && !lenta) leggiScorrimento(); } });
  });
})();
