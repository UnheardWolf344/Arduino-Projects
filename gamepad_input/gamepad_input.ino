#include <Servo.h>

const uint8_t LED = 12;
const uint8_t SERVO_PIN = 9;

enum class State : bool {
  OFF,
  ON
};

enum class InputType : uint8_t {
  NONE,
  BUTTON,
  ANALOG
};

enum class GamepadKeys : char {
  B = 'B',
  A = 'A',
  Y = 'Y',
  X = 'X',
  OPTIONS = 'O',
  START = 'S',
  DPAD_UP = 'U',
  DPAD_DOWN = 'D',
  DPAD_RIGHT = 'R',
  DPAD_LEFT = 'L',
  RIGHT_BUMPER = 'C',
  LEFT_BUMPER = 'E',
  RIGHT_TRIGGER = 'F',
  LEFT_TRIGGER = 'G',
  RIGHT_STICK_Y = 'H',
  RIGHT_STICK_X = 'I',
  LEFT_STICK_Y = 'J',
  LEFT_STICK_X = 'K'
};

struct InputData {
  InputType type;
  union {
    uint8_t buttonValue;
    float analogValue;
  };
};

struct Inputs {
  char key;
  InputData data;
};

const uint8_t inputsSize = 8;
Inputs inputs[inputsSize];
State state = State::OFF;

bool bPressed = LOW;
bool lastBPressed = LOW;

String inBuffer;
String* inValues;
uint8_t inValuesSize = 0;

Servo servo;
int servoTarget = 0;
float leftStickX = 0.0;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  pinMode(LED, OUTPUT);
  Serial.begin(115200);

  servo.attach(SERVO_PIN);
}

void loop() {
  // put your main code here, to run repeatedly:
  lastBPressed = bPressed;
  handleInput();

  servoTarget = mapFloat(leftStickX, -1.0, 1.0, 0, 180);
  servo.write(servoTarget);

  // switch state when button pressed
  if (bPressed && !lastBPressed) {
    state = state == State::ON ? State::OFF : State::ON;
    Serial.print("Free RAM (bytes): ");
    Serial.println(getFreeRam());
  }

  // led control
  switch (state) {
    case State::ON:
      digitalWrite(LED, HIGH);
      break;
    case State::OFF:
      digitalWrite(LED, LOW);
      break;
  }
}

void handleInput(){
  if (Serial.available()){
    inBuffer = Serial.readStringUntil('\n');
    Serial.print("Recieved: ");
    Serial.println(inBuffer);

    // String* of inValuesSize size
    inValues = split(inBuffer, inValuesSize);
    // now we have a string array of all passed inputs

    clearInputs(inputs, inputsSize);
    uint8_t inputsIndex = 0;
    for (uint8_t i = 0; i < inValuesSize; i++) {
      serialToValue(inValues[i], inputs, inputsIndex);
      inputsIndex++;
    }

    bPressed = getButton(inputs, inputsSize, GamepadKeys::B, bPressed);
    leftStickX = getAnalog(inputs, inputsSize, GamepadKeys::LEFT_STICK_X, leftStickX);

    delete[] inValues;
    inValues = nullptr;
  }
}

String* split(const String& input, uint8_t& size) {
  size = 1;
  int inputLength = input.length();

  for (int i = 0; i < inputLength; i++) {
    if (input.charAt(i) == ',') {
      size++;
    }
  }
  
  // dynamically sized array
  String* values = new String[size];

  int valueIndex = 0;
  int lastDelimiterIndex = -1;

  for (int i = 0; i < inputLength; i++) {
    if (input.charAt(i) == ',') {
      values[valueIndex] = input.substring(lastDelimiterIndex + 1, i);
      lastDelimiterIndex = i;
      valueIndex++;
    }
  }

  // get the last value between delimiter and endl
  values[valueIndex] = input.substring(lastDelimiterIndex + 1);

  return values;
}

void serialToValue(const String& in, Inputs inputs[], uint8_t index) {
  // in is in the format {KEY}:{VALUE}
  // int separatorIndex = in.indexOf(':');
  // if (separatorIndex == -1) return;
  inputs[index].key = in.charAt(0);

  if (in.length() <= 2) {
    inputs[index].data.type = InputType::BUTTON;
    inputs[index].data.buttonValue = (uint8_t) in.substring(1).toInt();
  } else {
    inputs[index].data.type = InputType::ANALOG;
    inputs[index].data.analogValue = in.substring(1).toFloat();
  }
}

bool getButton(Inputs inputs[], uint8_t size, char key, const bool lastValue) {
  for (int i = 0; i < size; i++) {
    if (inputs[i].key == key) {
      return inputs[i].data.buttonValue;
    }
  }
  return lastValue;
}

// overload so you can call getButton with keys
bool getButton(Inputs inputs[], uint8_t size, GamepadKeys key, const bool lastValue) {
  return getButton(inputs, size, (char) key, lastValue);
}

float getAnalog(Inputs inputs[], uint8_t size, char key, const float lastValue) {
  for (uint8_t i = 0; i < size; i++) {
    if (inputs[i].key == key) {
      return inputs[i].data.analogValue;
    }
  }
  return lastValue;
}

// overload so you can call getAnalog with keys
float getAnalog(Inputs inputs[], uint8_t size, GamepadKeys key, const float lastValue) {
  return getAnalog(inputs, size, (char) key, lastValue);
}

void clearInputs(Inputs inputs[], uint8_t inputsSize) {
  Inputs zeroInput = {};

  for (int i = 0; i < inputsSize; i++) {
    inputs[i] = zeroInput;
  }
}

int mapFloat(float value, float fromLower, float fromUpper, int toLower, int toUpper) {
  return (value - fromLower) * (((float) toUpper - (float) toLower) / (fromUpper - fromLower)) + (float) toLower;
}

int getFreeRam() {
  extern int __heap_start, *__brkval;
  int v;
  // This calculates the distance between the current stack pointer (&v)
  // and the current heap pointer (__brkval or __heap_start)
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
}