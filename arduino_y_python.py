import serial
from time import sleep
import cv2
import os
# Cargamos las caracteristicas de los rostros
cascade = os.getcwd()+'/cascade_face.xml'
face_cascade = cv2.CascadeClassifier(cascade)
# print(cascade)

# color del rectangulo de las caras
color_rectangle = (59, 67, 245)
cap = cv2.VideoCapture(0)

face_time = int(0)

# Funcion para detectar los rostros en el video
def Detectar_cara (imagen):
    global face_time
    global seleccion
    img_copy = imagen.copy()
    rectangulos = face_cascade.detectMultiScale(img_copy, 1.3, 5)
    if len(rectangulos) > 0:
      face_time += 1
      print("El contador esta por este nivel {}".format(face_time))
      if face_time == 60:
        print('\tRostro detectado')
        seleccion = 'horaio'
        print("Has enviado esto 1 {}".format(seleccion))
        msj = seleccion.encode("latin-1")      
        ser.write(msj)
        sleep(8)
      elif face_time == 90:        
        print('\tNo hay rostro')    
        seleccion = 'antihorario'
        print("Has enviado esto 2 {}".format(seleccion))
        msj = seleccion.encode("latin-1")      
        ser.write(msj)
        sleep(8)
        face_time = 0
        # GPIO.cleanup()
    for (x,y,w,h) in rectangulos:
        cv2.rectangle(img_copy,pt1= (x,y),pt2=(x+w, y+h), color=color_rectangle, thickness=4)      
    return img_copy





# NOMBRE DEL DISPOSITIVO SERIAL
# PARA ENCONTRAR EL NOMBRE DEL DISPOSITIVO SE PUDE EJECUTAR LOS SIGUIENTE:
# dmesg | grep -v disconnect | grep -Eo "tty(ACM|USB)." | tail -1
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.flushInput() # limpia todo lo que esta en la entrada serial antes de leer los datos
opc = int(6)
seleccion = ''
def iluminacion (line):
  if int(line) < 200:
    hacer = 'ON'
  else:
    hacer = 'OFF'
  return hacer


def main():
  while True:
    # print('RUnning...')    
    try:
      # print('In to try...')   
      _, frame = cap.read()
      frame = Detectar_cara(frame)
      cv2.imshow('Detectar Rostros', frame)
      tecla = cv2.waitKey(1)
      if tecla == 27:
        break
      # lineBytes = ser.readline() # lee los dato que vengan del Arduino
      # line = lineBytes.decode('utf-8').strip() # codificamos los datos a tipo string
      # print(line) 
      # msj = iluminacion(line).encode("latin-1") # codificamos el mensaje
      # y lo mandamos al arduino por este metodo
      # ser.write(msj)
      # giroMotor()
      # print("Has enviado esto {}".format(seleccion))
      # msj = seleccion.encode("latin-1")      
      # ser.write(msj)  
      # sleep(0.5)
    except KeyboardInterrupt:
      break  
  # Limpiamos y destruimos todas la ventanas creadas
  cap.release()
  cv2.destroyAllWindows()

def giroMotor():
  global seleccion
  global opc
  while True:
    print("\t\tElige una opcion\n\t 1. Giro sentido horario: \n\t 2. Sentido antihorario: \n\t 0. Salir\n")
    opc = int(input('Elige una opcion: '))
    if opc == 1: 
      seleccion = "horaio"
      print('\t\t\tElegiste la opcion 1')
      sleep(0.8)
      break
    elif opc == 2:
      seleccion = "antihorario"
      print('\t\t\tElegiste la opcion 2')
      sleep(0.8)
      break
    elif opc == 0:
      if len(seleccion) > 0:      
        print('El valor que se retorna es {}'.format(seleccion))
        print('\t\tSaliendo ...')
        sleep(1)
        # return seleccion
        break
      else:
        seleccion = 'vacia'
        print('Saliendo {}'.format(seleccion))
        break
  
# giroMotor()
main()