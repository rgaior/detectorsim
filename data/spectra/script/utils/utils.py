import numpy as np

def readspectrum(filename):
    f = open(filename,'r')
    lines = f.readlines()
    nrpoint = 0
    freq = np.array([])
    power = np.array([])
    read =False
    count = 0
    for l in lines:
        if 'UI_DATA_POINTS' in l:
            nrpoint = int(float(l.split('=')[1][:-2]))
        if read == True and count < nrpoint:
            count +=1
            data = l.split('=')[1]
            f = float(data.split(',')[1][:-6])
            pow = float(data.split(',')[0])
            freq = np.append(freq,f)
            power = np.append(power,pow)
        if '# Begin TRACE A Data' in l:
            read = True
    return [freq,power]


def readspectrumtwocol(filename,skiprow=None):
    f = open(filename,'r')
    lines = f.readlines()
    freq = np.array([])
    power = np.array([])
    fromline = 0
    if skiprow is not None:
        fromline = skiprow
    
    for l in lines[fromline:]:
        fr  = float(l.split()[0])
        freq = np.append(freq, fr)
        p = float(l.split()[1])
        power = np.append(power, p)
    return [freq,power]

def lintolog(lin):
    return 10*np.log10(lin)
def logtolin(log):
    return np.power(10,log/10)
