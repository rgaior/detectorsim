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
import constant
import simulation
import detector
import waveform

dt = sys.argv[1]
method = int(sys.argv[2])
#temp, gain, bw, tau of power det
tsys=100
det = detector.Detector(temp=tsys,type=dt)
#det.loadspectrum()
sim = simulation.Simulation(det=det,sampling=5e9)
sim.producetime()
sim.producenoise()
#sim.producenoise(True)
#sine = utils.wf_sine(1.2e9, 1e-3, sim.time[1] - sim.time[0], sim.time[-1])
simwf = waveform.Waveform(sim.time,sim.noise, type='hf')
wf = det.producesimwaveform(simwf,'adc',method)
#wf = det.producesimwaveform(simwf,'powerdetector',method)

bw = 437e6
print 'rms = ',  np.std(wf.amp)
plt.plot(wf.time, wf.amp)
plt.show()
