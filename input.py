import serial
import time
from enum import Enum, unique
from inputs import devices
import xbox_controller

# Constants
BAUD_RATE = 115200
SERIAL_PORT = "COM5"
DATA_DELIMITER = ','
DATA_SEPARATOR = ''

# Enum for consistency of transmission btwn this and arduino
@unique
class GamepadKeys(Enum):
    B = 'B'
    A = 'A'
    Y = 'Y'
    X = 'X'
    OPTIONS = 'O'
    START = 'S'
    DPAD_UP = 'U'
    DPAD_DOWN = 'D'
    DPAD_RIGHT = 'R'
    DPAD_LEFT = 'L'
    RIGHT_BUMPER = 'C'
    LEFT_BUMPER = 'E'
    RIGHT_TRIGGER = 'F'
    LEFT_TRIGGER = 'G'
    RIGHT_STICK_Y = 'H'
    RIGHT_STICK_X = 'I'
    LEFT_STICK_Y = 'J'
    LEFT_STICK_X = 'K'

data_to_send: str = ""

# checks serial input
def check_for_arduino_message(serial_connection: serial.Serial):
    if serial_connection.in_waiting:
        try:
            line = serial_connection.readline()
            
            message = line.decode('utf-8').strip()
            
            print(f"ARDUINO: {message}")
        
        except Exception as e:
            print(f"Error reading serial response: {e}")

# used to add data to the buffer to be transmitted to the arduino
def add_data(ID: str, data):
    global data_to_send

    # if there is no data yet, write directly
    # otherwise, add a delimiter
    if not data_to_send:
        data_to_send += f"{ID}{DATA_SEPARATOR}{data}"
    else:
        data_to_send += f"{DATA_DELIMITER}{ID}{DATA_SEPARATOR}{data}"

# transmit buffer to arduino, then clear buffer
def send_over_serial():
    global data_to_send
    data_to_send += "\n"
    ser.write(data_to_send.encode('utf-8'))
    print(f"Sending: {data_to_send.strip()}")
    data_to_send = ""

# set up serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    print(f"Serial port {SERIAL_PORT} opened successfully at {BAUD_RATE} baud.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# wait for arduino to restart
time.sleep(1.5)

if devices.gamepads.count == 0:
    print("No gamepad detected.")
    ser.close()
    exit()

gamepad = devices.gamepads[0]
print(f"Gamepad '{devices.gamepads[0].name}' detected.")

gamepad = xbox_controller.XboxController()

try:
    while True:
        # these allow serial data to only be sent on state change,
        # probably increasing efficiency or something
        if gamepad.bChanged():
            add_data(GamepadKeys.B.value, gamepad.b)
        if gamepad.left_joystick_xChanged():
            add_data(GamepadKeys.LEFT_STICK_X.value, f"{gamepad.left_joystick_x:.2f}")

        check_for_arduino_message(ser)

        if (data_to_send):
            send_over_serial()

except KeyboardInterrupt:
    print("\nScript terminated by user.")
except Exception as e:
    print(f"\nAn error occurred: {e}")
finally:
    if ser.is_open:
        ser.close()

