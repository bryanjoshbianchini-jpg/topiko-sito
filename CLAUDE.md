# Sito di Topiko Lab: regole per chi ci lavora

Ci lavorano Bryan e Davide, ognuno con il suo Claude Code. Queste regole valgono per tutti.

## Come si lavora

1. **Prima di iniziare** prendi le modifiche degli altri: `git pull`.
2. **Le modifiche si fanno solo in `build.py`.** È l'unica fonte del sito: scrive le pagine `.html`, `css/topiko.css` e gran parte dei file in `js/`. Quei file si rigenerano a ogni giro, quindi un cambio fatto a mano lì si perde. L'elenco preciso è in `.gitignore`.
3. **Rigenera e guarda:** `python3 build.py`, poi apri l'anteprima su http://localhost:3114 (in Claude Code: configurazione `sito-topiko` di `.claude/launch.json`). Controlla sempre a 1440 px e a 390 px di larghezza, e che la console non abbia errori.
4. **Metti online sulla bozza:** `bash aggiorna-link.sh "cosa hai cambiato"`. Lo script salva su GitHub e prende le modifiche dei colleghi. Vercel vede la modifica e dopo 1-2 minuti la bozza si aggiorna su https://topiko-sito-bozza.vercel.app.
5. **Se lo script si ferma per un conflitto**, vuol dire che tu e un collega avete toccato le stesse righe. Niente è andato online. Si uniscono le due versioni tenendo le modifiche di entrambi, poi si rilancia lo script.

La bozza non finisce su Google. Il sito vero (topikolab.it) non si tocca da qui.

L'archivio è pubblico: chiunque può leggerlo. Non scriverci mai password, chiavi o dati dei clienti che non sono già sul sito.

## Idee nuove

Un effetto o una sezione nuova si prova prima in una pagina a parte, fuori dal sito. Va sul sito solo quando chi l'ha chiesta l'ha vista e approvata. Se l'idea viene da un riferimento (un sito, un pin, un video), si guarda il riferimento movimento per movimento e si confronta la prova fianco a fianco prima di mostrarla.

## Stile

- **Font:** Aileron per titoli, sottotitoli e testo. Bitcount Single (a punti tondi) solo per le parole in risalto col gradiente (`.grad-t`) e per le etichette sopra i titoli. I due font sono già tarati per sembrare grandi uguali: non cambiare quelle misure.
- **Colori:** gradiente Topiko #9B03FF → #FF0082 → #FF7A2F. Sezioni scure (notte) e chiare (#F4EFF8), ognuna col suo colore fisso. Mai il verde lime.
- **Forme:** spigoli vivi sui blocchi grandi. Restano tondi bottoni, pillole, avatar e icone.
- **Movimento:** video e animazioni devono partire anche nella "modalità leggera" (`js/leggero.js`). Si fermano solo se il visitatore ha chiesto meno movimento nel sistema (`prefers-reduced-motion`).

## Testi

- I testi vengono dal Figma del sito, dove li scrivono Davide e Chiara, e si copiano parola per parola.
- Mai inventare testi, numeri, clienti o risultati. Se un testo manca, si lascia com'è e si segnala.
- Frasi brevi, una cosa per frase, si capiscono alla prima lettura. Si dà del tu.
- Nei casi studio mai costi, budget, euro spesi né parole del mestiere (reach, engagement, funnel, target).

## Recensioni Google

La bozza legge le recensioni da `recensioni-bozza.json`. Le aggiorna lo script solo dal Mac di Bryan, al massimo ogni 6 ore, perché Google concede 25 letture al giorno. Non scaricarle da altre parti.

## Cartelle

- `img/`, `seq-logo/`, `fonts/`, `vendor/`: immagini, sequenza del logo, font e librerie. Finiscono tutte sul sito.
- `js/`: alcuni file si scrivono a mano (`config.js`, `consenso.js`, `leggero.js`, `recensioni.js`, `servizi.js`, `valuta.js`), gli altri li genera `build.py`.
- `pubblica/`: la versione da mettere online, rigenerata a ogni giro.
- `vercel.json`: dice a Vercel come costruire la bozza e la tiene fuori da Google.
