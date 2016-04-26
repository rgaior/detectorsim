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

#dets = ['gi','dmx','norsat','realspec']
#dets = ['gi','dmx','norsat']
#dets = ['norsat']
dets = ['gi']
tsys = 50
gain = 1e6
#f1 = 0.95e9
f1 = 1.3e9
f2 = 1.75e9
deltaf = f2- f1
taus = np.linspace(1e-9,100e-9,10)
#taus = np.linspace(1e-9,100e-9,10)
#taus = np.linspace(1e-9,100e-9,10)
#taus = np.linspace(1,100e-9,100)
iter = 1
for dt in dets:
    rms = np.array([])
    errrms = np.array([])    
    for t in  taus:
        rms_temp = np.array([])
        for i in range(iter):
            det = detector.Detector(tsys, gain, f1, f2, t,type=dt)
            det.loadspectrum()
            sim = simulation.Simulation(det=det,sampling=5e9)
#            sim = simulation.Simulation(det=det,sampling=8e9)
            sim.producetime()
#            sim.producenoise()
            sim.producenoise(True)
            simwf = waveform.Waveform(sim.time,sim.noise, type='hf')
#            plt.plot(simwf.time,simwf.amp)
            wf = det.producesimwaveform(simwf,'adc')
            rms_temp = np.append(rms_temp,np.std(wf.amp))
        rms = np.append(rms,np.mean(rms_temp))
        errrms = np.append(errrms,np.std(rms_temp))
    plt.errorbar(taus*1e9,rms,yerr=errrms,label=dt)
plt.legend()
plt.xlabel('tau [ns]')
plt.ylabel('std (adc trace)')
plt.show()
#print np.std(wf.amp)

#plt.xlabel('delta f [MHz]')
#plt.legend()
#plt.show()
