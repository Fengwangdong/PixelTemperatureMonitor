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
        frameHist.GetYaxis().SetBinLabel(1,"inlet")
        frameHist.GetYaxis().SetBinLabel(2,"middle")
        frameHist.GetYaxis().SetBinLabel(3,"outlet")

        for iloop in xrange(len(loopnames[i])):
            frameHist.GetXaxis().SetBinLabel(iloop+1, str(iloop+1))


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


        canvas = ROOT.TCanvas("temperatures","temperatures",1200,900)
        canvas.SetTopMargin(0.08)
        canvas.SetLeftMargin(0.16)
        canvas.SetRightMargin(0.18)
        canvas.SetBottomMargin(0.14)
        canvas.cd()

        frameHist.GetYaxis().SetTitle("temperature probe position")
        frameHist.GetYaxis().SetTitleOffset(1.3)
        frameHist.GetYaxis().SetTitleSize(0.06)
        frameHist.GetYaxis().SetLabelSize(0.06)

        frameHist.GetXaxis().SetTitle("cooling loop")
        frameHist.GetXaxis().SetTitleOffset(1.)
        frameHist.GetXaxis().SetTitleSize(0.06)
        frameHist.GetXaxis().SetLabelSize(0.06)

        frameHist.GetZaxis().SetLabelSize(0.05)
        frameHist.GetZaxis().SetTitle(ilayer.replace("L","Layer") + "  temperature [degC]")
        frameHist.GetZaxis().SetTitleOffset(1.2)
        frameHist.GetZaxis().SetRangeUser(-16,-8)
        frameHist.SetMarkerSize(1.7)
        frameHist.Draw("colztext")

        label2 = ROOT.TLatex(0.19,0.94, "CMS  2018")
        label2.SetNDC()

        label3 = ROOT.TLatex(0.46,0.94, "Preliminary")
        label3.SetNDC()
        label3.SetTextFont(52)
        label3.SetTextSize(0.04)

        label2.Draw("same")
        label3.Draw("same")
        canvas.SaveAs("BPix_" + ilayer + "_temperature_2D.pdf")
