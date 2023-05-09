"""Api module for receiving data from thespacedevs."""

import datetime

import requests

from skylab.models.event_models import Event
from skylab.models.launch_models import Launch


class SpaceDevApi:
    """Interface for interacting with SpaceDev API."""

    BASE_URL = "https://ll.thespacedevs.com/2.2.0"
    GET_UPCOMING_LAUNCHES = f"{BASE_URL}/launch/upcoming/"
    GET_UPCOMING_EVENTS = f"{BASE_URL}/event/upcoming/"

    def __init__(self, timeout: float = 5.0) -> None:
        """Initialize SpaceDevApi object."""
        self.timeout = timeout
        self.session = requests.Session()

    def get_request(self, url: str) -> dict:
        """Make a get request to the SpaceDev API."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as ex:
            raise ValueError(f"Failed to retrieve the info: {ex}.")

    def launch_factory(self) -> list[Launch]:
        """Makes a request for upcoming launches, modifies and validates them."""
        results = self.get_request(self.GET_UPCOMING_LAUNCHES)["results"]
        launches = []
        for launch_dict in results:
            # checking if the launch date is not expired
            net = datetime.datetime.fromisoformat(launch_dict["net"][:-1])
            if net < datetime.datetime.now():
                continue

            # removing "configuration" nested layer from given data
            rocket_config = launch_dict["rocket"].pop("configuration")
            launch_dict["rocket"].update(rocket_config)

            # getting address name from "location" json
            launch_pad_address = launch_dict["pad"].pop("location")["name"]
            launch_dict["pad"]["address"] = launch_pad_address
            launches.append(Launch(**launch_dict))
        return launches

    def event_factory(self) -> list[Event]:
        """Make a request for upcoming events, modifies and validates them."""
        results = self.get_request(self.GET_UPCOMING_EVENTS)["results"]
        events = []
        for event_dict in results:
            events.append(Event(**event_dict))
        return events
