import pandas as pd
from .vinted_utils import (
    format_rarity, format_locale_code, format_locale_full,
    format_id, generate_description
)


def preprocess(df, DEFAULTS):
    set_translation_map = {
        # Scarlet & Violet era
        "Destined Rivals": "Rivalités Destinées",
        "Journey Together": "Aventure Ensemble",
        "Prismatic Evolutions": "Évolutions Prismatiques",
        "Surging Sparks": "Étincelles Déferlantes",
        "Stellar Crown": "Couronne Stellaire",
        "Shrouded Fable": "Fable Nébuleuse",
        "Twilight Masquerade": "Mascarade Crépusculaire",
        "Temporal Forces": "Forces Temporelles",
        "Paldean Fates": "Destinées de Paldea",
        "Paradox Rift": "Faille Paradoxe",
        "151": "151",
        "Obsidian Flames": "Flammes Obsidiennes",
        "Paldea Evolved": "Evolution à Paldea",
        "Scarlet & Violet": "Écarlate & Violet",
        "Black Star Promos": "Promos Écarlate & Violet",
        "Scarlet & Violet Promos": "Promos Écarlate & Violet",

        # Sword & Shield era
        "Crown Zenith": "Zenith Suprême",
        "Crown Zenith: Galarian Gallery": "Zenith Suprême : Galerie de Galar",
        "Silver Tempest": "Tempête Argenté",
        "Lost Origin": "Origine Perdue",
        "Pokémon GO": "Pokémon GO",
        "Astral Radiance": "Astres Radieux",
        "Brilliant Stars": "Stars Etincelantes",
        "Fusion Strike": "Poing de Fusion",
        "Celebrations": "Celebrations",
        "Evolving Skies": "Evolution Céleste",
        "Chilling Reign": "Règne de Glace",
        "Battle Styles": "Styles de Combat",
        "Shining Fates": "Destinées Radieuses",
        "Vivid Voltage": "Voltage Éclatant",
        "Champion's Path": "Voie du Maître",
        "Darkness Ablaze": "Ténèbres Embrasées",
        "Rebel Clash": "Clash des Rebelles",
        "Sword & Shield": "Épée & Bouclier",
        "Black Star Promos": "Promos Épée & Bouclier",
    }

    series_translation_map = {
        "Scarlet & Violet": "Écarlate & Violet",
        "Sword & Shield": "Épée & Bouclier",
        "Sun & Moon": "Soleil & Lune",
        "XY": "XY",
        "Black & White": "Noir & Blanc",
        "HeartGold & SoulSilver": "HeartGold & SoulSilver",
        "Platinum": "Platinum",
        "Diamond & Pearl": "Diamant & Perle",
        "EX": "EX",
        "POP": "POP",
        "e-Series": "e‑Series",
        "Neo": "Neo",
        "Original": "Original",
        "Call of Legends": "Appel des Légendes",
        "Legendary": "Legendary",
        "PCG": "PCG",
    }

    if DEFAULTS.get("LOCALE") == "FR":
        df["Set"] = df["Set"].map(lambda x: set_translation_map.get(x, x))
        df["Series"] = df["Series"].map(
            lambda x: series_translation_map.get(x, x))

    def localize_name(name):
        if DEFAULTS.get("LOCALE") == "FR" and "'s " in name:
            parts = name.split("'s ")
            if len(parts) == 2:
                x, rest = parts
                return f"{rest} de {x}"
        return name

    df["Name"] = df["Name"].map(localize_name)

    df["Rarity"] = df.apply(
        lambda row: row["Variant"] if row["Variant"] in [
            "Master Ball Holo", "Poké Ball Holo"] else row["Rarity"],
        axis=1
    )

    df = df[df["Quantity"] > 0].copy()
    return df


def generate_title(row, DEFAULTS):
    name = row["Name"]
    formatted_id = format_id(row["Id"])
    set_name = row["Set"] if pd.notna(row["Set"]) else ""

    if row["Locale"] == "Japan":
        locale_code = "JP"
    elif row["Locale"] == "China":
        locale_code = "CN"
    elif row["Locale"] == "International":
        locale_code = DEFAULTS["LOCALE"]
    else:
        locale_code = format_locale_code(row["Locale"], DEFAULTS["LOCALE"])

    if DEFAULTS["CATEGORY"] == "Lot":
        return f"Lot de Cartes Pokémon {name}"
    else:
        return f"Carte Pokémon {name} - {row['Rarity']} - {set_name} ({formatted_id}) [{locale_code}]"


def parse_dex_csv(input_path, output_path, DEFAULTS):
    df = pd.read_csv(input_path, encoding="utf-16", sep=";")
    df = preprocess(df, DEFAULTS)

    df_out = pd.DataFrame()
    df_out["Title"] = df.apply(
        lambda row: generate_title(row, DEFAULTS), axis=1)
    df_out["Description"] = df.apply(
        lambda row: generate_description(row, DEFAULTS), axis=1)
    df_out["Price"] = ""
    df_out["Category"] = DEFAULTS["CATEGORY"]
    df_out["Package"] = DEFAULTS["PACKAGE"]
    df_out["Condition"] = DEFAULTS["CONDITION"]
    df_out["Picture_1"] = ""
    df_out["Picture_2"] = ""
    df_out.to_csv(output_path, index=False)
    print("✅ File generated:", output_path)
