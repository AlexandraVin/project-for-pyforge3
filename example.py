import json
import subprocess
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
import logging

from load_data import get_compounds
from db_helper import Compound, insert_compounds


def run_cmd(cmd):
    proc = subprocess.run(cmd, capture_output=True)
    err = proc.stderr.decode("utf-8").strip()
    if proc.returncode != 0:
        err = err.strip()
        print(err)
        raise subprocess.CalledProcessError(
            proc.returncode, cmd, proc.stdout, proc.stderr)
    res = proc.stdout.decode("utf-8").strip() + '\n' + err
    return res.strip()



if __name__ == '__main__':

    
    print(run_cmd('load_data.py XP9 18W 29P 5444'))
    print(run_cmd('read_data.py'))

