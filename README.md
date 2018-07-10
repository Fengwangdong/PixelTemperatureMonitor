# PixelTemperatureMonitor
This tool is implemented for the communication with CMS OMDS database and customized plotter on the pixel temperature. 

First step:
One needs to log on lxplus in order to include the Oracle base dependence. Then get the data points of pixel temperatures from the CMS database:

python getTempFromDB.py

Second step:
Compute the mean value and RMS of pixel temperature for each layer during a specific period.

python tempReader.py

Third step:
Use pyROOT to plot the temperature dependence in azimuth.

python tempPlotter.py

Enjoy!
