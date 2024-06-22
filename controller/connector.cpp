#include "connector.h"


Connector::Connector(uint32_t baud_rate) {
  this->baud_rate = baud_rate;
  Serial.begin(this->baud_rate);
}

String Connector::Handle() {
  String incoming_data = "NULL";
  if (Serial.available() > 0) incoming_data = Serial.readString();
  else return "NULL";

  if (incoming_data.length() > 0) return incoming_data;
  else return "NULL";
}

void Connector::Send(String data) {
  Serial.println(data);
}