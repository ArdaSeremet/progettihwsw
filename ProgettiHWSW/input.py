# Copyright (c) 2020 Arda Seremet <ardaseremet@outlook.com>

from lxml import etree

from ProgettiHWSW.api import API
from ProgettiHWSW.const import STATUS_XML_PATH


class Input:
    """Class that represents an input object."""

    def __init__(self, api: API, input_number: int, is_old: bool):
        """Initialize Input class."""
        self.input_number = int(input_number)
        self.api = api
        self.state = None
        self.is_old = is_old

    @property
    def id(self) -> int:
        """Return the input number."""
        return self.input_number

    @property
    def is_on(self) -> bool:
        """Return if the input is on."""
        return self.state

    async def update(self):
        """Update the input status."""
        request = await self.api.request(STATUS_XML_PATH)
        if request is False:
            return False

        root = etree.XML(request)
        number = self.input_number - 1 if self.is_old is True else self.input_number
        if not number >= 0:
            return False

        path = root.xpath(f"//btn{str(number)}")
        if not len(path) > 0:
            return False

        self.state = True if path[0].text == "up" else False
        return True
