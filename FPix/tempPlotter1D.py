import ROOT
from ROOT import TStyle, TFile, TH1, TH1F, TCanvas, TROOT, TLegend, TLatex, TKey, TString, TAttFill, TColor
import tdrStyle
import os
from array import array

tdrStyle.setTDRStyle()
ROOT.gStyle.SetErrorX(0.5)

inputFileName = "temperatureFromDB.txt"
cylinder = ["BmI","BmO","BpI","BpO"]

if(os.path.exists(inputFileName)):
    fin = open(inputFileName, "r+")
    lines = fin.readlines()

    for idisk in xrange(3):

        histSFI = ROOT.TH1F("SFI","SFI",4,0,4)
        histSFO = ROOT.TH1F("SFO","SFO",4,0,4)
        histdiskI = ROOT.TH1F("diskI","diskI",4,0,4)
        histdiskO = ROOT.TH1F("diskO","diskO",4,0,4)

        for ibin,ihc in enumerate(cylinder):

            for l in lines:
                line = l.split()

                if ihc in line[0]:
                    if ("Disk" in line[0]) and ("I" in line[0]) and (str(idisk+1) in line[0]):
                        histdiskI.SetBinContent(ibin+1,float(line[1]))
                        histdiskI.SetBinError(ibin+1,0)

                    if ("Disk" in line[0]) and ("O" in line[0]) and (str(idisk+1) in line[0]):
                        histdiskO.SetBinContent(ibin+1,float(line[1]))
                        histdiskO.SetBinError(ibin+1,0)

                    if ("I_SF" in line[0]) and (str(idisk+1) in line[0]):
                        histSFI.SetBinContent(ibin+1,float(line[1]))
                        histSFI.SetBinError(ibin+1,0)

                    if ("O_SF" in line[0]) and (str(idisk+1) in line[0]):
                        histSFO.SetBinContent(ibin+1,float(line[1]))
                        histSFO.SetBinError(ibin+1,0)

                else:
                    continue


        canvas = ROOT.TCanvas("temperatures","temperatures",900,900)
        canvas.SetTopMargin(0.08)
        canvas.SetLeftMargin(0.2)
        canvas.SetBottomMargin(0.12)
        canvas.cd()

        maxValue = max(histSFI.GetMaximum(), histSFO.GetMaximum(), histdiskI.GetMaximum(), histdiskO.GetMaximum())
        minValue = min(histSFI.GetMinimum(), histSFO.GetMinimum(), histdiskI.GetMinimum(), histdiskO.GetMinimum())

        frameHist = ROOT.TH1D("temperatures","temperatures", 4, 0, 4)
        frameHist.SetStats(0)
        for ibin,ihc in enumerate(cylinder):
            frameHist.GetXaxis().SetBinLabel(ibin+1, ihc)

        frameHist.GetYaxis().SetRangeUser(minValue*1.2,maxValue*0.8)
        frameHist.GetYaxis().SetTitle("Temperature [degC]")
        frameHist.GetYaxis().SetTitleOffset(1.4)
        frameHist.GetYaxis().SetTitleSize(0.06)
        frameHist.GetYaxis().SetLabelSize(0.05)
        frameHist.GetXaxis().SetLabelSize(0.06)

        frameHist.Draw()

        histSFI.SetLineColor(2)
        histSFI.SetLineWidth(4)
        histSFI.SetMarkerSize(4)
        histSFI.SetMarkerStyle(20)
        histSFI.SetMarkerColor(2)

        histSFO.SetLineColor(4)
        histSFO.SetLineWidth(4)
        histSFO.SetMarkerSize(4)
        histSFO.SetMarkerStyle(21)
        histSFO.SetMarkerColor(4)

        histdiskI.SetLineColor(6)
        histdiskI.SetLineWidth(4)
        histdiskI.SetMarkerSize(4)
        histdiskI.SetMarkerStyle(22)
        histdiskI.SetMarkerColor(6)

        histdiskO.SetLineColor(8)
        histdiskO.SetLineWidth(4)
        histdiskO.SetMarkerSize(4)
        histdiskO.SetMarkerStyle(33)
        histdiskO.SetMarkerColor(8)

        label = ROOT.TLatex(0.21, 0.93, "FPix Disk" + str(idisk+1))
        label.SetNDC()

        legend = ROOT.TLegend(0.72,0.77,0.99,0.99)
        legend.SetFillColor(0)
        legend.SetTextSize(0.03)
        legend.AddEntry(histSFI,"Supply Flow In","lpe")
        legend.AddEntry(histSFO,"Supply Flow out","lpe")
        legend.AddEntry(histdiskI,"Disk in","lpe")
        legend.AddEntry(histdiskO,"Disk out","lpe")

        histSFI.Draw("ep same")
        histSFO.Draw("ep same")
        histdiskI.Draw("ep same")
        histdiskO.Draw("ep same")
        legend.Draw("same")
        label.Draw("same")
        canvas.SaveAs("FPix_disk_" + str(idisk+1) + "_temperature_1D.pdf")
