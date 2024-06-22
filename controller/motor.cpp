#include "motor.h"


Motor::Motor() {
  this->motor_direction = direction::FORWARD;
  this->resolution = 0;

  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIRECTION_PIN, OUTPUT);
}

void Motor::Move() {
  for (int x = 0; x < this->resolution; x++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(this->speed_delay);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(this->speed_delay);
  }    
}

void Motor::SetDirection(direction new_direction) {
  this->motor_direction = new_direction;
  switch (this->motor_direction) {
    case Motor::FORWARD:
      digitalWrite(DIRECTION_PIN, HIGH);
    break;

    case Motor::BACKWARD:
      digitalWrite(DIRECTION_PIN, LOW);
    break;
  }
}

void Motor::SetResolution(uint8_t new_resolution) {
  this->resolution = new_resolution;
}

void Motor::SetSpeedDelay(uint16_t new_delay) {
  this->speed_delay = new_delay;
}

void Motor::Start() {
  this->SetResolution(200);
  this->SetDirection(Motor::FORWARD);
  this->SetSpeedDelay(2000);
}

void Motor::Stop() {
  this->SetResolution(0);
}