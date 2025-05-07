import requests

proxies = {
    "http": "http://tkyI0qulQDCG5KFO:UBsO98dxBkyT9pZs@geo.floppydata.com:10080",
    "https": "http://tkyI0qulQDCG5KFO:UBsO98dxBkyT9pZs@geo.floppydata.com:10080",
}

try:
    r = requests.get("https://ipinfo.io", proxies=proxies, timeout=10)
    print(r.json())
except Exception as e:
    print("代理測試失敗：", e)
