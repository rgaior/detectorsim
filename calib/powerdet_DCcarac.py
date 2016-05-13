#################################################################################
### finds and plot the P_dBm vs V_powerdet for the DC component and the rest  ###
#################################################################################
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
import glob
#temp, gain, bw, tau of power det
datafolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/data/noise/'
files1_3mv = glob.glob(datafolder+'C1noise3mv*')
files2_3mv = glob.glob(datafolder+'C2noise3mv*')

files1_5mv = glob.glob(datafolder+'C1noise5mv*')
files2_5mv = glob.glob(datafolder+'C2noise5mv*')

files1_7mv = glob.glob(datafolder+'C1noise7mv*')
files2_7mv = glob.glob(datafolder+'C2noise7mv*')

meanlog = np.array([])
logmean = np.array([])
meanpd = np.array([])

#####################################
### the noise estimation          ###
#####################################
# the noise is measured in the first 10 waveforms:
noise3rf = 0
noise3pd = 0
noise5rf = 0
noise5pd = 0
noise7rf = 0
noise7pd = 0
nr = 10
for f1,f2 in zip(files1_3mv[:nr],files2_3mv[:nr]):
    wf1 = utils.readscopefile(f1)
    wf2 = utils.readscopefile(f2)
    power = wf1[1]*wf1[1]/50
    noise3rf += np.mean(power)
    noise3pd += np.mean(wf2[1])
for f1,f2 in zip(files1_5mv[:nr],files2_5mv[:nr]):
    wf1 = utils.readscopefile(f1)
    wf2 = utils.readscopefile(f2)
    power = wf1[1]*wf1[1]/50
    noise5rf += np.mean(power)
    noise5pd += np.mean(wf2[1])
for f1,f2 in zip(files1_7mv[:nr],files2_7mv[:nr]):
    wf1 = utils.readscopefile(f1)
    wf2 = utils.readscopefile(f2)
    power = wf1[1]*wf1[1]/50
    noise7rf += np.mean(power)
    noise7pd += np.mean(wf2[1])
noise3rf = noise3rf/nr
noise3pd = noise3pd/nr
noise5rf = noise5rf/nr
noise5pd = noise5pd/nr
noise7rf = noise7rf/nr
noise7pd = noise7pd/nr

#for f1,f2 in zip(files1[::10],files2[::10]):
nrskip = 10
for f1,f2 in zip(files1_3mv[10:],files2_3mv[10:]):
#for f1,f2 in zip(files1_3mv[10::nrskip],files2_3mv[10::nrskip]):
    print f1, f2
    wf1 = utils.readscopefile(f1)
    wf2 = utils.readscopefile(f2)
    power = wf1[1]*wf1[1]/50 
    logpower = utils.watttodbm(power)
    
    if (np.mean(wf2[1]) > 1.8) :
        continue
    meanlog = np.append(meanlog,np.mean(logpower))
    logmean = np.append(logmean,utils.watttodbm(np.mean(power - noise3rf)) )
    meanpd = np.append(meanpd,np.mean(wf2[1]))

for f1,f2 in zip(files1_5mv[10:],files2_5mv[10:]):
#for f1,f2 in zip(files1_5mv[10::nrskip],files2_5mv[10::nrskip]):
    print f1, f2
    wf1 = utils.readscopefile(f1)
    wf2 = utils.readscopefile(f2)
    power = wf1[1]*wf1[1]/50 
    logpower = utils.watttodbm(power)
    if (np.mean(wf2[1]) > 1.8) :
        continue
    meanlog = np.append(meanlog,np.mean(logpower))
    logmean = np.append(logmean,utils.watttodbm(np.mean(power -noise5rf)) )
    meanpd = np.append(meanpd,np.mean(wf2[1]))

for f1,f2 in zip(files1_7mv[10:],files2_7mv[10:]):
#for f1,f2 in zip(files1_7mv[10::nrskip],files2_7mv[10::nrskip]):
    print f1, f2
    wf1 = utils.readscopefile(f1)
    wf2 = utils.readscopefile(f2)
    power = wf1[1]*wf1[1]/50 
    logpower = utils.watttodbm(power)
    if (np.mean(wf2[1]) > 1.8) :
        continue
    meanlog = np.append(meanlog,np.mean(logpower))
    logmean = np.append(logmean,utils.watttodbm(np.mean(power - noise7rf)) )
    meanpd = np.append(meanpd,np.mean(wf2[1]))


    
fig1 = plt.figure()
ax1 = plt.subplot(111)
ax1.plot(meanlog,meanpd,'ro',label='mean log')
ax1.plot(logmean,meanpd,'bo',label='log mean')
fit1 = np.polyfit(meanlog,meanpd,1)
pfit1 = np.poly1d(fit1)
fit2 = np.polyfit(logmean,meanpd,1)
pfit2 = np.poly1d(fit2)
print fit1
print fit2
x1 = np.linspace(np.min(meanlog),np.max(meanlog),10)
# print fit
ax1.plot(x1,pfit1(x1),'r-',label='fit mean log')
x2 = np.linspace(np.min(logmean),np.max(logmean),10)
# print fit
ax1.plot(x2,pfit2(x2),'b-',label='fit log mean')
ax1.text(0.01, 0.95, 'fit mean log: \n V_pd = '+ str("%.4f" % fit1[0])+ 'P_dBm + ' +str("%.3f" % fit1[1]) ,
        verticalalignment='top', horizontalalignment='left',
        transform=ax1.transAxes,
        color='red', fontsize=15)
ax1.text(0.01, 0.85, 'fit log mean: \n V_pd = '+ str("%.4f" % fit2[0])+ 'P_dBm + ' +str("%.3f" % fit2[1]) ,
        verticalalignment='top', horizontalalignment='left',
        transform=ax1.transAxes,
        color='blue', fontsize=15)
ax1.set_ylabel('power detector [V]')
ax1.set_xlabel('power [dBm]')
ax1.set_ylim(1.65,1.87)
plt.legend()

plt.legend()
plt.show()

