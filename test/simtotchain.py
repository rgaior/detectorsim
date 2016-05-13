##################################################
## will do a simulation for the three detectors ##
## and save the distribution of ADC             ##
##################################################
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

dets = ['gi','dmx','norsat']
tsys = 50
gain = 1e6
#f1 = 0.95e9
f1 = 1.3e9
f2 = 1.75e9

method = int(sys.argv[1])
saveorplot = sys.argv[2]

iter = 50
rms = np.array([])
errrms = np.array([])    
distg = np.array([])
distd = np.array([])
distn = np.array([])
for dt in dets:
    rms_temp = np.array([])
    for i in range(iter):
        det = detector.Detector(tsys, gain, f1, f2,0,type=dt)
        det.loadspectrum()
        sim = simulation.Simulation(det=det,sampling=5e9)
        sim.producetime()
        sim.producenoise(True)
        simwf = waveform.Waveform(sim.time,sim.noise, type='hf')
        wf = det.producesimwaveform(simwf,'adc',method)
        if dt == 'gi':
            distg = np.append(distg,wf.amp)
        if dt == 'dmx':
            distd = np.append(distd,wf.amp)
        if dt == 'norsat':
            distn = np.append(distn,wf.amp)
        rms_temp = np.append(rms_temp,np.std(wf.amp))
    rms = np.append(rms,np.mean(rms_temp))
    errrms = np.append(errrms,np.std(rms_temp))


print '************************************'
print 'rms easier7 = ' , rms[0] , ' +- ', errrms[0]
print 'rms easier47 = ' , rms[1] , ' +- ', errrms[1] 
print 'rms gigaduck = ' , rms[2] , ' +- ', errrms[2]
print '************************************' 
if saveorplot == 'save':
    namebase = constant.resultfolder + 'rms/sim/m'+str(method)+'_'
    np.savez(namebase+'disteasier7',distg)
    np.savez(namebase+'disteasier47',distd)
    np.savez(namebase+'distgiga',distn)


if saveorplot == 'plot':
    plt.hist(distg,lw=2,histtype='step',label='easier7')
    plt.hist(distd,lw=2,histtype='step',label='easier61')
    plt.hist(distn,lw=2,histtype='step',label='gigaduck')
    plt.legend()
    plt.show()

