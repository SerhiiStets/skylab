"""Launch pydantic models."""

from typing import Union

from pydantic import BaseModel, Field, validator


class LaunchProvier(BaseModel):
    name: str


class Mission(BaseModel):
    name: str
    description: str


class Rocket(BaseModel):
    full_name: str


class LaunchPad(BaseModel):
    name: str
    address: str


class Launch(BaseModel):
    name: str
    net: str
    pad: LaunchPad = Field(LaunchPad(name="Unknown", address="Unknown"))
    rocket: Rocket = Field(Rocket(full_name="Rocket name not yet provided."))
    mission: Mission = Field(
        Mission(name="No name", description="No mission description yet.")
    )
    launch_service_provider: LaunchProvier = Field(
        LaunchProvier(name="Service provider is not known.")
    )

    @validator("mission", pre=True)
    def set_mission_default(cls, v: Union[Mission, None]) -> Mission:
        return (
            v
            if v
            else Mission(name="No name", description="No mission description yet.")
        )

    @validator("rocket", pre=True)
    def set_rocket_default(cls, v: Union[Rocket, None]) -> Rocket:
        return v if v else Rocket(full_name="Rocket name not yet provided.")

    @validator("launch_service_provider", pre=True)
    def set_launch_service_provider_default(
        cls, v: Union[LaunchProvier, None]
    ) -> LaunchProvier:
        return v if v else LaunchProvier(name="Service provider is not known.")

    @validator("pad", pre=True)
    def set_pad_default(cls, v: Union[LaunchPad, None]) -> LaunchPad:
        return v if v else LaunchPad(name="Unknown.", address="Unknown.")
