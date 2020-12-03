print("initialisation ...")
import os
import face_recognition
import picamera
import numpy as np
import pickle
import RPi.GPIO as GPIO
from time import sleep, localtime
from mfrc522 import SimpleMFRC522
GPIO.setwarnings(False)
#  /////////////////////////////////////////////////////////////////      menu function   \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def menu():
    while True:
        
        print(" _______________ menu ________________")
        print("|                                      |")
        print("| 1: Add client                        |")
        print("| 2: Remove client                     |")
        print("| 3: continue                              |")
        print("|______________________________________|")
        
        action = input("[in]: ")
        if action == '1':
            add()
        elif action == '2':
            delete()
        elif action == '3':
            break
        else:
            os.system('clear')
#  /////////////////////////////////////////////////////////////////      add user function   \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def add():
    
    state = 'add user'
    reader = SimpleMFRC522()
    camera = picamera.PiCamera()
    #camera.rotation = 180
    camera.resolution = (320, 240)
    IMG = np.empty((240, 320, 3), dtype=np.uint8)
    
    try:
        
        CIN = input('CIN: ')
        
        
        if not os.path.isfile('DB/'+CIN+'.medmsw'):
            NAME = input('NAME: ')
            print("Now place your tag to write")
            reader.write(CIN)
            print("Done")
            while True:
                print("taking a picture ...")
                camera.capture(IMG, format="rgb")
                print("encoding db...")
                DB_data = []
                face_encodings = face_recognition.face_encodings(IMG)
            
                if len(face_encodings) == 0:
                    
                    print("no face detected!")
                    print("stand in front the camera")
                    if input('press any key to try again or \'e\' to exit: ') == 'e':
                        break;
                if len(face_encodings) > 1:
                    print("more than 1 face is been detected, we need only 1 face")
                    print("stand in front the camera")
                    if input('press any key to try again or \'e\' to exit: ') == 'e':
                        break;
                
                    
                if len(face_encodings) == 1:
                    
                    DB_data.append(face_encodings[0])
                    DB_data.append(NAME)
                    db = open('DB/'+CIN+'.medmsw', 'wb')
                    pickle.dump(DB_data, db)
                    db.close()
                    log(CIN,NAME,state)
                    print("DONE SIGNUP")
                    break;
        else:
            print("this cin is already registered !")
            
    except:
        print("error !")
    finally:
        GPIO.cleanup()
        camera.close()


#  /////////////////////////////////////////////////////////////////      delete user function   \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
def delete():
    state = 'remove user'
    user_cin = input("enter the CIN of the user you want to delete :")
    file_path = 'DB/'+user_cin.replace(" ","")+'.medmsw'
    if os.path.isfile(file_path):
        db = open(file_path, 'rb') 
        loaded_db = pickle.load(db)
        db.close()
        name = loaded_db[1]
        print('do you want to remove ('+name+' | CIN: '+user_cin+' )')
        action = input("[Y|N] : ")
        if action == 'y' or action == 'Y':
            os.remove(file_path)
            log(user_cin,name,state)
            print('user removed successfuly')
            
#  /////////////////////////////////////////////////////////////////         log actions function        \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def log(cin,name,state):
    case_lenth = 30 # we are gonna use it to allign the logs
    # preparing date and time to be printed
    
    time_and_date ='['+str(localtime()[2])+'/'+(2-len(str(localtime()[1])))*'0'+str(localtime()[1])+'/'+(2-len(str(localtime()[0])))*'0'+str(localtime()[0])+' | '+(2-len(str(localtime()[3])))*'0'+str(localtime()[3])+':'+(2-len(str(localtime()[4])))*'0'+str(localtime()[4])+']'
    
    log = open("log.txt","a")
    if state == 'unregisterd':
        
        #                  year                                        month                                                 day                                        hour                     minute                        
        log.write(time_and_date+'  action: this card is not registered in the database\n')
    else:
        log.write(time_and_date+' name: '+name+(case_lenth-len(name))*' '+'| cin: '+cin.replace(" ","")+' | action: '+state+'\n')
        log.close()
    




    
#  /////////////////////////////////////////////////////////////////    -----  main program  ----- \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\






reader = SimpleMFRC522()
#print("starting script...")


# -----------------------------------     setting up the camera.
camera = picamera.PiCamera()
#camera.rotation = 180
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

while True:
    os.system('clear')
    print("waiting for card ...")
    id, text = reader.read()
    if os.path.isfile('DB/'+text.replace(" ","")+'.medmsw'):
        
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
            
        print("Capturing image.")
        camera.capture(output, format="rgb")
        
        
        print("encoding ...")
        face_locations = face_recognition.face_locations(output)
        face_encodings = face_recognition.face_encodings(output, face_locations)
        #print("encoded")
        print(len(face_locations))
        for face in face_encodings:
        
            # See if the face is a match for the known face(s)
            #print("before")
            match = face_recognition.compare_faces([DB_image], face)
            #print("after")
            state = "Unknown Person"
            print(match[0])
            if match[0]:
                #print("matching")
                state = "match"
               # log(text,name,state)
                if text.replace(" ","") == 'LA169308':
                    menu()
              #  AddClient()
            log(text,name,state)    
            print(state)
            sleep(2)            
    else:
        state = "unregisterd"
        print("this card is not registered in the database !")
        log('','',state)
        
        sleep(2)
        
