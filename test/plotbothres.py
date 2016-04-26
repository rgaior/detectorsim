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

############################################################################
## perform the simulation of the power det and plot the difference with the measured data     ##
############################################################################

datafolder1 = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/NoCapa/'
basefileRF1 = datafolder1 + 'C110mVNoCapa000*'
basefilePD1 = datafolder1 + 'C210mVNoCapa000*'
resultfolder1 = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/nocapa/'

datafolder2 = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/Capa/'
basefileRF2 = datafolder2 + 'C110mVCapa000*'
basefilePD2 = datafolder2 + 'C210mVCapa000*'
resultfolder2 = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/capa/'


filesRF1 = glob.glob(basefileRF1)
filesPD1 = glob.glob(basefilePD1)
filesRF2 = glob.glob(basefileRF2)
filesPD2 = glob.glob(basefilePD2)
#result arrays
deltav1 = np.array([])
deltav2 = np.array([])

res1 = np.load(resultfolder1 + 'results.npz')
tau1 = res1['res'][0]
a1 = res1['res'][1]
b1 = res1['res'][2]

res2 = np.load(resultfolder2 + 'results.npz')
tau2 = res2['res'][0]
a2 = res2['res'][1]
b2 = res2['res'][2]

nroffiles = 19
#loop over files
for f1, f2 in zip(filesRF1[:nroffiles], filesPD1[:nroffiles]):
    wfRF = utils.readscopefile(f1)
    wfPD = utils.readscopefile(f2)
    conv = utils.produceresponse(wfRF[0],wfRF[1],tau1)
    real = wfPD[1]
    sim = conv[1]
        #resize the two waveforms to the same size (because of the convolution)
    [real,sim] = utils.resize(real,sim)
    time = utils.gettime(wfPD[0],conv[0])
    delay = utils.finddelay2(real,sim)
    simshifted =  np.roll(sim,delay)        
        #fit the conv vs power:
    polyconv_pd = np.poly1d([a1,b1])
    simpd = polyconv_pd(simshifted)        
    size = len(simpd)
    deltav1 = np.append(deltav1,simpd[size/4:-size/4] - real[size/4:-size/4])

#loop over files
for f1, f2 in zip(filesRF2[:nroffiles], filesPD2[:nroffiles]):
    wfRF = utils.readscopefile(f1)
    wfPD = utils.readscopefile(f2)
    conv = utils.produceresponse(wfRF[0],wfRF[1],tau2)
    real = wfPD[1]
    sim = conv[1]
        #resize the two waveforms to the same size (because of the convolution)
    [real,sim] = utils.resize(real,sim)
    time = utils.gettime(wfPD[0],conv[0])
    delay = utils.finddelay2(real,sim)
    simshifted =  np.roll(sim,delay)        
        #fit the conv vs power:
    polyconv_pd = np.poly1d([a2,b2])
    simpd = polyconv_pd(simshifted)        
    size = len(simpd)
    deltav2 = np.append(deltav2,simpd[size/4:-size/4] - real[size/4:-size/4])

fig = plt.figure()
ax = plt.subplot(111)
bins = np.linspace(-0.2,0.2,100)
c1,b1,p1 = plt.hist(deltav1,bins=bins,histtype='step', lw=3, normed=False,alpha=0.75,log=True,label='no capacitor')
c2,b2,p2 = ax.hist(deltav2,bins=bins,histtype='step', lw=3,  normed=False,alpha=0.75,log=True,label='with capacitor')
ax.text(0.01, 0.95, 'mean = ' + str("%.3f" % np.mean(deltav1))+ '\n std = ' + str("%.3f" % np.std(deltav1)),
        verticalalignment='top', horizontalalignment='left',
        transform=ax.transAxes,
        color='blue', fontsize=15)
ax.text(0.01, 0.85, 'mean = ' + str("%.3f" % np.mean(deltav2))+ '\n std = ' + str("%.3f" % np.std(deltav2)),
        verticalalignment='top', horizontalalignment='left',
        transform=ax.transAxes,
        color='green', fontsize=15)

plt.xlabel('V_sim - V_meas')
plt.legend()
plt.show()