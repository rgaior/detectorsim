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

dets = ['gi']
#dets = ['gi','dmx','norsat']
tsys = 50
gain = 1e6
#f1 = 0e9
f2 = 2e9
#deltaf = f2- f1
#taus = np.array([5e-9,50e-9])
taus = np.linspace(1e-9,300e-9,10)
#taus = np.linspace(1,100e-9,100)
f1a = np.linspace(0,1.8e9,3)
col = ['k','r','b']

iter = 3
fig = plt.figure(figsize=(8,6))
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)
 
for f1,c in zip(f1a,col):
    rms = np.array([])
    errrms = np.array([])    
    for t in  taus:
        print t
        rms_temp = np.array([])
        for i in range(iter):
            det = detector.Detector(tsys, gain, f1, f2, t)
#            det.loadspectrum()
            sim = simulation.Simulation(det=det,sampling=8e9)
            sim.producetime()
            sim.producenoise()
            simwf = waveform.Waveform(sim.time,sim.noise, type='hf')
            wf = det.producesimwaveform(simwf,'logresponse')
            linwf = utils.dbmtowatt(wf.amp)
            nbins = int(t*sim.sampling)            
            fact = 5
            rms_temp = np.append(rms_temp,np.std(linwf[fact*nbins:-fact*nbins])/np.mean(linwf[fact*nbins:-fact*nbins]))
#            print np.std(linwf)/np.mean(linwf)
#            plt.plot(wf.time,linwf)
        rms = np.append(rms,np.mean(rms_temp))
        errrms = np.append(errrms,np.std(rms_temp))
#    plt.errorbar(taus,rms,yerr=errrms,label=dt)
    thratio = np.sqrt(2)/np.sqrt( (f2-f1) *  taus)
    plt.plot(taus,rms/thratio)
    

plt.legend()
plt.show()
#print np.std(wf.amp)

#plt.xlabel('tau [ns]')
#plt.xlabel('delta f [MHz]')
#plt.ylabel('std (adc trace)')
#plt.legend()
#plt.show()
