# detectorsim
## Synopsis
This code contains the EASIER/GIGADUCK detector simulation.
It contains the following folders: 
- data/: several types of data including calibration data, spectra
- utils/: utils.py (utility functions)  constant.py (constant needed for the simulation and path)
- classes/: classes needed for the simulation of a radio trace
- calib/: folder with the codes to find the electronics parameters for the power detector and the easier board
- results/: where the calibration results are kept
- test/: test funtions
- analysis/: more complicated functions (to be completed)

## Code example
analysis/simwf.py : perfoms the simulation of a waveform according the detector type and method to simulate the power detector.
(refer to the detector simulation note for details about the simulation method)
ex:  
python simwf gi 2 
runs thes simulation for the GI antenna with the method 2 



