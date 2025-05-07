from playwright.sync_api import sync_playwright
import os
import json
from fake_useragent import UserAgent

# 切換 VPN 國家（用 Windscribe）
def connect_vpn(country="France"):
    os.system(f"windscribe connect {country}")

# 載入個資資料
def load_profile(path="profile.json"):
    with open(path, 'r') as f:
        return json.load(f)

# 主程序：操作 Amazon 禮品卡頁面
def auto_order_amazon_giftcard():
    connect_vpn("France")  # 切換 VPN 到法國
    profile = load_profile()
    ua = UserAgent()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=ua.random)
        page = context.new_page()

        # 進入 Amazon 禮品卡頁面（預設是美國站）
        page.goto("https://www.amazon.com/gift-cards")

        # 點擊 Email Gift Card 類型（可根據實際頁面調整 selector）
        page.click("a[href*='/gift-card-email']")

        # 等待跳轉完成
        page.wait_for_load_state("networkidle")

        # 選擇金額（根據 profile["amount"]）
        amount_selector = f"button[value='{profile['amount']}']"
        page.click(amount_selector)

        # 填寫禮品卡訊息
        page.fill("input[name='recipientName']", profile["recipient_name"])
        page.fill("input[name='recipientEmail']", profile["recipient_email"])
        page.fill("input[name='senderName']", profile["name"])
        page.fill("input[name='message']", profile["message"])

        # 可選：截圖記錄操作
        page.screenshot(path="filled_form.png")

        # 以下為模擬點擊「購買」按鈕，請確認登入已完成
        # page.click("input#gc-buy-box-atc")

        print("✅ 表單已填寫完成，可手動檢查提交")

        # 清除環境
        context.close()
        browser.close()

if __name__ == "__main__":
    auto_order_amazon_giftcard()
