import numpy as np
import matplotlib.pyplot as plt


fnames = ['easier61.txt','344.txt','norsat.txt']
legs = ['DMX241', 'GI301','Norsat8115']

fig = plt.figure(figsize=(12,6))
ax1 = plt.subplot(121)
ax2 = plt.subplot(122)

for fname, leg in zip(fnames,legs):
    f = open(fname,'r')
    lines = f.readlines()
    freq = np.array([])
    power = np.array([])
    for l in lines[1:]:
        ls = l.split()
        freq = np.append(freq,float(ls[0]))
        power = np.append(power,float(ls[1]))
    if fname == 'norsat.txt':
        freq = freq/1000
    g = np.power(10,power/10)
    g = g/np.max(g)
    gdb  =10*np.log10(g)
    ax1.plot(freq,gdb,label=leg)
    ax2.plot(freq,g,label=leg)

ax1.set_ylabel('normalized gain [dB]')
ax1.set_xlabel('frequency [GHz]')
ax1.set_xlim(3,4.5)
ax1.set_ylim(-10,1)
ax2.set_ylabel('normalized gain [linear]')
ax2.set_xlabel('frequency [GHz]')
ax2.set_xlim(3,4.5)
plt.legend(loc=3)
plt.show()
