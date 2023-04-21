import requests
from pydantic import BaseModel


class Mission(BaseModel):
    name: str
    description: str


class Rocket(BaseModel):
    full_name: str


class Launch(BaseModel):
    name: str
    rocket: Rocket
    mission: Mission
    net: str


def get_laucnhes() -> list:
    response = requests.get("https://lldev.thespacedevs.com/2.2.0/launch/upcoming/")
    if response.status_code != 200:
        raise RuntimeError()
    return response.json()["results"]


def launch_factory() -> list[Launch]:
    results = get_laucnhes()
    launches = []
    for launch_dict in results:
        rocket_config = launch_dict["rocket"].pop("configuration")
        launch_dict["rocket"].update(rocket_config)
        launches.append(Launch(**launch_dict))

    return launches

if __name__ == "__main__":
    from pprint import pprint
    pprint(get_laucnhes())
