############################################################################
## loop over all the waveform to find the best tau and linear coefficent  ##
## for each waveform. Then takes the average and outputs the results      ##
############################################################################
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
import constant
import simulation
import detector
import waveform

capaornot = sys.argv[1]


if capaornot == 'nocapa':
    datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/NoCapa/'
    basefileRF = datafolder + 'C110mVNoCapa000*'
    basefilePD = datafolder + 'C210mVNoCapa000*'
    taus = np.arange(3e-9,10e-9,0.5e-9)
    resultfolder = constant.resultfolder + '/method3/nocapa/'
if capaornot == 'capa':
    datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/Capa/'
    basefileRF = datafolder + 'C110mVCapa000*'
    basefilePD = datafolder + 'C210mVCapa000*'
    taus = np.arange(30e-9,50e-9,2e-9)
    resultfolder = constant.resultfolder + '/method3/capa/'
filesRF = glob.glob(basefileRF)
filesPD = glob.glob(basefilePD)
#result arrays
restau = np.array([])
tsys = 50
gain = 1e6
f1 = 0.95e9
f2 = 1.75e9

count = 0
#loop over files
for f1, f2 in zip(filesRF, filesPD):
    mindist = 1e6
    dist = np.array([])
    besttau = 0
    alpha=0
    wfRF = utils.readscopefile(f1)
    wfPD = utils.readscopefile(f2)
    for t in taus:
        [sim,real] = utils.findparam_3(wfRF,wfPD,t)
        alpha = np.sum( (sim[1] - real[1])**2)
        dist = np.append(dist,alpha)
        if count == 0:
            count+=1
        if alpha < mindist:
            mindist = alpha
            besttau = t
    outname = resultfolder + 'distance_' + str(count) 
    count +=1
    np.savez(outname,tau=taus,dist=dist)
    restau = np.append(restau,besttau)

print '######## results #########'
print np.mean(restau) , '+- ' , np.std(restau)
print '##########################'
outnameres = resultfolder + 'results' 
np.savez(outnameres,tau=taus,res=np.mean(restau),sigmares=np.std(restau) )
