import pandas as pd

# 🔧 Variables globales à modifier selon la session
DATE_DE_VENTE = "2025-05-18"
PLATEFORME = "Whatnot"

# 🎁 Configurations des cas spécifiques
GIVE_DU_PROF = {
    "Produit": "Carte - RR",
    "Quantité": 1,
    "Prix": "0,30",
    "Remarques": "Give du prof"
}

GIVE_ACHETEUR_DU_PROF = {
    "Produit": "Carte - AR",
    "Quantité": 1,
    "Prix": "2,315",
    "Remarques": "Give acheteur du prof"
}

def create_row(row, produit="", quantite="", prix_p="", prix_vendu="", frais_even="",
               remarques=""):
    return {
        "Date de vente": DATE_DE_VENTE,
        "Plateforme": PLATEFORME,
        "Acheteur": row["buyer"],
        "Label": row["product name"],
        "Produit": produit,
        "QuantitéP": quantite,
        "PrixP": prix_p,
        "Bonus": "",
        "QuantitéB": "",
        "PrixB": "",
        "Langue": "JP",
        "Coût total (€)": "",
        "Prix vendu (€)": prix_vendu,
        "Frais Whatnot": "",
        "Frais éventuels (€)": frais_even,
        "Montant Perçu (€)": "",
        "URSSAF (€)": "",
        "Bénéfice (€)": "",
        "Liens / Factures": row["shipment manifest"],
        "Remarques": remarques
    }

def format_whatnot_csv(input_csv_path, output_csv_path):
    df = pd.read_csv(input_csv_path)

    if 'cancelled or failed' in df.columns:
        df = df[df['cancelled or failed'].isnull()]

    needed_columns = ['buyer', 'product name', 'sold price', 'shipment manifest']
    df = df[needed_columns]

    def transform_row(row):
        label = str(row["product name"]).lower()
        sold_price = str(row["sold price"]).replace("€", "").replace(",", ".")
        sold_price = "{:.2f}".format(float(sold_price)).replace(".", ",")

        if "give du prof" in label:
            return create_row(
                row,
                produit=GIVE_DU_PROF["Produit"],
                quantite=GIVE_DU_PROF["Quantité"],
                prix_p=GIVE_DU_PROF["Prix"],
                prix_vendu="",
                frais_even=sold_price,
                remarques=GIVE_DU_PROF["Remarques"]
            )

        elif "give acheteur du prof" in label:
            return create_row(
                row,
                produit=GIVE_ACHETEUR_DU_PROF["Produit"],
                quantite=GIVE_ACHETEUR_DU_PROF["Quantité"],
                prix_p=GIVE_ACHETEUR_DU_PROF["Prix"],
                prix_vendu="",
                frais_even=sold_price,
                remarques=GIVE_ACHETEUR_DU_PROF["Remarques"]
            )

        elif "lot" in label:
            return create_row(
                row,
                prix_vendu=sold_price,
                remarques="Give/Lot générique"
            )

        else:
            return create_row(
                row,
                produit="Carte - AR",
                quantite=1,
                prix_p="2,315",
                prix_vendu=sold_price
            )

    df_formatted = pd.DataFrame([transform_row(row) for _, row in df.iterrows()])

    # Trier : les produits définis d'abord, puis ceux à compléter à la main
    df_formatted.sort_values(by="Produit", key=lambda col: col.isna() | (col == ""), inplace=True)

    df_formatted.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ Fichier formaté exporté : {output_csv_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Nettoyer un export CSV Whatnot.")
    parser.add_argument("input_csv", help="Chemin vers le fichier CSV d'entrée")
    parser.add_argument("output_csv", help="Chemin vers le fichier CSV de sortie")
    args = parser.parse_args()

    format_whatnot_csv(args.input_csv, args.output_csv)
