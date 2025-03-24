# listing 3.9
# Adding a signal handler to cancel tasks

import asyncio
import signal
from asyncio import AbstractEventLoop
from typing import Set

from util import delay


def cancel_tasks():
    print("Got a SIGINT!")
    # asyncio.all_tasks() outputs all running tasks
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    print(f"Cancelling {len(tasks)} task(s).")
    [task.cancel() for task in tasks]


async def main():
    loop: AbstractEventLoop = asyncio.get_running_loop()
    # when SIGINT (Ctrl+C) is called, run cancel_tasks()
    loop.add_signal_handler(signal.SIGINT, cancel_tasks)
    await delay(10)  # give some time for tasks to finish


if __name__ == "__main__":
    asyncio.run(main())
