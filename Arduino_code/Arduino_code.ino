#include <Arduino.h>

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
// float mf = 11.24;
float mf = 2.981948184762631;
// float me = 0.41;
float me = 0.1832775164485459;
// float m0 = 1.36;
float m0 = 0.8669426255437207;
float uf_max = 4735.83;
float ue_max = 2000.35;
float uf_min = 1830.792;
float ue_min = 985.28;
float vel_max = 60;
float prev_velocity = 0;
float curr_velocity = 0;
float prev_position = 0;
float curr_position = 0;
float K_max = 7;
float K = 0;
float ENV_Freq = 25;

void setup() {
  Serial.begin(9600);
}

void loop() {
  float sig_flex = analogRead(A0); // Read the flexion sensor value
  float sig_ext = analogRead(A1); // Read the extension sensor value

  filtered_sig_flex = alpha * sig_flex + (1 - alpha) * filtered_sig_flex; // Apply the low pass filter
  filtered_sig_ext = alpha * sig_ext + (1 - alpha) * filtered_sig_ext; // Apply the low pass filter

  float sig_flex_millivolts = (filtered_sig_flex/1023) * 5; // Convert to millivolts
  float sig_flex_volts = sig_flex_millivolts * 1000; // Convert to volts

  float sig_ext_millivolts = (filtered_sig_ext/1023) * 5; // Convert to millivolts
  float sig_ext_volts = sig_ext_millivolts * 1000; // // Convert to millivolts

  float uf_norm = (sig_flex_volts - uf_min) / (uf_max - uf_min);
	float ue_norm = (sig_ext_volts - ue_min) / (ue_max - ue_min);

  if (uf_norm <= 0) uf_norm = 0;
  if (uf_norm >= 1) uf_norm = 1;
  if (ue_norm <= 0) ue_norm = 0;
  if (ue_norm >= 1) ue_norm = 1;

  float m = uf_norm / ue_norm;

  if      (m >= m0) curr_velocity = vel_max * ((m - m0)/(mf - m0));
  else if (m < m0)  curr_velocity = vel_max * ((m - m0)/(m0 - me));

  if      (curr_velocity > vel_max)  curr_velocity = vel_max;
  else if (curr_velocity < -vel_max) curr_velocity = -vel_max;

  K = K_max * sqrt(uf_norm * uf_norm + ue_norm * ue_norm);
  curr_position = (curr_velocity + prev_velocity) * 0.5 * (1 / ENV_Freq) + prev_position; // Integration
  
  /* Proportional control */
  // curr_position = uf_norm * 90; 
  // curr_position = (curr_position + prev_position) / 2.0; // Smooth the position

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

  prev_position = curr_position;
	prev_velocity = curr_velocity;

  delay(1);
}