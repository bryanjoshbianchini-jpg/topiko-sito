// Servizi: i riquadri si aprono sul posto, uno alla volta, senza cambiare pagina.
// Si chiudono con il tasto Chiudi, con Esc, con un altro clic o con il tasto indietro del telefono.
(() => {
  const griglia = document.querySelector('.servizi-g');
  if (!griglia) return;
  const voci = [...griglia.querySelectorAll('details')];
  const transizione = fn => {
    if (!document.startViewTransition || matchMedia('(prefers-reduced-motion:reduce)').matches) return fn();
    const vt = document.startViewTransition(fn);
    vt.ready.catch(() => {}); vt.finished.catch(() => {});
  };
  const vai = el => {
    const top = el.getBoundingClientRect().top + scrollY - 96;
    scrollTo({top, behavior: 'smooth'});
  };
  const chiudi = (d, storia = true) => {
    transizione(() => { d.open = false; });
    if (storia && history.state && history.state.servizio) history.back();
  };
  const apri = (d, storia = true) => {
    transizione(() => {
      voci.forEach(v => { v.open = v === d; });
    });
    if (storia) history.pushState({servizio: d.id}, '', `#${d.id}`);
    setTimeout(() => vai(d), 60);
  };
  voci.forEach(d => {
    d.querySelector('summary').addEventListener('click', e => {
      e.preventDefault();
      d.open ? chiudi(d) : apri(d);
    });
    const x = d.querySelector('.s-chiudi');
    if (x) x.addEventListener('click', () => { chiudi(d); d.querySelector('summary').focus({preventScroll: true}); });
  });
  addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    const d = voci.find(v => v.open);
    if (d) { chiudi(d); d.querySelector('summary').focus({preventScroll: true}); }
  });
  addEventListener('popstate', () => {
    const id = (history.state && history.state.servizio) || location.hash.slice(1);
    const d = voci.find(v => v.id === id);
    transizione(() => voci.forEach(v => { v.open = v === d; }));
  });
  // arrivo da un link diretto, per esempio servizi.html#social
  const iniziale = voci.find(v => v.id === location.hash.slice(1));
  if (iniziale) { iniziale.open = true; history.replaceState({servizio: iniziale.id}, '', location.hash); setTimeout(() => vai(iniziale), 300); }
})();
