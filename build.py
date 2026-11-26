"""Genera il sito Topiko multipagina.

Prende stile, sezioni e script dalla bozza a pagina unica (archivio-pagina-unica.html)
e scrive: css/topiko.css, js/*.js e una pagina .html per sezione del sito.
Uso: python3 build.py
"""
import re
from pathlib import Path

QUI = Path(__file__).parent
SRC = (QUI / "archivio-pagina-unica.html").read_text(encoding="utf-8")
righe = SRC.split("\n")


# ---------- tono delle sezioni: ogni variabile ha il valore scuro e quello chiaro ----------
# (nome, scuro, chiaro). Le sezioni scure usano i valori di :root, quelle con classe .chiara i valori chiari.
TEMA = [
    ("notte", "#0D0A12", "#F4EFF8"), ("notte-2", "#16121D", "#FFFFFF"), ("notte-3", "#211B2A", "#EDE7F4"),
    ("testo", "#F4F1F8", "#1B1424"), ("testo-2", "#B9B2C4", "#453D52"), ("testo-3", "#8F889B", "#5E566B"),
    ("testo-art", "#DDD7E6", "#2B2336"),
    ("linea", "rgba(255,255,255,.09)", "rgba(27,20,36,.13)"), ("giallo", "#FEC42D", "#9A5B00"),
    ("veli", "rgba(255,255,255,.06)", "rgba(27,20,36,.05)"), ("veli-h", "rgba(255,255,255,.12)", "rgba(27,20,36,.10)"),
    ("bordo", "rgba(255,255,255,.22)", "rgba(27,20,36,.28)"),
    ("campo", "rgba(13,10,18,.35)", "#FFFFFF"), ("campo-b", "rgba(255,255,255,.25)", "rgba(27,20,36,.40)"),
    ("scheda", "#08060C", "#FFFFFF"), ("scheda-2", "#17121F", "#FFFFFF"), ("scheda-2h", "#2A2235", "#EDE7F4"),
    ("vetro", "rgba(20,15,28,.94)", "rgba(255,255,255,1)"), ("vetro-s", "rgba(255,255,255,.035)", "rgba(255,255,255,1)"),
    ("incavo", "rgba(0,0,0,.36)", "rgba(27,20,36,.05)"),
    ("sh0", "rgba(0,0,0,0)", "rgba(27,20,36,.06)"), ("sh1", "rgba(0,0,0,.55)", "rgba(60,20,90,.28)"),
    ("errore", "#FF9B7A", "#9A3412"),
    ("glow-1", "rgba(155,3,255,.5)", "rgba(155,3,255,.16)"), ("glow-2", "rgba(255,0,130,.34)", "rgba(255,0,130,.10)"),
    ("glow-3", "rgba(255,122,47,.28)", "rgba(255,122,47,.12)"), ("glow-b", "rgba(255,255,255,.4)", "rgba(155,3,255,.38)"),
    ("glow-s", "rgba(255,0,130,.75)", "rgba(155,3,255,.38)"),
    ("open-1", "rgba(155,3,255,.26)", "rgba(155,3,255,.09)"), ("open-2", "rgba(255,0,130,.14)", "rgba(255,0,130,.05)"),
    ("g1", "#9B03FF", "#8A00E0"), ("g2", "#FF0082", "#D4006F"), ("g3", "#FF7A2F", "#CC400C"),
    ("gt1", "#FF9E03", "#8A00E0"), ("gt2", "#E10AE9", "#D4006F"), ("gt3", "#FFE3F6", "#CC400C"),
]
GRADS = ("--grad:linear-gradient(100deg,var(--g1) 0%,var(--g2) 50%,var(--g3) 100%);"
         "--grad-tit:linear-gradient(90deg,var(--gt1) 0%,var(--gt2) 44%,var(--gt3) 100%);")


def _tema_css():
    scuro = "".join(f"--{n}:{d};" for n, d, c in TEMA)
    chiaro = "".join(f"--{n}:{c};" for n, d, c in TEMA)
    return (f":root{{--chiaro:#F4EFF8;--grad-sc:linear-gradient(100deg,#8A00E0 0%,#D4006F 52%,#CC400C 100%);{scuro}{GRADS}}}\n"
            # sezione chiara: colore fisso a tutta larghezza, senza pannello; dentro valgono le variabili chiare
            + f"section.chiara{{{chiaro}{GRADS}background:var(--chiaro);color:var(--testo)}}\n"
            # blocchi che restano scuri anche dentro una sezione chiara (barra, riquadro col gradiente, foto dei lavori, banner)
            + f".nav,.vbox,.consenso,.lavoro:not(.pieno){{{scuro}{GRADS}}}\n")


def tra(inizio, fine, da=0):
    """Testo fra la prima riga che inizia con `inizio` (da `da`) e la prima che inizia con `fine`, inclusi."""
    a = next(i for i in range(da, len(righe)) if righe[i].lstrip().startswith(inizio))
    b = next(i for i in range(a, len(righe)) if righe[i].lstrip().startswith(fine))
    return "\n".join(righe[a:b + 1]), b


