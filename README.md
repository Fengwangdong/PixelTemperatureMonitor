# PixelTemperatureMonitor
This tool is implemented for the communication with CMS OMDS database and customized plotter on the pixel temperature. 

First step:
One needs to log on lxplus in order to include the Oracle base dependence. Then get the data points of pixel temperatures from the CMS database:

python getTempFromDB.py

Second step:
Since there are mis-matching between DCS and OMDS, one needs to correct the temperature values obtained from OMDS 
to match with DCS.

python checkMissDataAndCorrTempMap.py

Third step:
1) Compute the mean value and standard deviation of pixel temperature of each cooling loop for each layer 
during a specific period.

python tempPlotterPerLoop.py

2) Compute the mean value and standard deviation of temperature along different positions of each cooling loop for 
each layer during a specific period.

python tempReaderPerPosition.py

Forth step:
1) Use pyROOT to plot the temperature dependence in azimuth.

python tempPlotterPerLoop.py

2) Plot the 2D temperature dependence in different positions of each cooling loop.

python tempReaderPerPosition.py

In addition, this tool also provides function of 2D maps between leakage current channels and cooling loops. 

First step:
Fetch the HV current values from OMDS.

python getCurrentFromDB.py

Second step:
Read the HV current values in different channels mapping with cooling loops.

python currentReaderPerLoop.py

Third step:
Plot the 2D leakage current in each channel mapped with the corresponding cooling loop.

python currentPlotterPerLoop.py

Enjoy!
