import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)
import numpy as np
import os
import sys
import glob
cwd = os.getcwd()
classpath = cwd + '/../classes/'
utilspath = cwd + '/../utils/'
sys.path.append(utilspath)
sys.path.append(classpath)
import utils


capaornot = sys.argv[1]

if capaornot == 'nocapa':
    resultfolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/nocapa/'
if capaornot == 'capa':
    resultfolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/capa/'


files = glob.glob(resultfolder + 'distance*')
print files
for f in files:
    data = np.load(f)
    taus = data['tau']
    dist = data['dist']
    
    plt.plot(taus,dist)
plt.show()

