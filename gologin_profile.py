import requests
import logging
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODE2YjQ1Zjg1MjFhZDdkNWQ0ZDJhNDIiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2ODE2YjlmNjUzM2FhOTg1MjAyM2I5NWYifQ.DSvN_eym7YkH2yPxFrPn_zRqj4JddoEaXCUBS4rufXU"
PROXY = {
    "mode": "http",
    "host": "geo.floppydata.com",
    "port": 10080,
    "username": "tkyI0qulQDCG5KFO",
    "password": "UBsO98dxBkyT9pZs"
}

payload = {
    "name": "Gmail_US_Indiana",
    "browserType": "chrome",
    "os": "win",
    "notes": "Auto-created via script",
    "startUrl": "https://accounts.google.com/signup",
    "navigator": {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "language": "en-US",
        "platform": "Win32",
        "resolution": "1920x1080"
    },
    "proxy": PROXY,
    "timezone": {
        "enabled": True,
        "fillBasedOnIp": True
    },
    "geolocation": {
        "mode": "prompt",
        "enabled": True,
        "customize": True,
        "fillBasedOnIp": False,
        "latitude": 41.542,
        "longitude": -87.1373,
        "accuracy": 10
    }
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def create_profile():
    try:
        response = requests.post(
            "https://api.gologin.com/browser",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        profile_id = response.json()["id"]
        logger.info(f"[✅] Profile 建立成功！ID：{profile_id}")
        return profile_id
    except requests.exceptions.RequestException as e:
        logger.error(f"[❌] 建立失敗：{str(e)}")
        return None

def start_profile(profile_id):
    try:
        response = requests.get(
            f"https://api.gologin.com/browser/{profile_id}/start?automation=true",
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        port = data.get('port')
        logger.info(f"[✅] Profile 啟動成功！Port：{port}")
        return port
    except requests.exceptions.RequestException as e:
        logger.error(f"[❌] 啟動失敗：{str(e)}")
        return None

def setup_selenium(port):
    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    driver = webdriver.Chrome(options=options)
    return driver

def register_gmail(driver):
    try:
        # 等待頁面加載
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "firstName"))
        )

        # 填寫註冊表單
        driver.find_element(By.NAME, "firstName").send_keys("John")
        driver.find_element(By.NAME, "lastName").send_keys("Doe")
        # ... 其他表單填寫步驟 ...

        logger.info("[✅] Gmail 註冊表單填寫完成")
    except Exception as e:
        logger.error(f"[❌] Gmail 註冊失敗：{str(e)}")

if __name__ == "__main__":
    profile_id = create_profile()
    if profile_id:
        port = start_profile(profile_id)
        if port:
            driver = setup_selenium(port)
            register_gmail(driver)
            sleep(10)  # 等待一段時間以便觀察結果
            driver.quit()
