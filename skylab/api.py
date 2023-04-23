import requests
from pydantic import BaseModel

GET_UPCOMING_LAUNCHES = "https://lldev.thespacedevs.com/2.2.0/launch/upcoming/"


class LaunchProvier(BaseModel):
    name: str
    url: str


class Mission(BaseModel):
    name: str
    description: str


class Rocket(BaseModel):
    full_name: str
    ...


class Launch(BaseModel):
    name: str
    net: str
    rocket: Rocket
    mission: Mission
    launch_service_provider: LaunchProvier


def get_upcoming_laucnhes(url: str, timeout: float = 5.0) -> list:
    """Get request for upcoming launches."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()["results"]


def launch_factory() -> list[Launch]:
    """Makes a request for upcoming launches, modifies and validates them."""
    results = get_upcoming_laucnhes(GET_UPCOMING_LAUNCHES)
    launches = []
    for launch_dict in results:
        rocket_config = launch_dict["rocket"].pop("configuration")
        launch_dict["rocket"].update(rocket_config)
        launches.append(Launch(**launch_dict))
    return launches
