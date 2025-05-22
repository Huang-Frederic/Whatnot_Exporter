import argparse
import os
from utils.formatter import format_whatnot_csv

GITHUB_BASE_URL = "https://raw.githubusercontent.com/Huang-Frederic/Whatnot_Exporter/master/whatnot-images"
BACKGROUND_PATH = "assets/background.jpg"

BASE_PRICE_BY_RARITY = {
    "SAR": 10.0,
    "SR": 8.0,
    "AR": 5.0,
    "RRR": 3.0,
    "RR": 2.0,
    "Shiny": 4.0,
    "Other": 1.0,
    "ERROR": 0.5
}

RARITY_MAP = {
    "Common": "Other",
    "Uncommon": "Other",
    "Rare": "Other",
    "Shiny Rare": "Shiny",
    "Double Rare": "RRR",
    "Rare Ultra": "RR",
    "Rare Secret": "SR",
    "Art Rare": "AR",
    "Special Art Rare": "SAR",
    "Hyper Rare": "Other",
    "Character Ultra Rare": "Other",
    "Promo": "Other"
}

LOCALE_MAP = {
    "jpn": "JP",
    "scn": "CN",
    "default": "FR"
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exporter un fichier formaté pour Whatnot.")
    parser.add_argument(
        "input_csv", help="Chemin vers le fichier CSV d'entrée")
    args = parser.parse_args()

    os.makedirs("data_output", exist_ok=True)
    input_filename = os.path.basename(args.input_csv)
    output_path = os.path.join("data_output", f"formatted_{input_filename}")

    format_whatnot_csv(
        args.input_csv, output_path,
        GITHUB_BASE_URL, BACKGROUND_PATH,
        LOCALE_MAP, RARITY_MAP, BASE_PRICE_BY_RARITY
    )
