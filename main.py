import json
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/postgres")
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Compound(Base):
    n = 1000
    __tablename__ = 'compounds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    compound = Column(String(3))
    name = Column(String(n))
    formula = Column(String(n))
    inchi = Column(String(n))
    inchi_key = Column(String(n))
    smiles = Column(String(n))
    cross_links_count = Column(Integer)

    def __str__(self):
        return f'{self.compound}: {self.name}'

    def __repr__(self):
        return f'Compound({self.compound}={self.name})'


def read_test_json(file_name):
    with open(file_name) as f:
        return json.loads(f.read())


def parse_json_to_compounds(json):
    result = []
    for compound_key in json:
        for compound in json[compound_key]:
            name = compound['name']
            formula = compound['formula']
            inchi = compound['inchi']
            inchi_key = compound['inchi_key']
            smiles = compound['smiles']
            cross_links_count = len(compound['cross_links'])
            result.append(
                Compound(
                    compound=compound_key,
                    name=name,
                    formula=formula,
                    inchi=inchi,
                    inchi_key=inchi_key,
                    smiles=smiles,
                    cross_links_count=cross_links_count
                )
            )
    return result


def insert_compounds(list_compounds):
    with Session() as session:
        for c in list_compounds:
            session.add(c)
        session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    test_json = read_test_json('ATP.json')
    list_compounds = parse_json_to_compounds(test_json)
    insert_compounds(list_compounds)

    with Session() as session:
        for x in session.query(Compound).all():
            print(x.name)

