# Makelangelo 5 Control Software

Only usable on Linux. Tested to not work on Mac due to C library failures.

We use the [gcode-cli](https://github.com/hzeller/gcode-cli) to send commands to the plotter. Note that this library only works on Linux, as [this error occurs with the C librares on Mac](https://github.com/hzeller/gcode-cli/issues/7).

You can try out the sinusoid portrait generation code with a UI at [mitxela.com/plotterfun/](https://mitxela.com/plotterfun/) -- we use a different backend codebase but it will give you an idea of what the final product will look like.

Makelangelo uses 250K baud rate and the Java code doesn't function/compile well on different platforms, nor is it interoperable with other software easily. We found sending gcode commands manually is far easier when combining it with your own code.

This code will take a photo of the user, then convert it to grayscale with 1.5x brightness (due to the low light) then an SVG, then a sinusoidal approximation that's easier to draw with gcode, then gcode to the plotter via the gcode CLI. Note there are some Makelangelo specific commands like pen up and pen down.

## Setup

Find your port for your Makelangelo via

```
ls /dev/tty*
lsusb
# Set the below to your found port
sudo chmod 777 /dev/ttyACM0
```

Setup dependencies via
```
pip install -r requirements.txt
chmod +x RUNME.sh
sudo usermod -a -G dialout $USER
```

Then run either via `./RUNME.sh` or `python3 main.py`.

