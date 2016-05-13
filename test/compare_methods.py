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

capaornot = sys.argv[1]
method = int(sys.argv[2])

if capaornot == 'nocapa':
    datafolder = constant.calibdatafolder + '2013_05_10/NoCapa/'
    basefileRF = datafolder + 'C110mVNoCapa000*'
    basefilePD = datafolder + 'C210mVNoCapa000*'
    dt = 'dmx'
if capaornot == 'capa':
    datafolder = constant.calibdatafolder + '2013_05_10/Capa/'
    basefileRF = datafolder + 'C110mVCapa000*'
    basefilePD = datafolder + 'C210mVCapa000*'
#     datafolder = constant.calibdatafolder + 'noise/'
#     basefileRF = datafolder + 'C1noise7mv000*'
#     basefilePD = datafolder + 'C2noise7mv000*'
    dt = 'gi'

#temp, gain, bw, tau of power det
tsys = 50
gain = 1
#f1 = 0.95e9
f1 = 1.3e9
f2 = 1.75e9

filesRF = glob.glob(basefileRF)
filesPD = glob.glob(basefilePD)
det = detector.Detector(tsys, gain, f1, f2,0,type=dt)
file = 1

#fig1 = plt.figure(figsize=(10,8))
f, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=False, sharey=False)
ax1 = plt.subplot(411)
ax2 = plt.subplot(412)
ax3 = plt.subplot(413)
ax4 = plt.subplot(414)

for met in [1,2,3]:
    fcount = 0
    diff = np.array([])
    ex1 = np.array([])
    ex2 = np.array([])
    extime = np.array([])
    exrf = np.array([])
    timerf = np.array([])
#for f1, f2 in zip(filesRF[file:file+1], filesPD[file:file+1]):
    for f1, f2 in zip(filesRF[:2], filesPD[:2]):
        print f1
        wfRF = utils.readscopefile(f1)
        wfPD = utils.readscopefile(f2)
        sim = simulation.Simulation(det=det,sampling=5e9)
        sim.time = wfRF[0]
        sim.noise = wfRF[1]
        simwf = waveform.Waveform(sim.time,sim.noise, type='hf')    
        wf = det.producesimwaveform(simwf,'powerdetector',met)
        
        print len(wfPD[1]), ' ', len(wf.amp)
        print len(sim.time), ' ', len(wf.time)
        #        [amp1, amp2]= utils.alignwaveform2(wf.amp,wfPD[1],False)
        [amp1, amp2]= utils.alignwaveform2(wfPD[1],wf.amp)
        [time1, time2] = utils.gettime(wf.time,wfPD[0])
        realwf = waveform.Waveform(wfPD[0],wfPD[1],type='powerdet')
        acamp1 = amp1 - np.mean(amp1)
        acamp2 = amp2 - np.mean(amp2)
        size1 = len(acamp1)
        acamp1 = acamp1[size1/5:-size1/5]
        acamp2 = acamp2[size1/5:-size1/5]
        diff = np.append(diff,acamp2-acamp1)
        if fcount == file:
            ex1 = acamp1
            ex2 = acamp2
            extime = time1[size1/5:-size1/5]*1e6
            if met == 1:
                exrf = wfRF[1]
                timerf = wfRF[0]*1e6
                ax1.plot(timerf,exrf)
        fcount +=1
    if met == 1:
        print extime
        ax2.plot(extime,ex1,label='measured')
        ax2.plot(extime,ex2,lw=2,label='simulated')
    if met == 2:
        ax3.plot(extime,ex1,label='measured')
        ax3.plot(extime,ex2,lw=2,label='simulated')
    if met == 3:
        ax4.plot(extime,ex1,label='measured')
        ax4.plot(extime,ex2,lw=2,label='simulated')
plt.legend()

bins = np.linspace(-0.5,0.5,100)
fig2 = plt.figure()
#plt.hist(realwf.amp - np.mean(realwf.amp),bins=bins,histtype='step',normed=True,log=True)
#plt.hist(wf.amp- np.mean(wf.amp),bins=bins,histtype='step',normed=True,log=True)
plt.hist(diff,bins=bins,histtype='step',normed=True,log=True)
print 'std of diff = ', np.std(diff)
plt.show()
