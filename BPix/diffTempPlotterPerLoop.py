import ROOT
from ROOT import TStyle, TFile, TH1, TH1D, TCanvas, TROOT, TLegend, TLatex, TKey, TString, TAttFill, TGraphAsymmErrors, TColor
import tdrStyle
import os
from array import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)

inputFileName1 = "BeforeChangeFlow/temperatures_perloop.txt"
inputFileName2 = "AfterChangeFlow/temperatures_perloop.txt"
layer = ["L1","L2","L3","L4"]

data = {}

for j,index in enumerate(layer):
    data[j] = [array('d'), array('d'), array('d'), array('d')]

if(os.path.exists(inputFileName1) and os.path.exists(inputFileName2)):
    fin1 = open(inputFileName1, "r+")
    fin2 = open(inputFileName2, "r+")
    lines1 = fin1.readlines()
    lines2 = fin2.readlines()

    for l1 in lines1:
        line1 = l1.split()

        for l2 in lines2:
            line2 = l2.split()

            for i,ilayer in enumerate(layer):

                if (ilayer in line1[0]) and (line1[2]!="null") and (line1[3]!="null") and (line1[0] == line2[0]) and (line2[2]!="null") and (line2[3]!="null"):
                    data[i][0].append(float(line1[1]))
                    data[i][1].append(float(line1[2])-float(line2[2]))
                    data[i][2].append(0)

                    if (ilayer == "L1" or ilayer == "L2"):
                        data[i][3].append(45) # constant unc. for the phi

                    else:
                        data[i][3].append(22.5) # constant unc. for the phi

                else:
                    continue


    if len(data) > 0:

        for k,klayer in enumerate(layer):
            gr_temp = ROOT.TGraphAsymmErrors(len(data[k][0]), data[k][0], data[k][1], data[k][3], data[k][3], data[k][2], data[k][2])

            canvas = ROOT.TCanvas("temperatures","temperatures",900,900)
            canvas.SetTopMargin(0.05)
            canvas.SetLeftMargin(0.15)
            canvas.SetBottomMargin(0.18)
            canvas.cd()

            frameHist = ROOT.TH1D("temperatures","temperatures", 16, 0, 360)
            frameHist.SetStats(0)

            maxValue = max(data[k][1])

            frameHist.GetYaxis().SetRangeUser(0,2)
            frameHist.GetYaxis().SetTitle("Temperature (before - after) [degC]")
            frameHist.GetYaxis().SetTitleOffset(1.)
            frameHist.GetYaxis().SetTitleSize(0.06)
            frameHist.GetYaxis().SetLabelSize(0.05)

            frameHist.GetXaxis().SetTitle("#phi [*#pi/180 rad]")
            frameHist.GetXaxis().SetTitleSize(0.08)
            frameHist.GetXaxis().SetLabelSize(0.06)

            frameHist.Draw()

            gr_temp.SetLineColor(2)
            gr_temp.SetLineWidth(4)
            gr_temp.SetMarkerSize(4)
            gr_temp.SetMarkerStyle(20)
            gr_temp.SetMarkerColor(2)

            label = ROOT.TLatex(0.21,0.9, klayer.replace("L","LYR"))
            label.SetNDC()

            legend = ROOT.TLegend(0.55,0.87,0.99,0.99)
            legend.SetFillColor(0)
            legend.SetTextSize(0.04)
            legend.AddEntry(gr_temp,"BPix Cooling loop","lpe")

            gr_temp.Draw("ep same")
            legend.Draw("same")
            label.Draw("same")
            canvas.SaveAs("BPix_" + klayer + "_temperatureSpread_perloop.pdf")
