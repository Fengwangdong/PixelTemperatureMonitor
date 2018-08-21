import ROOT
from ROOT import TStyle, TProfile2D, TCanvas, TROOT, TLatex, TAttFill, TColor
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


inputFileName = "temperatures_perposition.txt"
layer = ["L1","L2","L3","L4"]

if(os.path.exists(inputFileName)):
    fin = open(inputFileName, "r+")
    lines = fin.readlines()

    for i,ilayer in enumerate(layer):
        frameHist = ROOT.TProfile2D("temp","temp",len(loopnames[i]),0,len(loopnames[i]),3,0,3)
        frameHist.GetYaxis().SetBinLabel(1,"begin")
        frameHist.GetYaxis().SetBinLabel(2,"middle")
        frameHist.GetYaxis().SetBinLabel(3,"end")

        for iloop in xrange(len(loopnames[i])):
            frameHist.GetXaxis().SetBinLabel(iloop+1, loopnames[i][iloop])


            for l in lines:
                line = l.split()

                if (loopnames[i][iloop] in line[0]) and (line[1]!="null"):

                    if "I_" in line[0]:
                        frameHist.Fill(iloop,0,float(line[1]))

                    elif "M_" in line[0]:
                        frameHist.Fill(iloop,1,float(line[1]))

                    elif "R_" in line[0]:
                        frameHist.Fill(iloop,2,float(line[1]))

                else:
                    continue


        canvas = ROOT.TCanvas("temperatures","temperatures",900,900)
        canvas.SetTopMargin(0.07)
        canvas.SetLeftMargin(0.15)
        canvas.SetRightMargin(0.15)
        canvas.SetBottomMargin(0.16)
        canvas.cd()


        frameHist.GetYaxis().SetTitle("position")
        frameHist.GetYaxis().SetTitleOffset(1.)
        frameHist.GetYaxis().SetTitleSize(0.06)
        frameHist.GetYaxis().SetLabelSize(0.05)

        frameHist.GetXaxis().SetTitle("cooling loop")
        frameHist.GetXaxis().SetTitleSize(0.07)
        frameHist.GetXaxis().SetLabelSize(0.05)

        frameHist.GetZaxis().SetLabelSize(0.05)
        frameHist.SetMarkerSize(1.7)
        frameHist.Draw("colztext")

        label = ROOT.TLatex(0.21,0.95, ilayer.replace("L","LYR") + "  temperature [degC]")
        label.SetNDC()

        label.Draw("same")
        canvas.SaveAs("BPix_" + ilayer + "_temperature_2D.pdf")
