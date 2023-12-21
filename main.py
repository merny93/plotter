import os

while True:
    print("press enter key to draw art")
    test = input()
    try:
        os.system("python3 do_thing.py | ./gcode-cli - /dev/tty,250000")
    except Exception as e:
        print("failed")
        print(e)
