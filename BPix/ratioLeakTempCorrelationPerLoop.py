import ROOT
from ROOT import TStyle, TFile, TH1, TH1D, TCanvas, TROOT, TLegend, TLatex, TKey, TString, TAttFill, TGraphAsymmErrors, TColor, TGaxis
import os
from array import array

leakInputFileName1 = "BeforeChangeFlow/leakageCurrentsPerLoopNoNorm.txt"
leakInputFileName2 = "AfterChangeFlow/leakageCurrentsPerLoopNoNorm.txt"
tempInputFileName1 = "BeforeChangeFlow/temperatures_perloop.txt"
tempInputFileName2 = "AfterChangeFlow/temperatures_perloop.txt"
layer = ["LAY1","LAY2","LAY3","LAY4"]
auxlayer = ["L1","L2","L3","L4"]

leakDataPlus = {}
leakDataMinus = {}
tempData = {}

for j,index in enumerate(layer):
    leakDataPlus[j] = [array('d'), array('d'), array('d'), array('d')]
    leakDataMinus[j] = [array('d'), array('d'), array('d'), array('d')]
    tempData[j] = [array('d'), array('d'), array('d'), array('d')]

if(os.path.exists(leakInputFileName1) and os.path.exists(leakInputFileName2) and os.path.exists(tempInputFileName1) and os.path.exists(tempInputFileName2)):
    finLeak1 = open(leakInputFileName1, "r+")
    finLeak2 = open(leakInputFileName2, "r+")
    linesLeak1 = finLeak1.readlines()
    linesLeak2 = finLeak2.readlines()

    finTemp1 = open(tempInputFileName1, "r+")
    finTemp2 = open(tempInputFileName2, "r+")
    linesTemp1 = finTemp1.readlines()
    linesTemp2 = finTemp2.readlines()

    for i,ilayer in enumerate(layer):

        for lLeak1 in linesLeak1:
            lineLeak1 = lLeak1.split()

            for lLeak2 in linesLeak2:
                lineLeak2 = lLeak2.split()

                if ilayer in lineLeak1[0] and ilayer in lineLeak2[0]:
                    if (("BpI" in lineLeak1[0]) or ("BpO" in lineLeak1[0])) and (lineLeak1[0] == lineLeak2[0]):
                        leakDataPlus[i][0].append(float(lineLeak1[2]))
                        leakDataPlus[i][1].append(float(lineLeak2[4])/float(lineLeak1[4]))
                        leakDataPlus[i][2].append(float(lineLeak1[3]))
                        leakDataPlus[i][3].append(float(0))

                    if (("BmI" in lineLeak1[0]) or ("BmO" in lineLeak1[0])) and (lineLeak1[0] == lineLeak2[0]):
                        leakDataMinus[i][0].append(float(lineLeak1[2]))
                        leakDataMinus[i][1].append(float(lineLeak2[4])/float(lineLeak1[4]))
                        leakDataMinus[i][2].append(float(lineLeak1[3]))
                        leakDataMinus[i][3].append(float(0))


        for lTemp1 in linesTemp1:
            lineTemp1 = lTemp1.split()

            for lTemp2 in linesTemp2:
                lineTemp2 = lTemp2.split()

                if (auxlayer[i] in lineTemp1[0]) and (lineTemp1[2]!="null") and (lineTemp1[0] == lineTemp2[0]) and (lineTemp2[2]!="null") and (lineTemp2[3]!="null"):
                    tempData[i][0].append(float(lineTemp1[1]))
                    tempData[i][1].append(0.5*(float(lineTemp1[2]) - float(lineTemp2[2])))

                    if (auxlayer[i] == "L1" or auxlayer[i] == "L2"):
                        tempData[i][2].append(45) # constant unc. for the phi

                    else:
                        tempData[i][2].append(22.5) # constant unc. for the phi

                    tempData[i][3].append(0)

    if len(leakDataPlus) > 0 and len(leakDataMinus) > 0 and len(tempData) > 0:

        for k,klayer in enumerate(layer):
            gr_plus = ROOT.TGraphAsymmErrors(len(leakDataPlus[k][0]), leakDataPlus[k][0], leakDataPlus[k][1], leakDataPlus[k][2], leakDataPlus[k][2], leakDataPlus[k][3], leakDataPlus[k][3])
            gr_minus = ROOT.TGraphAsymmErrors(len(leakDataMinus[k][0]), leakDataMinus[k][0], leakDataMinus[k][1], leakDataMinus[k][2], leakDataMinus[k][2], leakDataMinus[k][3], leakDataMinus[k][3])
            gr_temp = ROOT.TGraphAsymmErrors(len(tempData[k][0]), tempData[k][0], tempData[k][1], tempData[k][2], tempData[k][2], tempData[k][3], tempData[k][3])

            canvas = ROOT.TCanvas("temperatures","temperatures",900,900)
            canvas.SetTopMargin(0.09)
            canvas.SetLeftMargin(0.19)
            canvas.SetRightMargin(0.15)
            canvas.SetBottomMargin(0.14)
            canvas.cd()

            frameHist = ROOT.TH1F("","", 16, 0, 360)
            frameHist.SetStats(0)
            frameHist.GetYaxis().SetRangeUser(0,2)
            frameHist.GetYaxis().SetTitle("I_{leak}(after) / I_{leak}(before)")
            frameHist.GetYaxis().SetTitleOffset(1.6)
            frameHist.GetYaxis().SetTitleSize(0.05)
            frameHist.GetYaxis().SetLabelSize(0.04)
            frameHist.GetXaxis().SetTitle("#phi [*#pi/180 rad]")
            frameHist.GetXaxis().SetTitleSize(0.05)
            frameHist.GetXaxis().SetLabelSize(0.04)
            frameHist.Draw()

            gr_plus.SetLineColor(2)
            gr_plus.SetLineWidth(4)
            gr_plus.SetMarkerSize(3)
            gr_plus.SetMarkerStyle(20)
            gr_plus.SetMarkerColor(2)

            gr_minus.SetLineColor(4)
            gr_minus.SetLineWidth(4)
            gr_minus.SetMarkerSize(3)
            gr_minus.SetMarkerStyle(21)
            gr_minus.SetMarkerColor(4)

            gr_plus.Draw("ep same")
            gr_minus.Draw("ep same")
            canvas.Update()

            axis = TGaxis(ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax(), 0, 4, 510, "+L")
            axis.SetTitle("Temperature (before - after)[degC]")
            axis.SetTitleOffset(1.5)
            axis.SetLineColor(6)
            axis.SetTextColor(6)
            axis.SetLabelFont(42)
            axis.Draw()

            gr_temp.SetLineColor(6)
            gr_temp.SetLineWidth(4)
            gr_temp.SetMarkerSize(3)
            gr_temp.SetMarkerStyle(22)
            gr_temp.SetMarkerColor(6)

            label = ROOT.TLatex(0.68,0.75, klayer)
            label.SetNDC()

            label2 = ROOT.TLatex(0.2,0.93, "CMS")
            label2.SetNDC()

            label3 = ROOT.TLatex(0.23,0.86, "Preliminary")
            label3.SetNDC()
            label3.SetTextFont(52)
            label3.SetTextSize(0.04)

            legend = ROOT.TLegend(0.52,0.84,0.82,0.99)
            legend.SetFillColor(0)
            legend.SetTextSize(0.04)
            legend.AddEntry(gr_plus,"BPix+ I(leak)","lpe")
            legend.AddEntry(gr_minus,"BPix- I(leak)","lpe")
            legend.AddEntry(gr_temp,"BPix temp.","lpe")

            gr_temp.Draw("ep same")
            legend.Draw("same")
            label.Draw("same")
            label2.Draw("same")
            label3.Draw("same")
            canvas.SaveAs("BPix_" + klayer + "_LeakTempCorrRatio_perloop.pdf")
