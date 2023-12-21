from PIL import Image
import numpy as np
from scipy.interpolate import interp1d
from itertools import cycle
import cv2 
# from pathlib import Path

cam = cv2.VideoCapture(0) 
  
# # reading the input using the camera 
result, image = cam.read()
if not result:
    print("no webcam sad")
img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
img = Image.fromarray(img)
#img = Image.open('samples/stars.jpg')
img = img.resize([254,254])
img_bw = 255 - np.mean(img, axis = -1)
n_lines = 30

lines = img_bw[:n_lines *int(img_bw.shape[0]/n_lines) , :].reshape(n_lines, int(img_bw.shape[0]/n_lines), img_bw.shape[1])
lines = np.mean(lines/np.max(lines), axis=1)
print(lines.shape)

t = np.linspace(0,1, 1000)
lines_interp = interp1d(np.linspace(0,1, lines.shape[1]), lines, axis = 1)
lines = lines_interp(t)
print(lines.shape)
# exit()

fc = 10
b = 0.05
phi = fc*t + b * np.cumsum(lines, axis = 1)



line_vals = np.sin(2*np.pi * phi)*lines/n_lines/1.5/ (img_bw.shape[0]/img_bw.shape[1])
line_vals = line_vals + np.linspace(0,img_bw.shape[0]/img_bw.shape[1], n_lines)[:,np.newaxis]
line_vals = 1 - line_vals
print(line_vals.shape)
# [plt.plot(t,v) for v in line_vals]
# plt.show()
drawing = np.concatenate([np.vstack((t[::dir], v[::dir])).T for v, dir in zip(line_vals, cycle([1,-1]))])


drawing = [drawing,]

def gcode(code, comment = "", **args):
    '''print code followd by kwargs'''
    arg_list = []
    for arg, value in args.items():
        arg_list.append(f"{arg}{value:.5g}")
    return f'{code} {" ".join(arg_list)}; ({comment})\n'



SCALE_FACTOR = 300
XY_OFFSET = np.array([-150,-200])
G_CODE_FILE = "one_line.gcode"
PD_COMMAND = gcode("M400", comment="wait for current move finish") + gcode("M280", comment="pen down", P=0, S=10, T=50)
PU_COMMAND = gcode("M400", comment="wait for current move finish") + gcode("M280", comment="pen up",  P=0, S=90, T=50)
FEEDRATE = 1000
RAPID = 3600
HEADER = '''(The Follwoing gcode was generated by the line_painter program)
M280 P0 S90 T50; (pen up for safety)
G4 S1; (wait for pen)
G21; (metric)
G28; (home)
M280 P0 S90 T50; (pen up for safety)


'''



with open(G_CODE_FILE, "w") as f:
    f.write(HEADER)
    # f.write(f"(This will use pen {color_name})\n\n")

    for line in drawing:
        line *= SCALE_FACTOR
        line += XY_OFFSET
        f.write(gcode("G0", X=line[0,0], Y=line[0,1], F=RAPID))
        f.write(PD_COMMAND)
        for point in line[1:]:
            f.write(gcode("G1", X=point[0], Y=point[1], F=FEEDRATE))
        f.write(PU_COMMAND)
    f.write(gcode("G0", X=0, Y=0, F=RAPID))







print("done")
