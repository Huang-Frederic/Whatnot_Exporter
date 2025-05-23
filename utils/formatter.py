import pandas as pd
from tqdm import tqdm
from .image_utils import get_card_image_url, generate_card_img
import os


def format_id(id_str):
    try:
        return id_str.split("_")[-1].replace("-", " ")
    except:
        return id_str


def detect_locale(id_str, locale_map):
    if "_" in id_str:
        prefix = id_str.split("_")[0].lower()
        return locale_map.get(prefix, locale_map["default"])
    return locale_map["default"]


def load_base_listings(base_listing, github_url):
    base_rows = []
    for base in base_listing:
        if base.get("include", False):
            base_rows.append({
                "Catégorie": "Trading Card Games",
                "Sous-catégorie": "Cartes Pokémon",
                "Titre": base["Titre"],
                "Description": base["Description"],
                "Quantité": base["Quantity"],
                "Type": "Auction" if base["Prix"] > 0 else "Giveaway",
                "Prix": base["Prix"],
                "Profil de livraison": "De 0 à <20\u00a0grammes",
                "Matières dangereuses": "Not Hazmat",
                "État": "Near Mint",
                "Coût par article": "",
                "SKU": "",
                "Image URL 1": f"{github_url}/base{['Image URL 1']}",
                "Image URL 2": "",
                "Image URL 3": "",
                "Image URL 4": "",
                "Image URL 5": "",
                "Image URL 6": "",
                "Image URL 7": "",
                "Image URL 8": ""
            })
    return base_rows


def annex_whatnot_format(df, locale_map, rarity_map, base_price_by_rarity):
    df["Langue"] = df["Id"].apply(
        lambda id_str: detect_locale(id_str, locale_map))
    df["Formatted ID"] = df["Id"].map(format_id)
    df["Titre"] = df["Name"] + " - " + \
        df["Formatted ID"] + " - " + df["Langue"]

    df["Rareté"] = df["Rarity"].map(rarity_map)
    df["Rareté"] = df["Rareté"].fillna(df["Rarity"].apply(
        lambda r: "ERROR" if r.strip() == "—" else r))
    df["Description"] = df["Rareté"] + " - " + df["Set"] + " - " + df["Series"]
    df["Prix"] = df["Rareté"].map(base_price_by_rarity)

    return df


def annex_images(df, github_url, background_path):
    image_urls = []
    for id_str in tqdm(df["Id"], desc="🖼️ Génération des images Whatnot"):
        image_filename = f"whatnot-images/{id_str}.png"
        if os.path.exists(image_filename):
            image_urls.append(f"{github_url}/{id_str}.png")
        else:
            url = get_card_image_url(id_str)
            final_path = generate_card_img(
                id_str, url, github_url, background_path)
            image_urls.append(final_path)
    df["Image URL 1"] = image_urls
    return df


def build_output_df(df):
    return pd.DataFrame({
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


def format_whatnot_csv(input_path, output_path, github_url, background_path, locale_map, rarity_map, base_price_by_rarity, base_listing):
    df = pd.read_csv(input_path, encoding="utf-16", sep=";")
    df = annex_whatnot_format(df, locale_map, rarity_map, base_price_by_rarity)
    df = annex_images(df, github_url, background_path)
    base_df = pd.DataFrame(load_base_listings(base_listing, github_url))
    output_df = build_output_df(df)
    output_df = pd.concat([base_df, output_df], ignore_index=True)

    output_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"✅ CSV exporté : {output_path}")
