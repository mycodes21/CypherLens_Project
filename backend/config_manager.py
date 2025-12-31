import json
import os

CONFIG_FILE = "settings.json"

# Podrazumevane vrednosti (ako fajl ne postoji)
DEFAULT_SETTINGS = {
    "feed_rate": 1000,      # mm/min
    "plunge_rate": 300,     # mm/min
    "safe_z": 5.0,          # mm
    "cut_depth": 2.0,       # mm
    "tool_diameter": 3.175, # mm
    "spindle_speed": 12000  # RPM
}

class ConfigManager:
    @staticmethod
    def load_settings():
        """Učitava podešavanja iz JSON fajla ili vraća default."""
        if not os.path.exists(CONFIG_FILE):
            return DEFAULT_SETTINGS.copy()
        
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                # Spojimo sa default vrednostima (da ne pukne ako nešto fali)
                settings = DEFAULT_SETTINGS.copy()
                settings.update(data)
                return settings
        except:
            return DEFAULT_SETTINGS.copy()

    @staticmethod
    def save_settings(new_settings):
        """Čuva podešavanja u JSON fajl."""
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(new_settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False