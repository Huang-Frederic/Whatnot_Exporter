import pandas as pd
from .mappings import detect_locale, format_id, rarity_map, base_price_by_rarity
from .image_utils import get_card_image_direct, process_card_image

def format_whatnot_csv(input_path, output_path, background_path):
    df = pd.read_csv(input_path, encoding="utf-16", sep=";")

    df["Langue"] = df["Id"].map(detect_locale)
    df["Formatted ID"] = df["Id"].map(format_id)
    df["Titre"] = df["Name"] + " - " + df["Formatted ID"] + " - " + df["Langue"]

    df["Rareté"] = df["Rarity"].map(rarity_map)
    df["Rareté"] = df["Rareté"].fillna(df["Rarity"].apply(lambda r: "ERROR" if r.strip() == "—" else r))

    df["Description"] = df["Rareté"] + " - " + df["Set"] + " - " + df["Series"]
    df["Prix"] = df["Rareté"].map(base_price_by_rarity)

    df["Image URL 1"] = df["Id"].apply(lambda id_str: 
        process_card_image(
            id_str, 
            get_card_image_direct(id_str),
            background_path
        )
    )

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
        "Image URL 1": df["Image URL 1"],
        "Image URL 2": "",
        "Image URL 3": "",
        "Image URL 4": "",
        "Image URL 5": "",
        "Image URL 6": "",
        "Image URL 7": "",
        "Image URL 8": ""
    })

    output_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"✅ CSV exporté : {output_path}")
