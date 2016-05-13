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
specs = []
for nr in range(1,60):
    sd = spectrum.Spectrum(nr,type='dmx')
    sd.loadspectrum()
    specs.append(sd.getnormedspec())

nspecn = sn.getnormedspec()
nspecg = sg.getnormedspec()

meanspec = np.zeros(len(specs[0][0]))
freq = specs[0][0]
count = 0
for s in specs:
    plt.plot(s[0],s[1],'g',alpha=0.1)
    meanspec += s[1]
    count+=1

meanspec = meanspec/count
plt.plot(freq,meanspec,'g',lw=2,label='DMX')
plt.plot(nspecg[0],nspecg[1],'b',lw=2,label='GI301')
plt.plot(nspecn[0],nspecn[1],'r',lw=2,label='Norsat')
plt.xlabel('frequency [MHz]')
plt.ylabel('normed gain')
plt.ylim(0,1.1)
plt.legend()
plt.show()
