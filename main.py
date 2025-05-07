import time
import requests
import subprocess
import logging
from gmail_creator import GmailCreator
from gologin_client import GoLoginClient
from emulator_controller import EmulatorController

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_and_launch_profile():
    client = GoLoginClient()
    profile_id = client.create_profile()
    ws_url = client.start_profile(profile_id)
    logger.info(f"Profile launched with WebSocket URL: {ws_url}")
    return ws_url, profile_id

def start_ldplayer(instance_id="0"):
    try:
        subprocess.Popen(["C:/LDPlayer/ldmutiplayer/ldconsole.exe", "launch", instance_id])
        logger.info(f"LDPlayer instance {instance_id} launched")
        time.sleep(20)  # Wait for emulator to fully start
    except FileNotFoundError:
        logger.error("LDPlayer executable not found. Please check the path.")
        raise

def configure_emulator():
    emulator = EmulatorController()
    emulator.set_locale('en_US')
    emulator.set_timezone('America/New_York')
    emulator.restart()
    logger.info("Emulator configured with US locale and timezone")

def main():
    try:
        ws_url, profile_id = create_and_launch_profile()
        start_ldplayer()
        configure_emulator()

        creator = GmailCreator()
        creator.create_account()
        
        logger.info("Gmail account creation process completed")
        
        print("\nTo use this environment for browsing:")
        print(f"1. Open GoLogin and find the profile with ID: {profile_id}")
        print("2. Launch this profile in GoLogin")
        print("3. Use the opened browser to browse with the US residential IP")
        print("\nRemember to keep Proxifier settings as follows:")
        print("- GoLogin (gologin.exe) and LDPlayer (LdVBoxHeadless.exe) should use the FloppyData proxy")
        print("- Set the default rule to 'Direct' to avoid interfering with other connections")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()
