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
import spectrum

sn = spectrum.Spectrum(0,type='norsat')
sn.loadspectrum()

sg = spectrum.Spectrum(0,type='gi301')
sg.loadspectrum()

bws = np.array([])
for nr in range(1,60):
    sd = spectrum.Spectrum(nr,type='dmx')
    sd.loadspectrum()
    bw = sd.getbandwidth()
    bws = np.append(bws,bw)

bwn = sn.getbandwidth()
bwg = sg.getbandwidth()

meanbwd = np.mean(bws)
stdbwd = np.std(bws)
print '**************************'
print 'Bandwidth Norsat = ',bwn
print 'Bandwidth GI = ',bwg
print 'Bandwidth DMX = ', meanbwd , ' +- ', stdbwd
print '**************************'