# ---------- stile ----------
css = SRC[SRC.index("<style>") + 7:SRC.index("</style>")].replace('"Kumbh Sans"', '"Aileron"')
css = re.sub(r"^[ ]*(?:/\* manifesto \*/|\.manifesto[^\n]*)\n", "", css, flags=re.M)  # il manifesto non c'è più: la sua frase è il titolo dell'arco
css += r"""
/* prestazioni 4: la barra in alto resta vetro sfocato con il filo di luce, senza lente (si ridisegnerebbe a ogni fotogramma) */
.nav{backdrop-filter:blur(16px) saturate(175%) brightness(1.06)!important;-webkit-backdrop-filter:blur(16px) saturate(175%) brightness(1.06)!important}
.track.fermo,.rec-track.fermo{animation-play-state:paused!important}
"""
css += r"""
/* prestazioni 3: le macchie di colore stanno ferme, perché tutto ciò che si muove dietro il vetro lo fa ricalcolare a ogni fotogramma */
.blob,.proposta::before,.proposta::after,.rec::before{animation:none!important}
"""
css += r"""
/* prestazioni 2: grana fissa via; mentre si scorre il vetro perde la lente e resta solo sfocato */
body::after{display:none!important}
html.scorre :is(.nav,.tile:not(.t1),.card .in,form,.persona){backdrop-filter:blur(10px) saturate(160%)!important;-webkit-backdrop-filter:blur(10px) saturate(160%)!important}
.rec-scorre{-webkit-mask:none!important;mask:none!important;position:relative}
.rec-scorre::before,.rec-scorre::after{content:"";position:absolute;top:0;bottom:0;width:120px;z-index:2;pointer-events:none}
.rec-scorre::before{left:0;background:linear-gradient(90deg,var(--notte),transparent)}
.rec-scorre::after{right:0;background:linear-gradient(-90deg,var(--notte),transparent)}
.rec-track,.track{will-change:transform}
"""
css += r"""
/* ===== multipagina ===== */
.nav ul a.on{color:#fff}
.nav ul a.on::after{content:"";display:block;height:2px;margin-top:4px;border-radius:2px;background:var(--grad)}
.ph-hero{position:relative;overflow:hidden;padding:190px 0 90px}
.ph-hero .blob{opacity:.45}
.ph-hero .wrap{position:relative;z-index:1}
.ph-hero h1{font-size:clamp(48px,7.5vw,112px);font-weight:900;line-height:.92;letter-spacing:-.045em;margin:22px 0 26px;text-wrap:balance}
.ph-hero h1 .riga{display:block;overflow:hidden;padding-bottom:.06em}
.ph-hero h1 .riga span{display:inline-block}
.ph-hero .lead{font-size:clamp(18px,1.6vw,22px);color:var(--testo-2);max-width:640px}
.sezione{padding:110px 0}
.link-tutti{display:inline-flex;align-items:center;gap:10px;margin-top:40px;font-weight:700;color:#fff}
.link-tutti svg{width:18px;height:18px;transition:transform .3s var(--ease)}
.link-tutti:hover svg{transform:translateX(4px)}
.card a.leggi{margin-top:18px;font-weight:700;font-size:15px;color:#fff;display:inline-flex;gap:8px;align-items:center}
.card a.leggi::after{content:"→"}

/* home corta */
.mini-g{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:56px}
.mini{position:relative;display:block;border-radius:var(--r);overflow:hidden;aspect-ratio:4/5;background:var(--notte-2)}
.mini .ph{position:absolute;inset:0;background-size:cover;background-position:center;transition:transform 1s var(--ease)}
.mini:hover .ph{transform:scale(1.05)}
.mini::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(13,10,18,.92) 15%,rgba(13,10,18,.1) 60%)}
.mini .t{position:absolute;left:24px;right:24px;bottom:24px;z-index:1}
.mini .chip{margin:0 0 16px}
.mini strong{display:block;font-size:clamp(40px,4vw,60px);font-weight:900;letter-spacing:-.045em;line-height:1}
.mini small{color:var(--testo-2);font-size:15px}
.elenco{list-style:none;margin-top:50px;border-top:1px solid var(--linea)}
.elenco a{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:24px 0;border-bottom:1px solid var(--linea);font-size:clamp(24px,3vw,42px);font-weight:700;letter-spacing:-.03em;transition:padding .4s var(--ease),color .3s}
.elenco a svg{width:28px;height:28px;flex-shrink:0;opacity:.4;transition:opacity .3s,transform .4s var(--ease)}
.elenco a:hover{padding-left:16px}
.elenco a:hover span{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.elenco a:hover svg{opacity:1;transform:translateX(-6px)}
.squadra-foto{position:relative;display:block;border-radius:var(--r);overflow:hidden;height:min(70vh,640px)}
.squadra-foto .ph{position:absolute;inset:0;background-size:cover;background-position:center 35%;transition:transform 1.2s var(--ease)}
.squadra-foto:hover .ph{transform:scale(1.04)}
.squadra-foto::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(13,10,18,.85),transparent 55%)}
.squadra-foto .t{position:absolute;left:40px;bottom:36px;right:40px;z-index:1}
.squadra-foto h2{font-size:clamp(30px,3.6vw,52px);font-weight:800;letter-spacing:-.035em;line-height:1.05;margin-top:14px}
.suggerimento{color:var(--testo-3);margin-top:10px}
.nav ul{margin-left:auto;margin-right:22px}
.nav .social{display:flex;gap:4px;margin-right:10px}
.nav .social a{width:38px;height:38px;border-radius:50%;display:grid;place-items:center;color:var(--testo-2);transition:color .2s,background .2s}
.nav .social a:hover{color:#fff;background:rgba(255,255,255,.1)}
.nav .social svg{width:18px;height:18px}

.google-voto{display:inline-flex;align-items:center;gap:12px;margin-top:26px;padding:10px 18px;border-radius:100px;background:rgba(255,255,255,.05);border:1px solid var(--linea);font-weight:600;font-size:15px}
.g{display:grid;place-items:center;width:26px;height:26px;border-radius:50%;background:#fff;color:#4285F4;font-weight:800;font-size:15px}
.stelle{color:var(--giallo);letter-spacing:2px}
.rec-scorre{margin-top:50px;overflow:hidden;-webkit-mask:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.rec-track{display:flex;gap:18px;width:max-content;animation:mq 60s linear infinite}
.rec-scorre:hover .rec-track{animation-play-state:paused}
.rec-card{width:340px;flex-shrink:0;border-radius:var(--r);padding:26px;background:var(--notte-2);border:1px solid var(--linea)}
.rec-card .testa{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.rec-card .testa i{width:40px;height:40px;border-radius:50%;background:var(--grad)}
.rec-card .testa b{display:block;font-size:15px}
.rec-card .testa .g{margin-left:auto;width:22px;height:22px;font-size:13px}
.rec-card p{color:var(--testo-2);font-size:15px;line-height:1.55}
.rec-card.vuota .testa b,.rec-card.vuota p{height:11px;border-radius:6px;background:rgba(255,255,255,.08);margin-bottom:10px}
.rec-card.vuota .testa b{width:110px;margin-bottom:6px}
.rec-card.vuota p.corta{width:60%}
.rec-card{display:block;transition:border-color .3s}
a.rec-card:hover{border-color:rgba(255,255,255,.25)}
.rec-card .testa i{background-size:cover;background-position:center}
.rec-card p{display:-webkit-box;-webkit-line-clamp:5;-webkit-box-orient:vertical;overflow:hidden}
.rec-card small{display:block;margin-top:12px;color:var(--testo-3);font-size:13px}
.rec-google{display:grid;grid-template-columns:1fr 1.2fr;gap:20px;margin-top:50px}
.rec-google .widget{border-radius:var(--r);padding:40px;border:1px dashed rgba(255,255,255,.22);display:flex;flex-direction:column;justify-content:center}
.rec-google .widget p{color:var(--testo-2);margin-top:10px}
.rec-google .mappa{border-radius:var(--r);overflow:hidden;min-height:380px;background:var(--notte-2)}
.rec-google iframe{width:100%;height:100%;min-height:380px;border:0;filter:grayscale(.2) contrast(1.05)}
/* blog */
.filtri{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:40px}
.filtri span{padding:10px 18px;border-radius:100px;border:1px solid var(--linea);font-weight:600;font-size:14px;color:var(--testo-2)}
.filtri span.on{background:var(--grad);color:#fff;border-color:transparent}
.blog-g{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;padding-bottom:120px}
.post{display:block;border-radius:var(--r);overflow:hidden;background:var(--notte-2);border:1px solid var(--linea);transition:transform .4s var(--ease)}
.post:hover{transform:translateY(-4px)}
.post .ph{aspect-ratio:16/10;background:var(--grad);display:grid;place-items:center;font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.85)}
.post .t{padding:24px 26px 28px}
.post small{color:var(--testo-3);font-size:13px}
.post h3{font-size:22px;font-weight:700;letter-spacing:-.02em;line-height:1.2;margin:10px 0 8px}
.post p{color:var(--testo-2);font-size:15px}
.post.primo{grid-column:span 3;display:grid;grid-template-columns:1.3fr 1fr}
.post.primo .ph{aspect-ratio:auto;min-height:340px}
.post.primo .t{padding:44px;align-self:center}
.post.primo h3{font-size:clamp(28px,3vw,42px)}
.articolo{max-width:760px;margin:0 auto;padding-bottom:110px}
.articolo .ph{aspect-ratio:16/9;border-radius:var(--r);background:var(--grad);margin-bottom:56px;display:grid;place-items:center;font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:13px}
.articolo h2{font-size:clamp(26px,2.6vw,34px);font-weight:800;letter-spacing:-.02em;margin:46px 0 14px}
.articolo p{font-size:19px;line-height:1.7;color:#DDD7E6;margin-bottom:18px}
.articolo blockquote{margin:36px 0;padding:6px 0 6px 26px;border-left:3px solid var(--fucsia);font-size:24px;font-weight:600;line-height:1.4}
.articolo .autore{display:flex;align-items:center;gap:14px;margin-top:50px;padding-top:30px;border-top:1px solid var(--linea)}
.articolo .autore i{width:52px;height:52px;border-radius:50%;background-size:cover;background-position:center 20%}
.foot nav{flex-wrap:wrap;row-gap:10px}
html,body{overflow-x:clip!important}
.mega{display:inline-block;font-size:clamp(56px,13.5vw,210px);line-height:1;padding:.04em .06em .14em 0;max-width:100%}
.squadra-foto{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);height:auto;background:var(--notte-2);border:1px solid var(--linea)}
.squadra-foto .ph{position:relative;inset:auto;aspect-ratio:1400/1680}
.squadra-foto::after{display:none}
.squadra-foto .t{position:relative;left:auto;right:auto;bottom:auto;align-self:end;padding:48px}

/* elenco casi studio */
.casi-lista{display:grid;gap:28px;padding-bottom:120px}
.casi-lista .card{width:100%;height:560px}
.casi-lista .card.solo{height:auto;min-height:380px}
.casi-lista .card.solo .in{position:relative;inset:auto;margin:28px}

/* caso singolo */
.cs-cover{position:relative;height:min(68vh,640px);border-radius:var(--r);overflow:hidden;margin-top:10px}
.cs-cover .ph{position:absolute;inset:0;background-size:cover;background-position:center}
.cs-cover::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(13,10,18,.75),transparent 55%)}
.cs-meta{position:absolute;left:32px;bottom:28px;z-index:2;display:flex;gap:10px;flex-wrap:wrap}
.cs-blocchi{display:grid;grid-template-columns:280px 1fr;gap:28px 70px;padding:110px 0 40px}
.cs-blocchi h2{font-size:15px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--testo-3);padding-top:8px}
.cs-blocchi p,.cs-blocchi li{font-size:clamp(20px,1.9vw,26px);line-height:1.45;color:var(--testo);max-width:760px}
.cs-blocchi ul{list-style:none;display:grid;gap:14px}
.cs-blocchi li{padding-left:28px;position:relative}
.cs-blocchi li::before{content:"";position:absolute;left:0;top:.62em;width:12px;height:2px;background:var(--grad)}
.cs-num{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;padding:40px 0 110px}
.cs-num div{border-radius:var(--r);padding:34px;background:var(--notte-2);border:1px solid var(--linea)}
.cs-num strong{display:block;font-size:clamp(48px,5vw,76px);font-weight:900;letter-spacing:-.045em;line-height:1;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.cs-num small{display:block;margin-top:10px;color:var(--testo-2);font-size:16px}
.cs-nota{color:var(--testo-3);font-size:14px;margin-top:-80px;padding-bottom:90px}
.prossimo{display:flex;justify-content:space-between;align-items:center;gap:30px;padding:60px 0 120px;border-top:1px solid var(--linea)}
.prossimo small{color:var(--testo-3);font-size:14px;letter-spacing:.14em;text-transform:uppercase}
.prossimo a{font-size:clamp(30px,4vw,58px);font-weight:800;letter-spacing:-.035em}
.prossimo a:hover{color:transparent;background:var(--grad);-webkit-background-clip:text;background-clip:text}

/* squadra */
.team{display:grid;grid-template-columns:repeat(5,1fr);gap:18px;margin-top:40px}
.persona{border-radius:var(--r);overflow:hidden;background:var(--notte-2);border:1px solid var(--linea)}
.persona .foto{aspect-ratio:4/5;background-size:cover;background-position:center;background-color:var(--notte-3)}
.persona .foto.vuota{display:grid;place-items:center;background:var(--grad);font-size:72px;font-weight:900;color:rgba(255,255,255,.9)}
.persona div.t{padding:24px 26px 28px}
.persona h3{font-size:24px;font-weight:800;letter-spacing:-.02em}
.persona p{color:var(--testo-2);margin-top:6px}

/* passi statici (servizi, analisi) */
.passi-g{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:56px}
.passi-g div{border-radius:var(--r);padding:30px;background:var(--notte-2);border:1px solid var(--linea)}
.passi-g b{display:block;font-size:56px;font-weight:900;line-height:1;letter-spacing:-.04em;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;margin-bottom:18px}
.passi-g h3{font-size:21px;font-weight:700;margin-bottom:8px}
.passi-g p{color:var(--testo-2)}

/* contatti */
.contatti-g{display:grid;grid-template-columns:1.2fr .8fr;gap:50px;padding-bottom:130px;align-items:start}
.contatti-g form{background:rgba(255,255,255,.035)}
.contatti-g textarea{width:100%;margin-top:6px;font:inherit;font-size:16px;color:#fff;padding:15px 18px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);border-radius:14px;min-height:150px;resize:vertical}
.recapiti{display:grid;gap:18px}
.recapiti div{border-radius:var(--r);padding:28px;background:var(--notte-2);border:1px solid var(--linea)}
.recapiti small{display:block;color:var(--testo-3);font-size:13px;letter-spacing:.14em;text-transform:uppercase;margin-bottom:8px}
.recapiti b{font-size:20px}
.segnaposto{color:var(--giallo)}
.grazie{display:none;padding:24px;border-radius:14px;background:rgba(255,255,255,.06);font-weight:600}

/* fascia finale verso i contatti */
.cta-fine{padding:20px 0 140px}
.cta-fine .vbox{grid-template-columns:1fr auto}
.cta-fine h2{margin:0}

@media (max-width:960px){
  .ph-hero{padding:150px 0 60px}
  .cs-blocchi{grid-template-columns:1fr;gap:12px 0;padding-top:70px}
  .cs-blocchi h2{padding-top:30px}
  .passi-g,.contatti-g,.mini-g{grid-template-columns:1fr}
  .team{grid-template-columns:1fr 1fr}
  .squadra-foto{grid-template-columns:1fr}
  .rec-google,.blog-g{grid-template-columns:1fr}
  .post.primo{grid-column:auto;grid-template-columns:1fr}
  .nav .social{margin-left:auto}
  .nav .social a{width:32px;height:32px}
  .orbita{max-width:300px}
  .giro span{font-size:12px;padding:8px 12px}
  .squadra-foto .t{padding:28px 22px}
  .squadra-foto .t{left:22px;right:22px}
  .casi-lista .card{height:auto;min-height:560px}
  .cta-fine .vbox{grid-template-columns:1fr}
  .prossimo{flex-direction:column;align-items:flex-start}
}

/* correzioni di visualizzazione */
/* il bagliore dell'apertura sfuma nello sfondo invece di finire con un taglio dritto */
.ph-hero::after{content:"";position:absolute;left:0;right:0;bottom:0;height:160px;background:linear-gradient(180deg,rgba(13,10,18,0),var(--notte));pointer-events:none}
/* spazio per l'icona in alto a sinistra: il titolo non ci finisce sotto */
.tile{padding-top:104px}
/* le etichette che girano non escono dalla colonna */
@media (max-width:1400px){.orbita{max-width:min(560px,calc(100% - 190px))}}
/* il suggerimento del mouse non serve dove il mouse non c'è */
@media (hover:none){.suggerimento{display:none}}
/* menù a scomparsa sotto i 960px */
.nav .menu{display:none}
@media (max-width:960px){
  .wrap.h-copy{padding:70px 20px clamp(48px,9vh,90px)}
  .prog{bottom:22px}
  .orbita{max-width:min(300px,calc(100% - 130px))}
  .post.primo .t{padding:24px 26px 28px}
  .post.primo .ph{min-height:0;aspect-ratio:16/10}
  .nav .menu{display:flex;flex-direction:column;justify-content:center;align-items:center;gap:5px;width:40px;height:40px;flex-shrink:0;margin-left:8px;padding:0;border-radius:50%;border:1px solid var(--linea);background:rgba(255,255,255,.06);cursor:pointer}
  .nav .menu span{display:block;width:16px;height:2px;border-radius:2px;background:#fff;transition:transform .3s var(--ease)}
  .nav.aperto .menu span:first-child{transform:translateY(3.5px) rotate(45deg)}
  .nav.aperto .menu span:last-child{transform:translateY(-3.5px) rotate(-45deg)}
  .nav.aperto ul{display:flex;flex-direction:column;gap:0;position:absolute;top:calc(100% + 10px);left:0;right:0;margin:0;padding:10px;border-radius:24px;background:#120e18;border:1px solid var(--linea);box-shadow:0 20px 50px rgba(0,0,0,.45)}
  .nav.aperto ul a{display:block;padding:14px 16px;font-size:18px;font-weight:600;color:#fff;border-radius:14px}
  .nav.aperto ul a:hover{background:rgba(255,255,255,.06)}
  .nav.aperto ul a.on::after{width:28px}
}
@media (max-width:380px){
  .nav{padding-left:14px}
  .nav .social{display:none}
  .nav .btn{margin-left:auto}
}
"""
css += r"""
/* prestazioni: niente filtro di sfocatura sulle macchie, stessa resa con sfumature radiali */
.blob{filter:none!important;opacity:.85}
.b1{background:radial-gradient(circle,var(--viola) 0%,rgba(155,3,255,.35) 40%,transparent 70%)!important}
.b2{background:radial-gradient(circle,var(--fucsia) 0%,rgba(255,0,130,.35) 40%,transparent 70%)!important}
.b3{background:radial-gradient(circle,var(--arancio) 0%,rgba(255,122,47,.3) 40%,transparent 70%)!important}
.proposta::before,.proposta::after,.rec::before{filter:none!important}
.proposta::before{background:radial-gradient(circle,rgba(155,3,255,.9),transparent 68%)!important}
.proposta::after{background:radial-gradient(circle,rgba(255,122,47,.8),transparent 68%)!important}
.rec::before{background:radial-gradient(ellipse,rgba(255,0,130,.8),transparent 68%)!important}
@media (max-width:960px){.blob,.proposta::before,.proposta::after,.rec::before,.r2{animation:none!important}}
"""
(QUI / "css").mkdir(exist_ok=True)
FONT = """@font-face{font-family:'Aileron';font-style:normal;font-weight:300;font-display:swap;ascent-override:92%;descent-override:24%;line-gap-override:0%;src:url(../fonts/aileron-latin-300-normal.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Aileron';font-style:normal;font-weight:400;font-display:swap;ascent-override:92%;descent-override:24%;line-gap-override:0%;src:url(../fonts/aileron-latin-400-normal.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Aileron';font-style:italic;font-weight:400;font-display:swap;ascent-override:92%;descent-override:24%;line-gap-override:0%;src:url(../fonts/aileron-latin-400-italic.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Aileron';font-style:normal;font-weight:600;font-display:swap;ascent-override:92%;descent-override:24%;line-gap-override:0%;src:url(../fonts/aileron-latin-600-normal.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Aileron';font-style:normal;font-weight:700;font-display:swap;ascent-override:92%;descent-override:24%;line-gap-override:0%;src:url(../fonts/aileron-latin-700-normal.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Aileron';font-style:italic;font-weight:700;font-display:swap;ascent-override:92%;descent-override:24%;line-gap-override:0%;src:url(../fonts/aileron-latin-700-italic.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Aileron';font-style:normal;font-weight:800;font-display:swap;ascent-override:92%;descent-override:24%;line-gap-override:0%;src:url(../fonts/aileron-latin-800-normal.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Bitcount Single';font-style:normal;font-weight:100 900;font-display:swap;ascent-override:88.5%;descent-override:23.1%;line-gap-override:0%;src:url(../fonts/bitcount-single-latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Bitcount Single';font-style:normal;font-weight:100 900;font-display:swap;ascent-override:88.5%;descent-override:23.1%;line-gap-override:0%;src:url(../fonts/bitcount-single-latin-ext.woff2) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
.track.loghi{gap:90px;align-items:center}
.track.loghi img{display:block;width:auto;opacity:.72;transition:opacity .3s;flex:none}
.track.loghi img:hover{opacity:1}
"""
EXTRA = """
.h-copy h1 .riga,.ph-hero h1 .riga{padding:.02em .1em .34em;margin:0 -.1em -.28em}
.h-copy h1 .riga span,.ph-hero h1 .riga span{padding-bottom:.34em;margin-bottom:-.34em}
.h-copy h1 .grad-t,.ph-hero h1 .grad-t,.h-copy h1 em,.ph-hero h1 em{padding:0 .1em .34em;margin:0 -.1em -.34em;display:inline-block}
.consenso{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);width:min(620px,calc(100vw - 32px));max-height:calc(100vh - 40px);overflow:auto;z-index:9999;padding:26px;border-radius:20px;background:rgba(14,9,22,.97);border:1px solid rgba(255,255,255,.18);box-shadow:0 24px 70px rgba(0,0,0,.6);color:#fff}
.consenso h2{font-size:20px;font-weight:800;letter-spacing:-.01em;margin:0 30px 10px 0}
.consenso p{font-size:15px;line-height:1.55;color:#DDD7E6;margin:0}
.consenso a{color:#fff;text-decoration:underline}
.consenso-x{position:absolute;top:14px;right:14px;width:36px;height:36px;border:0;border-radius:50%;background:rgba(255,255,255,.08);color:#fff;font-size:22px;line-height:1;cursor:pointer}
.consenso-scelte{display:grid;gap:12px;margin-top:18px}
.consenso-scelte[hidden]{display:none}
.consenso-scelte label{display:flex;gap:12px;align-items:flex-start;font-size:14px;line-height:1.45;color:#DDD7E6;cursor:pointer}
.consenso-scelte input{width:18px;height:18px;margin-top:1px;flex:none;accent-color:#FF0082}
.consenso-scelte b{display:block;color:#fff}
.consenso-bottoni{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:20px}
.consenso-bottoni button{padding:13px 10px;border-radius:40px;border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.08);color:#fff;font:600 14px/1.2 inherit;font-family:inherit;cursor:pointer}
.consenso-bottoni button:hover,.consenso-x:hover{background:rgba(255,255,255,.18)}
.consenso-bottoni button:focus-visible,.consenso-x:focus-visible{outline:2px solid #fff;outline-offset:2px}
/* scheda dei lavori: la foto è il riquadro, numero enorme, nessun pannello */
.scena{height:220vh}
.casi-sez{padding-bottom:0}
.lavoro{position:relative;display:block;flex:none;width:min(82vw,1120px);height:min(calc(100vh - 150px),680px);overflow:hidden;background:#000;color:#fff}
.lavoro .ph{position:absolute;inset:0;background-size:cover;background-position:center;transition:transform 1s var(--ease)}
.lavoro:hover .ph{transform:scale(1.03)}
.lavoro::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.86),rgba(0,0,0,0) 66%)}
.l-t{position:absolute;z-index:1;left:32px;right:32px;bottom:30px;display:grid;grid-template-columns:1.15fr 1fr;gap:36px;align-items:end}
.l-num strong{display:block;font-size:clamp(84px,11.5vw,190px);font-weight:900;line-height:.86;letter-spacing:-.05em;white-space:nowrap}
.l-num small{display:block;font-size:19px;font-weight:600;margin-top:12px;color:#fff}
.l-det span{font-size:15px;font-weight:600}
.l-det h3{font-size:clamp(24px,2.5vw,38px);font-weight:800;line-height:1.05;letter-spacing:-.03em;margin:8px 0 12px}
.l-det em{display:inline-flex;align-items:center;gap:10px;font-style:normal;font-weight:700;font-size:16px;border-bottom:2px solid currentColor;padding-bottom:3px}
.l-det em svg{width:16px;height:16px}
.l-num strong.parola{white-space:normal;font-size:clamp(56px,7.4vw,120px);line-height:.92}
.lavoro.pieno{background:var(--notte-2);color:#fff}.lavoro.pieno::after{display:none}
.l-num strong{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;padding:.04em .04em .1em 0}
.casi-pagina{display:grid;gap:20px;padding-bottom:40px}.casi-pagina .lavoro{width:100%}
@media (max-width:960px){.lavoro{width:100%;height:min(82vh,620px)}.l-t{left:18px;right:18px;bottom:20px;grid-template-columns:1fr;gap:16px}.l-num strong{font-size:clamp(68px,22vw,130px)}.l-num strong[data-pre]{font-size:clamp(52px,15vw,110px)}.scena{height:170vh}}
/* elenco casi: stessa altezza, stesso pannello, numeri sempre in basso */
.casi-lista .card,.casi-lista .card.solo{width:100%;height:560px}
.casi-lista .card .in,.casi-lista .card.solo .in{width:560px;max-width:calc(100% - 56px);height:auto;inset:28px auto 28px 28px;padding:38px;display:flex;flex-direction:column;gap:0}
.casi-lista .card.solo .in{top:28px;bottom:28px;left:28px;margin:0;height:calc(100% - 56px)}
.casi-lista .card .chip{align-self:flex-start}
.casi-lista .card .stato{margin-bottom:12px}
.casi-lista .card h3{font-size:clamp(26px,2.6vw,38px);margin:18px 0 12px}
.casi-lista .card p{font-size:16px;line-height:1.5}
.casi-lista .card .kpi{margin-top:auto;padding-top:18px;display:grid;grid-template-columns:1fr 1fr;gap:20px}
.casi-lista .card .kpi strong{font-size:clamp(30px,3.4vw,46px);line-height:1}
.casi-lista .card .leggi{margin-top:14px}
.squadra-foto.sola{display:block;height:auto;background:none;border:0}
.squadra-foto.sola .ph{position:relative;inset:auto;aspect-ratio:16/9;background-position:center 30%}
/* casi in home: un caso grande e due accanto; bottone ben visibile */
.casi-testa{display:flex;justify-content:space-between;align-items:flex-end;gap:30px;flex-wrap:wrap}
.casi-tutti{font-size:18px;padding:20px 34px;flex:none}
.cs-testa{display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap}
.cs-testa .casi-tutti{font-size:16px;padding:15px 26px}
.casi-home{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:50px}
.casi-home .mini{aspect-ratio:5/4}
.casi-home .mini.grande{grid-column:1/-1;aspect-ratio:21/9}
/* scene 3D allo scorrimento */
.entra{position:relative;height:320vh;background:#0D0A12}
.entra-palco{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden}
.entra canvas{position:absolute;inset:0;width:100%;height:100%;display:block}
.entra-testo{position:absolute;left:0;right:0;bottom:0;padding:120px 32px 56px;opacity:0;background:linear-gradient(0deg,rgba(13,10,18,.94),rgba(13,10,18,0));will-change:opacity,transform}
.entra-testo h2{font-size:clamp(40px,6.4vw,96px);font-weight:900;line-height:.98;letter-spacing:-.04em;color:#fff;margin:0 0 26px}
.entra.ferma{height:auto}.entra.ferma .entra-palco{position:relative}.entra.ferma .entra-testo{opacity:1!important;transform:none!important}
@media (max-width:760px){.entra{height:280vh}.entra-testo{padding:100px 16px 40px}.entra-testo .btn{width:100%;justify-content:center}}
/* grafico: Topiko al centro, i servizi girano intorno e le etichette restano dritte */
.lead-u{font-size:20px;line-height:1.5;color:var(--testo-2);max-width:640px;margin-top:24px}
.universo{container-type:inline-size;position:relative;width:min(100%,880px);aspect-ratio:1;margin:30px auto 0;overflow:visible}
.universo::before,.universo::after{content:"";position:absolute;left:50%;top:50%;border-radius:50%;transform:translate(-50%,-50%);pointer-events:none}
.universo::before{width:56cqw;height:56cqw;border:1px solid rgba(255,255,255,.22)}
.universo::after{width:88cqw;height:88cqw;border:1px dashed rgba(255,255,255,.16)}
.u-anello{position:absolute;inset:0;animation:u-gira 90s linear infinite paused}
.universo.vivo .u-anello,.universo.vivo .u-et{animation-play-state:running}
.universo:hover .u-anello,.universo:hover .u-et{animation-play-state:paused}
.u-p{position:absolute;left:50%;top:50%;z-index:2;width:0;height:0;transform:rotate(var(--a)) translateY(calc(var(--r) * -1cqw)) rotate(calc(var(--a) * -1))}
.u-servizi .u-p{--r:28}
.u-et{position:absolute;left:0;top:0;translate:-50% -50%;display:block;white-space:nowrap;font-size:clamp(12px,1.65cqw,15px);font-weight:600;padding:.75em 1.15em;border-radius:100px;animation:u-gira 90s linear infinite reverse paused;transition:background .25s,box-shadow .25s}
.u-servizi .u-et{background:#17121f;border:1px solid rgba(255,255,255,.3);color:#fff}
a.u-p:hover .u-et,a.u-p:focus-visible .u-et{background:var(--grad);border-color:transparent;box-shadow:0 8px 30px -8px rgba(255,0,130,.8)}
.u-corto{display:none}
.u-centro{position:absolute;left:50%;top:50%;z-index:3;width:24cqw;height:24cqw;transform:translate(-50%,-50%);border-radius:50%;background:var(--grad);display:grid;place-items:center;box-shadow:0 0 90px -10px rgba(255,0,130,.65)}
.u-centro img{width:72%;height:auto}
@keyframes u-gira{to{rotate:360deg}}
.u-azione{display:flex;justify-content:center;margin-top:30px}
/* servizi: riquadri neri che si illuminano e si aprono sul posto */
.servizi-sez{padding:10px 0 90px}
.servizi-g{display:grid;grid-template-columns:repeat(6,1fr);gap:16px;grid-auto-flow:dense}
.servizio{grid-column:span 2;border-radius:var(--r);background:#08060c;border:1px solid var(--linea);transition:scale .3s var(--ease),border-color .3s,box-shadow .3s,background .3s;align-self:start;min-width:0}
.servizio:nth-child(n+4){grid-column:span 3}
.servizio:not([open]){align-self:stretch}
.servizio:not([open]) summary{height:100%}
.servizio summary{list-style:none;display:grid;grid-template-columns:1fr auto;gap:18px 14px;padding:28px;cursor:pointer;min-height:230px;align-content:space-between;border-radius:inherit}
.servizio summary::-webkit-details-marker{display:none}
.servizio summary:focus-visible{outline:2px solid #fff;outline-offset:3px}
.servizio .ico{width:48px;height:48px;border-radius:14px;display:grid;place-items:center;background:rgba(255,255,255,.06);border:1px solid var(--linea);color:#fff;transition:background .3s}
.servizio .ico svg{width:24px;height:24px}
.s-piu{position:relative;width:34px;height:34px;border-radius:50%;border:1px solid rgba(255,255,255,.3);transition:transform .3s var(--ease),background .3s}
.s-piu::before,.s-piu::after{content:"";position:absolute;left:50%;top:50%;width:13px;height:2px;margin:-1px -6.5px;background:#fff;border-radius:2px}
.s-piu::after{transform:rotate(90deg)}
.s-testa{grid-column:1/-1;grid-row:2;display:block}
.s-nome{display:block;font-size:clamp(22px,2.1vw,30px);font-weight:800;line-height:1.08;letter-spacing:-.025em}
.s-breve{display:block;margin-top:10px;color:var(--testo-2);font-size:16px;line-height:1.45}
@media (hover:hover){.servizio:not([open]):hover{scale:1.035!important;z-index:2;background:linear-gradient(145deg,rgba(155,3,255,.5),rgba(255,0,130,.34) 55%,rgba(255,122,47,.28));border-color:rgba(255,255,255,.4);box-shadow:0 26px 70px -22px rgba(255,0,130,.75)}
.servizio:not([open]):hover .s-breve{color:#fff}
.servizio:not([open]):hover .ico{background:rgba(255,255,255,.2)}}
.servizio[open]{grid-column:1/-1;background:linear-gradient(145deg,rgba(155,3,255,.26),rgba(255,0,130,.14) 55%,#08060c);border-color:rgba(255,255,255,.34);scroll-margin-top:96px}
.servizio[open] summary{min-height:0;grid-template-columns:auto 1fr auto;align-items:center;align-content:center}
.servizio[open] .s-testa{grid-column:2;grid-row:1}
.servizio[open] .s-piu{transform:rotate(45deg);background:rgba(255,255,255,.14)}
.s-dett{display:grid;grid-template-columns:1fr 1fr;gap:34px;padding:6px 28px 28px}
.s-dett.con-caso{grid-template-columns:1fr 1fr 300px}
.s-dett h4{font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--testo-3);margin-bottom:12px}
.s-dett ul{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.s-dett li{padding-left:20px;position:relative;line-height:1.45;font-size:17px;color:#EDE8F3}
.s-dett li::before{content:"";position:absolute;left:0;top:.55em;width:8px;height:8px;border-radius:50%;background:var(--grad)}
.s-dett p{line-height:1.55;font-size:17px;color:#EDE8F3}
.s-caso{padding:22px;border-radius:16px;background:rgba(0,0,0,.36);border:1px solid var(--linea);align-self:start}
.s-caso small{display:block;font-size:13px;color:var(--testo-3)}
.s-caso strong{display:block;font-size:clamp(30px,3vw,42px);font-weight:900;letter-spacing:-.03em;margin:8px 0 4px}
.s-caso span{font-size:15px;line-height:1.4;color:var(--testo-2)}
.s-chiudi{grid-column:1/-1;justify-self:end;position:sticky;bottom:14px;padding:12px 24px;border-radius:40px;border:1px solid rgba(255,255,255,.34);background:#17121f;color:#fff;font:600 15px/1 inherit;font-family:inherit;cursor:pointer}
.s-chiudi:hover{background:#2a2235}
.s-chiudi:focus-visible{outline:2px solid #fff;outline-offset:2px}
/* come lavoriamo: righe, un ritmo diverso dai riquadri */
.fasi{list-style:none;margin:44px 0 0;padding:0}
.fasi li{display:grid;grid-template-columns:90px minmax(0,1fr) minmax(0,1.3fr);gap:24px;align-items:baseline;padding:30px 0;border-top:1px solid var(--linea)}
.fasi li:last-child{border-bottom:1px solid var(--linea)}
.fasi span{font-size:44px;font-weight:900;line-height:1;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.fasi h3{font-size:clamp(24px,2.5vw,34px);font-weight:800;letter-spacing:-.025em;line-height:1.1}
.fasi p{font-size:18px;line-height:1.5;color:var(--testo-2)}
@media (hover:none){.suggerimento{display:none}}
/* telefono: l'universo diventa una colonna leggibile */
@media (max-width:760px){
  .casi-lista .card,.casi-lista .card.solo{height:auto;min-height:0}
  .casi-lista .card .in,.casi-lista .card.solo .in{position:relative;inset:auto;width:auto;max-width:none;height:auto;margin:12px;padding:24px}
  .casi-lista .card:not(.solo){padding-top:200px}
  .casi-lista .card .in,.casi-lista .card.solo .in{height:auto!important;min-height:0!important}
  .casi-lista .card .kpi{margin-top:20px}
  .squadra-foto.sola .ph{aspect-ratio:4/3}
  .casi-testa{align-items:stretch}
  .casi-tutti{width:100%;justify-content:center}
  .cs-testa .casi-tutti{width:auto;font-size:15px;padding:13px 20px}
  .casi-home{grid-template-columns:1fr}
  .casi-home .mini,.casi-home .mini.grande{grid-column:auto;aspect-ratio:4/3}
  .universo::before{width:72cqw;height:72cqw}
  .universo::after{display:none}
  .u-servizi .u-p{--r:36}
  .u-lungo{display:none}
  .u-corto{display:inline}
  .u-et{font-size:12.5px;padding:.6em .85em}
  .u-centro{width:32cqw;height:32cqw}
  .u-azione .btn{width:100%;justify-content:center}
  .servizi-g{grid-template-columns:1fr}
  .servizio,.servizio:nth-child(n+4),.servizio[open]{grid-column:auto}
  .servizio summary{min-height:0;padding:20px;gap:14px;grid-template-columns:auto 1fr auto;align-items:center}
  .s-testa,.servizio[open] .s-testa{grid-column:1/-1;grid-row:2}
  .servizio .ico{width:40px;height:40px;grid-column:1}
  .s-piu{grid-column:3}
  .s-dett,.s-dett.con-caso{grid-template-columns:1fr;gap:24px;padding:0 20px 20px}
  .s-chiudi{width:100%;text-align:center}
  .fasi li{grid-template-columns:44px 1fr;gap:6px 14px;padding:24px 0}
  .fasi span{font-size:30px;grid-row:span 2}
  .fasi p{font-size:17px;grid-column:2}
}
/* prestazioni: sul telefono e sui computer che faticano niente vetro calcolato, pannelli pieni */
@media (max-width:960px){.tile,.card .in,form,.persona,.chip,.giro span{backdrop-filter:none!important;-webkit-backdrop-filter:none!important}.card .in,form,.persona{background:rgba(20,15,28,.94)!important}}
html.leggero :is(.nav,.tile,.card .in,form,.persona,.chip,.btn-v){backdrop-filter:none!important;-webkit-backdrop-filter:none!important}
html.leggero :is(.nav,.card .in,form,.persona){background:rgba(20,15,28,.96)!important}
html.leggero :is(.blob,.proposta::before,.proposta::after,.rec::before){animation:none!important;filter:none!important}
@media (prefers-reduced-motion:reduce){.u-anello,.u-et{animation:none}.servizio{transition:none}}
.tabella-legale{width:100%;border-collapse:collapse;margin:8px 0 26px;font-size:15px;line-height:1.5}
.tabella-legale th,.tabella-legale td{text-align:left;vertical-align:top;padding:12px 12px 12px 0;border-bottom:1px solid var(--linea);color:#DDD7E6}
.tabella-legale th{color:#fff;font-weight:700}
.articolo ul.legale{margin:0 0 18px;padding-left:22px;color:#DDD7E6;font-size:19px;line-height:1.7}
.articolo .tabella-scorre{overflow-x:auto}
.foot-legale{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:26px;font-size:14px;color:var(--testo-3)}
.foot-legale a,.foot-legale button{color:inherit;background:none;border:0;padding:0;font:inherit;cursor:pointer;text-decoration:underline}
@media (max-width:520px){.consenso{bottom:12px;padding:22px 18px}.consenso-bottoni{grid-template-columns:1fr}}

.articolo p a,.articolo li a{text-decoration:underline;text-underline-offset:3px}
.vbox{color:#fff}

/* ===== font del brand kit: Aileron per tutto, Bitcount Single (Roman) sulle parole in risalto e sulle etichette ===== */
.grad-t{font-family:'Bitcount Single','Aileron',system-ui,sans-serif;font-weight:700;font-variation-settings:"CRSV" 0;letter-spacing:-.01em;word-spacing:-.2em!important}
.eyebrow{font-family:'Bitcount Single','Aileron',system-ui,sans-serif;font-weight:400;font-variation-settings:"CRSV" 0}
.h-copy p,.ph-hero .lead,.lead-u,.proposta .lead{font-style:italic}
.eyebrow{font-size:14px;letter-spacing:.1em}
/* Aileron è più stretto di Kumbh: la spaziatura stretta pensata per Kumbh fa toccare le lettere */
:is(h1,h2,h3,h4,h5,.s-nome,.prossimo a,.elenco a,.l-det h3,.persona h3,.post h3){letter-spacing:-.02em!important;word-spacing:.05em}
:is(.mega,.kpi strong,.l-num strong,.step .num,.cs-num strong,.passi-g b,.mini strong,.s-caso strong){letter-spacing:-.03em!important}

/* ===== sezioni scure e chiare =====
   Ogni sezione ha un colore fisso a tutta larghezza: scuro (notte) o chiaro (--chiaro, un punto solo), senza pannelli né angoli.
   Dove cambia tono c'è una fascia di quadratini (canvas .px, js/topiko.js). */
"""
TEMA_CSS = _tema_css() + r"""
/* ruota dei servizi: pillole e anelli seguono il tono */
.u-servizi .u-et{background:var(--notte-2);border:1px solid var(--bordo);color:var(--testo)}
.universo::before{border-color:var(--bordo)}.universo::after{border-color:var(--linea)}
.orb{border-color:var(--linea)}
a.u-p:hover .u-et,a.u-p:focus-visible .u-et{color:#fff}
/* fascia clienti: i loghi sono una maschera, quindi prendono il colore del testo e si leggono sia sul chiaro sia sullo scuro */
.track.loghi .lg{display:block;flex:none;opacity:.72;background:var(--testo);-webkit-mask:var(--m) center/contain no-repeat;mask:var(--m) center/contain no-repeat}
.clienti{border-top:0;border-bottom:0}
/* fascia finale: il gradiente Topiko è lo sfondo della sezione a tutta larghezza, non un riquadro */
.cta-fine{background:var(--grad);color:#fff;padding:90px 0!important}
@media (max-width:700px){.cta-fine{padding:60px 0!important}}
.cta-fine .vbox{background:none;padding:0;border-radius:0;overflow:visible}
.cta-fine .vbox::before{display:none}
/* "Cosa facciamo": una sola orbita, pillole con icona; in home due colonne con l'elenco dei servizi */
.universo::after{display:none!important}
.universo{width:min(100%,640px)}
.universo::before{width:74cqw;height:74cqw}
.u-servizi .u-p{--r:37}
.u-et{display:inline-flex!important;align-items:center;gap:.5em;font-size:clamp(13px,2.5cqw,17px)!important;font-weight:700;padding:.7em 1.1em!important;transition:background .25s,color .25s,box-shadow .25s,scale .25s}
.u-ico{display:grid;place-items:center;width:1.5em;height:1.5em;border-radius:50%;background:var(--veli)}
.u-ico svg{width:1em;height:1em}
.u-centro{width:30cqw!important;height:30cqw!important}
.u-p.acceso .u-et{background:var(--grad)!important;color:#fff!important;border-color:transparent!important;box-shadow:0 10px 30px -10px rgba(255,0,130,.7);scale:1.08}
.u-p.acceso .u-ico{background:rgba(255,255,255,.2)}
.hs-griglia{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);grid-template-areas:"tit ruota" "elenco ruota" "btn ruota";column-gap:56px;align-items:start}
.hs-tit{grid-area:tit}.home-servizi .mondo{grid-area:ruota;align-self:center}
.hs-elenco{grid-area:elenco;list-style:none;margin:30px 0 0;padding:0}
.home-servizi .u-azione{grid-area:btn;justify-content:flex-start;margin-top:26px}
.hs-griglia h2.big{font-size:clamp(38px,4vw,60px)}
.hs-voce{display:grid;grid-template-columns:34px 1fr;gap:14px;align-items:start;padding:9px 12px 9px 10px;border-top:1px solid var(--linea);transition:background .2s}
.hs-elenco li:last-child .hs-voce{border-bottom:1px solid var(--linea)}
.hs-voce b{display:block;font-size:16.5px;font-weight:800;letter-spacing:-.01em}
.hs-voce>span>span{display:block;font-size:14.5px;line-height:1.4;color:var(--testo-2);margin-top:2px}
.hs-ico{display:grid;place-items:center;width:34px;height:34px;background:var(--veli);color:var(--testo)}
.hs-ico svg{width:18px;height:18px}
.hs-voce.acceso{background:var(--veli)}
.hs-voce.acceso .hs-ico{background:var(--grad);color:#fff}
@media (max-width:960px){
  .hs-griglia{grid-template-columns:1fr;grid-template-areas:"tit" "ruota" "elenco" "btn"}
  .home-servizi .mondo{margin-top:24px}
  .home-servizi .u-azione .btn{width:100%;justify-content:center}
}
@media (max-width:760px){.u-et{font-size:12.5px!important;padding:.55em .8em!important}.u-servizi .u-p{--r:36}.universo::before{width:72cqw;height:72cqw}}
/* il mondo: canvas con la sfera e i fili, logo fermo al centro, pillole in HTML mosse con transform */
.home-servizi{overflow-x:clip}
.mondo{position:relative;width:min(100%,620px);aspect-ratio:1;margin:0 auto;isolation:isolate}
.mondo canvas{position:absolute;inset:0;width:100%;height:100%;z-index:2;pointer-events:none}
.mondo::before{content:"";position:absolute;inset:12%;border-radius:50%;z-index:0;pointer-events:none;
  background:radial-gradient(closest-side,rgba(155,3,255,.30),rgba(255,0,130,.16) 55%,rgba(255,122,47,0) 100%)}
.m-logo{position:absolute;left:50%;top:50%;z-index:4;width:24%;aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;
  background:var(--grad);display:grid;place-items:center;box-shadow:0 0 60px rgba(255,0,130,.45)}
.m-logo img{width:74%;height:auto}
.m-p{position:absolute;left:0;top:0;z-index:5;display:inline-flex;align-items:center;gap:.5em;white-space:nowrap;
  font:700 15px/1 "Aileron",sans-serif;padding:.6em 1em .6em .6em;border-radius:100px;background:var(--notte-2);color:var(--testo);
  border:1px solid var(--bordo);box-shadow:0 10px 24px -14px rgba(27,20,36,.45);will-change:transform,opacity;transform-origin:50% 50%;
  transition:background .25s,color .25s,border-color .25s}
.m-p.acceso{background:var(--grad);color:#fff;border-color:transparent}
.m-p.acceso .u-ico{background:rgba(255,255,255,.22)}
@media (max-width:760px){.mondo{width:100%;max-width:420px}.m-p{font-size:12px;padding:.5em .8em .5em .5em}.m-logo{width:26%}}
/* 15 servizi: schede su 3 colonne, elenco della home a due colonne di soli nomi */
.servizi-g{grid-template-columns:repeat(3,minmax(0,1fr))!important}
.servizio,.servizio:nth-child(n+4){grid-column:auto!important}
.servizio[open]{grid-column:1/-1!important}
.servizio summary{min-height:190px}
.hs-elenco{display:grid;grid-template-columns:1fr 1fr;column-gap:20px}
.hs-voce{grid-template-columns:30px 1fr!important;align-items:center!important;padding:8px 6px!important}
.hs-elenco li:nth-last-child(2) .hs-voce{border-bottom:1px solid var(--linea)}
.hs-ico{width:30px!important;height:30px!important}
.hs-voce b{font-size:15px!important}
.m-p{font-size:13px}
@media (max-width:960px){.servizi-g{grid-template-columns:1fr!important}.servizio summary{min-height:0}}
@media (max-width:760px){.m-p{font-size:12px;padding:.45em .7em .45em .45em}.hs-elenco{column-gap:12px}.hs-voce b{font-size:13.5px!important}}
/* Servizi: sottotitolo dell'apertura, titolo lungo di Come lavoriamo, frase grande */
.pil-sub{margin-top:18px;font-size:clamp(17px,1.6vw,22px);font-style:italic;color:var(--testo-2)}
.ps-sx h2{font-size:clamp(30px,3.3vw,50px)!important}
.frase-grande p{font-size:clamp(30px,4vw,58px);font-weight:800;line-height:1.08;letter-spacing:-.03em;max-width:1100px;text-wrap:balance}
/* blocchi grandi a spigolo vivo; restano tondi bottoni, pillole, avatar e icone */
.vbox,.lavoro,.casi-grid .lavoro,.servizio,.persona,.persona .foto,.rec-card,.post,.passi-g div,.cs-num div,.recapiti div,form,.contatti-g form,.cs-cover,.articolo .ph,.squadra-foto,.rec-google .mappa,.rec-google .widget,.rec-grid div,.mini,.tile,.card,.card .in,.ta-lato,.consenso,.nav.aperto ul,.ps-fasce div,.s-caso{border-radius:0!important}
.cs-cover .ph,.post .ph{border-radius:0}

body{background:var(--notte);color:var(--testo)}
section.chiara,section.scura{position:relative}
/* superfici e testi che seguono le variabili */
.btn-v{background:var(--veli);color:var(--testo);border:1px solid var(--bordo);box-shadow:none}
.btn-v:hover{background:var(--veli-h)}
.nav .btn-v{border-color:rgba(255,255,255,.22)}
.link-tutti,.card a.leggi{color:var(--testo)}
.lavoro.pieno{background:var(--notte-2);color:var(--testo);box-shadow:inset 0 0 0 1px var(--linea),0 16px 36px -20px var(--sh1)}
.lavoro.pieno .l-num small{color:var(--testo)}
.foot nav a:hover,.nav ul a:hover,.nav ul a.on{color:var(--testo)}
footer{border-top:0}
.btn-g{background:var(--grad);color:#fff}
.chip,.google-voto{background:var(--veli);border:1px solid var(--linea);box-shadow:none}
.rec-card.vuota .testa b,.rec-card.vuota p{background:var(--veli)}
.rec-grid div,.rec-google .widget{border-color:var(--bordo)}
a.rec-card:hover{border-color:var(--bordo)}
.segnaposto{color:var(--giallo)}
.g{box-shadow:0 0 0 1px var(--linea)}
.rec::before{opacity:.35}
.chiara.rec::before{opacity:.16}
/* schede (persone, post, recensioni, passi, numeri, recapiti): bordo leggero e ombra morbida sul chiaro */
.persona,.post,.rec-card,.passi-g div,.cs-num div,.recapiti div{background:var(--notte-2);border:1px solid var(--linea);box-shadow:0 1px 2px var(--sh0),0 16px 36px -20px var(--sh1)}
/* servizi */
.servizio{background:var(--scheda);border-color:var(--linea);box-shadow:0 22px 44px -26px var(--sh1)}
.servizio summary:focus-visible,.s-chiudi:focus-visible{outline-color:var(--testo)}
.servizio .ico{background:var(--veli);color:var(--testo)}
.s-piu{border-color:var(--bordo)}
.s-piu::before,.s-piu::after{background:var(--testo)}
.s-dett li,.s-dett p{color:var(--testo)}
.s-caso{background:var(--incavo)}
.s-chiudi{border-color:var(--bordo);background:var(--scheda-2);color:var(--testo)}
.s-chiudi:hover{background:var(--scheda-2h)}
@media (hover:hover){.servizio:not([open]):hover{background:linear-gradient(145deg,var(--glow-1),var(--glow-2) 55%,var(--glow-3));border-color:var(--glow-b);box-shadow:0 26px 70px -22px var(--glow-s)}
.servizio:not([open]):hover .s-breve{color:var(--testo)}
.servizio:not([open]):hover .ico{background:var(--veli-h)}}
.servizio[open]{background:linear-gradient(145deg,var(--open-1),var(--open-2) 55%,var(--scheda));border-color:var(--glow-b)}
.servizio[open] .s-piu{background:var(--veli-h)}
/* vetro: sul chiaro diventa scheda piena con bordo leggero */
form,.contatti-g form{background:var(--vetro-s);border:1px solid var(--linea);box-shadow:0 1px 2px var(--sh0),0 24px 50px -28px var(--sh1);-webkit-backdrop-filter:none;backdrop-filter:none}
form label.t{color:var(--testo)}
form .ck{color:var(--testo-2)}
form input[type=text],form input[type=email],.contatti-g textarea{background:var(--campo);color:var(--testo);border:1px solid var(--campo-b)}
form input::placeholder,form textarea::placeholder{color:var(--testo-3);opacity:1}
.grazie{background:var(--veli);color:var(--testo)}
.vbox .grazie{background:rgba(255,255,255,.12)}
.modulo-errore{color:var(--errore)!important}
.vbox .modulo-errore{color:#FFD9C2!important}
/* blog e articoli */
.filtri span.on{background:var(--grad);color:#fff}
.articolo p,.articolo ul.legale,.tabella-legale td{color:var(--testo-art)}
.tabella-legale th{color:var(--testo)}
/* misure interne: il respiro lo dà il contenuto, non il riquadro */
.contatti-g,.blog-g,.articolo,.casi-pagina{padding-bottom:0}
.cs-blocchi{padding:0}
.casi-sez{padding-top:96px;padding-bottom:20px}
/* casi in home: griglia ferma, schede più piccole */
.casi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:56px;padding-bottom:20px}
.casi-grid .lavoro{width:100%;height:auto;aspect-ratio:4/5;border-radius:var(--r)}
.casi-grid .l-t{left:20px;right:20px;bottom:20px;grid-template-columns:1fr;gap:12px}
.casi-grid .l-num strong,.casi-grid .l-num strong.parola,.casi-grid .l-num strong[data-pre]{font-size:clamp(40px,4.2vw,62px);white-space:normal;line-height:.92}
.casi-grid .l-num small{font-size:15px;margin-top:8px}
.casi-grid .l-det h3{font-size:clamp(17px,1.5vw,21px);margin:6px 0 10px}
.casi-grid .l-det span{font-size:13px}
.casi-grid .l-det em{font-size:14px}
@media (max-width:1100px){.casi-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){.casi-grid{gap:12px;margin-top:36px}.casi-grid .lavoro{aspect-ratio:auto;height:400px}.casi-grid .l-t{left:12px;right:12px;bottom:12px}.casi-grid .l-num strong,.casi-grid .l-num strong.parola,.casi-grid .l-num strong[data-pre]{font-size:clamp(30px,10vw,42px)}.casi-grid .l-det h3{font-size:14px}.casi-grid .l-det span,.casi-grid .l-det em{font-size:11px}.casi-grid .l-num small{font-size:12px}}
section.chiara:not(.ta-anello):not(.casi-sez):not(.rec):not(.servizi-sez):not(.cta-fine){padding-top:96px;padding-bottom:96px}
/* barra in alto: resta il vetro scuro anche sopra il chiaro */
.nav{background:rgba(14,10,20,.86)!important}
@media (max-width:960px){
  .casi-sez{padding-top:64px;padding-bottom:10px}
  section.chiara:not(.ta-anello):not(.casi-sez):not(.rec):not(.servizi-sez):not(.cta-fine){padding-top:64px;padding-bottom:64px}
  .card .in,form,.persona{background:var(--vetro)!important}
}
html.leggero :is(.card .in,form,.persona){background:var(--vetro)!important}
"""
css += r"""
/* Chi siamo: apertura con il team e l'anello dei servizi (sezione chiara). Prefisso ta- per non toccare il resto del sito.
   --gw = larghezza della foto del gruppo, --pw = unità delle schede dell'anello */
section.ta-anello{--ph:clamp(500px,88svh,880px);--pw:calc(var(--ph)*.72);--gw:min(calc(var(--ph)*.8),740px);
  overflow:hidden;isolation:isolate;text-align:center;padding:126px 0 0}
.ta-anello::before{content:"";position:absolute;inset:0;z-index:-2;pointer-events:none;
  background:radial-gradient(38% 46% at 50% 62%,rgba(155,3,255,.16),transparent 70%),radial-gradient(30% 34% at 72% 70%,rgba(255,0,130,.12),transparent 70%),radial-gradient(28% 30% at 24% 28%,rgba(255,122,47,.10),transparent 70%);
  transform:translate3d(calc(var(--mx,0)*9px),calc(var(--my,0)*6px + var(--sy,0)*.12px),0)}
.ta-testo{position:relative;z-index:5;padding:0 24px}
.ta-testo h1{font-size:clamp(40px,5vw,72px);font-weight:900;line-height:.95;letter-spacing:-.045em;margin:18px auto 0;text-wrap:balance}
.ta-testo h1 span{display:block}
.ta-testo .lead{font-size:clamp(17px,1.5vw,21px);color:var(--testo-2);max-width:620px;margin:16px auto 0}
.ta-palco{position:relative;width:var(--gw);height:calc(var(--gw)*1.046);margin:calc(var(--ph)*.06) auto 0;z-index:3}
.ta-foto{position:absolute;left:0;top:0;width:100%;height:auto;display:block;z-index:2;pointer-events:none;user-select:none;
  transform:perspective(1400px) translate3d(0,calc(var(--sy,0)*-.04px),0) rotateY(calc(var(--mx,0)*2deg)) rotateX(calc(var(--my,0)*-1.5deg));transform-origin:50% 40%}
.ta-ombra{position:absolute;left:-10%;top:-7%;width:120%;height:auto;z-index:1;pointer-events:none;opacity:.34;
  transform:translate3d(calc(var(--mx,0)*-10px),calc(var(--my,0)*-6px + var(--sy,0)*-.02px),0)}
.ta-giro{position:absolute;left:50%;top:31%;width:0;height:0;perspective:calc(var(--gw)*3.6);perspective-origin:50% 50%;
  transform:translate3d(calc(var(--mx,0)*-7px),calc(var(--my,0)*-5px + var(--sy,0)*-.09px),0)}
.ta-giro.dietro{z-index:1}.ta-giro.davanti{z-index:3}
.ta-s{position:absolute;left:0;top:0;border-radius:calc(var(--pw)*.03);overflow:hidden;will-change:transform,opacity;backface-visibility:hidden;-webkit-backface-visibility:hidden;
  border:1px solid var(--notte-2);box-shadow:0 18px 36px -14px var(--sh1);background:#16121D}
.ta-dietro .ta-s,.ta-giro.dietro .ta-s{filter:saturate(.8)}
.ta-s.vetro{width:calc(var(--pw)*.25);height:calc(var(--pw)*.16);padding:calc(var(--pw)*.022);display:flex;flex-direction:column;justify-content:space-between;text-align:left;color:var(--testo);
  background:var(--notte-2);border-color:var(--linea);box-shadow:0 18px 36px -14px var(--sh1)}
.ta-s .ic{width:calc(var(--pw)*.05);height:calc(var(--pw)*.05);border-radius:30%;display:grid;place-items:center;background:var(--grad-sc);color:#fff}
.ta-s .ic svg{width:58%;height:58%}
.ta-s .nm{font-weight:700;font-size:calc(var(--pw)*.024);line-height:1.15;letter-spacing:-.01em}
.ta-s.foto{width:calc(var(--pw)*.21);height:calc(var(--pw)*.175)}
.ta-s.foto>img,.ta-s.tel video,.ta-s.tel>img{width:100%;height:100%;object-fit:cover;display:block}
.ta-s.tel{width:calc(var(--pw)*.15);height:calc(var(--pw)*.267);border-radius:calc(var(--pw)*.022);border:2px solid #0d0a12;outline:1px solid rgba(27,20,36,.15)}
.ta-s.web{width:calc(var(--pw)*.31);height:calc(var(--pw)*.215);border-radius:calc(var(--pw)*.018);background:#fff;display:flex;flex-direction:column}
.ta-s .barra{flex:none;height:calc(var(--pw)*.026);display:flex;align-items:center;gap:calc(var(--pw)*.006);padding:0 calc(var(--pw)*.012);background:#ECE7F1;border-bottom:1px solid rgba(27,20,36,.08)}
.ta-s .barra i{width:calc(var(--pw)*.008);height:calc(var(--pw)*.008);border-radius:50%;background:#FF5F57}
.ta-s .barra i+i{background:#FEBC2E}.ta-s .barra i+i+i{background:#28C840}
.ta-s .barra span{flex:1;margin-left:calc(var(--pw)*.008);height:calc(var(--pw)*.015);border-radius:99px;background:#fff;color:#5E566B;font-size:calc(var(--pw)*.011);line-height:calc(var(--pw)*.015);font-weight:600;text-align:center}
.ta-s .vista{position:relative;flex:1;overflow:hidden}
.ta-s .vista img{position:absolute;left:0;top:0;width:100%;height:auto;display:block;animation:ta-scorri 18s ease-in-out infinite alternate}
@keyframes ta-scorri{0%,12%{transform:translateY(0)}88%,100%{transform:translateY(calc(-100% + var(--pw)*.189))}}
.ta-s.ins{width:calc(var(--pw)*.19);height:calc(var(--pw)*.3);border-radius:calc(var(--pw)*.018);background:#fff;color:#1B1424;display:flex;flex-direction:column;text-align:left}
.ta-s .testa{flex:none;display:flex;align-items:center;gap:calc(var(--pw)*.008);padding:calc(var(--pw)*.009) calc(var(--pw)*.01)}
.ta-s .testa i{flex:none;width:calc(var(--pw)*.022);height:calc(var(--pw)*.022);border-radius:50%;background:#0F7A3A;color:#fff;font:800 calc(var(--pw)*.011)/calc(var(--pw)*.022) "Aileron",sans-serif;font-style:normal;text-align:center;box-shadow:0 0 0 1.5px #fff,0 0 0 2.5px #D4006F}
.ta-s .testa span{display:flex;flex-direction:column;font-size:calc(var(--pw)*.011);line-height:1.15}
.ta-s .testa b{font-weight:700}.ta-s .testa small{font-size:calc(var(--pw)*.0095);color:#5E566B}
.ta-s .im{flex:1;min-height:0;width:100%;object-fit:cover;display:block}
.ta-s .scopri{flex:none;display:flex;justify-content:space-between;align-items:center;padding:calc(var(--pw)*.008) calc(var(--pw)*.01);font-size:calc(var(--pw)*.0115);font-weight:700;border-top:1px solid rgba(27,20,36,.08)}
.ta-s .scopri::after{content:"›";font-size:1.3em;line-height:1}
.ta-s .et{position:absolute;left:calc(var(--pw)*.01);bottom:calc(var(--pw)*.01);max-width:calc(100% - var(--pw)*.02);font-size:calc(var(--pw)*.021);font-weight:700;line-height:1.15;text-align:left;
  padding:.32em .7em;border-radius:calc(var(--pw)*.012);background:rgba(255,255,255,.92);color:#1B1424;box-shadow:0 2px 8px rgba(27,20,36,.18)}
.ta-s.web .et{bottom:auto;top:calc(var(--pw)*.034)}.ta-s.ins .et{bottom:auto;top:calc(var(--pw)*.052)}
.ta-ancora{position:relative}
.ta-orbita{position:absolute;left:0;top:calc(var(--ph)*.42);width:100%;height:calc(var(--ph)*.2);z-index:1;pointer-events:none;overflow:visible}
.ta-orbita path{fill:none;stroke:rgba(27,20,36,.28);stroke-width:1;vector-effect:non-scaling-stroke}
.ta-lato{position:absolute;z-index:4;width:clamp(210px,19vw,270px);padding:22px 22px 20px;border-radius:26px;text-align:left;background:var(--notte-2);border:1px solid var(--linea);
  box-shadow:0 1px 2px var(--sh0),0 24px 48px -22px var(--sh1)}
.ta-lato.sx{left:max(24px,calc(50% - 620px));top:calc(var(--ph)*.2);transform:rotate(-6deg)}
.ta-lato.dx{right:max(24px,calc(50% - 620px));top:calc(var(--ph)*.24);transform:rotate(5deg)}
.ta-lato p{margin:0;font-size:19px;font-weight:700;line-height:1.22;letter-spacing:-.02em;color:var(--testo)}
.ta-lato .ic{display:grid;place-items:center;width:34px;height:34px;border-radius:11px;background:var(--grad-sc);color:#fff;margin-bottom:12px}
.ta-lato .ic svg{width:19px;height:19px}
.ta-fila{display:none}
@media (max-width:1100px){
  .ta-ancora .ta-lato,.ta-orbita{display:none}
  .ta-fila{display:grid;grid-template-columns:1fr 1fr;gap:12px;position:relative;z-index:7;max-width:640px;margin:8px auto 0;padding:0 16px 28px}
  .ta-fila .ta-lato{position:static;width:auto;transform:none}
}
@media (max-width:760px){
  section.ta-anello{--ph:clamp(430px,118vw,520px);--gw:100vw;padding:108px 0 0}
  .ta-testo h1{font-size:38px}
  .ta-palco{margin-bottom:calc(var(--gw)*-.28)}
  .ta-fila{gap:10px;padding:0 16px 24px}
  .ta-fila .ta-lato{padding:14px;border-radius:18px}
  .ta-fila .ta-lato p{font-size:14px}.ta-fila .ta-lato .ic{margin-bottom:8px}
}
@media (prefers-reduced-motion:reduce){.ta-s{will-change:auto}.ta-s .vista img{animation:none}}
html.leggero .ta-s .vista img{animation:none}
"""

