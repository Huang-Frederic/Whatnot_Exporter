
import pandas as pd
import os


def link_images_to_csv(csv_path, image_folder):
    """
    Link images to the CSV file by adding two picture columns.
    """
    df = pd.read_csv(csv_path)
    images = sorted([img for img in os.listdir(image_folder)
                     if img.lower().endswith(('.jpg', '.jpeg', '.png'))])
    if len(images) < len(df) * 2:
        print("❌ Pas assez d'images pour le nombre d'articles.")
        return
    for i in range(len(df)):
        df.loc[i, "Picture_1"] = os.path.join(image_folder, images[2 * i])
        df.loc[i, "Picture_2"] = os.path.join(image_folder, images[2 * i + 1])
    df.to_csv(csv_path, index=False)
    print("✅ Images liées au fichier :", csv_path)
