# listing 2.10
# running code while other operations complete

import asyncio

from util import delay  # imports delay function from our util module


async def hello_every_second():
    """async corountine sleeps twice in concurrency while other async corourines run."""
    for _ in range(2):
        await asyncio.sleep(1)
        print("I'm running other code while I'm waiting!")


async def main():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))

    # print out task objects created by asyncio.create_task function
    print(first_delay, second_delay, sep="\n")

    # await async def main corountine, allowing other corountines run in the process
    await hello_every_second()
    await first_delay
    await second_delay


if __name__ == "__main__":
    asyncio.run(main())
