from PIL import Image
import requests
from io import BytesIO
import os

def fusionner_image_avec_fond(image_url, background_path, output_path, output_name):
    try:
        # 1. Charger l’image de la carte depuis l’URL
        response = requests.get(image_url, verify=False)
        carte = Image.open(BytesIO(response.content)).convert("RGBA")

        # 2. Charger l’image de fond depuis un fichier local
        fond = Image.open(background_path).convert("RGBA")

        # 3. Redimensionner la carte (50% plus petite que le fond)
        fond_w, fond_h = fond.size
        carte_w, carte_h = int(fond_w * 0.65), int(fond_h * 0.65)
        carte = carte.resize((carte_w, carte_h), Image.Resampling.LANCZOS)


        # 4. Centrer la carte sur le fond
        position = ((fond_w - carte_w) // 2, (fond_h - carte_h) // 2)
        fond.paste(carte, position, carte)  # Le 3e arg permet la transparence

        # 5. Sauvegarder le résultat
        os.makedirs(output_path, exist_ok=True)
        final_path = os.path.join(output_path, output_name)
        fond.save(final_path)
        print(f"✅ Image sauvegardée : {final_path}")
        return final_path

    except Exception as e:
        print(f"❌ Erreur fusion image : {e}")
        return ""

fusionner_image_avec_fond(
    image_url="https://static.dextcg.com/cards/jpn_s6a/77.png",
    background_path="background.jpg",
    output_path="whatnot-images",
    output_name="jpn_s6a-77.png"
)
