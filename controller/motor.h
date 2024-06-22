#ifndef MOTOR_H_
#define MOTOR_H_

#include <stdint.h>
#include <Arduino.h>

#define DIRECTION_PIN PB4
#define STEP_PIN      PB5


class Motor {
public:
  Motor();

  enum direction {
    FORWARD, BACKWARD
  };

  void Move();
  void SetDirection(direction new_direction);
  void SetResolution(uint8_t new_resolution);
  void SetSpeedDelay(uint16_t new_delay);

  void Start();
  void Stop();

private:
  direction motor_direction;
  uint8_t resolution;
  uint16_t speed_delay;

};

#endif