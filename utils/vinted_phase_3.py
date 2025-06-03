import os
import time
import pandas as pd
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import random

DEBUG_PORT = 9222
VINTED_URL = "https://www.vinted.fr/items/new"


def is_debug_active(port=DEBUG_PORT):
    try:
        r = requests.get(f"http://localhost:{port}/json")
        return r.status_code == 200
    except Exception:
        return False


def connect_to_chrome():
    print(f"🔍 Connexion à Chrome sur le port {DEBUG_PORT} ...")
    options = Options()
    options.debugger_address = f"127.0.0.1:{DEBUG_PORT}"
    driver = webdriver.Chrome(options=options)
    print("✅ Connecté à Chrome.")
    random_sleep(1, 1.25)
    return driver


def random_sleep(min_s=0.5, max_s=2.0):
    duration = random.uniform(min_s, max_s)
    time.sleep(duration)


def fill_form(driver, row):
    print("➡️ Remplissage du formulaire...")

    # === IMAGES ===
    try:
        file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        paths = "\n".join([
            os.path.abspath(row["Picture_1"]),
            os.path.abspath(row["Picture_2"])
        ])
        file_input.send_keys(paths)
        print("🖼️ Images uploadées.")
        random_sleep(1, 1.25)
    except Exception as e:
        print("❌ Erreur upload images :", e)

    # === TITRE ===
    try:
        title_input = driver.find_element(By.NAME, "title")
        title_input.clear()
        title_input.send_keys(row["Title"])
        print("🏷️ Titre rempli.")
        random_sleep(1, 1.25)
    except Exception:
        print("❌ Champ 'Titre' introuvable.")

    # === DESCRIPTION ===
    try:
        desc = row["Description"]
        desc_area = driver.find_element(
            By.CSS_SELECTOR, 'textarea[data-testid="description--input"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", desc_area)
        random_sleep(1, 1.25)
        desc_area.click()
        desc_area.clear()
        for char in desc:
            desc_area.send_keys(char)

        print("📝 Description remplie.")
        random_sleep(2, 2.25)
    except Exception as e:
        print(f"❌ Erreur Description :", e)

    # === CATÉGORIE ===
    try:
        print("🔽 Sélection catégorie...")
        cat_input = driver.find_element(By.ID, "catalog_id")
        cat_input.click()
        random_sleep(0.5, 0.75)
        driver.find_element(By.ID, "catalog-2309").click()
        random_sleep(0.5, 0.75)
        driver.find_element(By.ID, "catalog-3224").click()
        random_sleep(0.5, 0.75)
        driver.find_element(By.ID, "catalog-3233").click()
        print("✅ Catégorie sélectionnée.")
        random_sleep(2, 2.25)
    except Exception as e:
        print("❌ Sélection catégorie échouée :", e)

    # === MARQUE ===
    try:
        print("🔽 Sélection marque...")
        brand_input = driver.find_element(By.ID, "brand_id")
        brand_input.click()
        random_sleep(1, 1.25)
        driver.find_element(By.ID, "brand-191646").click()
        print("✅ Marque sélectionnée.")
        random_sleep(1, 1.25)
    except Exception as e:
        print("❌ Sélection marque échouée :", e)

    # === ÉTAT ===
    try:
        print("🔽 Sélection état...")
        condition_input = driver.find_element(By.ID, "status_id")
        condition_input.click()
        random_sleep(1, 1.25)
        driver.find_element(By.ID, "condition-2").click()
        print("✅ État sélectionné.")
        random_sleep(1, 1.25)
    except Exception as e:
        print("❌ Sélection état échouée :", e)

    # === PRIX ===
    try:
        price_input = driver.find_element(By.NAME, "price")
        price_input.clear()
        price_input.send_keys(str(row["Price"]))
        print("💰 Prix renseigné.")
        random_sleep(1, 1.25)
    except Exception:
        print("❌ Champ 'Prix' introuvable.")

    # === COLIS ===
    try:
        driver.find_element(By.ID, "package-size-1").click()
        print("📦 Colis sélectionné.")
        random_sleep(1, 1.25)
    except Exception as e:
        print("❌ Sélection colis échouée :", e)

    print(f"✅ Fiche {row['Title']} remplie.")
    random_sleep(2, 2.25)


def run_scraping(csv_path):
    if not is_debug_active():
        print("🟡 Chrome n'est pas lancé avec --remote-debugging-port=9222")
        print("🚀 Lancement automatique de Chrome via launch_chrome_debug.bat")
        subprocess.run(["start", "chrome_launcher.bat"], shell=True)
        input("Appuyez sur l'onglet fraîchement ouvert pour link le script ...")

    if not os.path.exists(csv_path):
        print(f"❌ Fichier introuvable : {csv_path}")
        return

    df = pd.read_csv(csv_path)
    if df.empty:
        print("❌ Le fichier CSV est vide.")
        return

    driver = connect_to_chrome()

    print(f"🔄 Démarrage du traitement de {len(df)} fiches...\n")
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Fiches remplies"):
        print(f"\n🧾 Fiche {index+1} / {len(df)} : {row['Title']}")
        try:
            driver.execute_script(f"window.open('{VINTED_URL}');")
            driver.switch_to.window(driver.window_handles[-1])
        except Exception as e:
            print(f"❌ Erreur lors de la connexion à Chrome : {e}")
            return
        print(f"🔍 Ouverture de la page item : {row['Title']}")
        random_sleep(2, 2.25)
        fill_form(driver, row)
        input("🔄 Apuuyez sur Entrée pour lancer la prochaine fiche")

    print("\n🎉 Toutes les fiches ont été traitées.")
