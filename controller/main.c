#include "motor.h"
#include "connector.h"


#define MOTOR_TYPE  0
#define DAC_TYPE    1
#define DAC_PIN     PA0


Connector connector;
Motor motor;
int type = MOTOR_TYPE;


void setup() {
  connector.Setup(9600);
}

void loop() {
  String raw_command = connector.Handle();
  const char* command = raw_command.c_str();

  if (strcmp(command, "NULL") != 0) {

    //==============================================
    // General command
    // F<speed> - forward movement
    // B<speed> - backward movement
    // N<speed> - don't change direction of movement
    // K - turn off motor
    // S - turn on motor
    // E - enable movement (infinity movement)
    // D - disable movement
    // ! - check status

      char primary_command = raw_command[0];
      raw_command.remove(0, 1); // Remove the primary command character

      switch (primary_command) {
          case '!':
            connector.Send("connected");
          return;

          case 'f':
              motor.SetDirection(Motor::FORWARD);
              connector.Send("forward");
          break;

          case 'b':
              motor.SetDirection(Motor::BACKWARD);
              connector.Send("backward");
          break;

          case 'n':
              connector.Send("none");
          break;

          case 'k':
              motor.Stop();
              connector.Send("stop");
          break;

          case 's':
              motor.Start();
              connector.Send("start");
          break;

          case 'e':
              motor.SetBlock(false);
              connector.Send("enable");
          break;

          case 'd':
              motor.SetBlock(true);
              connector.Send("disable");
          break;

          case 'a':
            type = DAC_TYPE;
          break;

          case 'm':
            type = MOTOR_TYPE;
            connector.Send("motor");
          break;

          default:
              connector.Send("unknown command");
          return;
      }

      if (isdigit(raw_command[0])) {
          motor.SetSpeedDelay((uint16_t)raw_command.toInt());
      }

    //==============================================
    // Optional command
    // S<steps> - steps of movement
    // I - infinity movement

      int opt_index = skip_digits(raw_command);
      if (opt_index < raw_command.length()) {
          char additional_option = raw_command[opt_index];
          if (additional_option == 's') { // Enable step movement
              raw_command.remove(0, opt_index + 1); // Skip digits and 's'
              uint16_t steps = (uint16_t)raw_command.toInt();
              motor.Move(steps);
              return;
          } else if (additional_option == 'i') { // Enable infinity movement
              motor.SetBlock(false);
          }
      }

    //==============================================
    // Examples:
    // f250s200 - Move forward with step delay 0.25 second by 360 degrees (200 steps with 1.8 degrees per step = 360 degrees)
    // b1000ie - Move backward with step delay 1 second
    // k - stop motor
    //
    // [Warn]
    // If you don't set movement direction and speed delay, motor will use default values:
    // SpeedDelay - 2000 ms
    // Direction - forward
    //==============================================
  }

  if (type == DAC_TYPE) {
    String output = String(analogRead(DAC_PIN));
    output.concat('\n');
    connector.Send(output);
    return;
  }

  if (motor.IsBlock() == false) motor.Move();
}

int skip_digits(String string) {
  int index = 0;
  while (isdigit(string[index]) == 1) index++;
  return index;
}