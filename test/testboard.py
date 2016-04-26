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
import glob
#temp, gain, bw, tau of power det
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/Capa/'
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_05_10/NoCapa/'
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_03_25/HF_box/'
datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_03_25/calib_board/'
#datafolder = '/Users/romain/work/Auger/EASIER/LPSC/filter/data/2013_03_25/calib_board/'
files1 = glob.glob(datafolder+'C1pdboard200*')
files2 = glob.glob(datafolder+'C2pdboard200*')
mean1 = np.array([])
mean2 = np.array([])

vminusmean1 = np.array([])
vminusmean2 = np.array([])
for f1,f2 in zip(files1[:5],files2[:5]):
    wf1 = utils.readscopefile(f1)
    wf2 = utils.readscopefile(f2)
    [pd,board] = utils.resize(wf1[1],wf2[1])
    delay = utils.finddelay2(pd,board)
    board =  np.roll(board,delay)        
    m1 = np.mean(pd)
    m2 = np.mean(board)
    mean1 = np.append(mean1,m1)
    mean2 = np.append(mean2,m2)
#    vminusmean1 = np.append(vminusmean1, pd - m1)
#    vminusmean2 = np.append(vminusmean2, board - m2)
    plt.plot(pd,board)
#    vminusmean1 = np.append(vminusmean1,pd)
#    vminusmean2 = np.append(vminusmean2,board)

#plt.subplot(121)
# plt.plot(mean1,mean2,'ro')
# fit = np.polyfit(mean1,mean2,1)
# pfit = np.poly1d(fit)
# x = np.linspace(np.min(mean1),np.max(mean1),10)
# print fit
# plt.plot(x,pfit(x))
# plt.subplot(122)
# plt.plot(vminusmean1,vminusmean2)
# fit2 = np.polyfit(vminusmean1,vminusmean2,1)
# pfit2 = np.poly1d(fit)
# print fit2
plt.show()


# fig = plt.figure()
# plt.plot(pd,shiftedboard)
# fit = np.polyfit(pd,shiftedboard,1)
# pfit = np.poly1d(fit)
# simboard = pfit(pd)
# fig2 = plt.figure()
# plt.plot(shiftedboard)
# plt.plot(simboard)
# print fit


