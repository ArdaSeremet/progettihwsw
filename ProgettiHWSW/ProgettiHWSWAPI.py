# Copyright (c) 2020 Arda Seremet <ardaseremet@outlook.com>

from lxml import etree

from ProgettiHWSW.api import API
from ProgettiHWSW.input import Input
from ProgettiHWSW.relay import Relay

from .const import STATUS_XML_PATH


class ProgettiHWSWAPI:
    """Class to communicate with ProgettiHWSW boards."""

    def __init__(self, ip: str, is_old_board: bool = False):
        """Initialize the API and return the corresponding object class."""
        self.api = API(f"http://{ip}")
        self.ip = ip
        self.is_old_board = is_old_board

    async def check_board(self):
        """Check if this board is existing."""
        request = await self.api.request(STATUS_XML_PATH)
        if request is False:
            return False

        root = etree.XML(request)

        is_old_board = len(root.xpath("//led0")) > 0
        relay_tags = root.xpath("//*[starts-with(local-name(), 'led')]")
        input_tags = root.xpath("//*[starts-with(local-name(), 'btn')]")
        self.is_old_board = is_old_board

        if len(relay_tags) <= 0 and len(input_tags) <= 0:
            return False

        return {
            "title": f"{len(relay_tags)}R & {len(input_tags)}IN Board",
            "is_old": is_old_board,
            "relay_count": len(relay_tags),
            "input_count": len(input_tags),
        }

    async def get_switches(self):
        """Return all switch states."""
        request = await self.api.request(STATUS_XML_PATH)
        if request is False:
            return False

        root = etree.XML(request)
        relay_tags = root.xpath("//*[starts-with(local-name(), 'led')]")
        if len(relay_tags) <= 0:
            return False
        is_old_board = len(root.xpath("//led0")) > 0
        self.is_old_board = is_old_board

        states = {}
        for i in relay_tags:
            number = int(i.tag.split("led")[1])
            states[number if is_old_board is False else number + 1] = (
                True if i.text == "1" else False
            )
        return states

    async def get_inputs(self):
        """Return all switch states."""
        request = await self.api.request(STATUS_XML_PATH)
        if request is False:
            return False

        root = etree.XML(request)
        relay_tags = root.xpath("//*[starts-with(local-name(), 'btn')]")
        if len(relay_tags) <= 0:
            return False
        is_old_board = len(root.xpath("//btn0")) > 0
        self.is_old_board = is_old_board

        states = {}
        for i in relay_tags:
            number = int(i.tag.split("btn")[1])
            states[number if is_old_board is False else number + 1] = (
                True if i.text == "up" else False
            )
        return states

    def get_relay(self, relay_number: int, relay_mode: str = "bistable") -> Relay:
        """Return the Relay class."""
        return Relay(self.api, relay_number, relay_mode, self.is_old_board)

    def get_input(self, input_number: int) -> Input:
        """Return the Input class."""
        return Input(self.api, input_number, self.is_old_board)
