import os
from PIL import Image
import requests
from io import BytesIO
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GITHUB_BASE_URL = "https://raw.githubusercontent.com/Huang-Frederic/Whatnot_Exporter/master/whatnot-images"

def get_card_image_direct(card_id):
    try:
        parts = card_id.split("-")
        if len(parts) != 2:
            raise ValueError("Format d'ID inattendu.")
        return f"https://static.dextcg.com/cards/{parts[0]}/{parts[1]}.png"
    except Exception as e:
        print(f"❌ Erreur format image pour l'ID {card_id} : {e}")
        return ""

def process_card_image(card_full_id, image_url, background_path, save_folder="whatnot-images"):
    try:
        os.makedirs(save_folder, exist_ok=True)
        response = requests.get(image_url, verify=False)
        if response.status_code == 200:
            carte = Image.open(BytesIO(response.content)).convert("RGBA")
        else:
            print(f"❌ Image non trouvée pour {card_full_id} (status: {response.status_code})")
            return ""

        carte = Image.open(BytesIO(response.content)).convert("RGBA")
        fond = Image.open(background_path).convert("RGBA")

        fond_w, fond_h = fond.size
        carte = carte.resize((int(fond_w * 0.6), int(fond_h * 0.6)), Image.Resampling.LANCZOS)

        pos = ((fond_w - carte.width) // 2, (fond_h - carte.height) // 2)
        fond.paste(carte, pos, carte)

        filename = f"{card_full_id}.png"
        full_path = os.path.join(save_folder, filename)
        fond.save(full_path)

        return f"{GITHUB_BASE_URL}/{filename}"
    except Exception as e:
        print(f"❌ Error for {card_full_id}: {e}")
        return ""
