import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from pathlib import Path

module_path = Path(__file__).parent.as_posix()
sys.path.append(module_path)
from GPW_Pane_class import GPW_Pane

def load_GPW_data():
    path = Path(module_path, 'Gridded ASCII Data')
    ascii_files = [f for f in os.listdir(path) if f.endswith('.asc')]
    npy_files = [f for f in os.listdir(path) if f.endswith('.npy')]
    
    
    panes = []
    for i in range(8):
        print('Loading pane {}'.format(i+1))
        pane = np.load(Path(path, npy_files[i]))
        
        with open(Path(path, ascii_files[i])) as f:
            header = dict(next(f).split() for i in range(6))
        
        panes.append(GPW_Pane(pane, header))
    
    return panes
        
def stitch_grid_together(panes):
    stitched_array = np.zeros([21600, 43200], dtype = np.float16)
    
    pane_index = 0
    for j in range(2):
        rows = 10800
        for i in range(4):
            cols = 10800
            print('Pane index: {}'.format(pane_index+1))
            print('Row bounds: {}'.format((j*rows, (j+1)*rows)))
            print('Column bounds: {}'.format((i*rows, (i+1)*rows)))
            stitched_array[j*rows:(j+1)*rows, i*cols:(i+1)*cols] = panes[pane_index].grid
            pane_index += 1
    
    return stitched_array

panes = load_GPW_data()
stitched_array = stitch_grid_together(panes)

if not (stitched_array[stitched_array < 0].size == 0):
    stitched_array[stitched_array < 0] = 0
    
stitched_array[stitched_array <= 1] = 0
print('Category 1/6 assigned')
stitched_array[(stitched_array > 1) & (stitched_array <= 5)] = 0.2
print('Category 2/6 assigned')
stitched_array[(stitched_array > 5) & (stitched_array <= 25)] = 0.4
print('Category 3/6 assigned')
stitched_array[(stitched_array > 25) & (stitched_array <= 250)] = 0.6
print('Category 4/6 assigned')
stitched_array[(stitched_array > 250) & (stitched_array <= 1000)] = 0.8
print('Category 5/6 assigned')
stitched_array[stitched_array > 1000] = 1.0
print('Category 6/6 assigned')

#stitched_array /= np.nanmax(stitched_array)
#
assert(np.max(stitched_array) == 1.0), 'The normalized matrix should have maximum value 1'
assert(np.min(stitched_array) == 0.0), 'The normalized matrix should have minimum value 0'

im = np.uint8(stitched_array*255)
plt.imshow(im, cmap='gray')
plt.show()