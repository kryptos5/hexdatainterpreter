"""
GUI module for HexDataInterpreter application.
Contains the user interface logic separated from business logic.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Optional

from hex_logic import HexConverter, HexFormatterUtility
from settings_manager import SettingsManager


class HexDataInterpreterGUI:
    """GUI controller for the hex data interpreter application."""

    def __init__(self, root: tk.Tk):
        """
        Initialize the GUI.
        
        Args:
            root: Main tkinter window
        """
        self.root = root
        self.root.title("Hex Data Interpreter")
        self.root.geometry("600x700")
        self.root.resizable(True, True)

        # Initialize business logic components
        self.hex_converter = HexConverter()
        self.settings_manager = SettingsManager()

        # GUI variables
        self.data_type = tk.StringVar()
        self.endianness = tk.StringVar()

        # UI components (will be set by setupUi)
        self.hex_text: Optional[tk.Text] = None
        self.results_text: Optional[tk.Text] = None

        # Load settings and setup UI
        self.loadSettings()
        self.setupUi()
        self.bindEvents()

        # Save settings when window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)

    def setupUi(self):
        """Set up the user interface components."""
        # Configure style
        style = ttk.Style()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame,
                                text="Hex Data Interpreter",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Input section
        self.setupInputSection(main_frame)

        # Options section
        self.setupOptionsSection(main_frame)

        # Buttons section
        self.setupButtonsSection(main_frame)

        # Results section
        self.setupResultsSection(main_frame)

    def setupInputSection(self, parent):
        """Set up the hex input section."""
        input_frame = ttk.LabelFrame(parent,
                                     text="Hex Data Input",
                                     padding="10")
        input_frame.grid(row=1,
                         column=0,
                         columnspan=2,
                         sticky="ew",
                         pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)

        # Hex input label
        input_label = ttk.Label(
            input_frame,
            text="Enter hexadecimal data (space-separated or continuous):")
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))

        # Text input with scrollbar
        text_frame = ttk.Frame(input_frame)
        text_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        text_frame.columnconfigure(0, weight=1)

        self.hex_text = tk.Text(text_frame,
                                height=4,
                                width=60,
                                wrap=tk.WORD,
                                font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(text_frame,
                                  orient=tk.VERTICAL,
                                  command=self.hex_text.yview)
        self.hex_text.configure(yscrollcommand=scrollbar.set)

        self.hex_text.grid(row=0, column=0, sticky="ew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Example text
        example_label = ttk.Label(
            input_frame,
            text="Examples: 01 02 03 04  •  3F800000  •  000000000000F03F",
            font=('Arial', 9),
            foreground='gray')
        example_label.grid(row=2, column=0, sticky=tk.W)

    def setupOptionsSection(self, parent):
        """Set up the conversion options section."""
        options_frame = ttk.LabelFrame(parent,
                                       text="Conversion Options",
                                       padding="10")
        options_frame.grid(row=2,
                           column=0,
                           columnspan=2,
                           sticky="ew",
                           pady=(0, 15))

        # Data type selection
        ttk.Label(options_frame, text="Data Type:").grid(row=0,
                                                         column=0,
                                                         sticky=tk.W,
                                                         pady=(0, 8))

        type_combo = ttk.Combobox(
            options_frame,
            textvariable=self.data_type,
            values=["32-bit int", "32-bit float", "64-bit double"],
            state="readonly",
            width=20)
        type_combo.grid(row=0,
                        column=1,
                        sticky=tk.W,
                        padx=(10, 0),
                        pady=(0, 8))

        # Endianness selection
        ttk.Label(options_frame, text="Byte Order:").grid(row=1,
                                                          column=0,
                                                          sticky=tk.W,
                                                          pady=(8, 0))

        endian_frame = ttk.Frame(options_frame)
        endian_frame.grid(row=1,
                          column=1,
                          sticky=tk.W,
                          padx=(10, 0),
                          pady=(8, 0))

        little_radio = ttk.Radiobutton(endian_frame,
                                       text="Little-Endian",
                                       variable=self.endianness,
                                       value="little")
        little_radio.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))

        big_radio = ttk.Radiobutton(endian_frame,
                                    text="Big-Endian",
                                    variable=self.endianness,
                                    value="big")
        big_radio.grid(row=0, column=1, sticky=tk.W)

    def setupButtonsSection(self, parent):
        """Set up the buttons section."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 15))

        convert_btn = ttk.Button(button_frame,
                                 text="Convert",
                                 command=self.onConvert,
                                 style='Accent.TButton')
        convert_btn.grid(row=0, column=0, padx=(0, 10))

        clear_btn = ttk.Button(button_frame,
                               text="Clear All",
                               command=self.onClear)
        clear_btn.grid(row=0, column=1, padx=(10, 0))

    def setupResultsSection(self, parent):
        """Set up the results display section."""
        results_frame = ttk.LabelFrame(parent,
                                       text="Conversion Results",
                                       padding="10")
        results_frame.grid(row=4,
                           column=0,
                           columnspan=2,
                           sticky="nsew",
                           pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        parent.rowconfigure(4, weight=1)

        # Results text area with scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.grid(row=0, column=0, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.results_text = tk.Text(text_frame,
                                    height=15,
                                    width=70,
                                    wrap=tk.WORD,
                                    state=tk.DISABLED,
                                    font=('Consolas', 9),
                                    bg='#f8f8f8')
        results_scrollbar = ttk.Scrollbar(text_frame,
                                          orient=tk.VERTICAL,
                                          command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scrollbar.set)

        self.results_text.grid(row=0, column=0, sticky="nsew")
        results_scrollbar.grid(row=0, column=1, sticky="ns")

    def bindEvents(self):
        """Bind event handlers."""
        # Auto-save settings when options change
        self.data_type.trace('w', self.onSettingChanged)
        self.endianness.trace('w', self.onSettingChanged)

        # Keyboard shortcuts
        self.root.bind('<Control-Return>', lambda e: self.onConvert())
        self.root.bind('<F5>', lambda e: self.onConvert())
        self.root.bind('<Control-l>', lambda e: self.onClear())

    def onConvert(self):
        """Handle convert button click."""
        try:
            # Get input
            if self.hex_text is None:
                return
            hex_input = self.hex_text.get(1.0, tk.END).strip()
            if not hex_input:
                messagebox.showerror("Error", "Please enter hexadecimal data.")
                return

            # Validate input first
            is_valid, error_msg = HexFormatterUtility.validateHexInput(
                hex_input)
            if not is_valid:
                messagebox.showerror("Invalid Input", error_msg)
                return

            # Get conversion parameters
            data_type = self.data_type.get()
            endianness = self.endianness.get()

            # Perform conversion
            results = self.hex_converter.convert(hex_input, data_type,
                                                 endianness)

            # Format and display results
            formatted_results = HexFormatterUtility.formatResults(
                results, data_type, endianness)
            self.displayResults(formatted_results)

        except ValueError as e:
            messagebox.showerror("Conversion Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error",
                                 f"An error occurred: {str(e)}")

    def onClear(self):
        """Handle clear button click."""
        if self.hex_text is not None:
            self.hex_text.delete(1.0, tk.END)
        self.clearResults()

    def displayResults(self, results_text: str):
        """
        Display conversion results.
        
        Args:
            results_text: Formatted results string
        """
        if self.results_text is not None:
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, results_text)
            self.results_text.config(state=tk.DISABLED)

    def clearResults(self):
        """Clear the results display."""
        if self.results_text is not None:
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.config(state=tk.DISABLED)

    def loadSettings(self):
        """Load settings from the settings manager."""
        settings = self.settings_manager.loadSettings()
        self.data_type.set(settings.get("DataType", "32-bit int"))
        self.endianness.set(settings.get("Endianness", "little"))

    def saveSettings(self):
        """Save current settings."""
        settings = {
            "DataType": self.data_type.get(),
            "Endianness": self.endianness.get()
        }
        self.settings_manager.saveSettings(settings)

    def onSettingChanged(self, *args):
        """Handle setting change events."""
        self.saveSettings()

    def onClosing(self):
        """Handle window closing event."""
        self.saveSettings()
        self.root.destroy()

    def run(self):
        """Start the GUI event loop."""
        self.root.mainloop()


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = HexDataInterpreterGUI(root)
    app.run()


if __name__ == "__main__":
    main()
