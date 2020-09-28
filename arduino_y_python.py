import serial
from time import sleep
# NOMBRE DEL DISPOSITIVO SERIAL
# PARA ENCONTRAR EL NOMBRE DEL DISPOSITIVO SE PUDE EJECUTAR LOS SIGUIENTE:
# dmesg | grep -v disconnect | grep -Eo "tty(ACM|USB)." | tail -1
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.flushInput() # limpia todo lo que esta en la entrada serial antes de leer los datos

def iluminacion (line):
  if int(line) < 200:
    hacer = 'ON'
  else:
    hacer = 'OFF'
  return hacer

while True:
  
  try:
      lineBytes = ser.readline() # lee los dato que vengan del Arduino
      line = lineBytes.decode('utf-8').strip() # codificamos los datos a tipo string
      print(line) 
      msj = iluminacion(line).encode("latin-1") # codificamos el mensaje
      # y lo mandamos al arduino por este metodo
      ser.write(msj)
      sleep(0.5)

  except KeyboardInterrupt:
      break
