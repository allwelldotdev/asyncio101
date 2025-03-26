# listing 4.15
# Using timeouts with `asyncio.wait`


import asyncio
import logging

import aiohttp
from util import async_timed, fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://example.com"
        fetchers = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url, delay=3)),
            asyncio.create_task(fetch_status(session, url)),
        ]
        done, pending = await asyncio.wait(fetchers, timeout=2)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            if done_task.exception() is None:
                print(await done_task)
            else:
                # pass
                logging.error(
                    "Request got an exception", exc_info=done_task.exception()
                )


if __name__ == "__main__":
    asyncio.run(main())

# NOTE: as before, our tasks in the pending set are not cancelled and will continue
# to run despite the timeout. If we have a use-case where we want to terminate the
# `pending` tasks, we'll need to explicitly loop through the `pending` set and call
# `cancel` on each task.
