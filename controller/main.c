#include <Wire.h> 

#define POT_PIN 0
#define LED     PC13


uint16_t a0_value = 0;


void setup() {
  pinMode(LED, OUTPUT);
  pinMode(POT_PIN, INPUT_ANALOG);

  Serial.begin(115200);
  Wire.begin();

  while (!Serial);

  digitalWrite(LED, LOW);
}

void loop() {
  a0_value = analogRead(POT_PIN);
  Serial.println(a0_value);

  if (a0_value > 1024) digitalWrite(LED, HIGH);
  else digitalWrite(LED, LOW);
}