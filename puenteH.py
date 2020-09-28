import RPi.GPIO as GPIO
import sys
import cv2
import os
from time import sleep
# Cargamos las caracteristicas de los rostros
cascade = os.getcwd()+'/cascade_face.xml'
face_cascade = cv2.CascadeClassifier(cascade)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

direccion = 24 # pin DIR
step = 26 # pin Step
numSteps = 200
microPausa = 0.002
# microPausa1 = 0.0002

# GPIO.setup(direccion, GPIO.OUT)
# GPIO.setup(step, GPIO.OUT)


# color del rectangulo de las caras
color_rectangle = (59, 67, 245)
cap = cv2.VideoCapture(0)

face_time = 0

# Funcion para detectar los rostros en el video
def Detectar_cara (imagen):
    global face_time
    img_copy = imagen.copy()
    rectangulos = face_cascade.detectMultiScale(img_copy, 1.3, 5)
    if len(rectangulos) > 0:
      face_time += 1
      print()
      if face_time > 15:
        print('\t\tRostro detectado')
        finished_step = Motor_nema()
        if finished_step:
          sys.exit(0)          
      else:
        print('\tNo hay rostro')
        GPIO.cleanup()
    for (x,y,w,h) in rectangulos:
        cv2.rectangle(img_copy,pt1= (x,y),pt2=(x+w, y+h), color=color_rectangle, thickness=4)      
    return img_copy




cont = 0
def Motor_nema():
  completado = False
  global cont 
  while True:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(direccion, GPIO.OUT)
    GPIO.setup(step, GPIO.OUT)
    print('Work {}'.format(cont))
    GPIO.output(direccion, 0)
    for item in range(0, numSteps):
      GPIO.output(step, 1)  
      sleep(microPausa)
      GPIO.output(step, 0)
    sleep(1.5) # Cambio de direccion
    GPIO.output(direccion, 1)
    for item in range(0, numSteps):
      GPIO.output(step, 1)
      sleep(microPausa)
      GPIO.output(step, 0)
    cont += 1
    print('El contador \t{}'.format(cont))
    if cont >= 15:
      print("Se acabo el programa")
      # sys.exit(0)
      print("Rompiendo el ciclo")
      completado = True
      return completado
      break
    else:
      completado = False 
      return completado

  # GPIO.output(direccion, 0)
  # GPIO.output(step, 0)
  # GPIO.setwarnings(False)          
  # GPIO.cleanup()
  
  
    

# num = 0
# for i in range(1, 3):
#   print('\t\tEjecucion {}'.format(i))
#   Motor_nema()
#   num += 1
#   if num>2:
#     sys.exit(0)

# Motor_nema()
# sleep(5)
# sys.exit(0)

while True:
  _, frame = cap.read()
  frame = Detectar_cara(frame)
  cv2.imshow('Detectar Rostros', frame)
  tecla = cv2.waitKey(1)
  GPIO.cleanup()
  if tecla == 27:
    break

GPIO.cleanup()
# Limpiamos y destruimos todas la ventanas creadas
cap.release()
cv2.destroyAllWindows()
# sys.exit(0)
