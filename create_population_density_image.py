import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from pathlib import Path

module_path = Path(__file__).parent.as_posix()
sys.path.append(module_path)
from GPW_Pane_class import GPW_Pane

def load_GPW_data():
    """
    Loads population density data stored in .npy files and bundles it with header data extracted from a corresponding ASCII file
    
    Returns:
        panes (list): A list of GPW_Pane objects, which themselves contain gridded population data and associated metadata for each octant of the world
    """
    
    #Creates a list of ASCII filenames and .npy filesnames to loop through
    path = Path(module_path, 'Gridded ASCII Data')
    ascii_files = [f for f in os.listdir(path) if f.endswith('.asc')]
    npy_files = [f for f in os.listdir(path) if f.endswith('.npy')]
    
    #Loads a numpy array of gridded population data from the ith .npy file
    #and header data from the ith ASCII file and bundles them into a GPW_Pane object
    panes = []
    for i in range(8):
        print('Loading pane {}'.format(i+1))
        pane = np.load(Path(path, npy_files[i]))
        
        with open(Path(path, ascii_files[i])) as f:
            header = dict(next(f).split() for i in range(6))
        
        panes.append(GPW_Pane(pane, header))
    
    return panes
        
def stitch_grid_together(panes):
    """
    Stitches together gridded population data from all eight octants of the globe into one large array of the whole world
    
    Args:
        panes (list):A list of GPW_Pane objects, which themselves contain gridded population data and associated metadata for each octant of the world
        
    Returns:
        stitched_array (ndarray): A numpy array containing gridded population data of the whole world at 1/120 degree resolution in both lat and long
    """
    
    #Preallocate a contiguous block of memory for speed
    stitched_array = np.zeros([21600, 43200], dtype = np.float16)
    
    #Each pane is 10800 x 10800 elements. Panes are arranged as shown on page 13 of the documentation found here:
    #http://sedac.ciesin.columbia.edu/binaries/web/sedac/collections/gpw-v4/gpw-v4-documentation-rev11.pdf
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

#Ensure that all elements are non-negative
if not (stitched_array[stitched_array < 0].size == 0):
    stitched_array[stitched_array < 0] = 0
    
#Data will be grouped into one of six categories, as defined here:
#http://sedac.ciesin.columbia.edu/downloads/maps/gpw-v4/gpw-v4-population-density-rev11/gpw-v4-population-density-rev11-global-2020.pdf
#The exact population densities are not of interest, we will bin them and assign each bin an intensity for visualization purposes
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

assert(np.max(stitched_array) == 1.0), 'The normalized matrix should have maximum value 1'
assert(np.min(stitched_array) == 0.0), 'The normalized matrix should have minimum value 0'

#Rescale array values to 0-255 for plotting and display the image
im = np.uint8(stitched_array*255)
plt.imshow(im, cmap='gray')
plt.show()