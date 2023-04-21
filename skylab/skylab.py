import os
import random
import urllib.parse
import webbrowser
from datetime import datetime, timedelta

import launch_api
from launch_api import Launch
from textual.app import App, ComposeResult
from textual.color import Color
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Label, Static

CURR_DIR = os.path.dirname(os.path.abspath(__file__))


class TimeDisplay(Static):
    time_to_launch = reactive(0.0)

    def __init__(self, *args, **kwargs) -> None:
        self.time = kwargs.pop("time_to_launch")
        self.launch_time = datetime.fromisoformat(self.time[:-1])
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        self.launch_time = self.launch_time - timedelta(seconds=1)
        self.time_to_launch = self.launch_time - datetime.now()
        self.set_interval(1, self.update_time)

    def update_time(self) -> None:
        self.launch_time = self.launch_time - timedelta(seconds=1)
        self.time_to_launch = self.launch_time - datetime.now()

    def watch_time_to_launch(self, time_to_launch: float) -> None:
        self.update(f"{time_to_launch}")


class LaunchWidget(Static):
    def __init__(self, *args, **kwargs) -> None:
        self.launch: Launch = kwargs.pop("launch")
        super().__init__(*args, **kwargs)
        self._net = datetime.fromisoformat(self.launch.net[:-1]).strftime("%h %d %Y")
        self._description = Static(f"{self.launch.mission.description}")
        self._rocket_name = Static(f"{self.launch.rocket.full_name}\n")
        self._launch_time = Static(f"{self._net}\n")
    

    def on_button_pressed(self) -> None:
        """Event handler called when a button is pressed."""
        query = f"{self.launch.name}" # replace with the search query you want
        base_url = "https://www.youtube.com"
        url = f"{base_url}/results?search_query={urllib.parse.quote(query)}"
        webbrowser.open(url, new=2)

    def compose(self) -> ComposeResult:
        yield Container(self._launch_time, self._rocket_name, self._description)

        yield Container(
            TimeDisplay(time_to_launch=self.launch.net, id="time-left"),
            Button("Watch", id="watch_button"),
        )


class LaunchWidgetBorder(Static):
    def compose(self) -> ComposeResult:
        yield Label("asd")

    def on_mount(self) -> None:
        label = self.query_one(Label)
        label.border_title = "Textual Rocks"


class SkyLabApp(App):
    TITLE = "skylab"
    BINDINGS = [("d", "exit", "Exit skylab.")]
    CSS_PATH = os.path.join(CURR_DIR, "css/styles.css")

    def compose(self) -> ComposeResult:
        """Create a child widgets for the app."""
        launches = launch_api.launch_factory()
        self.launch_widget_list = [LaunchWidget(launch=launch) for launch in launches]
        yield Header()
        yield Container(*self.launch_widget_list)
        yield Footer()

    def on_mount(self) -> None:
        for index, widget in enumerate(self.launch_widget_list, 1):
            alpha = 0.4
            colors = [
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ]
            widget.update(f"alpha={alpha:.1f}")
            widget.styles.background = Color(*colors, a=alpha)
            widget.styles.border = ("round", "white")
            widget.border_title = widget.launch.name
            widget.styles.border_title_align = "left"

    def action_exit(self) -> None:
        self.exit()
