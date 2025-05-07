import requests

# AdsPower 本機 API URL
api_url = "http://localhost:50325/api/v1/profile/create"

# Profile 設定資料
profile_payload = {
    "name": "Amazon_US_NY",
    "group_id": 0,  # 預設群組 ID
    "platform": "Amazon", 
    "proxy_type": 1,  # 1 = HTTP, 2 = Socks5
    "ip": "gate.decodo.com",
    "port": "10001",
    "proxy_user": "spiv3lmttw",
    "proxy_password": "Bzh8on5A9vm",
    "fingerprint": {
        "language": "en-US",
        "timezone": "America/New_York",
        "screen_resolution": "1920x1080",
        "webgl_vendor": "Intel Inc.",
        "renderer": "Intel Iris OpenGL Engine",
    }
}

# 發送建立請求
headers = {"Content-Type": "application/json"}
response = requests.post(api_url, json=profile_payload, headers=headers)

# 回傳結果
print("建立結果：", response.status_code)
print(response.json())
# 修正 API URL 為正確的 AdsPower API 位址
api_url = "http://local.adspower.net:50325/api/v1/profile/create"

# 更新 Profile 設定資料格式
profile_payload = {
    "name": "Amazon_US_NY",
    "group_id": 0,
    "platform": "Amazon",
    "proxy": {
        "proxyType": "http", 
        "proxyHost": "gate.decodo.com",
        "proxyPort": 10001,
        "proxyUser": "spiv3lmttw",
        "proxyPwd": "Bzh8on5A9vm"
    },
    "fingerprint": {
        "language": "en-US",
        "timezone": "America/New_York", 
        "screen_resolution": "1920x1080",
        "webgl_vendor": "Intel Inc.",
        "renderer": "Intel Iris OpenGL Engine"
    }
}

# 加入錯誤處理
try:
    response = requests.post(api_url, json=profile_payload, headers=headers)
    print("建立結果：", response.status_code)
    if response.status_code == 200:
        print("✅ Profile 建立成功")
        print(response.json())
    else:
        print("❌ 發送失敗，請檢查 API 是否啟動、端口是否正確")
        print("回應內容：", response.text)
except Exception as e:
    print("❌ 發生錯誤：", e)
