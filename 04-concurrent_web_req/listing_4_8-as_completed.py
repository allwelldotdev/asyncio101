# listing 4.8
# Using asyncio.as_completed()


import asyncio

import aiohttp
from util import async_timed
from util import fetch_status as _fetch_status

fetch_status = async_timed()(_fetch_status)  # decorated func


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, "https://www.example.com", 1),
            fetch_status(session, "https://www.example.com", 1),
            fetch_status(session, "https://www.example.com", 10),
        ]

        print("using as_completed")
        as_completed_results = []
        # using as_completed - results of Futures are returned through an iterator
        # as soon as they're ready
        # print(asyncio.as_completed(fetchers)) # a generator object (an iterator of futures)
        for finished_task in asyncio.as_completed(fetchers):
            returned_future = await finished_task
            as_completed_results.append(returned_future)
            print(returned_future)
        print(as_completed_results)

        # print("using gather")
        # # using gather - results are witheld until all Futures are returned
        # gather_results = await asyncio.gather(*fetchers)
        # print(gather_results)


if __name__ == "__main__":
    asyncio.run(main())
