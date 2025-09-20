import requests
import time
import os

# Ton token et chat ID
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# URL de ton API CoinGecko custom
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,polygon-ecosystem-token,polkadot,chainlink,algorand,tezos,filecoin,vechain,the-sandbox,fetch-ai,astar,pyth-network,usd-coin,tether&vs_currencies=usd"

# Niveaux d'alerte
alertes = {
    "bitcoin": {"achat": [107000, 87000], "vente": [125000]},
    "ethereum": {"achat": [4100, 2750], "vente": [4800]},
    "solana": {"achat": [150], "vente": [260]},
    "polygon-ecosystem-token": {"achat": [0.5, 0.2], "vente": [0.7]},  # Polygon (MATIC)
    "polkadot": {"achat": [7.0, 4.0], "vente": [10.0]},
    "chainlink": {"achat": [35.0, 15.0], "vente": [44.0]},
    "algorand": {"achat": [0.15], "vente": [0.41]},
    "tezos": {"achat": [1.33, 0.65], "vente": [2.0]},
    "filecoin": {"achat": [5.5], "vente": [9.0]},
    "vechain": {"achat": [0.05], "vente": [0.075]},
    "the-sandbox": {"achat": [0.7], "vente": [1.3]},
    "fetch-ai": {"achat": [1.3, 0.35], "vente": [2.0]},
    "astar": {"achat": [0.02], "vente": [0.03]},
    "pyth-network": {"achat": [0.45], "vente": []},
}

# Fonction d'envoi (format simplifié comme tu voulais)
def send_alert(crypto, zone, prix):
    couleur = "🟢" if zone == "achat" else "🔴"
    message = f"{couleur} {crypto.upper()}\nZone {zone} : {prix} $"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    print(r.json())  # debug console

# Boucle de surveillance
while True:
    try:
        data = requests.get(API_URL).json()
        for crypto, niveaux in alertes.items():
            if crypto not in data:
                continue

            prix_actuel = data[crypto]["usd"]

            # Vérifie zones d'achat
            for niveau in niveaux["achat"]:
                if abs(prix_actuel - niveau) < (0.01 * niveau):  # tolérance = 1%
                    send_alert(crypto, "achat", niveau)

            # Vérifie zones de vente
            for niveau in niveaux["vente"]:
                if abs(prix_actuel - niveau) < (0.01 * niveau):  # tolérance = 1%
                    send_alert(crypto, "vente", niveau)

        time.sleep(60)  # Vérifie toutes les 60 secondes

    except Exception as e:
        print("Erreur :", e)
        time.sleep(60)