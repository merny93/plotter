# Makelangelo 5 Control Software

Only usable on Linux. Tested to not work on Mac due to C library failures.

We use the [gcode-cli](https://github.com/hzeller/gcode-cli) to send commands to the plotter. Note that this library only works on Linux, as [this error occurs with the C librares on Mac](https://github.com/hzeller/gcode-cli/issues/7).

You can try out the sinusoid portrait generation code with a UI at (mitxela.com/plotterfun/)[https://mitxela.com/plotterfun/] -- we use a different backend codebase but it will give you an idea of what the final product will look like.

Makelangelo uses 250K baud rate and the Java code doesn't function/compile well on different platforms, nor is it interoperable with other software easily. So sending gcode commands manually is far easier when doing your own projects.

This code will take a photo of the user, then convert it to grayscale then an SVG, then a sinusoidal appproximation that's easier to draw with gcode, then gcode to the plotter via the gcode CLI. Note there are some Makelangelo specific commands like pen up and pen down.
