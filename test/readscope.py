import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)
import numpy as np
import os
import sys
cwd = os.getcwd()
classpath = cwd + '/../classes/'
utilspath = cwd + '/../utils/'
sys.path.append(utilspath)
sys.path.append(classpath)
import utils
import simulation
import detector
import waveform
#temp, gain, bw, tau of power det
datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/Capa/'
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/NoCapa/'
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_03_25/HF_box/'
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_03_25/calib_board/'
#filenameRF = 'C1pdboard200mV00002.txt'
#filenamePD = 'C2pdboard200mV00002.txt'
#filenameRF = 'C1hf10mVbox200mV00002.txt'
#filenamePD = 'C2hf10mVbox200mV00002.txt'
#filenameRF = 'C110mVNoCapa00017.txt'
#filenamePD = 'C210mVNoCapa00017.txt'
filenameRF = 'C110mVCapa00014.txt'
filenamePD = 'C210mVCapa00014.txt'

#filenameRF = 'C1hf10mVbox200mV00013.txt'
#filenamePD = 'C2hf10mVbox200mV00013.txt'
wfRF = utils.readscopefile(datafolder+filenameRF)
wfPD = utils.readscopefile(datafolder+filenamePD)
plt.subplot(211)
plt.plot(1e9*wfRF[0],wfRF[1])
plt.xlim(np.min(1e9*wfPD[0]), np.max(1e9*wfPD[0]) )
plt.ylabel('power detector [V]')
#plt.ylabel('RF (after antenna) [V]')
plt.subplot(212)
plt.plot(1e9*wfPD[0],wfPD[1],'g')
plt.xlim(np.min(1e9*wfPD[0]), np.max(1e9*wfPD[0]) )
plt.ylabel('EASIER board [V]')
#plt.ylabel('power detector [V]')
plt.xlabel('time [ns]')
plt.show()

