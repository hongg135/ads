import time
import subprocess
import logging
from account_generator import generate_account

class GmailCreator:
    def __init__(self, emulator_id='emulator-5554'):
        self.emulator_id = emulator_id
        self.account = generate_account()
        logging.basicConfig(level=logging.INFO)

    def run_adb(self, command):
        full_command = f"adb -s {self.emulator_id} shell {command}"
        subprocess.run(full_command, shell=True)

    def input_text(self, text):
        escaped_text = text.replace(' ', '%s')
        self.run_adb(f"input text {escaped_text}")
        time.sleep(1)

    def tap(self, x, y):
        self.run_adb(f"input tap {x} {y}")
        time.sleep(1)

    def swipe(self, x1, y1, x2, y2, duration=300):
        self.run_adb(f"input swipe {x1} {y1} {x2} {y2} {duration}")
        time.sleep(1)

    def create_account(self):
        logging.info(f"Creating account: {self.account['username']}")

        # 假設已啟動 Gmail 註冊頁面
        self.tap(540, 1700)  # 點選 "建立帳戶"
        time.sleep(2)

        self.tap(300, 1000)  # 選 "為自己"
        time.sleep(2)

        # 輸入姓與名
        self.input_text(self.account['first_name'])
        self.tap(900, 300)  # 下一欄位
        self.input_text(self.account['last_name'])
        self.tap(1000, 1700)  # 點選下一步

        # 輸入生日與性別
        time.sleep(2)
        self.input_text(self.account['birth_month'])
        self.tap(900, 300)  # 日
        self.input_text(self.account['birth_day'])
        self.tap(900, 300)  # 年
        self.input_text(self.account['birth_year'])
        self.tap(900, 1000)  # 性別預設點擊
        self.tap(1000, 1700)  # 下一步

        # 輸入帳號名稱
        time.sleep(2)
        self.input_text(self.account['username'])
        self.tap(1000, 1700)

        # 輸入密碼
        time.sleep(2)
        self.input_text(self.account['password'])
        self.tap(900, 300)
        self.input_text(self.account['password'])
        self.tap(1000, 1700)

        # 嘗試略過電話頁
        time.sleep(3)
        self.swipe(500, 1500, 500, 500)
        self.tap(1000, 1700)  # 嘗試略過電話

        # 同意條款
        time.sleep(3)
        self.swipe(500, 1500, 500, 500)
        self.tap(1000, 1700)

        # 儲存帳號
        with open('data/accounts.txt', 'a') as f:
            f.write(f"{self.account['username']}|{self.account['password']}\n")
        logging.info("Account saved.")

if __name__ == '__main__':
    creator = GmailCreator()
    creator.create_account()
