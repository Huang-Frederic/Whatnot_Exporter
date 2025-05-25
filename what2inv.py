import argparse
import os
from utils.inventory_utils import process_csv

# === Constantes globales ===

BASE_PRICE_BY_RARITY = {
    "SAR": 2.89, "SR": 2.92, "AR": 1.98,
    "RRR": 0.84, "RR": 0.30, "Shiny": 0.7,
    "Other": 0.40, "ERROR": -999
}

LANGUAGES = ["JP", "EN", "FR", "DE", "IT", "ES", "CN"]
PLATFORM = "Whatnot"
GIVEAWAY_ENTRY = "1RR"  # À ajuster selon le live
GIVEAWAY_LANG = "JP"    # À ajuster selon le live

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exporter un fichier formaté pour Whatnot.")
    parser.add_argument(
        "input_csv", help="Chemin vers le fichier CSV d'entrée")
    args = parser.parse_args()

    os.makedirs("data_output", exist_ok=True)
    input_filename = os.path.basename(args.input_csv)
    output_path = os.path.join("data_output", f"formatted_{input_filename}")

    process_csv(
        args.input_csv,
        output_path,
        base_price_by_rarity=BASE_PRICE_BY_RARITY,
        languages=LANGUAGES,
        platform=PLATFORM,
        giveaway_entry=GIVEAWAY_ENTRY,
        giveaway_lang=GIVEAWAY_LANG
    )

    print(f"✅ CSV exporté : {output_path}")
