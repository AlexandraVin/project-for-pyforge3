import asyncio
from aiohttp import ClientSession
import async_timeout
import json


async def fetch_all(urls: list):
    """ Fetch all URLs """
    tasks = []

    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        a = await asyncio.gather(*tasks)
    return a


async def fetch(url: str, session: object):
    """ Fetch a single URL """
    async with async_timeout.timeout(1):
        async with session.get(url) as response:
            resp = await response.read()
            resp = json.loads(resp.decode("utf-8"))
            return resp


def get_compounds(*args):

    url = 'https://www.ebi.ac.uk/pdbe/graph-api/compound/summary/'

    urls = [url + x for x in args]

    loop = asyncio.get_event_loop()
    total_future = asyncio.ensure_future(fetch_all(urls))

    res = loop.run_until_complete(total_future)

    return res


if __name__ == "__main__":
    res = get_compounds(
        'ADP',
        'ATP',
        'STI',
        'ZID',
        'DPM',
        'XP9',
        '18W',
        '29P',
    )
    print(len(res))
