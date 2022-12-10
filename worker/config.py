from os import PathLike
from configparser import ConfigParser
from pathlib import Path

defaults = {
    "DEFAULT": {
        "work type": "training, inference",
        "mediamanager location": "ws://localhost:8000/ws/auto_tag/",
        "client id": "<CLIENT ID>",
        "client secret": "<CLIENT SECRET>"
    }
}


class Config:
    def __init__(self, config_path: PathLike):
        self.path = Path(config_path)
        self.parser = ConfigParser()
        self.parser.read_dict(defaults)
        if self.path.is_file():
            self.parser.read(self.path)
        else:
            with self.path.open("w") as f:
                self.parser.write(f)
            print("Written default config file to", self.path)
            print("Please review this file to ensure the configuration is correct")

    @property
    def server_uri(self):
        return self.parser.get("DEFAULT", "mediamanager location")

    @property
    def do_training(self):
        return "training" in self.parser.get("DEFAULT", "work type")

    @property
    def do_inference(self):
        return "inference" in self.parser.get("DEFAULT", "work type")

    @property
    def client_id(self):
        return self.parser.get("DEFAULT", "client id")

    @property
    def client_secret(self):
        return self.parser.get("DEFAULT", "client secret")


config: Config
