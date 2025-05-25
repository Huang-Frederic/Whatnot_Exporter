import csv
import re
from datetime import datetime


def parse_product_description(description, giveaway_entry, rarities):
    if "give" in description.lower():
        match = re.match(r"(\d{0,2})([A-Za-z]+)", giveaway_entry.strip())
        qty = int(match.group(1)) if match and match.group(1) else 1
        rarity = match.group(2) if match else "ERROR"
        return [(rarity, qty)]

    base_part = description.split('-')[0].strip()
    matches = re.findall(r"(\d{0,2})([A-Za-z]+)", base_part)
    results = []

    for qty, rarity in matches:
        quantity = int(qty) if qty.isdigit() else 1
        if rarity in rarities:
            results.append((rarity, quantity))
        else:
            results.append(("ERROR", quantity))

    return results


def extract_language(product_name, is_giveaway, languages, giveaway_lang):
    if is_giveaway:
        return giveaway_lang
    for lang in languages:
        if f" {lang}" in product_name:
            return lang
    return ""


def fmt(x):
    return f"{x:.2f}".replace('.', ',') if isinstance(x, float) else x


def process_csv(input_file, output_file,
                base_price_by_rarity,
                languages,
                platform,
                giveaway_entry,
                giveaway_lang):
    rarities = list(base_price_by_rarity.keys())

    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []

        for row in reader:
            if row.get("cancelled or failed", "").strip():
                continue

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

            produit_infos = parse_product_description(
                description, giveaway_entry, rarities)

            produit, quantite_p = produit_infos[0] if produit_infos else (
                "ERROR", 0)
            prix_p = base_price_by_rarity.get(produit, 0.5)

            bonus, quantite_b = produit_infos[1] if len(
                produit_infos) > 1 else ("", "")
            prix_b = base_price_by_rarity.get(bonus, 0.0) if bonus else ""

            langue = extract_language(label, is_give, languages, giveaway_lang)

            try:
                prix_vendu = float(row["sold price"].replace("€", "").strip())
            except ValueError:
                prix_vendu = 0.0

            lien = row["shipment manifest"]
            remarques = "GIVEAWAY" if prix_vendu == 0 else ""

            rows.append([
                date_vente, platform, acheteur, label,
                f"Carte - {produit}", quantite_p, fmt(prix_p),
                f"Carte - {bonus}" if bonus else "", quantite_b, fmt(
                    prix_b) if prix_b != "" else "",
                langue, "", fmt(
                    prix_vendu), "", "", "", "", "", lien, remarques
            ])

    headers = [
        "Date de vente", "Plateforme", "Acheteur", "Label", "Produit", "QuantitéP", "PrixP",
        "Bonus", "QuantitéB", "PrixB", "Langue", "Coût total (€)", "Prix vendu (€)",
        "Frais Whatnot", "Frais éventuels (€)", "Montant Perçu (€)", "URSSAF (€)", "Bénéfice (€)",
        "Liens / Factures", "Remarques"
    ]

    with open(output_file, mode='w', newline='', encoding='utf-8') as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow(headers)
        writer.writerows(rows)
