
import pandas as pd
from .vinted_utils import (
    format_rarity, format_locale_code, format_locale_full,
    format_id, generate_description
)


def generate_title(row, DEFAULT_LOCALE_GLOBAL):
    """
    Generate the title for a Vinted listing based on the row data.
    """
    name = row["Name"]
    rarity_code = format_rarity(row["Rarity"])
    formatted_id = format_id(row["Id"])
    locale_code = format_locale_code(row["Locale"], DEFAULT_LOCALE_GLOBAL)
    set_name = row["Set"] if pd.notna(row["Set"]) else ""
    return f"{name} [{locale_code}] ({rarity_code} - {formatted_id}) - {set_name}"


def parse_dex_csv(input_path, output_path, DEFAULTS):
    """
    Parse the input CSV file and generate a new CSV file with formatted titles and descriptions.
    """
    df = pd.read_csv(input_path, encoding="utf-16", sep=";")
    df_out = pd.DataFrame()
    df_out["Title"] = df.apply(
        lambda row: generate_title(row, DEFAULTS["LOCALE"]), axis=1)
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
