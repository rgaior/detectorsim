############################################################################
## for one waveform, produce the simulation of the power detector         ##
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
import simulation
import detector
import waveform

wfnr = '00'
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/Capa/'
datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/NoCapa/'
## for easier7
#taus = np.arange(5e-9,100e-9,10e-9)
## for easier61
resultfile = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/nocapa/results.npz'
res = np.load(resultfile)
tau = res['res'][0]
a = res['res'][1]
b = res['res'][2]
print 'tau = ', tau, ' a = ', a, ' b = ', b
fileRF = datafolder + 'C110mVNoCapa000' + wfnr + '.txt'
filePD = datafolder + 'C210mVNoCapa000' + wfnr + '.txt'
#result arrays
restau = np.array([])
resa = np.array([])
resb = np.array([])
#save folder
#resultfolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/nocapa/results.npz'
count = 0
#loop over files
wfRF = utils.readscopefile(fileRF)
wfPD = utils.readscopefile(filePD)
conv = utils.produceresponse(wfRF[0],wfRF[1],tau)
real = wfPD[1]
sim = conv[1]
        #resize the two waveforms to the same size (because of the convolution)
[real,sim] = utils.resize(real,sim)
time = utils.gettime(wfPD[0],conv[0])
delay = utils.finddelay2(real,sim)
simshifted =  np.roll(sim,delay)
        #fit the conv vs power:
polyconv_pd = np.poly1d([a,b])
simpd = polyconv_pd(simshifted)        

xlim = 500
#fig = plt.figure(figsize=(12,8))
plt.subplot(211)
plt.plot(wfRF[0]*1e9,wfRF[1])
plt.ylabel('RF (after antenna) [V]')
plt.xlim(-xlim,xlim)
plt.subplot(212)
plt.plot(wfPD[0]*1e9,wfPD[1],label='measured')
plt.plot(time*1e9,simpd,label='simulated')
plt.xlim(-xlim,xlim)
plt.ylabel('power detector [V]')
plt.xlabel('time [ns]')
plt.legend()
plt.show()

