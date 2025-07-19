"""
Core hex conversion logic separated from GUI.
This module contains the business logic for converting hexadecimal data
to various numeric formats with support for different endianness.
"""

import re
import struct
from typing import Any, Dict, List, Union


class HexConverter:
    """Core hex conversion functionality."""

    def __init__(self):
        """Initialize the hex converter."""
        pass

    def parseHexInput(self, hex_input: str) -> bytes:
        """
        Parse and validate hexadecimal input string.
        
        Args:
            hex_input: String containing hexadecimal data (space-separated or continuous)
            
        Returns:
            bytes: Parsed hex data as bytes
            
        Raises:
            ValueError: If input contains invalid hexadecimal data
        """
        if not hex_input.strip():
            return b''

        # Remove any non-hex characters except spaces
        cleaned_input = re.sub(r'[^0-9a-fA-F\s]', '', hex_input.strip())

        # Split by whitespace and filter empty strings
        hex_parts = [part for part in cleaned_input.split() if part]

        if not hex_parts:
            raise ValueError("No valid hexadecimal data found")

        # Ensure each part is even length (pad with leading 0 if necessary)
        padded_parts = []
        for part in hex_parts:
            if len(part) % 2 != 0:
                part = '0' + part
            padded_parts.append(part)

        # Join all padded parts
        hex_string = ''.join(padded_parts)

        # Validate and convert
        try:
            return bytes.fromhex(hex_string)
        except ValueError as e:
            raise ValueError(f"Invalid hexadecimal data: {e}")

    def convertToInt(self, byte_data: bytes,
                     endianness: str) -> List[Dict[str, Any]]:
        """
        Convert bytes to integer representations.
        
        Args:
            byte_data: Raw bytes to convert
            endianness: 'little' or 'big' endian byte order
            
        Returns:
            List of dictionaries containing conversion results
        """
        if not byte_data:
            return []

        results = []
        endian_char = '<' if endianness == 'little' else '>'

        # 32-bit integer conversion
        if len(byte_data) >= 4:
            for i in range(0, len(byte_data), 4):
                chunk = byte_data[i:i + 4]
                if len(chunk) == 4:
                    unsigned = struct.unpack(f'{endian_char}I', chunk)[0]
                    signed = struct.unpack(f'{endian_char}i', chunk)[0]
                    results.append({
                        'bytes': ' '.join(f'{b:02X}' for b in chunk),
                        'unsigned': unsigned,
                        'signed': signed,
                        'size': '32-bit',
                        'type': 'integer'
                    })

        # 16-bit integer conversion
        if len(byte_data) >= 2:
            for i in range(0, len(byte_data), 2):
                chunk = byte_data[i:i + 2]
                if len(chunk) == 2:
                    unsigned = struct.unpack(f'{endian_char}H', chunk)[0]
                    signed = struct.unpack(f'{endian_char}h', chunk)[0]
                    results.append({
                        'bytes': ' '.join(f'{b:02X}' for b in chunk),
                        'unsigned': unsigned,
                        'signed': signed,
                        'size': '16-bit',
                        'type': 'integer'
                    })

        # 8-bit integer conversion (endianness doesn't matter for single bytes)
        for byte_val in byte_data:
            signed = struct.unpack('b', bytes([byte_val]))[0]
            results.append({
                'bytes': f'{byte_val:02X}',
                'unsigned': byte_val,
                'signed': signed,
                'size': '8-bit',
                'type': 'integer'
            })

        return results

    def convertToFloat(self, byte_data: bytes,
                       endianness: str) -> List[Dict[str, Any]]:
        """
        Convert bytes to 32-bit float representations.
        
        Args:
            byte_data: Raw bytes to convert
            endianness: 'little' or 'big' endian byte order
            
        Returns:
            List of dictionaries containing conversion results
        """
        if not byte_data or len(byte_data) < 4:
            return []

        results = []
        endian_char = '<' if endianness == 'little' else '>'

        # 32-bit float conversion
        for i in range(0, len(byte_data), 4):
            chunk = byte_data[i:i + 4]
            if len(chunk) == 4:
                try:
                    value = struct.unpack(f'{endian_char}f', chunk)[0]
                    results.append({
                        'bytes': ' '.join(f'{b:02X}' for b in chunk),
                        'value': value,
                        'size': '32-bit float',
                        'type': 'float'
                    })
                except struct.error as e:
                    # Handle potential struct unpacking errors
                    results.append({
                        'bytes': ' '.join(f'{b:02X}' for b in chunk),
                        'value': f"Error: {e}",
                        'size': '32-bit float',
                        'type': 'float'
                    })

        return results

    def convertToDouble(self, byte_data: bytes,
                        endianness: str) -> List[Dict[str, Any]]:
        """
        Convert bytes to 64-bit double representations.
        
        Args:
            byte_data: Raw bytes to convert
            endianness: 'little' or 'big' endian byte order
            
        Returns:
            List of dictionaries containing conversion results
        """
        if not byte_data or len(byte_data) < 8:
            return []

        results = []
        endian_char = '<' if endianness == 'little' else '>'

        # 64-bit double conversion
        for i in range(0, len(byte_data), 8):
            chunk = byte_data[i:i + 8]
            if len(chunk) == 8:
                try:
                    value = struct.unpack(f'{endian_char}d', chunk)[0]
                    results.append({
                        'bytes': ' '.join(f'{b:02X}' for b in chunk),
                        'value': value,
                        'size': '64-bit double',
                        'type': 'double'
                    })
                except struct.error as e:
                    # Handle potential struct unpacking errors
                    results.append({
                        'bytes': ' '.join(f'{b:02X}' for b in chunk),
                        'value': f"Error: {e}",
                        'size': '64-bit double',
                        'type': 'double'
                    })

        return results

    def convert(self, hex_input: str, data_type: str,
                endianness: str) -> List[Dict[str, Any]]:
        """
        Convert hex input to specified data type and endianness.
        
        Args:
            hex_input: Hexadecimal input string
            data_type: Target data type ('32-bit int', '32-bit float', '64-bit double')
            endianness: Byte order ('little' or 'big')
            
        Returns:
            List of conversion results
            
        Raises:
            ValueError: If input is invalid or conversion fails
        """
        # Parse the hex input
        byte_data = self.parseHexInput(hex_input)

        # Convert based on data type
        if data_type == "32-bit int":
            return self.convertToInt(byte_data, endianness)
        elif data_type == "32-bit float":
            return self.convertToFloat(byte_data, endianness)
        elif data_type == "64-bit double":
            return self.convertToDouble(byte_data, endianness)
        else:
            raise ValueError(f"Unsupported data type: {data_type}")


