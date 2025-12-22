# KB2040-CD74HCx4067-controller

CD74HCx4067 Controller using the KB2040 as a UART bridge

## Dependencies

### Arduino CLI

Install `arduino-cli` if not already installed:

```bash
# macOS (Homebrew)
brew install arduino-cli

# Or download from: https://arduino.github.io/arduino-cli/
```

### RP2040 Board Package

Add the Earle Philhower RP2040 board package and install:

```bash
# Add the board manager URL
arduino-cli config set board_manager.additional_urls https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json

# Update index and install
arduino-cli core update-index
arduino-cli core install rp2040:rp2040
```

### Board Selection

When compiling/uploading, use FQBN: `rp2040:rp2040:adafruit_kb2040`

## Hardware Wiring

Connect the KB2040 to the CD74HC4067 multiplexer as follows:

| KB2040 GPIO | CD74HC4067 Pin | Function | Binary Weight |
|-------------|----------------|----------|---------------|
| GPIO 2      | S0             | Select bit 0 | 2^0 (LSB) |
| GPIO 3      | S1             | Select bit 1 | 2^1 |
| GPIO 4      | S2             | Select bit 2 | 2^2 |
| GPIO 5      | S3             | Select bit 3 | 2^3 (MSB) |
| GND         | GND            | Common ground | - |
| 3.3V        | VCC            | Power supply | - |
| -           | E (Enable)     | Enable pin (tied to GND) | - |

**Note:** The Enable (E) pin on the CD74HC4067 must be LOW for the mux to function. It should be tied to GND.

**Important:** GPIO pin 1 on the KB2040 does not work properly for this application, so pins are shifted to GPIO 2-5.

## Building and Uploading

### Compile the sketch:

```bash
arduino-cli compile --fqbn rp2040:rp2040:adafruit_kb2040 mux_controller
```

### Upload to KB2040:

```bash
# Find your port (usually /dev/cu.usbmodemXXX on macOS)
arduino-cli board list

# Upload
arduino-cli upload -p /dev/cu.usbmodemXXX --fqbn rp2040:rp2040:adafruit_kb2040 mux_controller
```

Or use the Arduino MCP tools which can auto-detect the port.

## Serial Protocol

The controller communicates over USB Serial at **115200 baud**. Commands are newline-terminated.

### Commands

| Command | Example | Response | Description |
|---------|---------|----------|-------------|
| `CH n` | `CH 5` | `OK:5` | Select channel 0-15 |
| `STATUS` | `STATUS` | `CH:5` | Query current channel |
| `?` | `?` | `CH:5` | Query current channel (short form) |
| `HELP` | `HELP` | Help text | List available commands |

### Error Responses

- `ERR:RANGE` - Channel number out of valid range (0-15)
- `ERR:CMD` - Unknown command

### Usage Examples

```bash
# Connect via serial terminal (e.g., screen, minicom, Arduino Serial Monitor)
screen /dev/cu.usbmodem101 115200

# Select channel 0
CH 0
# Response: OK:0

# Select channel 15
CH 15
# Response: OK:15

# Check current channel
STATUS
# Response: CH:15

# Get help
HELP
# Response: CD74HC4067 Controller Commands: ...
```

## Channel Selection

The CD74HC4067 uses binary encoding to select channels:

| Channel | S3 | S2 | S1 | S0 |
|---------|----|----|----|----|
| 0       | 0  | 0  | 0  | 0  |
| 1       | 0  | 0  | 0  | 1  |
| 2       | 0  | 0  | 1  | 0  |
| 3       | 0  | 0  | 1  | 1  |
| ...     | ...| ...| ...| ...|
| 15      | 1  | 1  | 1  | 1  |

The controller automatically converts the channel number to the correct binary pattern on GPIO pins 2-5.
