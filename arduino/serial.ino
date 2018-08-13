/************************************************
 * Auxiliar Functions
 ***********************************************/

// Function to read command from serial port
char* readSerial(int max_char_length=40) {
  int i = 0;
  char command[max_char_length];
  for (i = 0; i < max_char_length; i++) {
    command[i] = '\0';
  }
  i = 0;
  while(Serial.available()) {
    command[i++] = (char) Serial.read();
    if (i == max_char_length) {
      break;
    }
  }

  return command;
}

/************************************************
 * Main Functions
 ***********************************************/

void setup() {
  Serial.begin(115200);
  pinMode(13, OUTPUT);
}

void loop() {

  // Reads command
  char* command = readSerial();

  // Logic to control led
  if (strcmp(command, "on") == 0) {
    Serial.println("turning on ..");
    digitalWrite(13, HIGH);
    }
  else if (strcmp(command, "off") == 0){
    Serial.println("turning off ..");
    digitalWrite(13, LOW);
  }

  delay(1000);
}
