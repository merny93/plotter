from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, rgb_to_hsv
from scipy.ndimage import gaussian_filter, laplace
from scipy.interpolate import interp1d
img = Image.open('samples/stars.jpg')
img = img.resize([254,254])
img = np.asarray(img)
print(img.dtype)
print(img.shape)
# plt.imshow(img)
# plt.show()


color_list = ["fb224f","faaf22","001398","d2b5ba","3c6509","15150a"]
# color_list = ["0c0b0a","faec25"]
color_list = list = ["F2C9D1", "F179AF", "FFDE98", "F6EA5E", "8ECFAB", "86D3DE", "209BC7", "95B5DF", "999ECF", "D0D2D4"]
def hex2rgb(hex_code):
    h = hex_code.lstrip('#')
    return np.array((tuple(int(h[i:i+2], 16) for i in (0, 2, 4))))
pallet_mapping = np.vstack([np.array(hex2rgb(c)) for c in color_list])

def split(arr, indecies, min_length=10):
    '''Like np.split but overlaps! with min length'''
    result = [] 
    prev = 0
    for idx in indecies:
        if idx-prev<min_length:
            #defer
            continue
        if idx + 1 >= arr.size-1 :
            result.append(arr[prev:])
        else:
            result.append(arr[prev:idx+1])
        prev = idx
    result.append(arr[prev:])
    return result


norm = np.linalg.norm

print(img.shape[:2])
color_distance = np.zeros((len(color_list),) + img.shape[:2] )
print(color_distance.shape)
for i,color in enumerate(color_list):
    color = hex2rgb(color)
    d = norm(img - color, axis=-1)
    d = gaussian_filter(d,1, )
    color_distance[i] = d
    print(d.shape)

color_region = np.argmin(color_distance, axis = 0)
# plt.imshow(color_region)
# plt.show()

# plt.imshow(color_region)
# plt.show()
img_bw = np.linalg.norm(img, axis = -1)
print(img_bw.shape)

n_lines = 25
lines = img_bw[:n_lines *int(img_bw.shape[0]/n_lines) , :].reshape(n_lines, int(img_bw.shape[0]/n_lines), img_bw.shape[1])
lines = np.mean(lines/np.max(lines), axis=1)
print(lines.shape)


t = np.linspace(0,1, 1000)
lines_interp = interp1d(np.linspace(0,1, lines.shape[1]), lines, axis = 1)
lines = lines_interp(t)
print(lines.shape)
# exit()

fc = 20
b = 0.2
phi = fc*t + b * np.cumsum(lines, axis = 1)



line_vals = np.sin(2*np.pi * phi)*lines/n_lines/1.5/ (img_bw.shape[0]/img_bw.shape[1])
line_vals = line_vals + np.linspace(0,img_bw.shape[0]/img_bw.shape[1], n_lines)[:,np.newaxis]

drawing={"#" + color_name: [] for color_name in color_list}

plt.clf()

for line in line_vals:
    u = np.clip(np.round(t*(color_region.shape[0]-1)).astype(int), 0, color_region.shape[0]-1)
    v = np.clip(np.round(line*(color_region.shape[1]-1)).astype(int),0,  color_region.shape[1]-1   )
    line_color = color_region.T[u,v]
    color_changes = np.argwhere(np.diff(line_color)).reshape(-1)
    # print(color_changes.shape)
    sections = split(line,color_changes)
    t_sections = split(t, color_changes)
    color_sections = split(line_color, color_changes)

    for t_bit, section, color in zip(t_sections,sections, color_sections):
        

        try:
            c = "#"+color_list[int(np.median(color))]
        except Exception as e:
            print(e)
            print(t_bit)
            continue
        previous_color = c
        plt.plot(t_bit, 1-section, c=c)
        drawing[c].append(np.stack((t_bit, 1-section)).T)
    # print("hello")

import pickle

with open("out.bin", "wb") as f:
    pickle.dump(drawing, f)


print("done")
plt.show()