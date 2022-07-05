# project-for-pyforge3

Before using it is required to run the docker container with PostgreSQL.
```
docker pull postgres
```
```
docker run -p 5432:5432 -e POSTGRES_PASSWORD=password postgres
```
```
git clone https://github.com/AlexandraVin/project-for-pyforge3.git 
```
```
cd project-for-pyforge3
```

To build docker image with script to load data:
```
docker image build -t pyforge3:0.0.1 -f Dockerfile1 .
```
```
docker run -v $(pwd)/config.json:/usr/src/config.json --network=host pyforge3:0.0.1 STI   
```
where STI - name of compound load

To build docker image with script to read data:
```
docker image build -t pyforge3-list:0.0.1 -f Dockerfile2 .
```
```
docker run -v $(pwd)/config.json:/usr/src/config.json --network=host pyforge3-list:0.0.1
```
## How to use:
run 
```load_data.py XP9 18W 29P G54```

output:
```
argument "G54" was ignored
Compound(XP9)
Compound(29P)
Compound(18W)
```
use ```read_data.py``` to read data from database
output:
```
formula       id            compound      inchi_key     smiles        inchi         name          cross_link...
C20 H22 N2 O9 3             18W           MBSNQHZDAB... Cc1c(c(c([... InChI=1S/C... 3-[(5Z)-5-... 2
C20 H24 N2 O9 2             29P           DHEOBTWDCM... Cc1c(c(c([... InChI=1S/C... 3-[(5S)-5-... 2
C13 H26 N ... 1             XP9           WUTPSGIFCC... CC(C(C(=O)... InChI=1S/C... O-phosphon... 3
```
## config.json
* engine - URI of a PostgreSQL database
* filemode_for_logger - [mode](https://docs.python.org/3/library/functions.html#open) for logger file
* support_list - the list of supported arguments (endpoints)
* compounds_url - URL to download data on compounds
* timeout - one-request connection timeout
* limit - maximum number of lines to read with read_data.py
## testing:
use ```pytest tests``` to run all tests
output:
```
===================== test session starts =====================
platform win32 -- Python 3.9.6, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: C:\Users\evgeniy.varganov\Desktop\proj\project-for-pyforge3
plugins: allure-pytest-2.9.43
collected 8 items

tests\db_helper_test.py ...                              [ 37%]
tests\load_data_test.py .....                            [100%]

====================== 8 passed in 2.13s ======================
```
