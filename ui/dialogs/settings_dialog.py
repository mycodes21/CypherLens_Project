import customtkinter as ctk
from tkinter import messagebox
from backend.config_manager import ConfigManager

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("400x400")
        self.current_settings = ConfigManager.load_settings()
        self.entries = {}

        ctk.CTkLabel(self, text="CNC Parameters", font=("Arial", 16, "bold")).pack(pady=10)
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.add_input("Feed Rate (mm/min):", "feed_rate")
        self.add_input("Safe Z (mm):", "safe_z")
        self.add_input("Cut Depth (mm):", "cut_depth")
        self.add_input("Spindle Speed:", "spindle_speed")

        ctk.CTkButton(self, text="Save", command=self.save).pack(pady=10)

    def add_input(self, text, key):
        row = ctk.CTkFrame(self.frame, fg_color="transparent")
        row.pack(fill="x", pady=5)
        ctk.CTkLabel(row, text=text, width=150, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(row)
        entry.insert(0, str(self.current_settings.get(key, 0)))
        entry.pack(side="right")
        self.entries[key] = entry

    def save(self):
        new_data = {}
        try:
            for key, entry in self.entries.items():
                new_data[key] = float(entry.get())
            ConfigManager.save_settings(new_data)
            self.destroy()
        except:
            messagebox.showerror("Error", "Invalid numbers")