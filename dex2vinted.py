
from utils.vinted_phase_1 import parse_dex_csv
from utils.vinted_phase_2 import link_images_to_csv
from utils.vinted_phase_3 import run_scraping

# === PARAMÈTRES GLOBAUX ===
PHASE = 1  # 1 = génération CSV / 2 = liaison images / 3 = scraping
INPUT_CSV = "vinted_data/up.csv"
OUTPUT_CSV = f"vinted_data/output_up.csv"
IMAGE_FOLDER = "vinted_images/vintedlot"
DEFAULTS = {
    "CATEGORY": "Unit",  # "Unit" pour une carte seule, "Lot" pour plusieurs cartes
    # "Small" pour envoi simple, "Medium"/"Large" si plusieurs cartes ou objets
    "PACKAGE": "Small",

    "CONDITION": "Very Good",  # Voir CONDITION_MAP ci-dessous
    "LOCALE": "FR",  # Langue de la carte (EN, FR, JP, CN…)

    "CONDITION_MAP": {
        "Very Good": "Très bon état (Near Mint), carte en excellent état (voir photos).",
        "Good": "Bon état, quelques légers défauts visibles (bords, coins ou surface).",
        "Average": "État correct, usure visible (rayures, coins blanchis, etc.) — veuillez consulter plus bas pour plus de détails.",
    },

    "LOCALE_MAP": {
        "EN": "Anglaise 🇬🇧",
        "FR": "Française 🇫🇷",
        "JP": "Japonaise 🇯🇵",
        "CN": "Chinoise 🇨🇳",
    },

    "DESC_TEMPLATE_UNIT": (
        "✨ Carte Pokémon {name} - {rarity} de la série {series} ({set})\n"
        "📘 Version {locale_full}\n"
        "✅ État : {condition_full}\n\n"
        "🛡️ Carte envoyée sous sleeve + toploader !\n"
        "🚀 Expédition rapide sous 1 à 2 jours ouvrés 📦\n"
        "🤝 Remise en main propre possible sur Paris / 92 / 95\n"
        "📸 Besoin de photos supplémentaires ? N'hésitez pas à me demander !\n\n"
        "🃏 Plein d'autres cartes sont disponibles sur mon profil !\n"
        "📦 Possibilité de créer des lots personnalisés avec réduction sur les frais de port 🤑\n"
    ),

    "DESC_TEMPLATE_LOT": (
        "✨ Lot de cartes Pokémon {name}\n"
        "📘 Cartes officielles {locale_full}\n"
        "✅ État : {condition_full}\n\n"
        "🛡️ Chaque carte est envoyée sous sleeve + toploader !\n"
        "🚀 Expédition rapide sous 1 à 2 jours ouvrés 📦\n"
        "🤝 Remise en main propre possible sur Paris / 92 / 95\n"
        "📸 Besoin de photos supplémentaires ? N'hésitez pas à me demander !\n\n"
        "🃏 Plein d'autres cartes sont disponibles sur mon profil !\n"
        "📦 Possibilité de créer des lots personnalisés avec réduction sur les frais de port 🤑\n"
    )

}

if __name__ == "__main__":
    if PHASE == 1:
        parse_dex_csv(INPUT_CSV, OUTPUT_CSV, DEFAULTS)
    elif PHASE == 2:
        link_images_to_csv(OUTPUT_CSV, IMAGE_FOLDER)
    elif PHASE == 3:
        run_scraping(OUTPUT_CSV)
    else:
        print("❌ Phase non reconnue. Utilise 1 (DEX), 2 (Images), 3 (Scraping).")
