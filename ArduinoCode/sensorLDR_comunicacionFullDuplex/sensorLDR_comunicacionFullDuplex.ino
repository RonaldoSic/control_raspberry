// PINES A USAR
int ldr = A0;
int led = 13;

void setup(){
  pinMode(ldr, INPUT);
  pinMode(led, OUTPUT);
  //velocidad de transmision serial
  Serial.begin(9600);  
}

void loop(){
// LECTURA DEL SENSOR ANALOGICO Y SE IMPRIME SU VALOR EN MONITR SERIAL
  int valorPin = analogRead(ldr);
  Serial.println(valorPin);
  delay(500);
// COMUNICACION DE LA RASPBERRY AL ARDUINO
  if (Serial.available() > 0){
    //DESCARTAMOS LOS SALTOS DE LINEA QUE PUEDEN VENIR DE LA RPI
    String data_in = Serial.readStringUntil('\n');
    // EL VALOR QUE ESPERAMOS SON LOS SIGUIENTES 'ON' O 'OFF' Y LOS VALIDAMOS SI ESTAN ESOS DATOS
    if (data_in == "ON"){
      digitalWrite(led, HIGH);      
    } else if(data_in == "OFF"){
      digitalWrite(led, LOW);      
    }
  }delay(100); //LA LECTURA DEL PUERTO SERIAL SERA A CADA 100 Mls
  
  
}

