from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


def normalize_str(arg: str):
    arg = str(arg)
    length = len(arg)
    if length > 13:
        arg = arg[:10] + '...'
    if length < 13:
        arg += ' ' * (13 - length)
    return arg + ' '


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

    def __str__(self) -> str:
        return f'Compound({self.compound})'

    def row(self) -> str:
        res = ''
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                res += normalize_str(v)
        return res

    def header(self) -> str:
        res = ''
        for k in self.__dict__.keys():
            if not k.startswith('_'):
                res += normalize_str(k)
        return res

    def __repr__(self) -> str:
        return str(self)


def parse_json_to_compounds(json) -> list[Compound]:
    result = []
    for compound_key in json.keys():
        for compound in json[compound_key]:
            kwargs = dict(compound=compound_key,
                          name=compound['name'],
                          formula=compound['formula'],
                          inchi=compound['inchi'],
                          inchi_key=compound['inchi_key'],
                          smiles=compound['smiles'],
                          cross_links_count=len(compound['cross_links']))
            result.append(Compound(**kwargs))
    return result


def insert_compounds(config, list_compounds):
    with config.session_maker() as session:
        for c in list_compounds:
            session.add(c)
        session.commit()


def read_compounds(config) -> list[str]:
    with config.session_maker() as session:
        data = session.query(Compound).order_by(
            Compound.id.desc()).limit(config.limit).all()
    res = []
    if data:
        res.append(data[0].header())
        for c in data:
            res.append(c.row())
    return res
