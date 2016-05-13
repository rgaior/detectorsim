############################################################################
## test one of the method (to put in argument), plot the real and sim     ##
##  waveform and the distributions                                        ##
############################################################################
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)
from matplotlib import gridspec
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
    resultfolder = constant.resultfolder + '/residuals/nocapa/'
if capaornot == 'capa':
    datafolder = constant.calibdatafolder + '2013_05_10/Capa/'
    basefileRF = datafolder + 'C110mVCapa000*'
    basefilePD = datafolder + 'C210mVCapa000*'
    resultfolder = constant.resultfolder + '/residuals/capa/'
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
file = 2
diff = np.array([])
exrf = np.array([])
ex1 = np.array([])
ex2 = np.array([])
extime = np.array([])
#fcount = file
#for f1, f2 in zip(filesRF[file:file+1], filesPD[file:file+1]):
fcount = 0
for f1, f2 in zip(filesRF, filesPD):
#for f1, f2 in zip(filesRF[:10], filesPD[:10]):
    wfRF = utils.readscopefile(f1)
    wfPD = utils.readscopefile(f2)
    sim = simulation.Simulation(det=det,sampling=5e9)
    sim.time = wfRF[0]
    sim.noise = wfRF[1]
    simwf = waveform.Waveform(sim.time,sim.noise, type='hf')    
    wf = det.producesimwaveform(simwf,'powerdetector',method)
    [amp1, amp2]= utils.alignwaveform2(wfPD[1],wf.amp)
    [time1, time2] = utils.gettime(wfPD[0],wf.time)
    realwf = waveform.Waveform(wfPD[0],wfPD[1],type='powerdet')
    acamp1 = amp1 - np.mean(amp1)
    acamp2 = amp2 - np.mean(amp2)
    size1 = len(acamp1)
    portion = int(size1/5)
    acamp1 = acamp1[portion:-portion]
    acamp2 = acamp2[portion:-portion]
    diff = np.append(diff,acamp2-acamp1)
    if fcount == file:
        exrf = wfRF[1]
        timerf = wfRF[0]
        ex1 = acamp1
        ex2 = acamp2
        extime = time1[portion:-portion]
    fcount+=1
fig1 = plt.figure(figsize=(10,8))
gs = gridspec.GridSpec(3, 1, height_ratios=[2,2,1]) 
ax1 = plt.subplot(gs[0])
plt.setp(ax1.get_xticklabels(), visible=False)
ax1.plot(timerf*1e6,exrf)
ax1.set_ylabel('RF signal [V]')
ax1.set_xlim(-1,1)
#ax2.plot(realwf.time/1e6,realwf.amp,label='measured')
#ax2.plot(wf.time/1e6,amp2,lw=2,label='simulated')
ax2 = plt.subplot(gs[1],sharex=ax1)
ax2.plot(extime*1e6, ex1,label='measured')
ax2.plot(extime*1e6, ex2,'r-',lw=1,label='simulated')
ax2.set_ylabel('power detector [V]')
ax2.set_xlim(-1,1)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.legend()
ax3 = plt.subplot(gs[2],sharex=ax1)
ax3.set_ylabel('difference: \n sim - meas [V]')
ax3.set_xlabel('time [us]')
ax3.set_xlim(-1,1)

ax3.plot(extime*1e6, ex2 - ex1,'k',lw=1,label='difference')

np.savez(resultfolder+'dist'+capaornot+'_'+str(method),diff)
bins = np.linspace(-0.5,0.5,100)
fig2 = plt.figure()
#plt.hist(realwf.amp - np.mean(realwf.amp),bins=bins,histtype='step',normed=True,log=True)
#plt.hist(wf.amp- np.mean(wf.amp),bins=bins,histtype='step',normed=True,log=True)
plt.hist(diff,bins=bins,histtype='step',normed=True,log=True)
print 'std of diff = ', np.std(diff)
plt.show()
