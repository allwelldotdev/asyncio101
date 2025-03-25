# listing 4.11
# Exceptions with `asyncio.wait`


import asyncio
import logging

import aiohttp
from util import async_timed, fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        good_fetch = fetch_status(session, "https://www.example.com")
        bad_fetch = fetch_status(session, "python://bad")

        fetchers = [
            asyncio.create_task(good_fetch),
            asyncio.create_task(bad_fetch),
        ]
        done, pending = await asyncio.wait(fetchers)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            # result = await done_task # this will throw an exception

            # handling exceptions using `Task.exception()` and `Task.result()`
            if done_task.exception() is None:
                print(done_task.result())
            else:
                # pass
                logging.error(
                    "Request got an exception", exc_info=done_task.exception()
                )


if __name__ == "__main__":
    asyncio.run(main())
