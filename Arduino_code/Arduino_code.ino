/*
Low pass filter implemented as a weighted average between the current sensor value
and the previously filtered value, rather than like a traditional analog filter with a defined cutoff frequency.
The alpha factor in the code serves as a smoothing parameter, not a traditional cutoff frequency.
The lower the alpha value, the smoother the filter response, and the higher the alpha value, the faster the filter response.
*/

/* Low Pass Filter Parameters */
const float alpha = 0.1; // Smoothing factor (0 < alpha < 1)
float filtered_sig_flex = 0; // Initial filtered flexion value 
float filtered_sig_ext = 0; // Initial filtered extension value

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

  Serial.print(sig_flex_volts);
  Serial.print(",");
  Serial.println(sig_ext_volts);

  delay(10);
}