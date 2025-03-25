from aiohttp import ClientSession


async def fetch_status(session: ClientSession, url: str) -> int:
    # access session using async with statement, returns result/response
    async with session.get(url) as response:
        return response.status
