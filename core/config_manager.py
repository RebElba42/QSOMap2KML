import json
import os

class ConfigManager:
    CONFIG_PATH = "config/settings.json"

    @staticmethod
    def load():
        if not os.path.exists(ConfigManager.CONFIG_PATH):
            return {}
        with open(ConfigManager.CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save(config):
        with open(ConfigManager.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)