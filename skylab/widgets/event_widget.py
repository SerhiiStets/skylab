"""Event widget of Skylab app."""

import datetime
import webbrowser

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Static

from skylab.models.event_models import Event


class EventWidget(Static):
    """Event object Static."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize Event widget."""
        self.event: Event = kwargs.pop("event")
        super().__init__(*args, **kwargs)
        self._explore_disabled = False if self.event.news_url else True
        self._watch_disabled = False if self.event.video_url else True
        if self.event.date:
            self._date = str(datetime.datetime.fromisoformat(self.event.date[:-1]))
        else:
            self._date = "No date given yet."

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Event handler called when a button is pressed.
        On press opens news or video url of the event.
        """
        if event.button.id == "explore-btn" and self.event.news_url:
            webbrowser.open(self.event.news_url, new=2)
        elif event.button.id == "watch-btn" and self.event.video_url:
            webbrowser.open(self.event.video_url, new=2)

    def on_mount(self) -> None:
        """Event handler for when EventWidget is being mounted."""
        # Set a delimeter as a gray border at the bottom of each widget.
        self.styles.border_bottom = ("hkey", "gray")

    def compose(self) -> ComposeResult:
        """Creates a child widget of EventWidget."""
        yield Static(f"{self.event.name}\n")
        yield Static(f"{self._date}\n")
        yield Static(f"{self.event.description}\n", classes="bg-text")
        yield Horizontal(
            Button(
                "Explore",
                id="explore-btn",
                variant="primary",
                disabled=self._explore_disabled,
            ),
            Button(
                "Watch", id="watch-btn", variant="error", disabled=self._watch_disabled
            ),
            classes="event-buttons",
        )
