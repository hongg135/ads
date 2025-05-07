import requests
import time
import random
import string

BASE_URL = "https://api.mail.tm"

def generate_random_name(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def get_available_domain():
    resp = requests.get(f"{BASE_URL}/domains")
    resp.raise_for_status()
    domains = resp.json()["hydra:member"]
    return domains[0]["domain"]

def create_account():
    domain = get_available_domain()
    username = generate_random_name()
    email = f"{username}@{domain}"
    password = "Test12345!"

    register_resp = requests.post(f"{BASE_URL}/accounts", json={
        "address": email,
        "password": password
    })

    if register_resp.status_code != 201:
        raise Exception("❌ 建立帳號失敗")

    token_resp = requests.post(f"{BASE_URL}/token", json={
        "address": email,
        "password": password
    })

    token_resp.raise_for_status()
    token = token_resp.json()["token"]
    print(f"📮 建立信箱成功: {email}")
    return email, token

def wait_for_verification_code(email, token, timeout=120):
    headers = {"Authorization": f"Bearer {token}"}
    print("⌛ 正在等待驗證碼信件...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        messages = requests.get(f"{BASE_URL}/messages", headers=headers).json()["hydra:member"]
        for msg in messages:
            if "Amazon" in msg["subject"]:
                msg_detail = requests.get(f"{BASE_URL}/messages/{msg['id']}", headers=headers).json()
                code = extract_code(msg_detail["text"])
                if code:
                    print(f"📬 驗證碼: {code}")
                    return code
        time.sleep(5)

    raise Exception("❌ 驗證碼等待超時")

def extract_code(text):
    import re
    match = re.search(r"\b(\d{6})\b", text)
    return match.group(1) if match else None

def get_verification_code(timeout=120):
    email, token = create_account()
    code = wait_for_verification_code(email, token, timeout)
    return email, code

if __name__ == "__main__":
    get_verification_code()
