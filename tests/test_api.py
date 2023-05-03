import pytest
import requests

from skylab.api import get_upcoming_laucnhes, launch_factory
from skylab.models import Launch

MOCK_LAUNCHES = {
    "results": [
        {
            "name": "Mock Launch 1",
            "net": "2033-05-01T12:00:00Z",
            "pad": {"name": "Mock Pad 1", "location": {"name": "Mock Address 1"}},
            "rocket": {"configuration": {"full_name": "Mock Manufacturer 1"}},
            "mission": {"name": "Mock Mission 1", "description": "Mock Description 1"},
            "launch_service_provider": {"name": "Mock Provider 1"},
        },
        {
            "name": "Mock Launch 2",
            "net": "2033-05-02T12:00:00Z",
            "pad": {"name": "Mock Pad 2", "location": {"name": "Mock Address 2"}},
            "rocket": {"configuration": {"full_name": "Mock Manufacturer 2"}},
            "mission": {"name": "Mock Mission 2", "description": "Mock Description 2"},
            "launch_service_provider": {"name": "Mock Provider 2"},
        },
    ]
}


@pytest.fixture
def mock_get_upcoming_launches(monkeypatch):
    def mock_get(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: MOCK_LAUNCHES
        return response

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_upcoming_launches(mock_get_upcoming_launches):
    results = get_upcoming_laucnhes("https://mockurl.com")
    assert results == MOCK_LAUNCHES


def test_launch_factory(mock_get_upcoming_launches):
    launches = launch_factory()
    assert isinstance(launches, list)
    assert len(launches) == len(MOCK_LAUNCHES["results"])
    for launch in launches:
        assert isinstance(launch, Launch)
