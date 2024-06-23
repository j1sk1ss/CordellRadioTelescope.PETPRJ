#include "motor.h"


Motor::Motor() {
  // Setup default params
  this->motor_direction = direction::FORWARD;
  this->speed_delay = 2000;
  this->is_block = true;

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

void Motor::Move(uint16_t steps) {
  this->is_block = true;
  for (int i = 0; i < steps; i++) Move();
  this->is_block = false;
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
  this->is_block = false;
  digitalWrite(ENABLE_PIN, LOW);
}

void Motor::Stop() {
  this->is_block = true;
  digitalWrite(ENABLE_PIN, HIGH);
}

void Motor::SetBlock(bool block) {
  this->is_block = block;
}

bool Motor::IsBlock() {
  return this->is_block;
}