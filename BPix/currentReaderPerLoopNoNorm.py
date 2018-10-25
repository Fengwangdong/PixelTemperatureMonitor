from HVTempMap import *
from pgphimap import *
from phiunc import *
import os
import ROOT
from ROOT import TH1, TH1F

def getPhi(alias):

    phi = -999.0

    for j in pgphimap.keys():
        if j.find(alias) != -1:
            phi = float(pgphimap[j])
            break

    return phi


def getPhiUnc(alias):

    unc = -999.0

    for j in phiunc.keys():
        if j.find(alias) != -1:
            unc = float(phiunc[j])
            break

    return unc

fileName = "currentsFromDB.txt"
outputFile = "leakageCurrentsPerLoopNoNorm.txt"

if(os.path.exists(fileName)):
    fin = open(fileName, "r+")
    lines = fin.readlines()

    fout = open(outputFile,"w")

    for iSec in HVTempMap.keys():

        currentHist = ROOT.TH1F("leakageCurrent", "leakageCurrent", 500, 0, 5000)
        phi = getPhi(iSec)
        phiUnc = getPhiUnc(iSec)

        for l in lines:
            line = l.split()
            if iSec in line[0]:
                currentHist.Fill(float(line[1]))
                if float(line[1]) <= 100.0:
                    print "anomalous HV current (maybe off): ", line[0], "  ", line[1], "  ", line[2], "  ", line[3]

        if currentHist.GetEntries() == 0:
            fout.write(iSec + "   " + HVTempMap[iSec] + "   " + str(phi) + "   " + str(phiUnc) + "   " + "null" + "\n")

        else:
            averageCurrent = currentHist.GetMean()
            fout.write(iSec + "   " + HVTempMap[iSec] + "   " + str(phi) + "   " + str(phiUnc) + "   " + str(averageCurrent) + "\n")

        currentHist.Reset()

    fin.close()
    fout.close()
