import json
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoLoginClient:
    def __init__(self, config_path='config.json'):
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
            self.api_key = self.config['gologin_api_key']
            self.base_url = 'https://api.gologin.com'
            self.headers = {'Authorization': f'Bearer {self.api_key}'}
            logger.info("GoLogin client initialized successfully")
        except FileNotFoundError:
            logger.error(f"Config file not found at {config_path}")
            raise
        except json.JSONDecodeError:
            logger.error("Invalid JSON in config file")
            raise
        except KeyError as e:
            logger.error(f"Missing required config key: {e}")
            raise

    def create_profile(self, profile_name='Auto-Gmail'):
        try:
            proxy = self.config['proxy']
            geo = self.config['geo']
            
            payload = {
                "name": profile_name,
                "os": "win",
                "navigator": {
                    "language": geo['language'],
                    "platform": "Win32",
                    "resolution": "1920x1080"
                },
                "proxyEnabled": True,
                "proxy": {
                    "mode": "http",
                    "host": proxy['host'],
                    "port": proxy['port'],
                    "username": proxy['username'],
                    "password": proxy['password']
                },
                "geoLocation": {
                    "mode": "manual",
                    "latitude": geo['latitude'],
                    "longitude": geo['longitude'],
                    "accuracy": 100
                }
            }

            logger.info(f"Creating new profile: {profile_name}")
            res = requests.post(
                f"{self.base_url}/browser", 
                headers=self.headers, 
                json=payload
            )
            res.raise_for_status()
            profile_id = res.json()['id']
            logger.info(f"Profile created successfully with ID: {profile_id}")
            return profile_id

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create profile: {e}")
            raise
        except KeyError as e:
            logger.error(f"Missing required configuration: {e}")
            raise

    def start_profile(self, profile_id):
        try:
            logger.info(f"Starting profile: {profile_id}")
            res = requests.get(
                f"{self.base_url}/browser/{profile_id}/start?automation=true",
                headers=self.headers
            )
            res.raise_for_status()
            data = res.json()
            ws_url = data['wsUrl']
            logger.info(f"Profile started successfully. WebSocket URL: {ws_url}")
            return ws_url

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to start profile: {e}")
            raise
        except KeyError as e:
            logger.error(f"Missing websocket URL in response: {e}")
            raise
