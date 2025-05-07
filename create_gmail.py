from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
import random
import time
import json
import os

def generate_profile():
    return {
        "first_name": random.choice(["Hans", "Pierre", "Luis", "Taro"]),
        "last_name": random.choice(["Müller", "Dubois", "Garcia", "Yamamoto"]), 
        "username": f"user{random.randint(10000,99999)}{random.randint(100,999)}",
        "password": "Aa123456!!",
        "birth_day": random.randint(1, 28),
        "birth_month": random.randint(1, 12),
        "birth_year": random.randint(1985, 2002),
        "gender": random.choice(["Male", "Female", "Rather not say"])
    }

def create_gmail():
    profile = generate_profile()
    ua = UserAgent()

    with sync_playwright() as p:
        # Load stealth.min.js to help avoid detection
        with open('stealth.min.json', 'r') as f:
            stealth_js = f.read()

        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent=ua.random,
            locale="de-DE", 
            viewport={"width": 1280, "height": 800},
            timezone_id="Europe/Berlin",
            geolocation={"latitude": 52.520008, "longitude": 13.404954},
            locale="de-DE"
        )
        
        # Add stealth script to avoid detection
        page = context.new_page()
        page.add_init_script(stealth_js)
        
        # Random delays between actions
        def random_delay():
            time.sleep(random.uniform(1, 3))

        try:
            page.goto("https://accounts.google.com/signup")
            random_delay()

            # Fill basic info with human-like delays
            page.fill("input[name='firstName']", profile['first_name'])
            random_delay()
            page.fill("input[name='lastName']", profile['last_name'])
            random_delay()
            page.fill("input[name='Username']", profile['username'])
            random_delay()
            page.fill("input[name='Passwd']", profile['password'])
            random_delay()
            page.fill("input[name='ConfirmPasswd']", profile['password'])
            random_delay()
            
            # Random mouse movements before clicking
            page.mouse.move(random.randint(0, 100), random.randint(0, 100))
            page.click("button:has-text('Next')")
            random_delay()

            # Fill birthday and gender
            page.select_option("select#month", str(profile['birth_month']))
            random_delay()
            page.fill("input#day", str(profile['birth_day']))
            random_delay()
            page.fill("input#year", str(profile['birth_year']))
            random_delay()
            page.select_option("select#gender", "1" if profile['gender'] == "Male" else "2")
            random_delay()
            
            page.click("button:has-text('Next')")

            print("Account details:")
            print(f"Username: {profile['username']}@gmail.com")
            print(f"Password: {profile['password']}")

            # Wait for manual verification if needed
            input("Press Enter after completing phone verification (if required)...")

        except Exception as e:
            print(f"Error occurred: {str(e)}")
        finally:
            browser.close()

if __name__ == "__main__":
    create_gmail()
