# listing 4.7
# Handling exceptions with ``asyncio.gather()``

# when in asyncio.gather() - return_exceptions=False (default):
# if any coroutines throw exceptions, gather will also throw when we await it
# when in asyncio.gather() - return_exceptions=True:
# gather will not *throw* an exception, instead it'll return it (the exception)
# as part of the result list


import asyncio

import aiohttp
from util import async_timed
from util import fetch_status as _fetch_status

# decorate fetch_status with async_timer
fetch_status = async_timed()(_fetch_status)


async def exceptions_false():
    async with aiohttp.ClientSession() as session:
        urls = [
            "python://example.com",
            "https://example.com",
            "python://example.com",
            "https://example.com",
        ]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)
        # try:
        #     status_codes = await asyncio.gather(*requests)
        #     print(status_codes)
        # except AssertionError:
        #     pass


async def exceptions_true():
    async with aiohttp.ClientSession() as session:
        urls = ["python://example.com", "https://example.com", "python://example.com"]
        requests = [fetch_status(session, url) for url in urls]
        # I noticed that when return_exceptions=True it takes a little bit longer to run
        results = await asyncio.gather(*requests, return_exceptions=True)

        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [res for res in results if not isinstance(res, Exception)]

        print(f"All results: {results}")
        print(f"Finished successfully: {successful_results}")
        print(f"Threw exceptions: {exceptions}")


@async_timed()
async def main():
    # await exceptions_false()
    await exceptions_true()


if __name__ == "__main__":
    asyncio.run(main())
