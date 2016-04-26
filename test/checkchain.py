############################################################################
## for one waveform, produce the simulation of the power detector         ##
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

wfnr = '19'
datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/Capa/'
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/NoCapa/'
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_03_25/HF_box/'
fileRF = datafolder + 'C110mVCapa000' + wfnr + '.txt'
filePD = datafolder + 'C210mVCapa000' + wfnr + '.txt'
filesRF = glob.glob(datafolder+ 'C110mVCapa000'+ '*.txt*')
filesPD = glob.glob(datafolder+ 'C210mVCapa000'+ '*.txt*')
count = 0

tsys = 50
gain = 1
f1 = 1.3e9
f2 = 1.75e9
deltaf = f2- f1
#tau = 4.7e-9
tau = 35e-9

#loop over files
for fileRF, filePD in zip(filesRF[::2],filesPD[::2]):
    print fileRF
    wfRF = utils.readscopefile(fileRF)
    wfPD = utils.readscopefile(filePD)
    

    det = detector.Detector(tsys, gain, f1, f2, tau,type='dmx')
    sim = simulation.Simulation(det=det,sampling=5e9)
    sim.noise = wfRF[1]
    sim.time = wfRF[0]
    simwf = waveform.Waveform(sim.time,sim.noise, type='hf')
    wf = det.producesimwaveform(simwf,'adc')
    
    
    gain2 = 1e6
    det2 = detector.Detector(tsys, gain2, f1, f2,tau,type='gi')
    sim2 = simulation.Simulation(det=det2,sampling=5e9)
    det2.loadspectrum()
    sim2.producetime()
    sim2.producenoise(True)
    detsimwf = waveform.Waveform(sim2.time,sim2.noise, type='hf')
    detwf = det2.producesimwaveform(detsimwf,'adc')
    
    
    det3 = detector.Detector(tsys, gain, f1, f2,tau,type='dmx')
    real = waveform.Waveform(wfPD[0],wfPD[1], type='pd')
#afterboard = det3.adaptationboard2(real)
    afterboard = det3.adaptationboard(real)
    afterFEfilter = det3.FEfilter(afterboard)
    timesampled = det3.FEtimesampling(afterFEfilter)
    adctrace = det3.FEampsampling(timesampled)





#print 'std meas = ' ,np.std(wfPD[1])
    print 'std chain sim= ' ,np.std(wf.amp[:len(wf.amp)/3])
    print 'std all detsim= ' ,np.std(detwf.amp[:len(detwf.amp)/3])
    print 'std real = ', np.std(adctrace.amp[:len(adctrace.amp)/3])

    fig = plt.figure()
    plt.plot(wf.amp- np.mean(wf.amp))
#    plt.plot(detwf.amp - np.mean(detwf.amp))
    plt.plot(adctrace.amp - np.mean(adctrace.amp))

#    plt.plot(wf.time,wf.amp- np.mean(wf.amp))
#    plt.plot(detwf.time,detwf.amp - np.mean(detwf.amp))
#    plt.plot(adctrace.time,adctrace.amp - np.mean(adctrace.amp))

# xlim = 500
# #plt.subplot(211)
# #plt.plot(wfPD[0]*1e9,wfPD[1])
# #plt.plot(wf.time*1e9,wf.amp,label='sim')
# #plt.plot(detwf.time*1e9,detwf.amp,label='detsim')
# spec1 = np.absolute(np.fft.rfft(sim.noise))
# spec2 = np.absolute(np.fft.rfft(sim2.noise))
# plt.plot(fr1,spec1/np.max(spec1[10:-10]) )
# plt.plot(fr2,spec2/np.max(spec2) )
# #plt.plot(fr2, np.absolute(np.fft.rfft(sim2.noise)))
plt.show()

