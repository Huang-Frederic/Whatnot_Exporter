
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os

# === CONFIG PROFIL LOCAL ===
CHROME_USER_DIR = "C:/Users/Frédéric/AppData/Local/Google/Chrome/User Data"
CHROME_PROFILE = "Profile 2"  # ou "Profile 1", "Profile 2", etc.


def run_scraping(csv_path):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(f"--user-data-dir={CHROME_USER_DIR}")
    options.add_argument(f"--profile-directory={CHROME_PROFILE}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    # === LECTURE CSV ===
    df = pd.read_csv(csv_path)
    if df.empty:
        print("❌ Le fichier CSV est vide.")
        return

    for index, row in df.iterrows():
        print(f"📤 Remplissage {index+1}/{len(df)} : {row['Title']}")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get("https://www.vinted.fr/items/new")
        time.sleep(4)

        # TITRE
        try:
            driver.find_element(By.NAME, "title").send_keys(row["Title"])
        except Exception as e:
            print(f"[{index+1}] ❌ Erreur Titre :", e)

        # PRIX
        try:
            price = str(row["Price"])
            price_input = driver.find_element(By.ID, "price")
            price_input.click()
            price_input.clear()
            for char in price:
                price_input.send_keys(char)
                time.sleep(0.05)
        except Exception as e:
            print(f"[{index+1}] ❌ Erreur Prix :", e)

        # DESCRIPTION
        try:
            desc = row["Description"]
            desc_area = driver.find_element(
                By.CSS_SELECTOR, 'textarea[data-testid="description--input"]')
            desc_area.click()
            desc_area.clear()
            for char in desc:
                desc_area.send_keys(char)
        except Exception as e:
            print(f"[{index+1}] ❌ Erreur Description :", e)

        # CATÉGORIE
        try:
            cat_input = driver.find_element(
                By.CSS_SELECTOR, '[data-testid="catalog-select-dropdown-input"]')
            cat_input.click()
            time.sleep(1)
            cat_input.send_keys("Single trading cards")
            cat_input.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"[{index+1}] ❌ Erreur Catégorie :", e)

        # CONDITION
        try:
            condition = row["Condition"]
            condition_input = driver.find_element(By.ID, "status_id")
            condition_input.click()
            time.sleep(1)
            condition_input.send_keys(condition)
            condition_input.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"[{index+1}] ❌ Erreur Condition :", e)

        # FORMAT DE COLIS
        try:
            package_map = {
                "Small": "1",
                "Medium": "2",
                "Large": "3"
            }
            package_id = package_map.get(row["Package"], "1")
            driver.find_element(By.ID, f"package-size-{package_id}").click()
        except Exception as e:
            print(f"[{index+1}] ❌ Erreur Colis :", e)

         # === UPLOAD PHOTOS ===
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

        print(f"[{index+1}] ✅ Fiche prête !")

    print("🧾 Toutes les fiches sont ouvertes. Poste-les manuellement.")
    input("🛑 Appuie sur Entrée pour fermer le navigateur quand tu as terminé.")
    driver.quit()


if __name__ == "__main__":
    run_scraping("vinted_ready.csv")
