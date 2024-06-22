#include "spectrum.h"


uint16_t Spectrum::Read() {
  uint16_t a0_value = analogRead(POT_PIN);
  return a0_value;
}

uint16_t* Spectrum::ReadSample(uint8_t count) {
  // TODO
}