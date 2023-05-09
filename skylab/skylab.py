"""Skylab TUI."""

import random

from textual.app import App, ComposeResult
from textual.color import Color
from textual.containers import Container
from textual.widgets import Footer, Header, Static

from skylab import settings
from skylab.api import SpaceDevApi
from skylab.widgets.event_widget import EventWidget
from skylab.widgets.launch_widget import LaunchWidget


class SkylabApp(App):
    """Skylab TUI app."""

    TITLE = "Skylab"
    BINDINGS = [
        ("d", "exit", "Exit skylab."),
        ("?", "", "SpaceDev API is free but allows no more than 15 requests per hour"),
    ]
    CSS_PATH = settings.CSS_PATH

    def __init__(self, *args, **kwargs):
        """Initialize SkylabApp."""
        super().__init__(*args, **kwargs)
        api_client = SpaceDevApi()
        self._launch_widget_list = [
            LaunchWidget(launch=launch) for launch in api_client.launch_factory()
        ]
        self._event_widget_list = [
            EventWidget(event=event) for event in api_client.event_factory()
        ]
        self._launch_widgets = Container(*self._launch_widget_list)
        self._event_widgets = Container(*self._event_widget_list)

    def action_exit(self) -> None:
        """
        Bindings action method for app exit.
        As set in Bindings - pressing D would exit the app.
        """
        self.exit()

    def on_mount(self) -> None:
        """
        Event handler for when widget added to the app.
        Changes style of given LaunchWidgets such as background.
        """
        for launch_widget in self._launch_widget_list:
            launch_widget.styles.background = Color(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                0.45,
            )

    def compose(self) -> ComposeResult:
        """Creates a component of SkylabApp."""
        yield Header()
        yield Container(
            Static("Launches", classes="title"),
            Static("Events", classes="title"),
            id="title-grid",
        )
        yield Container(self._launch_widgets, self._event_widgets, id="window-split")
        yield Footer()