# va dopo EXTRA (font del brand kit), così vale sopra le regole vecchie
TITOLI = r"""
/* ===== titoli come nel Figma (26/11): Aileron 800 con spaziatura stretta, parole in risalto in Bitcount Bold a punti tondi ===== */
.grad-t{background:var(--grad-tit);-webkit-background-clip:text;background-clip:text;color:transparent;font-variation-settings:"CRSV" 0,"ELSH" 0}
.eyebrow{font-variation-settings:"CRSV" 0,"ELSH" 0}
:is(.h-copy h1,.ph-hero h1,.ta-testo h1,.cs-testa + h1,h2.big,.ps-sx h2){font-weight:800;letter-spacing:-.03em!important}
:is(h1,h2.big) .grad-t{font-size:.89em;letter-spacing:-.01em!important}
/* home: titolo a sinistra come nel Figma, logo 3D a destra */
.h-copy h1{font-size:clamp(44px,10vw,150px);line-height:.94;color:var(--testo);margin:0 0 30px}
.h-copy h1 .riga{white-space:nowrap}
.h-copy h1 em.grad-t{font-style:normal;font-weight:700;background:var(--grad-tit);-webkit-background-clip:text;background-clip:text;color:transparent}
.h-copy p{font-style:normal;font-size:clamp(18px,2vw,28px);color:var(--testo);max-width:900px}
.h-copy .hero-sub{max-width:none}
@media (max-width:760px){.h-copy h1{font-size:clamp(40px,12.4vw,64px)}.h-copy h1 .riga{white-space:normal}.h-copy p{font-size:18px}}

/* ===== Chi siamo: come lavoriamo, passi che si accendono scorrendo (idea della storia di Bliss) ===== */
.passi-scorri{position:relative;height:calc(100vh + 4 * 55vh)}
.ps-pin{position:sticky;top:0;height:100vh;display:flex;flex-direction:column;justify-content:center;gap:clamp(20px,4vh,48px);padding-top:90px;overflow:hidden}
.ps-pin>.wrap{width:100%}
.ps-alto{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.3fr);gap:60px;align-items:start}
.ps-sx h2{font-size:clamp(36px,4.4vw,64px);line-height:.98;margin-top:18px}
.ps-tab{display:flex;flex-wrap:wrap;gap:6px 26px;border-bottom:1px solid var(--linea);padding-bottom:0}
.ps-tab button{background:none;border:0;padding:0 0 12px;font:500 15px/1.2 "Aileron",sans-serif;color:var(--testo-3);cursor:pointer;position:relative}
.ps-tab button[aria-selected=true]{color:var(--testo)}
.ps-tab button[aria-selected=true]::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--grad);border-radius:2px}
.ps-testi{position:relative;min-height:150px;margin-top:26px}
.ps-testi article{position:absolute;inset:0 0 auto 0;opacity:0;transform:translateY(14px);transition:opacity .45s var(--ease),transform .45s var(--ease)}
.ps-testi article.on{opacity:1;transform:none}
.ps-testi h3{font-size:clamp(26px,2.6vw,38px);font-weight:800;letter-spacing:-.025em;line-height:1.1}
.ps-testi p{margin-top:12px;font-size:clamp(17px,1.4vw,20px);color:var(--testo-2);max-width:620px}
.ps-curva{position:relative;height:clamp(230px,36vh,360px)}
.ps-fasce{position:absolute;inset:0;display:grid;grid-template-columns:repeat(4,1fr)}
.ps-fasce div{position:relative;border-left:1px solid var(--linea);padding:12px 16px;border-radius:18px 18px 0 0;transition:background .5s}
.ps-fasce div b{font-family:'Bitcount Single','Aileron',sans-serif;font-weight:700;font-variation-settings:"CRSV" 0,"ELSH" 0;font-size:15px;color:var(--testo-3);transition:color .4s}
.ps-fasce div.on{background:linear-gradient(180deg,rgba(225,10,233,.16),rgba(155,3,255,.05) 70%,transparent)}
.ps-fasce div.on b{background:var(--grad-tit);-webkit-background-clip:text;background-clip:text;color:transparent}
.ps-curva svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.ps-curva path{fill:none;stroke-width:2;vector-effect:non-scaling-stroke}
.ps-curva .base{stroke:var(--bordo)}
.ps-punto{position:absolute;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:var(--notte);border:2px solid var(--bordo);transition:transform .45s var(--ease),background .45s,border-color .45s,box-shadow .45s}
.ps-punto.fatto{background:#E10AE9;border-color:#E10AE9}
.ps-punto.on{transform:scale(1.7);background:var(--notte-2);border-color:#FF9E03;box-shadow:0 0 0 8px rgba(225,10,233,.22),0 0 30px 6px rgba(255,0,130,.55)}
.ps-punto span{position:absolute;top:22px;left:50%;transform:translateX(-50%);white-space:nowrap;font-size:13px;font-style:normal;color:var(--testo-3)}
.ps-punto.on span{color:var(--testo);transform:translateX(-50%) scale(.6);font-weight:700}
/* senza blocco: telefono, movimento ridotto, modalità leggera */
.passi-scorri.statico{height:auto}
.statico .ps-pin{position:static;height:auto;padding:110px 0 90px;display:block}
.statico .ps-alto{grid-template-columns:1fr;gap:30px}
.statico .ps-tab,.statico .ps-curva{display:none}
.statico .ps-testi{min-height:0;margin-top:0;display:grid;gap:0}
.statico .ps-testi article{position:relative;opacity:1;transform:none;padding:22px 0 22px 30px;border-left:2px solid var(--linea);transition:border-color .6s}
.statico .ps-testi article::before{content:"";position:absolute;left:-8px;top:30px;width:14px;height:14px;border-radius:50%;background:var(--notte);border:2px solid var(--bordo);transition:all .5s}
.statico .ps-testi article.acceso{border-left-color:#E10AE9}
.statico .ps-testi article.acceso::before{background:var(--notte-2);border-color:#FF9E03;box-shadow:0 0 0 6px rgba(225,10,233,.2),0 0 22px 4px rgba(255,0,130,.45)}
"""

ARCO_CSS = r"""
/* ===== arco di lavori in home ===== */
.ar-sez{position:relative;container-type:inline-size;overflow:hidden;color:var(--testo)}
.ar-palco{position:relative;height:40.9cqw}
.ar-dopo{padding:30px 32px 80px}
section.ar-sez{padding-top:0!important;padding-bottom:0!important}
.ar-pre{font-weight:700;font-size:clamp(16px,1.4cqw,19px)}
.ar-dopo h2.big{margin-top:14px;max-width:1000px;text-wrap:balance}
.ar-azioni{display:flex;flex-wrap:wrap;align-items:center;gap:16px 30px;margin-top:34px}
.ar-azioni .link-tutti{margin-top:0;color:var(--testo);border-bottom:2px solid currentColor;padding-bottom:3px}
/* ogni card sta sul raggio di un cerchio che ha il centro sotto la sezione */
.ar-arco{--w:16.5cqw;--R:90cqw;--cy:104.8cqw;--step:11.5deg;list-style:none;position:absolute;inset:0;margin:0;padding:0}
.ar-c{position:absolute;left:50%;top:var(--cy);width:var(--w);aspect-ratio:4/5;
  --a:calc((var(--i) - 3)*var(--step));--h:0px;z-index:calc(var(--i) + 1);
  transform:translate(-50%,-50%) rotate(var(--a)) translateY(calc(var(--R)*-1 + var(--h)));
  transition:transform .45s cubic-bezier(.16,1,.3,1)}
.ar-c:nth-child(4){z-index:20}
/* 5 card, ben distanziate e tutte dentro lo schermo: la prima e l'ultima delle 7 si nascondono (26/11, Bryan) */
.ar-c:is(:nth-child(1),:nth-child(7)){display:none}
.ar-f{display:block;cursor:pointer;position:absolute;inset:0;border-radius:14px;overflow:hidden;background:#d8d0f6;
  box-shadow:0 24px 40px -22px rgba(60,20,110,.45),0 6px 14px -6px rgba(60,20,110,.25)}
.ar-f img,.ar-f video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ar-f video{opacity:0;transition:opacity .5s}
.ar-f video.on{opacity:1}
.ar-l{position:absolute;left:10px;top:10px;padding:4px 10px;border-radius:7px;background:linear-gradient(100deg,#8A00E0 0%,#D4006F 52%,#CC400C 100%);color:#fff;
  font:700 clamp(10px,.85cqw,12.5px)/1.2 "Aileron",system-ui,sans-serif;letter-spacing:.01em}
/* card in risalto: al passaggio del mouse (o al primo tocco su telefono) si alza, si ingrandisce, si raddrizza e passa davanti */
.ar-c{transition:transform .3s cubic-bezier(.16,1,.3,1),opacity .3s}
.ar-f{transition:box-shadow .3s}
.ar-f::before{content:"";position:absolute;inset:0;z-index:3;border-radius:inherit;padding:2px;background:linear-gradient(100deg,#9B03FF,#FF0082 50%,#FF7A2F);pointer-events:none;
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;opacity:0;transition:opacity .3s}
.ar-arco:has(.ar-c:hover) .ar-c:not(:hover),.ar-arco:has(.ar-c.su) .ar-c:not(.su){opacity:.6}
/* la card sotto il mouse fa solo un passo avanti dove si trova: stessa inclinazione, nessuno spostamento verso il centro (26/11, Bryan) */
.ar-c:is(:hover,.su){z-index:40!important;transform:translate(-50%,-50%) rotate(var(--a)) translateY(calc(var(--R) * -1)) scale(1.2)}
.ar-c:is(:hover,.su) .ar-f{box-shadow:0 40px 70px -24px rgba(60,20,110,.65),0 12px 24px -10px rgba(60,20,110,.4)}
.ar-c:is(:hover,.su) .ar-f::before{opacity:1}
@media (hover:none){.ar-c:hover{transform:translate(-50%,-50%) rotate(var(--a)) translateY(calc(var(--R)*-1))}.ar-arco:has(.ar-c:hover) .ar-c:not(:hover){opacity:1}}
/* telefono: arco stretto con 5 card (le altre si nascondono) */
@media (max-width:700px){
  .ar-palco{height:48cqw}
  .ar-dopo{padding:16px 20px 56px}
  .ar-azioni .btn{width:100%;justify-content:center}
  .ar-arco{--w:15cqw;--R:100cqw;--cy:119.4cqw;--step:10.5deg}
  .ar-l{left:5px;top:5px;font-size:8px;padding:2px 5px;border-radius:5px}
  .ar-f{border-radius:9px}
}
@media (prefers-reduced-motion:reduce){.ar-c{transition:none}.ar-f video{display:none}}
"""
(QUI / "js/arco.js").write_text(r"""// arco di lavori in home: su telefono il primo tocco mette la card in risalto, il secondo apre il link.
document.querySelectorAll('#arco .ar-c').forEach((c, _, tutte) => c.querySelector('a').addEventListener('click', e => {
  if (matchMedia('(hover: hover)').matches || c.classList.contains('su')) return;
  e.preventDefault(); tutte.forEach(x => x.classList.toggle('su', x === c));
}));
// i video girano solo quando la sezione è a schermo.
// Movimento ridotto, risparmio dati o connessione lenta: restano sul poster. In modalità leggera girano lo stesso.
(() => {
  const sez = document.getElementById('arco'); if (!sez) return;
  const html = document.documentElement;
  const vids = [...sez.querySelectorAll('video')];
  const c = navigator.connection || {};
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || c.saveData || /2g/.test(c.effectiveType || '')) return;
  let visibile = false;
  const indice = v => +v.closest('.ar-c').style.getPropertyValue('--i');
  const giro = on => {
    // su telefono girano al massimo 2 video, nelle card più al centro (quella al centro è l'indice 3)
    const ok = new Set(innerWidth <= 700 ? [...vids].sort((a, b) => Math.abs(indice(a) - 3) - Math.abs(indice(b) - 3)).slice(0, 2) : vids);
    vids.forEach(v => {
    if (on && ok.has(v) && v.offsetParent !== null) {
      if (v.preload !== 'auto') v.preload = 'auto';
      v.play().then(() => v.classList.add('on')).catch(() => {});
    } else v.pause();
  });
  };
  new IntersectionObserver(e => { visibile = e[0].isIntersecting; giro(visibile); }, {threshold: .2}).observe(sez);
  document.addEventListener('visibilitychange', () => giro(visibile && !document.hidden));
  let w = innerWidth; addEventListener('resize', () => { if (innerWidth !== w) { w = innerWidth; giro(visibile); } });
})();
""", encoding="utf-8")


