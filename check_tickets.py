"""
Surveille la page de revente SEPHORiA London et envoie une alerte Telegram
dès qu'un billet semble disponible.

IMPORTANT — à faire avant de lancer en automatique :
1. Ouvre la page RESALE_URL dans ton navigateur, clique sur "Consulter le site"
   pour ouvrir le widget, et regarde le texte affiché quand il n'y a AUCUN billet
   en revente (ex: "Aucun billet en vente", "No tickets available", etc.)
2. Mets ce texte exact (ou une portion) dans NO_TICKET_TEXT ci-dessous.
   Le script considère qu'un billet est dispo si ce texte N'EST PLUS présent.
"""

import os
import sys
from playwright.sync_api import sync_playwright

RESALE_URL = "https://widget.weezevent.com/ticket/resale-sephoria-london-2026?locale=fr-fr"

# À ajuster après inspection manuelle de la page (voir note ci-dessus)
NO_TICKET_TEXT = "Tickets are unavailable at the moment"

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_telegram_alert(message: str) -> None:
    import urllib.request
    import urllib.parse

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("TELEGRAM_TOKEN / TELEGRAM_CHAT_ID manquants — impossible d'alerter.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": TELEGRAM_CHAT_ID, "text": message}).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=10) as resp:
        resp.read()


def check_tickets() -> bool:
    """Retourne True si un billet semble disponible."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(RESALE_URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(10000)  # 10 secondes au lieu de 5
        content = page.content()
        browser.close()

    import re
    text_only = re.sub(r"<[^>]+>", " ", content)
    text_only = re.sub(r"\s+", " ", text_only).strip()
    print(f"---- LONGUEUR TOTALE DU TEXTE : {len(text_only)} ----")
    print("---- DERNIERS 3000 CARACTÈRES (probablement le vrai contenu) ----")
    print(text_only[-3000:])
    print("---------------------------------------")

    ticket_available = NO_TICKET_TEXT not in content
    return ticket_available
   
def main():
    try:
        available = check_tickets()
    except Exception as e:
        print(f"Erreur pendant la vérification : {e}", file=sys.stderr)
        sys.exit(1)

    if available:
        print("Billet potentiellement disponible !")
        send_telegram_alert(
            "🎟️ Un billet revente SEPHORiA London semble disponible !\n"
            "https://sites.weezevent.com/sephoria-london/#ticketing"
        )
    else:
        print("Toujours aucun billet en revente.")


if __name__ == "__main__":
    main()