class HexFormatterUtility:
    """Utility class for formatting hex conversion results."""

    @staticmethod
    def formatResults(results: List[Dict[str, Any]], data_type: str,
                      endianness: str) -> str:
        """
        Format conversion results for display.
        
        Args:
            results: List of conversion result dictionaries
            data_type: The data type that was converted
            endianness: The endianness used
            
        Returns:
            Formatted string ready for display
        """
        if not results:
            return "No valid conversions possible with the given data."

        endian_text = "Little-Endian" if endianness == "little" else "Big-Endian"
        output_lines = []

        if data_type == "32-bit int":
            output_lines.append(f"Integer Conversions ({endian_text}):")
            output_lines.append("=" * 50)
            output_lines.append("")

            for i, result in enumerate(results):
                output_lines.append(f"Conversion {i+1}:")
                output_lines.append(f"  Bytes: {result['bytes']}")
                output_lines.append(f"  Size: {result['size']}")
                output_lines.append(f"  Unsigned: {result['unsigned']}")
                output_lines.append(f"  Signed: {result['signed']}")
                output_lines.append("-" * 30)

        elif data_type in ["32-bit float", "64-bit double"]:
            output_lines.append(
                f"{data_type.title()} Conversions ({endian_text}):")
            output_lines.append("=" * 50)
            output_lines.append("")

            for i, result in enumerate(results):
                output_lines.append(f"Conversion {i+1}:")
                output_lines.append(f"  Bytes: {result['bytes']}")
                output_lines.append(f"  Size: {result['size']}")
                output_lines.append(f"  Value: {result['value']}")
                output_lines.append("-" * 30)

        return "\n".join(output_lines)

    @staticmethod
    def validateHexInput(hex_input: str) -> tuple[bool, str]:
        """
        Validate hex input without converting it.
        
        Args:
            hex_input: Input string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not hex_input.strip():
            return False, "Please enter hexadecimal data."

        # Remove any non-hex characters except spaces
        cleaned_input = re.sub(r'[^0-9a-fA-F\s]', '', hex_input.strip())

        # Split by whitespace and filter empty strings
        hex_parts = [part for part in cleaned_input.split() if part]

        if not hex_parts:
            return False, "No valid hexadecimal data found."

        # Validate each part
        for part in hex_parts:
            try:
                int(part, 16)
            except ValueError:
                return False, f"Invalid hexadecimal value: {part}"

        return True, ""
