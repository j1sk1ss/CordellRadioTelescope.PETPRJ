#include "motor.h"


Motor::Motor() {
  // Setup default params
  this->motor_direction = direction::FORWARD;

  // Configure pins
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIRECTION_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);

  // Turn off driver
  digitalWrite(ENABLE_PIN, HIGH);
}

// 1.8° angle move per resolution
void Motor::Move() {
  digitalWrite(STEP_PIN, HIGH);
  delayMicroseconds(this->speed_delay);
  digitalWrite(STEP_PIN, LOW);
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

void Motor::SetSpeedDelay(uint16_t new_delay) {
  this->speed_delay = new_delay;
}

void Motor::Start() {
  digitalWrite(ENABLE_PIN, LOW);
}

void Motor::Stop() {
  digitalWrite(ENABLE_PIN, HIGH);
}