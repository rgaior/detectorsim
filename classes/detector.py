import utils
import math
import numpy as np
from scipy import signal
import constant
import waveform
#hard coded value:
#front end filter cut frquency
fcut = 20e6
fesampling = 40e6
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/spectra/'
datafolder = '/Users/romain/work/Auger/EASIER/data/spectra/'

class Detector:
    def __init__(self, temp, gain, f1,f2, tau,type=''):
        self.temp = temp
        self.gain = gain  
        self.f1 = f1
        self.f2 = f2
        self.tau = tau
        self.capaornot = 0
        self.noisespectrum = []
        self.type = type
        #cf thesis R.Gaior for the numbers
        # new note on detector
#        self.pd_slope = -0.02
        if type == 'dmx' or type=='norsat':
#            self.pd_slope = -0.0202
#            self.tau = 4.4e-9
            self.capaornot = 0
            self.pd_k = 0.88
            self.pd_slope = -0.0192
            self.tau = 4.7e-9
        elif type=='gi':
            self.capaornot = 1
            self.pd_k = 0.816
            self.pd_slope = -0.0217
            self.tau = 34.8e-9

#        self.pd_slope = -0.0234
        #cf depends on board,
        #take an example for now
#        self.board_k = 5.5
        self.board_k = 5.923
        self.board_slope = -4.19
        
    #return [time, amp] for the different stages of the detector
    def producesimwaveform(self, simwf, stage, method=None):
        stagelc = stage.lower()
        if stagelc not in ['logresponse','powerdetector','board','fefilter','timesampled','adc']:
            print 'choose among these stages: \n ', 'logresponse or powerdetector or board or fefilter or timesampled or adc'
            return 
        elif stagelc == 'logresponse':
            return self.produceresponse(simwf)
        elif stagelc == 'powerdetector':
            logresponse = self.produceresponse(simwf)
            return self.powerdetlinear(logresponse)
        elif stagelc == 'board':
            logresponse = self.produceresponse(simwf)
            afterpd = self.powerdetlinear(logresponse)
            return self.adaptationboard2(afterpd)
        elif stagelc == 'fefilter':
            logresponse = self.produceresponse(simwf)
            afterpd = self.powerdetlinear(logresponse)
            afterboard = self.adaptationboard2(afterpd)
            return self.FEfilter(afterboard)
        elif stagelc == 'timesampled':
            logresponse = self.produceresponse(simwf)
            afterpd = self.powerdetlinear(logresponse)
            afterboard = self.adaptationboard2(afterpd)
            afterFEfilter = self.FEfilter(afterboard)
            return self.FEtimesampling(afterFEfilter)
        elif stagelc == 'adc':
            if method == None:
                logresponse = self.produceresponse(simwf)
                afterpd = self.powerdetlinear(logresponse)
            else:
                afterpd = self.powerdetsim(simwf)
            afterboard = self.adaptationboard2(afterpd)
            afterFEfilter = self.FEfilter(afterboard)
            timesampled = self.FEtimesampling(afterFEfilter)
            return self.FEampsampling(timesampled)

    def produceresponse(self,wf):
        tend = 500e-9
        period = 1./wf.sampling
        x = np.arange(0,tend,period)
        convfunc = period*np.exp(-x/self.tau)/( -(math.exp(-tend/self.tau) - 1)*self.tau)
        # response in dBm
        power = self.gain*(wf.amp*wf.amp)/constant.impedance
        signal = 10*np.log10(power) + 30
        resp = np.convolve(signal,convfunc,'valid')
        newtime = np.linspace(wf.time[0], float(len(resp))/wf.sampling+wf.time[0], len(resp))
        newamp = resp        
        newwf = waveform.Waveform(newtime,newamp,'logresponse')
        return newwf

#power detector characteristic (P[dBm] vs V_pd[V])
    def powerdetlinear(self, wf):
        newwf = waveform.Waveform(wf.time,self.pd_k + self.pd_slope*wf.amp,'powerdetector')
        return newwf

