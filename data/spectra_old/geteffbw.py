import numpy as np
import matplotlib.pyplot as plt


#fnames = ['easier61.txt','344.txt','norsat.txt']
fnames = ['wsitot.txt','344.txt','norsattot.txt']
legs = ['DMX241', 'GI301','Norsat8115']
c = 3e8
for fname,leg in zip(fnames,legs):
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
    print freq
    wl = c/(freq*1e9)
    aeff = g*wl**2/(4*np.pi)
    g = g/np.max(g)
    aeff = aeff/np.max(aeff)
    int = np.trapz(aeff,freq)
    print 'effective BW for ', leg, ' = ', int
    plt.plot(freq,aeff)


plt.show()
