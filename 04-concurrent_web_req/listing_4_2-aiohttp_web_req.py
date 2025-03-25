# listing 4.2
# Making an aiohttp web request


import asyncio

import aiohttp
from aiohttp import ClientSession
from util import async_timed


@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    # access session using async with statement, returns result/response
    async with session.get(url) as response:
        return response.status


@async_timed()
async def main():
    # create a client http session
    async with aiohttp.ClientSession() as session:
        url = "https://www.example.com"
        # use session and url provided to get status code by calling `fetch_status` func
        status = await fetch_status(session, url)
        print(f"Status for {url} was {status}")


if __name__ == "__main__":
    asyncio.run(main())
