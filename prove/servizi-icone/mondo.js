// il mondo dei servizi: una sfera di punti (Fibonacci) col gradiente Topiko che gira piano su un asse inclinato.
// Le pillole sono agganciate a punti della sfera con un filo: davanti sono grandi e sopra al mondo, dietro piccole, trasparenti e sotto.
// Passando su un servizio (pillola o voce dell'elenco) il mondo rallenta e il filo si accende. Si ferma fuori schermo.
// Modalità leggera: meno punti. Movimento ridotto: fermo, con le pillole già al loro posto.
(() => {
  document.querySelectorAll('[data-mondo]').forEach(box => {
    const cv = box.querySelector('canvas'), ctx = cv.getContext('2d');
    const pil = [...box.querySelectorAll('.m-p')];
    const ridotto = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const leggero = () => document.documentElement.classList.contains('leggero');
    const STOPS = [[155, 3, 255], [255, 0, 130], [255, 122, 47]];
    const mix = t => { const q = Math.min(1.999, Math.max(0, t) * 2), j = Math.floor(q), f = q - j, a = STOPS[j], b = STOPS[j + 1]; return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f]; };
    let punti = [], N = 0;
    const fibonacci = n => {
      N = n; punti = []; const g = Math.PI * (3 - Math.sqrt(5));
      for (let i = 0; i < n; i++) {
        const y = 1 - (i + .5) / n * 2, rr = Math.sqrt(1 - y * y), th = g * i, x = Math.cos(th) * rr, z = Math.sin(th) * rr;
        const c = mix((x * .35 - y * .75 + 1) / 2);
        punti.push([x, y, z, `rgb(${c[0] | 0},${c[1] | 0},${c[2] | 0})`]);
      }
    };
    // ancore delle pillole: longitudini uguali, latitudini alterne, così davanti non coprono il logo
    const anc = pil.map((p, i) => { const sopra = i % 2 === 0, n = Math.ceil(pil.length / 2), j = Math.floor(i / 2), lon = (j / n + (sopra ? 0 : .5 / n)) * Math.PI * 2, lat = sopra ? .55 : -.5; return [Math.cos(lat) * Math.sin(lon), Math.sin(lat), Math.cos(lat) * Math.cos(lon)]; });
    const TILT = -0.38, ct = Math.cos(TILT), st = Math.sin(TILT);
    const ruota = (v, a) => { const ca = Math.cos(a), sa = Math.sin(a); const x = v[0] * ca + v[2] * sa, z = -v[0] * sa + v[2] * ca, y = v[1]; return [x, y * ct - z * st, y * st + z * ct]; };
    let misurePil = [], W = 0, dpr = 1, R = 0, ang = 0.35, vel = 0.16, vis = false, rAF = 0, ult = 0;
    const misura = () => {
      W = box.clientWidth; dpr = Math.min(devicePixelRatio || 1, 2);
      cv.width = Math.round(W * dpr); cv.height = Math.round(W * dpr);
      R = W * (W < 500 ? .31 : .33); misurePil = pil.map(p => [p.offsetWidth / 2, p.offsetHeight / 2]);
      fibonacci(leggero() ? 380 : (W < 500 ? 520 : 760));
    };
    const disegna = () => {
      const c = W / 2, D = R * 4.2;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, W);
      const proj = (v, k) => { const f = D / (D - v[2] * k); return [c + v[0] * k * f, c - v[1] * k * f, f]; };
      const fuoco = pil.find(p => p.classList.contains('acceso'));
      // pillole e fili
      const lr = W * (W < 500 ? .13 : .12) + 26;  // raggio del logo più mezzo spessore della pillola: le pillole non lo coprono
      const info = pil.map((p, i) => {
        const v = ruota(anc[i], ang), b = proj(v, R * (W < 500 ? 1.3 : 1.38));
        let dx = b[0] - c, dy = b[1] - c; const d = Math.hypot(dx, dy) || 1;
        if (d < lr) { dx *= lr / d; dy *= lr / d; }
        const [hw, hh] = misurePil[i] || [40, 16];
        b[0] = Math.min(W - hw * .9 - 2, Math.max(hw * .9 + 2, c + dx)); b[1] = Math.min(W - hh - 2, Math.max(hh + 2, c + dy));
        return {p, v, a: proj(v, R), b};
      });
      // almeno l'80% delle pillole resta visibile: spariscono solo le più nascoste dietro (2 su 15, così anche durante la dissolvenza restano almeno 12), con una dissolvenza
      const zs = info.map(o => o.v[2]).sort((x, y) => x - y), nasc = Math.max(0, Math.floor(info.length * .2) - 1);
      const thr = nasc ? (zs[nasc - 1] + zs[nasc]) / 2 : -9, fw = nasc ? Math.max(.02, Math.min(.15, zs[nasc] - zs[nasc - 1])) : 1;
      const alfaDi = o => o.p === fuoco ? 1 : Math.min(1, Math.max(0, .5 + (o.v[2] - thr) / fw));
      // con più pillole in vista alcune si toccherebbero: quella più dietro si sposta in alto o in basso quanto basta
      const vis2 = info.filter(o => alfaDi(o) > 0).sort((x, y) => y.v[2] - x.v[2]);
      for (let giro2 = 0; giro2 < 4; giro2++) for (let i = 0; i < vis2.length; i++) for (let j = i + 1; j < vis2.length; j++) {
        const A = vis2[i], B = vis2[j], [aw, ah] = misurePil[pil.indexOf(A.p)] || [40, 16], [bw, bh] = misurePil[pil.indexOf(B.p)] || [40, 16];
        const ox = aw * .9 + bw * .9 + 6 - Math.abs(A.b[0] - B.b[0]), oy = ah + bh + 6 - Math.abs(A.b[1] - B.b[1]);
        if (ox > 0 && oy > 0) { const su = B.b[1] < A.b[1] || (B.b[1] === A.b[1] && B.b[1] < c); B.b[1] = Math.min(W - bh - 2, Math.max(bh + 2, B.b[1] + (su ? -oy : oy))); }
      }
      const filo = (o, sopra) => {
        const acc = o.p === fuoco;
        ctx.globalAlpha = acc ? 1 : .55 * alfaDi(o) * (o.v[2] < 0 ? .55 : 1);
        if (acc) { const g = ctx.createLinearGradient(o.a[0], o.a[1], o.b[0], o.b[1]); g.addColorStop(0, '#9B03FF'); g.addColorStop(.5, '#FF0082'); g.addColorStop(1, '#FF7A2F'); ctx.strokeStyle = g; ctx.lineWidth = 2.2; }
        else { ctx.strokeStyle = '#8A6FB0'; ctx.lineWidth = 1; }
        ctx.beginPath(); ctx.moveTo(o.a[0], o.a[1]); ctx.lineTo(o.b[0], o.b[1]); ctx.stroke();
        ctx.globalAlpha = 1; ctx.fillStyle = acc ? '#FF0082' : '#9B03FF';
        ctx.beginPath(); ctx.arc(o.a[0], o.a[1], acc ? 3.4 : 2.4, 0, 6.2832); ctx.fill();
      };
      // dietro: resta solo il punto d'aggancio, senza filo né pillola
      info.filter(o => o.v[2] < 0 && o.p !== fuoco && alfaDi(o) > 0).forEach(o => filo(o));
      info.filter(o => o.v[2] < 0 && o.p !== fuoco && alfaDi(o) === 0).forEach(o => { ctx.globalAlpha = .5; ctx.fillStyle = '#9B03FF'; ctx.beginPath(); ctx.arc(o.a[0], o.a[1], 2.2, 0, 6.2832); ctx.fill(); ctx.globalAlpha = 1; });
      // sfera: prima i punti dietro, poi quelli davanti
      const rp = Math.max(1.1, R * .0105);
      for (const pass of [0, 1]) for (const pt of punti) {
        const v = ruota(pt, ang); if ((v[2] >= 0) !== !!pass) continue;
        const q = proj(v, R), luce = (v[2] + 1) / 2;
        ctx.globalAlpha = .14 + .86 * luce * luce; ctx.fillStyle = pt[3];
        ctx.beginPath(); ctx.arc(q[0], q[1], rp * (.55 + .6 * luce), 0, 6.2832); ctx.fill();
      }
      ctx.globalAlpha = 1;
      info.filter(o => o.v[2] >= 0 || o.p === fuoco).forEach(o => { ctx.save(); ctx.globalAlpha = 1; filo(o, true); ctx.restore(); });
      for (const o of info) {
        const z = o.v[2], s = z < 0 ? .8 + .05 * (1 + z) : .85 + .2 * z;
        const acc = o.p === fuoco;
        o.p.style.transform = `translate(${o.b[0].toFixed(1)}px,${o.b[1].toFixed(1)}px) translate(-50%,-50%) scale(${(acc ? Math.max(1.05, s) : s).toFixed(3)})`;
        // si vede solo quando il testo è leggibile: davanti o di lato verso davanti; dietro sparisce con una dissolvenza veloce
        const a0 = alfaDi(o), alfa = acc ? 1 : a0 * (z < 0 ? .82 + .18 * (1 + z) : 1);
        o.p.style.opacity = alfa.toFixed(3); o.p.style.visibility = alfa > 0 ? 'visible' : 'hidden';
        o.p.style.pointerEvents = alfa > .5 ? '' : 'none';
        o.p.style.zIndex = acc ? 7 : (z < 0 ? 4 : 5);
      }
    };
    const giro = ts => {
      rAF = 0; if (!vis) return;
      const dt = Math.min(50, ts - (ult || ts)) / 1000; ult = ts;
      const target = pil.some(p => p.classList.contains('acceso')) ? .03 : .16;
      vel += (target - vel) * Math.min(1, dt * 4);
      ang += vel * dt; disegna();
      rAF = requestAnimationFrame(giro);
    };
    misura(); disegna();
    if (!ridotto) new IntersectionObserver(es => {
      vis = es[es.length - 1].isIntersecting;
      if (vis && !rAF) { ult = 0; rAF = requestAnimationFrame(giro); }
      if (!vis) { cancelAnimationFrame(rAF); rAF = 0; }
    }, {rootMargin: '80px 0px'}).observe(box);
    else (box.closest('section') || box).addEventListener('pointerover', () => setTimeout(disegna, 0));
    let lw = W; new ResizeObserver(() => { if (box.clientWidth !== lw) { lw = box.clientWidth; misura(); disegna(); } }).observe(box);
  });
})();
