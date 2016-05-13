#################################################################################
## finds and plot the V_board vs V_powerdet for the DC component and the rest ###
#################################################################################
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)
import numpy as np
from scipy.optimize import curve_fit
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
import glob


datafolder = constant.calibdatafolder+ '/2013_03_25/calib_board/'
files1 = glob.glob(datafolder+'C1pdboard200*')
files2 = glob.glob(datafolder+'C2pdboard200*')
mean1 = np.array([])
mean2 = np.array([])

vminusmean1 = np.array([])
vminusmean2 = np.array([])
count = 0
#for f1,f2 in zip(files1,files2):
for f1,f2 in zip(files1[:1],files2[:1]):
    wf1 = utils.readscopefile(f1)
    wf2 = utils.readscopefile(f2)
    [pd,board] = utils.resize(wf1[1],wf2[1])
    delay = utils.finddelay2(pd,board)
    board =  np.roll(board,delay)        
    fpd = np.fft.rfft(pd)
    fboard = np.fft.rfft(board)
    fboardfake = np.fft.rfft(-4*pd + 5.9)
    if count==0:
        firstphase = np.unwrap((np.unwrap( np.angle(fboard)  -  np.angle(fpd),discont=0.2*np.pi)),discont=0.5*np.pi)
        meanfpd = np.zeros(len(fpd))
        meanfboard = np.zeros(len(fboard))
        meanratio = np.zeros(len(fboard))
        meanratiofake = np.zeros(len(fboard))
        meanphase = np.zeros(len(fboard))
        meanphase2 = np.zeros(len(fboard))
        freq = np.fft.rfftfreq(len(pd), wf1[0][1] - wf1[0][0])
    meanfpd = meanfpd + np.absolute(fpd)
    meanfboard =  meanfboard + np.absolute(fboard)
    meanratiofake = meanratiofake + np.absolute(fboardfake)/np.absolute(fpd)
    meanratio = meanratio + np.absolute(fboard)/np.absolute(fpd)
    #    meanphase = meanphase +  np.angle(fboard) 
    #    meanphase = meanphase +  np.angle(fpd)
    meanphase = meanphase + np.unwrap((np.unwrap( np.angle(fboard)  -  np.angle(fpd),discont=0.2*np.pi)),discont=0.5*np.pi)
    meanphase2 = meanphase2 + np.angle(fboard)  -  np.angle(fpd)
    count+=1



#############################
###      fit of spec   ######
#############################
spec = meanratio/count
phase = firstphase
#freqM = freq
freqM = freq/1e6
def func(x, a,mu,sigma,j):
    return a*np.exp(-(x - mu)**2/(2*sigma**2)) + j
#print freqM
limfreq = 200
newspec = spec[ (freqM < limfreq) & (freqM > 2)]
newphase = phase[ (freqM < limfreq) & (freqM > 2)]
newfreq = freqM[ (freqM < limfreq) & (freqM > 2)]
guess = [4,0,60,1]
popt, pcov = curve_fit(func, newfreq, newspec,p0=guess)
fitphase = np.polyfit(newfreq,newphase,2)
polyphase = np.poly1d(fitphase)
print 'spectrum fit : ', popt
print 'phase fit : ' , fitphase



fig1 = plt.figure()
ax1 = plt.subplot(111)
#ax1.plot(freq/1e6,meanratio/count,label=' mean pd spectrum')
ax1.plot(newfreq,newspec,label='data',)
ax1.plot(newfreq,func(newfreq,popt[0],popt[1],popt[2],popt[3]),'r',lw=2,label='fit')
#ax1.plot(newfreq,func(newfreq,popt[0],popt[1],popt[2],popt[3],popt[4]),'r',lw=2,label='fit')
#ax1.plot(newfreq,func(newfreq,guess[0],guess[1],guess[2]),'g')
#ax1.plot(freq/1e6,meanratiofake/count,label=' mean pd spectrum')
ax1.set_xlabel('frequency [MHz]')
ax1.set_ylabel('spectrum ratio')
ax1.set_xlim(0,limfreq)
plt.legend()
fig2 = plt.figure()
ax2 = plt.subplot(111)
ax2.set_ylabel('phase difference [radian]')
ax2.set_xlabel('frequency [MHz]')
#ax2.plot(freq/1e6,meanphase/count,'.--',label=' mean pd spectrum')
ax2.plot(freq/1e6,firstphase,label='data')
#ax2.plot(newfreq,polyphase(newfreq),'r',lw=2,label='fit')
#ax2.plot(freq/1e6,meanphase2/count,'.--',label=' mean pd spectrum')
ax2.set_xlim(0,limfreq)
ax2.set_ylim(0,10)
plt.legend()
#ax1.plot(freq,meanfboard,label=' mean pd spectrum')

fig3 = plt.figure()
ax3 = plt.subplot(111)
ax3.semilogy(freq/1e6,meanfpd/count,label='power detector')
ax3.semilogy(freq/1e6,meanfboard/count,label='board')
ax3.set_xlabel('frequency [MHz]')
ax3.set_xlim(0,1000)
plt.legend()





plt.show()

