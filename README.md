# Facelock
This project is an implementation of facial recognition as a security feature as well as the conventional RFID capability in a Raspberry pi 3 B+ (Not tested on other versions).the Script has been developed o build a door lock security system that can recognize the person holding the Identification card (mifare classic 1K) and authenticate the access based on the facial features of the ID owner that is stored in the database.</br>
It's based on Python face recognition library: https://github.com/ageitgey/face_recognition
<h5>some Details</h5>

facelock</br>
|</br>
|---- main.py</br>
|</br>
|---- /DB</br>

the /DB folder is the database folder whre every entry is been saved as binary file (created with pickle python library) named with the ID number of the user.
