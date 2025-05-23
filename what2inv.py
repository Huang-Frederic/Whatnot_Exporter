import csv
import re
from datetime import datetime
import argparse
import os

# === Constantes globales ===

BASE_PRICE_BY_RARITY = {
    "SAR": 2.89, "SR": 2.92, "AR": 1.98,
    "RRR": 0.84, "RR": 0.30, "Shiny": 0.7,
    "Other": 0.40, "ERROR": -999
}

LANGUAGES = ["JP", "EN", "FR", "DE", "IT", "ES", "CN"]
RARITIES = list(BASE_PRICE_BY_RARITY.keys())

PLATFORM = "Whatnot"
GIVEAWAY_ENTRY = "1RR"  # À ajuster selon le live
GIVEAWAY_LANG = "JP"    # À ajuster selon le live

# === Fonctions utilitaires ===


def parse_product_description(description):
    """
    Extrait la ou les raretés et quantités depuis la description du produit.
    """
    if "give" in description.lower():
        match = re.match(r"(\d{0,2})([A-Za-z]+)", GIVEAWAY_ENTRY.strip())
        qty = int(match.group(1)) if match and match.group(1) else 1
        rarity = match.group(2) if match else "ERROR"
        return [(rarity, qty)]

    base_part = description.split('-')[0].strip()
    matches = re.findall(r"(\d{0,2})([A-Za-z]+)", base_part)
    results = []

    for qty, rarity in matches:
        quantity = int(qty) if qty.isdigit() else 1
        if rarity in RARITIES:
            results.append((rarity, quantity))
        else:
            results.append(("ERROR", quantity))

    return results


def fmt(x):
    return f"{x:.2f}".replace('.', ',') if isinstance(x, float) else x


def extract_language(product_name, is_giveaway=False):
    """
    Détecte la langue dans le nom du produit ou utilise celle du giveaway.
    """
    if is_giveaway:
        return GIVEAWAY_LANG
    for lang in LANGUAGES:
        if f" {lang}" in product_name:
            return lang
    return ""


def process_csv(input_file, output_file):
    """
    Transforme un fichier CSV brut de ventes Whatnot en un tableau formaté.
    """
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []

        for row in reader:
            # Ignorer les ventes annulées ou échouées
            if row.get("cancelled or failed", "").strip():
                continue

            # Date
            placed_at = row["placed at"]
            try:
                date_vente = datetime.strptime(
                    placed_at, "%Y-%m-%d %H:%M:%S.%f").strftime("%d/%m/%Y")
            except ValueError:
                date_vente = datetime.strptime(
                    placed_at, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")

            acheteur = row["buyer"]
            label = row["product name"]
            description = row["product description"]
            is_give = "give" in description.lower()

            produit_infos = parse_product_description(description)

            # Produit principal
            produit, quantite_p = produit_infos[0] if produit_infos else (
                "ERROR", 0)
            prix_p = BASE_PRICE_BY_RARITY.get(produit, 0.5)

            # Bonus éventuel
            bonus, quantite_b = produit_infos[1] if len(
                produit_infos) > 1 else ("", "")
            prix_b = BASE_PRICE_BY_RARITY.get(
                bonus, 0.0) if bonus else ""

            langue = extract_language(label, is_give)

            # Prix vendu
            try:
                prix_vendu = float(row["sold price"].replace("€", "").strip())
            except ValueError:
                prix_vendu = 0.0

            lien = row["shipment manifest"]
            remarques = "GIVEAWAY" if prix_vendu == 0 else ""

            # Ligne complète
            rows.append([
                date_vente, PLATFORM, acheteur, label,
                f"Carte - {produit}", quantite_p, fmt(prix_p),
                f"Carte - {bonus}" if bonus else "", quantite_b, fmt(
                    prix_b) if prix_b != "" else "",
                langue, "", fmt(
                    prix_vendu), "", "", "", "", "", lien, remarques
            ])

    # En-têtes du fichier de sortie
    headers = [
        "Date de vente", "Plateforme", "Acheteur", "Label", "Produit", "QuantitéP", "PrixP",
        "Bonus", "QuantitéB", "PrixB", "Langue", "Coût total (€)", "Prix vendu (€)",
        "Frais Whatnot", "Frais éventuels (€)", "Montant Perçu (€)", "URSSAF (€)", "Bénéfice (€)",
        "Liens / Factures", "Remarques"
    ]

    # Écriture du fichier de sortie
    with open(output_file, mode='w', newline='', encoding='utf-8') as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow(headers)
        writer.writerows(rows)


# === Exemple d'exécution ===

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exporter un fichier formaté pour Whatnot.")
    parser.add_argument(
        "input_csv", help="Chemin vers le fichier CSV d'entrée")
    args = parser.parse_args()

    os.makedirs("data_output", exist_ok=True)
    input_filename = os.path.basename(args.input_csv)
    output_path = os.path.join("data_output", f"formatted_{input_filename}")

    process_csv(
        args.input_csv, output_path
    )
    print(f"✅ CSV exporté : {output_path}")
