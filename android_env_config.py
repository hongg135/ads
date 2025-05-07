import subprocess

def run_adb(cmd):
    full_cmd = f'adb shell {cmd}'
    subprocess.run(full_cmd, shell=True)

def set_locale_and_timezone(locale="de_DE", timezone="Europe/Berlin"):
    print("設定語言與時區...")
    run_adb(f"setprop persist.sys.locale {locale}")
    run_adb(f"setprop persist.sys.timezone {timezone}")
    run_adb("stop; sleep 1; start")
