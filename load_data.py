import asyncio
import sys

from aiohttp import ClientSession, ClientTimeout
import json
import logging
from datetime import date
from upload_data import Compound, parse_json_to_compounds


async def fetch_all(urls: list):
    """ Fetch all URLs """
    tasks = []
    logging.debug(f'fetch_all urls = {urls}')

    async with ClientSession(timeout=ClientTimeout(total=1)) as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        a = await asyncio.gather(*tasks)
    return a


async def fetch(url: str, session: ClientSession) -> list[Compound]:
    """ Fetch a single URL """
    async with session.get(url) as response:
        resp = await response.read()
        logging.info(
            f'fetch finished url = {url} (Status: {response.status})')
        resp = json.loads(resp.decode("utf-8"))
        return parse_json_to_compounds(resp)


def get_compounds(*args):

    url = 'https://www.ebi.ac.uk/pdbe/graph-api/compound/summary/'
    logging.debug(f'get_compounds url = {url}, args = {args}')
    urls = [url + x for x in args]

    loop = asyncio.get_event_loop()
    total_future = asyncio.ensure_future(fetch_all(urls))

    resp = loop.run_until_complete(total_future)
    res = []
    for r in resp:
        res.extend(r)
    return res


if __name__ == "__main__":
    logging.basicConfig(filename=f'logs/load_data.log',
                        filemode='w',
                        format='%(asctime)s:%(msecs)d\t%(name)s\t%(levelname)s\t%(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    support_list = ['ADP',
                    'ATP',
                    'STI',
                    'ZID',
                    'DPM',
                    'XP9',
                    '18W',
                    '29P',
                    ]

    if len(sys.argv) > 1:
        arg_set = set(sys.argv[1:])
        ignored = arg_set-set(support_list)
        if ignored:
            for arg in list(ignored):
                msg = f'argument "{arg}" was ignored'
                print(msg)
                logging.warning(msg)
        compounds = list(arg_set - ignored)
        res = get_compounds(*compounds)
        print(*res, sep='\n')
    else:
        support = '\n'.join(support_list)
        print(
            f'Expected at least one argument\nThese arguments are supported: \n{support}')
