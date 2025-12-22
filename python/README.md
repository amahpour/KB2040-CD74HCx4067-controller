# CD74HC4067 Mux Controller

Python library to control the CD74HC4067 16-channel multiplexer via serial communication with the KB2040 microcontroller.

## Installation

### Install from GitHub (Recommended)

```bash
pip install git+https://github.com/amahpour/KB2040-CD74HCx4067-controller.git#subdirectory=python
```

Or with Poetry:

```bash
poetry add git+https://github.com/amahpour/KB2040-CD74HCx4067-controller.git#subdirectory=python
```

### From source

```bash
git clone https://github.com/amahpour/KB2040-CD74HCx4067-controller.git
cd KB2040-CD74HCx4067-controller/python
poetry install
```

### Using pip (if published to PyPI)

```bash
pip install cd74hc4067-mux-controller
```

### Using Poetry (if published to PyPI)

```bash
poetry add cd74hc4067-mux-controller
```

## Quick Start

```python
from mux_controller import MuxController

# Connect to the mux controller
mux = MuxController("/dev/cu.usbmodem101")

# Select channel 5
mux.set_channel(5)

# Query current channel
channel = mux.get_channel()
print(f"Current channel: {channel}")

# Close the connection
mux.close()
```

## Usage

### Basic Usage

```python
from mux_controller import MuxController

# Initialize the controller
mux = MuxController(
    port="/dev/cu.usbmodem101",  # Serial port path
    baudrate=115200,              # Default: 115200
    timeout=2.0                   # Default: 2.0 seconds
)

# Set a channel (0-15)
mux.set_channel(10)

# Get the current channel
current = mux.get_channel()
print(f"Channel {current} is active")

# Close when done
mux.close()
```

### Context Manager

The `MuxController` supports Python's context manager protocol for automatic cleanup:

```python
from mux_controller import MuxController

with MuxController("/dev/cu.usbmodem101") as mux:
    mux.set_channel(5)
    # Connection is automatically closed when exiting the context
```

### Error Handling

The library provides custom exceptions for better error handling:

```python
from mux_controller import MuxController, MuxConnectionError, MuxCommandError

try:
    mux = MuxController("/dev/cu.usbmodem101")
    mux.set_channel(20)  # Invalid channel
except ValueError as e:
    print(f"Invalid channel: {e}")
except MuxCommandError as e:
    print(f"Command failed: {e}")
except MuxConnectionError as e:
    print(f"Connection error: {e}")
finally:
    mux.close()
```

## API Reference

### MuxController

#### `__init__(port, baudrate=115200, timeout=2.0)`

Initialize the mux controller.

**Parameters:**
- `port` (str): Serial port path (e.g., "/dev/cu.usbmodem101" or "COM3")
- `baudrate` (int): Serial baud rate (default: 115200)
- `timeout` (float): Serial read timeout in seconds (default: 2.0)

**Raises:**
- `MuxConnectionError`: If the serial connection cannot be established

#### `set_channel(channel) -> bool`

Select a channel on the multiplexer.

**Parameters:**
- `channel` (int): Channel number (0-15)

**Returns:**
- `bool`: True if the channel was set successfully

**Raises:**
- `ValueError`: If channel is out of range (0-15)
- `MuxCommandError`: If the command fails or returns an error
- `MuxConnectionError`: If the serial connection is lost

#### `get_channel() -> int`

Get the currently selected channel.

**Returns:**
- `int`: Current channel number (0-15)

**Raises:**
- `MuxCommandError`: If the command fails or returns an invalid response
- `MuxConnectionError`: If the serial connection is lost

#### `close()`

Close the serial connection.

### Exceptions

#### `MuxConnectionError`

Raised when there's an issue with the serial connection (port not found, connection lost, etc.).

#### `MuxCommandError`

Raised when a command fails or returns an invalid response from the controller.

## Finding Your Serial Port

### macOS/Linux

```bash
# List serial ports
ls /dev/cu.*  # macOS
ls /dev/tty*  # Linux

# Or use Python
python -m serial.tools.list_ports
```

### Windows

```powershell
# Check Device Manager > Ports (COM & LPT)
# Or use Python
python -m serial.tools.list_ports
```

## Requirements

- Python >= 3.8
- pyserial >= 3.5
- KB2040 with mux controller firmware installed

## License

MIT

## Testing

Run the test suite with pytest:

```bash
cd python
poetry install
poetry run pytest test_mux.py -v
```

To test with a different serial port, set the `MUX_PORT` environment variable:

```bash
MUX_PORT=/dev/cu.usbmodemXXX poetry run pytest test_mux.py -v
```

## Links

- [Project Repository](https://github.com/amahpour/KB2040-CD74HCx4067-controller)
- [Hardware Documentation](../README.md)

