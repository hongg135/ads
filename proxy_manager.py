import random

def get_random_proxy():
    # 格式: ip:port 或 ip:port:user:pass
    proxy_list = [
        "de.proxyserver.com:1080:user:pass",
        "fr.proxyserver.com:1080:user:pass",
        "jp.proxyserver.com:1080:user:pass",
    ]
    return random.choice(proxy_list)

def format_proxy_for_playwright(proxy_str):
    parts = proxy_str.split(":")
    if len(parts) == 4:
        ip, port, user, pw = parts
        return {
            "server": f"http://{ip}:{port}",
            "username": user,
            "password": pw
        }
    else:
        ip, port = parts
        return {
            "server": f"http://{ip}:{port}"
        }