#power detector simulation with the filter (P[dBm] vs V_pd[V])
    def powerdetsim(self, wf):
        newamp = utils.powerdetectorsim(wf.time,wf.amp,self.capaornot)
        newwf = waveform.Waveform(wf.time,newamp,'powerdetector')
        return newwf

#adaptation board characteristic (V_pd [V] vs V_board [V])
    def adaptationboard(self, wf):
        newwf = waveform.Waveform(wf.time,self.board_k + self.board_slope*wf.amp,'board')
        return newwf
#adaptation board characteristic (V_pd [V] vs V_board [V])
#another way to simulate the easier board is to account for the spectrum of the amplifier
    def adaptationboard2(self, wf):
        # first we compute the fft of the wf:
        fft = np.fft.rfft(wf.amp)
        spec = np.absolute(fft)
        fftfreq = np.fft.rfftfreq(len(wf.amp),wf.time[1] - wf.time[0])
        # then we produce the gain of the amplifier for the given frequencies (exept DC)
        # according the study that extracted the parameters empirically
        prefact = 3.86
        mu = -40
        sigma = 75.1
        k = 1
        gainspec = prefact*np.exp(-(fftfreq/1e6 - mu)**2/(2*sigma**2)) + k 
        a =4.8e-5
        b = -1.1e-3
        c = 2.97
        pgainphase  = np.poly1d([a,b,c])
        gainphase = pgainphase(fftfreq/1e6)
        gainfft = gainspec[1:]*np.exp(1j*gainphase[1:])
#        hf = fft[1:]*gainfft[1:]        
        dcgain = self.board_slope + self.board_k/np.mean(wf.amp)
        gainfft = np.insert(gainfft,0,dcgain)
        newamp = np.fft.irfft(gainfft*fft)
        newwf = waveform.Waveform(wf.time[:-1],newamp,'board')
#        newwf = waveform.Waveform(wf.time,self.board_k + self.board_slope*wf.amp,'board')
        return newwf
#simulate the Front end filter of Auger electronics 
    def FEfilter(self, wf):
        Nyfreq = wf.sampling/2
        ratiofreq = float(fcut)/Nyfreq
        b, a = signal.butter(4, ratiofreq)
        y = utils.lowpass(wf.amp,wf.sampling,4,1*fcut)
#        y = utils.lowpasshard(wf.amp,wf.sampling,fcut)
 #       y = utils.lowpasshard(wf.amp,wf.sampling,2*fcut)
#        y = signal.filtfilt(b, a, wf.amp)
#        newwf = waveform.Waveform(wf.time[:-1],y,'fefilter')
        newwf = waveform.Waveform(wf.time,y,'fefilter')
        return newwf

#simulate:
    # the sampling in time (every 25ns)
    def FEtimesampling(self, wf):
        #first time sampling:
        step = float(1./fesampling)
        tracelength = wf.length
        nrofpoints = int(tracelength/step)
        newtime = np.linspace(wf.tstart,wf.tend,nrofpoints)
        [a,b] = utils.resize(wf.time,wf.amp)
#        newy = np.interp(newtime,wf.time,wf.amp)
        newy = np.interp(newtime,a,b)
        newwf = waveform.Waveform(newtime,newy,'timesampled')
        return newwf

#simulate
    # the gain of the input amplifier g = (-1/2)
    # the sampling in amplitude (0-1 to 0-1023)
    def FEampsampling(self, wf):
        #first time sampling:
        newy = -0.5*wf.amp*1023
        newy = newy.astype(int)
        newwf = waveform.Waveform(wf.time,newy,'adc')
        return newwf


    def loadspectrum(self):
        fname = ''
        if 'norsat' in self.type.lower():
            fname = 'Norsat8115_n.txt'
        if 'dmx' in self.type.lower():
            fname = 'DMX241_n.txt'
        if 'gi' in self.type.lower():
            fname = 'GI301_n.txt'
        f = open(datafolder+fname,'r')
        print datafolder+fname
        freq = np.array([])
        gain = np.array([])
        for l in f:
            freq = np.append(freq,float(l.split()[0]))
            gain = np.append(gain,float(l.split()[1]))
        self.noisespectrum = [freq,gain]
