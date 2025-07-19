"""
Unit tests for the hex_logic module.
"""
import os
import sys
import unittest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hex_logic import HexConverter, HexFormatterUtility


class TestHexConverter(unittest.TestCase):
    """Test cases for HexConverter class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.converter = HexConverter()

    def test_parseHexInput_valid_input(self):
        """Test parsing valid hex input."""
        # Test space-separated hex
        result = self.converter.parseHexInput("01 02 03 04")
        expected = bytes([0x01, 0x02, 0x03, 0x04])
        self.assertEqual(result, expected)

        # Test hex without spaces
        result = self.converter.parseHexInput("01020304")
        self.assertEqual(result, expected)

        # Test mixed case
        result = self.converter.parseHexInput("aB cD eF")
        expected = bytes([0xAB, 0xCD, 0xEF])
        self.assertEqual(result, expected)

    def test_parseHexInput_odd_length(self):
        """Test parsing odd-length hex strings."""
        result = self.converter.parseHexInput("1 2 3")
        expected = bytes([0x01, 0x02, 0x03])
        self.assertEqual(result, expected)

    def test_parseHexInput_invalid_input(self):
        """Test parsing invalid hex input."""
        with self.assertRaises(ValueError):
            self.converter.parseHexInput("GG HH")

        with self.assertRaises(ValueError):
            self.converter.parseHexInput("XYZ")

    def test_parseHexInput_empty_input(self):
        """Test parsing empty input."""
        result = self.converter.parseHexInput("")
        self.assertEqual(result, b'')

        result = self.converter.parseHexInput("   ")
        self.assertEqual(result, b'')

    def test_convertToInt_little_endian(self):
        """Test integer conversion with little-endian."""
        byte_data = bytes([0x01, 0x02, 0x03, 0x04])
        results = self.converter.convertToInt(byte_data, "little")

        # Should contain 8-bit, 16-bit, and 32-bit interpretations
        sizes = [result['size'] for result in results]
        self.assertIn("8-bit", sizes)
        self.assertIn("16-bit", sizes)
        self.assertIn("32-bit", sizes)

        # Check specific values for 32-bit little-endian
        result_32bit = next(r for r in results if r['size'] == '32-bit')
        self.assertEqual(result_32bit['unsigned'], 67305985)

    def test_convertToInt_big_endian(self):
        """Test integer conversion with big-endian."""
        byte_data = bytes([0x01, 0x02, 0x03, 0x04])
        results = self.converter.convertToInt(byte_data, "big")

        # Check that big-endian gives different results
        result_32bit = next(r for r in results if r['size'] == '32-bit')
        self.assertEqual(result_32bit['unsigned'], 16909060)

    def test_convertToFloat_32bit(self):
        """Test 32-bit float conversion."""
        # IEEE 754 representation of 1.0 (little-endian: 00 00 80 3F)
        byte_data = bytes([0x00, 0x00, 0x80, 0x3F])
        results = self.converter.convertToFloat(byte_data, "little")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['value'], 1.0)
        self.assertEqual(results[0]['size'], '32-bit float')

    def test_convertToDouble_64bit(self):
        """Test 64-bit double conversion."""
        # IEEE 754 representation of 1.0 as double (little-endian)
        byte_data = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF0, 0x3F])
        results = self.converter.convertToDouble(byte_data, "little")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['value'], 1.0)
        self.assertEqual(results[0]['size'], '64-bit double')

    def test_convert_method_integration(self):
        """Test the main convert method."""
        # Test integer conversion
        results = self.converter.convert("01 02 03 04", "32-bit int", "little")
        self.assertTrue(len(results) > 0)
        self.assertTrue(any(r['size'] == '32-bit' for r in results))

        # Test float conversion
        results = self.converter.convert("00 00 80 3F", "32-bit float",
                                         "little")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['value'], 1.0)

        # Test double conversion
        results = self.converter.convert("00 00 00 00 00 00 F0 3F",
                                         "64-bit double", "little")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['value'], 1.0)

    def test_convert_invalid_data_type(self):
        """Test convert method with invalid data type."""
        with self.assertRaises(ValueError):
            self.converter.convert("01 02", "invalid-type", "little")


class TestHexFormatterUtility(unittest.TestCase):
    """Test cases for HexFormatterUtility class."""

    def test_validateHexInput_valid(self):
        """Test validation of valid hex input."""
        is_valid, error_msg = HexFormatterUtility.validateHexInput(
            "01 02 03 04")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")

        is_valid, error_msg = HexFormatterUtility.validateHexInput("ABCDEF")
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")

    def test_validateHexInput_invalid(self):
        """Test validation of invalid hex input."""
        is_valid, error_msg = HexFormatterUtility.validateHexInput("")
        self.assertFalse(is_valid)
        self.assertIn("Please enter", error_msg)

        is_valid, error_msg = HexFormatterUtility.validateHexInput("GG HH")
        self.assertFalse(is_valid)
        self.assertIn("No valid hexadecimal data found", error_msg)

    def test_formatResults_integer(self):
        """Test formatting of integer results."""
        results = [{
            'bytes': '01 02 03 04',
            'unsigned': 67305985,
            'signed': 67305985,
            'size': '32-bit',
            'type': 'integer'
        }]

        formatted = HexFormatterUtility.formatResults(results, "32-bit int",
                                                      "little")
        self.assertIn("Integer Conversions", formatted)
        self.assertIn("Little-Endian", formatted)
        self.assertIn("67305985", formatted)

    def test_formatResults_float(self):
        """Test formatting of float results."""
        results = [{
            'bytes': '00 00 80 3F',
            'value': 1.0,
            'size': '32-bit float',
            'type': 'float'
        }]

        formatted = HexFormatterUtility.formatResults(results, "32-bit float",
                                                      "little")
        self.assertIn("32-Bit Float Conversions", formatted)
        self.assertIn("Little-Endian", formatted)
        self.assertIn("1.0", formatted)

    def test_formatResults_empty(self):
        """Test formatting of empty results."""
        formatted = HexFormatterUtility.formatResults([], "32-bit int",
                                                      "little")
        self.assertIn("No valid conversions", formatted)


if __name__ == '__main__':
    unittest.main(verbosity=2)
