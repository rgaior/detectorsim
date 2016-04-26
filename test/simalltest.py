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

fig1 = plt.figure()
axfft = plt.subplot()
iter = 1
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
#        sim = simulation.Simulation(det=det,sampling=8e9)
        sim.producetime()
        sim.producenoise(True)
        simwf = waveform.Waveform(sim.time,sim.noise, type='hf')
        wf = det.producesimwaveform(simwf,'adc')
        if dt == 'gi':
            distg = np.append(distg,wf.amp)
        if dt == 'dmx':
            distd = np.append(distd,wf.amp)
        if dt == 'norsat':
            distn = np.append(distn,wf.amp)
        fft = np.fft.rfft(sim.noise)
        pfft = np.fft.rfft(sim.noise*sim.noise)
        freq = np.fft.rfftfreq(len(sim.noise),sim.time[1] - sim.time[0])
#        axfft.plot(freq,np.absolute(fft))
        axfft.plot(freq,np.absolute(pfft))
        rms_temp = np.append(rms_temp,np.std(wf.amp))
    rms = np.append(rms,np.mean(rms_temp))
    errrms = np.append(errrms,np.std(rms_temp))


print '************************************'
print 'rms easier7 = ' , rms[0] , ' +- ', errrms[0]
print 'rms easier47 = ' , rms[1] , ' +- ', errrms[1] 
print 'rms gigaduck = ' , rms[2] , ' +- ', errrms[2]
print '************************************' 


# plt.errorbar(np.array([1,2,3]),rms,yerr=errrms,label=dt)
# plt.legend()
# #plt.xlabel('tau [ns]')
# plt.ylabel('std (adc trace)')

# fig = plt.figure()
# bins = 50
# c1,b1,p1 = plt.hist(distg,bins=bins,histtype='step', lw=3, normed=False,alpha=0.75,log=True,label='gi')

#np.savez('disteasier7',distg)
#np.savez('disteasier47',distd)
#np.savez('distgiga',distn)


# c2,b2,p2 = plt.hist(distd,bins=bins,histtype='step', lw=3, normed=False,alpha=0.75,log=True,label='dmx')
# c3,b3,p3 = plt.hist(distn,bins=bins,histtype='step', lw=3, normed=False,alpha=0.75,log=True,label='norsat')
plt.show()
#print np.std(wf.amp)

#plt.xlabel('delta f [MHz]')
#plt.legend()
#plt.show()