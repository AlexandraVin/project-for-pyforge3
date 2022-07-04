import json


class Config:
    def __init__(self, config_path) -> None:
        with open(config_path) as f:
            config = json.loads(f.read())
        for k, v in config.items():
            setattr(self, k, v)
