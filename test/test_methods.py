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
for f1, f2 in zip(filesRF[file:file+1], filesPD[file:file+1]):
#for f1, f2 in zip(filesRF, filesPD):
    print f1
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

fig1 = plt.figure(figsize=(10,8))
ax1 = plt.subplot(211)
ax1.plot(wfRF[0],wfRF[1])
ax2 = plt.subplot(212)
ax2.plot(realwf.time/1e6,realwf.amp,label='measured')
ax2.plot(time2/1e6,amp2,lw=2,label='simulated')
plt.legend()

bins = np.linspace(-0.5,0.5,100)
fig2 = plt.figure()
plt.hist(realwf.amp- np.mean(realwf.amp),bins=bins,histtype='step',normed=True,log=True)
plt.hist(wf.amp- np.mean(wf.amp),bins=bins,histtype='step',normed=True,log=True)

plt.show()
