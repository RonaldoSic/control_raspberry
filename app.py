# IMPORTANDO LAS LIBRERIAS NECESARIAS
import RPi.GPIO as GPIO
import time
import cv2
import os
# Cargamos las caracteristicas de los rostros
cascade = os.getcwd()+'/cascade_face.xml'
face_cascade = cv2.CascadeClassifier(cascade)
# print(cascade)


# CONFIGURANDO LOS PINES NECESARIO
pin = 7 
servo = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# DECLARANDO EL MODO DE USO DE LOS PINES 
GPIO.setup(pin, GPIO.OUT)
GPIO.setup(servo, GPIO.OUT)

# config
pulso = GPIO.PWM(servo, 50)
pulso.start(2.5)

# color del rectangulo de las caras
color_rectangle = (59, 67, 245)

# Funcion para detectar los rostros en el video
def detectar_cara (imagen):
    img_copy = imagen.copy()
    rectangulos = face_cascade.detectMultiScale(img_copy)
    for (x,y,w,h) in rectangulos:
        cv2.rectangle(img_copy,pt1= (x,y),pt2=(x+w, y+h), color=color_rectangle, thickness=4)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.010)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.020)
        # servoMove()
    return img_copy

def servoMove():
    # pulso = GPIO.PWM(servo, 50)
    # pulso.start(2.5)
    try:
        while True:
            for i in range(0, 180):
                grados = ((1.0/18.0) * i) + 2.5
                pulso.ChangeDutyCycle(grados)
            time.sleep(1)
            for i in range(180, 0, -1):
                grados = ((1.0/18.0) * i) + 2.5
                pulso.ChangeDutyCycle(grados)
            time.sleep(1)
    except KeyboardInterrupt:
        pulso.stop()
        GPIO.cleanup()

cap = cv2.VideoCapture(0)

while True:
    res, frame = cap.read()
# if res:
#     GPIO.output(pin, GPIO.HIGH)
#     time.sleep(0.33)
#     GPIO.output(pin, GPIO.LOW)
#     time.sleep(0.40)
    frame = detectar_cara(frame)
    cv2.imshow('Detectar Rostros', frame)
    tecla = cv2.waitKey(1)
    if tecla == 27:
        break

# CODIGO QUE HARA LOS PINES
# for item in range(0, 5):
#     GPIO.output(pin, GPIO.HIGH)
#     time.sleep(1)
#     GPIO.output(pin, GPIO.LOW)
#     time.sleep(1)

GPIO.cleanup()
# Limpiamos y destruimos todas la ventanas creadas
cap.release()
cv2.destroyAllWindows()

