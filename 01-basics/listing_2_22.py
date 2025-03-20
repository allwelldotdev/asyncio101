# listing 2.22
# Accessing the event loop

import asyncio

from util import async_timed, delay


def call_later():
    print("I'm being called in the future!")


def call_later_math(num):
    print(sum([num**2 for _ in range(10)]))


@async_timed()
async def main():
    loop = asyncio.get_running_loop()
    # calls `call_later` in the next iteration after awaiting `delay(1)`
    loop.call_soon(call_later)
    loop.call_soon(call_later_math, 2)
    await delay(1)
    loop.call_soon(call_later_math, 10)
    # call_later_math(10)
    delay_3 = await delay(3)
    loop.call_soon(call_later_math, delay_3)


if __name__ == "__main__":
    asyncio.run(main())
