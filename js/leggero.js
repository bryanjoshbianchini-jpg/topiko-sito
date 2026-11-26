// Prestazioni: se il computer fatica mentre si scorre, il vetro diventa un pannello semplice. L'aspetto resta scuro e pulito.
(() => {
  const CHIAVE = 'topiko_leggero', html = document.documentElement;
  const attiva = () => {
    html.classList.add('leggero');
    try { sessionStorage.setItem(CHIAVE, '1'); } catch {}
  };
  try { if (sessionStorage.getItem(CHIAVE)) { html.classList.add('leggero'); return; } } catch {}
  const risparmio = navigator.connection && navigator.connection.saveData;
  if (risparmio || (navigator.deviceMemory && navigator.deviceMemory <= 4) || matchMedia('(prefers-reduced-motion:reduce)').matches) { attiva(); return; }
  // misura i primi 40 fotogrammi mentre la pagina scorre
  let n = 0, inizio = 0, ultimo = 0, lenti = 0, finito = false;
  const passo = t => {
    if (finito) return;
    if (ultimo && t - ultimo > 24) lenti++;
    ultimo = t; n++;
    if (n >= 40) { finito = true; if (lenti >= 12) attiva(); return; }
    requestAnimationFrame(passo);
  };
  addEventListener('scroll', () => { if (!inizio) { inizio = 1; requestAnimationFrame(passo); } }, {passive: true});
})();

document.querySelectorAll('.universo').forEach(u => new IntersectionObserver(es => u.classList.toggle('vivo', es[0].isIntersecting)).observe(u));
