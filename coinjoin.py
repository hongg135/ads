import pyautogui
import time
import keyboard
import pyperclip

# Step 1: 啟動 Wasabi Wallet
pyautogui.press('win')
time.sleep(1)
pyautogui.write('Wasabi Wallet')
time.sleep(1)
pyautogui.press('enter')

# Step 2: 等待應用程式啟動
time.sleep(10)

# Step 3: 開啟指定錢包（用 Tab / Enter 導航，視你 UI 而定）
# 你可以錄製或截圖 UI 座標來微調這部分點擊

# Step 4: 複製 BTC 入金地址
pyautogui.hotkey('ctrl', 'shift', 'c')  # 有些版本支援這組快捷鍵
time.sleep(2)
address = pyperclip.paste()
print("BTC 收款地址為:", address)

# Step 5: 混幣自動進行中，手動等待或透過 logs 監控完成

# Step 6: 混幣完成後，點選 Send，自動填寫轉出資料
# 以下為模擬點擊 & 輸入的範例
pyautogui.moveTo(100, 200)  # 這裡是「Send」按鈕的座標
pyautogui.click()
time.sleep(1)

pyautogui.write('destination_wallet_btc_address')
pyautogui.press('tab')
pyautogui.write('0.005')  # 金額
pyautogui.press('tab')
pyautogui.press('enter')  # 確認發送

print("混幣後 BTC 已轉出")
# 定義一個函數來獲取滑鼠位置
def get_mouse_position():
    try:
        while True:
            x, y = pyautogui.position()
            print(f"目前滑鼠位置：x={x}, y={y}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n已停止讀取滑鼠位置")

# 改用滑鼠操作來複製地址
def copy_btc_address():
    # 點選 Receive 頁籤
    pyautogui.moveTo(150, 120)  # 請根據實際 UI 調整座標
    pyautogui.click()
    time.sleep(2)
    
    # 點選 Copy Address 按鈕
    pyautogui.moveTo(300, 350)  # 請根據實際 UI 調整座標
    pyautogui.click()
    time.sleep(1)
    
    # 獲取複製的地址
    address = pyperclip.paste()
    return address

# 如果需要找座標，取消下面這行的註解
# get_mouse_position()

# 使用新的方法複製地址
address = copy_btc_address()
print("BTC 收款地址為:", address)
