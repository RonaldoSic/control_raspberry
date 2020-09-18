import RPi.GPIO as GPIO
import sys
import cv2
import os
from time import sleep
# Cargamos las caracteristicas de los rostros
cascade = os.getcwd()+'/cascade_face.xml'
face_cascade = cv2.CascadeClassifier(cascade)


GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)

direccion = 24 # pin DIR
step = 26 # pin Step
numSteps = 400
microPausa = 0.0009
microPausa1 = 0.002

# GPIO.setup(direccion, GPIO.OUT)
# GPIO.setup(step, GPIO.OUT)


# color del rectangulo de las caras
color_rectangle = (59, 67, 245)
cap = cv2.VideoCapture(0)

# Funcion para detectar los rostros en el video
def Detectar_cara (imagen):
    img_copy = imagen.copy()
    rectangulos = face_cascade.detectMultiScale(img_copy)
    for (x,y,w,h) in rectangulos:
        cv2.rectangle(img_copy,pt1= (x,y),pt2=(x+w, y+h), color=color_rectangle, thickness=4)
        # Motor_nema()
    # if img_copy:
    print('\t\t Detectando algo \n\t{}'.format(img_copy))
    return img_copy




def Motor_nema():
  cont = 0
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
    sleep(1) # Cambio de direccion
    GPIO.output(direccion, 1)
    for item in range(0, numSteps):
      GPIO.output(step, 1)
      sleep(microPausa1)
      GPIO.output(step, 0)
    cont += 1

    # if cont > 5:
    #   print("Se acabo el programa")
    #   sys.exit(0)
    #   print("Rompiendo el ciclo")
    #   break          
  GPIO.cleanup()
  
    

# num = 0
# for i in range(1, 3):
#   print('\t\tEjecucion {}'.format(i))
#   Motor_nema()
#   num += 1
#   if num>2:
#     sys.exit(0)

# Motor_nema()


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
sys.exit(0)
