#!/bin/bash
# Mette online le modifiche sulla bozza del sito: https://topiko-sito-bozza.vercel.app (il link resta sempre lo stesso).
# Uso: bash aggiorna-link.sh "cosa hai cambiato"
#  1. salva le tue modifiche su GitHub e prende quelle degli altri (Bryan, Davide)
#  2. rigenera il sito con build.py, per fermarsi subito se c'è un errore
#  3. Vercel vede la modifica su GitHub e aggiorna la bozza da solo in 1-2 minuti
# Con --prova prepara solo la cartella della bozza, senza salvare (lo usa Vercel per costruire il sito).
set -e
SITO="$(cd "$(dirname "$0")" && pwd)"
BOZZA="${BOZZA:-$HOME/Developer/topiko-sito-bozza}"

# git: una copia normale (Davide) oppure, sul Mac di Bryan, l'archivio tenuto fuori dal vault
if [ -d "$SITO/.git" ]; then G() { git -C "$SITO" "$@"; }
elif [ -d "$HOME/Developer/topiko-sito.git" ]; then G() { git --git-dir="$HOME/Developer/topiko-sito.git" --work-tree="$SITO" "$@"; }
else G() { return 1; }; fi

# recensioni Google per la bozza (solo sul Mac di Bryan): al massimo ogni 6 ore, perché il tetto è di 25 letture al giorno.
# Il file si sostituisce solo se Google risponde con le recensioni, mai con un errore.
REC="$SITO/recensioni-bozza.json"
if [ -z "$CI" ] && [ "$1" != "--prova" ] && [ -d "$HOME/Developer/topiko-sito.git" ] && [ -n "$(find "$REC" -mmin +360 2>/dev/null)" ]; then
  CHIAVE=$(grep -o "AIza[A-Za-z0-9_-]*" "$SITO/js/config.js"); LUOGO=$(grep -o "ChIJ[A-Za-z0-9_-]*" "$SITO/js/config.js")
  curl -s -m 20 -H "Referer: https://topikolab.it/" -H "X-Goog-Api-Key: $CHIAVE" -H "X-Goog-FieldMask: rating,userRatingCount,googleMapsUri,reviews" \
    "https://places.googleapis.com/v1/places/$LUOGO?languageCode=it" -o "$REC.nuovo" || true
  if grep -q '"reviews"' "$REC.nuovo" 2>/dev/null; then mv "$REC.nuovo" "$REC"; else rm -f "$REC.nuovo"; touch "$REC"; fi
fi

# 1. salva e prende le modifiche degli altri
if [ -z "$CI" ] && [ "$1" != "--prova" ] && G rev-parse -q --verify HEAD >/dev/null 2>&1; then
  G add -A
  G diff --cached --quiet || G commit -q -m "${1:-Modifiche al sito}"
  if ! G pull -q --rebase origin main; then
    G rebase --abort 2>/dev/null || true
    echo "STOP: le tue modifiche e quelle di un collega toccano le stesse righe. Niente è stato pubblicato: chiedi a Claude di unire le due versioni."
    exit 1
  fi
fi

# 2. rigenera il sito (se build.py ha un errore ci si ferma qui, prima di pubblicare)
python3 -I "$SITO/build.py" > /dev/null

# cartella della bozza: il sito più il file che lo tiene fuori da Google (le altre regole sono in vercel.json)
mkdir -p "$BOZZA"
if command -v rsync >/dev/null; then
  rsync -a --delete --exclude='._*' --exclude='.DS_Store' --exclude='.htaccess' --exclude='.vercel' "$SITO/pubblica/" "$BOZZA/"
else
  cp -R "$SITO/pubblica/." "$BOZZA/"; rm -f "$BOZZA/.htaccess"
fi
cp "$REC" "$BOZZA/js/recensioni-bozza.json"
printf 'User-agent: *\nDisallow: /\n' > "$BOZZA/robots.txt"

[ "$1" = "--prova" ] || [ -n "$CI" ] && { echo "Cartella pronta: $BOZZA ($(find "$BOZZA" -type f | wc -l | tr -d ' ') file)"; exit 0; }

# 3. manda le modifiche su GitHub: da lì Vercel aggiorna la bozza da solo
if G rev-parse -q --verify HEAD >/dev/null 2>&1; then
  G push -q origin HEAD:main && echo "Salvato su GitHub. La bozza si aggiorna in 1-2 minuti: https://topiko-sito-bozza.vercel.app"
fi
