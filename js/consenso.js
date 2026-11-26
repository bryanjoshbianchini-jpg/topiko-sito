// Banner cookie e consenso. Senza una scelta positiva non parte nessun tracciamento.
// Statistiche e pubblicità si attivano solo su topikolab.it: anteprime e bozze non sporcano i dati.
// Con GTM_ID in config.js parte solo Tag Manager, che gestisce GA4 e pixel. Senza, partono GA4 e pixel diretti.
(() => {
  const CHIAVE = 'topiko_consenso', VERSIONE = 1, DURATA = 182 * 864e5; // la scelta vale circa 6 mesi
  const cfg = window.TOPIKO || {};
  const sitoVero = /(^|\.)topikolab\.it$/.test(location.hostname);
  const caricati = {};

  window.dataLayer = window.dataLayer || [];
  const gtag = window.gtag = function () { window.dataLayer.push(arguments); };
  gtag('consent', 'default', {ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'denied', wait_for_update: 500});

  const leggi = () => {
    try {
      const c = JSON.parse(localStorage.getItem(CHIAVE));
      return c && c.v === VERSIONE && Date.now() - c.data < DURATA ? c : null;
    } catch { return null; }
  };
  const scrivi = c => { try { localStorage.setItem(CHIAVE, JSON.stringify(c)); } catch {} };

  const script = src => {
    if (caricati[src]) return;
    caricati[src] = true;
    const s = document.createElement('script');
    s.async = true; s.src = src;
    document.head.appendChild(s);
  };

  const pixel = id => {
    if (window.fbq) return;
    const f = window.fbq = function () { f.callMethod ? f.callMethod.apply(f, arguments) : f.queue.push(arguments); };
    window._fbq = f; f.push = f; f.loaded = true; f.version = '2.0'; f.queue = [];
    script('https://connect.facebook.net/en_US/fbevents.js');
    f('init', id);
    f('track', 'PageView');
  };

  const applica = c => {
    const sta = c.statistiche ? 'granted' : 'denied', mkt = c.marketing ? 'granted' : 'denied';
    gtag('consent', 'update', {analytics_storage: sta, ad_storage: mkt, ad_user_data: mkt, ad_personalization: mkt});
    window.dataLayer.push({event: 'consenso_aggiornato', consenso_statistiche: !!c.statistiche, consenso_marketing: !!c.marketing});
    if (!sitoVero) return;
    if (cfg.GTM_ID) {
      if (!c.statistiche && !c.marketing) return;
      window.dataLayer.push({'gtm.start': Date.now(), event: 'gtm.js'});
      script(`https://www.googletagmanager.com/gtm.js?id=${encodeURIComponent(cfg.GTM_ID)}`);
      return;
    }
    if (c.statistiche && cfg.GA4_ID) {
      script(`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(cfg.GA4_ID)}`);
      gtag('js', new Date());
      gtag('config', cfg.GA4_ID);
    }
    if (c.marketing && cfg.PIXEL_ID) pixel(cfg.PIXEL_ID);
  };

  // chi ritira il consenso: si cancellano i cookie già salvati e si ricarica la pagina senza tracciamenti
  const cancellaCookie = () => {
    const dominio = location.hostname.replace(/^www\./, '');
    document.cookie.split(';').map(x => x.split('=')[0].trim()).filter(n => /^(_ga|_gid|_gat|_gcl|_fbp|_fbc)/.test(n)).forEach(n => {
      [`path=/`, `path=/; domain=${dominio}`, `path=/; domain=.${dominio}`].forEach(d => {
        document.cookie = `${n}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; ${d}`;
      });
    });
  };

  let banner = null;
  const chiudi = () => { if (banner) banner.remove(); banner = null; };

  const salva = (statistiche, marketing) => {
    const prima = leggi();
    scrivi({v: VERSIONE, data: Date.now(), statistiche, marketing});
    chiudi();
    if (prima && ((prima.statistiche && !statistiche) || (prima.marketing && !marketing))) {
      cancellaCookie();
      location.reload();
      return;
    }
    applica({statistiche, marketing});
  };

  const apri = () => {
    chiudi();
    const c = leggi() || {};
    banner = document.createElement('section');
    banner.className = 'consenso';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Preferenze cookie');
    banner.innerHTML = `
      <button class="consenso-x" type="button" aria-label="Chiudi e rifiuta i cookie non necessari">&times;</button>
      <h2>Prima del caffè, i cookie</h2>
      <p>I cookie tecnici fanno funzionare il sito. Con il tuo consenso usiamo anche Google Analytics per le statistiche. Per la pubblicità usiamo il pixel di Meta. Se chiudi con la X, restano solo i cookie tecnici. Puoi cambiare idea quando vuoi da "Preferenze cookie", in fondo alla pagina. Trovi i dettagli nella <a href="cookie.html">cookie policy</a>.</p>
      <div class="consenso-scelte" hidden>
        <label><input type="checkbox" checked disabled> <span><b>Tecnici</b> Sempre attivi: servono al sito.</span></label>
        <label><input type="checkbox" id="consenso-stat"${c.statistiche ? ' checked' : ''}> <span><b>Statistiche</b> Ci dicono quali pagine vengono visitate.</span></label>
        <label><input type="checkbox" id="consenso-mkt"${c.marketing ? ' checked' : ''}> <span><b>Pubblicità</b> Misurano le inserzioni e ti mostrano le nostre su Meta.</span></label>
      </div>
      <div class="consenso-bottoni">
        <button type="button" data-azione="rifiuta">Rifiuta</button>
        <button type="button" data-azione="personalizza">Personalizza</button>
        <button type="button" data-azione="accetta">Accetta</button>
      </div>`;
    document.body.appendChild(banner);
    banner.addEventListener('click', e => {
      const azione = e.target.closest('[data-azione]')?.dataset.azione;
      if (e.target.closest('.consenso-x') || azione === 'rifiuta') return salva(false, false);
      if (azione === 'accetta') return salva(true, true);
      if (azione === 'salva') return salva(banner.querySelector('#consenso-stat').checked, banner.querySelector('#consenso-mkt').checked);
      if (azione === 'personalizza') {
        banner.querySelector('.consenso-scelte').hidden = false;
        const b = e.target.closest('[data-azione]');
        b.dataset.azione = 'salva';
        b.textContent = 'Salva le scelte';
      }
    });
    banner.querySelector('[data-azione="rifiuta"]').focus({preventScroll: true});
  };

  document.addEventListener('click', e => {
    if (e.target.closest('[data-preferenze-cookie]')) { e.preventDefault(); apri(); }
  });

  const scelta = leggi();
  if (scelta) applica(scelta); else apri();
})();