PILLOLE_CSS = r"""
/* ===== apertura dei Servizi: pillole che cadono (js/pillole.js + vendor/matter.min.js) ===== */
.pil{position:relative;overflow:hidden;background:var(--notte);height:calc(clamp(640px,100vh,900px) + 76px);isolation:isolate}
.pil::before{content:"";position:absolute;inset:0;background:radial-gradient(60% 50% at 50% 0%,rgba(155,3,255,.26),transparent 70%),radial-gradient(40% 40% at 85% 10%,rgba(255,0,130,.14),transparent 70%);z-index:0}
.pil-tit{position:relative;z-index:3;text-align:center;padding:clamp(72px,12vh,120px) 24px 0;pointer-events:none}
.pil-tit h1{margin-top:18px;font-size:clamp(34px,5.6vw,80px);font-weight:800;line-height:1.04;letter-spacing:-.03em}
.pil-tit .bit{font-family:"Bitcount Single",monospace;font-weight:600;letter-spacing:0;display:inline-block}
.pil-campo{position:absolute;inset:0 0 76px 0;z-index:2;overflow:hidden}
.pil-p{position:absolute;left:0;top:0;display:flex;align-items:center;justify-content:center;white-space:nowrap;
  font:800 var(--pf,26px)/1 "Aileron",sans-serif;text-transform:uppercase;letter-spacing:.01em;
  height:var(--ph,56px);padding:0 calc(var(--ph,56px)*.52);border-radius:999px;
  touch-action:none;user-select:none;-webkit-user-select:none;cursor:grab;will-change:transform;
  box-shadow:0 8px 18px -10px rgba(0,0,0,.6)}
.pil-p.cerchio{padding:0;width:var(--ph,56px);font-size:calc(var(--pf,26px)*1.15);font-weight:700}
.pil-p.preso{cursor:grabbing;z-index:5}
.pil-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
@media (max-width:600px){.pil{height:calc(clamp(600px,88vh,720px) + 44px)}.pil-campo{bottom:44px}}
.servizi-sez .tocca{font-style:italic;color:var(--testo-2);font-size:clamp(17px,1.5vw,20px);margin:0 0 28px}
"""
(QUI / "js/pillole.js").write_text(r"""(function(){
var M=Matter,Engine=M.Engine,Bodies=M.Bodies,Body=M.Body,Composite=M.Composite,Constraint=M.Constraint,Sleeping=M.Sleeping;
var sez=document.getElementById('pil'),campo=document.getElementById('pil-campo'),tit=document.getElementById('pil-tit').querySelector('h1');
var ridotto=matchMedia('(prefers-reduced-motion: reduce)').matches,html=document.documentElement;
/* movimento ridotto: pillole già ammucchiate e ferme (in modalità leggera cadono lo stesso) */
function fermo(){return ridotto}

/* etichette: tutte prese dalle schede di servizi.html */
var ETI=campo.dataset.eti.split('|');
var COL=[ /* sfondo, testo */
 ['#9B03FF','#fff'],['#FF0082','#000'],['#FF7A2F','#000'],['#FFC93C','#000'],['#CDA7FF','#000'],['#FFB3D6','#000'],
 ['linear-gradient(100deg,#9B03FF,#FF0082)','#fff'],['linear-gradient(100deg,#FF0082,#FF7A2F)','#000'],['linear-gradient(100deg,#FF7A2F,#FFC93C)','#000']];

var W,H,eng,corpi,rAF=0,visibile=false,attivo=false,spawnT=0,t0=0,pronti=false,presa=null,rnd;
function seme(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}

function conta(w){return w>=900?{p:34,c:6,f:30,h:64}:w>=600?{p:26,c:4,f:22,h:48}:{p:17,c:4,f:15,h:38}}

function costruisci(){
  cancella();
  W=sez.clientWidth;H=campo.clientHeight;rnd=seme(7);
  var cfg=conta(W);
  sez.style.setProperty('--pf',cfg.f+'px');sez.style.setProperty('--ph',cfg.h+'px');
  eng=Engine.create({enableSleeping:true});eng.gravity.y=1.1;
  eng.positionIterations=8;eng.velocityIterations=6;
  corpi=[];
  /* ordine: mescola le etichette, colori a rotazione senza due uguali vicini */
  var el=ETI.slice().sort(function(){return rnd()-.5});
  var lista=[];
  for(var i=0;i<cfg.p;i++){lista.push({t:el[i%el.length],c:COL[(i*4+Math.floor(i/COL.length))%COL.length]})}
  lista.sort(function(){return rnd()-.5});
  lista.forEach(function(d){
    var e=document.createElement('div');e.className='pil-p'+(d.cerchio?' cerchio':'');e.textContent=d.t;
    e.style.background=d.c[0];e.style.color=d.c[1];campo.appendChild(e);d.e=e;
  });
  lista.forEach(function(d){
    var w=d.e.offsetWidth,h=d.e.offsetHeight,b;
    if(d.cerchio)b=Bodies.circle(-500,-500,h/2,{restitution:.45,friction:.35,frictionAir:.004,density:.0015});
    else b=Bodies.rectangle(-500,-500,w,h,{chamfer:{radius:h/2-1},restitution:.42,friction:.35,frictionAir:.004,density:.0015});
    b.sleepThreshold=50;b.pw=w;b.ph=h;b.el=d.e;b.lanciato=false;d.e._b=b;corpi.push(b);
    Sleeping.set(b,true);Body.setStatic(b,true);b.statico=true;
    d.e.style.transform='translate(-999px,-999px)';
  });
  /* muri */
  var t=200,o={isStatic:true,friction:.4,restitution:.2};
  Composite.add(eng.world,[
    Bodies.rectangle(W/2,H+t/2-1,W*3,t,o),
    Bodies.rectangle(-t/2,-H,t,H*4,o),
    Bodies.rectangle(W+t/2,-H,t,H*4,o)]);
  Composite.add(eng.world,corpi);
  /* ordine di caduta a gruppi */
  corpi.forEach(function(b,i){b.gruppo=Math.floor(i/4)});
  spawnT=0;pronti=true;
}
function cancella(){cancelAnimationFrame(rAF);rAF=0;attivo=false;campo.innerHTML='';presa=null}

function lancia(b){
  var cfg=conta(W);
  Body.setStatic(b,false);b.statico=false;Sleeping.set(b,false);
  Body.setPosition(b,{x:b.pw/2+10+rnd()*(W-b.pw-20),y:-b.ph-rnd()*60});
  Body.setAngle(b,(rnd()-.5)*2.4);Body.setAngularVelocity(b,(rnd()-.5)*.12);
  Body.setVelocity(b,{x:(rnd()-.5)*3,y:2+rnd()*2});
}
function disegna(){
  for(var i=0;i<corpi.length;i++){var b=corpi[i];if(b.statico)continue;
    b.el.style.transform='translate('+(b.position.x-b.pw/2).toFixed(1)+'px,'+(b.position.y-b.ph/2).toFixed(1)+'px) rotate('+b.angle.toFixed(4)+'rad)'}
}
function tuttiFermi(){
  if(presa)return false;
  for(var i=0;i<corpi.length;i++){var b=corpi[i];if(b.statico)return false;if(!b.isSleeping)return false}
  return true;
}
var ult=0,acc=0;
function ciclo(ts){
  rAF=0;if(!visibile||!attivo)return;
  var dt=Math.min(40,ts-(ult||ts));ult=ts;acc+=dt;
  var el=ts-t0;
  /* partenza a gruppi sfalsati: ~1,7 s */
  var gMax=Math.ceil(corpi.length/4);
  for(var i=0;i<corpi.length;i++){var b=corpi[i];if(b.statico&&el>=b.gruppo*(1700/gMax))lancia(b)}
  while(acc>=1000/60){
    if(presa){var p=presa;p.c.pointA.x=p.x;p.c.pointA.y=p.y;Sleeping.set(p.b,false)}
    Engine.update(eng,1000/60);acc-=1000/60}
  disegna();
  if(tuttiFermi()){attivo=false;ult=0;return}
  rAF=requestAnimationFrame(ciclo);
}
function sveglia(){if(!pronti)return;if(!attivo){attivo=true;ult=0;acc=0}if(!rAF&&visibile)rAF=requestAnimationFrame(ciclo)}

/* mucchio già fatto (reduced motion e resize) */
function ammucchia(){
  corpi.forEach(lancia);
  for(var i=0;i<1100;i++)Engine.update(eng,1000/60);
  disegna();
}
/* trascinamento: parte solo da una pillola */
campo.addEventListener('pointerdown',function(ev){
  var e=ev.target.closest('.pil-p');if(!e||!e._b||e._b.statico)return;
  var b=e._b,r=campo.getBoundingClientRect(),x=ev.clientX-r.left,y=ev.clientY-r.top;
  e.setPointerCapture(ev.pointerId);Sleeping.set(b,false);e.classList.add('preso');
  var c=Constraint.create({pointA:{x:x,y:y},bodyB:b,pointB:{x:x-b.position.x,y:y-b.position.y},stiffness:.12,damping:.12,length:0});
  Composite.add(eng.world,c);presa={b:b,c:c,x:x,y:y,id:ev.pointerId,e:e};
  b.lanciato=true;sveglia();ev.preventDefault();
});
campo.addEventListener('pointermove',function(ev){
  if(!presa||ev.pointerId!==presa.id)return;var r=campo.getBoundingClientRect();
  presa.x=Math.max(0,Math.min(W,ev.clientX-r.left));presa.y=Math.max(0,Math.min(H,ev.clientY-r.top));
});
function rilascia(ev){
  if(!presa||ev.pointerId!==presa.id)return;
  Composite.remove(eng.world,presa.c);presa.e.classList.remove('preso');presa=null;sveglia();
}
campo.addEventListener('pointerup',rilascia);campo.addEventListener('pointercancel',rilascia);
/* passando col mouse le pillole si scompigliano: spinta via dal cursore, più forte se il mouse va veloce */
var mx=null,my=null,mt=0;
campo.addEventListener('pointermove',function(ev){
  if(presa||ev.pointerType!=='mouse'||!pronti)return;
  var r=campo.getBoundingClientRect(),x=ev.clientX-r.left,y=ev.clientY-r.top,now=performance.now();
  if(mx===null||now-mt>120){mx=x;my=y;mt=now;return}
  var dt=Math.max(8,now-mt),vx=(x-mx)/dt*16,vy=(y-my)/dt*16;mx=x;my=y;mt=now;
  var vel=Math.min(30,Math.hypot(vx,vy)),mosso=false;
  for(var i=0;i<corpi.length;i++){var b=corpi[i];if(b.statico)continue;
    var dx=b.position.x-x,dy=b.position.y-y,d=Math.hypot(dx,dy),rag=Math.max(b.pw,b.ph)/2+30;
    if(d>rag)continue;
    var k=(1-d/rag),f=3+vel*.5;d=d||1;
    Sleeping.set(b,false);
    Body.setVelocity(b,{x:b.velocity.x+(dx/d*f+vx*.35)*k,y:b.velocity.y+(dy/d*f+vy*.35-2.5)*k});
    Body.setAngularVelocity(b,b.angularVelocity+(rnd()-.5)*.08*k);mosso=true}
  if(mosso)sveglia();
});
campo.addEventListener('pointerleave',function(){mx=null});

/* avvio */
var io=new IntersectionObserver(function(en){
  visibile=en[0].isIntersecting;
  if(visibile&&pronti){
    if(fermo()){if(!sez._fermata){ammucchia();sez._fermata=1;sez._partita=1}return}
    if(!sez._partita){sez._partita=1;t0=performance.now();attivo=true;ult=0}
    if(attivo&&!rAF)rAF=requestAnimationFrame(ciclo);
  }
},{threshold:.35});
function avvia(){
  costruisci();sez._partita=0;
  if(fermo()){ammucchia();sez._partita=1;sez._fermata=1}
  else if(visibile){sez._partita=1;t0=performance.now();attivo=true;ult=0;rAF=requestAnimationFrame(ciclo)}
}
var lw=0,tmr;
addEventListener('resize',function(){clearTimeout(tmr);tmr=setTimeout(function(){
  if(sez.clientWidth===lw)return;lw=sez.clientWidth;costruisci();ammucchia();sez._partita=1;},250)});
function init(){lw=sez.clientWidth;io.observe(sez);avvia()}
(document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(init);
})();
""", encoding="utf-8")

(QUI / "js/mondo.js").write_text(r"""// il mondo dei servizi: una sfera di punti (Fibonacci) col gradiente Topiko che gira piano su un asse inclinato.
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
      const filo = (o, sopra) => {
        const acc = o.p === fuoco;
        ctx.globalAlpha = acc ? 1 : .55 * Math.min(1, Math.max(0, (o.v[2] + .05) / .2));
        if (acc) { const g = ctx.createLinearGradient(o.a[0], o.a[1], o.b[0], o.b[1]); g.addColorStop(0, '#9B03FF'); g.addColorStop(.5, '#FF0082'); g.addColorStop(1, '#FF7A2F'); ctx.strokeStyle = g; ctx.lineWidth = 2.2; }
        else { ctx.strokeStyle = '#8A6FB0'; ctx.lineWidth = 1; }
        ctx.beginPath(); ctx.moveTo(o.a[0], o.a[1]); ctx.lineTo(o.b[0], o.b[1]); ctx.stroke();
        ctx.globalAlpha = 1; ctx.fillStyle = acc ? '#FF0082' : '#9B03FF';
        ctx.beginPath(); ctx.arc(o.a[0], o.a[1], acc ? 3.4 : 2.4, 0, 6.2832); ctx.fill();
      };
      // dietro: resta solo il punto d'aggancio, senza filo né pillola
      info.filter(o => o.v[2] < -0.05 && o.p !== fuoco).forEach(o => { ctx.globalAlpha = .5; ctx.fillStyle = '#9B03FF'; ctx.beginPath(); ctx.arc(o.a[0], o.a[1], 2.2, 0, 6.2832); ctx.fill(); ctx.globalAlpha = 1; });
      // sfera: prima i punti dietro, poi quelli davanti
      const rp = Math.max(1.1, R * .0105);
      for (const pass of [0, 1]) for (const pt of punti) {
        const v = ruota(pt, ang); if ((v[2] >= 0) !== !!pass) continue;
        const q = proj(v, R), luce = (v[2] + 1) / 2;
        ctx.globalAlpha = .14 + .86 * luce * luce; ctx.fillStyle = pt[3];
        ctx.beginPath(); ctx.arc(q[0], q[1], rp * (.55 + .6 * luce), 0, 6.2832); ctx.fill();
      }
      ctx.globalAlpha = 1;
      info.filter(o => o.v[2] >= -0.05 || o.p === fuoco).forEach(o => { ctx.save(); ctx.globalAlpha = 1; filo(o, true); ctx.restore(); });
      for (const o of info) {
        const z = o.v[2], s = .85 + .2 * Math.max(0, z);
        const acc = o.p === fuoco;
        o.p.style.transform = `translate(${o.b[0].toFixed(1)}px,${o.b[1].toFixed(1)}px) translate(-50%,-50%) scale(${(acc ? Math.max(1.05, s) : s).toFixed(3)})`;
        // si vede solo quando il testo è leggibile: davanti o di lato verso davanti; dietro sparisce con una dissolvenza veloce
        const vis = acc || z > -0.05, alfa = acc ? 1 : Math.min(1, Math.max(0, (z + .05) / .2));
        o.p.style.opacity = alfa.toFixed(3); o.p.style.visibility = alfa > 0 ? 'visible' : 'hidden';
        o.p.style.pointerEvents = alfa > .5 ? '' : 'none';
        o.p.style.zIndex = acc ? 7 : 5;
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
""", encoding="utf-8")

(QUI / "js/portfolio.js").write_text(r"""// Portfolio: i video girano muti solo quando la card è a schermo, al massimo 3 alla volta. Al clic foto e video si aprono grandi.
// Movimento ridotto, risparmio dati o modalità leggera: restano sul poster. Esc o la X chiudono.
(() => {
  const sez = document.getElementById('portfolio'); if (!sez) return;
  const html = document.documentElement, c = navigator.connection || {};
  const fermo = () => matchMedia('(prefers-reduced-motion: reduce)').matches || c.saveData || html.classList.contains('leggero');
  const vids = [...sez.querySelectorAll('.pf-grid video')], vis = new Set();
  const aggiorna = () => {
    const ok = fermo() ? [] : vids.filter(v => vis.has(v)).slice(0, 3);
    vids.forEach(v => {
      if (ok.includes(v)) { if (v.preload !== 'auto') v.preload = 'auto'; v.play().catch(() => {}); }
      else if (!v.paused) v.pause();
    });
  };
  const io = new IntersectionObserver(es => { es.forEach(e => e.isIntersecting ? vis.add(e.target) : vis.delete(e.target)); aggiorna(); }, {threshold: .35});
  vids.forEach(v => io.observe(v));
  document.addEventListener('visibilitychange', () => document.hidden ? vids.forEach(v => v.pause()) : aggiorna());
  // lightbox
  const box = sez.querySelector('.pf-box'), media = box.querySelector('.pf-media'), cap = box.querySelector('.pf-cap');
  sez.querySelectorAll('.pf-apri').forEach(b => b.addEventListener('click', () => {
    const fig = b.closest('figure'), v = b.querySelector('video'), im = b.querySelector('img');
    media.innerHTML = '';
    if (v) {
      const nv = document.createElement('video');
      Object.assign(nv, {muted: true, loop: true, playsInline: true, controls: true, autoplay: true, poster: v.poster});
      v.querySelectorAll('source').forEach(s => nv.appendChild(s.cloneNode()));
      media.appendChild(nv);
    } else {
      const ni = document.createElement('img'); ni.src = im.src; ni.alt = im.alt; media.appendChild(ni);
    }
    cap.textContent = fig.querySelector('.pf-et').textContent;
    box.showModal();
  }));
  const chiudi = () => { box.close(); };
  box.querySelector('.pf-x').addEventListener('click', chiudi);
  box.addEventListener('click', e => { if (e.target === box) chiudi(); });
  box.addEventListener('close', () => { media.innerHTML = ''; });
})();
""", encoding="utf-8")

SPAZI_CSS = r"""
/* ===== portfolio (pagina I nostri lavori) ===== */
.pf-grid{columns:3;column-gap:16px;margin-top:56px}
.pf-c{break-inside:avoid;margin:0 0 16px;position:relative;border-radius:4px;overflow:hidden;background:var(--notte-2)}
.pf-apri{display:block;width:100%;border:0;padding:0;margin:0;background:none;cursor:zoom-in}
.pf-c img,.pf-c video{display:block;width:100%;height:auto;object-fit:cover;transition:transform .6s var(--ease)}
.pf-v img,.pf-v video{aspect-ratio:9/16}.pf-r img,.pf-r video{aspect-ratio:4/5}.pf-q img,.pf-q video{aspect-ratio:1}
@media (hover:hover){.pf-c:hover img,.pf-c:hover video{transform:scale(1.03)}}
.pf-apri:focus-visible{outline:2px solid #fff;outline-offset:-4px}
.pf-et{position:absolute;left:10px;top:10px;padding:5px 10px;border-radius:6px;background:rgba(13,10,18,.74);color:#fff;font:700 12px/1.2 "Aileron",sans-serif;pointer-events:none}
.pf-box{margin:auto;border:0;padding:0;background:transparent;max-width:94vw;max-height:94vh;overflow:visible}
.pf-box::backdrop{background:rgba(8,6,12,.9)}
.pf-media img,.pf-media video{display:block;max-width:92vw;max-height:84vh;width:auto;height:auto;margin:0 auto;border-radius:4px}
.pf-cap{margin-top:12px;text-align:center;color:#fff;font:700 14px/1.3 "Aileron",sans-serif}
.pf-x{position:fixed;top:18px;right:18px;width:46px;height:46px;border-radius:50%;border:1px solid rgba(255,255,255,.4);background:rgba(13,10,18,.7);color:#fff;font-size:26px;line-height:1;cursor:pointer}
@media (max-width:760px){.pf-grid{columns:2;column-gap:10px;margin-top:40px}.pf-c{margin-bottom:10px}.pf-et{left:6px;top:6px;font-size:10px;padding:3px 7px}}

/* ===== spazi: una scala sola =====
   tra le sezioni 120 px (72 su telefono); l'apertura ha più aria sopra per la barra fissa.
   Due sezioni vicine dello stesso tono non sommano i loro spazi: la seconda parte senza spazio sopra. */
:root{--sez:120px;--sez-top:172px}
@media (max-width:760px){:root{--sez:72px;--sez-top:128px}}
body>section:not(.scena):not(.pil):not(.passi-scorri):not(.ar-sez):not(.ph-hero):not(.ta-anello):not(.consenso){padding-top:var(--sez)!important;padding-bottom:var(--sez)!important}
body>section.ph-hero{padding-top:var(--sez-top)!important;padding-bottom:var(--sez)!important}
body>section.chiara+section.chiara:not(.ar-sez):not(.passi-scorri),
body>section:not(.chiara):not(.cta-fine):not(.consenso)+section:not(.chiara):not(.cta-fine):not(.consenso):not(.scena):not(.pil):not(.passi-scorri){padding-top:0!important}
body>section.ph-hero+section:not(.chiara):not(.cta-fine){padding-top:0!important}
.ph-hero::after{display:none}
footer{padding-top:var(--sez)}
/* dentro le sezioni: eyebrow → titolo 16, titolo → testo 24, testo → bottoni 32, titolo → contenuto 48-56 */
.eyebrow+:is(h1,h2,h3),.eyebrow+div>:is(h1,h2):first-child{margin-top:16px!important}
.ph-hero h1{margin:16px 0 0!important}
:is(h1,h2)+:is(p,.lead,.lead-u,.suggerimento,.pil-sub){margin-top:24px!important}
.ph-hero .lead{margin-top:24px}
:is(.lead,.lead-u,.pil-sub)+:is(.btn,.h-btn,.ar-azioni,.u-azione){margin-top:32px!important}
.casi-grid,.servizi-g,.passi-g,.team-g,.rec-scorre,.cs-num{margin-top:56px}
.servizi-sez .servizi-g{margin-top:0}
.ps-pin{padding-top:90px}
/* passaggio scuro/chiaro: fascia ferma con una sfumatura morbida, che a metà passa per un tono viola leggero.
   La fascia aggiunge spazio, quindi le due sezioni vicine si accorciano: il testo non finisce mai sulla parte centrale. */
.sfuma{height:200px;pointer-events:none}
.sfuma-sc{background:linear-gradient(180deg,#0D0A12 0%,#120D1A 12%,#1E1529 24%,#32244A 38%,#55447A 50%,#8B7BAE 62%,#BFB2D6 75%,#E2D9EE 88%,#F4EFF8 100%)}
.sfuma-cs{background:linear-gradient(0deg,#0D0A12 0%,#120D1A 12%,#1E1529 24%,#32244A 38%,#55447A 50%,#8B7BAE 62%,#BFB2D6 75%,#E2D9EE 88%,#F4EFF8 100%)}
body>section.pre-sf{padding-bottom:40px!important}
body>section.post-sf{padding-top:40px!important}
@media (max-width:760px){.sfuma{height:110px}body>section.pre-sf{padding-bottom:24px!important}body>section.post-sf{padding-top:24px!important}}
body>section.clienti{padding:48px 0!important}
@media (max-width:760px){body>section.clienti{padding:36px 0!important}}
body>section.passi-scorri{padding:0!important}
body>section.ta-anello+section{padding-top:72px!important}
.frase-grande .grad-t{white-space:nowrap}
"""

FONT_UGUALI = r"""
/* ===== Aileron e Bitcount grandi uguali e con gli stessi spazi =====
   Misure nel browser (canvas, ai pesi usati): Aileron 800 x-height 0,533 em, maiuscole 0,690; Bitcount 700 x-height 0,530, maiuscole 0,630.
   Non combaciano tutte e due: nei titoli Bitcount sta al 104% (minuscole +4%, maiuscole -5%), una via di mezzo che a occhio pesa uguale.
   Nelle eyebrow (tutte maiuscole) si fanno combaciare le maiuscole: cap-height .69 = Bitcount al 115%.
   Il box delle righe è lo stesso per i due font (ascent 92%, descent 24%, gap 0 nei @font-face, compensati per il 104% di Bitcount),
   quindi l'interlinea dipende solo dal line-height del titolo. */
.grad-t,.h-copy h1 em.grad-t,.pil-tit .bit,:is(h1,h2,h3,p) .grad-t{font-size:1.04em!important;line-height:inherit!important;
  display:inline!important;vertical-align:baseline!important;padding:0!important;margin:0!important;
  letter-spacing:-.03em!important;word-spacing:-.39em!important;font-weight:700}
.eyebrow,.ps-fasce div b{font-size-adjust:cap-height .69}
.h-copy h1 .riga span,.ph-hero h1 .riga span{padding-bottom:0!important;margin-bottom:0!important}
.h-copy h1 .riga>span,.ph-hero h1 .riga>span{vertical-align:top}
.h-copy h1 .riga,.ph-hero h1 .riga{padding:0 .1em .12em!important;margin:0 -.1em -.12em!important}
:is(.h-copy h1,.ph-hero h1,.ta-testo h1,.pil-tit h1,h2.big,.ps-sx h2,.ar-dopo h2,.vbox h2,.frase-grande p){line-height:1.02!important}
/* apertura della home: con Bitcount a grandezza piena la riga "nel topic giusto." deve stare nella colonna */
.h-copy h1{font-size:clamp(40px,8.2vw,120px)!important}
/* Bitcount è al 104%: la sua riga è 1,02 del titolo, cioè 1,02/1,04 della sua misura */
:is(.h-copy h1,.ph-hero h1,.ta-testo h1,.pil-tit h1,h2.big,.ps-sx h2,.ar-dopo h2,.vbox h2,.frase-grande p,h1,h2) .grad-t{line-height:.9808em!important}
"""

CASI_CSS = r"""
/* Contatti: il modulo arriva subito sotto il titolo, stesso fondo */
body>section.ph-hero:has(+ .contatti-sez){padding-bottom:40px!important;overflow-x:clip;overflow-y:visible}
.contatti-sez{padding-top:0!important;position:relative;z-index:1}
/* ===== casi in home: fila di pannelli, quello attivo largo, le strisce strette accanto ===== */
.casi-fila{--fp-h:360px;--fp-w:380px;--fp-s:74px;--fp-g:14px;overflow:hidden}
.fp-vista{margin-top:32px;height:var(--fp-h);position:relative}
.fp-track{display:flex;gap:var(--fp-g);align-items:flex-start;height:100%;transition:transform .8s cubic-bezier(.65,0,.35,1);will-change:transform;touch-action:pan-y}
.fp-p{position:relative;flex:none;display:block;overflow:hidden;width:var(--fp-s);background:#16121D;transition:width .8s cubic-bezier(.65,0,.35,1),height .8s cubic-bezier(.65,0,.35,1),margin .8s cubic-bezier(.65,0,.35,1),opacity .4s}
.fp-p img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.fp-main{height:86%;margin-top:3%}
.fp-s0{height:78%;margin-top:6%}.fp-s1{height:70%;margin-top:11%}.fp-s2{height:82%;margin-top:2%}
.fp-main.on{width:var(--fp-w);height:100%;margin-top:0}
.fp-p{transition:width .8s cubic-bezier(.65,0,.35,1),height .8s cubic-bezier(.65,0,.35,1),margin .8s cubic-bezier(.65,0,.35,1),opacity .5s,transform .6s cubic-bezier(.2,.8,.2,1),box-shadow .6s}
/* il caso attivo fa un passo avanti dove si trova: più grande, in primo piano; gli altri restano al loro posto, un po' spenti */
.fp-p:not(.att){opacity:.5}
.fp-p:not(.att):hover{opacity:.85}
.fp-p.att{opacity:1;z-index:2;transform:scale(1.06);box-shadow:0 30px 60px -24px rgba(0,0,0,.7)}
.fp-vista{overflow:visible}.fp-track{padding:0 20px}
.casi-fila .fp-sotto{margin-top:44px}
.fp-parola{position:absolute;inset:0;display:grid;place-items:center;padding:16px;text-align:center;font:900 clamp(22px,2.6vw,40px)/1 "Aileron",sans-serif;letter-spacing:-.03em;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.fp-main:not(.on) .fp-parola{font-size:0}
.fp-main:not(.on):has(.fp-parola){background:var(--grad)}
.fp-sotto{display:grid;grid-template-columns:auto 1fr auto;align-items:end;gap:24px;margin-top:22px}
.fp-freccia{width:56px;height:56px;border-radius:50%;border:1.5px solid var(--bordo);background:none;color:var(--testo);display:grid;place-items:center;cursor:pointer;transition:background .2s,border-color .2s}
.fp-freccia svg{width:22px;height:22px}
.fp-freccia:hover{background:var(--veli-h);border-color:var(--testo)}
.fp-freccia:focus-visible{outline:2px solid var(--testo);outline-offset:3px}
.fp-caps{display:grid;text-align:center}
.fp-cap{grid-area:1/1;opacity:0;transform:translateY(10px);transition:opacity .45s,transform .45s;pointer-events:none}
.fp-cap.on{opacity:1;transform:none;pointer-events:auto}
.fp-et{display:block;font:700 12px/1.3 "Aileron",sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--testo-2)}
.fp-tit{display:block;margin-top:6px;font:800 clamp(22px,2.55vw,37px)/1.1 "Aileron",sans-serif;letter-spacing:-.025em;color:var(--testo);text-wrap:balance}
.fp-num{margin-top:8px;display:flex;flex-wrap:wrap;justify-content:center;align-items:baseline;gap:4px 12px}
.fp-num strong{font:900 clamp(22px,1.9vw,28px)/1 "Aileron",sans-serif;letter-spacing:-.03em;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;padding-bottom:.06em}
.fp-num span{font-size:15px;color:var(--testo-2)}
.fp-freccia{margin-bottom:-4px}
body>section.casi-fila{padding-top:100px!important}
.casi-fila .casi-testa h2.big{margin-top:12px!important}
.casi-fila h2.big{font-size:clamp(36px,5vw,72px)}
@media (max-width:760px){
  .casi-fila{--fp-h:300px;--fp-w:calc(100vw - 96px);--fp-s:30px;--fp-g:8px}
  .fp-tit{font-size:20px;text-wrap:balance}
  body>section.casi-fila{padding-top:72px!important}
  .fp-vista{margin-top:28px}
  .fp-sotto{grid-template-columns:1fr 1fr;gap:16px 12px}
  .fp-caps{grid-column:1/-1;grid-row:1}
  .fp-prima{justify-self:end}.fp-dopo{justify-self:start}
  .fp-freccia{width:48px;height:48px}
  .fp-num span{font-size:14px}
}
@media (prefers-reduced-motion:reduce){.fp-track,.fp-p,.fp-cap{transition:none}}
"""

