"""Time till lauch countdown widget."""

import datetime

from textual.reactive import reactive
from textual.widgets import Static

from skylab import settings


class TimeDisplay(Static):
    """Time till launch Static."""

    time_to_launch: reactive[datetime.timedelta] = reactive(datetime.timedelta(0))

    def __init__(self, *args, **kwargs) -> None:
        """Initialize TimeDisplay."""
        # Remove passed time_to_launch var before calling super()
        self._launch_time = kwargs.pop("launch_time")
        offset = self._launch_time.astimezone(settings.LOCAL_TIMEZONE).utcoffset()
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
