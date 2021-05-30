import json
from pathlib import Path


class Settings:
    def __init__(self, config):
        self.config_file = Path('../' + config)

        with open(self.config_file, 'r') as conf:
            self.config = json.load(conf)

    def get(self, key):
        return self.config[key]

    def set(self, key, value):
        self.config[key] = value
        self.save()

    def save(self):
        with open(self.config_file, 'w') as conf:
            conf.write(json.dumps(self.config, indent=4))
