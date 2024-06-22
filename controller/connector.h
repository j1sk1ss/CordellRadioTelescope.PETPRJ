#ifndef CONNECTOR_H_
#define CONNECTOR_H_


#include <Arduino.h>
#include <cstdint> 


class Connector {
public:
  Connector(uint32_t baud_rate);
  String Handle();
  void Send(String data);

private:
  uint32_t baud_rate;

};

#endif