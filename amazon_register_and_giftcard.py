import os
import sys
import time
import json
import random
import string
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import cloudscraper
from secmail import SecMail
from twocaptcha import TwoCaptcha

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# 設置 Chrome 驅動器選項
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

# 2captcha solver
solver = TwoCaptcha(os.getenv('APIKEY_2CAPTCHA', 'YOUR_API_KEY'))

# 載入配置文件
def load_address_config():
    with open('address_info.json', 'r') as f:
        return json.load(f)

# 隨機生成郵箱
def generate_random_email():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f'{random_string}@1secmail.com', random_string

# Helper: Get Amazon code from email
def get_amazon_code(login, retries=30, delay=5):
    domain = "1secmail.com"
    secmail = SecMail()
    for i in range(retries):
        try:
            messages = secmail.get_messages(login)
            for msg in messages:
                if "Amazon" in msg['subject']:
                    body = secmail.read_message(msg['id'])['body']
                    import re
                    match = re.search(r"(\d{6})", body)
                    if match:
                        return match.group(1)
        except Exception as e:
            print(f"Error fetching email: {e}")
        print(f"Waiting for verification email... ({i+1})")
        time.sleep(delay)
    raise Exception("❌ Unable to receive Amazon verification code")

# Helper: Wait for element
def wait_for_element(driver, by, value, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

# Helper: Human-like typing
def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

# 開啟 Amazon 網站
def open_amazon(driver):
    driver.get("https://www.amazon.com/")
    time.sleep(5)  # 等待頁面加載
    print("✅ Amazon website opened")

# 模擬人類滑鼠移動
def human_like_mouse_movement(driver, target_element):
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(target_element, random.randint(5, 15), random.randint(5, 15))
    actions.pause(random.uniform(0.2, 0.8))
    actions.click()
    actions.perform()

# 繞過滑動驗證碼
def bypass_slider_captcha(driver):
    try:
        slider = driver.find_element(By.CLASS_NAME, 'a-slider-bar')  # 假設的 class name
        if slider:
            print("⚠️ 檢測到滑動驗證，嘗試處理中...")
            action = ActionChains(driver)
            action.click_and_hold(slider).perform()
            move_by = 200 + random.randint(-10, 10)
            action.move_by_offset(move_by, 0).pause(0.5).release().perform()
            print("✅ 嘗試完成滑動驗證")
            time.sleep(2)
    except Exception as e:
        print("ℹ️ 沒有滑動驗證或處理失敗:", str(e))

# 註冊帳戶
def register_account(driver, ADDRESS):
    driver.get("https://www.amazon.com/ap/register")
    time.sleep(2)

    email, login = generate_random_email()
    print(f"📮 Generated email: {email}")

    human_typing(wait_for_element(driver, By.ID, "ap_customer_name"), ADDRESS["full_name"])
    time.sleep(random.uniform(1, 2))
    human_typing(wait_for_element(driver, By.ID, "ap_email"), email)
    time.sleep(random.uniform(1, 2))
    human_typing(wait_for_element(driver, By.ID, "ap_password"), "Amazon123!")
    time.sleep(random.uniform(1, 2))
    human_typing(wait_for_element(driver, By.ID, "ap_password_check"), "Amazon123!")
    time.sleep(random.uniform(1, 2))
    
    continue_button = wait_for_element(driver, By.ID, "continue")
    human_like_mouse_movement(driver, continue_button)
    
    bypass_slider_captcha(driver)

    # Check for CAPTCHA
    try:
        captcha_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "auth-captcha-image")))
        print("⚠️ CAPTCHA detected. Attempting to solve...")
        captcha_image = captcha_element.get_attribute("src")
        result = solver.normal(captcha_image)
        human_typing(wait_for_element(driver, By.ID, "auth-captcha-guess"), result['code'])
        wait_for_element(driver, By.ID, "auth-captcha-guess-button").click()
    except TimeoutException:
        print("No CAPTCHA detected, continuing...")

    # Verification
    code = get_amazon_code(login)
    print(f"✅ Verification code received: {code}")
    human_typing(wait_for_element(driver, By.ID, "cvf-input-code"), code)
    time.sleep(random.uniform(1, 2))
    wait_for_element(driver, By.CLASS_NAME, "a-button-input").click()
    
    print("✅ Account registered successfully")
    return email

