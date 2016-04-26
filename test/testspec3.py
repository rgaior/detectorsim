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

datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/NoCapa/'
filenameRF = 'C110mVNoCapa00000.txt'
wfRF = utils.readscopefile(datafolder+filenameRF)

tsys = 50
gain = 1e6
f1 = 0.95e9
f2 = 1.75e9
deltaf = f2- f1
taus = np.linspace(1e-9,20e-9,5)
#taus = np.linspace(1,100e-9,100)
iter = 1
rms = np.array([])
errrms = np.array([])
for t in  taus:
    rms_temp = np.array([])
    for i in range(iter):
        det = detector.Detector(tsys, gain, f1, f2, t)
#        det.loadspectrum()
        sim = simulation.Simulation(det=det,sampling=5e9)
#            sim = simulation.Simulation(det=det,sampling=8e9)
        sim.noise = wfRF[1]
        sim.time = wfRF[0]
        simwf = waveform.Waveform(sim.time,sim.noise, type='hf')
        wf = det.producesimwaveform(simwf,'adc')
        rms_temp = np.append(rms_temp,np.std(wf.amp[:2000]))
        print rms_temp
    rms = np.append(rms,np.mean(rms_temp))
    errrms = np.append(errrms,np.std(rms_temp))
#    count,bins,patch = plt.hist(wf.amp)
    plt.plot(wf.time, wf.amp)
#plt.errorbar(taus*1e9,rms,yerr=errrms)
plt.legend()
plt.xlabel('tau [ns]')
plt.ylabel('std (adc trace)')
plt.show()
#print np.std(wf.amp)

#plt.xlabel('delta f [MHz]')
#plt.legend()
#plt.show()
