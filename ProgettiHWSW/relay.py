# Copyright (c) 2020 Arda Seremet <ardaseremet@outlook.com>

from lxml import etree

from .api import API
from .const import (
    STATUS_XML_PATH,
    TEMP_MONOSTABLE_BASE,
    TOGGLE_BASE,
    TURN_OFF_BASE,
    TURN_ON_BASE,
)


class Relay:
    """Class that represents a relay object."""

    def __init__(self, api: API, relay_number: int, relay_mode: str):
        """Initialize Relay class."""
        self.relay_number = int(relay_number)
        self.relay_mode = relay_mode
        self.api = api
        self.state = None

    @property
    def id(self) -> int:
        """Return the relay number."""
        return self.relay_number

    @property
    def is_on(self) -> bool:
        """Return if the relay is on."""
        return self.state

    async def toggle(self):
        """Toggle the relay."""
        command = TOGGLE_BASE + self.relay_number
        await self.api.execute(command)

    async def control(self, state: bool):
        """Control the relay state."""
        command = (
            (TURN_ON_BASE if self.relay_mode ==
             "bistable" else TEMP_MONOSTABLE_BASE)
            if state is True
            else TURN_OFF_BASE
        ) + self.relay_number
        await self.api.execute(command)

    async def update(self):
        """Update the relay status."""
        request = await self.api.request(STATUS_XML_PATH)
        if request is False:
            return False

        root = etree.XML(bytes(request, encoding='utf-8'))

        path = root.xpath(f"//led{str(self.relay_number)}")
        if not len(path) > 0:
            return False

        self.state = True if path[0].text in ("up", "1", "on") else False
        return True
