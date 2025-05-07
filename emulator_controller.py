import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmulatorController:
    def __init__(self, emulator_id='emulator-5554'):
        """Initialize emulator controller with device ID."""
        self.emulator_id = emulator_id
        logger.info(f"Initialized EmulatorController for device: {emulator_id}")

    def set_locale(self, locale='en_US'):
        """Set the system locale."""
        cmd = ['adb', '-s', self.emulator_id, 'shell', 'setprop', 'persist.sys.locale', locale]
        self._run(cmd, f"Setting locale to {locale}")

    def set_timezone(self, timezone='America/New_York'):
        """Set the system timezone."""
        cmd = ['adb', '-s', self.emulator_id, 'shell', 'setprop', 'persist.sys.timezone', timezone]
        self._run(cmd, f"Setting timezone to {timezone}")

    def restart(self):
        """Restart the Android system to apply changes."""
        logger.info("Restarting Android system...")
        stop_cmd = ['adb', '-s', self.emulator_id, 'shell', 'stop']
        start_cmd = ['adb', '-s', self.emulator_id, 'shell', 'start']
        
        self._run(stop_cmd, "Stopping Android system")
        # Small delay to ensure clean shutdown
        subprocess.run(['sleep', '1'], check=True)
        self._run(start_cmd, "Starting Android system")
        logger.info("System restart completed")

    def _run(self, cmd, desc):
        """Execute an ADB command with error handling."""
        try:
            result = subprocess.run(cmd, 
                                  check=True,
                                  capture_output=True,
                                  text=True)
            logger.info(f"{desc} - Success")
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"{desc} - Failed")
            logger.error(f"Command: {' '.join(cmd)}")
            logger.error(f"Error: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during: {desc}")
            logger.error(f"Error: {str(e)}")
            raise
