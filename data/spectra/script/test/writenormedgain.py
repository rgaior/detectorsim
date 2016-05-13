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

specgi = []
folder = '/Users/romain/work/Auger/EASIER/data/spectra/EASIER7/'
filelist = ['bastille.spa','concorde.spa','jaime.spa','leandro.spa','magali.spa','nene.spa','paloma.spa']
for f in filelist:
    sg = spectrum.Spectrum(0,type='allgi301',name=folder + f)
    sg.loadspectrum()
#    b = sg.getbandwidth()
    specgi.append(sg.getnormedspec())

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
    plt.plot(s[0],s[1],'b',alpha=0.1)
    meanspec += s[1]
    count+=1

meanspecgi = np.zeros(len(specgi[0][0]))
freqgi = specgi[0][0]
countgi = 0
for s in specgi:
    plt.plot(s[0],s[1],'b',alpha=0.1)
    meanspecgi += s[1]
    countgi+=1

meanspec = meanspec/count
meanspecgi = meanspecgi/countgi

datafolder = '/Users/romain/work/Auger/EASIER/data/spectra/'
legs = ['DMX241', 'GI301','Norsat8115']

#write DMX:
outnamed = datafolder+legs[0]+'_n.txt'
f1 = open(outnamed,'w')
for fr,sp in zip(freq,meanspec):
    f1.write(str(fr*1e6) + ' ' + str(sp) + '\n')
f1.close()

#write GI:
outnameg = datafolder+legs[1]+'_n.txt'
f2 = open(outnameg,'w')
for fr,sp in zip(freqgi,meanspecgi):
    f2.write(str(fr*1e6) + ' ' + str(sp) + '\n')
f2.close()

#write Norsat:
outnamen = datafolder+legs[2]+'_n.txt'
f3 = open(outnamen,'w')
for fr,sp in zip(nspecn[0][::-1],nspecn[1][::-1]):
    f3.write(str(fr*1e6) + ' ' + str(sp) + '\n')
f3.close()

