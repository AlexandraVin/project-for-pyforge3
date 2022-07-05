import json
from db_helper import Compound
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Config:
    def __init__(self, config_path) -> None:
        with open(config_path) as f:
            config = json.loads(f.read())
        for k, v in config.items():
            setattr(self, k, v)

        engine = create_engine(self.engine)
        Session = sessionmaker(bind=engine)
        Compound.metadata.create_all(engine)
        self.session_maker = Session


def extract_config(args: list[str]) -> Config:
    if '--config' in args:
        i = args.index('--config')
        config_path = args[i + 1]
        del args[i: i + 2]
    else:
        config_path = 'config.json'
    return Config(config_path)