RUOTA_CSS = r"""
/* ===== I nostri lavori: fila dritta senza fine dei casi studio ===== */
/* Prove A (fila dritta) e B (curva leggera): casi studio, solo anteprima */
.rot-sez{position:relative;overflow:hidden}
.rot-sez::before{content:"";position:absolute;width:1100px;height:1100px;left:50%;top:120px;margin-left:-550px;background:radial-gradient(closest-side,rgba(155,3,255,.26),rgba(255,0,130,.08) 60%,transparent);pointer-events:none}
.rt{--w:1000px;--h:520px;position:relative;margin-top:0;height:calc(var(--h) + 50px);touch-action:pan-y;user-select:none;-webkit-user-select:none;outline:none}
.rt:focus-visible{outline:2px solid rgba(255,255,255,.5);outline-offset:6px}
.rt-stage{position:absolute;inset:0}
.rc{position:absolute;left:50%;top:10px;width:var(--w);height:var(--h);margin-left:calc(var(--w) / -2);overflow:hidden;border-radius:3px;container-type:inline-size;display:block;color:#F4F1F8;text-decoration:none;background:#16121d;box-shadow:0 45px 80px -38px rgba(0,0,0,.85),0 12px 28px -12px rgba(0,0,0,.6),0 0 0 1px rgba(255,255,255,.1)}
.rc::after{content:"";position:absolute;inset:0;padding:1px;border-radius:inherit;background:linear-gradient(135deg,rgba(255,255,255,.55),rgba(155,3,255,.5) 32%,rgba(255,0,130,.3) 66%,rgba(255,255,255,.12));-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none;z-index:6}
.rc-dim{position:absolute;inset:0;z-index:7;background:#0b0810;opacity:var(--dim,0);pointer-events:none}
.rc-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.rc-vel{position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,rgba(13,10,18,.8) 0%,rgba(13,10,18,.62) 24%,rgba(13,10,18,.24) 42%,rgba(13,10,18,0) 58%),radial-gradient(55% 80% at 0% 100%,rgba(155,3,255,.32),transparent 70%)}
.rc-top{position:absolute;z-index:3;left:4.6cqw;right:4.6cqw;top:4.2cqw;display:flex;align-items:baseline;gap:1.8cqw;flex-wrap:wrap}
.rc-nome{font-weight:800;font-size:max(20px,3.1cqw);letter-spacing:-.03em;line-height:1;text-shadow:0 2px 18px rgba(0,0,0,.5)}
.rc-sett{font-family:'Bitcount Single','Aileron',sans-serif;font-variation-settings:"CRSV" 0,"ELSH" 0;font-size:max(11px,1.35cqw);letter-spacing:.1em;text-transform:uppercase;color:#E6E0EE;display:flex;align-items:center;gap:10px;text-shadow:0 1px 10px rgba(0,0,0,.6)}
.rc-sett::before{content:"";width:24px;height:2px;background:var(--grad);flex:none}
.rc-testo{position:absolute;z-index:3;left:4.6cqw;bottom:4.4cqw;width:52cqw}
.rc-pre{display:block;font-size:2.5cqw;font-weight:700;line-height:1;margin-bottom:.4cqw;text-shadow:0 2px 14px rgba(0,0,0,.5)}
.rt-num{display:block;font-size:11.6cqw;font-weight:800;letter-spacing:-.045em;line-height:.86;white-space:nowrap;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;padding:.04em .1em .12em 0;filter:drop-shadow(0 4px 22px rgba(13,10,18,.45))}
.rc-lab{display:block;font-size:max(15px,1.95cqw);margin-top:1.1cqw;line-height:1.25;font-weight:700;text-shadow:0 2px 14px rgba(0,0,0,.55)}
.rc-tit{display:block;font-size:max(13px,1.55cqw);margin-top:.9cqw;line-height:1.4;color:#E4DEEC;max-width:44cqw;text-shadow:0 1px 12px rgba(0,0,0,.6)}
.rc-ln{display:inline-flex;align-items:center;gap:12px;margin-top:2.2cqw;font-weight:700;font-size:max(14px,1.6cqw);color:#fff;padding:1.1cqw 2.2cqw;border-radius:100px;background:var(--grad);box-shadow:0 10px 36px -10px rgba(255,0,130,.8)}
.rc-ln svg{width:1.1em;height:1.1em;transition:transform .35s var(--ease)}
.rc:hover .rc-ln svg{transform:translateX(5px)}
.rc-ins{position:absolute;z-index:3;overflow:hidden;background:#211B2A;box-shadow:0 30px 60px -20px rgba(0,0,0,.8),0 0 0 1px rgba(255,255,255,.3)}
.rc-ins img,.rc-ins video{width:100%;height:100%;object-fit:cover;display:block;pointer-events:none;-webkit-user-drag:none}
.rc-ins.v{right:7.5cqw;top:14cqw;width:21cqw;aspect-ratio:9/16;transform:rotate(3deg)}
.rc-ins.f{right:25cqw;bottom:6.5cqw;width:13.5cqw;aspect-ratio:1;transform:rotate(-5deg)}
/* quarta card: mosaico nitido dei lavori, gradiente Topiko che si muove */
.rc-fine .coll{position:absolute;inset:0;display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(2,1fr)}
.rc-fine .coll img{width:100%;height:100%;object-fit:cover}
.rc-fine .anim{position:absolute;inset:0;z-index:1;background:linear-gradient(115deg,rgba(155,3,255,.8),rgba(255,0,130,.62),rgba(255,122,47,.55),rgba(155,3,255,.8));background-size:300% 100%;animation:rcMove 9s linear infinite;mix-blend-mode:multiply;opacity:.85}
@keyframes rcMove{to{background-position:-300% 0}}
.rc-fine .vel2{position:absolute;inset:0;z-index:2;background:radial-gradient(75% 110% at 0% 50%,rgba(13,10,18,.9),rgba(13,10,18,.45) 62%,rgba(13,10,18,.05))}
.rc-fine .rc-testo{width:68cqw;bottom:auto;top:50%;transform:translateY(-50%)}
.rc-fine h2{font-size:6.9cqw;font-weight:800;letter-spacing:-.03em;line-height:.98em;margin-top:2.2cqw;text-shadow:0 2px 20px rgba(0,0,0,.5)}
.rc-fine h2 .grad-t{margin-left:.1em;white-space:nowrap}
.rc-fine .rc-ln{margin-top:3cqw}
.rc-gira{position:absolute;z-index:3;right:6cqw;bottom:6cqw;width:14cqw;height:14cqw;border-radius:50%;border:2px solid rgba(255,255,255,.8);display:grid;place-items:center;background:rgba(13,10,18,.35);transition:transform .5s var(--ease),background .4s}
.rc-gira svg{width:46%;height:46%}
.rc-fine:hover .rc-gira{background:var(--grad);border-color:transparent;transform:rotate(-45deg)}
.rt-dots{display:flex;justify-content:center;align-items:center;gap:10px;margin-top:6px;position:relative;z-index:2}
.rt-dots button{height:34px;min-width:34px;padding:0 12px;border-radius:100px;border:1px solid rgba(255,255,255,.28);background:transparent;color:#B9B2C4;font:700 13px/1 'Aileron';letter-spacing:.04em;transition:background .3s,color .3s,border-color .3s,min-width .4s var(--ease)}
.rt-dots button[aria-current=true]{background:var(--grad);border-color:transparent;color:#fff;min-width:78px}
.rt-dots button[aria-current=true]::after{content:" / 04";opacity:.8}
@media (max-width:860px){
 .rt{--w:min(78vw,360px);--h:500px;margin-top:0}
 .rc-vel{background:linear-gradient(180deg,rgba(13,10,18,.55) 0%,rgba(13,10,18,0) 24%),linear-gradient(0deg,rgba(13,10,18,.92) 0%,rgba(13,10,18,.78) 36%,rgba(13,10,18,.12) 68%,rgba(13,10,18,0) 100%),radial-gradient(70% 50% at 0% 100%,rgba(155,3,255,.3),transparent 70%)}
 .rc-top{left:6cqw;right:6cqw;top:6cqw;gap:1.5cqw 3cqw}
 .rc-nome{font-size:8cqw}.rc-sett{font-size:11px}
 .rc-testo{left:6cqw;right:6cqw;bottom:6cqw;width:auto}
 .rc-pre{font-size:5.6cqw}.rt-num{font-size:21cqw}
 .rc-lab{font-size:4.8cqw;margin-top:2cqw}.rc-tit{font-size:3.9cqw;max-width:none;margin-top:1.6cqw}
 .rc-ln{margin-top:4cqw;font-size:4cqw;padding:3cqw 6cqw}
 .rc-ins.v{right:6cqw;top:23cqw;width:30cqw}
 .rc-ins.f{right:auto;left:6cqw;top:26cqw;bottom:auto;width:21cqw}
 .rc-fine .rc-testo{width:auto;top:46%}
 .rc-fine h2{font-size:12.4cqw}.rc-fine .rc-ln{margin-top:7cqw}
 .rc-fine .coll{grid-template-columns:repeat(2,1fr);grid-template-rows:repeat(3,1fr)}
 .rc-gira{width:22cqw;height:22cqw;right:7cqw;bottom:7cqw}
}
@media (prefers-reduced-motion:reduce){.rc-fine .anim{animation:none}.rc-ln svg,.rc-gira{transition:none}}
/* frecce (solo computer): cerchio sottile, al passaggio si riempie un poco */
.rt-fr{position:absolute;top:calc(10px + var(--h) / 2 - 28px);z-index:300;width:56px;height:56px;border-radius:50%;border:1px solid rgba(255,255,255,.45);background:rgba(13,10,18,.35);color:#fff;display:grid;place-items:center;transition:background .3s,border-color .3s}
.rt-fr:hover{background:rgba(255,255,255,.16);border-color:rgba(255,255,255,.85)}
.rt-fr:focus-visible{outline:2px solid #fff;outline-offset:3px}
.rt-fr svg{width:22px;height:22px}
.rt-prev{left:28px}.rt-next{right:28px}
@media (max-width:860px){.rt-fr{display:none}}
/* spazio tra la fila e il Portfolio: 120px a schermo (72 su telefono), come --sez in SPAZI_CSS; 45px sono già dentro il Portfolio (ripetizioni della classe per battere le regole generali) */
body>section.rot-sez.rot-sez.rot-sez.rot-sez.rot-sez.rot-sez.rot-sez{padding-bottom:75px!important}
@media (max-width:760px){body>section.rot-sez.rot-sez.rot-sez.rot-sez.rot-sez.rot-sez.rot-sez{padding-bottom:27px!important}}
/* la freccia tonda della quarta card si vede solo quando la card è davanti: nelle laterali sfuma */
.rc-gira{opacity:calc(1 - var(--dim,0) * 3.4)}
"""
(QUI / "js/ruota.js").write_text(r"""// Casi studio (pagina I nostri lavori): fila dritta senza fine. Frecce (computer), tastiera, puntini e swipe (telefono). Video muti, gira solo quello della card davanti; si fermano solo con movimento ridotto.
(() => {
const I = 'img/', P = I + 'portfolio/', S = '';
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const ARR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
const vid = f => `<video muted loop playsinline preload="none" poster="${P}${f}.webp" aria-hidden="true"><source src="${P}${f}.webm" type="video/webm"><source src="${P}${f}.mp4" type="video/mp4"></video>`;
const img = (src, alt, cls = '', pos = 'center') => `<img ${cls ? `class="${cls}"` : ''} src="${src}" alt="${alt}" loading="lazy" decoding="async" draggable="false" style="object-position:${pos}">`;
const CASI = [
 {url: S + 'caso-gapor.html', nome: 'Gapor', sett: 'scale su misura', pre: '', num: '123', lab: 'richieste di preventivo in cinque settimane', tit: 'Far vedere come nasce una scala a chi ristruttura casa', bg: I + 'gapor-grande.webp', pos: '60% 62%', v: 'gapor-g8', f: P + 'gapor-scala-luci.webp'},
 {url: S + 'caso-insmile.html', nome: 'Insmile', sett: 'sbiancamento dentale', pre: '', num: '3 → 33', lab: 'ordini nel primo mese di campagne', tit: 'Brand book, contenuti e campagne per un negozio online', bg: I + 'insmile.webp', pos: '60% 28%', v: 'insmile-macchie', f: P + 'insmile-azzurro.webp'},
 {url: S + 'caso-koloro.html', nome: 'Koloro', sett: 'caffè bistrot a Parma', pre: 'oltre', num: '600.000', lab: 'visualizzazioni in 113 giorni', tit: 'Dalle locandine ai piatti: un profilo che si riconosce', bg: I + 'koloro.webp', pos: '60% 38%', v: 'koloro-panino', f: P + 'koloro-bowl.webp'}
];
const COLL = ['koloro-bowl', 'gapor-scala-luci', 'insmile-azzurro', 'parmapast-aperitivo', 'farneto-gabian', 'koloro-cannoncini', 'gapor-chiocciola', 'parmapast-tortelli'];
const N = 4;
const card = k => {
 if (k < 3) { const c = CASI[k]; return `<a class="rc" href="${c.url}" aria-label="${c.nome}: ${c.num} ${c.lab}">${img(c.bg, c.nome, 'rc-bg', c.pos)}<span class="rc-vel"></span>
  <span class="rc-ins v">${vid(c.v)}</span><span class="rc-ins f">${img(c.f, c.nome)}</span>
  <span class="rc-top"><span class="rc-nome">${c.nome}</span><span class="rc-sett">${c.sett}</span></span>
  <span class="rc-testo">${c.pre ? `<span class="rc-pre">${c.pre}</span>` : ''}<span class="rt-num">${c.num}</span><span class="rc-lab">${c.lab}</span><span class="rc-tit">${c.tit}</span><span class="rc-ln">Leggi il caso ${ARR}</span></span><span class="rc-dim"></span></a>`; }
 return `<a class="rc rc-fine" href="${S}contatti.html" aria-label="Il prossimo potrebbe essere il tuo progetto. Scrivici"><span class="coll">${COLL.map(f => `<img src="${P}${f}.webp" alt="" loading="lazy" decoding="async" draggable="false">`).join('')}</span><span class="anim"></span><span class="vel2"></span>
  <span class="rc-top"><span class="rc-sett">Il prossimo passo</span></span>
  <span class="rc-testo"><h2>Il prossimo potrebbe essere <span class="grad-t">il tuo progetto</span></h2><span class="rc-ln">Scrivici ${ARR}</span></span>
  <span class="rc-gira" aria-hidden="true">${ARR}</span><span class="rc-dim"></span></a>`;
};
const rt = document.getElementById('rot'), stage = document.getElementById('rot-stage'), dots = document.getElementById('rot-dots');
stage.innerHTML = Array.from({length: N}, (_, k) => card(k)).join('');
dots.innerHTML = Array.from({length: N}, (_, i) => `<button type="button" aria-label="Vai alla card ${i + 1} di ${N}">${String(i + 1).padStart(2, '0')}</button>`).join('');
const cards = [...stage.children], vids = cards.map(c => [...c.querySelectorAll('video')]), db = [...dots.children];
const mod = (a, n) => ((a % n) + n) % n, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
let pos = 0, target = 0, drag = null, moved = false;
const W = () => cards[0].offsetWidth;
const dist = k => mod(k - pos + N / 2, N) - N / 2;   // -2 .. +2, la fila gira sempre nello stesso senso
function draw() {
 const w = W(), gap = innerWidth < 861 ? 6 : 24, S = (innerWidth < 861 ? .9 : .93) * w + gap;
 cards.forEach((c, k) => {
  const d = dist(k), ad = Math.abs(d), sg = Math.sign(d) || 1, near = Math.min(ad, 1);
  let t;
  if (reduce) { t = `translate3d(${d * (w + gap)}px,0,0)`; c.firstElementChild; c.style.setProperty('--dim', (.3 * near).toFixed(3)); }
  else {
   const x = sg * (ad <= 1 ? ad * S : S + (ad - 1) * (.85 * w + gap)), s = 1 - .15 * near;
   t = `translate3d(${x.toFixed(1)}px,0,0) scale(${s.toFixed(4)})`; c.style.setProperty('--dim', (.3 * near).toFixed(3));
  }
  c.style.transform = t; c.style.zIndex = 100 - Math.round(ad * 10);
  c.style.pointerEvents = ad < 1.5 ? 'auto' : 'none';
 });
}
function stato() {
 const cur = mod(Math.round(pos), N);
 db.forEach((b, i) => b.setAttribute('aria-current', i === cur));
 cards.forEach((c, k) => { c.tabIndex = k === cur ? 0 : -1; c.setAttribute('aria-hidden', k === cur ? 'false' : 'true'); });
 vids.forEach((vs, k) => vs.forEach(v => { const on = !reduce && !drag && k === cur && !document.hidden; if (on) { if (v.paused) { v.preload = 'auto'; v.play().catch(() => {}); } } else if (!v.paused) v.pause(); }));
}
// l'aggancio: la fila scorre morbida fino alla card scelta (frecce, tastiera, puntini, swipe)
let run = false, lastT = 0, shown = -1;
function frame(t) {
 const dt = Math.min(.05, (t - lastT) / 1000 || .016); lastT = t;
 pos += (target - pos) * (1 - Math.exp(-dt * 6));
 if (Math.abs(target - pos) < .001) { pos = target; run = false; draw(); stato(); return; }
 draw(); const c = Math.round(pos); if (c !== shown) { shown = c; stato(); }
 requestAnimationFrame(frame);
}
const parti = () => { if (!run) { run = true; lastT = performance.now(); requestAnimationFrame(frame); } };
function anima() { if (reduce) { pos = target; draw(); stato(); return; } stato(); parti(); }
const passo = n => { target = Math.round(target) + n; anima(); };
function vai(i) { const base = Math.round(pos), cur = mod(base, N); target = base + (mod(i - cur + 2, N) - 2); anima(); }
db.forEach((b, i) => b.onclick = () => vai(i));
rt.querySelector('.rt-prev').onclick = () => passo(-1); rt.querySelector('.rt-next').onclick = () => passo(1);
addEventListener('keydown', e => { if (e.key === 'ArrowLeft') passo(-1); if (e.key === 'ArrowRight') passo(1); });
document.addEventListener('visibilitychange', stato);
// dito (o mouse se il movimento è ridotto): la fila segue, poi si aggancia
rt.addEventListener('pointerdown', e => { if (e.button > 0 || (e.pointerType === 'mouse' && !reduce)) return; run = false; drag = {x: e.clientX, y: e.clientY, p: pos, lx: e.clientX, lt: performance.now(), v: 0, on: false}; moved = false; });
addEventListener('pointermove', e => {
 if (!drag) return;
 const dx = e.clientX - drag.x;
 if (!drag.on && Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(e.clientY - drag.y)) { drag.on = true; rt.classList.add('trascina'); try { rt.setPointerCapture(e.pointerId); } catch (_) {} stato(); }
 if (!drag.on) return;
 moved = true; const sp = W() * .7, t = performance.now();
 drag.v = (e.clientX - drag.lx) / Math.max(1, t - drag.lt); drag.lx = e.clientX; drag.lt = t;
 pos = drag.p - dx / sp; draw();
});
const fine = () => {
 if (!drag) return; const d = drag; drag = null; rt.classList.remove('trascina');
 if (d.on) { const sp = W() * .7; let t = Math.round(pos - d.v * 240 / sp); if (t === Math.round(d.p) && Math.abs(pos - d.p) > .18) t = Math.round(d.p) + Math.sign(pos - d.p); target = t; anima(); }
};
addEventListener('pointerup', fine); addEventListener('pointercancel', fine);
rt.addEventListener('click', e => { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
cards.forEach((c, k) => c.addEventListener('click', e => { const d = Math.round(dist(k)); if (d !== 0 && !e.defaultPrevented) { e.preventDefault(); passo(d); } }));
cards.forEach(c => c.addEventListener('dragstart', e => e.preventDefault()));
addEventListener('resize', draw);
draw(); stato();
})();
""", encoding="utf-8")

(QUI / "css/topiko.css").write_text(FONT + css.strip() + "\n" + EXTRA + TITOLI + ARCO_CSS + PILLOLE_CSS + TEMA_CSS + SPAZI_CSS + FONT_UGUALI + CASI_CSS + RUOTA_CSS, encoding="utf-8")

# ---------- script ----------
script_vetro = re.search(r'<svg id="lenti".*?</svg>\n<script>(.*?)</script>', SRC, re.S).group(1)
script_vetro = script_vetro.replace("const SEL = '.nav,.tile:not(.t1),.card .in,form';", "const SEL = '.tile:not(.t1),.card .in,form,.persona';")
(QUI / "js").mkdir(exist_ok=True)
script_vetro = script_vetro.replace("addEventListener('load', tutti);",
    "// le lenti si preparano dopo l'apertura e solo su schermi grandi: sul telefono resta il vetro sfocato\n  if (innerWidth >= 960) addEventListener('load', () => (window.requestIdleCallback ? requestIdleCallback(tutti, {timeout: 1500}) : setTimeout(tutti, 300)));")
script_vetro += """
// mentre la pagina scorre la lente si spegne (resta il vetro sfocato) e torna 180 ms dopo l'ultimo movimento
(() => {
  let t;
  addEventListener('scroll', () => {
    document.documentElement.classList.add('scorre');
    clearTimeout(t);
    t = setTimeout(() => document.documentElement.classList.remove('scorre'), 180);
  }, {passive: true});
})();
"""
(QUI / "js/vetro.js").write_text(script_vetro.strip() + "\n", encoding="utf-8")
blocchi = re.findall(r"<script>\n(.*?)</script>", SRC, re.S)
NUOVA_SCENA = r"""// sequenza renderizzata in Blender, legata allo scorrimento
(() => {
  const N = 120, canvas = document.getElementById('gl'), ctx = canvas.getContext('2d');
  const mobile = () => canvas.clientWidth < 960;
  const lenta = navigator.connection && (navigator.connection.saveData || /(^|-)2g|3g/.test(navigator.connection.effectiveType || ''));
  const passo = mobile() ? 3 : 1;            // sul telefono basta un fotogramma su tre
  const src = i => `seq-logo/f_${String(i + 1).padStart(4, '0')}.webp`;
  const imgs = new Array(N);
  const carica = i => { if (!imgs[i]) { imgs[i] = new Image(); imgs[i].decoding = 'async'; imgs[i].src = src(i); const im = imgs[i]; im.decode && im.decode().catch(() => {}); } return imgs[i]; };
  carica(0).onload = () => { sporco = true; };
  // gli altri fotogrammi arrivano dopo l'apertura, senza rubare tempo al primo disegno
  // partono al primo gesto o dopo 4 secondi: chi non scorre non scarica nulla in più, con rete lenta resta il primo fotogramma
  let partiti = false;
  const parti = () => {
    if (partiti || lenta) return;
    partiti = true;
    let i = passo;
    const prossimo = () => { for (let k = 0; k < 6 && i < N; k++, i += passo) carica(i); if (i < N) setTimeout(prossimo, 80); };
    prossimo();
  };
  addEventListener('scroll', parti, {passive: true, once: true});
  addEventListener('pointermove', parti, {passive: true, once: true});
  addEventListener('load', () => { if (!mobile()) setTimeout(parti, 4000); });
  const tappe = [{p: 0, x: .3, s: .84}, {p: .35, x: .3, s: .84}, {p: 1, x: .3, s: .76}];
  const liscio = t => t * t * (3 - 2 * t);
  const stato = p => { for (let i = 1; i < tappe.length; i++) if (p <= tappe[i].p) { const a = tappe[i - 1], b = tappe[i], t = liscio((p - a.p) / (b.p - a.p || 1)); return {x: a.x + (b.x - a.x) * t, s: a.s + (b.s - a.s) * t}; } return tappe[tappe.length - 1]; };
  const vivo = !matchMedia('(prefers-reduced-motion:reduce)').matches;
  let prog = 0, cur = {f: 0, x: .3, s: .84}, mx = 0, my = 0, smx = 0, smy = 0, sporco = true, visibile = true, inCorso = false;
  if (window.ScrollTrigger) ScrollTrigger.create({trigger: '#scena', start: 'top top', end: 'bottom bottom', onUpdate: s => { prog = s.progress; sveglia(); }});
  addEventListener('pointermove', e => { mx = e.clientX / innerWidth - .5; my = e.clientY / innerHeight - .5; sveglia(); }, {passive: true});
  const misura = () => { const d = Math.min(devicePixelRatio, 1.5); canvas.width = canvas.clientWidth * d; canvas.height = canvas.clientHeight * d; sporco = true; sveglia(); };
  addEventListener('resize', misura); misura();
  new IntersectionObserver(es => { visibile = es[0].isIntersecting; if (visibile) sveglia(); }).observe(canvas);
  function sveglia() { if (!inCorso && visibile) { inCorso = true; requestAnimationFrame(giro); } }
  function vicino(f) { // il fotogramma più vicino già arrivato
    for (let d = 0; d < N; d++) for (const j of [f - d, f + d]) { const im = imgs[j]; if (im && im.complete && im.naturalWidth) return im; }
    return null;
  }
  function giro() {
    const w = canvas.width, h = canvas.height, mob = mobile(), st = stato(prog);
    const t = {f: prog * (N - 1), x: mob ? 0 : st.x, s: mob ? .9 : st.s};
    const prima = cur.f + cur.x + cur.s + smx + smy;
    cur.f += (t.f - cur.f) * .12; cur.x += (t.x - cur.x) * .07; cur.s += (t.s - cur.s) * .07;
    smx += (mx - smx) * .1; smy += (my - smy) * .1;
    const fermo = Math.abs(cur.f + cur.x + cur.s + smx + smy - prima) < .0005;
    if (vivo || !fermo || sporco) {
      const im = vicino(Math.round(cur.f));
      ctx.clearRect(0, 0, w, h);
      if (im) {
        const lato = Math.min(w * (mob ? .95 : .5), h * (mob ? .55 : .86)) * cur.s;
        const cx = w / 2 + cur.x * w + smx * 20, cy = (mob ? h * .32 : h / 2) + smy * 20 + (vivo ? Math.sin(performance.now() / 1300) * h * .014 : 0);
        ctx.drawImage(im, cx - lato / 2, cy - lato / 2, lato, lato);
        sporco = false;
      }
    }
    // quando tutto è fermo il ciclo si spegne e riparte al prossimo scorrimento o movimento del mouse
    if (!visibile || (!vivo && fermo && !sporco)) { inCorso = false; return; }
    requestAnimationFrame(giro);
  }
})();
"""
(QUI / "js/scena.js").write_text(NUOVA_SCENA, encoding="utf-8")


# Chi siamo: come lavoriamo, i passi si accendono scorrendo. Parte solo dove c'è #come-lavoriamo.
(QUI / "js/passi.js").write_text(r"""// come lavoriamo: la sezione resta ferma e i passi si accendono uno alla volta; su telefono, movimento ridotto o modalità leggera i passi stanno uno sotto l'altro
(() => {
  const sez = document.getElementById('come-lavoriamo'); if (!sez) return;
  const art = [...sez.querySelectorAll('.ps-testi article')], tab = [...sez.querySelectorAll('.ps-tab button')];
  const fasce = [...sez.querySelectorAll('.ps-fasce div')], punti = [...sez.querySelectorAll('.ps-punto')], N = art.length;
  const statico = innerWidth < 760 || matchMedia('(prefers-reduced-motion:reduce)').matches;
  if (statico) {
    sez.classList.add('statico');
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) e.target.classList.add('acceso'); }), {rootMargin: '0px 0px -35% 0px'});
    art.forEach(a => io.observe(a));
    return;
  }
  // curva che sale da sinistra a destra: stessi punti per la linea e per i pallini
  const X = [.125, .375, .625, .875], y = x => 86 - 70 * Math.pow(x, 1.7);  // in percentuale dell'altezza
  const d = Array.from({length: 61}, (_, i) => { const x = i / 60; return (i ? 'L' : 'M') + (x * 1000).toFixed(1) + ' ' + (y(x) * 3).toFixed(1); }).join(' ');
  const svg = sez.querySelector('.ps-curva svg');
  svg.querySelectorAll('path').forEach(pa => pa.setAttribute('d', d));
  const taglio = svg.querySelector('#ps-taglio rect');
  punti.forEach((pu, i) => { pu.style.left = X[i] * 100 + '%'; pu.style.top = y(X[i]) + '%'; });
  let ora = -1;
  const accendi = k => {
    if (k === ora) return; ora = k;
    art.forEach((a, i) => a.classList.toggle('on', i === k));
    tab.forEach((t, i) => t.setAttribute('aria-selected', i === k));
    fasce.forEach((f, i) => f.classList.toggle('on', i === k));
    punti.forEach((pu, i) => { pu.classList.toggle('on', i === k); pu.classList.toggle('fatto', i < k); });
  };
  const misura = () => {
    const r = sez.getBoundingClientRect(), corsa = r.height - innerHeight;
    const p = Math.min(1, Math.max(0, -r.top / corsa)), t = p * (N - 1);
    const xa = X[Math.floor(t)], xb = X[Math.min(N - 1, Math.floor(t) + 1)], fx = xa + (xb - xa) * (t - Math.floor(t));
    taglio.setAttribute('width', (fx * 1000).toFixed(1));
    accendi(Math.round(t));
  };
  tab.forEach((t, i) => t.addEventListener('click', () => {
    const top = sez.getBoundingClientRect().top + scrollY, corsa = sez.offsetHeight - innerHeight;
    scrollTo({top: top + corsa * i / (N - 1) + 2, behavior: 'smooth'});
  }));
  let att = false;
  addEventListener('scroll', () => { if (!att) { att = true; requestAnimationFrame(() => { att = false; misura(); }); } }, {passive: true});
  addEventListener('resize', misura);
  misura();
})();
""", encoding="utf-8")


# Chi siamo: anello dei servizi intorno al team. Parte solo sulle pagine con .ta-anello.
(QUI / "js/anello.js").write_text(r"""// anello dei servizi intorno alla foto del team (pagina Chi siamo)
(() => {
  const sez = document.querySelector('.ta-anello'); if (!sez) return;
  const palco = sez.querySelector('.ta-palco'), dietro = sez.querySelector('.ta-giro.dietro'), davanti = sez.querySelector('.ta-giro.davanti');
  const fermo = matchMedia('(prefers-reduced-motion:reduce)').matches;
  const leggero = () => document.documentElement.classList.contains('leggero');
  const A = 'img/anello/';
  const ICONA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/></svg>';
  const SCHEDE = [
    {t: 'vetro', n: 'Strategia e posizionamento'},
    {t: 'tel', n: 'Social e contenuti', v: A + 'reel-insmile'},
    {t: 'web', n: 'Sito web', s: A + 'sito-gapor.webp', u: 'gapor.it'},
    {t: 'tel', n: 'Foto e video', v: A + 'video-topiko'},
    {t: 'ins', n: 'Inserzioni Meta e Google', s: 'img/gapor.webp'},
    {t: 'foto', n: 'Koloro', s: 'img/koloro.webp'}
  ];
  const et = n => `<span class="et">${n}</span>`;
  // la copia davanti ha il video, quella dietro solo il poster: al massimo due video che girano
  const crea = (c, avanti) => {
    const d = document.createElement('div'); d.className = 'ta-s ' + c.t;
    if (c.t === 'vetro') d.innerHTML = `<span class="ic">${ICONA}</span><span class="nm">${c.n}</span>`;
    else if (c.t === 'tel') d.innerHTML = (avanti && !fermo
      ? `<video muted loop playsinline preload="metadata" poster="${c.v}.jpg" style="background:url(${c.v}.jpg) center/cover"><source src="${c.v}.webm" type="video/webm"><source src="${c.v}.mp4" type="video/mp4"></video>`
      : `<img src="${c.v}.jpg" alt="">`) + et(c.n);
    else if (c.t === 'web') d.innerHTML = `<div class="barra"><i></i><i></i><i></i><span>${c.u}</span></div><div class="vista"><img src="${c.s}" alt="" decoding="async"></div>` + et(c.n);
    else if (c.t === 'ins') d.innerHTML = `<div class="testa"><i>g</i><span><b>gapor</b><small>Sponsorizzato</small></span></div><img class="im" src="${c.s}" alt="" decoding="async"><div class="scopri">Scopri di più</div>` + et(c.n);
    else d.innerHTML = `<img src="${c.s}" alt="" decoding="async">` + et(c.n);
    return d;
  };
  const av = [], di = [], video = [];
  SCHEDE.forEach((c, k) => {
    const a = crea(c, true), b = crea(c, false); davanti.appendChild(a); dietro.appendChild(b); av.push(a); di.push(b);
    const v = a.querySelector('video'); if (v) video.push({k, v, on: false});
  });
  const N = SCHEDE.length, TILT = -22, cl = x => x < 0 ? 0 : x > 1 ? 1 : x;
  let base = -25, spinta = 0, ultimo = 0, vivo = false, cs = new Array(N).fill(0);
  const video_ = () => video.forEach(o => {
    const vuoi = vivo && cs[o.k] > .05;
    if (vuoi && !o.on) { o.on = true; const p = o.v.play(); if (p && p.catch) p.catch(() => {}); }
    else if (!vuoi && o.on) { o.on = false; o.v.pause(); }
  });
  const disegna = () => {
    const R = palco.offsetWidth * (innerWidth < 760 ? .5 : .58), th0 = base + spinta;
    for (let k = 0; k < N; k++) {
      const th = th0 + k * 360 / N, c = Math.cos(th * Math.PI / 180), pre = `translate(-50%,-50%) rotateX(${TILT}deg) `;
      cs[k] = c;
      av[k].style.transform = pre + `rotateY(${th}deg) translateZ(${R}px)`;
      di[k].style.transform = pre + `rotateY(${th + 180}deg) translateZ(${-R}px)`;
      av[k].style.opacity = cl((c + .04) / .22); di[k].style.opacity = cl((-c + .04) / .22) * .72;
      av[k].style.zIndex = Math.round(c * 100) + 100; di[k].style.zIndex = Math.round(-c * 100) + 100;
    }
    video_();
  };
  // parallasse leggera: mouse (solo desktop) e scorrimento; spenta con movimento ridotto e in modalità leggera
  let tx = 0, ty = 0, mx = 0, my = 0;
  const mouse = matchMedia('(hover:hover) and (pointer:fine)').matches;
  if (mouse && !fermo) addEventListener('pointermove', e => { tx = e.clientX / innerWidth * 2 - 1; ty = e.clientY / innerHeight * 2 - 1; }, {passive: true});
  const parallasse = () => {
    if (leggero()) { tx = ty = 0; }
    mx += (tx - mx) * .06; my += (ty - my) * .06;
    sez.style.setProperty('--mx', mx.toFixed(3)); sez.style.setProperty('--my', my.toFixed(3));
    sez.style.setProperty('--sy', leggero() ? 0 : Math.min(scrollY, 900).toFixed(0));
  };
  const giro = t => {
    if (!vivo) return;
    const dt = Math.min(60, t - ultimo); ultimo = t;
    base += dt * 360 / 30000; // un giro in 30 secondi
    parallasse(); disegna(); requestAnimationFrame(giro);
  };
  addEventListener('scroll', () => { spinta = scrollY * .12; if (fermo) disegna(); }, {passive: true});
  addEventListener('resize', disegna);
  disegna();
  if (!fermo) new IntersectionObserver(e => {
    const v = e[0].isIntersecting;
    if (v && !vivo) { vivo = true; ultimo = performance.now(); requestAnimationFrame(giro); }
    else if (!v && vivo) { vivo = false; video_(); }
  }).observe(sez);
})();
""", encoding="utf-8")


