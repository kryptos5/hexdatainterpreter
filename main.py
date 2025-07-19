"""
Main entry point for the Hex Data Interpreter application.
This module provides the main entry point and can be used for both GUI and CLI modes.
"""

import sys
import tkinter as tk

from hex_gui import HexDataInterpreterGUI
from hex_logic import HexConverter, HexFormatterUtility


def run_gui():
    """Run the application in GUI mode."""
    root = tk.Tk()
    app = HexDataInterpreterGUI(root)
    app.run()


def run_cli(hex_input: str,
            data_type: str = "32-bit int",
            endianness: str = "little"):
    """
    Run the application in CLI mode.
    
    Args:
        hex_input: Hexadecimal input string
        data_type: Target data type
        endianness: Byte order
    """
    try:
        converter = HexConverter()
        results = converter.convert(hex_input, data_type, endianness)
        formatted_results = HexFormatterUtility.formatResults(
            results, data_type, endianness)
        print(formatted_results)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    """Main entry point with command line argument support."""
    if len(sys.argv) == 1:
        # No arguments, run GUI
        run_gui()
    elif len(sys.argv) >= 2:
        # Command line arguments provided, run CLI
        hex_input = sys.argv[1]
        data_type = sys.argv[2] if len(sys.argv) > 2 else "32-bit int"
        endianness = sys.argv[3] if len(sys.argv) > 3 else "little"

        # Validate data_type
        valid_types = ["32-bit int", "32-bit float", "64-bit double"]
        if data_type not in valid_types:
            print(
                f"Error: Invalid data type '{data_type}'. Valid types: {', '.join(valid_types)}"
            )
            sys.exit(1)

        # Validate endianness
        valid_endianness = ["little", "big"]
        if endianness not in valid_endianness:
            print(
                f"Error: Invalid endianness '{endianness}'. Valid values: {', '.join(valid_endianness)}"
            )
            sys.exit(1)

        run_cli(hex_input, data_type, endianness)
    else:
        print("Usage:")
        print("  python main.py                              # Run GUI mode")
        print(
            "  python main.py <hex_data>                   # CLI mode with defaults"
        )
        print(
            "  python main.py <hex_data> <type>            # CLI mode with data type"
        )
        print(
            "  python main.py <hex_data> <type> <endian>   # CLI mode with all options"
        )
        print()
        print("Examples:")
        print("  python main.py '01 02 03 04'")
        print("  python main.py '3F800000' '32-bit float' 'little'")
        print("  python main.py '000000000000F03F' '64-bit double' 'little'")


if __name__ == "__main__":
    main()
