import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from load_data import get_compounds
from upload_data import Compound, parse_json_to_compounds, insert_compounds

engine = create_engine(
    "postgresql+psycopg2://postgres:password@localhost:5432/postgres")
Session = sessionmaker(bind=engine)


def read_test_json(file_name):
    with open(file_name) as f:
        return json.loads(f.read())


if __name__ == '__main__':
    Compound.metadata.create_all(engine)
    json_data = get_compounds(
        'ADP',
        'ATP',
        'STI',
        'ZID',
        'DPM',
        'XP9',
        '18W',
        '29P',
    )

    list_compounds = []
    for j in json_data:
        list_compounds.extend(parse_json_to_compounds(j))
    insert_compounds(list_compounds, Session)

    with Session() as session:
        for x in session.query(Compound).all():
            print(x.name)
