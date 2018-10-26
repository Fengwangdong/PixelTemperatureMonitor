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
"3I_L1D1PN",
"3R_L1D1PN",
"4I_L1D2MN",
"4M_L1D2MN",
"4R_L1D2MN",
"3I_L2D1MN",
"3M_L2D1MN",
"3R_L2D1MN",
"4M_L2D2PN",
"4R_L2D2PN",
"2I_L3D1MN",
"2R_L3D1MN",
"2I_L3D2PN",
"2M_L3D2PN",
"2R_L3D2PN",
"5I_L3D3MN",
"5M_L3D3MN",
"5R_L3D3MN",
"5I_L3D4PN",
"5M_L3D4PN",
"5R_L3D4PN",
"1I_L4D1PN",
"1M_L4D1PN",
"1R_L4D1PN",
"1I_L4D2MN",
"1M_L4D2MN",
"1R_L4D2MN",
"6I_L4D3PN",
"6M_L4D3PN",
"6R_L4D3PN",
"6I_L4D4MN",
"6M_L4D4MN",
"6R_L4D4MN",
"3I_L1D1MF",
"3M_L1D1MF",
"3R_L1D1MF",
"4I_L1D2PF",
"4R_L1D2PF",
"3I_L2D1PF",
"3M_L2D1PF",
"3R_L2D1PF",
"4M_L2D2MF",
"4R_L2D2MF",
"2I_L3D1PF",
"2M_L3D1PF",
"2R_L3D1PF",
"2I_L3D2MF",
"2M_L3D2MF",
"2R_L3D2MF",
"5I_L3D3PF",
"5M_L3D3PF",
"5R_L3D3PF",
"5I_L3D4MF",
"5M_L3D4MF",
"5R_L3D4MF",
"1I_L4D1MF",
"1M_L4D1MF",
"1R_L4D1MF",
"1I_L4D2PF",
"1M_L4D2PF",
"1R_L4D2PF",
"6I_L4D3MF",
"6M_L4D3MF",
"6R_L4D3MF",
"6I_L4D4PF",
"6M_L4D4PF",
"6R_L4D4PF"]

fileName = "temperatureFromDB_Corr.txt"
outputFile = "temperatures_perloop.txt"

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
            fout.write(index + "   " + str(phi) + "   " + "null" + "   " + "null" + "\n")

        else:
            aveTemp = tempHist.GetMean()
            uncTemp = tempHist.GetStdDev()
            fout.write(index + "   " + str(phi) + "   " + str(aveTemp) + "   " + str(uncTemp) + "\n")

        tempHist.Reset()


    fin.close()
    fout.close()
