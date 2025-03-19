# listing 2.13
# shielding a task from cancellation

import asyncio

from util import delay


async def main():
    task = asyncio.create_task(delay(10))

    try:
        result = await asyncio.wait_for(asyncio.shield(task), timeout=5)
        print(
            result
        )  # didn't print any result because the above line threw an exception
    except asyncio.TimeoutError:
        print("Task took longer than five seconds, it will finish soon!")
        result = await task
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
