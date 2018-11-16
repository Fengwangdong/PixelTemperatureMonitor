import ROOT
from ROOT import TStyle, TFile, TH1, TH1D, TCanvas, TROOT, TLegend, TLatex, TKey, TString, TAttFill, TGraphAsymmErrors, TColor
import tdrStyle
import os
from array import array
import math

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)

#inputFileName3 = "ChangeCoolingFlow1/StableBeamRun/BeforeChangeFlow/temperatures_perloop.txt"
#inputFileName2 = "ChangeCoolingFlow2/StableBeamRun/BeforeChangeFlow/temperatures_perloop.txt"
#inputFileName1 = "ChangeCoolingFlow2/StableBeamRun/AfterChangeFlow/temperatures_perloop.txt"
inputFileName3 = "ChangeCoolingFlow1/TS2Local/BeforeChangeFlow/temperatures_perloop.txt"
inputFileName2 = "ChangeCoolingFlow2/CosmicRun/BeforeChangeFlow/temperatures_perloop.txt"
inputFileName1 = "ChangeCoolingFlow2/CosmicRun/AfterChangeFlow/temperatures_perloop.txt"
fileList = [inputFileName1, inputFileName2, inputFileName3]
layer = ["LAY1","LAY2","LAY3","LAY4"]
auxlayer = ["L1","L2","L3","L4"]
flowList = [1.8, 2.0, 2.5]
colors = [1,2,4,6]

inletTempVSFlow = {}
outletTempVSFlow = {}
diffTempVSFlow = {}

for j,index in enumerate(layer):
    inletTempVSFlow[j] = [array('d'), array('d'), array('d'), array('d')]
    outletTempVSFlow[j] = [array('d'), array('d'), array('d'), array('d')]
    diffTempVSFlow[j] = [array('d'), array('d'), array('d'), array('d')]

plots = [inletTempVSFlow, outletTempVSFlow]
plotName = ["Pixel Barrel Inlet", "Pixel Barrel Outlet"]

for i,ilayer in enumerate(layer):

    for ifile,iName in enumerate(fileList):
        fin = open(iName, "r+")
        lines = fin.readlines()

        inletTemp = ROOT.TH1F("","",20,-20,0)
        inletTemp.SetDirectory(0)
        outletTemp = ROOT.TH1F("","",20,-20,0)
        outletTemp.SetDirectory(0)

        for l in lines:
            line = l.split()

            if (auxlayer[i] in line[0]) and ("I" in line[0]):
                inletTemp.Fill(float(line[2]))

            if (auxlayer[i] in line[0]) and ("R" in line[0]):
                outletTemp.Fill(float(line[2]))


        inletTempVSFlow[i][0].append(flowList[ifile])
        inletTempVSFlow[i][1].append(inletTemp.GetMean())
        inletTempVSFlow[i][2].append(0)
        inletTempVSFlow[i][3].append(inletTemp.GetStdDev())

        outletTempVSFlow[i][0].append(flowList[ifile])
        outletTempVSFlow[i][1].append(outletTemp.GetMean())
        outletTempVSFlow[i][2].append(0)
        outletTempVSFlow[i][3].append(outletTemp.GetStdDev())

        diffTempVSFlow[i][0].append(flowList[ifile])
        diffTempVSFlow[i][1].append(inletTemp.GetMean()-outletTemp.GetMean())
        diffTempVSFlow[i][2].append(0)
        diffTempVSFlow[i][3].append(0)

