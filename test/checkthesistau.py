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
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/Capa/'
datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/NoCapa/'
#filenameRF = 'C110mVCapa00001.txt'
#filenamePD = 'C210mVCapa00001.txt'
filenameRF = 'C110mVNoCapa00001.txt'
filenamePD = 'C210mVNoCapa00001.txt'
#taus = np.arange(5e-9,100e-9,10e-9)
taus = np.arange(3e-9,7e-9,0.2e-9)
basefileRF = datafolder + 'C110mVNoCapa000'
basefilePD = datafolder + 'C210mVNoCapa000'
filesRF = glob.glob(basefileRF)
filesPD = glob.glob(basefilePD)
restau = np.array([])
resa = np.array([])
resb = np.array([])
for f1, f2 in zip(filesRF, filesPD):
    mindist = 1e6
    dist = np.array([])
    besttau = 0
    besta = 0
    bestb = 0
    for t in taus:
        wfRF = utils.readscopefile(datafolder+filenameRF)
        wfPD = utils.readscopefile(datafolder+filenamePD)
        conv = utils.produceresponse(wfRF[0],wfRF[1],t)
        real = wfPD[1]
        sim = conv[1]
        [real,sim] = utils.resize(real,sim)
        time = utils.gettime(wfPD[0],conv[0])
        delay = utils.finddelay2(real,sim)
        simshifted =  np.roll(sim,delay)
        #fit the conv vs power:
        realp = utils.watttodbm(real**2/50)
        fitconv_pd = np.polyfit(simshifted,real,1)
        polyconv_pd = np.poly1d(fitconv_pd)
        simpd = polyconv_pd(simshifted)        
        alpha = np.sum( (simpd - real)**2)
        dist = np.append(dist,alpha)
        if alpha < mindist:
            besttau = t
            besta = fitconv_pd[0]
            bestb = fitconv_pd[1]



fig = plt.figure(figsize = (12,6))
plt.subplot(121)
plt.plot(wfPD[0],wfPD[1],label='measured')
plt.plot(besttime, bestsim,label='simulation')
plt.subplot(122)
plt.plot(taus,dist)
#plt.plot(real)
#plt.plot(simpd)
#fig = plt.figure()
#fft = np.fft.rfft(wfRF[1])
#freq = np.fft.rfftfreq(len(wfRF[1]), wfRF[0][1]-wfRF[0][0])
#plt.plot(freq,np.absolute(fft**2))
plt.show()
