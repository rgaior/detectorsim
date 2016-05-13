kb = 1.38e-23
impedance = 50 # ohm


#############################
#### detector constants #####
#############################

## SD front end filter frequency cut ##
fefcut = 20e6 #Hz
## SD front end sampling rate ##
fesampling = 40e6 #S/s

########################
## constant for powerdetector with capacitor ##
##1rst method
c_powerdetoffset = 0.816
c_powerdetslope = -0.0217
c_powerdettau = 34.8e-9


## 3rd method
c3_powerdetoffset = 0.684
c3_powerdetslope = -0.0252
c3_powerdettau = 41.5e-9


##2nd method
##spec param:
c2_slope = -0.0252
c2_offset = 0.684
c2_prefact = 0.02408611
c2_k = 7.6977e-08
c2_j = 0.00138642
c2_dc = 0.04282547
#c2_file = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/test/capameanspec.npz'
c2_file = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/method2/capa/meanspec.npz'

## constant for power detector **without** capacitor ##
nc_powerdetoffset = 0.88
nc_powerdetslope = -0.0192
nc_powerdettau = 4.7e-9
##2nd method
##spec param:
nc2_slope = -0.0252
nc2_offset = 0.684
nc2_prefact = 0.02463391
nc2_k = 1.0523e-08
nc2_j = 0.00148898
nc2_dc = 0.04282547
#nc2_file = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/test/nocapameanspec.npz'
nc2_file = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/results/method2/nocapa/meanspec.npz'

## 3rd method
nc3_powerdetoffset = 0.684
nc3_powerdetslope = -0.0252
nc3_powerdettau = 6.3e-9

#########################
## board carac:
## 1rst method
boardoffset = 5.923
boardslope = -4.19
## 2nd method:
## spectrum paramaters:
boardspecprefact = 3.86
boardspecmu = -40
boardspecsigma = 75.1
boardspeck = 1
## phase param:
boardphasea = 4.8e-5
boardphaseb = -1.1e-3
boardphasec = 2.97


##############################
###    folder path    ########
##############################
basefolder = '/Users/romain/work/Auger/EASIER/LPSC/detectorsim/'
spectrafolder = basefolder + 'data/spectra/'
resultfolder = basefolder + 'results/'
calibdatafolder = basefolder + 'data/'
