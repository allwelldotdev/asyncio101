# listing 2.23
# Running CPU-bound code in debug mode

import asyncio

from util import async_timed


@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for i in range(100_000_000):
        counter = counter + 2
    # expression below does the same thing as the `for` loop but is less efficient on cpu
    # counter = [counter := counter + 2 for i in range(100_000_000)][-1]
    return counter


async def main() -> None:
    # start comment 101:
    loop = asyncio.get_running_loop()
    loop.slow_callback_duration = (
        0.250  # changes slow callback duration of event loop to 250ms (milliseconds)
    )

    task_one = asyncio.create_task(cpu_bound_work())
    await task_one


if __name__ == "__main__":
    asyncio.run(main(), debug=True)  # enabling debug mode for asyncio
    # tells when some coroutines, normal functions, or cpu-bound code is taking time
    # time is 100ms by default - this time is called slow callback duration
    # it can be changed like so: see `comment 101`
    # notice after changing the slow callback duration to 250ms from 100ms the
    # debug warning still fires because the cpu_bound code takes ~4 seconds
    # 4s > .250ms
