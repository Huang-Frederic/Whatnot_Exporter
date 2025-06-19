import argparse
import os
from utils.whatnot_formatter import format_whatnot_csv

GITHUB_BASE_URL = "https://raw.githubusercontent.com/Huang-Frederic/Whatnot_Exporter/master/whatnot-images"
BACKGROUND_PATH = "assets/Background.png"

# TODO : PRICES SHOULD BE ROUNDED, GIVEAWAY ERROR

BASE_PRICE_BY_RARITY = {
    "SAR": 5.0,
    "SR": 4.0,
    "AR": 3.0,
    "CHR": 3.0,
    "RRR": 2.0,
    "RR": 1.0,
    "Shiny": 1.0,
    "Other": 1.0,
    "ERROR": 0.5
}

BASE_LISTINGS = [
    {
        "Titre": "AR vu en Live - JP",
        "Description": "AR",
        "Quantity": 43,
        "Prix": 3,
        "Image URL 1": "Single.png",
        "include": True
    },
    {
        "Titre": "Lot 2 AR + 1 EX - JP",
        "Description": "2AR1EX",
        "Quantity": 76,
        "Prix": 5,
        "Image URL 1": "2AR1EX.png",
        "include": False
    },
    {
        "Titre": "Lot 3 AR + 1 EX - JP",
        "Description": "3AR1EX",
        "Quantity": 44,
        "Prix": 8,
        "Image URL 1": "3AR1EX.png",
        "include": False
    },
    {
        "Titre": "Lot 5 AR + 2 EX - JP",
        "Description": "5AR2EX",
        "Quantity": 13,
        "Prix": 13,
        "Image URL 1": "5AR2EX.png",
        "include": False
    },
    {
        "Titre": "Lot 25 Ans - JP",
        "Description": "2Other",
        "Quantity": 15,
        "Prix": 1,
        "Image URL 1": "25a.png",
        "include": True
    },
    {
        "Titre": "Lot 1RRR + 1RR - JP",
        "Description": "1RRR1R",
        "Quantity": 50,
        "Prix": 1,
        "Image URL 1": "1RRR1R.png",
        "include": False
    },
    {
        "Titre": "Lot 2RR - JP",
        "Description": "1RRR1R",
        "Quantity": 50,
        "Prix": 1,
        "Image URL 1": "1RRR1R.png",
        "include": False
    },
    {
        "Titre": "Lot GemPack 1 - CN",
        "Description": "5Other",
        "Quantity": 22,
        "Prix": 5,
        "Image URL 1": "Lots.png",
        "include": True
    },
    {
        "Titre": "EX VU EN LIVE - JP",
        "Description": "1RR",
        "Quantity": 20,
        "Prix": 1,
        "Image URL 1": "1RR.png",
        "include": True
    },
    {
        "Titre": "Carte vu en Live - JP",
        "Description": "CC - JP",
        "Quantity": 19,
        "Prix": 1,
        "Image URL 1": "Lots.png",
        "include": False
    },
    {
        "Titre": "Lot Custom",
        "Description": "Lot custom défini en Live",
        "Quantity": 31,
        "Prix": 1,
        "Image URL 1": "Lots.png",
        "include": False
    }
]

RARITY_MAP = {
    "Common": "Other",
    "Uncommon": "Other",
    "Rare": "Other",
    "Ultra Rare Shiny": "SR",
    "Ultra Rare": "CHR",
    "Shiny Ultra Rare": "SR",
    "Secret Rare": "SR",
    "Rare Shiny": "Shiny",
    "Double Rare": "RR",
    "Rare Ultra": "AR",
    "Rare Secret": "SR",
    "Art Rare": "AR",
    "Special Art Rare": "SAR",
    "Secret Art Rare": "SAR",
    "Hyper Rare": "SAR",
    "Character Ultra Rare": "AR",
    "Promo": "Other",
    "Rare": "Other",
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
        LOCALE_MAP, RARITY_MAP, BASE_PRICE_BY_RARITY, BASE_LISTINGS
    )
    print(f"✅ CSV exporté : {output_path}")
