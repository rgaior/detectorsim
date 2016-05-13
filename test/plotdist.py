###############################################
###script to plot the residual distribution ###
###############################################

import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('xtick', labelsize=15)
matplotlib.rc('ytick', labelsize=15)
from matplotlib import gridspec
import numpy as np
import os
import sys
cwd = os.getcwd()
utilspath = cwd + '/../utils/'
sys.path.append(utilspath)
import utils
import constant

method = int(sys.argv[1])
resultfolder = constant.resultfolder 
'/residuals/nocapa/distnocapa'+str(method)+'.npz'
nocapa = np.load(resultfolder + '/residuals/nocapa/distnocapa_'+str(method)+'.npz')
capa = np.load(resultfolder + '/residuals/capa/distcapa_'+str(method)+'.npz')

bins = np.linspace(-0.2,0.2,100)
fig = plt.figure()
fig.suptitle('method: ' + str(method), fontsize=15, fontweight='bold')
ax = plt.subplot(111)
ax.hist(nocapa['arr_0'],bins=bins,histtype='step',lw=2,log=True,label='no capacitor')
ax.hist(capa['arr_0'],bins=bins,histtype='step',lw=2,log=True,label='with capacitor')
ax.set_xlabel('V_sim - V_meas [V]')
ax.text(0.01, 0.95, 'std = ' + str("%.3f" % np.std(nocapa['arr_0']) + ' V'),
        verticalalignment='top', horizontalalignment='left',
        transform=ax.transAxes,
        color='blue', fontsize=15)
ax.text(0.01, 0.85, 'std = ' + str("%.3f" % np.std(capa['arr_0']) + ' V'),
        verticalalignment='top', horizontalalignment='left',
        transform=ax.transAxes,
        color='green', fontsize=15)
plt.legend()


plt.show()
