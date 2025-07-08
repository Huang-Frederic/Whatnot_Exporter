import pandas as pd
import re


def format_rarity(rarity: str) -> str:
    """
    Normalize a card's rarity into standard acronyms for Vinted listings.
    Returns: RR, RRR, AR, SAR, SR, P, M/P Ball, ERROR
    """
    if not isinstance(rarity, str):
        return "ERROR"

    normalized = rarity.strip().lower()

    if normalized in ["holo rare v", "double rare", "rare holo", "holo rare", "holo"]:
        return "RR"
    elif normalized in ["double rare holo"]:
        return "RRR"
    elif normalized in ["shiny ultra rare", "super rare", "full art rare", "ultra rare"]:
        return "SR"
    elif normalized in ["ar", "art rare", "illustration rare", "rare illustration", "trainer gallery holo rare"]:
        return "AR"
    elif normalized in ["sar", "special art rare", "rare ultra"]:
        return "SAR"
    elif normalized in ["promo", "promo holo", "holo promo", "holo rare promo"]:
        return "P"
    elif normalized in ["master ball holo", "poké ball holo"]:
        return "M/P Ball"
    else:
        return "_"


def format_locale_code(locale, default_locale_global):
    if locale == "Japan":
        return "JP"
    elif locale == "China":
        return "CN"
    else:
        return default_locale_global


def format_locale_full(locale, default_locale_global):
    if locale == "Japan":
        return "Japonais"
    elif locale == "China":
        return "Chinois"
    elif default_locale_global == "FR":
        return "Français"
    else:
        return "Anglais"


def format_id(card_id):
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
    rarity_code = format_rarity(row["Rarity"])
    name = row["Name"]
    rarity = f"{rarity_code} {row['Rarity']}"
    series = row["Set"]
    set_name = row["Id"]

    if row["Locale"] == "Japan":
        locale_code = "JP"
    elif row["Locale"] == "China":
        locale_code = "CN"
    elif row["Locale"] == "International":
        locale_code = DEFAULTS["LOCALE"]
    else:
        locale_code = format_locale_code(row["Locale"], DEFAULTS["LOCALE"])

    condition_code = DEFAULTS["CONDITION"]
    locale_full = DEFAULTS["LOCALE_MAP"].get(locale_code, locale_code)
    condition_full = DEFAULTS["CONDITION_MAP"].get(
        condition_code, condition_code)

    if DEFAULTS["CATEGORY"] == "Lot":
        template = DEFAULTS["DESC_TEMPLATE_LOT"]
    else:
        template = DEFAULTS["DESC_TEMPLATE_UNIT"]

    description = template.format(
        name=name,
        # rarity=rarity,
        series=series,
        set=set_name,
        locale_full=locale_full,
        condition_full=condition_full
    )

    if condition_code == "Average":
        description += "\n⚠️ Visible flaws: please update manually."

    return description
