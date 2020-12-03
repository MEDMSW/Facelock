print("initialisation ...")
import os
import face_recognition
#import picamera
import numpy as np
import pickle
#import RPi.GPIO as GPIO
from time import sleep
import cv2

#  ------------------------------------------------------------------      functions   ------------------------

def menu():
    print(" _______________ menu ________________")
    print("|                                      |")
    print("| 1: Add client                        |")
    print("| 2: Remove client                     |")
    print("| 3: exit                              |")
    print("|______________________________________|")
    
def AddClient():
    
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
    
#  ------------------------------------------------------------------      main program   ------------------------



print("starting script...")
#id, text = reader.read()

# enabled your camera in raspi-config and rebooted first.




output = np.empty((240, 320, 3), dtype=np.uint8)

while True:
    os.system('clear')
    print("waiting for card ...")
    id, text = 0,'LA169308'
    try: #text != None and os.path.isfile('DB/'+text.replace(" ","")+'.medmsw'):
        
        print('DB/'+text.replace(" ","")+'.medmsw')
        db = open('DB/'+text.replace(" ","")+'.medmsw', 'rb') 
        loaded_db = pickle.load(db)
        db.close()
        DB_image = loaded_db[0]
        name = loaded_db[1]
        print(name)
        # Initialize some variables
        face_locations = []
        face_encodings = []

        #while True:
        camera = cv2.VideoCapture(0)
        camera.set(3,320)
        camera.set(4,240)    
        print("Capturing image.")
        rtv,output = camera.read()
        cv2.imwrite('test.jpg',output)
        camera.release()
        
        
        
        print("encoding ...")
        face_locations = face_recognition.face_locations(output)
        face_encodings = face_recognition.face_encodings(output, face_locations)
        print("end encoding ...")
        for face in face_encodings:
        
            # See if the face is a match for the known face(s)
            #print(len(face))
            #print(len(DB_image[0]))
            print("end comparing")
            match = face_recognition.compare_faces([DB_image], face)

            state = "Unknown Person"

            if match[0]:
                
                state = "match"
                #AddClient()
                
            print(state)
            sleep(2)            
    except exception as e:
        print(str(e))
        print("this card is not registered in the database !")
        sleep(2)
        
