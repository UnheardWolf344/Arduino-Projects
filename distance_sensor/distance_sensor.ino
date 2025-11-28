const uint8_t echoPin = 2;
const uint8_t trigPin = 3;
const uint8_t ledPin = 12;

long duration; 
float distance = 0;
float rawDistance = 0;
float lastDistance = 0;
float lowPass = 0.15;

void setup()
{
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT); 
    pinMode(ledPin, OUTPUT);

    // Serial Communication is starting with 9600 of
    // baudrate speed
    Serial.begin(115200);

    // The text to be printed in serial monitor
    Serial.println(F("Distance measurement using Arduino Uno."));
    delay(500);
}

void loop(){
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2); // wait for 2 ms to avoid
                          // collision in serial monitor
    digitalWrite(trigPin, HIGH); // turn on the Trigger to generate pulse
    delayMicroseconds(10); // keep the trigger "ON" for 10 ms to generate
             // pulse for 10 ms.

    digitalWrite(trigPin, LOW); // Turn off the pulse trigger to stop
                       // pulse generation

    // If pulse reached the receiver echoPin
    // become high Then pulseIn() returns the
    // time taken by the pulse to reach the
    // receiver

    duration = pulseIn(echoPin, HIGH);
    lastDistance = distance;
    rawDistance = duration * 0.0344 / 2; // Expression to calculate
                                 // distance using time

    if (abs(rawDistance - lastDistance) <= 700) {
      distance = lowPass * rawDistance + (1 - lowPass) * lastDistance;
    }

    Serial.print("Distance:");
    Serial.print(distance); // Print the output in serial monitor
    Serial.print(",");
    Serial.print("RawDistance:");
    Serial.print(rawDistance);
    Serial.println(",");
    delay(100);

    if (distance < 10) {
      digitalWrite(ledPin, HIGH);
    } else {
      digitalWrite(ledPin, LOW);
    }
}
