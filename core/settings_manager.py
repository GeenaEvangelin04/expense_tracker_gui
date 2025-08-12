#core/settings_manager.py
import json
import os
import logging

logger = logging.getLogger(__name__)

# Use package-relative path for settings.json
DEFAULT_SETTINGS_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    'data',
    'settings.json'
)

class SettingsManager:
    def __init__(self, filepath=None):
        # Use provided filepath or fall back to package-relative default
        self.filepath = os.path.normpath(filepath or DEFAULT_SETTINGS_PATH)
        # Ensure the folder exists before saving
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        # Default settings
        self.settings = {
            "monthly_budget": 25000,
            "currency_symbol": "₹",
            "theme": "litera",
            "csv_delimiter": ","
        }
        self.load_settings()

    def load_settings(self):
        """Load settings from file, falling back to defaults on error."""
        if not os.path.exists(self.filepath):
            self.save_settings()
        else:
            try:
                with open(self.filepath, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.settings.update(data)
            except (json.JSONDecodeError, IOError):
                logger.exception("Error loading settings; using default values.")

    def save_settings(self):
        """Write current settings to file."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(self.settings, file, indent=4)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def reset_defaults(self):
        """Restore default settings and save them."""
        self.settings = {
            "monthly_budget": 25000,
            "currency_symbol": "₹",
            "theme": "litera",
            "csv_delimiter": ","
        }
        self.save_settings()

    # ✅ Additional helper methods
    def get_theme(self):
        return self.get("theme", "litera")

    def get_budget(self):
        return self.get("monthly_budget", 25000)

    def get_currency(self):
        return self.get("currency_symbol", "₹")
