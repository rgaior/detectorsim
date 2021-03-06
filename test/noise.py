import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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



#temp, gain, bw, tau of power det
tsys = 50
gain = 1e6
f1 = 0
#f1 = 0.95e9
#f2 = 1.75e9
f2 = 2e9
tau = 5e-9
det = detector.Detector(tsys, gain, f1, f2, tau)

sim = simulation.Simulation(det=det, snr=10, siglength = 50e-9)

sim.producetime()
sim.producenoise()
#filt = utils.lowpasshard(sim.noise,sim.sampling,1e9)
#sim.noise =filt


# plt.subplot(311)
# plt.plot(sim.time, sim.noise)
# plt.subplot(312) 
# freq= np.fft.rfftfreq(len(sim.time),sim.time[1]-sim.time[0])
# fft = np.fft.rfft(sim.noise)
# plt.plot(freq,np.absolute(fft))
# plt.subplot(313)
# plt.plot(freq,np.arctan2(fft.imag,fft.real))
# plt.show()

fig1 = plt.figure(figsize = (8,8))
ax1 = plt.subplot2grid((2,2), (0,0), colspan=2)
ax2 = plt.subplot2grid((2,2), (1,0))
ax3 = plt.subplot2grid((2,2), (1,1))

ax1.plot(sim.time*1e6, sim.noise)
ax1.set_xlabel('time [us]',fontsize =15)
ax1.set_ylabel('amplitude [V]',fontsize =15)
n, bins, patches = ax2.hist(sim.noise, 50, facecolor='green', alpha=0.75)
#ax2.xaxis.set_major_locator(ticker.MultipleLocator( (np.max(sim.noise) -np.min(sim.noise))/2))
ax2.ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
ax2.set_xlabel('amplitude [V]',fontsize =15)
ax2.set_ylabel('entries',fontsize =15)
mvnoise = np.mean(sim.noise)
stdvnoise = np.std(sim.noise)
pnoise = sim.noise*sim.noise/50
n1, bins1, patches1 = ax3.hist(pnoise, 50, facecolor='red', alpha=0.75)
ax3.set_xlabel('power [W]',fontsize =15)
#ax3.set_ylabel('entries',fontsize =15)
mpnoise = np.mean(pnoise)
stdpnoise = np.std(pnoise)
print 'ratio = ' ,stdpnoise/mpnoise
ax1.text(0.95, 0.90, 'Tsys = '+ str("%.2f" % tsys) + ' K',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax1.transAxes,
        color='black', fontsize=15)
ax2.text(0.95, 0.90, 'mean = '+ str("%.2g" % mvnoise),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax2.transAxes,
        color='black', fontsize=12)
ax2.text(0.95, 0.85, 'std = '+ str("%.2g" % stdvnoise),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax2.transAxes,
        color='black', fontsize=12)
ax3.text(0.95, 0.90, 'mean = '+ str("%.2g" % mpnoise),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax3.transAxes,
        color='black', fontsize=12)
ax3.text(0.95, 0.85, 'std = '+  str("%.2g" % stdpnoise),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax3.transAxes,
        color='black', fontsize=12)

fft = np.fft.rfft(sim.noise)
freq = np.fft.rfftfreq(len(sim.noise), sim.time[1] - sim.time[0])

fig2 = plt.figure(figsize=(8,8))
ax21 = plt.subplot(211)
ax21.plot(freq/1e6,np.absolute(fft))
ax21.set_ylabel('spectrum [a.u.]')
ax22 = plt.subplot(212, sharex=ax21)
ax22.plot(freq/1e6,np.angle(fft))
ax22.set_ylabel('phase [radian]')
ax22.set_xlabel('frequency [MHz]')
#stdvnoise = np.std(sim.noise)
# plt.xlabel('power at installation [dBm]', fontsize =15)
# plt.ylabel('entries',fontsize = 15)
# plt.legend(fontsize=15)


plt.show()
