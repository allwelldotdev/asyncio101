# listing 4.3
# Setting timeouts with aiohttp


import asyncio

import aiohttp
from aiohttp import ClientSession
from util import async_timed


@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    time_in_millis = aiohttp.ClientTimeout(total=0.75)
    # from my timed tests, on my pc, avg time for GET req to run is <=.75 (750 milliseconds)
    async with session.get(url, timeout=time_in_millis) as response:
        return response.status


@async_timed()
async def main():
    session_timeout = aiohttp.ClientTimeout(total=1, connect=0.03)
    # from my timed tests, on my pc, avg time for client-session to connect is <=.03 (30 milliseconds)
    # while total client-session time is <1 (under 1 second)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        url = "https://www.example.com"
        status = await fetch_status(session, url)
        print(f"Status for {url} was {status}")


if __name__ == "__main__":
    asyncio.run(main())

# this would likely run into a TimeoutError, would have but I've set the timeout param
# to match the appropriate timeout on my pc
