from HVTempMap import *
from numberOfROCs import *
import os
import ROOT
from ROOT import TH1, TH1F

def getLeakageCurrent(alias, currentValue):
    rocCurrent = 0.

    for k in numberOfRocs.keys():

        if k.find(alias)!=-1:
            rocCurrent = currentValue/float(numberOfRocs[k])
            break

    return rocCurrent


fileName = "currentsFromDB.txt"
outputFile = "leakageCurrentsPerLoop.txt"

if(os.path.exists(fileName)):
    fin = open(fileName, "r+")
    lines = fin.readlines()

    fout = open(outputFile,"w")

    for iSec in HVTempMap.keys():

        currentHist = ROOT.TH1F("leakageCurrent", "leakageCurrent", 500, 0, 5000)

        for l in lines:
            line = l.split()
            if iSec in line[0]:
                currentHist.Fill(float(line[1]))
                if float(line[1]) <= 100.0:
                    print "anomalous HV current (maybe off): ", line[0], "  ", line[1], "  ", line[2], "  ", line[3]

        if currentHist.GetEntries() == 0:
            fout.write(iSec + "   " + HVTempMap[iSec] + "   " + "null" + "\n")

        else:
            averageCurrent = currentHist.GetMean()
            rocCurrent = getLeakageCurrent(iSec, averageCurrent)
            fout.write(iSec + "   " + HVTempMap[iSec] + "   " + str(rocCurrent) + "\n")

        currentHist.Reset()

    fin.close()
    fout.close()
