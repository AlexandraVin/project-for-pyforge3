from db_helper import get_session_maker, read_compounds
from config import Config

if __name__ == "__main__":
    config = Config('config.json')
    session_maker = get_session_maker(config.engine)
    res = read_compounds(session_maker)
    res = '\n'.join(res)
    print(res)
