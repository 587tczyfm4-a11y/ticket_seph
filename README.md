# SEPHORiA London — Ticket Watcher

Surveille automatiquement la page de revente de billets SEPHORiA London et
t'envoie un message Telegram dès qu'un billet semble disponible.

## Mise en place (10-15 min, une seule fois)

### 1. Créer un bot Telegram
1. Ouvre Telegram, cherche **@BotFather**, envoie `/newbot`, suis les instructions.
2. Il te donne un **token** (ex: `123456:ABC-DEF...`) — note-le.
3. Envoie un message à ton nouveau bot (n'importe quoi, ex: "salut").
4. Va sur `https://api.telegram.org/bot<TON_TOKEN>/getUpdates` dans ton navigateur
   (remplace `<TON_TOKEN>`) et repère `"chat":{"id": ...}` — c'est ton **chat_id**.

### 2. Créer un repo GitHub
1. Crée un nouveau repo sur GitHub (privé ou public, peu importe).
2. Upload ces 4 fichiers en gardant la même arborescence :
   - `check_tickets.py`
   - `requirements.txt`
   - `.github/workflows/check-tickets.yml`
   - `README.md` (optionnel)

### 3. Ajouter tes secrets
Dans le repo : **Settings → Secrets and variables → Actions → New repository secret**
- `TELEGRAM_TOKEN` = ton token du bot
- `TELEGRAM_CHAT_ID` = ton chat_id

### 4. Ajuster le texte détecté (important !)
Ouvre `check_tickets.py`, variable `NO_TICKET_TEXT`. Va sur la page de revente
dans ton navigateur, regarde le texte affiché quand il n'y a aucun billet, et
mets ce texte exact dans la variable. C'est ce qui permet au script de savoir
si la situation a changé.

### 5. Lancer / tester
Onglet **Actions** du repo → sélectionne le workflow → **Run workflow** pour
tester manuellement. Ensuite il tournera tout seul toutes les 5 minutes.

## Limites à connaître
- GitHub Actions ne garantit pas une précision à la minute près sur les cron
  (peut avoir quelques minutes de retard en période de forte charge).
- Le repo gratuit a un quota de minutes d'exécution (largement suffisant pour
  ce usage, sauf compte très chargé par ailleurs).
- Si Weezevent change la structure de sa page, il faudra remettre à jour
  `NO_TICKET_TEXT`.
