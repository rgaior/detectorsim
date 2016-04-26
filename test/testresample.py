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


iter = 1
rms = np.array([])
errrms = np.array([])    
distg = np.array([])
distd = np.array([])
distn = np.array([])
det = detector.Detector(tsys, gain, f1, f2,0,type='gi')
det.loadspectrum()
sim = simulation.Simulation(det=det,sampling=5e9)
sim.producetime()
sim.producenoise(True)
[t,a] = utils.resample(sim.time,sim.noise,10e9)

#plt.plot(sim.time,sim.noise,'.')
#plt.plot(t,a)
fft1 = np.fft.rfft(sim.noise)
fft2 = np.fft.rfft(a)

freq1 = np.fft.rfftfreq(len(sim.noise),sim.time[1] - sim.time[0])
freq2 = np.fft.rfftfreq(len(a),t[1] - t[0])

plt.plot(freq1,np.absolute(fft1))
plt.plot(freq2,np.absolute(fft2))


plt.show()
