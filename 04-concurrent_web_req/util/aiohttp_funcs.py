from aiohttp import ClientSession


async def fetch_status(session: ClientSession, url: str) -> int:
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
    # access session using async with statement, returns result/response
    async with session.get(url) as response:
        return response.status
