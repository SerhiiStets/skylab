"""Skylab TUI."""

import datetime
import os
import random
import urllib.parse
import webbrowser

import tzlocal
from textual.app import App, ComposeResult
from textual.color import Color
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static

import skylab.api
from skylab.api import Launch

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_TIMEZONE = tzlocal.get_localzone()


class TimeDisplay(Static):
    """Time till launch Static."""

    time_to_launch: reactive[datetime.timedelta] = reactive(datetime.timedelta(0))

    def __init__(self, *args, **kwargs) -> None:
        """Initialize TimeDisplay."""
        # Remove passed time_to_launch var before calling super()
        self._launch_time = kwargs.pop("launch_time")
        offset = self._launch_time.astimezone(LOCAL_TIMEZONE).utcoffset()
        self._offset = offset if offset else datetime.timedelta(0)
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        """On widget mount sets interval to call update_tim every second."""
        self.time_to_launch = self._launch_time - datetime.datetime.now() + self._offset
        self.set_interval(1, self.update_time)

    def update_time(self) -> None:
        """Updates time_to_launch value."""
        self.time_to_launch = self._launch_time - datetime.datetime.now() + self._offset

    def watch_time_to_launch(self, time_to_launch: datetime.timedelta) -> None:
        """
        Updates screen value of time_to_launch every time the value changes
        and removes milliseconds from time_to_launch value to display.
        """
        formated_time = datetime.timedelta(
            days=time_to_launch.days, seconds=time_to_launch.seconds
        )
        self.update(f"{formated_time}")


class LaunchWidget(Static):
    """Launch object Static."""

    youtube_url = "https://www.youtube.com"

    def __init__(self, *args, **kwargs) -> None:
        """Initialize LaunchWidget."""
        # remove launch object from kwargs before doing super()
        self.launch: Launch = kwargs.pop("launch")
        super().__init__(*args, **kwargs)
        self._net = datetime.datetime.fromisoformat(self.launch.net[:-1])
        self._description = Static(f"{self.launch.mission.description}")
        self._rocket_name = Static(f"Rocket: {self.launch.rocket.full_name}\n")
        self._launch_time = Static(f"{LOCAL_TIMEZONE.localize(self._net)}\n")

    def on_button_pressed(self) -> None:
        """
        Event handler called when a button is pressed.
        On press creates a youtube search query for upcoming launch.
        """
        query = f"{self.launch.name} {self._net}"
        launch_url = (
            f"{self.youtube_url}/results?search_query={urllib.parse.quote(query)}"
        )
        webbrowser.open(launch_url, new=2)

    def compose(self) -> ComposeResult:
        """Creates a child widget of LaunchWidget."""
        yield Container(self._launch_time, self._rocket_name, self._description)
        yield Container(
            TimeDisplay(launch_time=self._net, id="time-left"),
            Button("Watch", id="watch_button"),
        )


class SkylabApp(App):
    """Skylab TUI app."""

    TITLE = "skylab"
    BINDINGS = [("d", "exit", "Exit skylab.")]
    CSS_PATH = os.path.join(CURR_DIR, "css/styles.css")

    def __init__(self, *args, **kwargs):
        """Initialize SkylabApp."""
        super().__init__(*args, **kwargs)
        self.launch_widget_list = [
            LaunchWidget(launch=launch) for launch in skylab.api.launch_factory()
        ]

    def on_mount(self) -> None:
        """
        Event handler for when widget added to the app.
        Changes style of given LaunchWidgets such as border,
        background-color, border_title, etc.
        """
        for launch_widget in self.launch_widget_list:
            colors = [
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ]
            launch_widget.styles.background = Color(*colors, a=0.45)
            launch_widget.styles.border = ("round", "white")
            launch_widget.border_title = launch_widget.launch.name
            launch_widget.styles.border_title_align = "left"

    def action_exit(self) -> None:
        """Bindings action method for app exit."""
        self.exit()

    def compose(self) -> ComposeResult:
        """Creates a component of SkylabApp."""
        yield Header()
        yield Container(*self.launch_widget_list)
        yield Footer()
