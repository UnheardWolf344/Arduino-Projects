from inputs import get_gamepad
import math
import threading

class XboxController:
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        # define private gamepads vals
        self._leftJoystickY = 0
        self._leftJoystickX = 0
        self._rightJoystickY = 0
        self._rightJoystickX = 0
        self._leftTrigger = 0
        self._rightTrigger = 0
        self._leftBumper = 0
        self._rightBumper = 0
        self._leftThumb = 0
        self._rightThumb = 0
        self._a = 0
        self._x = 0
        self._y = 0
        self._b = 0
        self._options = 0
        self._start = 0
        self._leftDPad = 0
        self._rightDPad = 0
        self._upDPad = 0
        self._downDPad = 0

        # private last gamepad vals for checking for change
        self._lastLeftJoystickY = 0
        self._lastLeftJoystickX = 0
        self._lastRightJoystickY = 0
        self._lastRightJoystickX = 0
        self._lastLeftTrigger = 0
        self._lastRightTrigger = 0
        self._lastLeftBumper = 0
        self._lastRightBumper = 0
        self._lastLeftThumb = 0
        self._lastRightThumb = 0
        self._lastA = 0
        self._lastX = 0
        self._lastY = 0
        self._lastB = 0
        self._lastOptions = 0
        self._lastStart = 0
        self._lastLeftDPad = 0
        self._lastRightDPad = 0
        self._lastUpDPad = 0
        self._lastDownDPad = 0

        # use a separate thread for polling gamepad so we don't miss inputs
        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=(), daemon=True)
        self._monitor_thread.start()

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self._leftJoystickY = round(event.state / XboxController.MAX_JOY_VAL, 2) # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self._leftJoystickX = round(event.state / XboxController.MAX_JOY_VAL, 2) # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self._rightJoystickY = round(event.state / XboxController.MAX_JOY_VAL, 2) # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self._rightJoystickX = round(event.state / XboxController.MAX_JOY_VAL, 2) # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self._leftTrigger = round(event.state / XboxController.MAX_TRIG_VAL, 2) # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self._rightTrigger = round(event.state / XboxController.MAX_TRIG_VAL, 2) # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self._leftBumper = event.state
                elif event.code == 'BTN_TR':
                    self._rightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self._a = event.state
                elif event.code == 'BTN_NORTH':
                    self._y = event.state
                elif event.code == 'BTN_WEST':
                    self._x = event.state
                elif event.code == 'BTN_EAST':
                    self._b = event.state
                elif event.code == 'BTN_THUMBL':
                    self._leftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self._rightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self._options = event.state
                elif event.code == 'BTN_START':
                    self._start = event.state
                elif event.code == 'ABS_HAT0X':
                    self._leftDPad = 1 if event.state == -1 else 0
                    self._rightDPad = 1 if event.state == 1 else 0
                elif event.code == 'ABS_HAT0Y':
                    self._upDPad = 1 if event.state == -1 else 0
                    self._downDPad = 1 if event.state == 1 else 0

    # Then we use custom getters for every single input
    # so that the last state can be updated when it is read,
    # since you would normally update the last state in the main update loop
    # (which is when these will be read).
    # The normal way of updating them in the main loop won't work because 
    # the _monitor_controller function could run multiple times per main loop,
    # so state changes could be missed.
    
    # --- Button A ---
    @property
    def a(self):
        self._lastA = self._a
        return self._a

    def aChanged(self):
        return self._a != self._lastA
        
    # --- Button B ---
    @property
    def b(self):
        self._lastB = self._b
        return self._b

    def bChanged(self):
        return self._b != self._lastB
        
    # --- Button X ---
    @property
    def x(self):
        self._lastX = self._x
        return self._x

    def xChanged(self):
        return self._x != self._lastX
        
    # --- Button Y ---
    @property
    def y(self):
        self._lastY = self._y
        return self._y

    def yChanged(self):
        return self._y != self._lastY

    # --- Left Joystick X ---
    @property
    def left_joystick_x(self):
        self._lastLeftJoystickX = self._leftJoystickX
        return self._leftJoystickX

    def left_joystick_xChanged(self):
        # Using a small tolerance for floating point numbers
        return abs(self._leftJoystickX - self._lastLeftJoystickX) > 0.01

    # --- Left Joystick Y ---
    @property
    def left_joystick_y(self):
        self._lastLeftJoystickY = self._leftJoystickY
        return self._leftJoystickY

    def left_joystick_yChanged(self):
        return abs(self._leftJoystickY - self._lastLeftJoystickY) > 0.01

    # --- Right Joystick X ---
    @property
    def right_joystick_x(self):
        self._lastRightJoystickX = self._rightJoystickX
        return self._rightJoystickX

    def right_joystick_xChanged(self):
        return abs(self._rightJoystickX - self._lastRightJoystickX) > 0.01

    # --- Right Joystick Y ---
    @property
    def right_joystick_y(self):
        self._lastRightJoystickY = self._rightJoystickY
        return self._rightJoystickY

    def right_joystick_yChanged(self):
        return abs(self._rightJoystickY - self._lastRightJoystickY) > 0.01
        
    # --- Left Trigger ---
    @property
    def left_trigger(self):
        self._lastLeftTrigger = self._leftTrigger
        return self._leftTrigger

    def left_triggerChanged(self):
        return abs(self._leftTrigger - self._lastLeftTrigger) > 0.01
        
    # --- Right Trigger ---
    @property
    def right_trigger(self):
        self._lastRightTrigger = self._rightTrigger
        return self._rightTrigger

    def right_triggerChanged(self):
        return abs(self._rightTrigger - self._lastRightTrigger) > 0.01

    # --- Left Bumper ---
    @property
    def left_bumper(self):
        self._lastLeftBumper = self._leftBumper
        return self._leftBumper

    def left_bumperChanged(self):
        return self._leftBumper != self._lastLeftBumper

    # --- Right Bumper ---
    @property
    def right_bumper(self):
        self._lastRightBumper = self._rightBumper
        return self._rightBumper

    def right_bumperChanged(self):
        return self._rightBumper != self._lastRightBumper

    # --- Left Thumb ---
    @property
    def left_thumb(self):
        self._lastLeftThumb = self._leftThumb
        return self._leftThumb

    def left_thumbChanged(self):
        return self._leftThumb != self._lastLeftThumb

    # --- Right Thumb ---
    @property
    def right_thumb(self):
        self._lastRightThumb = self._rightThumb
        return self._rightThumb

    def right_thumbChanged(self):
        return self._rightThumb != self._lastRightThumb

    # --- Options Button ---
    @property
    def options(self):
        self._lastOptions = self._options
        return self._options

    def optionsChanged(self):
        return self._options != self._lastOptions

    # --- Start Button ---
    @property
    def start(self):
        self._lastStart = self._start
        return self._start

    def startChanged(self):
        return self._start != self._lastStart

    # --- D-Pad Left ---
    @property
    def left_dpad(self):
        self._lastLeftDPad = self._leftDPad
        return self._leftDPad

    def left_dpadChanged(self):
        return self._leftDPad != self._lastLeftDPad

    # --- D-Pad Right ---
    @property
    def right_dpad(self):
        self._lastRightDPad = self._rightDPad
        return self._rightDPad

    def right_dpadChanged(self):
        return self._rightDPad != self._lastRightDPad

    # --- D-Pad Up ---
    @property
    def up_dpad(self):
        self._lastUpDPad = self._upDPad
        return self._upDPad

    def up_dpadChanged(self):
        return self._upDPad != self._lastUpDPad

    # --- D-Pad Down ---
    @property
    def down_dpad(self):
        self._lastDownDPad = self._downDPad
        return self._downDPad

    def down_dpadChanged(self):
        return self._downDPad != self._lastDownDPad