if len(inletTempVSFlow) > 0 and len(outletTempVSFlow) > 0:

    for i,iplot in enumerate(plots):

        frameHist = ROOT.TH1D("temperatures","temperatures", 10, 1.5, 3)
        frameHist.SetStats(0)
        frameHist.GetYaxis().SetRangeUser(-16,-6)
        frameHist.GetYaxis().SetTitle("Temperature [degC]")
        frameHist.GetYaxis().SetTitleOffset(1.3)
        frameHist.GetYaxis().SetTitleSize(0.05)
        frameHist.GetYaxis().SetLabelSize(0.04)
        frameHist.GetXaxis().SetTitle("CO_{2} flow [g/s]")
        frameHist.GetXaxis().SetTitleOffset(1.)
        frameHist.GetXaxis().SetTitleSize(0.05)
        frameHist.GetXaxis().SetLabelSize(0.04)

        canvas = ROOT.TCanvas("temperatures","temperatures",900,900)
        canvas.SetTopMargin(0.05)
        canvas.SetLeftMargin(0.16)
        canvas.SetBottomMargin(0.13)
        canvas.cd()
        frameHist.Draw()

        label = ROOT.TLatex(0.5,0.96, plotName[i])
        label.SetNDC()
        label.SetTextFont(42)
        label.SetTextSize(0.04)

        label2 = ROOT.TLatex(0.18,0.96, "CMS  2018")
        label2.SetNDC()

        label3 = ROOT.TLatex(0.21,0.9, "Preliminary")
        label3.SetNDC()
        label3.SetTextFont(52)
        label3.SetTextSize(0.04)

        legend = ROOT.TLegend(0.85,0.81,0.99,0.99)
        legend.SetFillColor(0)
        legend.SetTextSize(0.04)

        gr_temp = {}

        for k,klayer in enumerate(layer):
            gr_temp[k] = ROOT.TGraphAsymmErrors(len(iplot[k][0]), iplot[k][0], iplot[k][1], iplot[k][2], iplot[k][2], iplot[k][3], iplot[k][3])
            gr_temp[k].SetLineColor(colors[k])
            gr_temp[k].SetLineWidth(4)
            gr_temp[k].SetMarkerSize(3)
            gr_temp[k].SetMarkerStyle(20)
            gr_temp[k].SetMarkerColor(colors[k])

            legend.AddEntry(gr_temp[k],klayer,"lpe")

            if k == 0:
                gr_temp[k].Draw("ep")
            else:
                gr_temp[k].Draw("ep same")

        legend.Draw("same")
        label.Draw("same")
        label2.Draw("same")
        label3.Draw("same")
        canvas.SaveAs(plotName[i].replace(" ","_") + "_temperatureVSflow.pdf")

#================= temperature difference between inlet and outlet ==================

    frameHist = ROOT.TH1D("temperatures","temperatures", 10, 1.5, 3)
    frameHist.SetStats(0)
    frameHist.GetYaxis().SetRangeUser(0,6)
    frameHist.GetYaxis().SetTitle("#Delta T (inlet - outlet) [degC]")
    frameHist.GetYaxis().SetTitleOffset(1.3)
    frameHist.GetYaxis().SetTitleSize(0.05)
    frameHist.GetYaxis().SetLabelSize(0.04)
    frameHist.GetXaxis().SetTitle("CO_{2} flow [g/s]")
    frameHist.GetXaxis().SetTitleOffset(1.)
    frameHist.GetXaxis().SetTitleSize(0.05)
    frameHist.GetXaxis().SetLabelSize(0.04)

    canvas = ROOT.TCanvas("temperatures","temperatures",900,900)
    canvas.SetTopMargin(0.05)
    canvas.SetLeftMargin(0.16)
    canvas.SetBottomMargin(0.13)
    canvas.cd()
    frameHist.Draw()

    label = ROOT.TLatex(0.6,0.96, "Pixel Barrel")
    label.SetNDC()
    label.SetTextSize(0.04)

    label2 = ROOT.TLatex(0.18,0.96, "CMS  2018")
    label2.SetNDC()

    label3 = ROOT.TLatex(0.21,0.9, "Preliminary")
    label3.SetNDC()
    label3.SetTextFont(52)
    label3.SetTextSize(0.04)

    legend = ROOT.TLegend(0.85,0.81,0.99,0.99)
    legend.SetFillColor(0)
    legend.SetTextSize(0.04)

    gr_temp_diff = {}

    for k,klayer in enumerate(layer):
        gr_temp_diff[k] = ROOT.TGraphAsymmErrors(len(diffTempVSFlow[k][0]), diffTempVSFlow[k][0], diffTempVSFlow[k][1], diffTempVSFlow[k][2], diffTempVSFlow[k][2], diffTempVSFlow[k][3], diffTempVSFlow[k][3])
        gr_temp_diff[k].SetLineColor(colors[k])
        gr_temp_diff[k].SetLineWidth(4)
        gr_temp_diff[k].SetMarkerSize(3)
        gr_temp_diff[k].SetMarkerStyle(20)
        gr_temp_diff[k].SetMarkerColor(colors[k])

        print diffTempVSFlow[k][1]

        legend.AddEntry(gr_temp_diff[k],klayer,"lpe")

        if k == 0:
            gr_temp_diff[k].Draw("ep")
        else:
            gr_temp_diff[k].Draw("ep same")

    legend.Draw("same")
    label.Draw("same")
    label2.Draw("same")
    label3.Draw("same")
    canvas.SaveAs("BPix_diffinletoutlet_temperatureVSflow.pdf")
