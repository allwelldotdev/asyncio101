# listing 4.9
# Setting a timeout on `asyncio.as_completed`


import asyncio

import aiohttp
from util import async_timed, fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, "https://www.example.com", 1),
            fetch_status(session, "https://www.example.com", 10),
            fetch_status(session, "https://www.example.com", 10),
        ]

        for done_task in asyncio.as_completed(fetchers, timeout=3):
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print("We got a timeout error!")

        for task in asyncio.tasks.all_tasks():
            print(task)


if __name__ == "__main__":
    asyncio.run(main())

# `as_completed` works well for getting results as fast as possible but has drawbacks.
# The first is that the order of the results is non-deterministic. If we don't care about
# order this may be fine but if we need to associate the results to the requests somehow
# we're left with a challenge.
# The second is that with timeouts, while we will correctly throw an exception and move on,
# any tasks created will still be running in the background.
# To solve this asyncio provides another API method called `wait`
