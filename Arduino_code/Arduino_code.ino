/*
Filtro passa-baixa implementado como uma média ponderada entre o valor atual do sensor 
e o valor filtrado anteriormente, e não como um filtro analógico tradicional com uma frequência de corte definida.

O fator alpha no código serve como um parâmetro de suavização, e não como uma frequência de corte tradicional.
 Quanto menor o valor de alpha, mais suave será a resposta do filtro, e quanto maior o valor de alpha, mais rápida será a resposta do filtro.
*/

// Parâmetros do filtro passa-baixa
const float alpha = 0.1; // Fator de suavização (0 < alpha < 1)
float filtered_sig_flex = 0; // Valor filtrado inicial

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  float sig_flex = analogRead(A0); // Read the signal
  // float sig_ext = analogRead(A1);
  filtered_sig_flex = alpha * sig_flex + (1 - alpha) * filtered_sig_flex; // Aplica o filtro passa-baixa
  // filtered_sig_ext = alpha * sig_ext + (1 - alpha) * filtered_sig_ext; // Aplica o filtro passa-baixa

  float sig_flex_millivolts = (filtered_sig_flex/1023) * 5; // Convert to millivolts
  float sig_flex_volts = sig_flex_millivolts * 1000;

  // float sig_ext_millivolts = (sig_ext/1023) * 5; // Convert to millivolts
  // float sig_ext_volts = sig_ext_millivolts * 1000;


  // Serial.print(sig_flex_volts);
  // Serial.print(",");
  // Serial.println(sig_ext_volts);

  Serial.println(sig_flex_volts);


  delay(10);
}