import functools
import time
from typing import Any, Callable


def async_timed():
    """ASYNC Decorator Factory. Used to time async corounties and concurrent tasks."""

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f"starting {func} with args {args} {kwargs}")
            start = time.time()

            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f"finished {func} in {total:.4f} second(s)")

        return wrapped

    return wrapper
