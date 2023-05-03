import pytest
from textual.widgets import Static

from skylab.models import Launch
from skylab.skylab import LaunchWidget

CORRECT_MOCK_LAUNCHES = {
    "results": {
        "name": "Mock Launch 1",
        "net": "2023-05-01T12:00:00Z",
        "pad": {"name": "Mock Pad 1", "address": "Mock Address 1"},
        "rocket": {"full_name": "Mock Manufacturer 1"},
        "mission": {"name": "Mock Mission 1", "description": "Mock Description 1"},
        "launch_service_provider": {"name": "Mock Provider 1"},
    }
}


class TestLaunchWidget:
    @pytest.fixture
    def launch(self):
        launch_json = CORRECT_MOCK_LAUNCHES["results"]
        launch = Launch(**launch_json)
        return LaunchWidget(launch=launch)

    def test_init(self, launch):
        assert isinstance(getattr(launch, "_launch_time"), Static)
