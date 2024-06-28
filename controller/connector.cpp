#include "connector.h"


void Connector::Setup(uint32_t baud_rate) {
  Serial.begin(baud_rate);
}

String Connector::Handle() {
  if (Serial.available() == 0) return "NULL";

  String incoming_data = "NULL";
  if (Serial.available() > 0) incoming_data = Serial.readStringUntil('\n');
  else return "NULL";

  if (incoming_data.length() > 0) return incoming_data;
  else return "NULL";
}

void Connector::Send(String data) {
  Serial.println(data);
}