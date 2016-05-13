########################################################
## produce waveform out of different types of spectra ##
## and draws the sigma/mu distribution                ##
########################################################

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
datafolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/data/noise/'
filenameRF = 'C1noise7mv00015.txt'
wfRF = utils.readscopefile(datafolder+filenameRF)

#temp, gain, bw, tau of power det
tsys = 10
tsys2 = 100
gain = 1
f1 = 1.0e9
f2=  f1+680e6
f2bis= f1+445e6
sampling=5e9
det = detector.Detector(tsys, gain, f1, f2,0,type='dmx')
det2 = detector.Detector(tsys2, gain, f1, f2bis,0,type='dmx')
file = 1

#fig1 = plt.figure(figsize=(10,8))
sim1 = simulation.Simulation(det=det,sampling=5e9)
sim1.producenoise()
sim1.producetime()

sim2 = simulation.Simulation(det=det2,sampling=5e9)
det2.loadspectrum()
sim2.producenoise(True)
sim2.producetime()

sim3 = simulation.Simulation(det=det2,sampling=5e9)
sim3.producenoise()
sim3.producetime()

# power0 = wfRF[1]
# power1 = sim1.noise
# power2 = sim2.noise
# power2 = sim3.noise

power0 = wfRF[1]**2/np.mean(wfRF[1]**2)
power1 = sim1.noise**2/np.mean(sim1.noise**2)
power2 = sim2.noise**2/np.mean(sim2.noise**2)
power3 = sim3.noise**2/np.mean(sim3.noise**2)

fcut = 100e6
filt0 = utils.lowpasshard(power0, 1/(wfRF[0][1] -wfRF[0][0]), fcut)
filt1 = utils.lowpasshard(power1, sampling, fcut)
filt2 = utils.lowpasshard(power2, sampling, fcut)
filt3 = utils.lowpasshard(power3, sampling, fcut)

#filt0 = power0
#filt1 = power1
#filt2 = power2

fft0 = np.fft.rfft(power0)
fft1 = np.fft.rfft(power1)
fft2 = np.fft.rfft(power2)
freq0 = np.fft.rfftfreq(len(power0),wfRF[0][1] - wfRF[0][0])
freq1 = np.fft.rfftfreq(len(power1),sim1.time[1] - sim1.time[0])
freq2 = np.fft.rfftfreq(len(power2),sim2.time[1] - sim2.time[0])

fig = plt.figure(figsize=(10,6))
ax1 = plt.subplot(121)
ax1.plot(sim1.time,power1)
ax1.plot(sim2.time,power2)
#ax1.plot(sim2.time,power2)

ax2 = plt.subplot(122)
ax2.semilogy(freq0,np.absolute(fft0)/np.max(np.absolute(fft0)[1:]))
ax2.semilogy(freq1,np.absolute(fft1)/np.max(np.absolute(fft1)[1:]))
ax2.semilogy(freq2,0.5*np.absolute(fft2)/np.max(np.absolute(fft2)[1:]))
#ax2.set_ylim(1e-2,1.5)

print np.std(filt0)/np.mean(filt0)
print np.std(filt1)/np.mean(filt1)
print np.std(filt2)/np.mean(filt2)

fig2 = plt.figure()
bins = np.linspace(-2,10,100)
plt.hist(filt0,bins=bins,histtype='step',lw=2,log=True,normed=True,label='real spec: measured')
plt.hist(filt1,bins=bins,histtype='step',lw=2,log=True,normed=True,label='flat spec: voltage gain BW')
plt.hist(filt3,bins=bins,histtype='step',lw=2,log=True,normed=True,label='flat spec: power gain BW')
plt.hist(filt2,bins=bins,histtype='step',lw=2,log=True,normed=True,label='real spec: simulated ')
plt.legend()
plt.show()


