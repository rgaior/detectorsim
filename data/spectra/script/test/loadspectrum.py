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

#load file:
specnr = 10

s = spectrum.Spectrum(specnr)
s.loadspectrum()


plt.plot(s.spectrum[0],s.spectrum[1])
plt.show()