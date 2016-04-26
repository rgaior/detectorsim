from scipy.optimize import curve_fit
import numpy as np

import matplotlib.pyplot as plt

from lmfit import minimize, Parameters, Parameter, report_fit
def fcn2min(params, x, data):
    """ model decaying sine wave, subtract data"""
    a = params['a'].value
    b = params['b'].value
    k = params['k'].value
    j = params['j'].value
    model = a*np.exp(-(k*x)) + j + b*x
#    model = a * x + b                                                                                          
#    return (model - data)/dataerr
    return (model - data)


specfreq = np.load('capameanspec.npz')
#specfreq = np.load('nocapameanspec.npz')
spec = specfreq['spec']
freq = specfreq['freq']
spec = spec[(freq < 1e8)]
freq = freq[(freq < 1e8)]

#############################
###      fit of spec   ######
#############################
def func(x,a,b, k, j):
    return a*np.exp(-(k*x)) + j + b*x
#print freqM


params = Parameters()
params.add('a', value=0.024)
params.add('b',value = -1e-6,vary=True)
params.add('k', value=1e-8,vary=True)
params.add('j', value=1e-4,expr='0.024-a')

result = minimize(fcn2min, params, args=(freq,spec))
#print result
report_fit(result.params)

# guess = [1e-8,1e-4]
# popt, pcov = curve_fit(func, freq, spec,p0=guess)
# print popt
plt.plot(freq,spec)
plt.plot(freq,func(freq,result.params['a'].value,result.params['b'].value,result.params['k'].value,result.params['j'].value))
# plt.plot(freq,func(freq,popt[0],popt[1]))

plt.show()
