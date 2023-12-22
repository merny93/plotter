import os
from do_thing import start

while True:
    print("""---------------pen plotter---------------
Press enter key to draw art of yourself.

Smile for the camera! (photo is not stored).
Use flashlight for best results.
""", end="")
    test = input()
    try:
        start()
        os.system('gcode-cli one_line.gcode "/dev/ttyACM0,b250000"')
    except Exception as e:
        print("failed")
        print(e)
