"""Event pydantic models."""

from typing import Union

from pydantic import BaseModel


class Event(BaseModel):
    """Event model from SpaceDev API."""

    name: str
    description: str = "No description yet."
    date: Union[str, None]
    news_url: Union[str, None]
    video_url: Union[str, None]
