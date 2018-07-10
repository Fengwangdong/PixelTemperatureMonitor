import ROOT
from ROOT import TStyle, TFile, TH1, TH1D, TCanvas, TROOT, TLegend, TLatex, TKey, TString, TAttFill, TGraphAsymmErrors, TColor
import tdrStyle
import os
from array import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)

inputFileName = "temperatures.txt"
layer = ["L1","L2","L3","L4"]

dataPlus = {}
dataMinus = {}

for j,index in enumerate(layer):
    dataPlus[j] = [array('d'), array('d'), array('d'), array('d')]
    dataMinus[j] = [array('d'), array('d'), array('d'), array('d')]

if(os.path.exists(inputFileName)):
    fin = open(inputFileName, "r+")
    lines = fin.readlines()

    for l in lines:
        line = l.split()

        for i,ilayer in enumerate(layer):

            if ilayer in line[0]:
                if ("P" in line[0]):
                    dataPlus[i][0].append(float(line[1]))
                    dataPlus[i][1].append(float(line[2]))
                    dataPlus[i][2].append(float(line[3]))
                    dataPlus[i][3].append(45) # constant unc. for the phi

                elif("M" in line[0]):
                    dataMinus[i][0].append(float(line[1]))
                    dataMinus[i][1].append(float(line[2]))
                    dataMinus[i][2].append(float(line[3]))
                    dataMinus[i][3].append(45) # constant unc. for the phi

            else:
                continue


    if len(dataPlus) > 0 and len(dataMinus) > 0:

        for k,klayer in enumerate(layer):
            gr_plus = ROOT.TGraphAsymmErrors(len(dataPlus[k][0]), dataPlus[k][0], dataPlus[k][1], dataPlus[k][3], dataPlus[k][3], dataPlus[k][2], dataPlus[k][2])
            gr_minus = ROOT.TGraphAsymmErrors(len(dataMinus[k][0]), dataMinus[k][0], dataMinus[k][1], dataMinus[k][3], dataMinus[k][3], dataMinus[k][2], dataMinus[k][2])

            canvas = ROOT.TCanvas("temperatures","temperatures",900,900)
            canvas.SetTopMargin(0.05)
            canvas.SetLeftMargin(0.15)
            canvas.SetBottomMargin(0.18)
            canvas.cd()

            frameHist = ROOT.TH1D("temperatures","temperatures", 16, 0, 360)
            frameHist.SetStats(0)

            maxValue = max(dataPlus[k][1])
            if maxValue < max(dataMinus[k][1]):
                maxValue = max(dataMinus[k][1])

            frameHist.GetYaxis().SetRangeUser(-15,-4)
            frameHist.GetYaxis().SetTitle("Temperature [C]")
            frameHist.GetYaxis().SetTitleOffset(1.)
            frameHist.GetYaxis().SetTitleSize(0.06)
            frameHist.GetYaxis().SetLabelSize(0.05)

            frameHist.GetXaxis().SetTitle("#phi [*#pi/180 rad]")
            frameHist.GetXaxis().SetTitleSize(0.08)
            frameHist.GetXaxis().SetLabelSize(0.06)

            frameHist.Draw()

            gr_plus.SetLineColor(2)
            gr_plus.SetLineWidth(4)
            gr_plus.SetMarkerSize(4)
            gr_plus.SetMarkerStyle(20)
            gr_plus.SetMarkerColor(2)

            gr_minus.SetLineColor(4)
            gr_minus.SetLineWidth(4)
            gr_minus.SetMarkerSize(3)
            gr_minus.SetMarkerStyle(21)
            gr_minus.SetMarkerColor(4)

            label = ROOT.TLatex(0.21,0.9, klayer.replace("L","LYR"))
            label.SetNDC()

            legend = ROOT.TLegend(0.7,0.87,0.99,0.99)
            legend.SetFillColor(0)
            legend.SetTextSize(0.04)
            legend.AddEntry(gr_plus,"BPix_plus","lpe")
            legend.AddEntry(gr_minus,"BPix_minus","lpe")

            gr_plus.Draw("ep same")
            gr_minus.Draw("ep same")
            legend.Draw("same")
            label.Draw("same")
            canvas.SaveAs("BPix_" + klayer + "_temperature.pdf")
