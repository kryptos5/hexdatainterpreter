"""
Unit tests for the settings_manager module.
"""
import os
import sys
import unittest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings_manager import SettingsManager


class TestSettingsManager(unittest.TestCase):
    """Test cases for SettingsManager class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Use a test-specific registry path
        self.test_registry_path = r"SOFTWARE\HexDataInterpreter_Test"
        self.settings_manager = SettingsManager(self.test_registry_path)

    def tearDown(self):
        """Clean up after each test."""
        # Clean up test registry entries
        try:
            self.settings_manager.deleteSettings()
        except:
            pass  # Ignore errors during cleanup

    def test_default_settings(self):
        """Test that default settings are correct."""
        expected_defaults = {"DataType": "32-bit int", "Endianness": "little"}
        self.assertEqual(self.settings_manager.default_settings,
                         expected_defaults)

    def test_isRegistryAvailable(self):
        """Test registry availability check."""
        # This will depend on the platform
        available = self.settings_manager.isRegistryAvailable()
        self.assertIsInstance(available, bool)

    def test_loadSettings_no_existing_settings(self):
        """Test loading settings when none exist."""
        # Delete any existing settings first
        self.settings_manager.deleteSettings()

        settings = self.settings_manager.loadSettings()

        # Should return default settings
        self.assertEqual(settings["DataType"], "32-bit int")
        self.assertEqual(settings["Endianness"], "little")

    def test_saveAndLoadSettings(self):
        """Test saving and loading settings."""
        if not self.settings_manager.isRegistryAvailable():
            self.skipTest("Registry not available on this platform")

        # Save test settings
        test_settings = {"DataType": "64-bit double", "Endianness": "big"}

        result = self.settings_manager.saveSettings(test_settings)
        self.assertTrue(result)

        # Load them back
        loaded_settings = self.settings_manager.loadSettings()
        self.assertEqual(loaded_settings["DataType"], "64-bit double")
        self.assertEqual(loaded_settings["Endianness"], "big")

    def test_getSetting(self):
        """Test getting a specific setting."""
        if not self.settings_manager.isRegistryAvailable():
            self.skipTest("Registry not available on this platform")

        # Save a setting first
        test_settings = {"DataType": "32-bit float", "Endianness": "little"}
        self.settings_manager.saveSettings(test_settings)

        # Get specific setting
        data_type = self.settings_manager.getSetting("DataType")
        self.assertEqual(data_type, "32-bit float")

        # Get non-existent setting
        invalid_setting = self.settings_manager.getSetting("NonExistent")
        self.assertIsNone(invalid_setting)

    def test_setSetting(self):
        """Test setting a specific setting."""
        if not self.settings_manager.isRegistryAvailable():
            self.skipTest("Registry not available on this platform")

        # Set a specific setting
        result = self.settings_manager.setSetting("DataType", "64-bit double")
        self.assertTrue(result)

        # Verify it was set
        value = self.settings_manager.getSetting("DataType")
        self.assertEqual(value, "64-bit double")

    def test_resetToDefaults(self):
        """Test resetting settings to defaults."""
        if not self.settings_manager.isRegistryAvailable():
            self.skipTest("Registry not available on this platform")

        # First set some non-default values
        test_settings = {"DataType": "64-bit double", "Endianness": "big"}
        self.settings_manager.saveSettings(test_settings)

        # Reset to defaults
        result = self.settings_manager.resetToDefaults()
        self.assertTrue(result)

        # Verify they are back to defaults
        settings = self.settings_manager.loadSettings()
        self.assertEqual(settings["DataType"], "32-bit int")
        self.assertEqual(settings["Endianness"], "little")


if __name__ == '__main__':
    unittest.main(verbosity=2)
