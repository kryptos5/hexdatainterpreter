"""
Integration tests for the complete application workflow.
"""
import os
import sys
import unittest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hex_logic import HexConverter, HexFormatterUtility
from settings_manager import SettingsManager


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""

    def setUp(self):
        """Set up test fixtures."""
        self.converter = HexConverter()
        self.settings_manager = SettingsManager(
            r"SOFTWARE\HexDataInterpreter_IntegrationTest")

    def tearDown(self):
        """Clean up after tests."""
        try:
            self.settings_manager.deleteSettings()
        except:
            pass

    def test_complete_workflow_integer(self):
        """Test complete workflow for integer conversion."""
        # Parse and convert
        hex_input = "01 02 03 04"
        results = self.converter.convert(hex_input, "32-bit int", "little")

        # Format results
        formatted = HexFormatterUtility.formatResults(results, "32-bit int",
                                                      "little")

        # Verify result structure
        self.assertIsInstance(formatted, str)
        self.assertIn("Integer Conversions", formatted)
        self.assertIn("Little-Endian", formatted)
        self.assertIn("8-bit", formatted)
        self.assertIn("16-bit", formatted)
        self.assertIn("32-bit", formatted)

    def test_complete_workflow_float(self):
        """Test complete workflow for float conversion."""
        # IEEE 754 representation of 1.0
        hex_input = "00 00 80 3F"
        results = self.converter.convert(hex_input, "32-bit float", "little")
        formatted = HexFormatterUtility.formatResults(results, "32-bit float",
                                                      "little")

        # Verify result
        self.assertIn("1.0", formatted)
        self.assertIn("32-Bit Float", formatted)

    def test_complete_workflow_double(self):
        """Test complete workflow for double conversion."""
        # IEEE 754 representation of 1.0 as double
        hex_input = "00 00 00 00 00 00 F0 3F"
        results = self.converter.convert(hex_input, "64-bit double", "little")
        formatted = HexFormatterUtility.formatResults(results, "64-bit double",
                                                      "little")

        # Verify result
        self.assertIn("1.0", formatted)
        self.assertIn("64-Bit Double", formatted)

    def test_endianness_difference(self):
        """Test that endianness makes a difference."""
        hex_input = "01 02 03 04"

        # Convert with different endianness
        little_results = self.converter.convert(hex_input, "32-bit int",
                                                "little")
        big_results = self.converter.convert(hex_input, "32-bit int", "big")

        # Find 32-bit results
        little_32bit = next(r for r in little_results if r['size'] == '32-bit')
        big_32bit = next(r for r in big_results if r['size'] == '32-bit')

        # Results should be different
        self.assertNotEqual(little_32bit['unsigned'], big_32bit['unsigned'])
        self.assertEqual(little_32bit['unsigned'], 67305985)  # Little-endian
        self.assertEqual(big_32bit['unsigned'], 16909060)  # Big-endian

    def test_error_handling_invalid_hex(self):
        """Test error handling for invalid hex input."""
        with self.assertRaises(ValueError):
            self.converter.convert("GG HH II", "32-bit int", "little")

    def test_error_handling_invalid_type(self):
        """Test error handling for invalid data type."""
        with self.assertRaises(ValueError):
            self.converter.convert("01 02", "invalid-type", "little")

    def test_settings_integration(self):
        """Test settings manager integration."""
        if not self.settings_manager.isRegistryAvailable():
            self.skipTest("Registry not available on this platform")

        # Test saving and loading settings
        original_settings = {"DataType": "32-bit float", "Endianness": "big"}

        self.settings_manager.saveSettings(original_settings)
        loaded_settings = self.settings_manager.loadSettings()

        self.assertEqual(loaded_settings["DataType"], "32-bit float")
        self.assertEqual(loaded_settings["Endianness"], "big")

        # Use loaded settings for conversion
        hex_input = "00 00 80 3F"
        results = self.converter.convert(hex_input,
                                         loaded_settings["DataType"],
                                         loaded_settings["Endianness"])

        # Should get float results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['type'], 'float')


if __name__ == '__main__':
    unittest.main(verbosity=2)
