
from utils.vinted_phase_1 import parse_dex_csv
from utils.vinted_phase_2 import link_images_to_csv
from utils.vinted_phase_3 import run_scraping

# === PARAMÈTRES GLOBAUX ===
PHASE = 3  # 1 = génération CSV / 2 = liaison images / 3 = scraping
DEFAULTS = {
    "CATEGORY": "Unit",
    "PACKAGE": "Small",
    "CONDITION": "Very Good",
    "LOCALE": "EN",
    "DESC_TEMPLATE": "Carte Pokémon {name} ({rarity}) de la série {series} ({set}) en langue {locale_full}. État : {condition}. Envoi rapide et soigné 📦."
}
INPUT_CSV = "vinted.csv"
OUTPUT_CSV = "vinted_ready.csv"
IMAGE_FOLDER = "vinted_images"

if __name__ == "__main__":
    if PHASE == 1:
        parse_dex_csv(INPUT_CSV, OUTPUT_CSV, DEFAULTS)
    elif PHASE == 2:
        link_images_to_csv(OUTPUT_CSV, IMAGE_FOLDER)
    elif PHASE == 3:
        run_scraping(OUTPUT_CSV)
    else:
        print("❌ Phase non reconnue. Utilise 1 (DEX), 2 (Images), 3 (Scraping).")
