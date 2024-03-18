#define SIG_PIN A0

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  float sig = analogRead(SIG_PIN); // Read the signal
  // Serial.println(sig);

  float sigMillivolts = (sig/1023) * 5; // Convert to millivolts
  Serial.println(sigMillivolts*1000);

  delay(1);
}
