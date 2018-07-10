from phimap import *
import os
import ROOT
from ROOT import TH1, TH1F

def getPhi(alias):

    phi = -999.0

    for j in phimap.keys():
        if j.find(alias)!=-1:
            phi = float(phimap[j])
            break

    return phi


loopnames = [
"L1D1PN",
"L1D2MN",
"L2D1MN",
"L2D2PN",
"L3D1MN",
"L3D2PN",
"L3D3MN",
"L3D4PN",
"L4D1PN",
"L4D2MN",
"L4D3PN",
"L4D4MN",
"L1D1MF",
"L1D2PF",
"L2D1PF",
"L2D2MF",
"L3D1PF",
"L3D2MF",
"L3D3PF",
"L3D4MF",
"L4D1MF",
"L4D2PF",
"L4D3MF",
"L4D4PF"]

fileName = "temperatureFromDB.txt"
outputFile = "temperatures.txt"

if(os.path.exists(fileName)):
    fin = open(fileName, "r+")
    lines = fin.readlines()

    fout = open(outputFile,"w")

    for index in loopnames:

        phi = getPhi(index)
        tempHist = ROOT.TH1F("temperature", "temperature", 200, -20, 0)

        for l in lines:
            line = l.split()

            if index in line[0]:
                tempHist.Fill(float(line[1]))

        if tempHist.GetEntries() == 0:
            fout.write(index + "   " + str(phi) + "   " + str(0) + "   " + str(0) + "\n")

        else:
            aveTemp = tempHist.GetMean()
            uncTemp = tempHist.GetStdDev()
            fout.write(index + "   " + str(phi) + "   " + str(aveTemp) + "   " + str(uncTemp) + "\n")

        tempHist.Reset()


    fin.close()
    fout.close()
