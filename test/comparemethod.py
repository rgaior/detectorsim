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


iter = 3
rms = np.array([])
rms2 = np.array([])
errrms = np.array([])    
distg = np.array([])
distd = np.array([])
distn = np.array([])
distg2 = np.array([])
distd2 = np.array([])
distn2 = np.array([])
for dt in dets:
    rms_temp = np.array([])
    rms_temp2 = np.array([])
    for i in range(iter):
        det = detector.Detector(tsys, gain, f1, f2,0,type=dt)
        det.loadspectrum()
        sim = simulation.Simulation(det=det,sampling=5e9)
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

        wf2 = det.producesimwaveform(simwf,'adc',1)
        if dt == 'gi':
            distg2 = np.append(distg2,wf2.amp)
        if dt == 'dmx':
            distd2 = np.append(distd2,wf2.amp)
        if dt == 'norsat':
            distn2 = np.append(distn,wf2.amp)
        rms_temp = np.append(rms_temp,np.std(wf.amp))
        rms_temp2 = np.append(rms_temp2,np.std(wf2.amp))
    rms = np.append(rms,np.mean(rms_temp))
    rms2 = np.append(rms2,np.mean(rms_temp2))
    errrms = np.append(errrms,np.std(rms_temp))


print '************************************'
print 'rms easier7 = ' , rms[0] , ' +- ', errrms[0]
print 'rms easier47 = ' , rms[1] , ' +- ', errrms[1] 
print 'rms gigaduck = ' , rms[2] , ' +- ', errrms[2]
print '************************************' 

print '************* method 2***********************'
print 'rms easier7 = ' , rms2[0] , ' +- ', errrms[0]
print 'rms easier47 = ' , rms2[1] , ' +- ', errrms[1] 
print 'rms gigaduck = ' , rms2[2] , ' +- ', errrms[2]
print '************************************' 


# plt.errorbar(np.array([1,2,3]),rms,yerr=errrms,label=dt)
# plt.legend()
# #plt.xlabel('tau [ns]')
# plt.ylabel('std (adc trace)')

# fig = plt.figure()
# bins = 50
# c1,b1,p1 = plt.hist(distg,bins=bins,histtype='step', lw=3, normed=False,alpha=0.75,log=True,label='gi')

# np.savez('disteasier7',distg)
# np.savez('disteasier47',distd)
# np.savez('distgiga',distn)


# c2,b2,p2 = plt.hist(distd,bins=bins,histtype='step', lw=3, normed=False,alpha=0.75,log=True,label='dmx')
# c3,b3,p3 = plt.hist(distn,bins=bins,histtype='step', lw=3, normed=False,alpha=0.75,log=True,label='norsat')

# plt.show()
#print np.std(wf.amp)

#plt.xlabel('delta f [MHz]')
#plt.legend()
#plt.show()