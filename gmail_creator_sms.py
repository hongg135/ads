# gmail_creator_sms.py
# 使用 5SIM 自動購買號碼並完成 Gmail 註冊驗證

import requests
import time

API_KEY = "YOUR_5SIM_API_KEY"
BASE_URL = "https://5sim.net/v1/user"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def buy_number():
    resp = requests.get(f"{BASE_URL}/buy/activation/google/usa/any", headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    return data['id'], data['phone']

def poll_code(order_id, timeout=120):
    for _ in range(timeout // 5):
        resp = requests.get(f"{BASE_URL}/check/{order_id}", headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        if data['sms']:  # 有收到簡訊
            return data['sms'][0]['code']
        time.sleep(5)
    raise TimeoutError("未收到驗證碼")

def main():
    order_id, phone = buy_number()
    print("📞 手機號碼:", phone)
    print("➡️ 請在 Gmail 註冊頁面輸入此號碼後等待驗證碼")
    code = poll_code(order_id)
    print("✅ 收到驗證碼:", code)

if __name__ == "__main__":
    main()
