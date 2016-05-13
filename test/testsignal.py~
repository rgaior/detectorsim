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
import constant
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
tsys = 10
det = detector.Detector(temp=tsys,type=dettype)
det.loadspectrum()
sim = simulation.Simulation(det=det,snr=10,siglength=10e-9,sampling=5e9)
sim.producetime()

sim.producenoise(True)

sim.setpowerenvelope('gauss')
sim.producesignal()

simwf = waveform.Waveform(sim.time,sim.noise + sim.signal, type='hf')

wf = det.producesimwaveform(simwf,'adc',method)
plt.plot(wf.time, wf.amp)
plt.show()
