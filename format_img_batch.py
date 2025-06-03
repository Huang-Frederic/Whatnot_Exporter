import os
from PIL import Image, ImageEnhance
import tkinter as tk
from tkinter import filedialog


def crop_5_percent(image):
    width, height = image.size
    left = width * 0.05
    top = height * 0.05
    right = width * 0.95
    bottom = height * 0.95
    return image.crop((left, top, right, bottom))


def process_image(image_path, output_folder):
    img = Image.open(image_path).convert('RGB')

    # Rotation 180° (inversion complète)
    img = img.rotate(-90, expand=True)

    # Crop 5% de chaque côté
    img = crop_5_percent(img)

    # Filtre de luminosité (+10%)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)

    # Sauvegarde
    base_name = os.path.basename(image_path)
    new_name = f"REF_{base_name}"
    output_path = os.path.join(output_folder, new_name)
    img.save(output_path)


def main():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(
        title="Sélectionne le dossier contenant les images")

    if not folder:
        print("Aucun dossier sélectionné.")
        return

    output_folder = os.path.join(folder, f"output")
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
            image_path = os.path.join(folder, file)
            process_image(image_path, output_folder)

    print(f"✅ Traitement terminé. Images sauvegardées dans : {output_folder}")


if __name__ == "__main__":
    main()
