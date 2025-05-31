
import pandas as pd
import os
from .vinted_utils import (
    format_rarity, format_locale_code, format_locale_full,
    format_id, generate_description
)


def generate_title(row, DEFAULTS):
    """
    Generate the title for a Vinted listing based on the row data.
    """
    locale = DEFAULTS["LOCALE"]
    
    name = row["Name"]
    formatted_id = format_id(row["Id"])
    locale_code = format_locale_code(row["Locale"], locale)
    set_name = row["Set"] if pd.notna(row["Set"]) else ""

    if DEFAULTS["CATEGORY"]  == "Lot":
        return f"Lot de Cartes Pokémon {name}"
    else:
        return f"Carte Pokémon {name} - {row['Rarity']} - {set_name} ({formatted_id}) [{locale_code}]"


def generate_description(row, DEFAULTS):
    rarity_code = format_rarity(row["Rarity"])
    name = row["Name"]
    rarity = f"{rarity_code} {row['Rarity']}"
    series = row["Set"]
    set_name = row["Id"]
    locale_code = DEFAULTS["LOCALE"]
    condition_code = DEFAULTS["CONDITION"]

    locale_full = DEFAULTS["LOCALE_MAP"].get(locale_code, locale_code)
    condition_full = DEFAULTS["CONDITION_MAP"].get(condition_code, condition_code)

    if DEFAULTS["CATEGORY"]  == "Lot":
        template = DEFAULTS["DESC_TEMPLATE_LOT"]
    else:
        template = DEFAULTS["DESC_TEMPLATE_UNIT"]

    description = template.format(
        name=name,
        rarity=rarity,
        series=series,
        set=set_name,
        locale_full=locale_full,
        condition_full=condition_full
    )

    if condition_code == "Average":
        description += "\n⚠️ Défauts visibles : à compléter manuellement."

    return description


def parse_dex_csv(input_path, output_path, DEFAULTS):
    """
    Parse the input CSV file and generate a new CSV file with formatted titles and descriptions.
    """
    # os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.read_csv(input_path, encoding="utf-16", sep=";")
    df_out = pd.DataFrame()
    df_out["Title"] = df.apply(
        lambda row: generate_title(row, DEFAULTS), axis=1)
    df_out["Price"] = ""
    df_out["Category"] = DEFAULTS["CATEGORY"]
    df_out["Package"] = DEFAULTS["PACKAGE"]
    df_out["Condition"] = DEFAULTS["CONDITION"]
    df_out["Description"] = df.apply(
        lambda row: generate_description(row, DEFAULTS), axis=1)
    df_out["Picture_1"] = ""
    df_out["Picture_2"] = ""
    df_out.to_csv(output_path, index=False)
    print("✅ Fichier généré :", output_path)
