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

BASE_LISTINGS = [
    {
        "Titre": "AR vu en Live - JP",
        "Description": "AR",
        "Quantity": 237,
        "Prix": 3,
        "Image URL 1": "Single.png",
        "include": True
    },
    {
        "Titre": "Lot 2 AR + 1 EX - JP",
        "Description": "2AR+1EX",
        "Quantity": 76,
        "Prix": 5,
        "Image URL 1": "2AR1EX.png",
        "include": True
    },
    {
        "Titre": "Lot 3 AR + 1 EX - JP",
        "Description": "3AR+1EX",
        "Quantity": 44,
        "Prix": 8,
        "Image URL 1": "3AR1EX.png",
        "include": True
    },
    {
        "Titre": "Lot 5 AR + 2 EX - JP",
        "Description": "5AR+2EX",
        "Quantity": 13,
        "Prix": 13,
        "Image URL 1": "5AR2EX.png",
        "include": True
    },
    {
        "Titre": "Lot 25 Ans - JP",
        "Description": "2Other",
        "Quantity": 10,
        "Prix": 1,
        "Image URL 1": "25a.png",
        "include": True
    },
    {
        "Titre": "Lot Custom",
        "Description": "Lot custom défini en Live",
        "Quantity": 31,
        "Prix": 1,
        "Image URL 1": "Lots.png",
        "include": True
    },
    {
        "Titre": "Give du Prof",
        "Description": "Give_du_prof",
        "Quantity": 10,
        "Prix": 0,
        "Image URL 1": "GIVEABO.png",
        "include": True
    },
    {
        "Titre": "Give Acheteur du Prof",
        "Description": "Give_acheteur_du_prof",
        "Quantity": 5,
        "Prix": 0,
        "Image URL 1": "GIVEACHETEUR.png",
        "include": True
    },
]

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
        LOCALE_MAP, RARITY_MAP, BASE_PRICE_BY_RARITY, BASE_LISTINGS
    )
