# Copyright (c) 2020 Arda Seremet <ardaseremet@outlook.com>

from lxml import etree

from .api import API
from .const import STATUS_XML_PATH


class AnalogInput:
    """Class that represents an analog input object."""

    def __init__(self, api: API, pot_number: int):
        """Initialize AnalogInput class."""
        self.pot_number = int(pot_number)
        self.api = api
        self._state = None

    @property
    def id(self) -> int:
        """Return the analog number."""
        return self.pot_number

    @property
    def state(self):
        """Return the analog input value."""
        return self._state

    async def update(self):
        """Update the input status."""
        request = await self.api.request(STATUS_XML_PATH)
        if request is False:
            return False

        root = etree.XML(bytes(request, encoding='utf-8'))

        path = root.xpath(f"//pot{str(self.pot_number)}")
        if not len(path) > 0:
            return False

        self._state = path[0].text
        return True
