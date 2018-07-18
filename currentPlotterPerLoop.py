import ROOT
from ROOT import TStyle, TH2, TH2F, TCanvas, TROOT, TLatex, TAttFill, TColor
import tdrStyle
import os
from array import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("4.1f")
ROOT.gStyle.SetPalette(87)

loopnames = [
[
"L1D1PN",
"L1D2MN",
"L1D1MF",
"L1D2PF",
],
[
"L2D1MN",
"L2D2PN",
"L2D1PF",
"L2D2MF",
],
[
"L3D1MN",
"L3D2PN",
"L3D3MN",
"L3D4PN",
"L3D1PF",
"L3D2MF",
"L3D3PF",
"L3D4MF",
],
[
"L4D1PN",
"L4D2MN",
"L4D3PN",
"L4D4MN",
"L4D1MF",
"L4D2PF",
"L4D3MF",
"L4D4PF",
],
]

inputFileName = "leakageCurrentsPerLoop.txt"
layer = ["L1","L2","L3","L4"]
sector = ["S1","S2","S3","S4","S5","S6","S7","S8"]

if(os.path.exists(inputFileName)):
    fin = open(inputFileName, "r+")
    lines = fin.readlines()

    for i,ilayer in enumerate(layer):
        frameHist = ROOT.TH2F("leakageCurrent","leakageCurrent",8,0,8,len(loopnames[i]),0,len(loopnames[i]))
        for ibinX in xrange(8):
            frameHist.GetXaxis().SetBinLabel(ibinX+1,str(ibinX+1))

        for iloop in xrange(len(loopnames[i])):
            if "PN" in loopnames[i][iloop]:
                frameHist.GetYaxis().SetBinLabel(iloop+1, loopnames[i][iloop] + "(BpI)")

            if "MN" in loopnames[i][iloop]:
                frameHist.GetYaxis().SetBinLabel(iloop+1, loopnames[i][iloop] + "(BmI)")

            if "PF" in loopnames[i][iloop]:
                frameHist.GetYaxis().SetBinLabel(iloop+1, loopnames[i][iloop] + "(BpO)")

            if "MF" in loopnames[i][iloop]:
                frameHist.GetYaxis().SetBinLabel(iloop+1, loopnames[i][iloop] + "(BmO)")

            for iSec in xrange(len(sector)):

                for l in lines:
                    line = l.split()

                    if (sector[iSec] in line[0]) and (loopnames[i][iloop] in line[1]) and (line[2]!="null"):
                        frameHist.SetBinContent(iSec+1,iloop+1,float(line[2]))

                    else:
                        continue


        canvas = ROOT.TCanvas("leakageCurrent","leakageCurrent",1300,1000)
        canvas.SetTopMargin(0.07)
        canvas.SetLeftMargin(0.25)
        canvas.SetRightMargin(0.15)
        canvas.SetBottomMargin(0.16)
        canvas.cd()

        frameHist.GetYaxis().SetTitle("cooling loop")
        frameHist.GetYaxis().SetTitleOffset(2.2)
        frameHist.GetYaxis().SetTitleSize(0.06)
        frameHist.GetYaxis().SetLabelSize(0.05)

        frameHist.GetXaxis().SetTitle("sector")
        frameHist.GetXaxis().SetTitleSize(0.07)
        frameHist.GetXaxis().SetLabelSize(0.05)

        frameHist.GetZaxis().SetLabelSize(0.03)
        frameHist.SetMarkerSize(1.5)
        frameHist.Draw("colztext")

        label = ROOT.TLatex(0.21,0.95, ilayer.replace("L","LYR") + " HV current [uA]")
        label.SetNDC()

        label.Draw("same")
        canvas.SaveAs("BPix_" + ilayer + "_leakageCurrent_2D.pdf")
