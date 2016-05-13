####################################################
### just a test function to look at the output    ##
## of a noise waveform with a sine waveform added ##
####################################################

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
import simulation
import detector
import waveform

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("detector", type=str, nargs='?',default='norsat', help="type of detector: gi, dmx, norsat, helix")
parser.add_argument("method", type=int, nargs='?', default=3, help="power detection simulation  method: 1,2 or 3")
args = parser.parse_args()

print '#####################################'
print '###### detector: ', args.detector ,' ######'
print '###### power det method: ', args.method ,' ######'
print '#####################################'
dettype = args.detector
method = args.method


det = detector.Detector(type=dettype)
det.loadspectrum()
sim = simulation.Simulation(det=det,sampling=5e9)
sim.producetime()
sim.producenoise(True)
simwf = waveform.Waveform(sim.time,sim.noise, type='hf')
sinefreq = 2e9
sineamp = 1e-2
deltat = sim.time[1] - sim.time[0]
sine = utils.wf_sine(sinefreq, sineamp, deltat, sim.time[-1])
sinewf = waveform.Waveform(sim.time,sine, type='hf')
sumwf =  waveform.Waveform(sim.time,sine + sim.noise, type='hf')
wf = det.producesimwaveform(sumwf,'adc',method)

fftadc = np.fft.rfft(wf.amp)
freq = np.fft.rfftfreq(len(wf.amp),2e-10)
#freq = np.fft.rfftfreq(len(wf.amp),25e-9)
#plt.semilogy(freq,np.absolute(fftadc))
print 'rms = ',  np.std(wf.amp)
plt.plot(wf.time, wf.amp)
plt.show()
