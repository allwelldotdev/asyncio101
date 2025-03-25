# listing 2.21
# Manually creating the event loop

import asyncio

from util import delay


async def main():
    print("Starting tasks")
    task_one = asyncio.create_task(delay(1))
    asyncio.create_task(delay(3))
    print(await task_one)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        # asyncio.run(main())

        loop.run_until_complete(main())
    finally:
        loop.close()
        print("Ending tasks")

# this code is similar to what asyncio.run() does, the only difference being that it
# does not perform cancelling any remaining tasks. If we want any special cleanup logic,
# we would have to do so in our `finally` clause.
