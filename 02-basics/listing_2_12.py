# listing 2.12
# cancelling a task by creating a timeout for a task with `wait_for`

import asyncio

from util import delay


async def main():
    delay_task = asyncio.create_task(delay(2))

    try:
        # cancel delay_task with timeout of 1 second
        result = await asyncio.wait_for(delay_task, timeout=1)
        # this doesn't print because .wait_for throws an exception
        print(result)
    except asyncio.TimeoutError:
        print("Got a timeout!")
        print(f"Was the task cancelled? {delay_task.cancelled()}")


if __name__ == "__main__":
    asyncio.run(main())
