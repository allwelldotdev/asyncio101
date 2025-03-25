import asyncio

from aiohttp import ClientSession

# could cause circular import issues, therefore, will decorate in the main script instead
# from .async_timer import async_timed


# @async_timed()
async def fetch_status(session: ClientSession, url: str, delay: int = 0) -> int:
    """async aiohttp client-session function. Takes session and url and returns GET request status code

    Parameters
    ----------
    session : ClientSession
        client-session from aiohttp.ClientSession context manager
    url : str
        URLs for HTTP GET request

    Returns
    -------
    int
        HTTP GET request status code
    """
    await asyncio.sleep(delay)
    # access session using async with statement, returns result/response
    async with session.get(url) as response:
        return response.status
