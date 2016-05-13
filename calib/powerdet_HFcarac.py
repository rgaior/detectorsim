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
    basefileRF = datafolder + 'C110mVNoCapa000*'
    basefilePD = datafolder + 'C210mVNoCapa000*'
    resultfolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/nocapa/'
if capaornot == 'capa':
    datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/Capa/'
    basefileRF = datafolder + 'C110mVCapa000*'
    basefilePD = datafolder + 'C210mVCapa000*'
    resultfolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/capa/'

filesRF = glob.glob(basefileRF)
filesPD = glob.glob(basefilePD)

count = 0
#loop over files

fig = plt.figure(figsize=(12,6))
ax1 = plt.subplot(121)
ax2 = plt.subplot(122)
allspec = []
onephase = np.array([])
onespec= np.array([])
count = 0
## DC carac: V_pd = -0.0234P_dbm + 0.877
dcvaluepd = 0
dcvaluelogpower = 0
for f1, f2 in zip(filesRF, filesPD):
#for f1, f2 in zip(filesRF[::2], filesPD[::2]):
#for f1, f2 in zip(filesRF[:20], filesPD[:20]):
    wfRF = utils.readscopefile(f1)
    wfPD = utils.readscopefile(f2)
    power = wfRF[1]*wfRF[1]/50
    logpower = utils.watttodbm(power)
    realpd = wfPD[1]
    dcvaluepd += np.mean(realpd)
    dcvaluelogpower += np.mean(logpower)
    fftrealpd = np.fft.rfft(realpd)
    freq1 = np.fft.rfftfreq(len(wfRF[1]), wfRF[0][1] - wfRF[0][0])[:-1]
    fftlogpower = np.fft.rfft(logpower)[:-1]
    fftpower = np.fft.rfft(power)[:-1]
    phase1 = np.unwrap(np.angle(fftrealpd))
    phase2 = np.unwrap(np.angle(fftlogpower))
    spec1 = np.absolute(fftrealpd)
    spec2 = np.absolute(fftlogpower)
    allspec.append(spec1/spec2)
    ax1.semilogy(freq1,spec1/spec2)
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

dcvaluepd = dcvaluepd/len(allspec)
dcvaluelogpower = dcvaluelogpower/len(allspec)

#dcvalue = -0.0234 + 0.877/dcvaluelogpower
dcvalue = -0.0252 + 0.684/dcvaluelogpower
print dcvaluepd 
print dcvaluelogpower
print -0.0252*dcvaluelogpower + 0.684
np.savez(capaornot+'meanspec',freq=freq1,spec=meanspec/len(allspec),phase=onephase,dcval=dcvalue)


plt.show()
