############################################################################
## loop over all the waveform to find the best tau and linear coefficent  ##
## for each waveform. Then takes the average and outputs the results      ##
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

capaornot = sys.argv[1]


if capaornot == 'nocapa':
    datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/NoCapa/'
if capaornot == 'capa':
    datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/Capa/'
## for easier7
#taus = np.arange(5e-9,100e-9,10e-9)
## for easier61

if capaornot == 'nocapa':
    basefileRF = datafolder + 'C110mVNoCapa000*'
    basefilePD = datafolder + 'C210mVNoCapa000*'
    t = 5e-9
    taus = np.arange(2e-9,7e-9,3e-9)
if capaornot == 'capa':
    basefileRF = datafolder + 'C110mVCapa000*'
    basefilePD = datafolder + 'C210mVCapa000*'
    t = 35e-9
    taus = np.arange(25e-9,45e-9,10e-9)
#    taus = np.arange(25e-9,45e-9,1e-9)
filesRF = glob.glob(basefileRF)
filesPD = glob.glob(basefilePD)
#result arrays
restau = np.array([])
resa = np.array([])
resb = np.array([])
#save folder
if capaornot == 'nocapa':
    resultfolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/nocapa/'
if capaornot == 'capa':
    resultfolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/capa/'
count = 0
#loop over files
file = 1
fig = plt.figure(figsize=(12,6))
ax1 = plt.subplot(121)
ax2 = plt.subplot(122)
allspec = []
onephase = np.array([])
onespec= np.array([])
count = 0
#for f1, f2 in zip(filesRF[::5], filesPD[::5]):
for f1, f2 in zip(filesRF[:20], filesPD[:20]):
#    for t in taus:
    wfRF = utils.readscopefile(f1)
    wfPD = utils.readscopefile(f2)
    logpower = utils.watttodbm(wfRF[1]*wfRF[1]/50)
    realpd = wfPD[1]
    
    fftrealpd = np.fft.rfft(realpd)
    freq1 = np.fft.rfftfreq(len(wfRF[1]), wfRF[0][1] - wfRF[0][0])[:-1]
    fftlogpower = np.fft.rfft(logpower)[:-1]
    phase1 = np.unwrap(np.angle(fftrealpd))
    phase2 = np.unwrap(np.angle(fftlogpower))
    spec1 = np.absolute(fftrealpd)
    spec2 = np.absolute(fftlogpower)
    allspec.append(spec1/spec2)
#    ax1.semilogy(freq1,spec1/spec2)
    if count == 0:
        count+=1
        onespec = spec1/spec2
        onephase = np.unwrap(phase1 - phase2)
        ax2.plot(freq1,np.unwrap(phase1 - phase2))

meanspec = np.zeros(len(allspec[0]))
for s in allspec:
    meanspec+=s

ax1.semilogy(freq1,meanspec/len(allspec),'r-',lw=2)
ax1.semilogy(freq1,onespec,'r--',lw=1)
#ax2.loglog(freq1,meanspec/len(allspec),'r--',lw=3)
np.savez(capaornot+'meanspec',freq=freq1,spec=meanspec/len(allspec),phase=onephase)


plt.show()
