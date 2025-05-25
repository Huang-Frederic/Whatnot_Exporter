
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os


def run_scraping(csv_path):
    # === CONFIG SELENIUM AVEC PROTECTION CLOUDFLARE ===
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)

    # === OUVERTURE VINTED ===
    driver.get("https://www.vinted.fr")
    print("🔐 Merci de te connecter manuellement à Vinted.")
    input("✅ Appuie sur Entrée une fois connecté(e) et prêt(e) à continuer...")

    # === LECTURE CSV ===
    df = pd.read_csv(csv_path)
    if df.empty:
        print("❌ Le fichier CSV est vide.")
        return

    # === UNE SEULE ANNONCE POUR LE TEST ===
    row = df.iloc[0]
    print(f"📤 Publication de : {row['Title']}")

    # === NAVIGUER VERS LE FORMULAIRE DE VENTE ===
    driver.get("https://www.vinted.fr/items/new")
    time.sleep(3)

    # === TITRE ===
    try:
        driver.find_element(By.NAME, "title").send_keys(row["Title"])
    except Exception as e:
        print("❌ Erreur champ titre :", e)

    # === PRIX ===
    try:
        price = str(row["Price"])
        price_input = driver.find_element(By.ID, "price")
        price_input.click()
        price_input.clear()
        for char in price:
            price_input.send_keys(char)
            time.sleep(0.05)
        print("💶 Prix injecté :", price)
    except Exception as e:
        print("❌ Erreur saisie prix :", e)

    # === DESCRIPTION ===
    try:
        desc = row["Description"]
        desc_area = driver.find_element(
            By.CSS_SELECTOR, 'textarea[data-testid="description--input"]')
        desc_area.click()
        desc_area.clear()
        for char in desc:
            desc_area.send_keys(char)
    except Exception as e:
        print("❌ Erreur sur la description :", e)

    # === CATÉGORIE ===
    try:
        cat_input = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="catalog-select-dropdown-input"]')
        cat_input.click()
        time.sleep(1)
        cat_input.send_keys("Single trading cards")
        cat_input.send_keys(Keys.ENTER)
    except Exception as e:
        print("❌ Erreur sélection catégorie :", e)

    # === CONDITION ===
    try:
        condition = row["Condition"]
        condition_input = driver.find_element(By.ID, "status_id")
        condition_input.click()
        time.sleep(1)
        condition_input.send_keys(condition)
        condition_input.send_keys(Keys.ENTER)
    except Exception as e:
        print("❌ Erreur sélection condition :", e)

    # === FORMAT DE COLIS ===
    try:
        package_map = {
            "Small": "1",
            "Medium": "2",
            "Large": "3"
        }
        package_id = package_map.get(row["Package"], "1")
        driver.find_element(By.ID, f"package-size-{package_id}").click()
    except Exception as e:
        print("❌ Erreur sélection colis :", e)

    # === UPLOAD PHOTOS ===
    try:
        file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        paths = "\n".join([
            os.path.abspath(row["Picture_1"]),
            os.path.abspath(row["Picture_2"])
        ])
        file_input.send_keys(paths)
        print("🖼️ Images uploadées.")
    except Exception as e:
        print("❌ Erreur upload images :", e)

    # === FIN ===
    print("✅ Fiche pré-remplie. Vérifie et clique sur 'Mettre en ligne' manuellement !")
    input("🛑 Appuie sur Entrée pour fermer le navigateur quand tu as fini.")
    driver.quit()
