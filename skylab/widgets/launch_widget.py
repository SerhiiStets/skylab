"""Launch widget of Skylab app."""

import datetime
import urllib.parse
import webbrowser

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Button, Static

from skylab import settings
from skylab.models.launch_models import Launch
from skylab.widgets.time_widget import TimeDisplay


class LaunchWidget(Static):
    """Launch object Static."""

    YOUTUBE_URL = "https://www.youtube.com"

    def __init__(self, *args, **kwargs) -> None:
        """Initialize LaunchWidget."""
        # remove launch object from kwargs before doing super()
        self.launch: Launch = kwargs.pop("launch")
        super().__init__(*args, **kwargs)
        self._net = datetime.datetime.fromisoformat(self.launch.net[:-1])
        self._launch_time = Static(
            f"{settings.LOCAL_TIMEZONE.localize(self._net)}\n", classes="bg-text"
        )
        self._launch_provider = Static(f"{self.launch.launch_service_provider.name}\n")
        self._rocket_name = Static(f"{self.launch.rocket.full_name}\n")
        self._launch_pad = Static(
            f"{self.launch.pad.name}, {self.launch.pad.address}\n", classes="bg-text"
        )
        self._description = Static(
            f"{self.launch.mission.description}", classes="bg-text"
        )

    def on_mount(self) -> None:
        """Set height of the widget depending on description lenght on mount."""
        descr_len = len(self.launch.mission.description)
        if descr_len < 70:
            self.styles.height = 13
        elif descr_len < 160:
            self.styles.height = 14
        elif descr_len < 300:
            self.styles.height = 16
        else:
            self.styles.height = 19

    def on_button_pressed(self) -> None:
        """
        Event handler called when a button is pressed.
        On press creates a youtube search query for upcoming launch.
        """
        query = f"{self.launch.name} {self._net}"
        launch_url = (
            f"{self.YOUTUBE_URL}/results?search_query={urllib.parse.quote(query)}"
        )
        webbrowser.open(launch_url, new=2)

    def compose(self) -> ComposeResult:
        """Creates a child widget of LaunchWidget."""
        yield Container(
            self._launch_provider,
            self._rocket_name,
            self._launch_time,
            self._launch_pad,
            self._description,
        )
        yield Vertical(
            TimeDisplay(launch_time=self._net, id="launch-counter", classes="bg-text"),
            Button("Watch", id="watch-button"),
            id="right-launch-widget",
        )