(QUI / "js/topiko.js").write_text(r"""// animazioni comuni a tutte le pagine; ogni blocco parte solo se la pagina ha i suoi elementi
// ogni pagina si apre dall'inizio: il browser non deve ricordare dove eri arrivato
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
const allInizio = () => { if (!location.hash) window.scrollTo(0, 0); };
allInizio();
addEventListener('pageshow', allInizio);
const ridotto = matchMedia('(prefers-reduced-motion: reduce)').matches;
const $ = s => document.querySelector(s);
const numero = (el, v) => el.textContent = (el.dataset.pre || '') + Math.round(v).toLocaleString('it-IT');


if (window.gsap && !ridotto) {
  gsap.registerPlugin(ScrollTrigger);
  ScrollTrigger.clearScrollMemory('manual');
  addEventListener('load', () => { allInizio(); ScrollTrigger.refresh(); });

  // titoli d'apertura
  if ($('.h-copy h1')) gsap.from('.h-copy h1 .riga > span', {yPercent: 110, duration: 1.2, ease: 'expo.out', stagger: .12, delay: .15});
  if ($('.ph-hero h1')) gsap.from('.ph-hero h1 .riga > span', {yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: .1, delay: .1});
  gsap.from('.h-in', {y: 24, opacity: 0, duration: .6, ease: 'expo.out', stagger: .06, delay: .1});

  gsap.utils.toArray('.rv').forEach(el => gsap.to(el, {opacity: 1, y: 0, duration: 1, ease: 'expo.out', scrollTrigger: {trigger: el, start: 'top 88%'}}));

  // contatori
  document.querySelectorAll('[data-to]').forEach(el => {
    const o = {v: 0};
    ScrollTrigger.create({trigger: el.closest('.card, .cs-num') || el, start: 'top 80%', once: true,
      onEnter: () => gsap.to(o, {v: +el.dataset.to, duration: 1.8, ease: 'power3.out', onUpdate: () => numero(el, o.v), onComplete: () => numero(el, +el.dataset.to)})});
  });

  // scena 3D della home
  if ($('#scena')) {
    const tl = gsap.timeline({scrollTrigger: {trigger: '#scena', start: 'top top', end: 'bottom bottom', scrub: .6}});
    tl.to('.h-copy', {opacity: 0, y: -80, ease: 'none', duration: .35}, .35); tl.to({}, {duration: .3}, .7);
    gsap.utils.toArray('.step').forEach((st, i) => {
      const c = [.3, .48, .66, .84][i], da = st.classList.contains('sx') ? -60 : 60;
      tl.fromTo(st, {opacity: 0, x: da}, {opacity: 1, x: 0, ease: 'power2.out', duration: .06}, c - .08)
        .to(st, {opacity: 0, x: -da / 2, ease: 'power2.in', duration: .05}, c + .06);
    });
  }

  // quadrante del voto
  if ($('#voto')) {
    const o = {v: 0};
    ScrollTrigger.create({trigger: '.vbox', start: 'top 65%', once: true, onEnter: () => gsap.to(o, {v: 72, duration: 2, ease: 'power3.out',
      onUpdate: () => { $('#voto').textContent = Math.round(o.v); $('#arco').style.strokeDashoffset = 327 - 327 * o.v / 100; }})});
  }

  document.querySelectorAll('.mag').forEach(b => {
    b.addEventListener('mousemove', e => { const r = b.getBoundingClientRect();
      gsap.to(b, {x: (e.clientX - r.left - r.width / 2) * .25, y: (e.clientY - r.top - r.height / 2) * .35, duration: .4}); });
    b.addEventListener('mouseleave', () => gsap.to(b, {x: 0, y: 0, duration: .6, ease: 'elastic.out(1,.4)'}));
  });
} else {
  document.querySelectorAll('[data-to]').forEach(el => numero(el, +el.dataset.to));
  if ($('#voto')) { $('#voto').textContent = 72; $('#arco').style.strokeDashoffset = 327 * .28; }
  document.querySelectorAll('.rv').forEach(el => { el.style.opacity = 1; el.style.transform = 'none'; });
}

document.querySelectorAll('.tile').forEach(t => t.addEventListener('mousemove', e => {
  const r = t.getBoundingClientRect(); t.style.setProperty('--mx', e.clientX - r.left + 'px'); t.style.setProperty('--my', e.clientY - r.top + 'px');
}));

// squadra: al passaggio del mouse la persona cammina
document.querySelectorAll('[data-cammina]').forEach(card => {
  const [k, n] = card.dataset.cammina.split(':'), foto = card.querySelector('.foto'), orig = foto.style.backgroundImage;
  const fr = Array.from({length: +n}, (_, i) => `img/cammina/${k}-${String(i + 1).padStart(2, '0')}.jpg`);
  fr.forEach(src => { new Image().src = src; });
  let t = null, i = 0;
  const via = () => { if (t || ridotto) return; t = setInterval(() => { foto.style.backgroundImage = `url(${fr[i++ % fr.length]})`; }, 110); };
  const stop = () => { clearInterval(t); t = null; i = 0; foto.style.backgroundImage = orig; };
  if (matchMedia('(hover: hover)').matches) { card.addEventListener('mouseenter', via); card.addEventListener('mouseleave', stop); }
  else new IntersectionObserver(es => es.forEach(e => e.isIntersecting ? via() : stop()), {threshold: .6}).observe(card);
});

// menù a scomparsa sotto i 960px
const nv = $('.nav'), mb = $('.nav .menu');
if (mb) {
  const chiudi = () => { nv.classList.remove('aperto'); mb.setAttribute('aria-expanded', 'false'); };
  mb.addEventListener('click', e => { e.stopPropagation(); const a = nv.classList.toggle('aperto'); mb.setAttribute('aria-expanded', String(a)); });
  document.addEventListener('click', e => { if (!nv.contains(e.target)) chiudi(); });
  addEventListener('keydown', e => { if (e.key === 'Escape') chiudi(); });
  addEventListener('resize', () => { if (innerWidth > 960) chiudi(); });
}

// le fasce che scorrono da sole si fermano quando non sono sullo schermo
document.querySelectorAll('.track, .rec-track').forEach(t => new IntersectionObserver(es => t.classList.toggle('fermo', !es[0].isIntersecting)).observe(t.parentElement));

// "Cosa facciamo": passando su un servizio dell'elenco si accende la sua pillola nella ruota, e viceversa
document.querySelectorAll('.home-servizi').forEach(sez => {  // vale anche per il mondo dei Servizi
  const tutti = [...sez.querySelectorAll('[data-k]')];
  const accendi = k => tutti.forEach(el => el.classList.toggle('acceso', el.dataset.k === k));
  tutti.forEach(el => {
    el.addEventListener('pointerenter', () => accendi(el.dataset.k));
    el.addEventListener('focus', () => accendi(el.dataset.k));
    el.addEventListener('pointerleave', () => accendi(null));
    el.addEventListener('blur', () => accendi(null));
  });
});

// nei Servizi, un clic su una voce dell'elenco o su una pillola del mondo apre la scheda del servizio e ci porta lì
if (document.querySelector('.servizi-g')) document.querySelectorAll('.home-servizi [data-k]').forEach(el => el.addEventListener('click', e => {
  const d = document.getElementById(el.dataset.k); if (!d || d.tagName !== 'DETAILS') return;
  e.preventDefault();
  if (!d.open) d.querySelector('summary').click();
  else scrollTo({top: d.getBoundingClientRect().top + scrollY - 96, behavior: 'smooth'});
}));

// casi in home: fila di pannelli. Il caso attivo ha il pannello largo e fa un passo avanti dove si trova; frecce, trascinamento col dito,
// passaggio automatico ogni 5 secondi (fermo al passaggio del mouse, fuori schermo e con movimento ridotto).
document.querySelectorAll('.casi-fila').forEach(sez => {
  const vista = sez.querySelector('.fp-vista'), track = sez.querySelector('.fp-track');
  const pann = [...track.children], mains = pann.filter(p => p.classList.contains('fp-main')), caps = [...sez.querySelectorAll('.fp-cap')];
  const n = mains.length, cs = getComputedStyle(sez);
  let att = 0, giro = 0, sopra = false, visibile = false;
  const px = v => { const t = document.createElement('div'); t.style.width = v; sez.appendChild(t); const w = t.getBoundingClientRect().width; t.remove(); return w; };
  // la fila resta ferma e centrata; scorre solo se non entra nello schermo (telefono), quanto basta a mostrare il caso attivo
  const posiziona = () => {
    const W = px('var(--fp-w)'), S = px('var(--fp-s)'), G = px('var(--fp-g)'), V = vista.clientWidth, P = 20;
    let x = 0;
    for (const p of pann) { if (p === mains[att]) break; x += S + G; }
    const tot = W + (pann.length - 1) * S + (pann.length - 1) * G + 2 * P;
    let t;
    if (tot <= V) t = (V - tot) / 2;
    else { t = Math.min(0, Math.max(V - tot, V - (x + W + 2 * P) - 24)); if (x + t < 24) t = 24 - x - P; t = Math.min(0, Math.max(V - tot, t)); }
    track.style.transform = `translateX(${t.toFixed(1)}px)`;
  };
  const vai = i => {
    att = (i + n) % n;
    mains.forEach((m, k) => m.classList.toggle('on', k === att));
    pann.forEach(p => p.classList.toggle('att', +p.dataset.caso === att));
    caps.forEach((c, k) => { c.classList.toggle('on', k === att); c.setAttribute('aria-hidden', k === att ? 'false' : 'true'); });
    posiziona();
  };
  sez.querySelector('.fp-prima').addEventListener('click', () => vai(att - 1));
  sez.querySelector('.fp-dopo').addEventListener('click', () => vai(att + 1));
  // un clic su un pannello di un altro caso lo fa diventare attivo; sul pannello largo apre il caso
  pann.forEach(p => p.addEventListener('click', e => { const c = +p.dataset.caso; if (!(p.classList.contains('fp-main') && c === att)) { e.preventDefault(); vai(c); } }));
  // trascinamento col dito
  let x0 = null, mosso = false;
  vista.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') { x0 = e.clientX; mosso = false; } });
  vista.addEventListener('pointerup', e => {
    if (x0 === null) return; const dx = e.clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) { mosso = true; vai(att + (dx < 0 ? 1 : -1)); }
  });
  vista.addEventListener('click', e => { if (mosso) { e.preventDefault(); e.stopPropagation(); mosso = false; } }, true);
  // automatico
  const auto = () => { clearInterval(giro); if (visibile && !sopra && !matchMedia('(prefers-reduced-motion: reduce)').matches) giro = setInterval(() => vai(att + 1), 5000); };
  sez.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') { sopra = true; auto(); } });
  sez.addEventListener('pointerleave', e => { if (e.pointerType === 'mouse') { sopra = false; auto(); } });
  sez.addEventListener('focusin', () => { sopra = true; auto(); });
  sez.addEventListener('focusout', () => { sopra = false; auto(); });
  new IntersectionObserver(es => { visibile = es[0].isIntersecting; auto(); }).observe(sez);
  addEventListener('resize', posiziona, {passive: true});
  vai(0);
});

// modulo Contatti: manda il messaggio al motore (valuta-worker), che lo gira via mail al team
const modulo = document.getElementById('modulo-contatti');
if (modulo) modulo.addEventListener('submit', async e => {
  e.preventDefault();
  const motore = /localhost|127\.0\.0\.1/.test(location.hostname) ? 'http://127.0.0.1:8788' : (window.TOPIKO_VALUTA || '');
  const errore = modulo.querySelector('.modulo-errore'), bottone = modulo.querySelector('button'), grazie = modulo.querySelector('.grazie');
  errore.textContent = '';
  bottone.disabled = true;
  try {
    const r = await fetch(motore, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({
      tipo: 'contatto', ...Object.fromEntries(new FormData(modulo)), privacy: modulo.querySelector('#c-priv').checked})});
    const d = await r.json();
    if (!r.ok) throw new Error(d.errore);
    modulo.reset();
    grazie.style.display = 'block';
  } catch (err) {
    errore.textContent = (err instanceof TypeError || !err.message ? 'Il messaggio non è partito.' : err.message) + ' Puoi scriverci a info@topikolab.it.';
  }
  bottone.disabled = false;
});

""", encoding="utf-8")

# ---------- pezzi comuni ----------
FRECCIA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
VOCI = [("servizi.html", "Servizi"), ("casi-studio.html", "I nostri lavori"), ("chi-siamo.html", "Chi siamo"), ("blog.html", "Appunti dal lab"), ("analisi.html", "Analisi gratuita")]
SOCIAL = [("https://www.instagram.com/topikolab/", "Instagram", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'),
          ("https://www.linkedin.com/company/topikolab/", "LinkedIn", '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.06c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.77 2.65 4.77 6.1V21h-4v-5.1c0-1.22-.02-2.78-1.7-2.78-1.7 0-1.96 1.33-1.96 2.7V21h-4z"/></svg>'),
          ("https://www.facebook.com/profile.php?id=61576566621857", "Facebook", '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7.5h2.5l.4-3h-2.9V8.6c0-.86.24-1.45 1.48-1.45H16.6V4.47A20 20 0 0 0 14.3 4.35c-2.28 0-3.84 1.39-3.84 3.95v2.2H8v3h2.46V21z"/></svg>')]


def nav(attiva):
    ul = "".join(f'<li><a href="{h}"{" class=\"on\"" if h == attiva else ""}>{t}</a></li>' for h, t in VOCI)
    return f'''<svg id="lenti" width="0" height="0" style="position:absolute" aria-hidden="true"></svg>
<header class="nav">
  <a href="index.html"><img src="img/logo-topiko.png" alt="Topiko Lab"></a>
  <ul id="voci">{ul}</ul>
  <div class="social">{"".join(f'<a href="{u}" aria-label="{n}">{i}</a>' for u, n, i in SOCIAL)}</div>
  <a class="btn btn-g" href="contatti.html">Contatti</a>
  <button class="menu" type="button" aria-label="Apri il menù" aria-controls="voci" aria-expanded="false"><span></span><span></span></button>
</header>'''


FOOTER = f'''<footer>
  <div class="wrap">
    <div class="eyebrow">Su Instagram vedi a cosa lavoriamo. Per tutto il resto, scrivici qui</div>
    <a href="contatti.html" class="mega">Parliamone.</a>
    <div class="foot">
      <div><img src="img/logo-topiko.png" alt="Topiko Lab">Agenzia di comunicazione per PMI</div>
      <nav>{"".join(f'<a href="{h}">{t}</a>' for h, t in VOCI)}<a href="https://www.instagram.com/topikolab/">Instagram</a><a href="https://www.linkedin.com/company/topikolab/">LinkedIn</a><a href="https://www.facebook.com/profile.php?id=61576566621857">Facebook</a></nav>
    </div>
    <div class="foot-legale"><span>Topiko Lab · P.IVA 03058460357</span><a href="privacy.html">Privacy policy</a><a href="cookie.html">Cookie policy</a><button type="button" data-preferenze-cookie>Preferenze cookie</button></div>
  </div>
</footer>'''


import time
VERSIONE = str(int(time.time()))  # cambia a ogni build: il browser riscarica stile e script aggiornati


# Cosa può caricare il sito. L'indirizzo 127.0.0.1 serve solo in prova e viene tolto dalla versione da pubblicare.
CSP = ("default-src 'self'; script-src 'self' https://www.googletagmanager.com https://connect.facebook.net; "
       "style-src 'self' 'unsafe-inline'; font-src 'self'; frame-src https://www.facebook.com; "
       "img-src 'self' data: blob: https://*.googleusercontent.com https://*.cdninstagram.com https://*.fbcdn.net "
       "https://www.facebook.com https://www.googletagmanager.com https://*.google-analytics.com; "
       "connect-src 'self' https://places.googleapis.com https://*.workers.dev https://www.googletagmanager.com "
       "https://*.google-analytics.com https://*.analytics.google.com https://www.facebook.com https://connect.facebook.net http://127.0.0.1:8788; "
       "object-src 'none'; base-uri 'self'; form-action 'self'")


def con_sfumature(mezzo):
    """Dove una sezione scura confina con una chiara (nei due sensi) mette una fascia ferma con la sfumatura fra i due colori.
    Vicino alla fascia finale col gradiente non mette niente: lì resta il taglio netto."""
    trovati = [m for m in re.finditer(r'<(section|footer)\b[^>]*>', mezzo) if 'consenso' not in m.group(0)]
    def tono(m):  # c = chiara, g = fascia finale col gradiente, s = scura
        cl = (re.search(r'class="([^"]*)"', m.group(0)) or [0, ''])[1].split()
        return 'g' if m.group(1) == 'section' and 'cta-fine' in cl else 'c' if m.group(1) == 'section' and 'chiara' in cl else 's'
    def con_classe(tag, cls):
        if re.search(r'class="', tag):
            return re.sub(r'class="([^"]*)"', lambda k: f'class="{k.group(1)} {cls}"', tag, 1)
        return re.sub(r'^<(\w+)', lambda k: f'<{k.group(1)} class="{cls}"', tag, 1)
    def fisso(tag):  # sezioni con altezza e respiro propri
        return any(x in tag for x in ('scena', 'passi-scorri', 'ar-sez', 'class="pil', 'ta-anello', 'clienti'))
    classi, fasce = {}, {}
    for i in range(len(trovati) - 1):
        su, giu = trovati[i], trovati[i + 1]
        if tono(su) == tono(giu) or 'g' in (tono(su), tono(giu)):
            continue
        fasce[i + 1] = f'<div class="sfuma {"sfuma-sc" if tono(su) == "s" else "sfuma-cs"}" aria-hidden="true"></div>\n'
        if not fisso(su.group(0)):
            classi.setdefault(i, []).append('pre-sf')
        if not fisso(giu.group(0)):
            classi.setdefault(i + 1, []).append('post-sf')
    for i in sorted(set(classi) | set(fasce), reverse=True):
        m = trovati[i]
        tag = con_classe(m.group(0), ' '.join(classi[i])) if i in classi else m.group(0)
        mezzo = mezzo[:m.start()] + fasce.get(i, '') + tag + mezzo[m.end():]
    return mezzo


def pagina(nome, titolo, attiva, corpo, scena=False):
    testa = f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo}</title>
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="preload" href="fonts/aileron-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/aileron-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/topiko.css">
</head>
<body>
'''
    piede = f'''
<script src="js/config.js"></script>
<script src="js/consenso.js"></script>
<script src="vendor/gsap.min.js"></script>
<script src="vendor/ScrollTrigger.min.js"></script>
<script src="js/topiko.js"></script>
{'<script src="js/scena.js"></script>' if scena else ''}
<script src="js/leggero.js"></script>
{'<script src="js/servizi.js"></script>' if 'servizi-g' in corpo else ''}{'<script src="js/anello.js"></script>' if 'ta-anello' in corpo else ''}{'<script src="js/arco.js"></script>' if 'id="arco"' in corpo else ''}{'<script src="js/mondo.js"></script>' if 'data-mondo' in corpo else ''}{'<script src="js/portfolio.js"></script>' if 'id="portfolio"' in corpo else ''}{'<script src="js/ruota.js"></script>' if 'id="rot"' in corpo else ''}{'<script src="vendor/matter.min.js"></script><script src="js/pillole.js"></script>' if 'id="pil"' in corpo else ''}{'<script src="js/passi.js"></script>' if 'id="come-lavoriamo"' in corpo else ''}
{'<script src="js/entra.js"></script>' if 'data-entra' in corpo else ''}
{'<script src="js/recensioni.js"></script>' if 'recensioni-google' in corpo else ''}
{'<script src="js/valuta.js"></script>' if 'id="valuta"' in corpo else ''}
<script src="js/vetro.js"></script>
</body>
</html>
'''
    corpo = corpo.replace('<form onsubmit="return false">', '<form>')
    for vecchio, nuovo in SOST:
        corpo = corpo.replace(vecchio, nuovo)
    # foto: dove c'è la versione leggera usa quella
    corpo = re.sub(r"img/([\w-]+)\.jpg", lambda m: f"img/{m.group(1)}.webp" if (QUI / f"img/{m.group(1)}.webp").exists() else m.group(0), corpo)
    corpo = corpo.replace("Ho letto l'informativa privacy", 'Ho letto l\'<a href="privacy.html" target="_blank" style="text-decoration:underline">informativa privacy</a>')
    piede_pag = FOOTER
    if nome == "contatti.html":  # nei Contatti il modulo è già lì: via l'invito "Parliamone." in fondo (26/11, Bryan)
        piede_pag = re.sub(r'\s*<div class="eyebrow">Su Instagram.*?</div>\s*<a href="contatti.html" class="mega">Parliamone.</a>', '', FOOTER, count=1, flags=re.S)
    html = testa + nav(attiva) + "\n" + con_sfumature(corpo + "\n" + piede_pag) + piede
    html = re.sub(r'((?:href|src)="(?:css|js)/[a-z]+\.(?:css|js))"', r'\1?v=' + VERSIONE + '"', html)
    (QUI / nome).write_text(html, encoding="utf-8")


def ph_hero(eyebrow, riga1, riga2, lead, risalto=True):
    return f'''<section class="ph-hero">
  <div class="blob b1"></div><div class="blob b2"></div>
  <div class="wrap">
    <div class="eyebrow h-in">{eyebrow}</div>
    <h1><span class="riga"><span>{riga1}</span></span>{f'<span class="riga"><span>{f'<span class="grad-t">{riga2}</span>' if risalto else riga2}</span></span>' if riga2 else ''}</h1>
    <p class="lead h-in">{lead}</p>
  </div>
</section>'''


CTA_FINE = f'''<section class="cta-fine">
  <div class="wrap">
    <div class="vbox rv">
      <div><div class="eyebrow">Il prossimo passo</div><h2>Parlaci della tua azienda.</h2></div>
      <a class="btn btn-v mag" href="contatti.html">Scrivici {FRECCIA}</a>
    </div>
  </div>
</section>'''

# sezioni prese dalla bozza
import struct
def _dim_png(f):
    # larghezza e altezza di un PNG, lette dall'intestazione
    with open(QUI / f"img/clienti/{f}.png", "rb") as fp:
        return struct.unpack(">II", fp.read(24)[16:24])
scena, _ = tra('<section class="scena"', "</section>")
# fascia "Lavoriamo con": per togliere o aggiungere un cliente basta questa lista (nome, file, altezza in px)
LOGHI = [("Tecnoproject", "tecnoproject", 62), ("Gapor", "gapor", 30), ("Koloro", "koloro", 50),
         ("Unimotor", "unimotor", 26), ("Il Porto", "ilporto", 48), ("Sfojart", "sfojart", 50)]
loghi_html = "".join(
    "".join(f'<span class="lg" role="img" aria-label="{n}"' if giro == 0 else f'<span class="lg" aria-hidden="true"'
            + f' style="height:{h}px;width:{round(h * _dim_png(f)[0] / _dim_png(f)[1])}px;--m:url(../img/clienti/{f}.png)"></span>' for n, f, h in LOGHI)
    for giro in range(4))  # si ripete: la fascia scorre di metà della sua larghezza e riparte senza salti
clienti = f'''<section class="clienti" aria-label="Clienti">
  <div class="lab">Alcuni dei nostri clienti</div>
  <div class="track loghi">{loghi_html}</div>
