import pandas as pd

# === PARAMÈTRES GLOBAUX ===
INPUT_CSV = "vinted_data/ToList.csv"
OUTPUT_CSV = f"vinted_data/output_ToList.csv"
DEFAULTS = {
    "CONDITION_MAP": {
        "near_mint": "Très bon état (Near Mint), carte en excellent état (voir photos).",
    },

    "LOCALE_MAP": {
        "en": "Anglaise 🇬🇧",
        "fr": "Française 🇫🇷"
    },

    "DESC_TEMPLATE_UNIT": (
        "✨ Carte MTG Magic The Gathering {name} #{CollectorNumber} - {SetName} ({SetCode})\n"
        "📘 Version {locale_full}\n"
        "✅ État : {condition}\n\n"
        "🃏 Plein d'autres cartes sont disponibles sur mon profil mais aussi non listé ! N'hésitez pas à me demander pour la liste complète de ma collection !\n\n"
        "🛡️ Carte envoyée sous sleeve + toploader !\n"
        "🚀 Expédition rapide sous 1 à 2 jours ouvrés 📦\n"
        "🤝 Remise en main propre possible sur Paris / 92 / 95\n"
        "📸 Besoin de photos supplémentaires ? N'hésitez pas à me demander !\n\n"
        "📦 Possibilité de créer des lots personnalisés avec réduction sur les frais de port 🤑\n\n"
        "🌟 Je recherche activement une Lightning, Army of One V.1 #320 en version Anglaise ou Française, Foil ou Non Foil, pour échange ou achat (préférence pour RMP en IDF) 🌟\n"
    ),
}

def parse_mana_csv(input_csv, output_csv, defaults):
    df = pd.read_csv(input_csv)

    lang_order = {"fr": 1, "en": 0}

    df["lang_order"] = df["Language"].map(lang_order).fillna(99)

    df = df.sort_values(
        by=["lang_order", "Purchase price"],
        ascending=[True, False]
    )


    def build_title(row):
        name = row["Name"]
        num = row["Collector number"]
        setname = row["Set name"]
        setcode = row["Set code"]
        lang = row["Language"].upper()
        foil_tag = "Foil" if row["Foil"].strip(
        ).lower() == "foil" else "Non Foil"
        return f"{name} #{num} ({lang}) - {setname} ({setcode}) - {foil_tag}"

    def build_description(row):
        return defaults["DESC_TEMPLATE_UNIT"].format(
            name=row["Name"],
            CollectorNumber=row["Collector number"],
            SetName=row["Set name"],
            SetCode=row["Set code"],
            locale_full=defaults["LOCALE_MAP"].get(
                row["Language"], row["Language"]),
            condition=defaults["CONDITION_MAP"].get(
                row["Condition"], row["Condition"]),
        )

    df["title"] = df.apply(build_title, axis=1)
    df["description"] = df.apply(build_description, axis=1)

    df[["title", "description"]].to_csv(output_csv, index=False)
    print(f"✅ Export terminé : {output_csv}")


if __name__ == "__main__":
    parse_mana_csv(INPUT_CSV, OUTPUT_CSV, DEFAULTS)

# ✨ Carte MTG Magic The Gathering NAME #XX/53 (FR) - Final Fantasy Art Series (FIN-AS)
# 📘 Version Française
# ✅ État : Très bon état (Near Mint), carte en excellent état (voir photos).

# 🛡️ Carte envoyée sous sleeve + toploader !
# 🚀 Expédition rapide sous 1 à 2 jours ouvrés 📦
# 🤝 Remise en main propre possible sur Paris / 92 / 95

# 📸 Besoin de photos supplémentaires ? N'hésitez pas à me demander !
# 🃏 Plein d'autres cartes sont disponibles sur mon profil mais aussi non listé ! N'hésitez pas à me demander pour des communes ou non communes que je pourrais avoir.
# 📦 Possibilité de créer des lots personnalisés avec réduction sur les frais de port 🤑

# 🌟 Je recherche activement une Lightning, Army of One V.1 #320 en version Anglaise ou Française, Foil ou Non Foil, pour échange ou achat (préférence pour RMP en IDF) 🌟
