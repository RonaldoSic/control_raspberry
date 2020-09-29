#define dirPin 2
#define stepPin 3
#define stepsPerRevolution 200
void setup() {
  // Declare pins as output:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  //velocidad de transmision serial
  Serial.begin(9600);
}

//int unavez = 0;
void loop() {
  //LECTURA DEL PUERTO SERIAL 
  // COMUNICACION DE LA RASPBERRY AL ARDUINO
  if (Serial.available() > 0){
    //DESCARTAMOS LOS SALTOS DE LINEA QUE PUEDEN VENIR DE LA RPI
    String data_in = Serial.readStringUntil('\n');
    // EL VALOR QUE ESPERAMOS SON LOS SIGUIENTES 'ON' O 'OFF' Y LOS VALIDAMOS SI ESTAN ESOS DATOS
    if (data_in == "horaio"){
       girotipoHorario();
    } else if(data_in == "antihorario"){
      giroAntihorario();
    }
  }delay(1000); //LA LECTURA DEL PUERTO SERIAL SERA A CADA 100 Mls 
}

//FUNCION DONDE DA LE GIRO COMPLETO
void giroAntihorario(){
  // Set the spinning direction clockwise:
  digitalWrite(dirPin, HIGH);
  // Spin the stepper motor 1 revolution slowly:
  for (int i = 0; i < stepsPerRevolution * 10; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }
}

void girotipoHorario(){
  // Set the spinning direction counterclockwise:
  digitalWrite(dirPin, LOW);
  // Spin the stepper motor 1 revolution quickly:
  for (int i = 0; i < stepsPerRevolution * 10; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(500);
  }
}





