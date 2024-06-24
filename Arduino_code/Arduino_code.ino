#include <Arduino.h>
#include <EEPROM.h>
#include <string.h>
#include <SoftwareSerial.h>

/*
Low pass filter implemented as a weighted average between the current sensor value
and the previously filtered value, rather than like a traditional analog filter with a defined cutoff frequency.
The alpha factor in the code serves as a smoothing parameter, not a traditional cutoff frequency.
The lower the alpha value, the smoother the filter response, and the higher the alpha value, the faster the filter response.
*/

/* Low Pass Filter Parameters */
const float alpha = 0.5; // Smoothing factor (0 < alpha < 1)
float filtered_sig_flex = 0; // Initial filtered flexion value 
float filtered_sig_ext = 0; // Initial filtered extension value

/* Co-contraction parameters */
float mf = 11.0;
float me = 0.5;
float m0 = 1.5;
float uf_max = 4000.0;
float ue_max = 4000.0;
float uf_min = 2000.0;
float ue_min = 2000.0;
float vel_max = 70;
float K_max = 7;
float prev_velocity = 0;
float curr_velocity = 0;
float prev_position = 0;
float curr_position = 0;
float K = 0;
float ENV_Freq = 25;

float receivedValues[9];
bool newDataReceived = false;

/* Creating a virtual serial port to receive parameters from python script */
int RX = 10; // RX digital PIN
int TX = 9;  // TX digital PIN
SoftwareSerial my_serial(TX, RX); 


void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Native USB only
  }
  Serial.println("Native serial ready!");

  my_serial.begin(9600);
  my_serial.println("Virtual serial ready!");
}


void loop() {
  
  /* Check if there is data available in the virtual serial port */
  if (my_serial.available() > 0) {
    read_parameters();
  }

  if (newDataReceived) {
    for (int i = 0; i < 9; i++) {
      Serial.print("Value ");
      Serial.print(i);
      Serial.print(": ");
      Serial.println(receivedValues[i]);
    }

    /* Update the parameters */
    mf = receivedValues[0];
    me = receivedValues[1];
    m0 = receivedValues[2];
    uf_max = receivedValues[3];
    ue_max = receivedValues[4];
    uf_min = receivedValues[5];
    ue_min = receivedValues[6];
    vel_max = receivedValues[7];
    K_max = receivedValues[8];

    newDataReceived = false; // Reset the flag
  }

  /* Read the sensor values */
  float sig_flex = analogRead(A0); // Read the flexion sensor value
  float sig_ext = analogRead(A1); // Read the extension sensor value

  /* Apply the low pass filter */
  filtered_sig_flex = alpha * sig_flex + (1 - alpha) * filtered_sig_flex; // Apply the low pass filter
  filtered_sig_ext = alpha * sig_ext + (1 - alpha) * filtered_sig_ext; // Apply the low pass filter

  /* Convert the sensor values to millivolts and then to volts */
  float sig_flex_millivolts = (filtered_sig_flex/1023) * 5; // Convert to millivolts
  float sig_flex_volts = sig_flex_millivolts * 1000; // Convert to volts
  float sig_ext_millivolts = (filtered_sig_ext/1023) * 5; // Convert to millivolts
  float sig_ext_volts = sig_ext_millivolts * 1000; // Convert to millivolts

  /* Normalize the sensor values */
  float uf_norm = (sig_flex_volts - uf_min) / (uf_max - uf_min);
  float ue_norm = (sig_ext_volts - ue_min) / (ue_max - ue_min);

  /* Saturate the normalized values */
  if (uf_norm <= 0) uf_norm = 0;
  if (uf_norm >= 1) uf_norm = 1;
  if (ue_norm <= 0) ue_norm = 0;
  if (ue_norm >= 1) ue_norm = 1;

  /* Calculate the current velocity */
  float m = uf_norm / ue_norm;

  if      (m >= m0) curr_velocity = vel_max * ((m - m0)/(mf - m0));
  else if (m < m0)  curr_velocity = vel_max * ((m - m0)/(m0 - me));

  /* Saturate the velocity */
  if      (curr_velocity > vel_max)  curr_velocity = vel_max;
  else if (curr_velocity < -vel_max) curr_velocity = -vel_max;

  /* Calculate the current impedance and position */
  K = K_max * sqrt(uf_norm * uf_norm + ue_norm * ue_norm);
  curr_position = (curr_velocity + prev_velocity) * 0.5 * (1 / ENV_Freq) + prev_position; // Integration
  
  /* Proportional control */
  // curr_position = uf_norm * 90; 
  // curr_position = (curr_position + prev_position) / 2.0; // Smooth the position

  /* Saturate the position */
  if      (curr_position > 90.0) curr_position = 90.0;
  else if (curr_position < 0.0)  curr_position = 0;

  Serial.print(sig_flex_volts);
  Serial.print(",");
  Serial.print(sig_ext_volts);
  Serial.print(",");
  Serial.print(uf_norm);
  Serial.print(",");
  Serial.print(ue_norm);
  Serial.print(",");
  Serial.print(curr_position);
  Serial.print(",");
  Serial.println(K);

  // print_paramns();

  prev_position = curr_position;
  prev_velocity = curr_velocity;

  delay(1);
}


/**
 * @brief Read the parameters from the virtual serial port
 * 
 * @param None
 * @return None
 */
void read_parameters() {
  String dataString = ""; // Accumulated string
  while (my_serial.available() > 0) { // While there is data available in the virtual serial port
    char receivedChar = my_serial.read(); // Read the first byte (char)
    dataString += receivedChar; // Append the char to the accumulated string
    delay(2); // Small delay to ensure we get the whole message
  }
  
  /* Attempt to parse the accumulated string to floats */
  if (dataString.length() > 0) {
    int index = 0;
    int startIndex = 0;
    int endIndex = dataString.indexOf(',');

    while (endIndex != -1 && index < 9) {
      receivedValues[index] = dataString.substring(startIndex, endIndex).toFloat();
      startIndex = endIndex + 1;
      endIndex = dataString.indexOf(',', startIndex);
      index++;
    }

    if (index < 9 && startIndex < dataString.length()) {
      receivedValues[index] = dataString.substring(startIndex).toFloat();
      index++;
    }

    if (index == 9) {
      newDataReceived = true;
    }
  }
}


/**
 * @brief Print the parameters to the serial port
 * 
 * @param None
 * @return None
 */
void print_paramns() {
  Serial.print(mf);
  Serial.print(",");
  Serial.print(me);
  Serial.print(",");
  Serial.print(m0);
  Serial.print(",");
  Serial.print(uf_max);
  Serial.print(",");
  Serial.print(ue_max);
  Serial.print(",");
  Serial.print(uf_min);
  Serial.print(",");
  Serial.print(ue_min);
  Serial.print(",");
  Serial.print(vel_max);
  Serial.print(",");
  Serial.println(K_max);
}