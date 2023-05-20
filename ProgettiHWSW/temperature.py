# Copyright (c) 2020 Arda Seremet <ardaseremet@outlook.com>

from lxml import etree

from .api import API
from .const import STATUS_XML_PATH


class Temperature:
    """Class that represents a temperature sensor."""

    def __init__(self, api: API, temp_number: int):
        """Initialize Temperature class."""
        self.temp_number = int(temp_number)
        self.api = api
        self._state = None

    @property
    def id(self) -> int:
        """Return the input number."""
        return self.temp_number

    @property
    def state(self):
        """Return the temperature value."""
        return self._state

    async def update(self):
        """Update the input status."""
        request = await self.api.request(STATUS_XML_PATH)
        if request is False:
            return False

        root = etree.XML(bytes(request, encoding = 'utf-8'))

        path = root.xpath(f"//temp{str(self.temp_number)}")
        if not len(path) > 0:
            return False

        self._state = path[0].text
        return True
