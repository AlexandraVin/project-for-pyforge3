import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
import logging

from load_data import get_compounds
from upload_data import Compound, parse_json_to_compounds, insert_compounds


def read_test_json(file_name):
    with open(file_name) as f:
        return json.loads(f.read())


class Config:
    def __init__(self) -> None:
        with open('config.json') as f:
            config = json.loads(f.read())
        for k, v in config.items():
            self.__setattr__(k, v)


if __name__ == '__main__':

    config = Config()
    engine = create_engine(config.engine)
    Session = sessionmaker(bind=engine)

    logging.basicConfig(filename=f'logs/{date.today()}.log',
                        filemode=config.filemode_for_logger,
                        format='%(asctime)s:%(msecs)d\t%(name)s\t%(levelname)s\t%(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    Compound.metadata.create_all(engine)
    json_data = get_compounds(*config.compounds_to_load)

    # list_compounds = []
    # for j in json_data:
    #     list_compounds.append(j)
    # insert_compounds(list_compounds, Session)
    insert_compounds(json_data, Session)

    with Session() as session:
        for x in session.query(Compound).all():
            print(x.name)
