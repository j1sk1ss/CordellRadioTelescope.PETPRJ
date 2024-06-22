#ifndef SPECTRUM_H_
#define SPECTRUM_H_


#include <Arduino.h>
#include <stdint.h>

#define POT_PIN 0


class Spectrum {
public:
  uint16_t Read();
  uint16_t* ReadSample(uint8_t count);
};

#endif