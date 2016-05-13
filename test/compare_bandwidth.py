############################################################################
## test one of the method (to put in argument), plot the real and sim     ##
##  waveform and the distributions                                        ##
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
import constant
import simulation
import detector
import waveform


#temp, gain, bw, tau of power det
tsys = 10
tsys2 = 100
gain = 1
#f1 = 0.95e9
f1 = 1.0e9
#f2=  f1+438e6
#f2 = 1.75e9
f2 = 2.5e9
sampling=5e9
det = detector.Detector(tsys, gain, f1, f2,0,type='gi')
det2 = detector.Detector(tsys2, gain, f1, f2,0,type='gi')
file = 1

#fig1 = plt.figure(figsize=(10,8))
sim1 = simulation.Simulation(det=det,sampling=8e9)
sim1.producenoise()
sim1.producetime()

sim2 = simulation.Simulation(det=det2,sampling=8e9)
det2.loadspectrum()
sim2.producenoise(True)
sim2.producetime()


fcut = 100e6
filt1 = utils.lowpasshard(sim1.noise**2, sampling, fcut)
filt2 = utils.lowpasshard(sim2.noise**2, sampling, fcut)

#plt.hist(sim1.noise,bins=100,histtype='step')
#plt.hist(sim2.noise,bins=100,histtype='step')
#power1= sim1.noise**2
#power2= sim2.noise**2
#power1= filt1
#power2= filt2
power1= sim1.noise**2
power2= sim2.noise**2
print np.std(power1)/np.mean(power1)
print np.std(power2)/np.mean(power2)
min1 = np.min(power1)
min2 = np.min(power2)
max1 = np.max(power1)
max2 = np.max(power2)
min = np.min(np.array([min1,min2]))
max = np.max(np.array([max1,max2]))
bins = np.linspace(min,max,100)
plt.hist(power1,bins=bins,histtype='step',log=True,normed=True)
plt.hist(power2,bins=bins,histtype='step',log=True,normed=True)
print ' mean 1 = ' ,np.mean(power1)
print ' std 1 = ' ,np.std(power1)
print ' mean 2 = ' ,np.mean(power2)
print ' std 2 = ' ,np.std(power2)

plt.show()
