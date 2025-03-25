# listing 4.5
# Using tasks concurrently with a list comprehension
# the right way and the wrong way


import asyncio

from util import async_timed, delay


@async_timed()
async def wrong_way():
    """This will take a total of 3 x 3 x 3 seconds = 9 seconds to run"""
    delay_times = [3, 3, 3]
    [await asyncio.create_task(delay(seconds)) for seconds in delay_times]


@async_timed()
async def right_way():
    """This will take a total of 3 seconds to run"""
    delay_times = [3, 3, 3]
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    [await task for task in tasks]


async def main():
    await wrong_way()
    await right_way()


if __name__ == "__main__":
    asyncio.run(main())

# there is a better way of running multiple awaitables (coroutines or tasks) together.
# asyncio APIs provided a lot of methods that do this and more
# one of them is asyncio.gather()
