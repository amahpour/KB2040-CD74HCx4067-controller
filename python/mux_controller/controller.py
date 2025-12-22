"""CD74HC4067 Multiplexer Controller for KB2040.

This module provides a Python interface to control the CD74HC4067
16-channel multiplexer via serial communication with the KB2040.
"""

import serial
import time
from typing import Optional


class MuxConnectionError(Exception):
    """Raised when there's an issue with the serial connection."""
    pass


class MuxCommandError(Exception):
    """Raised when a command fails or returns an invalid response."""
    pass


class MuxController:
    """Controller for CD74HC4067 multiplexer via KB2040 serial interface.
    
    This class provides a simple API to select channels on the multiplexer
    by sending serial commands to the KB2040 controller.
    
    Example:
        >>> mux = MuxController("/dev/cu.usbmodem101")
        >>> mux.set_channel(5)
        True
        >>> channel = mux.get_channel()
        5
        >>> mux.close()
    """
    
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 2.0):
        """Initialize the mux controller.
        
        Args:
            port: Serial port path (e.g., "/dev/cu.usbmodem101" or "COM3")
            baudrate: Serial baud rate (default: 115200)
            timeout: Serial read timeout in seconds (default: 2.0)
            
        Raises:
            MuxConnectionError: If the serial connection cannot be established
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._serial: Optional[serial.Serial] = None
        
        try:
            self._serial = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout,
                write_timeout=timeout
            )
            # Give the serial port a moment to initialize
            time.sleep(0.1)
            # Clear any buffered data
            self._serial.reset_input_buffer()
        except serial.SerialException as e:
            raise MuxConnectionError(f"Failed to connect to {port}: {e}") from e
    
    def set_channel(self, channel: int) -> bool:
        """Select a channel on the multiplexer.
        
        Args:
            channel: Channel number (0-15)
            
        Returns:
            True if the channel was set successfully
            
        Raises:
            ValueError: If channel is out of range (0-15)
            MuxCommandError: If the command fails or returns an error
            MuxConnectionError: If the serial connection is lost
        """
        if not 0 <= channel <= 15:
            raise ValueError(f"Channel must be between 0 and 15, got {channel}")
        
        if self._serial is None or not self._serial.is_open:
            raise MuxConnectionError("Serial connection is not open")
        
        try:
            # Send command
            command = f"CH {channel}\n"
            self._serial.write(command.encode('ascii'))
            self._serial.flush()
            
            # Read response
            response = self._serial.readline().decode('ascii').strip()
            
            if response.startswith("OK:"):
                # Parse the channel number from response
                try:
                    response_channel = int(response.split(":")[1])
                    if response_channel == channel:
                        return True
                    else:
                        raise MuxCommandError(
                            f"Channel mismatch: requested {channel}, got {response_channel}"
                        )
                except (ValueError, IndexError):
                    raise MuxCommandError(f"Invalid response format: {response}")
            elif response.startswith("ERR:"):
                error_type = response.split(":")[1]
                raise MuxCommandError(f"Controller error: {error_type}")
            else:
                raise MuxCommandError(f"Unexpected response: {response}")
                
        except serial.SerialException as e:
            raise MuxConnectionError(f"Serial communication error: {e}") from e
    
    def get_channel(self) -> int:
        """Get the currently selected channel.
        
        Returns:
            Current channel number (0-15)
            
        Raises:
            MuxCommandError: If the command fails or returns an invalid response
            MuxConnectionError: If the serial connection is lost
        """
        if self._serial is None or not self._serial.is_open:
            raise MuxConnectionError("Serial connection is not open")
        
        try:
            # Send STATUS command
            self._serial.write(b"STATUS\n")
            self._serial.flush()
            
            # Read response
            response = self._serial.readline().decode('ascii').strip()
            
            if response.startswith("CH:"):
                try:
                    channel = int(response.split(":")[1])
                    if 0 <= channel <= 15:
                        return channel
                    else:
                        raise MuxCommandError(f"Invalid channel number in response: {channel}")
                except (ValueError, IndexError):
                    raise MuxCommandError(f"Invalid response format: {response}")
            else:
                raise MuxCommandError(f"Unexpected response: {response}")
                
        except serial.SerialException as e:
            raise MuxConnectionError(f"Serial communication error: {e}") from e
    
    def close(self):
        """Close the serial connection."""
        if self._serial is not None and self._serial.is_open:
            self._serial.close()
            self._serial = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close()

