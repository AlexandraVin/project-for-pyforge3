import sys
from db_helper import read_compounds
from config import extract_config

if __name__ == "__main__":
    config = extract_config(sys.argv)
    res = read_compounds(config)
    res = '\n'.join(res)
    print(res)
