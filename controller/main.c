#include "motor.h"
#include "connector.h"


#define LED PC13


Connector connector;
Motor motor;


void setup() {
  connector.Setup(9600);
}

void loop() {
  String raw_command = connector.Handle();
  const char* command = raw_command.c_str();

  if (strcmp(command, "NULL") != 0) {
    char direction = command[0];
    raw_command.remove(0, 1);

    if (direction == 'f') {
      motor.SetDirection(Motor::FORWARD);
      connector.Send("forward");
    }

    else if (direction == 'b') {
      motor.SetDirection(Motor::BACKWARD);
      connector.Send("backward");
    }

    else if (direction == 'k') {
      motor.Stop();
      connector.Send("stop");
    }

    else if (direction == 's') {
      motor.Start();
      connector.Send("start");
    }

    motor.SetSpeedDelay((uint16_t)raw_command.toInt());
  }

  motor.Move();
}