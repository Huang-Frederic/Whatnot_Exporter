import pandas as pd

# === PARAMÈTRES GLOBAUX ===
INPUT_CSV = "vinted_data/manabox.csv"
OUTPUT_CSV = f"vinted_data/output_manabox.csv"
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
        "🛡️ Carte envoyée sous sleeve + toploader !\n"
        "🚀 Expédition rapide sous 1 à 2 jours ouvrés 📦\n"
        "🤝 Remise en main propre possible sur Paris / 92 / 95\n"
        "📸 Besoin de photos supplémentaires ? N'hésitez pas à me demander !\n\n"
        "🃏 Plein d'autres cartes sont disponibles sur mon profil mais aussi non listé ! N'hésitez pas à me demander pour des communes ou non communes que je pourrais avoir.\n"
        "📦 Possibilité de créer des lots personnalisés avec réduction sur les frais de port 🤑\n"
    ),
}


def parse_mana_csv(input_csv, output_csv, defaults):
    df = pd.read_csv(input_csv)

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
