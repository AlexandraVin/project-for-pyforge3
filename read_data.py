from db_helper import read_compounds

if __name__ == "__main__":
    res = read_compounds()
    res = '\n'.join(res)
    print(res)
