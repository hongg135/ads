import json
import os

ACCOUNTS_FILE = "accounts.json"

def save_account(account):
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump([], f)

    with open(ACCOUNTS_FILE, 'r+') as f:
        data = json.load(f)
        data.append(account)
        f.seek(0)
        json.dump(data, f, indent=2)

def get_all_accounts():
    with open(ACCOUNTS_FILE, 'r') as f:
        return json.load(f)
