import time
import os
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

CSV_PATH = "vinted_ready.csv"
VINTED_URL = "https://www.vinted.fr/items/new"
DEBUG_PORT = 9222


def is_debug_active(port=DEBUG_PORT):
    try:
        r = requests.get(f"http://localhost:{port}/json")
        return r.status_code == 200
    except Exception:
        return False


def connect_to_chrome():
    options = Options()
    options.debugger_address = f"127.0.0.1:{DEBUG_PORT}"
    driver = webdriver.Chrome(options=options)
    return driver


def fill_form(driver, row):
    print(f"📝 Remplissage de : {row['Title']}")
    driver.get(VINTED_URL)
    time.sleep(6)

    # === IMAGES ===
    try:
        file_input = driver.find_element(
            By.CSS_SELECTOR, 'input[type="file"]')
        paths = "\n".join([
            os.path.abspath(row["Picture_1"]),
            os.path.abspath(row["Picture_2"])
        ])
        file_input.send_keys(paths)
        print("🖼️ Images uploadées.")
    except Exception as e:
        print("❌ Erreur upload images :", e)

    # === TITRE ===
    try:
        title_input = driver.find_element(By.NAME, "title")
        title_input.clear()
        title_input.send_keys(row["Title"])
        time.sleep(3)
    except Exception:
        print("❌ Champ 'Titre' introuvable.")

    # === DESCRIPTION ===
    try:
        desc = row["Description"]
        desc_area = driver.find_element(
            By.CSS_SELECTOR, 'textarea[data-testid="description--input"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", desc_area)
        time.sleep(0.2)
        desc_area.click()
        desc_area.clear()
        for char in desc:
            desc_area.send_keys(char)
        print("📝 Description remplie.")
    except Exception as e:
        print(f"❌ Erreur Description :", e)

    # === CATÉGORIE : "Cartes à collectionner à l'unité" ===
    try:
        cat_input = driver.find_element(By.ID, "catalog_id")
        cat_input.click()
        time.sleep(1)
        driver.find_element(By.ID, "catalog-2309").click()  # Divertissement
        time.sleep(1)
        # Cartes à collectionner
        driver.find_element(By.ID, "catalog-3224").click()
        time.sleep(1)
        driver.find_element(By.ID, "catalog-3233").click()  # Cartes à l'unité
        time.sleep(3)
    except Exception as e:
        print("❌ Sélection catégorie échouée :", e)

    # === MARQUE : "Pokémon" ===
    try:
        brand_input = driver.find_element(By.ID, "brand_id")
        brand_input.click()
        time.sleep(1)
        driver.find_element(By.ID, "brand-191646").click()
        time.sleep(3)
    except Exception as e:
        print("❌ Sélection marque échouée :", e)

    # === ÉTAT : "Très bon état" ===
    try:
        condition_input = driver.find_element(By.ID, "status_id")
        condition_input.click()
        time.sleep(1)
        driver.find_element(By.ID, "condition-2").click()
        time.sleep(3)
    except Exception as e:
        print("❌ Sélection état échouée :", e)

    # === PRIX ===
    try:
        price_input = driver.find_element(By.NAME, "price")
        price_input.clear()
        price_input.send_keys(str(row["Price"]))
        time.sleep(3)
    except Exception:
        print("❌ Champ 'Prix' introuvable.")

    # === FORMAT DE COLIS : "Petit" ===
    try:
        driver.find_element(By.ID, "package-size-1").click()
        time.sleep(1)
    except Exception as e:
        print("❌ Sélection colis échouée :", e)

    print("✅ Fiche complétée automatiquement.")


def main():
    if not is_debug_active():
        print("❌ Chrome n'est pas lancé avec --remote-debugging-port=9222")
        print("👉 Lance d'abord launch_chrome_debug.bat")
        return

    if not os.path.exists(CSV_PATH):
        print(f"❌ Fichier introuvable : {CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH)
    if df.empty:
        print("❌ Le fichier CSV est vide.")
        return

    row = df.iloc[0]
    driver = connect_to_chrome()
    fill_form(driver, row)


if __name__ == "__main__":
    main()
