############################################################################
## for one waveform, produce the simulation of the power detector         ##
############################################################################
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
import simulation
import detector
import waveform

wfnr = '00'
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/Capa/'
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/NoCapa/'
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_03_25/HF_box/'
datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_03_25/HF_box_capa/'
fileRF = datafolder + 'C1hf10mVbox200mV000' + wfnr + '.txt'
filePD = datafolder + 'C2hf10mVbox200mV000' + wfnr + '.txt'

#save folder
#resultfolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/nocapa/results.npz'
count = 0
#loop over files
wfRF = utils.readscopefile(fileRF)
wfPD = utils.readscopefile(filePD)

tsys = 50
gain = 1
#f1 = 0.95e9
f1 = 1.3e9
f2 = 1.75e9
deltaf = f2- f1
#tau = 4.7e-9
tau = 35e-9

det = detector.Detector(tsys, gain, f1, f2, tau,type='gi')
sim = simulation.Simulation(det=det,sampling=5e9)
sim.noise = wfRF[1]
sim.time = wfRF[0]
simwf = waveform.Waveform(sim.time,sim.noise, type='hf')
print simwf.sampling
wf = det.producesimwaveform(simwf,'board')


gain2 = 1e6
det2 = detector.Detector(tsys, gain2, f1, f2,tau,type='gi')
sim2 = simulation.Simulation(det=det2,sampling=5e9)
det2.loadspectrum()
sim2.producetime()
sim2.producenoise(True)
detsimwf = waveform.Waveform(sim2.time,sim2.noise, type='hf')
detwf = det2.producesimwaveform(detsimwf,'board')
fr1 = np.fft.rfftfreq(len(sim.noise),sim.time[1] - sim.time[0])
fr2 = np.fft.rfftfreq(len(sim2.noise),sim2.time[1] - sim2.time[0])


print 'std meas = ' ,np.std(wfPD[1])
print 'std sim= ' ,np.std(wf.amp)
print 'std detsim= ' ,np.std(detwf.amp)
xlim = 500
#plt.subplot(211)
#plt.plot(wfPD[0]*1e9,wfPD[1])
#plt.plot(wf.time*1e9,wf.amp,label='sim')
#plt.plot(detwf.time*1e9,detwf.amp,label='detsim')
spec1 = np.absolute(np.fft.rfft(sim.noise))
spec2 = np.absolute(np.fft.rfft(sim2.noise))
plt.plot(fr1,spec1/np.max(spec1[10:-10]) )
plt.plot(fr2,spec2/np.max(spec2) )
#plt.plot(fr2, np.absolute(np.fft.rfft(sim2.noise)))
plt.show()

