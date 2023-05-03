"""Api module for receiving data from thespacedevs."""
import datetime

import requests

from skylab.models import Launch

GET_UPCOMING_LAUNCHES = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"


def get_upcoming_laucnhes(url: str, timeout: float = 5.0) -> dict:
    """Get request for upcoming launches."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as ex:
        raise ValueError(f"Failed to retrieve upcoming launches: {ex}.")


def launch_factory() -> list[Launch]:
    """Makes a request for upcoming launches, modifies and validates them."""
    results = get_upcoming_laucnhes(GET_UPCOMING_LAUNCHES)["results"]
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
