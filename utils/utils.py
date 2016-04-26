import numpy as np
from scipy import signal
import math



###############################################
####  reading functions                 #####
###############################################

# read a file with: time power [W]
def readsimfile(file):
    f = open(file,'r+')
    time = np.array([])
    power = np.array([])
    for l in f:
        lsplit = l.split()
        time = np.append(time,float(lsplit[0]))
        power = np.append(power,float(lsplit[1]))
    return [time,power]

def readscopefile(filename):
    f = open(filename,'r+')
    time = np.array([])
    v = np.array([])
    count = 0
    for l in f:
        if count < 6:
            count = count+1
            continue
        lsplit = l.split(',')
        time = np.append(time,float(lsplit[-2]))
        v = np.append(v,float(lsplit[-1]))
    return [time,v]

###############################################
####  producing functions                 #####
###############################################


def wf_normal(mean,sigma,nrofsamples):
    return np.random.normal(mean,sigma,nrofsamples)

def wf_dirac(nrofsamples):
    return  np.append(np.array([1]),np.zeros(nrofsamples-1))

def wf_sine(freq, amp, deltat, tend):
    t = np.arange(0, tend + deltat, deltat)
    print freq
    print freq*t
    thesine = amp*np.sin(2*math.pi*freq*t)
    return thesine


def func_normedgauss(x,mean,sigma):
    #a = (1./(sigma*( math.sqrt(2*math.pi) )) )*np.exp(-0.5* ((x - mean)/sigma)**2 )
    a = np.exp(-0.5* ((x - mean)/sigma)**2 )
    return a



###############################################
#### conversion function (voltage to adc, #####
#### voltage FE to voltage board etc... ) #####
###############################################
#for np array
#adc counts to volt at the FE input (between 0-1V)
def adctov_fe(adc):
    return adc.astype(float)/1024
def v_fetoadc(vfe):
    return vfe.astype(float)*1024

#voltage at front end to voltage at GIGAS/EASIER board
def v_fetov_board(vfe):
    return vfe*(-2)
def v_boardtov_fe(vboard):
    return vboard*(-1/2)

#adc to v board (between -2 and 0 V)
def adctov_board(adc):
    return v_fetov_board(adctov_fe(adc))
def v_boardtoadc(vboard):
    return v_fetoadc(v_boardtov_fe(vboard))


def dbmtowatt(dbm):
    return 10*np.power(10., (dbm - 30) /10)

def dbtowatt(db):
    return 10*np.power(10., db)

def watttodb(db):
    return 10*np.log10(db)

def watttodbm(dbm):
    return 10*np.log10(dbm)



###############################################
####              filtering               #####
###############################################

def lowpass(amp, sampling, order, fcut):
    Nyfreq = sampling/2
    ratiofcut = float(fcut)/Nyfreq
    b, a = signal.butter(order, ratiofcut, 'low')
    filtered = signal.filtfilt(b, a, amp)
    return filtered

def lowpasshard(amp, sampling, fcut):
    fft = np.fft.rfft(amp)
    freq = np.fft.rfftfreq(len(fft),float(1./sampling))
    Nyfreq = sampling/2
    min = np.min(np.absolute(fft))
    ratiofcut = float(fcut)/Nyfreq
    size = len(fft)
    newpass = fft[:int(ratiofcut*size)]
    sizeofzeros = size - len(newpass)
    newcut = np.zeros(sizeofzeros)
    newfft = np.append(newpass,newcut)
    out = np.fft.irfft(newfft)
    return out.real

def highpass(amp, sampling, order, fcut):
    Nyfreq = sampling/2
    ratiofcut = float(fcut)/Nyfreq
    b, a = signal.butter(order, ratiofcut, 'high')
    filtered = signal.filtfilt(b, a, amp)
    return filtered


def slidingwindow(y,bins,option=None):                                          
    window = np.ones(bins)/bins                                                 
    if option is not None:                                                      
        if option.lower() not in ['full','same','valid']:                       
            print 'invalid option, check your sliding window'                   
    if option == None:                                                          
        return np.convolve(y,window,'same')                                     
    else:                                                                       
        return np.convolve(y,window,option) 




