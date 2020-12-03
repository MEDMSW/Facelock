import face_recognition
import pickle
import picamera
import numpy as np
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
camera = picamera.PiCamera()
camera.resolution = (320, 240)
IMG = np.empty((240, 320, 3), dtype=np.uint8)
try:
        
        CIN = input('CIN: ')
        print("Now place your tag to write")
        reader.write(CIN)
        print("Done")
        print("taking a picture ...")
        camera.capture(IMG, format="rgb")
        print("encoding db...")
        #DB_image = face_recognition.load_image_file('capture.png')
        DB_image = face_recognition.face_encodings(IMG)[0]
        filename = CIN+'.medmsw'
        db = open('DB/'+CIN+'.medmsw', 'wb') 
        pickle.dump(DB_image, db)
        db.close()
        
finally:
        GPIO.cleanup()

