
import pandas as pd
import re


def format_rarity(rarity):
    """
    Format the full name of the rarity to an acronym.
    egg: "Rare Holo" -> "RH"
    """
    if pd.isna(rarity):
        return ""
    return "".join(word[0].upper() for word in rarity.split())


def format_locale_code(locale, default_locale_global):
    """
    Format the Locale Name to the Acrronym
    e.g. "Japan" -> "JP"
    """
    if locale == "Japan":
        return "JAP"
    elif locale == "China":
        return "CN"
    else:
        return default_locale_global


def format_locale_full(locale, default_locale_global):
    """
    Format the Locale Name to the descriptive Full Name
    e.g. "Japan" -> "Japonais"
    """
    if locale == "Japan":
        return "Japonais"
    elif locale == "China":
        return "Chinois"
    elif default_locale_global == "FR":
        return "Français"
    else:
        return "Anglais"


def format_id(card_id):
    """
    Format the Card ID to a more readable format
    e.g. "jp_sv9a-70" -> "SV9A 70"
    """
    if pd.isna(card_id):
        return ""
    card_id = re.sub(r"^(jpn_|cn_|eng_|fr_)", "", card_id, flags=re.IGNORECASE)
    match = re.match(r"([a-zA-Z0-9]+)-(\d+)", card_id)
    if match:
        set_code = match.group(1).upper()
        number = match.group(2)
        return f"{set_code} {number}"
    return card_id


def generate_description(row, DEFAULTS):
    """
    Generate the Description for the Card according to the template
    """
    return DEFAULTS["DESC_TEMPLATE"].format(
        name=row["Name"],
        rarity=row["Rarity"] if pd.notna(row["Rarity"]) else "",
        series=row["Series"] if pd.notna(row["Series"]) else "",
        set=row["Set"] if pd.notna(row["Set"]) else "",
        locale_full=format_locale_full(row["Locale"], DEFAULTS["LOCALE"]),
        condition=DEFAULTS["CONDITION"]
    )
