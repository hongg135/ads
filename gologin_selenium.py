import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ====== 設定值 ======
GLOGIN_PROFILE_ID = "6817159c8521ad7d5d8b34db"
GLOGIN_API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODE2YjQ1Zjg1MjFhZDdkNWQ0ZDJhNDIiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2ODE2YjlmNjUzM2FhOTg1MjAyM2I5NWYifQ.DSvN_eym7YkH2yPxFrPn_zRqj4JddoEaXCUBS4rufXU"
GOLOGIN_API_URL = f"https://api.gologin.com/browser/{GLOGIN_PROFILE_ID}/start"

# Gmail 註冊資料
GMAIL_ACCOUNT = {
    "first_name": "John",
    "last_name": "Doe", 
    "username": "johndoe928173",
    "password": "Example123!",
    "birth_month": "May",
    "birth_day": "3",
    "birth_year": "1995",
    "gender": "Male"
}

def start_profile():
    res = requests.get(
        GOLOGIN_API_URL,
        headers={"Authorization": f"Bearer {GLOGIN_API_TOKEN}"}
    )
    if res.status_code != 200:
        print("[❌] 啟動 profile 失敗:", res.text)
        return None
    port = int(res.json()["wsUrl"].split(":")[-1].split("/")[0])
    print(f"[✅] Profile 啟動成功，Remote Debugger Port: {port}")
    return port

def attach_selenium(port):
    options = Options()
    options.debugger_address = f"127.0.0.1:{port}"
    driver = webdriver.Chrome(options=options)
    return driver

def fill_gmail_signup(driver, account):
    wait = WebDriverWait(driver, 15)

    driver.get("https://accounts.google.com/signup")

    wait.until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys(account["first_name"])
    driver.find_element(By.ID, "lastName").send_keys(account["last_name"])
    driver.find_element(By.ID, "username").send_keys(account["username"])
    driver.find_element(By.NAME, "Passwd").send_keys(account["password"])
    driver.find_element(By.NAME, "ConfirmPasswd").send_keys(account["password"])
    driver.find_element(By.XPATH, "//span[text()='Next']").click()

    # 等待生日欄位載入
    wait.until(EC.presence_of_element_located((By.ID, "month")))
    
    Select(driver.find_element(By.ID, "month")).select_by_visible_text(account["birth_month"])
    driver.find_element(By.ID, "day").send_keys(account["birth_day"])
    driver.find_element(By.ID, "year").send_keys(account["birth_year"])
    Select(driver.find_element(By.ID, "gender")).select_by_visible_text(account["gender"])
    driver.find_element(By.XPATH, "//span[text()='Next']").click()

    print("[✅] 表單已送出，接下來等候驗證或簡訊步驟（需人工處理）")

def main():
    port = start_profile()
    if not port:
        return

    time.sleep(3)  # 等 browser 啟動

    driver = attach_selenium(port)
    fill_gmail_signup(driver, GMAIL_ACCOUNT)

    input("🛑 按 Enter 結束並關閉...")
    driver.quit()

if __name__ == "__main__":
    main()