def rms(x):
    return np.sqrt(np.mean(x**2))


def produceresponse(time,amp,tau):
    tend = 500e-9
    period = time[1] - time[0]
    x = np.arange(0,tend,period)
    convfunc = period*np.exp(-x/tau)/( -(math.exp(-tend/tau) - 1)*tau)
    power = (amp**2)/50
    signal = 10*np.log10(power) + 30
    resp = np.convolve(signal,convfunc,'valid')
#    resp = np.convolve(signal,convfunc,'same')
    newtime = np.linspace(time[0], float(len(resp))*period, len(resp))
    newamp = resp
#    newwf = waveform.Waveform(newtime,newamp,'logresponse')
    return [newtime,newamp]

def powerdetfunc(x, k, j):
    a = 0.024
    return a*np.exp(-(k*x)) + j
def powerdetfunc2(x,a, k, j):
    return a*np.exp(-(k*x)) + j

def powerdetectorsim(time,amp,capaornot):
    logamp = watttodbm(amp*amp/50)
    freq = np.fft.rfftfreq(len(time),time[1]-time[0])
    fft = np.fft.rfft(logamp)
    # no capa
    if capaornot == 1: 
        file = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/test/capameanspec.npz'
        phase = np.load(file)['phase']
        freqori = np.load(file)['freq']
        interpphase = np.interp(freq,freqori,phase)
        a = 0.02260368
        k = 7.5661e-08
        j =  0.00139631
#        k = 7.77611495e-8
#        j = 1.39148723e-3
        spec = powerdetfunc2(freq,a,k,j)
        response = spec*np.exp(1j*interpphase)
        outfft = fft*response
        out = np.fft.irfft(outfft)
    if capaornot == 0: 
        file = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/test/nocapameanspec.npz'
        phase = np.load(file)['phase']
        freqori = np.load(file)['freq']
        interpphase = np.interp(freq,freqori,phase)
        a = 0.02253473
        k = 9.5678e-09
        j  = 0.00146526
#        k = 1.02232797e-08  
#        j = 1.49219664e-03
        spec = powerdetfunc2(freq,a,k,j)
        response = spec*np.exp(1j*interpphase)
        outfft = fft*response
        out = np.fft.irfft(outfft)
    return out

#find the best time delay to match the two waveforms
def finddelay(amp1,amp2):
    conv = np.correlate(amp1,amp2,'full')
    max = np.argmax(conv)
    l = len(conv)
#    print 'l = ', l
    #print 'max = ', max
    #ratio = float(max)/float(l)
    #argmax = int(ratio*len(amp2))
#    print max
#    return argmax
#    print conv
    return conv

def resize(amp1,amp2):
    difflen = len(amp1) - len(amp2)
    if difflen==1:
        return [amp1[:-1],amp2]
    elif difflen==-1:
        return [amp1,amp2[:-1]]
    elif len(amp1) > len(amp2):
        amp1 = amp1[difflen/2:-difflen/2]
    elif len(amp1) < len(amp2):
        amp2 = amp1[-difflen/2:difflen/2]
#    else:
#        print 'same size'
    return [amp1,amp2]

def gettime(time1,time2):
    difflen = len(time1) - len(time2)
    if len(time1) > len(time2):
        time1 = time1[difflen/2:-difflen/2]
    elif len(time1) < len(time2):
        time2 = time1[-difflen/2:difflen/2]
#    else:
#        print 'same size'
    return time1



def finddelay2(amp1,amp2):
    fftamp1 = np.fft.fft(amp1)
    fftamp2 = np.fft.fft(amp2)
    cfftamp1 = -fftamp1.conjugate()
    cfftamp2 = -fftamp2.conjugate()
#    print np.argmax(np.abs(np.fft.ifft(cfftamp1*fftamp2)))
#    print np.argmax(np.abs(np.fft.ifft(fftamp1*cfftamp2)))
    return np.argmax(np.abs(np.fft.ifft(fftamp1*cfftamp2)))


def resample(time, amp, newsampling):
    newtime = np.arange(time[0],time[-1],1/newsampling)
    newamp = np.interp(newtime,time,amp)
    return [newtime,newamp]
