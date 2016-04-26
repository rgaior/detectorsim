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
import simulation
import detector
import waveform
#temp, gain, bw, tau of power det
datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_03_25/calib_board/'
filename1 = 'C1hf10mVbox200mV00002.txt'
filename2 = 'C2hf10mVbox200mV00002.txt'
files1 = glob.glob(datafolder+'C1pdboard200*')
files2 = glob.glob(datafolder+'C2pdboard200*')

tsys = 50
gain = 1e6
f1 = 0.95e9
f2 = 1.75e9
det = detector.Detector(tsys, gain, f1, f2, 5e-9)
deltav1 = np.array([])
deltav2 = np.array([])
#for f1,f2 in zip(files1,files2):
for f1,f2 in zip(files1[:1],files2[:1]):
#for f1,f2 in zip(files1[::5],files2[::5]):
    wf1 = utils.readscopefile(f1)
    wf2 = utils.readscopefile(f2)
    [pd,board] = utils.resize(wf1[1],wf2[1])
    time = utils.gettime(wf1[0],wf2[0])
    delay = utils.finddelay2(pd,board)
    board =  np.roll(board,delay)        

    realpd = simulation.Simulation(det=det,sampling=5e9)
    realpd.noise = pd
    realpd.time = time
    realpdwf = waveform.Waveform(realpd.time,realpd.noise, type='powerdetector')
    
    realboard = simulation.Simulation(det=det,sampling=5e9)
    realboard.noise = board
    realboard.time = time
    realboardwf = waveform.Waveform(realboard.time,realboard.noise, type='board')
    
    simboard = simulation.Simulation(det=det,sampling=5e9)
    simboard.noise = pd
    simboard.time = time
#    simboard = waveform.Waveform(simboard.time,simboard.noise, type='powerdetector')
    simboardwf = det.adaptationboard(realpdwf)
    simboardwf2 = det.adaptationboard2(realpdwf)
    deltav1 = np.append(deltav1,realboardwf.amp - simboardwf.amp)
    deltav2 = np.append(deltav2,realboardwf.amp[:-1] - simboardwf2.amp)

fig = plt.figure()
plt.plot(realboardwf.time*1e9,realboardwf.amp,label='measured')
plt.plot(simboardwf.time*1e9,simboardwf.amp,label='sim. (constant gain)')
plt.plot(simboardwf2.time[:-1]*1e9,simboardwf2.amp,label='sim (freq. dependent gain)')
plt.xlim(-100,100)
plt.ylim(-1.6,-0.6)
plt.xlabel('time [ns]')
plt.ylabel('EASIER board [V]')
plt.legend()


# fig2 = plt.figure()
# ax = plt.subplot(111)
# bins = np.linspace(-0.5,0.5,100)
# c1,b1,p1 = plt.hist(deltav1,bins=bins,histtype='step', lw=3,color='g', normed=False,alpha=0.75,log=True,label='constant gain')
# c2,b2,p2 = ax.hist(deltav2,bins=bins,histtype='step', lw=3,color='r',  normed=False,alpha=0.75,log=True,label='freq. dependent gain')
# ax.text(0.01, 0.95, 'mean = ' + str("%.3f" % np.mean(deltav1))+ '\n std = ' + str("%.3f" % np.std(deltav1)),
#         verticalalignment='top', horizontalalignment='left',
#         transform=ax.transAxes,
#         color='green', fontsize=15)
# ax.text(0.01, 0.85, 'mean = ' + str("%.3f" % np.mean(deltav2))+ '\n std = ' + str("%.3f" % np.std(deltav2)),
#         verticalalignment='top', horizontalalignment='left',
#         transform=ax.transAxes,
#         color='red', fontsize=15)

# plt.xlabel('V_sim - V_meas')
# plt.legend()
# plt.show()

plt.show()
