# listing 4.14
# Processing all results as they come in


import asyncio
import logging

import aiohttp
from util import async_timed, fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://example.com"
        pending = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url, delay=2)),
            asyncio.create_task(fetch_status(session, url)),
        ]

        # loop through all pending tasks and run until complete
        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )
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
