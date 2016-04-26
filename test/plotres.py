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

capaornot = sys.argv[1]

if capaornot == 'nocapa':
    datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/NoCapa/'
    basefileRF = datafolder + 'C110mVNoCapa000*'
    basefilePD = datafolder + 'C210mVNoCapa000*'
    taus = np.arange(4e-9,6e-9,0.1e-9)
    resultfolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/nocapa/'
if capaornot == 'capa':
    datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/Capa/'
    basefileRF = datafolder + 'C110mVCapa000*'
    basefilePD = datafolder + 'C210mVCapa000*'
    taus = np.arange(30e-9,40e-9,1e-9)
    resultfolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/fittau/capa/'


filesRF = glob.glob(basefileRF)
filesPD = glob.glob(basefilePD)
#result arrays
deltav = np.array([])
count = 0
res = np.load(resultfolder + 'results.npz')
tau = res['res'][0]
a = res['res'][1]
b = res['res'][2]

#loop over files
for f1, f2 in zip(filesRF[::5], filesPD[::5]):
    wfRF = utils.readscopefile(f1)
    wfPD = utils.readscopefile(f2)
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
    deltav = np.append(deltav,simpd - real)



c,b,p = plt.hist(deltav,bins=100)
plt.show()