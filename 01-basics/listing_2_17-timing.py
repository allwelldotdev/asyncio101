# listing 2.17
# Timing two concurrent tasks with a decorator

import asyncio
import functools
import time
from typing import Any, Callable

from util import delay as _delay


# defining async decorator factory
def async_timed():
    """ASYNC Decorator Factory. Used to time async corounties and concurrent tasks."""

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f"starting {func} with args {args} {kwargs}")
            start = time.time()

            # func.time_start = round(start, 4)  # testing decorated closure access

            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()

                # func.time_end = round(end, 4)  # testing decorated closure access

                total = end - start
                print(f"finished {func} in {total:.4f} second(s)")

        return wrapped

    return wrapper


@async_timed()
async def main():
    delay = async_timed()(_delay)
    task_one = asyncio.create_task(delay(2))
    task_two = asyncio.create_task(delay(3))
    task_three = asyncio.create_task(delay(3))

    await task_one
    await task_two
    await task_three

    # figured out a new way to access decorated closure attributes
    # print(delay.__wrapped__.time_start, delay.__wrapped__.time_end, sep="\n")


if __name__ == "__main__":
    asyncio.run(main())
