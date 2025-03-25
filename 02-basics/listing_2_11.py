# listing 2.11
# manually cancelling a task

import asyncio

# from asyncio import CancelledError
from util import delay


async def main():
    long_task = asyncio.create_task(delay(10))
    short_task = asyncio.create_task(delay(6))
    seconds_elapsed = 0

    while not long_task.done():
        print("Task not finished, checking again in a second.")
        await asyncio.sleep(1)
        seconds_elapsed += 1
        if seconds_elapsed == 5:
            long_task.cancel()  # cancel long_task

    short_task = await short_task  # long_task is cancelled here
    print(short_task)
    print(long_task.cancelled())  # checking to see if long_task was cancelled

    try:
        # long_task throws a CancelledError here
        long_task = await long_task
        print(long_task)
    except asyncio.CancelledError:
        print(f"{long_task} task was cancelled!")


if __name__ == "__main__":
    asyncio.run(main())
