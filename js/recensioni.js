// Recensioni Google della scheda "Topiko lab", lette dal vivo con l'API Places (New).
// Serve una chiave API limitata ai domini del sito (vedi config.js). Senza chiave restano le schede segnaposto.
(() => {
  const box = document.getElementById('recensioni-google');
  const cfg = window.TOPIKO || {};
  if (!box || !cfg.GOOGLE_API_KEY) return;

  const CAMPI = 'rating,userRatingCount,googleMapsUri,reviews';
  const url = cfg.GOOGLE_PLACE_ID
    ? `https://places.googleapis.com/v1/places/${cfg.GOOGLE_PLACE_ID}?languageCode=it`
    : 'https://places.googleapis.com/v1/places:searchText';
  const richiesta = cfg.GOOGLE_PLACE_ID
    ? {headers: {'X-Goog-Api-Key': cfg.GOOGLE_API_KEY, 'X-Goog-FieldMask': CAMPI}}
    : {method: 'POST', body: JSON.stringify({textQuery: cfg.GOOGLE_PLACE_QUERY, languageCode: 'it'}),
       headers: {'Content-Type': 'application/json', 'X-Goog-Api-Key': cfg.GOOGLE_API_KEY, 'X-Goog-FieldMask': CAMPI.split(',').map(c => 'places.' + c).join(',')}};

  const esc = t => String(t || '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
  const link = u => /^https:\/\//.test(u || '') ? esc(u) : '#';
  const stelle = n => '★'.repeat(Math.round(n || 0)) + '☆'.repeat(5 - Math.round(n || 0));

  const nascondi = () => { box.style.display = 'none'; };
  const bozza = /vercel\.app$/.test(location.hostname);
  const leggi = () => (bozza ? fetch('js/recensioni-bozza.json') : fetch(url, richiesta)).then(r => r.json()).then(d => {
    const p = cfg.GOOGLE_PLACE_ID ? d : (d.places || [])[0];
    if (!p || d.error) return nascondi();
    const voto = document.querySelector('.google-voto');
    if (voto) {
      voto.href = /^https:\/\//.test(p.googleMapsUri || '') ? p.googleMapsUri : voto.href;
      voto.querySelector('span:last-child').textContent =
        `${(p.rating || 0).toLocaleString('it-IT', {minimumFractionDigits: 1})} · ${p.userRatingCount} recensioni su Google`;
    }
    const conTesto = (p.reviews || []).filter(r => (r.text || r.originalText || {}).text);
    if (!conTesto.length) return nascondi();
    // la fascia scorre all'infinito: le schede si ripetono finché riempiono due giri
    let giro = conTesto; while (giro.length < 8) giro = giro.concat(conTesto);
    const card = r => {
      const a = r.authorAttribution || {}, testo = (r.text || r.originalText).text;
      return `<a class="rec-card" href="${link(a.uri)}" target="_blank" rel="noopener">
        <div class="testa"><i style="background-image:url('${link(a.photoUri)}')"></i>
          <div><b>${esc(a.displayName)}</b><span class="stelle">${stelle(r.rating)}</span></div><span class="g">G</span></div>
        <p>${esc(testo)}</p><small>${esc(r.relativePublishTimeDescription)}</small></a>`;
    };
    box.querySelector('.rec-track').innerHTML = giro.concat(giro).map(card).join('');
  }).catch(nascondi);
  const vista = new IntersectionObserver(es => {
    if (es.some(e => e.isIntersecting)) { vista.disconnect(); leggi(); }
  }, {rootMargin: '600px'});
  vista.observe(box);
})();
