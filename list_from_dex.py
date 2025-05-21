import pandas as pd

# Dictionnaires de mappage
locale_map = {
    "jpn": "JP",
    "scn": "CN",
    "default": "FR"
}

rarity_map = {
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

# Prix de base par rareté (modifiable selon tes besoins)
base_price_by_rarity = {
    "SAR": 5.0,
    "SR": 3.0,
    "AR": 3.0,
    "RRR": 1.0,
    "RR": 1.0,
    "Shiny": 1.0,
    "Other": 1.0,
    "ERROR": 0.5
}


def format_id(id_str):
    try:
        right_part = id_str.split("_")[-1]
        return right_part.replace("-", " ")
    except:
        return id_str


def detect_locale(id_str):
    if "_" in id_str:
        prefix = id_str.split("_")[0].lower()
        return locale_map.get(prefix, locale_map["default"])
    return locale_map["default"]


def format_whatnot_csv(input_path, output_path):
    df = pd.read_csv(input_path, encoding="utf-16", sep=";")

    df["Langue"] = df["Id"].map(detect_locale)
    df["Formatted ID"] = df["Id"].map(format_id)
    df["Titre"] = df["Name"] + " - " + \
        df["Formatted ID"] + " - " + df["Langue"]

    df["Rareté"] = df["Rarity"].map(rarity_map)
    df["Rareté"] = df["Rareté"].fillna(df["Rarity"].apply(
        lambda r: "ERROR" if r.strip() == "—" else r))

    df["Description"] = df["Rareté"] + " - " + df["Set"] + " - " + df["Series"]
    df["Prix"] = df["Rareté"].map(base_price_by_rarity)

    output_df = pd.DataFrame({
        "Catégorie": "Trading Card Games",
        "Sous-catégorie": "Cartes Pokémon",
        "Titre": df["Titre"],
        "Description": df["Description"],
        "Quantité": df["Quantity"],
        "Type": "Auction",
        "Prix": df["Prix"],
        "Profil de livraison": "De 0 à <20\u00a0grammes",
        "Matières dangereuses": "Not Hazmat",
        "État": "Near Mint",
        "Coût par article": "",
        "SKU": "",
        "Image URL 1": "",
        "Image URL 2": "",
        "Image URL 3": "",
        "Image URL 4": "",
        "Image URL 5": "",
        "Image URL 6": "",
        "Image URL 7": "",
        "Image URL 8": ""
    })

    output_df.to_csv(output_path, index=False, encoding="utf-8")

# Exemple d'utilisation
# format_whatnot_csv("mon_stock.csv", "listing_whatnot.csv")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Formatter un CSV Dex vers le listing Whatnot.")
    parser.add_argument(
        "input_csv", help="Chemin vers le fichier CSV d'entrée")
    parser.add_argument(
        "output_csv", help="Chemin vers le fichier CSV de sortie")
    args = parser.parse_args()

    format_whatnot_csv(args.input_csv, args.output_csv)
