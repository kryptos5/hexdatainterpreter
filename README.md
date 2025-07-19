# Hexadecimal to Number Converter

A Python GUI application that converts hexadecimal binary data to integers or floating point numbers with support for both little-endian and big-endian byte order.

## Features

- **User-friendly GUI**: Clean interface with text input and dropdown selection
- **Multiple data types**: Convert to integers (8-bit, 16-bit, 32-bit), 32-bit float, or 64-bit double
- **Endianness support**: Choose between little-endian and big-endian byte order
- **Settings persistence**: Your conversion preferences are automatically saved and restored
- **Flexible input**: Accepts hexadecimal data separated by spaces
- **Comprehensive output**: Shows both signed and unsigned integer values, multiple data type interpretations

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)

## Usage

1. Run the application:
   ```
   python hex_converter.py
   ```

2. Enter hexadecimal data in the text box, separated by spaces
   - Example: `01 02 03 04`
   - Example: `3F800000` (for a 32-bit float)
   - Example: `000000000000F03F` (for a 64-bit double)

3. Select the target data type from the dropdown:
   - **int**: Converts to various integer formats (8-bit, 16-bit, 32-bit)
   - **32-bit float**: Converts to 32-bit IEEE 754 floating point
   - **64-bit double**: Converts to 64-bit IEEE 754 double precision

4. Choose the byte order:
   - **Little-Endian**: Least significant byte first
   - **Big-Endian**: Most significant byte first

5. Click "Convert" to see the results

6. Use "Clear All" to reset the input and output fields

## Examples

### Integer Conversion (Little-Endian)
Input: `01 02 03 04`
- 8-bit: Each byte converted separately (1, 2, 3, 4)
- 16-bit: `01 02` → 513, `03 04` → 1027
- 32-bit: `01 02 03 04` → 67305985

### Integer Conversion (Big-Endian)
Input: `01 02 03 04`
- 8-bit: Each byte converted separately (1, 2, 3, 4)
- 16-bit: `01 02` → 258, `03 04` → 772
- 32-bit: `01 02 03 04` → 16909060

### 32-bit Float Conversion
Input: `00 00 80 3F` (Little-Endian)
- Result: 1.0

### 64-bit Double Conversion
Input: `00 00 00 00 00 00 F0 3F` (Little-Endian)
- Result: 1.0

## Technical Details

- Uses Python's `struct` module for binary data interpretation
- Supports both little-endian (`<`) and big-endian (`>`) byte order
- Handles both signed and unsigned integer interpretations
- Implements IEEE 754 floating point formats
- Uses camelCase naming convention for methods
- **Settings persistence**: Stores user preferences in Windows Registry under `HKEY_CURRENT_USER\SOFTWARE\HexDataInterpreter`
- Automatically saves settings when changed and loads them on startup
- Gracefully handles non-Windows platforms (settings won't persist but app will work)

## File Structure

```
hextonumberconverter/
├── hex_converter.py       # Main application file
├── debug_test.py         # Test script for validation
├── test_converter.py     # Additional test utilities
├── test_registry.py      # Registry functionality tests
├── test_persistence.py   # Settings persistence tests
└── README.md            # This documentation
```
