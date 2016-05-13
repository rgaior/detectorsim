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
import simulation
import detector
import waveform
import constant
capaornot = sys.argv[1]


if capaornot == 'nocapa':
    datafolder = constant.calibdatafolder + '2013_05_10/NoCapa/'
    basefileRF = datafolder + 'C110mVNoCapa000*'
    basefilePD = datafolder + 'C210mVNoCapa000*'
    taus = np.arange(2e-9,7e-9,0.5e-9)
    resultfolder = constant.resultfolder + '/method1/nocapa/'
if capaornot == 'capa':
    datafolder = constant.calibdatafolder + '2013_05_10/Capa/'
    basefileRF = datafolder + 'C110mVCapa000*'
    basefilePD = datafolder + 'C210mVCapa000*'
    taus = np.arange(25e-9,45e-9,1e-9)
    resultfolder = constant.resultfolder + '/method1/capa/'

filesRF = glob.glob(basefileRF)
filesPD = glob.glob(basefilePD)
print 'don t worry execution can be long '
#result arrays
restau = np.array([])
resa = np.array([])
resb = np.array([])

count = 0
#loop over files
#for f1, f2 in zip(filesRF, filesPD):
for f1, f2 in zip(filesRF[::5], filesPD[::5]):
    mindist = 1e6
    #result for each file
    dist = np.array([])
    besttau = 0
    besta = 0
    bestb = 0
    wfRF = utils.readscopefile(f1)
    wfPD = utils.readscopefile(f2)
    for t in taus:
        conv = utils.produceresponse(wfRF[0],wfRF[1],t)
        real = wfPD[1]
        sim = conv[1]
        #resize the two waveforms to the same size (because of the convolution)
        [real,sim] = utils.resize(real,sim)
        time = utils.gettime(wfPD[0],conv[0])
        delay = utils.finddelay2(real,sim)
        simshifted =  np.roll(sim,delay)        
        #fit the conv vs power:
        fitconv_pd = np.polyfit(simshifted,real,1)
        polyconv_pd = np.poly1d(fitconv_pd)
        simpd = polyconv_pd(simshifted)        
        size = len(simpd)
        alpha = np.sum( (simpd - real)**2)
        dist = np.append(dist,alpha)
        if alpha < mindist:
            mindist = alpha
            besttau = t
            besta = fitconv_pd[0]
            bestb = fitconv_pd[1]
    outname = resultfolder + 'distance_' + str(count) 
    count +=1
    np.savez(outname,tau=taus,dist=dist)
    restau = np.append(restau,besttau)
    resa = np.append(resa, besta)
    resb = np.append(resb, bestb)



print '######## results #########'
print 'mean tau = ',np.mean(restau)
print 'mean a = ',np.mean(resa)
print 'mean b = ',np.mean(resb)
print '###########################'
outnameres = resultfolder + 'results'
np.savez(outnameres,tau=taus,res=np.array([np.mean(restau),np.mean(resa),np.mean(resb)]),sigmares=np.array([np.std(restau),np.std(resa),np.std(resb)]))
