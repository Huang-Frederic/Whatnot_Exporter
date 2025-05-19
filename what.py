import pandas as pd

# 🔧 Variables globales à modifier selon la session
DATE_DE_VENTE = "2025-05-18"
PLATEFORME = "Whatnot"

def format_whatnot_csv(input_csv_path, output_csv_path):
    """
    Transforme un export brut Whatnot vers un format compatible avec ton Google Sheet de ventes.
    """

    # Lecture du fichier CSV brut
    df = pd.read_csv(input_csv_path)

    # Étape 1 : supprimer les lignes annulées
    if 'cancelled or failed' in df.columns:
        df = df[df['cancelled or failed'].isnull()]

    # Étape 2 : conserver uniquement les colonnes utiles
    needed_columns = ['buyer', 'product name', 'sold price', 'shipment manifest']
    df = df[needed_columns]

    # Étape 3 : transformation personnalisée
    def transform_row(row):
        label = str(row["product name"]).lower()
        sold_price = str(row["sold price"]).replace("€", "").replace(",", ".")
        sold_price = "{:.2f}".format(float(sold_price)).replace(".", ",")
        lien = row["shipment manifest"]

        if "give du prof" in label:
            return {
                "Date de vente": DATE_DE_VENTE,
                "Plateforme": PLATEFORME,
                "Acheteur": row["buyer"],
                "Label": row["product name"],
                "Produit": "Carte - RR",
                "QuantitéP": 1,
                "PrixP": "0,30",
                "Bonus": "",
                "QuantitéB": "",
                "PrixB": "",
                "Langue": "JP",
                "Coût total (€)": "",
                "Prix vendu (€)": "",
                "Frais Whatnot": "",
                "Frais éventuels (€)": sold_price,
                "Montant Perçu (€)": "",
                "URSSAF (€)": "",
                "Bénéfice (€)": "",
                "Liens / Factures": lien,
                "Remarques": "Give du prof"
            }

        elif "give acheteur du prof" in label:
            return {
                "Date de vente": DATE_DE_VENTE,
                "Plateforme": PLATEFORME,
                "Acheteur": row["buyer"],
                "Label": row["product name"],
                "Produit": "Carte - AR",
                "QuantitéP": 1,
                "PrixP": "2,315",
                "Bonus": "",
                "QuantitéB": "",
                "PrixB": "",
                "Langue": "JP",
                "Coût total (€)": "",
                "Prix vendu (€)": "",
                "Frais Whatnot": "",
                "Frais éventuels (€)": sold_price,
                "Montant Perçu (€)": "",
                "URSSAF (€)": "",
                "Bénéfice (€)": "",
                "Liens / Factures": lien,
                "Remarques": "Give acheteur du prof"
            }

        elif "lot" in label:
            # Cas générique d'un lot ou give quelconque
            return {
                "Date de vente": DATE_DE_VENTE,
                "Plateforme": PLATEFORME,
                "Acheteur": row["buyer"],
                "Label": row["product name"],
                "Produit": "",
                "QuantitéP": "",
                "PrixP": "",
                "Bonus": "",
                "QuantitéB": "",
                "PrixB": "",
                "Langue": "JP",
                "Coût total (€)": "",
                "Prix vendu (€)": sold_price,
                "Frais Whatnot": "",
                "Frais éventuels (€)": "",
                "Montant Perçu (€)": "",
                "URSSAF (€)": "",
                "Bénéfice (€)": "",
                "Liens / Factures": lien,
                "Remarques": "Give/Lot générique"
            }

        else:
            # Cas classique : vente d'une carte AR
            return {
                "Date de vente": DATE_DE_VENTE,
                "Plateforme": PLATEFORME,
                "Acheteur": row["buyer"],
                "Label": row["product name"],
                "Produit": "Carte - AR",
                "QuantitéP": 1,
                "PrixP": "2,315",
                "Bonus": "",
                "QuantitéB": "",
                "PrixB": "",
                "Langue": "JP",
                "Coût total (€)": "",
                "Prix vendu (€)": sold_price,
                "Frais Whatnot": "",
                "Frais éventuels (€)": "",
                "Montant Perçu (€)": "",
                "URSSAF (€)": "",
                "Bénéfice (€)": "",
                "Liens / Factures": lien,
                "Remarques": ""
            }

    # Appliquer la transformation à toutes les lignes
    df_formatted = pd.DataFrame([transform_row(row) for _, row in df.iterrows()])

    # Exporter au format CSV compatible Google Sheet
    df_formatted.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ Fichier formaté exporté : {output_csv_path}")

# Exemple d’utilisation :
# format_whatnot_csv("export_whatnot.csv", "export_google_sheet.csv")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Nettoyer un export CSV Whatnot.")
    parser.add_argument("input_csv", help="Chemin vers le fichier CSV d'entrée")
    parser.add_argument("output_csv", help="Chemin vers le fichier CSV de sortie")
    args = parser.parse_args()

    format_whatnot_csv(args.input_csv, args.output_csv)