"""Pytest tests for the mux controller library."""

import pytest
from mux_controller import MuxController, MuxConnectionError, MuxCommandError


# Default port - can be overridden with pytest --port flag or environment variable
DEFAULT_PORT = "/dev/cu.usbmodem101"


@pytest.fixture
def mux_port():
    """Fixture to get the serial port for testing."""
    import os
    return os.getenv("MUX_PORT", DEFAULT_PORT)


@pytest.fixture
def mux(mux_port):
    """Fixture that provides a connected MuxController instance."""
    mux_controller = MuxController(mux_port)
    yield mux_controller
    mux_controller.close()


def test_connection(mux_port):
    """Test that we can connect to the mux controller."""
    with MuxController(mux_port) as mux:
        assert mux._serial is not None
        assert mux._serial.is_open


def test_get_channel(mux):
    """Test getting the current channel."""
    channel = mux.get_channel()
    assert isinstance(channel, int)
    assert 0 <= channel <= 15


def test_set_channel_0(mux):
    """Test setting channel 0."""
    mux.set_channel(0)
    assert mux.get_channel() == 0


def test_set_channel_5(mux):
    """Test setting channel 5."""
    mux.set_channel(5)
    assert mux.get_channel() == 5


def test_set_channel_15(mux):
    """Test setting channel 15."""
    mux.set_channel(15)
    assert mux.get_channel() == 15


def test_set_invalid_channel(mux):
    """Test that setting an invalid channel raises ValueError."""
    with pytest.raises(ValueError, match="Channel must be between 0 and 15"):
        mux.set_channel(20)
    
    with pytest.raises(ValueError):
        mux.set_channel(-1)


def test_context_manager(mux_port):
    """Test that the context manager works correctly."""
    with MuxController(mux_port) as mux:
        assert mux._serial.is_open
        mux.set_channel(10)
    
    # Connection should be closed after exiting context
    assert mux._serial is None or not mux._serial.is_open


def test_multiple_channels(mux):
    """Test setting multiple channels in sequence."""
    channels = [0, 5, 10, 15, 3, 7, 12]
    for channel in channels:
        mux.set_channel(channel)
        assert mux.get_channel() == channel
