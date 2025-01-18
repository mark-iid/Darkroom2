# darkroom2

Dark Room 2 Code

Dark Room was an escape room project utilizing Raspberry Pi Pico microcontrollers, Raspberry Pi 4 computers, and other devices to control the main scoring/tracking system, various puzzles involving codes, servos, displays, and hidden buttons.

## Videos

[![Dark Room 2 Main Control Unit](https://img.youtube.com/vi/k65V7-WZjJ0/0.jpg)](https://www.youtube.com/watch?v=k65V7-WZjJ0)
[![Dark Room 2 Failure](https://img.youtube.com/vi/XCMcgiAZ-34/0.jpg)](https://

## Key Components

### KeyLockPico

- `lcd_api.py`: Provides an API for interacting with HD44780 compatible character LCDs.
- `lcdtest.py`: Test script for the LCD display.
- `main.py`: Main script for the keypad lock system.
- `pico_i2c_lcd.py`: Implements the LCD interface using I2C.

### MainComputerPi

- `GridItem.py`: Defines the `GridItem` class and `Status` enum for battery status.
- `main.py`: Main script for the portal control system.
- `reset.py`: Script to reset the locks.
- `UI.py`: Custom widget for displaying a 3D box outline using `urwid`.
- `unlock.py`: Script to unlock the door and bookcase linear actuators.
- `resources/griditems.json`: Configuration file for grid items.

### MainComputerPico

- `main.py`: Main script for the Pico microcontroller to handle input/output operations.

### RatCage

- `main.py`: Main script for controlling the servo motor and input/output operations.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.