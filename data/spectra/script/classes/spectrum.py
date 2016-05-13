import utils
import math
import numpy as np
from scipy import signal

datafolder = '/Users/romain/work/Auger/EASIER/data/spectra/2011_12_06/'
datanorsat = '/Users/romain/work/Auger/EASIER/data/spectra/norsat.txt'
datagi301 = '/Users/romain/work/Auger/EASIER/data/spectra/gi301.txt'

#################################################
###  defines a gain pattern at one frequency  ###
#################################################
class Spectrum:
    def __init__(self,nr,type='',name=None):
        self.nr = nr
        self.spectrum = []      
        self.type = type
        self.name = name

    def loadspectrum(self):
        if self.type.lower()=='dmx':
            filename = datafolder + 'refantenna_#'+str(self.nr) + '.spa'
            utils.readspectrum(filename) 
            self.spectrum = utils.readspectrum(filename)
        if self.type.lower() == 'norsat':
            self.spectrum = utils.readspectrumtwocol(datanorsat)
            self.shiftfreq()
        if self.type.lower() == 'gi301':
            self.spectrum = utils.readspectrumtwocol(datagi301,1)
            self.spectrum[0] = self.spectrum[0]*1000
            self.shiftfreq()
        if self.type.lower() == 'allgi301':
            self.spectrum = utils.readspectrum(self.name)
            self.spectrum[0] = self.spectrum[0]
            #self.shiftfreq()
            
    def getnormedspec(self):
        if len(self.spectrum) >0:
            spec = self.spectrum[1][1:]
            freq = self.spectrum[0][1:]
            spec = utils.logtolin(spec)
            maxspec = np.max(spec)
            spec = spec/maxspec
            return [freq,spec]
        else:
            print '!!!!!!!!!!! no spectrum loaded !!!!!!!!'
        
    def getbandwidth(self):
        [freq,spec] = self.getnormedspec()
        bandwidth = np.absolute(np.trapz(spec,freq))
        return bandwidth
            
    def shiftfreq(self):
        fLO = 5150
        self.spectrum[0] = fLO - self.spectrum[0]
