from playwright.sync_api import sync_playwright
from storage_utils import get_all_accounts

def login_gmail(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://accounts.google.com/signin")

        page.fill("input[type='email']", username)
        page.click("#identifierNext")
        page.wait_for_timeout(2000)
        page.fill("input[type='password']", password)
        page.click("#passwordNext")

        page.wait_for_timeout(5000)
        print(f"✅ Login attempt for {username}")
        browser.close()

if __name__ == "__main__":
    accounts = get_all_accounts()
    for acc in accounts:
        login_gmail(acc["username"], acc["password"])