</section>'''
casi, _ = tra('<section class="casi"', "</section>")
proposta, _ = tra('<section class="proposta"', "</section>")
valuta, _ = tra('<section class="valuta"', "</section>")
MAPS = "https://www.google.com/maps/place/Topiko+lab/@44.6986948,10.4424187,17z/data=!4m8!3m7!1s0x4780111272d00c4f:0x8bcaed3398cb4b48!8m2!3d44.6986948!4d10.4424187!9m1!1b1!16s%2Fg%2F11xdtfkbgk"
rec = f"""<section class="rec chiara">
  <div class="wrap">
    <div class="eyebrow rv">Recensioni</div>
    <h2 class="big rv" style="margin-top:20px">Cosa dicono <span class="grad-t">i clienti</span></h2>
    <a class="google-voto rv" href="{MAPS}"><span class="g">G</span><span class="stelle">★★★★★</span><span>Recensioni Google</span></a>
  </div>
  <!-- fascia che scorre: le schede vengono riempite dal widget collegato alla scheda Google (Trustindex o API Google Places) -->
  <div class="rec-scorre" id="recensioni-google" aria-label="Recensioni Google">
    <div class="rec-track">{"".join('<div class="rec-card vuota"><div class="testa"><i></i><div><b></b><span class="stelle">★★★★★</span></div><span class="g">G</span></div><p></p><p></p><p class="corta"></p></div>' for _ in range(12))}</div>
  </div>
</section>"""

for a, b in [('href="#contatti"', 'href="contatti.html"'), ('href="#valuta"', 'href="analisi.html"')]:
    scena = scena.replace(a, b)
scena = re.sub(r'\s*<div class="step [^>]*>.*?</div>', '', scena, flags=re.S)
scena = re.sub(r'\s*<div class="prog">.*?</div>', '', scena, flags=re.S)
# titolo della home come nel Figma (26/11): a sinistra, senza etichetta, "topic giusto." in Bitcount col gradiente
for a, b in [('      <div class="eyebrow h-in">Agenzia di comunicazione per PMI</div>\n', ''),
             ('<span>Il tuo brand,</span>', '<span>Il tuo brand</span>'),
             ('nel <em>topic giusto.</em>', 'nel <em class="grad-t">topic giusto.</em>'),
             ('Seguiamo la comunicazione delle piccole e medie imprese, dai social alle fiere. Parli con una persona sola, che conosce la tua azienda e coordina chi ci lavora.', 'Un referente unico per tutta la comunicazione della tua azienda.'),
             ('Parliamo del tuo progetto', 'Raccontaci la tua azienda'),
             ('Fai valutare il tuo profilo</a>', 'Analizziamo il tuo sito, gratis</a>')]:
    assert a in scena, a
    scena = scena.replace(a, b)

# card della home con il link al caso
CASI = {"Gapor": "caso-gapor.html", "Insmile": "caso-insmile.html", "Koloro": "caso-koloro.html"}
for nome_c, pag in CASI.items():
    casi = re.sub(rf'(<span class="chip">{nome_c} ·[^<]*</span>.*?<div class="kpi">.*?</div>\s*</div>)',
                  lambda mm: mm.group(1) + f'\n          <a class="leggi" href="{pag}">Leggi il caso</a>', casi, count=1, flags=re.S)
casi = casi.replace('<p>I numeri vengono dagli account dei clienti e sono arrotondati per difetto.</p>',
                    f'<p>I numeri vengono dagli account dei clienti e sono arrotondati per difetto.<br><a class="link-tutti" href="casi-studio.html">I nostri lavori {FRECCIA}</a></p>')
proposta_home = proposta.replace('</div>\n  </div>\n</section>', f'</div>\n    <a class="link-tutti rv" href="servizi.html">Tutti i servizi e come lavoriamo {FRECCIA}</a>\n  </div>\n</section>')
valuta_home = valuta

# ---------- servizi: un posto solo per i testi ----------
ICO = {
 "strategia": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/>',
 "analisi": '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/>',
 "brand": '<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h11"/>',
 "cataloghi": '<path d="M4 5h7v15H4zM13 5h7v15h-7z"/>',
 "social": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m10 9 5 3-5 3z"/>',
 "shooting": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
 "grafica": '<path d="m4 20 4-1L19 8l-3-3L5 16z"/><path d="m14 7 3 3"/>',
 "meta": '<path d="M4 19V9M10 19V5M16 19v-7M22 19H2"/>',
 "google": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/><path d="M8 11h6"/>',
 "sito": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18"/>',
 "blog": '<path d="M5 4h14v16H5z"/><path d="M8 8h8M8 12h8M8 16h5"/>',
 "seo": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
 "amazon": '<path d="M3 7h18l-2 12H5z"/><path d="M8 7a4 4 0 0 1 8 0"/>',
 "email": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 "ai": '<path d="M12 3l2 6 6 2-6 2-2 6-2-6-6-2 6-2z"/>',
}
# I servizi: una voce per servizio. Da qui si aggiornano schede dei Servizi, elenco in home, mondo 3D e pillole che cadono.
# (chiave, nome, frase breve, "Cosa facciamo" (lista, anche vuota), "Come funziona" (frase o None), caso (o None))
# Le frasi vengono dalle schede raggruppate di prima: niente di nuovo. Andranno sostituite dai testi del Figma.
COME_STRATEGIA = "Partiamo dai tuoi clienti e da quello che dicono i concorrenti. Scriviamo il piano e lo discutiamo con te. Poi cataloghi, grafiche e contenuti usano tutti gli stessi messaggi."
COME_SOCIAL = "Ogni mese ti mandiamo il piano dei contenuti. Tu lo approvi, poi pubblichiamo. A fine mese guardiamo insieme cosa ha funzionato."
COSA_INSERZIONI = ["Campagne che portano richieste di preventivo o ordini.", "Testi e grafiche delle inserzioni.", "Un report breve ogni mese, con parole semplici."]
COME_INSERZIONI = "Decidiamo con te l'obiettivo: richieste o ordini. Poi misuriamo quello. Ogni mese ti spieghiamo cosa abbiamo cambiato e perché."
COME_SITO = "Partiamo dalle domande che i clienti fanno davvero. Su quelle scriviamo pagine e articoli. Poi guardiamo le visite e le richieste che arrivano dal sito."
SERVIZI = [
 ("strategia", "Strategia di comunicazione", "Prima ti ascoltiamo. Poi decidiamo con te a chi parlare, con quale voce e su quali canali.", [], COME_STRATEGIA, None),
 ("analisi", "Analisi di mercato e concorrenti", "Analisi del mercato e dei concorrenti.", [], COME_STRATEGIA, None),
 ("brand", "Brand book e voce del marchio", "Messaggi, voce del marchio e brand book.", [], COME_STRATEGIA, None),
 ("cataloghi", "Cataloghi e grafiche", "Cataloghi e grafiche costruiti sulla stessa strategia.", [], COME_STRATEGIA, None),
 ("social", "Gestione social", "Piano editoriale, foto, video e grafiche per i tuoi profili. Riprese e montaggio sono nostri.", [], COME_SOCIAL,
  ("Koloro · caffè bistrot a Parma", "oltre 600.000", "visualizzazioni su Instagram e Facebook in 113 giorni")),
 ("shooting", "Shooting foto e video", "Foto e video girati da noi nella tua azienda.", [], COME_SOCIAL, None),
 ("grafica", "Grafiche e animazioni", "Grafiche e animazioni per post, storie e reel.", [], COME_SOCIAL, None),
 ("meta", "Inserzioni Meta", "Campagne su Facebook e Instagram, valutate sulle richieste e sulle vendite.", COSA_INSERZIONI, COME_INSERZIONI,
  ("Gapor · scale su misura", "123", "richieste di preventivo in cinque settimane")),
 ("google", "Google Ads", "Campagne su Google, valutate sulle richieste e sulle vendite.", COSA_INSERZIONI, COME_INSERZIONI, None),
 ("sito", "Sito web", "Un sito chiaro e veloce, pensato per ricevere richieste.", [], COME_SITO, None),
 ("blog", "Blog", "Articoli del blog che rispondono alle domande dei tuoi clienti.", [], COME_SITO, None),
 ("seo", "SEO e GEO", "Pagine scritte per essere trovate su Google (SEO) e citate da ChatGPT e simili (GEO).", [], COME_SITO, None),
 ("amazon", "Amazon e Amazon Ads", "Schede prodotto, contenuti A+ e inserzioni su Amazon.",
  ["Titoli, testi e foto delle schede prodotto.", "Contenuti A+, cioè le immagini e i testi lunghi sotto la scheda.", "Inserzioni su Amazon (Amazon Ads)."],
  "Guardiamo le tue schede e cosa cercano i clienti su Amazon. Rifacciamo le schede, poi accendiamo le inserzioni. Ogni mese controlliamo le vendite.", None),
 ("email", "Email e newsletter", "Raccolta contatti, newsletter e email automatiche per chi è vicino all'acquisto.",
  ["Un modulo per raccogliere i contatti.", "Una newsletter con un ritmo che decidiamo insieme.", "Email automatiche, con i dati su chi le apre e chi clicca."],
  "Costruiamo la lista dei contatti. Scriviamo e programmiamo le email. Ti diciamo chi ha letto e chi ha cliccato, così sai chi chiamare.", None),
 ("ai", "Contenuti con l'AI", "Foto e video creati con l'intelligenza artificiale, partendo dai tuoi prodotti.",
  ["Foto del prodotto in ambienti difficili da fotografare.", "Video brevi per social e inserzioni.", "Più versioni dello stesso contenuto, nei formati che servono."],
  "Ci mandi le foto del prodotto o l'idea. Noi prepariamo immagini e video. Controlliamo ogni contenuto prima di mandartelo. Tu dici cosa cambiare prima dell'uso.", None),
]
# etichette corte per le pillole del mondo e per quelle che cadono
CORTI = {"strategia": "Strategia", "analisi": "Analisi", "brand": "Brand book", "cataloghi": "Cataloghi", "social": "Social", "shooting": "Shooting",
         "grafica": "Grafica", "meta": "Meta Ads", "google": "Google Ads", "sito": "Sito", "blog": "Blog", "seo": "SEO e GEO",
         "amazon": "Amazon", "email": "Email", "ai": "AI"}


def icona(k):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">{ICO[k]}</svg>'


def scheda_servizio(k, tit, chiuso, punti, come, caso_s):
    piccolo = f'<div class="s-caso"><small>{caso_s[0]}</small><strong>{caso_s[1]}</strong><span>{caso_s[2]}</span></div>' if caso_s else ""
    return f"""<details class="servizio rv" id="{k}">
      <summary><span class="ico">{icona(k)}</span><span class="s-testa"><span class="s-nome">{tit}</span><span class="s-breve">{chiuso}</span></span><span class="s-piu" aria-hidden="true"></span></summary>
      <div class="s-dett{' con-caso' if caso_s else ''}">
        {f'<div><h4>Cosa facciamo</h4><ul>{"".join(f"<li>{p}</li>" for p in punti)}</ul></div>' if punti else ''}
        {f'<div><h4>Come funziona</h4><p>{come}</p></div>' if come else ''}
        {piccolo}
        <button type="button" class="s-chiudi">Chiudi</button>
      </div>
    </details>"""


pillole_mondo = "".join(f'<a class="m-p" data-k="{k}" data-i="{i}" href="servizi.html" aria-label="{tit}"><span class="u-ico">{icona(k)}</span>{CORTI[k]}</a>' for i, (k, tit, *_r) in enumerate(SERVIZI))
# il mondo dei servizi: sfera di punti col gradiente che gira, logo fermo al centro, pillole agganciate con un filo (js/mondo.js)
RUOTA = f"""<div class="mondo rv" data-mondo role="group" aria-label="Topiko Lab al centro, i servizi intorno">
      <canvas aria-hidden="true"></canvas>
      <div class="m-logo"><img src="img/logo-topiko.png" alt="Topiko Lab"></div>
      {pillole_mondo}
    </div>"""
# elenco della home: nome e descrizione presi parola per parola dalle schede dei Servizi
elenco_servizi = "".join(f'<li><a class="hs-voce" data-k="{k}" href="servizi.html" title="{chiuso}"><span class="hs-ico">{icona(k)}</span><b>{tit}</b></a></li>' for k, tit, chiuso, *_r in SERVIZI)

# testi presi dalla prima bozza e riscritti
SOST = [
 ("Seguiamo la comunicazione delle piccole e medie imprese, dai social alle fiere. Parli con una persona sola, che conosce la tua azienda e coordina chi ci lavora.",
  "Social, sito, brochure e foto con un solo messaggio."),
 ("<h3>Ascoltiamo</h3><p>Una call con te e un'analisi di come comunichi oggi.</p>", "<h3>Partiamo da te</h3><p>Cosa vendi, a chi e perché ti scelgono.</p>"),
 ("<h3>Scriviamo la strategia</h3><p>Obiettivi, pubblici, messaggi e calendario, su carta prima di partire.</p>", "<h3>Troviamo il messaggio</h3><p>La frase che ti presenta.</p>"),
 ("<h3>Produciamo</h3><p>Contenuti, campagne e materiali per fiere e punti vendita.</p>", "<h3>Lo portiamo ovunque</h3><p>Social, sito, brochure e foto parlano uguale.</p>"),
 ("<h3>Misuriamo</h3><p>Ogni mese guardiamo insieme i numeri e decidiamo cosa cambiare.</p>", "<h3>Ogni mese lo misuriamo</h3><p>Ti mostriamo cosa ha funzionato e cosa cambiamo.</p>"),
 ("Il titolare di una PMI fa già dieci lavori. Noi gli togliamo l'undicesimo: social, inserzioni, sito, fiere e packaging passano da una persona sola, che conosce l'azienda.",
  "Diamo alla tua azienda coerenza e una linea editoriale. Lo stesso messaggio, dal primo post all'ultima brochure."),
 ("<h3>Chi ristruttura casa ha visto come nasce una scala Gapor</h3>", "<h3>Far vedere come nasce una scala a chi ristruttura casa</h3>"),
 ("I contenuti raccontano l'officina e il mestiere. Le inserzioni portano le richieste di preventivo da dieci province.", "Con i contenuti abbiamo raccontato l'officina e il mestiere. Con le inserzioni abbiamo portato richieste di preventivo."),
 ("<small>persone raggiunte</small>", "<small>persone hanno visto le inserzioni</small>"),
 ("<h3>Un marchio nato da zero e un negozio online che vende</h3>", "<h3>Brand book, contenuti e campagne per un negozio online</h3>"),
 ("Abbiamo costruito il brand book, i contenuti e le campagne. Nel primo mese di inserzioni il sito ha cominciato a ricevere ordini con regolarità.", "Abbiamo scritto il brand book, girato i video con l'igienista e impostato le campagne. Nel primo mese di campagne gli ordini sul sito sono passati da 3 a 33."),
 ("<small>ordini al mese</small>", "<small>ordini nel primo mese di campagne</small>"),
 ("<h3>Da bacheca di volantini a profilo che si riconosce senza leggere il nome</h3>", "<h3>Dalle locandine ai piatti: un profilo che si riconosce</h3>"),
 ("Abbiamo scelto un font e una palette calda, e scriviamo con il tono lento del locale. Foto e video li facciamo noi, nel locale.", "Il profilo era una raccolta di locandine, ognuna diversa dall'altra. Abbiamo scelto colori e carattere uguali per tutti i post. Foto e video di piatti e sala li abbiamo girati nel locale."),
 ("<h3>Perché comprare da un installatore e non da un altro</h3>", "<h3>Uscire dalla guerra dei prezzi</h3>"),
 ("Abbiamo studiato nove concorrenti della zona e le domande che le persone fanno nei commenti. Su quello abbiamo scritto il brand book e impostato le campagne.", "Quasi tutti i concorrenti competono sul prezzo. Abbiamo costruito la strategia per far scegliere Tecnoproject per la competenza."),
 ("Mandaci il link del tuo profilo Instagram. Ti rispondiamo con un punteggio e le prime cose da sistemare, poi se vuoi ne parliamo in una call.", "Il tempo di un caffè per compilare. Il report lo mettiamo in forno noi: entro 24 ore hai il voto su 100."),
 ("Il link del profilo Instagram dell'azienda e una mail a cui risponderti.", "Ci scrivi il nome dell'azienda, il profilo Instagram e un'email per la risposta."),
 ("Bio, griglia, contenuti e numeri, con lo stesso metodo che usiamo per i clienti.", "Controlliamo la bio, i contenuti pubblicati e i numeri del profilo."),
 ("Un punteggio su 100 e le prime cose da sistemare.", "Ti arriva un voto su 100 e le prime cose da sistemare."),
 ("<h3>Se vuoi, ne parliamo</h3><p>Una call per capire da dove partire.</p>", "<h3>Ne parliamo, se vuoi</h3><p>Una call per capire da dove cominciare.</p>"),
 ("Raccontaci cosa fa la tua azienda e cosa vorresti cambiare nella comunicazione.", "Scrivici cosa fa la tua azienda e cosa vuoi cambiare nella comunicazione. Ti rispondiamo noi."),
 ("I numeri vengono dagli account dei clienti e sono arrotondati per difetto.", "Qui raccontiamo cosa abbiamo fatto noi e cosa è successo dopo. I numeri vengono dagli account dei clienti."),
]

# ---------- pagine ----------
def scheda_lavoro(l):
    foto = f"<div class=\"ph\" style=\"background-image:url('img/{l['foto']}');background-position:{l.get('pos', 'center')}\"></div>" if l.get("foto") else ""
    num = f'<strong data-to="{l["to"]}" data-pre="{l.get("pre", "")}">{l.get("pre", "")}{l["vis"]}</strong><small>{l["lab"]}</small>' if l.get("to") else f'<small>{l["lab"]}</small>'
    return f"""<a class="lavoro{' pieno' if not l.get('foto') else ''}" href="{l['url']}">{foto}<div class="l-t"><div class="l-num">{num}</div><div class="l-det"><span>{l['chip']}</span><h3>{l['tit']}</h3><em>{l['azione']} {FRECCIA}</em></div></div></a>"""


LAVORI = [
 dict(url="caso-gapor.html", foto="gapor-grande.webp", pos="center 62%", to=123, vis="123", lab="richieste di preventivo in cinque settimane", chip="Gapor · scale su misura", tit="Far vedere come nasce una scala a chi ristruttura casa", azione="Leggi il caso"),
 dict(url="caso-insmile.html", foto="insmile.jpg", to=33, pre="3 → ", vis="33", lab="ordini nel primo mese di campagne", chip="Insmile · sbiancamento dentale", tit="Brand book, contenuti e campagne per un negozio online", azione="Leggi il caso"),
 dict(url="caso-koloro.html", foto="koloro.jpg", to=600000, pre="oltre ", vis="600.000", lab="visualizzazioni in 113 giorni", chip="Koloro · caffè bistrot a Parma", tit="Dalle locandine ai piatti: un profilo che si riconosce", azione="Leggi il caso"),
 dict(url="contatti.html", lab="la nuova strategia, in corso", chip="Tecnoproject · clima e riscaldamento", tit="Una strategia per farsi scegliere per la competenza", azione="Parliamone"),
]
schede_lavori = "".join(scheda_lavoro(l) for l in LAVORI)

# casi in home: fila di pannelli verticali (schema della copertina "index-3" di Onovo, mai lime).
# Ogni caso ha un pannello che diventa largo quando è attivo, più 2-3 strisce strette con altri lavori dello stesso cliente.
STRISCE = {"Gapor": ["portfolio/gapor-scala-luci.webp", "portfolio/gapor-chiocciola.webp", "portfolio/gapor-legno.webp"],
           "Insmile": ["portfolio/insmile-azzurro.webp", "portfolio/insmile-macchie.webp"],
           "Koloro": ["portfolio/koloro-bowl.webp", "portfolio/koloro-cannoncini.webp", "portfolio/koloro-bartender.webp"]}
def _numero(l):
    return f'{l.get("pre", "")}{l["vis"]}' if l.get("vis") else ""
def _link_home(l):
    return "casi-studio.html" if l["url"] == "contatti.html" else l["url"]
pannelli = ""
for i, l in enumerate(LAVORI):
    cliente = l["chip"].split(" · ")[0]
    media = (f'<img src="img/{l["foto"]}" alt="" loading="lazy" decoding="async" style="object-position:{l.get("pos", "center")}">' if l.get("foto")
             else f'<span class="fp-parola">{l.get("parola", cliente)}</span>')
    pannelli += f'<a class="fp-p fp-main{" on" if i == 0 else ""}" data-caso="{i}" href="{_link_home(l)}" aria-label="{cliente}: {l["tit"]}">{media}</a>'
    for j, f in enumerate(STRISCE.get(cliente, [])):
        pannelli += f'<a class="fp-p fp-str fp-s{j % 3}" data-caso="{i}" href="{_link_home(l)}" tabindex="-1" aria-hidden="true"><img src="img/{f}" alt="" loading="lazy" decoding="async"></a>'
didascalie = "".join(
    f'<div class="fp-cap{" on" if i == 0 else ""}" data-caso="{i}" aria-hidden="{"false" if i == 0 else "true"}"><span class="fp-et">{l["chip"]}</span>'
    f'<p class="fp-num">{f"<strong>{_numero(l)}</strong> " if _numero(l) else ""}<span>{l["lab"]}</span></p>'
    f'<a class="fp-tit" href="{_link_home(l)}">{l["tit"]}</a></div>' for i, l in enumerate(LAVORI))
home_casi = f"""<section class="sezione casi-sez casi-fila" aria-roledescription="carosello" aria-label="Casi studio">
  <div class="wrap">
    <div class="casi-testa">
      <div>
        <div class="eyebrow rv">Casi studio</div>
        <h2 class="big rv">Storie vere<br><span class="grad-t">con numeri veri</span></h2>
      </div>
      <a class="btn btn-g casi-tutti rv" href="casi-studio.html">Tutti i nostri lavori {FRECCIA}</a>
    </div>
  </div>
  <div class="fp-vista rv"><div class="fp-track">{pannelli}</div></div>
  <div class="wrap fp-sotto">
    <button type="button" class="fp-freccia fp-prima" aria-label="Caso precedente"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></button>
    <div class="fp-caps" aria-live="polite">{didascalie}</div>
    <button type="button" class="fp-freccia fp-dopo" aria-label="Caso successivo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
  </div>
</section>"""
home_entra = f"""<section class="entra" data-entra="seq-computer:48" aria-label="I numeri">
  <div class="entra-palco"><canvas></canvas>
    <div class="entra-testo"><h2>I numeri<br>li guardiamo con te</h2><a class="btn btn-g" href="casi-studio.html">Guarda i casi studio {FRECCIA}</a></div>
  </div>
</section>"""
home_servizi = f"""<section class="sezione home-servizi">
  <div class="wrap hs-griglia">
    <div class="hs-tit">
      <div class="eyebrow rv">Cosa facciamo</div>
      <h2 class="big rv" style="margin-top:20px">Il nostro lavoro fa parte<br><span class="grad-t">del vostro mondo</span></h2>
    </div>
    {RUOTA}
    <ul class="hs-elenco rv">{elenco_servizi}</ul>
    <div class="u-azione rv"><a class="btn btn-v mag" href="servizi.html">Guarda i servizi {FRECCIA}</a></div>
  </div>
</section>"""
# stessa ruota nei Servizi, da sola: titolo ed elenco li danno già l'apertura e le schede
# nei Servizi la stessa sezione della home (elenco a sinistra, mondo a destra), senza il bottone "Guarda i servizi"
# nei Servizi le voci non portano altrove: si accendono e basta (le schede sotto al mondo sono state tolte il 26/11)
ruota_servizi = re.sub(r'\s*<div class="u-azione rv">.*?</div>', '', home_servizi, count=1, flags=re.S).replace(' href="servizi.html"', '').replace('class="sezione home-servizi"', 'class="sezione home-servizi chiara"', 1)
home_squadra = f"""<section class="sezione" style="padding-top:0">
  <div class="wrap">
    <a class="squadra-foto rv" href="chi-siamo.html">
      <div class="ph" style="background-image:url('img/gruppo.jpg')"></div>
      <div class="t"><div class="eyebrow">Chi siamo</div><h2>Davide, Bryan, Chiara, Barbara e Fabio</h2><span class="link-tutti" style="margin-top:14px">Conosci la squadra {FRECCIA}</span></div>
    </a>
  </div>
</section>"""
home_analisi = f"""<section class="cta-fine">
  <div class="wrap">
    <div class="vbox rv">
      <div><div class="eyebrow">Analisi gratuita</div><h2>Ad oggi, come parla la tua azienda online?</h2><p>Il tempo di un caffè per compilare. Il report lo inviamo noi dal laboratorio.</p></div>
      <a class="btn btn-v mag" href="analisi.html">Per l'analisi gratuita di qua {FRECCIA}</a>
    </div>
  </div>
</section>"""
# arco di lavori (prova approvata in prove/arco-lavori/): 9 card sul raggio di un cerchio, i video girano solo a schermo (js/arco.js). Immagini e clip in img/arco/
ARCO = [("parmapast-ravioli", "Piatto di ravioli di Natale, per Parma Past", "Shooting", False),
        ("farneto-gabian", "Etichetta animata Gabiàn, per Il Farneto", "Motion", True),
        ("koloro-cannoncini", "Post dei cannoncini, per Koloro", "Social", False),
        ("gapor-scala", "Scala sospesa con le luci, per Gapor", "Foto", False),
        ("insmile-menta", "Dentifricio con foglie di menta, per Insmile", "Reel", True),
        ("farneto-bottiglia", "Bottiglia nella penombra, per Il Farneto", "Video", True),
        ("koloro-bowl", "Bowl Fit con le ombre delle mani, per Koloro", "Grafica", False)]
def carta_arco(i, f, alt, et, video):
    v = (f'<video muted loop playsinline preload="none" poster="img/arco/{f}.jpg" aria-hidden="true">'
         f'<source src="img/arco/{f}.webm" type="video/webm"><source src="img/arco/{f}.mp4" type="video/mp4"></video>') if video else ""
    lazy = ' loading="lazy"' if i in (0, 6) else ""
    return (f'<li class="ar-c" style="--i:{i}"><a class="ar-f" href="casi-studio.html#portfolio"><img src="img/arco/{f}.jpg" alt="{alt}" width="600" height="750" decoding="async"{lazy}>'
            f'{v}<span class="ar-l">{et}</span></a></li>')
home_arco = f"""<section class="ar-sez chiara" id="arco" aria-label="Alcuni nostri lavori">
  <div class="ar-palco"><ul class="ar-arco">{"".join(carta_arco(i, *x) for i, x in enumerate(ARCO))}</ul></div>
  <div class="wrap ar-dopo">
    <p class="ar-pre rv">Siamo un piccolo laboratorio creativo in Emilia.</p>
    <h2 class="big rv">Abbastanza grande per seguire tutto, abbastanza piccolo <span class="grad-t">per conoscerti per nome.</span></h2>
    <div class="ar-azioni rv"><a class="btn btn-g" href="chi-siamo.html">Scopri che facce abbiamo {FRECCIA}</a><a class="link-tutti" href="contatti.html">Parlaci dei tuoi obiettivi {FRECCIA}</a></div>
  </div>
</section>"""
# alternanza della home: apertura S, arco C, casi S, ruota C, recensioni S, fascia finale C, footer S
home_casi_s = home_casi
home_servizi_c = home_servizi  # scura: in home l'unico blocco chiaro è l'arco
rec_s = rec.replace('<section class="rec chiara">', '<section class="rec">', 1).replace('Cosa dicono <span class="grad-t">i clienti</span>', 'La nostra <span class="grad-t">pagella</span>', 1)
home_analisi_c = home_analisi
pagina("index.html", "Topiko Lab", "index.html",
       "\n".join([scena, clienti, home_arco, home_casi_s, home_servizi_c, rec_s, home_analisi_c]), scena=True)

# come lavoriamo: passi della pagina Servizi, con la curva che si accende scorrendo (js/passi.js)
PASSI = [("Ti ascoltiamo", "Ci racconti la tua azienda e cosa vuoi ottenere. Prima di proporre qualcosa guardiamo sito, social e inserzioni di oggi."),
         ("Scriviamo la linea", "Scriviamo a chi parlare e con quale voce. Lo leggi e lo correggi con noi."),
         ("Produciamo", "Prepariamo contenuti, campagne e materiali."),
         ("Il controllo mensile", "Guardiamo i numeri insieme. Teniamo quello che funziona e cambiamo il resto. E tranquillo: dopo la consegna non sparisce nessuno.")]
come_lavoriamo = f"""<section class="passi-scorri" id="come-lavoriamo">
  <div class="ps-pin">
    <div class="wrap ps-alto">
      <div class="ps-sx"><div class="eyebrow">Come lavoriamo</div><h2>Ogni progetto è l'inizio di un percorso.<br><span class="grad-t">ti portiamo dove vuoi arrivare.</span></h2></div>
      <div class="ps-dx">
        <div class="ps-tab" role="tablist" aria-label="Passi">{"".join(f'<button type="button" role="tab" aria-selected="{str(i == 0).lower()}">{t}</button>' for i, (t, _) in enumerate(PASSI))}</div>
        <div class="ps-testi">{"".join(f'<article{" class=on" if i == 0 else ""}><h3>{t}</h3><p>{d}</p></article>' for i, (t, d) in enumerate(PASSI))}</div>
      </div>
    </div>
    <div class="wrap"><div class="ps-curva" aria-hidden="true">
      <div class="ps-fasce">{"".join(f'<div{" class=on" if i == 0 else ""}><b>0{i + 1}</b></div>' for i in range(len(PASSI)))}</div>
      <svg viewBox="0 0 1000 300" preserveAspectRatio="none"><defs><linearGradient id="ps-grad" x1="0" x2="1"><stop offset="0" stop-color="#FF9E03"/><stop offset=".44" stop-color="#E10AE9"/><stop offset="1" stop-color="#FFE3F6"/></linearGradient><clipPath id="ps-taglio"><rect x="0" y="-20" width="0" height="340"/></clipPath></defs><path class="base"/><path stroke="url(#ps-grad)" clip-path="url(#ps-taglio)"/></svg>
      {"".join(f'<i class="ps-punto"><span>{t}</span></i>' for t, _ in PASSI)}
    </div></div>
  </div>
</section>"""

servizi_corpo = f"""<section class="pil" id="pil" aria-labelledby="pil-t">
  <div class="pil-tit" id="pil-tit">
    <div class="eyebrow">Cosa facciamo</div>
    <h1 id="pil-t">Ogni lavoro inizia<br><span class="grad-t bit">facendo chiarezza</span></h1>
  </div>
  <div class="pil-campo" id="pil-campo" aria-hidden="true" data-eti="{'|'.join(CORTI[k].upper() for k, *_r in SERVIZI)}"></div>
  <ul class="pil-sr">
    {"".join(f"<li>{tit}</li>" for _k, tit, *_r in SERVIZI)}
  </ul>
</section>"""
servizi_corpo += f'''
{ruota_servizi}
{come_lavoriamo}
<section class="sezione frase-grande">
  <div class="wrap"><p class="rv">Non importa da dove inizi, davanti a te c'è una persona sola ma dietro c'è <span class="grad-t">una squadra</span>, pronta ad accompagnarti.</p></div>
</section>
{CTA_FINE.replace('<h2>Parlaci della tua azienda.</h2>', '<h2>Fin qui abbiamo raccontato noi. Ora tocca a te.</h2>', 1)}'''
pagina("servizi.html", "Servizi · Topiko Lab", "servizi.html", servizi_corpo)

# elenco casi: le stesse card della home, una sotto l'altra
rail = casi[casi.index('<div class="rail">') + len('<div class="rail">'):casi.rindex('</div>\n  </div>\n</section>')]
rail = re.sub(r'<span class="n">\d+ / \d+</span>', '', rail)
rail = re.sub(r'<article class="card solo">(?:(?!</article>).)*?Pranzo Qui.*?</article>', '', rail, flags=re.S)
rail = rail.replace("url('img/gapor.jpg')", "url('img/gapor-grande.webp')")
# Portfolio (pagina I nostri lavori): solo i contenuti più belli. File leggeri in img/portfolio/ (foto webp 800 px, video mp4+webm 540 px con poster).
# (file, cliente, tipo, formato: "v" 9:16, "r" 4:5, "q" quadrato, video sì/no). L'ordine alterna i clienti.
PF = [("koloro-panino", "Koloro", "Video", "v", True), ("parmapast-cucchiaio", "Parma Past", "Shooting", "q", False),
      ("farneto-gabian", "Il Farneto", "Motion", "v", True), ("gapor-scala-luci", "Gapor", "Social", "r", False),
      ("insmile-macchie", "Insmile", "Reel", "v", True), ("koloro-bowl", "Koloro", "Social", "r", False),
      ("parmapast-aperitivo", "Parma Past", "Shooting", "r", False), ("farneto-inverno", "Il Farneto", "Video", "v", True),
      ("gapor-chiocciola", "Gapor", "Social", "r", False), ("insmile-azzurro", "Insmile", "Reel", "v", True),
      ("koloro-cannoncini", "Koloro", "Social", "r", False), ("parmapast-tortelli", "Parma Past", "Shooting", "r", False),
      ("farneto-berzmain", "Il Farneto", "Motion", "v", True), ("gapor-g8", "Gapor", "Video", "v", True),
      ("koloro-bartender", "Koloro", "Social", "r", False), ("parmapast-natale", "Parma Past", "Shooting", "r", False),
      ("farneto-vendemmia", "Il Farneto", "Video", "v", True), ("gapor-legno", "Gapor", "Social", "q", False),
      ("koloro-cucina", "Koloro", "Video", "v", True), ("parmapast-ravioli", "Parma Past", "Shooting", "q", False),
      ("farneto-brut", "Il Farneto", "Motion", "v", True), ("gapor-scala-ferro", "Gapor", "Foto", "r", False)]
def carta_pf(f, cliente, tipo, fmt, video):
    et = f"{cliente} · {tipo}"
    if video:
        media = (f'<video muted loop playsinline preload="none" poster="img/portfolio/{f}.webp" aria-hidden="true">'
                 f'<source src="img/portfolio/{f}.webm" type="video/webm"><source src="img/portfolio/{f}.mp4" type="video/mp4"></video>')
    else:
        media = f'<img src="img/portfolio/{f}.webp" alt="{et}" loading="lazy" decoding="async">'
    return (f'<figure class="pf-c pf-{fmt} rv"><button type="button" class="pf-apri" aria-label="Apri {et} a schermo grande">{media}</button>'
            f'<figcaption class="pf-et">{et}</figcaption></figure>')
PORTFOLIO = f"""<section class="sezione portfolio" id="portfolio">
  <div class="wrap">
    <div class="eyebrow rv">Portfolio</div>
    <h2 class="big rv">I contenuti<br><span class="grad-t">che abbiamo creato</span></h2>
    <div class="pf-grid">{"".join(carta_pf(*x) for x in PF)}</div>
  </div>
  <dialog class="pf-box" aria-label="Contenuto a schermo grande"><button type="button" class="pf-x" aria-label="Chiudi">×</button><div class="pf-media"></div><p class="pf-cap"></p></dialog>
</section>"""
casi_corpo = ph_hero("Casi studio", "Cosa è cambiato", "per chi lavora con noi",
                     "Dietro le quinte dei nostri lavori: il problema da cui siamo partiti, cosa abbiamo fatto e cosa è cambiato. I numeri vengono dagli account dei clienti.")
casi_corpo += f'''
<section class="rot-sez" aria-label="Casi studio">
  <div class="rt" id="rot" tabindex="0" role="region" aria-roledescription="carosello" aria-label="Casi studio"><div class="rt-stage" id="rot-stage"></div>
    <button class="rt-fr rt-prev" type="button" aria-label="Caso precedente"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></button>
    <button class="rt-fr rt-next" type="button" aria-label="Caso successivo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
  </div>
  <div class="rt-dots" id="rot-dots" role="group" aria-label="Scegli il caso"></div>
