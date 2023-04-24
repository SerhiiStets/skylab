from skylab.models import Launch, LaunchPad, LaunchProvier, Mission, Rocket


def test_launch_default_values():
    """Testing default values of Launch model."""
    launch = Launch(name="Test Launch", net="2023-04-30")

    assert launch.mission == Mission(
        name="No name", description="No mission description yet."
    )
    assert launch.rocket == Rocket(full_name="Rocket name not yet provided.")
    assert launch.launch_service_provider == LaunchProvier(
        name="Service provider is not known."
    )
    assert launch.pad == LaunchPad(name="Unknown", address="Unknown")


def test_launch_custom_values():
    """Testing Launch model with mock values."""
    mission = Mission(name="Test Mission", description="Test Description")
    rocket = Rocket(full_name="Test Rocket")
    lsp = LaunchProvier(name="Test Provider")
    pad = LaunchPad(name="Test Pad", address="Test Address")

    launch = Launch(
        name="Test Launch",
        net="2023-04-30",
        mission=mission,
        rocket=rocket,
        launch_service_provider=lsp,
        pad=pad,
    )

    assert launch.mission == mission
    assert launch.rocket == rocket
    assert launch.launch_service_provider == lsp
    assert launch.pad == pad
