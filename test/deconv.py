############################################################################
## loop over all the waveform to find the best tau and linear coefficent  ##
## for each waveform. Then takes the average and outputs the results      ##
############################################################################
import numpy as np
import matplotlib.pyplot as plt
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
    tau = constant.nc3_powerdettau
    offset = constant.nc3_powerdetoffset
    slope = constant.nc3_powerdetslope
if capaornot == 'capa':
    datafolder = constant.calibdatafolder + '2013_05_10/Capa/'
    basefileRF = datafolder + 'C110mVCapa000*'
    basefilePD = datafolder + 'C210mVCapa000*'
    taus = np.arange(25e-9,45e-9,1e-9)
    resultfolder = constant.resultfolder + '/method1/capa/'
    tau = constant.c3_powerdettau
    offset = constant.c3_powerdetoffset
    slope = constant.c3_powerdetslope

filesRF = glob.glob(basefileRF)
filesPD = glob.glob(basefilePD)
print 'don t worry execution can be long '
#result arrays
restau = np.array([])
resa = np.array([])
resb = np.array([])
gain = 1
file = 10
count = 0
#loop over files
#for f1, f2 in zip(filesRF, filesPD):
for f1, f2 in zip(filesRF[file:file+1], filesPD[file:file+1]):
    wfRF = utils.readscopefile(f1)
    wfPD = utils.readscopefile(f2)
#    conv = utils.produceresponse(wfRF[0],wfRF[1],gain,tau)
    conv = utils.produceresponse2(wfRF[0],wfRF[1],gain,tau)
    real = wfPD[1]
    sim = conv[1]
        #resize the two waveforms to the same size (because of the convolution)
    [real,sim] = utils.resize(real,sim)
    time = utils.gettime(wfPD[0],conv[0])
    delay = utils.finddelay2(real,sim)
    simshifted =  np.roll(sim,delay)        
    poly = np.poly1d([slope,offset])
        #fit the conv vs power:
    simpd = poly(simshifted)
    print len(time), ' ' , len(real)

    # deconvolution:
    deconv = utils.deconv(wfPD[0],wfPD[1],gain,tau)
    polydeconv = np.poly1d([1./slope, - offset/slope])
    dec = polydeconv(deconv[1])
    power = wfRF[1]**2/constant.impedance
    logpower = utils.watttodbm(power)
    decsamp = 1./(deconv[0][1] - deconv[0][0])
    print decsamp
    fcut = 2e8
#    dec = utils.lowpasshard(dec,decsamp, fcut)
    dec = utils.lowpass(dec,decsamp, 4, fcut)
    lindec = utils.dbmtowatt(dec)
    fft = np.fft.rfft(dec)
    fftfreq = np.fft.rfftfreq(len(dec),deconv[0][1] - deconv[0][0])
#    plt.semilogy(fftfreq,np.absolute(fft))
#    plt.plot(wfRF[0],logpower)
#    plt.plot(deconv[0],dec)
    plt.plot(wfRF[0],power)
    plt.plot(deconv[0],lindec)
    
#    plt.plot(time,real)
#    plt.plot(time,simpd)

    
plt.show()
