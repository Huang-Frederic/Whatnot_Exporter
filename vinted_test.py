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
    time.sleep(5)

    try:
        title_input = driver.find_element(By.NAME, "title")
        title_input.clear()
        title_input.send_keys(row["Title"])
    except Exception:
        print("❌ Champ 'Titre' introuvable.")

    try:
        price_input = driver.find_element(By.NAME, "price")
        price_input.clear()
        price_input.send_keys(str(row["Price"]))
    except Exception:
        print("❌ Champ 'Prix' introuvable.")

    try:
        desc_input = driver.find_element(By.NAME, "description")
        desc_input.clear()
        desc_input.send_keys(row["Description"])
    except Exception:
        print("❌ Champ 'Description' introuvable.")

    print("⚠️ Remplis manuellement la catégorie, condition et colis.")
    print("✅ Fiche prête.")


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