# 填寫地址
def fill_address(driver, ADDRESS):
    driver.get("https://www.amazon.com/a/addresses/add")
    time.sleep(random.uniform(3, 5))
    
    human_typing(wait_for_element(driver, By.ID, "address-ui-widgets-enterAddressFullName"), ADDRESS["full_name"])
    time.sleep(random.uniform(1, 2))
    human_typing(wait_for_element(driver, By.ID, "address-ui-widgets-enterAddressLine1"), ADDRESS["address_line1"])
    time.sleep(random.uniform(1, 2))
    human_typing(wait_for_element(driver, By.ID, "address-ui-widgets-enterAddressCity"), ADDRESS["city"])
    time.sleep(random.uniform(1, 2))
    human_typing(wait_for_element(driver, By.ID, "address-ui-widgets-enterAddressStateOrRegion"), ADDRESS["state"])
    time.sleep(random.uniform(1, 2))
    human_typing(wait_for_element(driver, By.ID, "address-ui-widgets-enterAddressPostalCode"), ADDRESS["zip"])
    time.sleep(random.uniform(1, 2))
    human_typing(wait_for_element(driver, By.ID, "address-ui-widgets-enterAddressPhoneNumber"), ADDRESS["phone_number"])
    time.sleep(random.uniform(1, 2))
    
    submit_button = wait_for_element(driver, By.XPATH, '//input[@aria-labelledby="address-ui-widgets-form-submit-button-announce"]')
    human_like_mouse_movement(driver, submit_button)
    
    print("✅ Address filled successfully")

# 購買 Apple Gift Card
def purchase_gift_card(driver, email):
    driver.get("https://www.amazon.com/dp/B08K2S1NKS")
    time.sleep(random.uniform(3, 5))
    
    amount_button = wait_for_element(driver, By.ID, "gc-buy-box-amount-1")
    human_like_mouse_movement(driver, amount_button)
    time.sleep(random.uniform(1, 2))
    
    human_typing(wait_for_element(driver, By.ID, "gc-buy-box-email"), email)
    time.sleep(random.uniform(1, 2))
    
    buy_now_button = wait_for_element(driver, By.NAME, "submit.buy-now")
    human_like_mouse_movement(driver, buy_now_button)

    # Wait for order confirmation
    try:
        order_confirmation = wait_for_element(driver, By.XPATH, "//span[contains(text(), 'Order placed, thanks!')]", timeout=30)
        print("✅ Apple Gift Card purchase completed!")
        
        # Log the transaction
        with open('log.txt', 'a') as log_file:
            log_file.write(f"Transaction completed: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(f"Email: {email}\n")
            log_file.write("Status: Success\n\n")
    except TimeoutException:
        print("❌ Order confirmation not found. Please check manually.")
        
        # Log the failed transaction
        with open('log.txt', 'a') as log_file:
            log_file.write(f"Transaction failed: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(f"Email: {email}\n")
            log_file.write("Status: Failed\n\n")

# 啟用 stealth.min.js
def enable_stealth(driver):
    try:
        with open("stealth.min.js") as f:
            js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        print("✅ Stealth.min.js loaded successfully")
    except FileNotFoundError:
        print("❌ Error: stealth.min.js not found. Please make sure it's in the same directory as the script.")
        raise

# 模擬人類互動
def simulate_human_interaction(driver):
    action = ActionChains(driver)
    for _ in range(random.randint(3, 7)):
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        action.move_by_offset(x_offset, y_offset).perform()
        time.sleep(random.uniform(0.1, 0.3))

# 主流程
def main():
    ADDRESS = load_address_config()
    
    driver = None
    try:
        print("Starting Amazon Gift Card Bot...")
        driver = uc.Chrome(options=options)
        enable_stealth(driver)
        print("✅ Browser launched successfully")
        
        open_amazon(driver)
        simulate_human_interaction(driver)
        email = register_account(driver, ADDRESS)
        fill_address(driver, ADDRESS)
        purchase_gift_card(driver, email)
        
        print("✅ Process completed successfully!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        if driver:
            try:
                driver.quit()
                print("✅ Browser closed")
            except Exception as e:
                print(f"Error closing browser: {e}")

if __name__ == "__main__":
    main()
