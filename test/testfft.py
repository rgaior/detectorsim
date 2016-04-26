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
tsys = 50
gain = 1e6
f1 = 0.95e9
f2 = 1.75e9
deltaf = f2- f1
iter = 1
det = detector.Detector(tsys, gain, f1, f2, 1,type='gi')
det.loadspectrum()
sim = simulation.Simulation(det=det,sampling=5e9)
sim.producetime()
sim.producenoise(True)
simwf = waveform.Waveform(sim.time,sim.noise, type='hf')

fft = np.fft.rfft(simwf.amp)
plt.plot(np.absolute(fft)/np.max(np.absolute(fft)))
plt.plot(np.absolute(fft)**2/np.max(np.absolute(fft)**2))


plt.show()
