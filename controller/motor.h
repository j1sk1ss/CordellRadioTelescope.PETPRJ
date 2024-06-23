#ifndef MOTOR_H_
#define MOTOR_H_

#include <stdint.h>
#include <Arduino.h>


#define DIRECTION_PIN PA0
#define STEP_PIN      PA1
#define ENABLE_PIN    PA2

#define FULL_CIRCLE 200


class Motor {
public:
  Motor();

  enum direction {
    FORWARD, BACKWARD
  };

  void Move();
  void SetDirection(direction new_direction);
  void SetSpeedDelay(uint16_t new_delay);

  void Start();
  void Stop();

private:
  direction motor_direction;
  uint16_t speed_delay;

};

#endif