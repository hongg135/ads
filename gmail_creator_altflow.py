# gmail_creator_altflow.py
# 嘗試透過 YouTube 建立 Gmail，避開強制驗證手機

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def create_browser():
    chrome_options = Options()
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def register_via_youtube():
    driver = create_browser()
    driver.get("https://www.youtube.com")
    time.sleep(3)
    driver.find_element(By.XPATH, "//tp-yt-paper-button[@aria-label='Sign in']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Create account']"))).click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[text()='For myself']").click()
    # 接著進入 Google 帳號註冊頁，填表略。
    print("✅ 進入註冊流程，請手動觀察是否要求手機")
    input("按 Enter 關閉瀏覽器...")
    driver.quit()

if __name__ == "__main__":
    register_via_youtube()
