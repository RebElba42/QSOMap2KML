import json
import os

class I18n:
    def __init__(self, lang="en"):
        self.lang = lang
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        path = f"resources/translations/{self.lang}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)

    def t(self, key):
        return self.translations.get(key, key)