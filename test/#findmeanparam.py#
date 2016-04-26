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
    taus = np.arange(2e-9,7e-9,0.5e-9)
if capaornot == 'capa':
    basefileRF = datafolder + 'C110mVCapa000*'
    basefilePD = datafolder + 'C210mVCapa000*'
    taus = np.arange(25e-9,45e-9,1e-9)
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
for f1, f2 in zip(filesRF[::5], filesPD[::5]):
    mindist = 1e6
    dist = np.array([])
    besttau = 0
    besta = 0
    bestb = 0
    for t in taus:
        wfRF = utils.readscopefile(f1)
        wfPD = utils.readscopefile(f2)
        #test with the noise part
        size = len(wfRF[1])
        wfRF = [wfRF[0][:size/3],wfRF[1][:size/3]]
        wfPD = [wfPD[0][:size/3],wfPD[1][:size/3]]
        #        newpd =wfPD[1][:size/3]
#        newrf = wfRF[1][:size/3]
#        newtimerf = wfRF[0][:size/3]
#        newtimepf = wfPD[0][:size/3]
        #test with resampling:
#        newpd = utils.resample(wfPD[0],wfPD[1],10e9)
#        newrf = utils.resample(wfRF[0],wfRF[1],10e9)
        conv = utils.produceresponse(wfRF[0],wfRF[1],t)
#        conv = utils.produceresponse(newrf[0],newrf[1],t)
#        real = newpd
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
#        alpha = np.sum( (simpd[size/4:-size/4] - real[size/4:-size/4])**2)
        alpha = np.sum( (simpd - real)**2)
        dist = np.append(dist,alpha)
        if alpha < mindist:
            mindist = alpha
            besttau = t
            besta = fitconv_pd[0]
            bestb = fitconv_pd[1]
    outname = resultfolder + 'distance_' + str(count) 
    count +=1
#    np.savez(outname,tau=taus,dist=dist)
    restau = np.append(restau,besttau)
    print 'best tau = ', besttau
    print 'a = ' ,besta 
    print 'b = ' ,bestb 
    resa = np.append(resa, besta)
    resb = np.append(resb, bestb)

print '######## results #########'
print 'mean tau = ',np.mean(restau)
print 'mean a = ',np.mean(resa)
print 'mean b = ',np.mean(resb)
print '###########################'
outnameres = resultfolder + 'results' 
#np.savez(outnameres,tau=taus,res=np.array([np.mean(restau),np.mean(resa),np.mean(resb)]),sigmares=np.array([np.std(restau),np.std(resa),np.std(resb)]))
