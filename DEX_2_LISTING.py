import argparse
from utils.formatter import format_whatnot_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exporter un fichier formaté pour Whatnot.")
    parser.add_argument("input_csv", help="Chemin vers le fichier CSV d'entrée")
    parser.add_argument("output_csv", help="Chemin vers le fichier CSV de sortie")
    parser.add_argument("--background", default="assets/background.jpg", help="Fond pour les images")
    args = parser.parse_args()

    format_whatnot_csv(args.input_csv, args.output_csv, args.background)
