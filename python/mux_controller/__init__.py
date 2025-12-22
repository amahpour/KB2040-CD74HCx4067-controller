"""CD74HC4067 Multiplexer Controller for KB2040.

A Python library to control the CD74HC4067 16-channel multiplexer
via serial communication with the KB2040 microcontroller.
"""

from mux_controller.controller import (
    MuxController,
    MuxConnectionError,
    MuxCommandError,
)

__all__ = [
    "MuxController",
    "MuxConnectionError",
    "MuxCommandError",
]

__version__ = "0.1.0"