</section>
{PORTFOLIO}
{CTA_FINE}'''
pagina("casi-studio.html", "I nostri lavori · Topiko Lab", "casi-studio.html", casi_corpo)


def caso(file, titolo_pag, chip, foto, h1a, h1b, blocchi, numeri, nota, prossimo):
    corpo = f'''<section class="ph-hero" style="padding-bottom:30px">
  <div class="blob b1"></div><div class="blob b2"></div>
  <div class="wrap">
    <div class="cs-testa"><a class="eyebrow h-in" href="casi-studio.html">Casi studio</a><a class="btn btn-g casi-tutti h-in" href="casi-studio.html">I nostri lavori {FRECCIA}</a></div>
    <h1><span class="riga"><span>{h1a}</span></span><span class="riga"><span><span class="grad-t">{h1b}</span></span></span></h1>
  </div>
</section>
<section class="chiara" style="padding-bottom:70px">
  <div class="wrap">
    <div class="cs-cover rv"><div class="ph" style="background-image:url('img/{foto}')"></div><div class="cs-meta">{"".join(f'<span class="chip">{c}</span>' for c in chip)}</div></div>
  </div>
</section>
<section class="chiara" style="padding-top:0">
  <div class="wrap">
    <div class="cs-blocchi">
      {"".join(f'<h2 class="rv">{t}</h2><div class="rv">{c}</div>' for t, c in blocchi)}
    </div>
  </div>
</section>
<section style="padding-top:20px">
  <div class="wrap">
    <div class="cs-num">
      {"".join(f'<div class="rv"><strong data-to="{to}" data-pre="{pre}">{pre}{f'{to:,}'.replace(',', '.')}</strong><small>{lab}</small></div>' for to, pre, lab in numeri)}
    </div>
    <p class="cs-nota">{nota}</p>
    <div class="prossimo"><small>Prossimo caso</small><a href="{prossimo[0]}">{prossimo[1]}</a></div>
  </div>
</section>'''
    pagina(file, titolo_pag, "casi-studio.html", corpo)


caso("caso-gapor.html", "Gapor · Topiko Lab", ["Gapor", "Scale su misura", "Inserzioni e contenuti"], "gapor.jpg",
     "Far vedere come nasce una scala", "a chi ristruttura casa",
     [("Il cliente", "<p>Gapor disegna, costruisce e posa scale su misura.</p>"),
      ("La richiesta", "<p>Far conoscere i progetti e il lavoro in officina a chi ristruttura o costruisce casa.</p>"),
      ("Cosa abbiamo fatto", "<ul><li>Contenuti che mostrano come nasce una scala, con la rubrica \"anatomia della scala\".</li><li>Inserzioni con la scala finita e un modulo per chiedere il preventivo.</li><li>Un solo compito per le inserzioni: portare richieste di preventivo.</li></ul>"),
      ("Cosa è successo", "<p>Chi compra una scala su misura ci pensa per mesi. Molte richieste diventano lavori più avanti. Intanto Gapor ha già parlato con 50 persone che hanno chiesto il preventivo.</p>")],
     [(123, "", "richieste di preventivo in cinque settimane"), (95000, "", "persone hanno visto le inserzioni"), (50, "", "persone con cui Gapor ha già parlato")],
     "Dati dall'account pubblicitario del cliente, dal 10/06 al 16/07 2026.", ("caso-insmile.html", "Insmile"))

caso("caso-insmile.html", "Insmile · Topiko Lab", ["Insmile", "Sbiancamento dentale", "Identità, negozio online, inserzioni"], "insmile.jpg",
     "Brand book, contenuti e campagne", "per un negozio online",
     [("Il cliente", "<p>Insmile vende prodotti per lo sbiancamento dei denti da fare a casa.</p>"),
      ("Cosa abbiamo fatto", "<ul><li>Il brand book: colori, caratteri e come devono apparire i prodotti.</li><li>I contenuti per Instagram, con i video girati in studio insieme all'igienista.</li><li>Le campagne per il negozio online, valutate sugli ordini veri del sito.</li></ul>"),
      ("Il risultato", "<p>Nel primo mese di campagne il sito ha cominciato a ricevere ordini con regolarità.</p>")],
     [(33, "3 → ", "ordini nel primo mese di campagne"), (2633, "248 → ", "visite al sito nello stesso periodo"), (451, "+", "follower in 30 giorni")],
     "Confronto fra il 27/07-23/08 e il 31/08-27/09 2026. Dati dal negozio online del cliente, da Google Analytics e da Meta.", ("caso-koloro.html", "Koloro"))

caso("caso-koloro.html", "Koloro · Topiko Lab", ["Koloro", "Caffè bistrot a Parma", "Identità social e contenuti"], "koloro.jpg",
     "Dalle locandine ai piatti:", "un profilo che riconosci subito",
     [("Da dove partivamo", "<p>Il profilo era una raccolta di locandine di eventi, ognuna con caratteri e colori diversi. Di colazioni, panini e pausa pranzo non c'era traccia.</p>"),
      ("La richiesta", "<p>Migliorare la comunicazione e la presenza online.</p>"),
      ("Cosa abbiamo fatto", "<ul><li>Un carattere pulito e un corsivo per l'accento da bistrot.</li><li>Colori caldi: legno, oliva, crema e oro.</li><li>Foto e video dei piatti e della sala, girati nel locale.</li><li>Testi diretti, con il tu.</li><li>Inserzioni mostrate solo a chi abita intorno a Parma.</li></ul>")],
     [(1750, "oltre ", "follower in 113 giorni, partendo da 1.150"), (600000, "oltre ", "visualizzazioni su Instagram e Facebook"), (10000, "oltre ", "visite al profilo"), (500, "oltre ", "clic sul menu")],
     "Dal 25/03 al 16/07 2026, inserzioni solo intorno a Parma.", ("caso-gapor.html", "Gapor"))

team = '''<section class="sezione chiara">
  <div class="wrap">
    <div class="eyebrow rv">La squadra</div>
    <h2 class="big rv" style="margin-top:20px">Ognuno fa <span class="grad-t">un mestiere solo, e lo fa bene.</span></h2>
    <p class="suggerimento rv">Passa con il mouse sulle foto: abbiamo provato a stare fermi, senza successo.</p>
    <div class="team">
      <div class="persona rv" data-cammina="davide:11"><div class="foto" style="background-image:url('img/team-davide.jpg')"></div><div class="t"><h3>Davide</h3><p>Segue clienti e progetti. È la persona da chiamare per sapere a che punto siamo.</p></div></div>
      <div class="persona rv" data-cammina="bryan:9"><div class="foto" style="background-image:url('img/team-bryan.jpg')"></div><div class="t"><h3>Bryan</h3><p>Pensa la strategia e segue social, inserzioni e contenuti con l'AI.</p></div></div>
      <div class="persona rv" data-cammina="chiara:10"><div class="foto" style="background-image:url('img/team-chiara.jpg')"></div><div class="t"><h3>Chiara</h3><p>Fa la grafica per social e inserzioni.</p></div></div>
      <div class="persona rv" data-cammina="barbara:11"><div class="foto" style="background-image:url('img/team-barbara.jpg')"></div><div class="t"><h3>Barbara</h3><p>Gestisce i social dei clienti.</p></div></div>
      <div class="persona rv" data-cammina="fabio:6"><div class="foto" style="background-image:url('img/team-fabio.jpg')"></div><div class="t"><h3>Fabio</h3><p>Gira foto e video, nelle aziende e in studio.</p></div></div>
    </div>
  </div>
</section>'''
# apertura: il team con l'anello dei servizi (sezione chiara, versione a colori); lo muove js/anello.js
TA_SX = '<span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.2 10.9 15.8 7.1M8.2 13.1l7.6 3.8"/></svg></span><p>Ti parliamo chiaro, con i numeri davanti.</p>'
TA_DX = '<span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg></span><p>Un solo referente per tutta la comunicazione</p>'
chi_corpo = f"""<section class="chiara ta-anello">
  <div class="ta-testo">
    <div class="eyebrow h-in">Chi siamo</div>
    <h1 class="h-in"><span>Un laboratorio</span><span><span class="grad-t">che ti conosce per nome</span></span></h1>
    <p class="lead h-in">Siamo giovani, sul pezzo e amiamo questo lavoro. Abbiamo un debole per le aziende del nostro territorio: le raccontiamo come se fossero nostre. Ti parliamo chiaro, con i numeri davanti.</p>
  </div>
  <div class="ta-ancora">
    <div class="ta-palco">
      <div class="ta-giro dietro" aria-hidden="true"></div>
      <img class="ta-ombra" src="img/anello/gruppo-ombra.webp" alt="" aria-hidden="true">
      <img class="ta-foto" src="img/anello/gruppo-colori.webp" width="1100" height="1150" alt="Il team di Topiko Lab nello studio, seduto su poltrone colorate">
      <div class="ta-giro davanti" aria-hidden="true"></div>
    </div>
    <svg class="ta-orbita" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path d="M17.5 0 C 17.5 70, 82.5 78, 82.5 0"/></svg>
    <div class="ta-lato sx">{TA_SX}</div>
    <div class="ta-lato dx">{TA_DX}</div>
  </div>
  <div class="ta-fila"><div class="ta-lato">{TA_SX}</div><div class="ta-lato">{TA_DX}</div></div>
</section>"""
chi_corpo += "\n" + team + "\n" + rec.replace('Cosa dicono <span class="grad-t">i clienti</span>', 'La nostra <span class="grad-t">pagella</span>', 1) + "\n" + CTA_FINE  # Chi siamo: tutto chiaro fino alla fascia finale
pagina("chi-siamo.html", "Chi siamo · Topiko Lab", "chi-siamo.html", chi_corpo)

analisi_corpo = ph_hero("Analisi gratuita", "Che voto prende", "il tuo profilo Instagram?",
                        "Il tempo di un caffè per compilare. Il report lo mettiamo in forno noi: entro 24 ore hai il voto su 100.")
# titolo e frase stanno nell'apertura, come nelle altre pagine: nel riquadro restano voto e modulo
valuta_analisi = re.sub(r'\s*<div class="eyebrow">Analisi gratuita</div>\s*<h2>.*?</h2>\s*<p>.*?</p>', '', valuta, count=1, flags=re.S)
analisi_corpo += f'''
{valuta_analisi.replace('class="valuta" id="valuta"', 'class="valuta" id="valuta" style="padding-top:0"')}
<section class="sezione chiara">
  <div class="wrap">
    <div class="eyebrow rv">Come funziona</div>
    <div class="passi-g">
      <div class="rv"><b>01</b><h3>Mandi il profilo</h3><p>Il link del profilo Instagram dell'azienda e una mail a cui risponderti.</p></div>
      <div class="rv"><b>02</b><h3>Lo guardiamo</h3><p>Bio, griglia, contenuti e numeri, con lo stesso metodo che usiamo per i clienti.</p></div>
      <div class="rv"><b>03</b><h3>Ricevi il voto</h3><p>Un punteggio su 100 e le prime cose da sistemare.</p></div>
      <div class="rv"><b>04</b><h3>Se vuoi, ne parliamo</h3><p>Una call per capire da dove partire.</p></div>
    </div>
  </div>
</section>'''
pagina("analisi.html", "Analisi gratuita · Topiko Lab", "analisi.html", analisi_corpo)

contatti_corpo = ph_hero("Contatti", "Prendiamoci", "un caffè.",
                         "Scrivici due righe sulla tua azienda e su cosa vuoi cambiare. Se siamo lontani facciamo una call, ma il caffè te lo prepari tu.")
# Contatti (26/11, Bryan): il modulo resta sullo stesso fondo scuro del titolo, subito sotto, senza cambio di colore
contatti_corpo += f'''
<section class="contatti-sez">
  <div class="wrap contatti-g">
    <form class="rv" id="modulo-contatti">
      <label class="t" for="c-nome">Nome e cognome<input id="c-nome" name="nome" type="text" placeholder="Mario Rossi" required></label>
      <label class="t" for="c-az">Azienda<input id="c-az" name="azienda" type="text" placeholder="Rossi Srl"></label>
      <label class="t" for="c-mail">Email<input id="c-mail" name="email" type="email" placeholder="nome@azienda.it" required></label>
      <label class="t" for="c-tel">Telefono<input id="c-tel" name="telefono" type="text" placeholder="333 123 4567"></label>
      <label class="t" for="c-msg">Di cosa vuoi parlare<textarea id="c-msg" name="messaggio" placeholder="Siamo un'azienda di..." required></textarea></label>
      <input type="text" name="sito_web" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
      <label class="ck"><input type="checkbox" id="c-priv" required> <span>Ho letto l'informativa privacy (obbligatorio).</span></label>
      <button class="btn btn-g">Invia {FRECCIA}</button>
      <p class="modulo-errore" role="alert" style="color:#FFE3A3;font-size:14px;font-weight:600"></p>
      <div class="grazie">Messaggio arrivato. Intanto puoi mettere su la moka.</div>
    </form>
    <div class="recapiti">
      <div class="rv"><small>Email</small><b><a href="mailto:info@topikolab.it">info@topikolab.it</a></b></div>
      <div class="rv"><small>Telefono</small><b>327 856 4694</b></div>
      <div class="rv"><small>Dove siamo</small><b>Via Sante Conti 7, Montecchio Emilia (RE)</b></div>
      <div class="rv"><small>Social</small><b><a href="https://www.instagram.com/topikolab/">Instagram</a> · <a href="https://www.linkedin.com/company/topikolab/">LinkedIn</a></b></div>
      <div class="rv"><small>Analisi gratuita</small><b><a href="analisi.html">Fai valutare il tuo profilo →</a></b></div>
    </div>
  </div>
</section>'''
pagina("contatti.html", "Contatti · Topiko Lab", "contatti.html", contatti_corpo)

CATEGORIE = ["Social", "Inserzioni", "Sito e SEO", "AI", "Casi studio"]
segn = '<span class="segnaposto">'
schede = []
for i, cat in enumerate(["Social", "Inserzioni", "Sito e SEO", "AI", "Social", "Casi studio", "Inserzioni"]):
    schede.append(f"""<a class="post rv{' primo' if i == 0 else ''}" href="articolo.html"><div class="ph">{cat}</div><div class="t"><small>{cat} · {segn}data</span></small><h3>{segn}Titolo dell'articolo</span></h3><p>{segn}Due righe di anteprima dell'articolo.</span></p></div></a>""")
blog_corpo = ph_hero("Blog", "Appunti", "dal laboratorio", "Quello che impariamo lavorando con i clienti, su social, inserzioni, siti e AI.")
blog_corpo += f"""
<section class="chiara">
  <div class="wrap">
    <div class="filtri rv"><span class="on">Tutti</span>{"".join(f"<span>{c}</span>" for c in CATEGORIE)}</div>
    <div class="blog-g">{"".join(schede)}</div>
  </div>
</section>
{CTA_FINE}"""
pagina("blog.html", "Blog · Topiko Lab", "blog.html", blog_corpo)

articolo_corpo = f"""<section class="ph-hero" style="padding-bottom:40px">
  <div class="blob b1"></div><div class="blob b2"></div>
  <div class="wrap" style="max-width:860px">
    <a class="eyebrow h-in" href="blog.html">Blog · Social</a>
    <h1 style="font-size:clamp(40px,5.4vw,76px)"><span class="riga"><span>{segn}Titolo dell'articolo</span></span></h1>
    <p class="lead h-in">{segn}Sottotitolo: in una frase, cosa porta a casa chi legge.</span></p>
  </div>
</section>
<section class="chiara">
  <div class="wrap">
    <article class="articolo">
      <div class="ph rv">Immagine dell'articolo</div>
      <p class="rv">{segn}Paragrafo d'apertura. Qui si vede come scorre il testo: corpo grande, righe ariose, larghezza comoda da leggere.</span></p>
      <h2 class="rv">{segn}Titolo di paragrafo</span></h2>
      <p class="rv">{segn}Testo del paragrafo.</span></p>
      <blockquote class="rv">{segn}Una frase da mettere in evidenza.</span></blockquote>
      <p class="rv">{segn}Testo del paragrafo.</span></p>
      <div class="autore rv"><i style="background-image:url('img/team-bryan.jpg')"></i><div><b>Bryan</b><br><small style="color:var(--testo-3)">Strategia social e AI</small></div></div>
    </article>
  </div>
</section>
{CTA_FINE}"""
pagina("articolo.html", "Articolo · Topiko Lab", "blog.html", articolo_corpo)

# Privacy e cookie policy. Testo da far controllare a chi segue la parte legale prima di andare online.
AGGIORNATO = "6 novembre 2026"
privacy_corpo = ph_hero("Privacy", "Privacy", "policy", "Quali dati raccogliamo, perché li usiamo e come puoi controllarli.", risalto=False)
privacy_corpo += f"""
<section class="chiara"><div class="wrap"><article class="articolo">
<p>Questa informativa vale per chi visita topikolab.it o compila i suoi moduli. Segue gli articoli 13 e 14 del Regolamento UE 2016/679 (GDPR).</p>

<h2>1. Chi tratta i tuoi dati</h2>
<p>Il titolare del trattamento è Davide Dobelli, per Topiko Lab. In questa pagina "noi" indica il titolare.</p>
<p>Via Sante Conti 7, 42027 Montecchio Emilia (RE)<br>P.IVA 03058460357<br>Email: <a href="mailto:davide.dobelli@topikolab.it">davide.dobelli@topikolab.it</a><br>Telefono: +39 327 856 4694</p>

<h2>2. Quali dati raccogliamo</h2>
<ul class="legale">
<li><b>Modulo Contatti:</b> nome, azienda e recapiti, più il testo del tuo messaggio.</li>
<li><b>Analisi gratuita:</b> azienda, email e nome del profilo Instagram che indichi.</li>
<li><b>Dati pubblici del profilo Instagram:</b> nome, bio e sito. Del profilo vediamo anche follower e foto. Dei post vediamo numero, date, like e commenti. Questi dati arrivano da Meta, tramite le sue API.</li>
<li><b>Dati di navigazione:</b> il server registra indirizzo IP, browser, sistema operativo e pagine richieste.</li>
<li><b>Cookie:</b> i dettagli sono nella <a href="cookie.html">cookie policy</a>.</li>
</ul>

<h2>3. Perché usiamo i dati e su quale base</h2>
<div class="tabella-scorre"><table class="tabella-legale">
<tr><th>Scopo</th><th>Base giuridica</th><th>Per quanto tempo</th></tr>
<tr><td>Rispondere al tuo messaggio</td><td>Tua richiesta, prima di un eventuale contratto, art. 6.1.b</td><td>5 anni, salvo richiesta di cancellazione</td></tr>
<tr><td>Inviarti l'analisi del profilo che hai richiesto</td><td>Tua richiesta, prima di un eventuale contratto, art. 6.1.b</td><td>5 anni, salvo richiesta di cancellazione</td></tr>
<tr><td>Inviarti comunicazioni commerciali, se lo accetti nel modulo dell'Analisi gratuita</td><td>Consenso, art. 6.1.a</td><td>Fino alla revoca del consenso</td></tr>
<tr><td>Statistiche e pubblicità con i cookie</td><td>Consenso, art. 6.1.a</td><td>Vedi la cookie policy</td></tr>
<tr><td>Proteggere il sito da abusi</td><td>Legittimo interesse, art. 6.1.f</td><td>24 mesi per i log tecnici</td></tr>
<tr><td>Rispettare obblighi di legge</td><td>Obbligo legale, art. 6.1.c</td><td>Il tempo previsto dalla legge</td></tr>
</table></div>
<p>Senza i dati dei moduli non possiamo risponderti. Il consenso commerciale è facoltativo.</p>
<p>L'analisi gratuita dà un voto al profilo Instagram. Il voto è un calcolo automatico sui dati pubblici e non ha effetti legali su di te. La mail con l'analisi arriva entro 24 ore. Il nostro team riceve subito una copia, con azienda, email e scelta sul consenso commerciale.</p>

<h2>4. A chi arrivano i dati</h2>
<p>Non diffondiamo i tuoi dati. I dati arrivano ai collaboratori di Topiko Lab che seguono la tua richiesta. Arrivano anche a questi fornitori:</p>
<ul class="legale">
<li><b>VHosting Solution S.r.l.</b> (Italia): ospita il sito.</li>
<li><b>Cloudflare:</b> elabora i moduli e calcola il voto. Legge l'indirizzo IP per limitare gli abusi.</li>
<li><b>Brevo</b> (Francia): invia le email. Se dai il consenso commerciale, conserva nella nostra lista email e azienda. Conserva anche profilo Instagram e voto.</li>
<li><b>Google:</b> Analytics, se lo accetti, e recensioni della nostra scheda.</li>
<li><b>Meta:</b> riceve il nome del profilo Instagram che indichi, per leggere i dati pubblici. Se accetti i cookie pubblicitari, riceve anche i dati del pixel.</li>
</ul>
<p>Alcuni fornitori agiscono per nostro conto (responsabili del trattamento). Altri decidono da soli come usare i dati (titolari autonomi). Possiamo comunicare i dati anche alle autorità, se la legge lo richiede.</p>

<h2>5. Dati fuori dall'Unione Europea</h2>
<p>Cloudflare, Google e Meta possono trattare dati negli Stati Uniti. In questi casi il trasferimento si basa sul Data Privacy Framework UE-USA. Se un fornitore non vi aderisce, valgono le clausole contrattuali standard della Commissione Europea.</p>

<h2>6. I tuoi diritti</h2>
<p>Puoi chiederci di vedere i tuoi dati, correggerli, cancellarli o riceverli in un formato leggibile. Puoi anche limitarne l'uso o opporti. Puoi revocare il consenso quando vuoi. Quello che abbiamo fatto prima della revoca resta valido.</p>
<p>Per esercitare questi diritti scrivi a <a href="mailto:davide.dobelli@topikolab.it">davide.dobelli@topikolab.it</a>. Ogni email commerciale contiene anche il link per disiscriverti. Puoi inoltre fare reclamo al <a href="https://www.garanteprivacy.it" rel="noopener">Garante per la protezione dei dati personali</a>.</p>

<h2>7. Minori</h2>
<p>Il sito non è rivolto a chi ha meno di 16 anni. Se scopriamo di avere dati di un minore, li cancelliamo.</p>

<h2>8. Sicurezza e responsabile della protezione dei dati</h2>
<p>Usiamo misure tecniche e organizzative adatte a proteggere i dati. Non abbiamo nominato un responsabile della protezione dei dati (DPO), perché per la nostra attività non è obbligatorio.</p>

<h2>9. Modifiche</h2>
<p>Se questa informativa cambia, trovi la versione aggiornata su questa pagina.</p>
<p>Ultimo aggiornamento: {AGGIORNATO}</p>
</article></div></section>"""
pagina("privacy.html", "Privacy policy · Topiko Lab", "", privacy_corpo)

cookie_corpo = ph_hero("Cookie", "Cookie", "policy", "Quali cookie usa il sito e come puoi sceglierli.", risalto=False)
cookie_corpo += f"""
<section class="chiara"><div class="wrap"><article class="articolo">
<p>I cookie sono piccoli file che un sito salva sul tuo dispositivo. In questa pagina chiamiamo "cookie" anche la memoria locale del browser e il pixel. Il pixel è un piccolo codice che segnala la tua visita.</p>
<p><button type="button" class="btn btn-g" data-preferenze-cookie>Cambia le tue preferenze</button></p>

<h2>1. Cookie tecnici</h2>
<p>I cookie tecnici servono al sito e non richiedono il consenso.</p>
<div class="tabella-scorre"><table class="tabella-legale">
<tr><th>Nome</th><th>Di chi è</th><th>A cosa serve</th><th>Durata</th></tr>
<tr><td>topiko_consenso</td><td>Topiko Lab</td><td>Ricorda la tua scelta sui cookie. Il dato resta nella memoria locale del browser.</td><td>Circa 6 mesi</td></tr>
</table></div>

<h2>2. Cookie statistici</h2>
<p>Partono solo se li accetti. Ci dicono quali pagine vengono visitate.</p>
<div class="tabella-scorre"><table class="tabella-legale">
<tr><th>Nome</th><th>Di chi è</th><th>A cosa serve</th><th>Durata</th></tr>
<tr><td>_ga</td><td>Google Analytics</td><td>Distingue i visitatori</td><td>2 anni</td></tr>
<tr><td>_ga_*</td><td>Google Analytics</td><td>Conserva lo stato della visita</td><td>2 anni</td></tr>
</table></div>

<h2>3. Cookie pubblicitari</h2>
<p>Partono solo se li accetti. Misurano le nostre inserzioni. Ci permettono anche di mostrare le inserzioni su Facebook e Instagram a chi ha visitato il sito.</p>
<div class="tabella-scorre"><table class="tabella-legale">
<tr><th>Nome</th><th>Di chi è</th><th>A cosa serve</th><th>Durata</th></tr>
<tr><td>_fbp</td><td>Meta</td><td>Riconosce il browser per misurare le inserzioni</td><td>3 mesi</td></tr>
<tr><td>_fbc</td><td>Meta</td><td>Ricorda il clic su un'inserzione</td><td>3 mesi</td></tr>
</table></div>

<h2>4. Contenuti esterni</h2>
<p>Le recensioni nella home arrivano da Google, comprese le foto degli autori. Quando arrivi alla sezione, il tuo browser si collega ai server di Google. Google riceve così il tuo indirizzo IP. Il sito non salva cookie per questo collegamento.</p>
<p>Le icone di Instagram, LinkedIn e Facebook sono semplici link. Il social interessato riceve dati solo se clicchi l'icona.</p>

<h2>5. Come scegliere</h2>
<p>Alla prima visita puoi accettare, rifiutare o scegliere per categoria. Se chiudi il banner con la X, restano attivi solo i cookie tecnici. Dopo circa 6 mesi ti chiediamo di nuovo la scelta.</p>
<p>Puoi cambiare la scelta quando vuoi da "Preferenze cookie", in fondo a ogni pagina. Puoi anche cancellare i cookie dalle impostazioni del browser.</p>
<p>Per sapere come usiamo i dati personali leggi la <a href="privacy.html">privacy policy</a>.</p>
<p>Ultimo aggiornamento: {AGGIORNATO}</p>
</article></div></section>"""
pagina("cookie.html", "Cookie policy · Topiko Lab", "", cookie_corpo)


# ---------- versione da pubblicare: solo i file che servono ai visitatori ----------
import shutil
DIST = QUI / "pubblica"
shutil.rmtree(DIST, ignore_errors=True)
DIST.mkdir()
# seq-computer e seq-computer-m non servono più: il computer della home è stato tolto il 26/11 (le cartelle sorgente restano)
for cartella in ("css", "js", "img", "seq-logo", "fonts", "vendor"):
    shutil.copytree(QUI / cartella, DIST / cartella, ignore=shutil.ignore_patterns("._*", ".DS_Store", "mazzo"), copy_function=shutil.copyfile)
for p in QUI.glob("*.html"):
    if not p.name.startswith(("._", "base-", "archivio", "sito-")):
        (DIST / p.name).write_text(p.read_text(encoding="utf-8").replace(" http://127.0.0.1:8788", ""), encoding="utf-8")
shutil.copyfile(QUI / "htaccess.txt", DIST / ".htaccess")
(DIST / "js/entra.js").unlink(missing_ok=True)  # muoveva il computer della home, non lo usa più nessuna pagina

print("pagine:", ", ".join(sorted(p.name for p in QUI.glob("*.html") if not p.name.startswith(("base-", "archivio", "sito-")))))
