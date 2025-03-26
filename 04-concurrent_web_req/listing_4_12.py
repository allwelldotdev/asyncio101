# listing 4.12
# Cancelling running requests on an exception


import asyncio
import logging

import aiohttp
from util import async_timed, fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, "python://bad")),
            asyncio.create_task(fetch_status(session, "https://example.com", 3)),
            asyncio.create_task(fetch_status(session, "https://example.com", 3)),
        ]
        done, pending = await asyncio.wait(
            fetchers, return_when=asyncio.FIRST_EXCEPTION
        )

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                # pass
                logging.error(
                    "Request got an exception", exc_info=done_task.exception()
                )

        # here we can handle the pending tasks, like cancel them from running in background
        for pending_task in pending:
            pending_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())

# NOTE: our application took almost no time to run, as we quickly reacted to the fact that
# one of our requests threw an exception; the power of using this option is we achieve
# fail-fast behaviour, quickly reacting to any issues that arise.
