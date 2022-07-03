from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


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


def insert_compounds(list_compounds, sessionmarker):
    with sessionmarker() as session:
        for c in list_compounds:
            session.add(c)
        session.commit()
