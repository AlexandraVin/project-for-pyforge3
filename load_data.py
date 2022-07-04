import asyncio
import sys
import json
from aiohttp import ClientSession, ClientTimeout
import json
import logging
from datetime import date

from config import CONFIG
from db_helper import Compound, insert_compounds, parse_json_to_compounds


async def fetch_all(urls: list):
    """ Fetch all URLs """
    tasks = []
    logging.debug(f'fetch_all urls = {urls}')

    async with ClientSession(timeout=ClientTimeout(total=CONFIG.timeout)) as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        resp = await asyncio.gather(*tasks)
    res = []
    for r in resp:
        res.extend(r)
    return res


async def fetch(url: str, session: ClientSession) -> list[Compound]:
    """ Fetch a single URL """
    async with session.get(url) as response:
        resp = await response.read()
        logging.info(
            f'fetch finished url = {url} (Status: {response.status})')
        resp = json.loads(resp.decode("utf-8"))
        return parse_json_to_compounds(resp)


def get_compounds(*args):

    url = CONFIG.compounds_url
    logging.debug(f'get_compounds url = {url}, args = {args}')
    urls = [url + x for x in args]

    loop = asyncio.get_event_loop()
    total_future = asyncio.ensure_future(fetch_all(urls))
    res = loop.run_until_complete(total_future)
    return res


def main(args):
    logging.basicConfig(filename=f'load_data.log',
                        filemode=CONFIG.filemode_for_logger,
                        format='%(asctime)s:%(msecs)d\t%(name)s\t%(levelname)s\t%(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    support_list = CONFIG.support_list

    if len(args) > 1:
        arg_set = set(args[1:])
        ignored = arg_set-set(support_list)
        if ignored:
            for arg in ignored:
                msg = f'argument "{arg}" was ignored'
                print(msg)
                logging.warning(msg)
        compounds = list(arg_set - ignored)
        res = get_compounds(*compounds)
        print(*res, sep='\n')

        insert_compounds(res)
    else:
        support = '\n'.join(support_list)
        print(
            f'Expected at least one argument\nThese arguments are supported: \n{support}')


if __name__ == "__main__":
    main(sys.argv)
