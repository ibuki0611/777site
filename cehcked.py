from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import pickle
import os
from datetime import datetime

# ===== ユーザー設定 =====
COOKIE_PATH = 'cookies_pc.pkl'
HOME_URL = 'https://www.d-deltanet.com/'
address_text = "茨城県常総市新井木町字江畑３７－１"

# 機種名とCSVファイル名のマッピング
machines = {
    "ゴーゴージャグラー３": "gogojuggler3.csv",
    "キングハナハナ-30": "kinghanahana.csv",
    "SアイムジャグラーＥＸ": "SimJuggler.csv",
    "ハナハナホウオウ～天翔～-30": "hououhanahana.csv",
    "ジャグラーガールズSS": "jugglergirls.csv",
    "マイジャグラーV": "myjuggler5.csv",
    "ミスタージャグラー": "misterjuggler.csv",
    "ハッピージャグラーＶＩＩＩ": "happyjuggler8.csv"
}

# ===== Selenium 初期設定 =====
def init_driver():
    options = Options()
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)

# ===== Cookieでログイン =====
def load_cookies(driver, cookie_path):
    driver.get(HOME_URL)
    with open(cookie_path, "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(2)
    print("✔ Cookieでログイン完了")

# ===== 店舗ページへ遷移 =====
def navigate_to_hall(driver):
    wait = WebDriverWait(driver, 20)
    driver.get(HOME_URL)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "HOME"))).click()
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "茨城"))).click()
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "常総市"))).click()
    xpath_hall = f"//p[@class='address' and contains(text(), '{address_text}')]/preceding-sibling::p[@class='hall-name']/a"
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_hall))).click()

# ===== 各機種の出玉データへ遷移してデータ抽出 =====
def extract_and_save_machine_data(driver, machine_name, csv_filename):
    wait = WebDriverWait(driver, 10)
    try:
        xpath = f"//span[contains(text(), '{machine_name}')]/ancestor::tr[1]//input[@value='出玉データ']"
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        print(f"➡ {machine_name} 出玉データクリック")
        time.sleep(2)

        rows = driver.find_elements(By.XPATH, "//div[@id='ata0']//tr[.//span[@class='num']]")
        results = []

        for row in rows:
            try:
                tds = row.find_elements(By.TAG_NAME, "td")
                if len(tds) >= 5:
                    台番号 = tds[0].find_element(By.CLASS_NAME, "num").text
                    総スタート = tds[1].text.strip()
                    BB回数 = tds[2].text.strip()
                    RB回数 = tds[3].text.strip()
                    合成確率 = tds[4].text.strip()

                    if all([台番号, 総スタート, BB回数, RB回数, 合成確率]):
                        results.append({
                            "日付": datetime.now().strftime("%Y-%m-%d"),
                            "曜日": datetime.now().strftime("%A"),
                            "台番号": 台番号,
                            "総スタート": 総スタート,
                            "BB回数": BB回数,
                            "RB回数": RB回数,
                            "合成確率": 合成確率
                        })
            except Exception as e:
                print("⚠️ データ抽出失敗:", e)

        if results:
            df = pd.DataFrame(results)
            df.to_csv(
                csv_filename,
                mode='a',
                header=not os.path.exists(csv_filename),
                index=False,
                encoding="utf-8-sig"
            )
            print(f"✅ {csv_filename} にデータを保存")

        driver.back()
        time.sleep(2)

    except Exception as e:
        print(f"❌ {machine_name} の処理中にエラー: {e}")

# ===== メイン処理 =====
def main():
    driver = init_driver()
    try:
        load_cookies(driver, COOKIE_PATH)
        navigate_to_hall(driver)

        for name, csv in machines.items():
            extract_and_save_machine_data(driver, name, csv)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
