// Analisi gratuita: manda il modulo al motore (valuta-worker) e mostra il voto sulla pagina.
// L'analisi a passi dura circa 13 secondi; alla fine la pagina conferma che il voto arriva per mail entro 24 ore.
(() => {
  const box = document.querySelector('#valuta .vbox');
  const form = box && box.querySelector('form');
  if (!form) return;
  const stile = document.createElement('link');
  stile.rel = 'stylesheet'; stile.href = 'css/valuta.css?v=' + Date.now().toString().slice(0, 8);
  document.head.appendChild(stile);
  const MOTORE = /localhost|127\.0\.0\.1/.test(location.hostname) ? 'http://127.0.0.1:8788' : (window.TOPIKO_VALUTA || '');

  const [azienda, profilo, email] = form.querySelectorAll('input[type=text], input[type=email]');
  const [privacy, marketing] = form.querySelectorAll('input[type=checkbox]');
  const esc = t => String(t).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
  const fotoSicura = u => /^https:\/\//.test(u || '') ? encodeURI(u).replace(/'/g, '%27') : '';
  // campo nascosto: lo compilano solo i bot
  const trappola = document.createElement('input');
  Object.assign(trappola, {type: 'text', name: 'sito_web', tabIndex: -1, autocomplete: 'off'});
  trappola.setAttribute('aria-hidden', 'true');
  trappola.style.cssText = 'position:absolute;left:-9999px';
  form.appendChild(trappola);
  const pausa = ms => new Promise(r => setTimeout(r, ms));
  const errore = document.createElement('p');
  errore.className = 'valuta-errore';
  form.appendChild(errore);
  const moduloOriginale = [...form.childNodes];

  // [frase grande mentre lavora, voce corta nella lista]
  const PASSI = n => [
    [`Stiamo aprendo il profilo @${n}`, 'Profilo'],
    ['Stiamo analizzando la bio', 'Bio'],
    ['Stiamo controllando nome e link', 'Nome e link'],
    ["Stiamo contando i post dell'ultimo mese", 'Frequenza'],
    ['Stiamo guardando ogni quanto pubblichi', 'Costanza'],
    ['Stiamo analizzando i tuoi reel', 'Reel'],
    ['Stiamo misurando le interazioni', 'Interazioni'],
    ['Il tempo di un caffè: stiamo calcolando il voto', 'Voto']
  ];

  function attesa(n) {
    form.innerHTML = `<div class="analisi">
      <div class="avatar"><span>${esc(n.slice(0, 1).toUpperCase())}</span></div>
      <p class="frase-analisi" aria-live="polite"></p>
      <ul class="passi-analisi">${PASSI(esc(n)).map(p => `<li>${p[1]}</li>`).join('')}</ul>
      <div class="barra-analisi"><i></i></div>
    </div>`;
  }

  form.addEventListener('submit', async e => {
    e.preventDefault();
    errore.textContent = '';
    if (!privacy.checked) { errore.textContent = "Per ricevere l'analisi serve accettare l'informativa privacy."; return; }
    const prova = !MOTORE && !/(^|\.)topikolab\.it$/.test(location.hostname); // bozza: mostra il percorso senza inviare nulla
    if (!MOTORE && !prova) { errore.textContent = "L'analisi non è ancora attiva su questa pagina."; return; }

    const n = String(profilo.value || '').trim().replace(/^https?:\/\/(www\.)?instagram\.com\//i, '').replace(/^@/, '').split(/[/?#\s]/)[0] || 'profilo';
    const dati = {azienda: azienda.value, profilo: profilo.value, email: email.value, privacy: privacy.checked, marketing: marketing.checked, sito_web: trappola.value};
    attesa(n);

    // la richiesta parte subito, mentre scorrono i passi
    const risposta = prova ? Promise.resolve({ok: true, profilo: n, foto: ''}) : fetch(MOTORE, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(dati)})
      .then(async r => { const d = await r.json(); if (!r.ok) throw new Error(d.errore || 'Qualcosa non ha funzionato, riprova tra poco.'); return d; });
    let d = null, err = null;
    risposta.then(x => {
      d = x;
      const av = form.querySelector('.avatar');
      if (av && fotoSicura(x.foto)) av.style.backgroundImage = `url('${fotoSicura(x.foto)}')`, av.classList.add('con-foto');
    }, x => { err = x; });

    const voci = form.querySelectorAll('.passi-analisi li'), barra = form.querySelector('.barra-analisi i');
    const frase = form.querySelector('.frase-analisi'), passi = PASSI(n);
    for (let i = 0; i < voci.length; i++) {
      voci[i].classList.add('ora');
      frase.classList.remove('frase-in'); void frase.offsetWidth;
      frase.textContent = passi[i][0];
      frase.classList.add('frase-in');
      barra.style.width = ((i + 1) / voci.length * 100) + '%';
      await pausa(1450 + Math.random() * 500);
      if (err && i >= 1) break;
      voci[i].classList.remove('ora');
      voci[i].classList.add('fatto');
    }
    try { d = d || await risposta; } catch (x) { err = x; }

    if (err || !d) {
      form.replaceChildren(...moduloOriginale);
      errore.textContent = (err && err.message) || 'Qualcosa non ha funzionato, riprova tra poco.';
      return;
    }
    // il voto non si mostra: arriva per mail entro 24 ore
    form.innerHTML = `<div class="esito conferma">
      ${fotoSicura(d.foto) ? `<i class="foto-conferma" style="background-image:url('${esc(fotoSicura(d.foto))}')"></i>` : ''}
      <h3>Il report di @${esc(d.profilo)} è in cottura</h3>
      <p>Entro 24 ore te lo gusti nella tua mail: <b>${esc(dati.email)}</b>. Dentro trovi il voto e le prime cose da sistemare.</p>
      <p class="nota-conferma">Se non la trovi, guarda anche nella posta indesiderata.</p>
      <a class="btn btn-g" href="casi-studio.html">Intanto guarda i casi studio</a>
    </div>`;
  });
})();
