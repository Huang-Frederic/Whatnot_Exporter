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

base_price_by_rarity = {
    "SAR": 10.0,
    "SR": 8.0,
    "AR": 5.0,
    "RRR": 3.0,
    "RR": 2.0,
    "Shiny": 4.0,
    "Other": 1.0,
    "ERROR": 0.5
}

def format_id(id_str):
    try:
        return id_str.split("_")[-1].replace("-", " ")
    except:
        return id_str

def detect_locale(id_str):
    if "_" in id_str:
        prefix = id_str.split("_")[0].lower()
        return locale_map.get(prefix, locale_map["default"])
    return locale_map["default"]
