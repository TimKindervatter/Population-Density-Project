#%%
import os
from pathlib import Path
import time
import numpy as np

#%%
#Population data is split among 8 separate ASCII files, get a list of their names
module_path = Path(__file__).parent.as_posix()
path = Path(module_path, 'Gridded ASCII Data')
files = [f for f in os.listdir(path) if f.endswith('.asc')]

#%%
#Reading the ASCII files takes some time, we will store their data in .npy files for faster access later
for i in range(8):
    print('Reading file {} (this could take a minute)...'.format(i+1))
    t = time.time()
    pane = np.loadtxt(Path(path, files[i]), dtype=np.float16, skiprows=6) #First 6 rows are header lines, skip them
    elapsed = time.time() - t
    #Print a progress message to the user after the current file has been parsed
    print('File {0} processed, took {1} seconds\n'.format(i+1, elapsed))
    pane[(pane == -10000) | (pane == np.inf)] = 0
    #Save the numpy array in the same directory as the ASCII files
    np.save(Path(path, 'pane{}.npy'.format(i+1)), pane)

