# Copyright (c) 2020 Arda Seremet <ardaseremet@outlook.com>

import aiohttp
import async_timeout
from asyncio import TimeoutError

class API:
    """Class to interact with the API of ProgettiHWSW boards."""

    def __init__(self, ip: str):
        """Initialize the API."""
        self.ip = ip

    async def request(self, path: str):
        try:
            with async_timeout.timeout(5):
                async with aiohttp.request("GET", f"{self.ip}/{path}") as resp:
                    return await resp.text()
        except TimeoutError:
            return False
    
    async def execute(self, code: int):
        """Make requests with API codes for boards."""
        try:
            return await self.request(f"index.htm?execute={code}")
        except Exception:
            return False
