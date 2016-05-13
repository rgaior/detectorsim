############################################################################
## computes the average ratio of the spectra from the input RF and        ##
## the power detector's. Saves the average ratio and one phase.           ##
## then fits the average spectrum and write the results.                  ##
############################################################################
from lmfit import minimize, Parameters, Parameter, report_fit
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
    resultfolder = constant.resultfolder + '/method2/nocapa/'
if capaornot == 'capa':
    datafolder = constant.calibdatafolder + '2013_05_10/Capa/'
    basefileRF = datafolder + 'C110mVCapa000*'
    basefilePD = datafolder + 'C210mVCapa000*'
    resultfolder = constant.resultfolder + '/method2/capa/'

filesRF = glob.glob(basefileRF)
filesPD = glob.glob(basefilePD)

allspec = []
onephase = np.array([])
dcvaluepd = 0
dcvaluelogpower = 0
count=0
for f1, f2 in zip(filesRF, filesPD):
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
    if count == 0:
        count+=1
        onephase = np.unwrap(phase1 - phase2)

meanspec = np.zeros(len(allspec[0]))
for s in allspec:
    meanspec+=s
meanspec = meanspec/len(allspec)

dcvaluepd = dcvaluepd/len(allspec)
dcvaluelogpower = dcvaluelogpower/len(allspec)

dcvalue = -0.0252 + 0.684/dcvaluelogpower
np.savez(resultfolder+'meanspec',freq=freq1,spec=meanspec,phase=onephase,dcval=dcvalue)

#####################################
#### fitting part ###################
#####################################

def fcn2min(params, x, data):
    """ model decaying sine wave, subtract data"""
    a = params['a'].value
    k = params['k'].value
    j = params['j'].value
    model = a*np.exp(-(k*x)) + j 
    return (model - data)

spec = meanspec
freq = freq1
spec = spec[(freq > 0) ]
freq = freq[(freq > 0) ]
#flim = 2e8
#spec = spec[(freq > 0) & (freq < flim) ]
#freq = freq[(freq > 0) & (freq < flim)]

params = Parameters()
params.add('a', value=0.024)
params.add('dcvalue', value=dcvalue,vary=False)
params.add('k', value=1e-8,vary=True)
params.add('j', value=1e-4)

result = minimize(fcn2min, params, args=(freq,spec))
report_fit(result.params)

np.savez(resultfolder+'fitresults',a = result.params['a'].value, k = result.params['k'].value,j = result.params['j'].value)

