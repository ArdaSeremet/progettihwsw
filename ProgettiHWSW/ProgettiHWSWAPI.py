# Copyright (c) 2020 Arda Seremet <ardaseremet@outlook.com>

from lxml import etree
import base64

from .api import API
from .input import Input
from .relay import Relay
from .analog import AnalogInput
from .temperature import Temperature

from .const import STATUS_XML_PATH

import random


class ProgettiHWSWAPI:
    """Class to communicate with ProgettiHWSW boards."""

    def __init__(self, ip: str):
        """Initialize the API and return the corresponding object class."""
        self.api = API(f"http://{ip}")
        self.ip = ip
        self.board_data = None

    def create_unique_id(self, number, io_type: str):
        """Generate an id based on IP address and a number."""
        unencoded_ascii = (
            f"{self.ip}_{io_type}_{number}_{random.random()}").encode('ascii')
        base64_bytes = base64.b64encode(unencoded_ascii)

        return base64_bytes.decode('ascii')

    async def check_board(self):
        """Check if this board is existing and valid."""
        request = await self.api.request(STATUS_XML_PATH)
        if request is False:
            return False

        root = etree.XML(bytes(request, encoding='utf-8'))

        relay_tags = root.xpath("//*[starts-with(local-name(), 'led')]")
        input_tags = root.xpath("//*[starts-with(local-name(), 'btn')]")
        analog_tags = root.xpath("//*[starts-with(local-name(), 'pot')]")
        temp_tags = root.xpath("//*[starts-with(local-name(), 'temp')]")
        rfid_tags = root.xpath("//*[starts-with(local-name(), 'rfid')]")

        if (len(relay_tags) + len(input_tags) + len(analog_tags) + len(temp_tags) + len(rfid_tags)) <= 0:
            return False

        self.board_data = {
            "title": f"{len(relay_tags)}R Board",
            "relays": [i.tag[3:] for i in relay_tags],
            "inputs": [i.tag[3:] for i in input_tags],
            "analogs": [i.tag[3:] for i in analog_tags],
            "temps": [i.tag[4:] for i in temp_tags],
            "rfid": True if (len(rfid_tags) > 0) else False,
        }

        return self.board_data

    async def get_states_by_tag_prefix(self, tag: str, is_analog: bool = False):
        """Return all states with the XML tag prefix."""
        request = await self.api.request(STATUS_XML_PATH)
        if request is False:
            return False

        root = etree.XML(bytes(request, encoding='utf-8'))
        tags = root.xpath(f"//*[starts-with(local-name(), '{tag}')]")

        if len(tags) <= 0:
            return False

        states = {}
        for i in tags:
            number = str(i.tag[len(tag):], 16)
            if is_analog:
                states[number] = i.text
            else:
                states[number] = (
                    True if i.text in ("up", "1", "on") else False
                )

        return states

    async def get_rfid(self):
        """Return the RFID number of lastly read tag."""
        request = await self.api.request(STATUS_XML_PATH)
        if request is False:
            return False

        root = etree.XML(bytes(request, encoding='utf-8'))
        tags = root.xpath(f"//*[starts-with(local-name(), 'rfid')]")

        if len(tags) <= 0:
            return False

        rfid_number = tags[0].text

        return rfid_number

    async def get_switches(self):
        """Return all switch states."""
        return await self.get_states_by_tag_prefix("led")

    async def get_inputs(self):
        """Return all input states."""
        return await self.get_states_by_tag_prefix("btn")

    async def get_pots(self):
        """Return all analog input states."""
        return await self.get_states_by_tag_prefix("pot", True)

    async def get_temps(self):
        """Return all temperature states."""
        return await self.get_states_by_tag_prefix("temp", True)

    def get_relay(self, relay_number: int, relay_mode: str = "bistable") -> Relay:
        """Return the Relay class."""
        return Relay(self.api, relay_number, relay_mode)

    def get_input(self, input_number: int) -> Input:
        """Return the Input class."""
        return Input(self.api, input_number)

    def get_pot(self, pot_number: int) -> AnalogInput:
        """Return the AnalogInput class."""
        return AnalogInput(self.api, pot_number)

    def get_temp(self, temp_number: int) -> Temperature:
        """Return the Temperature class."""
        return Temperature(self.api, temp_number)
