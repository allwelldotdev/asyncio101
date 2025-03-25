# listing 4.10
# Examining the default behaviour or `asyncio.wait`


import asyncio

import aiohttp
from util import async_timed, fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, "https://www.example.com")),
            asyncio.create_task(fetch_status(session, "https://www.example.com")),
        ]
        done, pending = await asyncio.wait(fetchers)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            result = await done_task
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
