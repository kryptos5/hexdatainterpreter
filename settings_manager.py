"""
Settings management for HexDataInterpreter application.
Handles saving and loading user preferences to/from Windows Registry.
"""

try:
    import winreg
    REGISTRY_AVAILABLE = True
except ImportError:
    REGISTRY_AVAILABLE = False

from typing import Any, Dict, Optional


class SettingsManager:
    """Manages application settings persistence."""

    def __init__(self,
                 registry_key_path: str = r"SOFTWARE\HexDataInterpreter"):
        """
        Initialize the settings manager.
        
        Args:
            registry_key_path: Windows registry path for storing settings
        """
        self.registry_key_path = registry_key_path
        self.default_settings = {
            "DataType": "32-bit int",
            "Endianness": "little"
        }

    def createRegistryKey(self) -> bool:
        """
        Create registry key if it doesn't exist.
        
        Returns:
            True if key was created or already exists, False on error
        """
        if not REGISTRY_AVAILABLE:
            return False

        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.registry_key_path)
            return True
        except Exception as e:
            print(f"Error creating registry key: {e}")
            return False

    def saveSettings(self, settings: Dict[str, str]) -> bool:
        """
        Save settings to Windows registry.
        
        Args:
            settings: Dictionary of setting name -> value pairs
            
        Returns:
            True if successful, False otherwise
        """
        if not REGISTRY_AVAILABLE:
            print("Registry not available - settings will not be saved")
            return False

        try:
            # Create the key if it doesn't exist
            self.createRegistryKey()

            # Open the key for writing
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 self.registry_key_path, 0,
                                 winreg.KEY_SET_VALUE)

            # Save each setting
            for setting_name, setting_value in settings.items():
                winreg.SetValueEx(key, setting_name, 0, winreg.REG_SZ,
                                  setting_value)

            winreg.CloseKey(key)
            print("Settings saved to registry successfully")
            return True

        except Exception as e:
            print(f"Error saving settings to registry: {e}")
            return False

    def loadSettings(self) -> Dict[str, str]:
        """
        Load settings from Windows registry.
        
        Returns:
            Dictionary of setting name -> value pairs
        """
        if not REGISTRY_AVAILABLE:
            print("Registry not available - using default settings")
            return self.default_settings.copy()

        settings = {}

        try:
            # Try to open the registry key
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 self.registry_key_path, 0, winreg.KEY_READ)

            # Load each setting with fallback to defaults
            for setting_name, default_value in self.default_settings.items():
                try:
                    value, _ = winreg.QueryValueEx(key, setting_name)
                    settings[setting_name] = value
                except FileNotFoundError:
                    settings[setting_name] = default_value

            winreg.CloseKey(key)
            print("Settings loaded from registry successfully")

        except FileNotFoundError:
            # Registry key doesn't exist, use default values
            settings = self.default_settings.copy()
            print("Registry key not found, using default settings")

        except Exception as e:
            # Other error, use default values
            settings = self.default_settings.copy()
            print(f"Error loading settings from registry: {e}")

        return settings

    def getSetting(self, setting_name: str) -> Optional[str]:
        """
        Get a specific setting value.
        
        Args:
            setting_name: Name of the setting to retrieve
            
        Returns:
            Setting value or None if not found
        """
        settings = self.loadSettings()
        return settings.get(setting_name)

    def setSetting(self, setting_name: str, setting_value: str) -> bool:
        """
        Set a specific setting value.
        
        Args:
            setting_name: Name of the setting
            setting_value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        # Load current settings
        settings = self.loadSettings()

        # Update the specific setting
        settings[setting_name] = setting_value

        # Save back to registry
        return self.saveSettings(settings)

    def resetToDefaults(self) -> bool:
        """
        Reset all settings to default values.
        
        Returns:
            True if successful, False otherwise
        """
        return self.saveSettings(self.default_settings.copy())

    def isRegistryAvailable(self) -> bool:
        """
        Check if registry functionality is available.
        
        Returns:
            True if registry is available, False otherwise
        """
        return REGISTRY_AVAILABLE

    def deleteSettings(self) -> bool:
        """
        Delete all settings from registry.
        
        Returns:
            True if successful, False otherwise
        """
        if not REGISTRY_AVAILABLE:
            return False

        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self.registry_key_path)
            print("Settings deleted from registry successfully")
            return True
        except FileNotFoundError:
            print("Settings key not found (already deleted)")
            return True
        except Exception as e:
            print(f"Error deleting settings: {e}")
            return False
