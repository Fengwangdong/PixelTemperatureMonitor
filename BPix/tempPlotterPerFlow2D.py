import ROOT
from ROOT import TStyle, TFile, TH1, TH1D, TCanvas, TROOT, TLegend, TLatex, TKey, TString, TAttFill, TGraphAsymmErrors, TColor
import tdrStyle
import os
from array import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)

inputFileName3 = "ChangeCoolingFlow1/TS2Local/BeforeChangeFlow/temperatures_perloop.txt"
#inputFileName2 = "ChangeCoolingFlow1/TS2Local/AfterChangeFlow/temperatures_perloop.txt"
inputFileName2 = "ChangeCoolingFlow2/CosmicRun/BeforeChangeFlow/temperatures_perloop.txt"
inputFileName1 = "ChangeCoolingFlow2/CosmicRun/AfterChangeFlow/temperatures_perloop.txt"
fileList = [inputFileName1, inputFileName2, inputFileName3]
layer = ["LAY1","LAY2","LAY3","LAY4"]
auxlayer = ["L1","L2","L3","L4"]
flowList = [1.8, 2.0, 2.5]
phiunc = [15, 15, 7.5, 7.5]
colors = [1,2,4]
markers = [20,21,22]

tempVSFlow = {}

for i,index in enumerate(layer):
    tempVSFlow[i] = {}

    for j,iflow in enumerate(flowList):
        tempVSFlow[i][j] = [array('d'), array('d'), array('d'), array('d')]


for i,ilayer in enumerate(layer):

    for j,iflow in enumerate(flowList):
        fin = open(fileList[j], "r+")
        lines = fin.readlines()

        for l in lines:
            line = l.split()

            if (auxlayer[i] in line[0]):
                tempVSFlow[i][j][0].append(float(line[1]))
                tempVSFlow[i][j][1].append(float(line[2]))
                tempVSFlow[i][j][2].append(phiunc[i])
                tempVSFlow[i][j][3].append(0)


if len(tempVSFlow) > 0:

    for i,ilayer in enumerate(layer):

        frameHist = ROOT.TH1D("temperatures","temperatures", 20, 0, 360)
        frameHist.SetStats(0)
        frameHist.GetYaxis().SetRangeUser(-16,-4)
        frameHist.GetYaxis().SetTitle("Temperature [degC]")
        frameHist.GetYaxis().SetTitleOffset(1.3)
        frameHist.GetYaxis().SetTitleSize(0.05)
        frameHist.GetYaxis().SetLabelSize(0.04)
        frameHist.GetXaxis().SetTitle("#phi[*#pi/180 rad]")
        frameHist.GetXaxis().SetTitleOffset(1.)
        frameHist.GetXaxis().SetTitleSize(0.05)
        frameHist.GetXaxis().SetLabelSize(0.04)

        canvas = ROOT.TCanvas("temperatures","temperatures",900,900)
        canvas.SetTopMargin(0.05)
        canvas.SetLeftMargin(0.16)
        canvas.SetBottomMargin(0.13)
        canvas.cd()
        frameHist.Draw()

        label = ROOT.TLatex(0.48,0.87, ilayer)
        label.SetNDC()

        label2 = ROOT.TLatex(0.18,0.96, "CMS  2018")
        label2.SetNDC()

        label3 = ROOT.TLatex(0.21,0.89, "Preliminary")
        label3.SetNDC()
        label3.SetTextFont(52)
        label3.SetTextSize(0.04)

        legend = ROOT.TLegend(0.62,0.8,0.99,0.99)
        legend.SetFillColor(0)
        legend.SetTextSize(0.04)

        gr_temp = {}

        for k,iflow in enumerate(flowList):
            gr_temp[k] = ROOT.TGraphAsymmErrors(len(tempVSFlow[i][k][0]), tempVSFlow[i][k][0], tempVSFlow[i][k][1], tempVSFlow[i][k][2], tempVSFlow[i][k][2], tempVSFlow[i][k][3], tempVSFlow[i][k][3])
            gr_temp[k].SetLineColor(colors[k])
            gr_temp[k].SetLineWidth(4)
            gr_temp[k].SetMarkerSize(3)
            gr_temp[k].SetMarkerStyle(markers[k])
            gr_temp[k].SetMarkerColor(colors[k])

            legend.AddEntry(gr_temp[k],"CO_{2} flow: " + str(iflow) + "g/s","lpe")

            if k == 0:
                gr_temp[k].Draw("ep")
            else:
                gr_temp[k].Draw("ep same")

        legend.Draw("same")
        label.Draw("same")
        label2.Draw("same")
        label3.Draw("same")
        canvas.SaveAs("BPix_" + ilayer + "_temperatureVSflow2D.pdf")
