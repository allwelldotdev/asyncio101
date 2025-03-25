# listing 4.6
# Running 1000 requests concurently with asyncio.gather()


import asyncio

import aiohttp
from util import async_timed, fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ["https://example.com" for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


if __name__ == "__main__":
    asyncio.run(main())
