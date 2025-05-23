import json
from utils.app_utils import resource_path 
import logging

class I18n:
    def __init__(self, lang="en"):
        self.lang = lang
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        path = resource_path(f"resources/translations/{self.lang}.json")
        logging.debug(f"Load i18n from path: {path} ")
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            logging.error(f"Load i18n from path: {path} - failed")
            self.translations = {}

    def t(self, key):
        return self.translations.get(key, key)