**pyEye** 
---
pyEye (Pythonic Eye) is a library for facial visual changes detectoni such as blinking, eye direction, mouth states and more.

run the main.py file for instructions.

main.py takes 4 arguments:
* type of detection
* detection type option
* boolean video output
* STDOUT redirection to a com port

[-] for type blink
    [-] chose eithr: facePosition / leftEye / rightEye / twoEyes
    [-] set the video output to either: True / False
    [-] set redirect to COM to 0 for disable, 1-4 for relative com port

        [-] e.g pythom main.py blink rightEye False 0

[-] for type direction
    [-] chose eithr: leftEye / rightEye / twoEyes
    [-] set the video output to either: True / False
    [-] set the redirect to COM port ID if needed, if enabled, make sure to edit the config file

        [-] e.g pythom main.py direction rightEye False 0


IMPORTANT
---
make sure to *pip install -r requirements.txt*

redirecting STDOUT to a serial com port requires you to define the port in the config.py file.
run *main.py listCom* to get a list of all avilable com ports on your system.