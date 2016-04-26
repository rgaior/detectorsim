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
if capaornot == 'capa':
    basefileRF = datafolder + 'C110mVCapa000*'
    basefilePD = datafolder + 'C210mVCapa000*'
    t = 35e-9
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

meanspec = np.load('capameanspec.npz')['spec']
freq  = np.load('capameanspec.npz')['freq']
phase = np.load('capameanspec.npz')['phase']
phase2 = np.pi*np.ones(len(freq))
def func(x, k, j):
    a = 0.024
    return a*np.exp(-(k*x)) + j

k = 7.77611495e-8
j = 1.39148723e-3
spec2 = func(freq,k,j)
response = meanspec*np.exp(1j*phase)
response2 = spec2*np.exp(1j*phase)
response3 = spec2*np.exp(1j*phase2)

real = np.array([])
sim = np.array([])
sim2 = np.array([])
sim3 = np.array([])

for f1, f2 in zip(filesRF[15:16], filesPD[15:16]):
#for f1, f2 in zip(filesRF, filesPD):
#    for t in taus:
    wfRF = utils.readscopefile(f1)
    wfPD = utils.readscopefile(f2)
    logpower = utils.watttodbm(wfRF[1]*wfRF[1]/50)
    realpd = wfPD[1]
    freq1 = np.fft.rfftfreq(len(wfRF[1]), wfRF[0][1] - wfRF[0][0])[:-1]
    fftlogpower = np.fft.rfft(logpower)[:-1]
    fftsim = fftlogpower*response
    fftsim2 = fftlogpower*response2
    fftsim3 = fftlogpower*response3
    simintime = np.fft.irfft(fftsim)
    simintime2 = np.fft.irfft(fftsim2)
    simintime3 = np.fft.irfft(fftsim3)
    print len(simintime)
    print len(wfRF[0])
    ax1.plot(wfPD[0],wfPD[1] - np.mean(wfPD[1]))
    ax1.plot(wfPD[0][:-1],simintime - np.mean(simintime))
    ax1.plot(wfPD[0][:-1],simintime2 - np.mean(simintime2))
#    ax1.plot(wfPD[0][:-1],simintime3 - np.mean(simintime3))
    size1 = len(wfPD[1])
    size2 = len(simintime)
    size3 = len(simintime2)
    realcent = wfPD[1] - np.mean(wfPD[1])
    simcent = simintime - np.mean(simintime)
    simcent2 = simintime2 - np.mean(simintime2)
    simcent3 = simintime3 - np.mean(simintime3)
    
#     real = np.append(real,realcent[:size1/3])
#     sim = np.append(sim,simcent[:size2/3])
#     sim2 = np.append(sim2,simcent2[:size3/3])
#     sim3 = np.append(sim3,simcent3[:size3/3])
    real = np.append(real,realcent)
    sim = np.append(sim,simcent)
    sim2 = np.append(sim2,simcent2)
    sim3 = np.append(sim3,simcent3)

bins = np.linspace(-0.2,0.2,100)
#bins = 100
ax2.hist(real,bins=bins,histtype='step',log=True)
ax2.hist(sim,bins=bins,histtype='step',log=True)
ax2.hist(sim2,bins=bins,histtype='step',log=True)
ax2.hist(sim3,bins=bins,histtype='step',log=True)

plt.show()