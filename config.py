import json


class Config:
    def __init__(self) -> None:
        with open('config.json') as f:
            config = json.loads(f.read())
        for k, v in config.items():
            self.__setattr__(k, v)


CONFIG = Config()
