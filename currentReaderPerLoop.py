from HVTempMap import *
import os
import ROOT
from ROOT import TH1, TH1F

fileName = "currentsFromDB.txt"
outputFile = "leakageCurrentsPerLoop.txt"

if(os.path.exists(fileName)):
    fin = open(fileName, "r+")
    lines = fin.readlines()

    fout = open(outputFile,"w")

    for iSec in HVTempMap.keys():

        currentHist = ROOT.TH1F("leakageCurrent", "leakageCurrent", 300, 0, 3000)

        for l in lines:
            line = l.split()
            if iSec in line[0]:
                currentHist.Fill(float(line[1]))
                if float(line[1]) <= 100.0:
                    print "anomalous HV current (maybe off): ", line[0], "  ", line[1], "  ", line[2], "  ", line[3]

        if currentHist.GetEntries() == 0:
            fout.write(iSec + "   " + HVTempMap[iSec] + "   " + "null" + "   " + "null" + "\n")

        else:
            averageCurrent = currentHist.GetMean()
            uncCurrent = currentHist.GetStdDev()
            fout.write(iSec + "   " + HVTempMap[iSec] + "   " + str(averageCurrent) + "   " + str(uncCurrent) + "\n")

        currentHist.Reset()

    fin.close()
    fout.close()
