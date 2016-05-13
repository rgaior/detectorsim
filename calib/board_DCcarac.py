#################################################################################
## finds and plot the V_board vs V_powerdet for the DC component and the rest ###
#################################################################################
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)
import numpy as np
import os
import sys
cwd = os.getcwd()
utilspath = cwd + '/../utils/'
sys.path.append(utilspath)
import utils
import constant
import glob
#temp, gain, bw, tau of power det
datafolder = constant.calibdatafolder+ '/2013_03_25/calib_board/'
files1 = glob.glob(datafolder+'C1pdboard200*')
files2 = glob.glob(datafolder+'C2pdboard200*')
mean1 = np.array([])
mean2 = np.array([])

vminusmean1 = np.array([])
vminusmean2 = np.array([])
for f1,f2 in zip(files1[::5],files2[::5]):
    wf1 = utils.readscopefile(f1)
    wf2 = utils.readscopefile(f2)
    [pd,board] = utils.resize(wf1[1],wf2[1])
    delay = utils.finddelay2(pd,board)
    board =  np.roll(board,delay)        
    m1 = np.mean(pd)
    m2 = np.mean(board)
    #DC component
    mean1 = np.append(mean1,m1)
    mean2 = np.append(mean2,m2)
    #non DC component
    vminusmean1 = np.append(vminusmean1, pd - m1)
    vminusmean2 = np.append(vminusmean2, board - m2)

fig1 = plt.figure()
ax1 = plt.subplot(111)
ax1.plot(mean1,mean2,'ro',label='mean waveform')
fit = np.polyfit(mean1,mean2,1)
pfit = np.poly1d(fit)
x = np.linspace(np.min(mean1),np.max(mean1),10)
print fit
ax1.plot(x,pfit(x),label='linear fit')
ax1.text(0.01, 0.1, 'fit results: \n V_board = '+ str("%.3f" % fit[0])+ ' V_pd + ' +str("%.3f" % fit[1]) ,
        verticalalignment='top', horizontalalignment='left',
        transform=ax1.transAxes,
        color='black', fontsize=15)
ax1.set_xlabel('power detector [V]')
ax1.set_ylabel('EASIER board[V]')
plt.legend()

fig1 = plt.figure()
ax2 = plt.subplot(111)
plt.plot(vminusmean1,vminusmean2,'.',alpha=0.3,label='data')
fit2 = np.polyfit(vminusmean1,vminusmean2,1)
pfit2 = np.poly1d(fit2)
ax2.text(0.01, 0.1, 'fit results: \n V_board = '+ str("%.3f" % fit2[0])+ ' V_pd + ' + str("%.3f" % fit2[1]) ,verticalalignment='top', horizontalalignment='left',
        transform=ax2.transAxes,
        color='black', fontsize=15)
print fit2
x2 = np.linspace(np.min(vminusmean1),np.max(vminusmean1),10)
ax2.set_xlabel('power detector (mean subtracted) [V]')
ax2.set_ylabel('EASIER board (mean subtracted) [V]')
plt.plot(x2,pfit2(x2),label='linear fit')
plt.legend()
plt.show()

