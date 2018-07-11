#!/usr/bin/env python
import os, subprocess, sys
import os, sys, time,math
import ROOT
from optparse import OptionParser
from collections import OrderedDict
execfile("../python/data_manager.py")
ROOT.gStyle.SetOptStat(0)

from optparse import OptionParser
parser = OptionParser()
parser.add_option(
    "--input", type="string", dest="input",
    help="A valid file with the shapes as output of combine FitDiagnostics",
    default="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/tth-bdt-training/treatDatacards/gpetrucc_2017/posfit_3poi_ttVFromZero/ttH_fitDiagnostics.Test_shapes.root"
    )
parser.add_option(
    "--odir", type="string", dest="odir",
    help="Directory for the output plots",
    default="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/tth-bdt-training/treatDatacards/gpetrucc_2017/posfit_3poi_ttVFromZero/"
    )
parser.add_option(
    "--original", type="string", dest="original",
    help="The original datacard: used only to rebin",
    default="none"
    )
parser.add_option(
    "--channel", type="string", dest="channel",
    help="Name of the category as it is appear on the input file",
    default="ttH_1l_2tau_OS"
    )
parser.add_option(
    "--labelX ", type="string", dest="labelX",
    help="To appear on final plot",
    default="BDT"
    )
parser.add_option(
    "--useLogPlot", action="store_true", dest="useLogPlot",
    help="Self explanatory",
    default=False
    )
parser.add_option(
    "--notFlips", action="store_true", dest="notFlips",
    help="Self explanatory",
    default=False
    )
parser.add_option(
    "--notConversions", action="store_true", dest="notConversions",
    help="Self explanatory",
    default=False
    )
parser.add_option(
    "--MC_IsSplit", action="store_true", dest="MC_IsSplit",
    help="If the MC components on card are separated as 'gentau' and 'faketau' ",
    default=False
    )
parser.add_option(
    "--divideByBinWidth", action="store_true", dest="divideByBinWidth",
    help="If final plot shall be done dividing bin content by bin width ",
    default=False
    )
parser.add_option(
    "--doMultilep", action="store_false", dest="doMultilep",
    help="Do subcategories from multilepton cards ",
    default=True
    )
parser.add_option(
    "--unblind", action="store_true", dest="unblind",
    help="Do subcategories from multilepton cards ",
    default=False
    )
parser.add_option(
    "--doPostFit", action="store_true", dest="doPostFit",
    help="Do the postfit instead of prefit ",
    default=False
    )
parser.add_option(
    "--minY", type="float", dest="minY",
    help="For the final plot",
    default=0.
    )
parser.add_option(
    "--maxY", type="float", dest="maxY",
    help="For the final plot",
    default=1.
    )
parser.add_option(
    "--fromHavester", action="store_true", dest="fromHavester",
    help="The input file is from CombineHavester. In this case you do not need to enter 'original' if you called the PostFitShapesFromWorkspace with the -d option",
    default=False
    )
(options, args) = parser.parse_args()

divideByBinWidth = options.divideByBinWidth
category = options.channel
print ("category", category)

labelY = "Events"
if divideByBinWidth : labelY = "Events / bin width"

if options.doPostFit :
    if not options.fromHavester :
        folder = "shapes_fit_s/"+category
        folder_data = "shapes_fit_s/"+category # it is a TGraphAsymmErrors, not histogram
        typeFit = "postfit"
    else :
        folder = category+"_postfit"
        folder_data = category+"_postfit" # it is a histogram
        typeFit = "postfit"
else :
    if not options.fromHavester :
        folder = "shapes_prefit/"+category
        folder_data = "shapes_prefit/"+category # it is a TGraphAsymmErrors, not histogram
        typeFit = "prefit"
    else :
        folder = category+"_prefit"
        folder_data = category+"_prefit" # it is a histogram
        typeFit = "prefit"

if not options.fromHavester : name_total = "total"
else : name_total = "TotalProcs"

if "tau" not in category :
    conversions = "Convs"
    fakes       = "data_fakes"
    flips       = "data_flips"
else :
    conversions = "conversions"
    fakes       = "fakes_data"
    flips       = "flips_data"

dprocs = OrderedDict()
if not options.MC_IsSplit :
    # if label == "none" it means that this process is to be merged with the anterior key
    #                      color, fillStype, label,       , make border
    dprocs[fakes]        = [1,     3005,      "Mis.",        True]
    dprocs[flips]        = [1,     3004,      "Flips",       True]
    dprocs[conversions]  = [5,     1001,      "Conversions", True]
    dprocs["Rares"]      = [851,   1001,      "Rares",       True]
    dprocs["EWK"]        = [610,   1001,      "EWK",         True]
    dprocs["TTW"]        = [823,   1001,      "none",        False]
    dprocs["TTWW"]       = [823,   1001,      "ttW + ttWW",        True]
    dprocs["TTZ"]        = [822,   1001,      "ttZ",         True]
    dprocs["ttH_hzg"]    = [2,     1001,      "none",        False]
    dprocs["ttH_hww"]    = [2,     1001,      "none",        False]
    dprocs["ttH_hzz"]    = [2,     1001,      "none",        False]
    dprocs["ttH_hmm"]    = [2,     1001,      "none",        False]
    dprocs["ttH_htt"]    = [2,     1001,      "ttH",     True]
    #})
else :
    # if label == "none" it means that this process is to be merged with the anterior key
    #                      color, fillStype, label,       , make border
    dprocs[fakes]        = [1,     3005,      "Mis.",        True]
    dprocs[flips]        = [1,     3004,      "Flips",       True]
    dprocs[conversions]  = [5,     1001,      "Conversions", True]
    dprocs["Rares_faketau"]  = [851,   1001,      "none",       False]
    dprocs["Rares_gentau"]   = [851,   1001,      "Rares",       True]
    dprocs["EWK_faketau"]    = [610,   1001,      "none",       False]
    dprocs["EWK_gentau"]     = [610,   1001,      "EWK",         True]
    dprocs["TTWW_faketau"]    = [823,   1001,      "none",         False]
    dprocs["TTWW_gentau"]     = [823,   1001,      "none",         False]
    dprocs["TTW_faketau"]   = [823,   1001,      "none",        False]
    dprocs["TTW_gentau"]    = [823,   1001,      "ttW + ttWW",  True]
    dprocs["TTZ_faketau"]    = [822,   1001,      "none",       False]
    dprocs["TTZ_gentau"]     = [822,   1001,      "TTZ",         True]
    dprocs["ttH_fake"]       = [682,   1001,      "none",     False]
    dprocs["ttH_hzg_gentau"] = [2,   1001,      "none",     False]
    dprocs["ttH_hww_gentau"] = [2,   1001,      "none",     False]
    dprocs["ttH_hzz_gentau"] = [2,   1001,      "none",     False]
    dprocs["ttH_hmm_gentau"] = [2,   1001,      "none",     False]
    dprocs["ttH_htt_gentau"] = [2,   1001,      "ttH",     True]

label_head = "teste"
if "1l_2tau" in category :
    label_head = "1l 2#tau"
    ## remove "fakes_data" from first entry and add as last
    del dprocs[fakes]
    dprocs[fakes] =      [1,     3005,      "Mis.",        True]
if "2l_2tau" in category :
    label_head = "2l 2#tau"
if "3l_1tau" in category :
    label_head = "3l 1#tau"
if "2lss_1tau" in category :
    label_head = "2lss 1#tau"

if typeFit == "prefit" : label_head = label_head+" "+typeFit
print label_head

if options.notFlips : del dprocs[flips]
if options.notConversions : del dprocs[conversions]
print ("will draw processes", list(dprocs.keys()))

if not options.original == "none" :
    fileOrig = options.original
    readFrom = category+"/data_obs"
else :
    fileOrig = options.input
    readFrom = folder+"/data_obs"
fileorriginal = ROOT.TFile(fileOrig)
template = fileorriginal.Get(readFrom)
template.GetYaxis().SetTitle(labelY)
template.SetTitle(" ")
fin = ROOT.TFile(options.input)

legend_y0 = 0.650;
legend1 = ROOT.TLegend(0.2600, legend_y0, 0.9350, 0.9150);
legend1.SetNColumns(3)
legend1.SetFillStyle(0);
legend1.SetBorderSize(0);
legend1.SetFillColor(10);
legend1.SetTextSize(0.050);
legend1.SetHeader(label_head);

if options.unblind :
    data = rebin_data(template, folder, fin, options.fromHavester)
    legend1.AddEntry(data, "Observed", "p");
hist_total = rebin_total(template, folder, fin, divideByBinWidth, name_total)
legend1.AddEntry(hist_total, "Uncertainty", "f");

canvas = ROOT.TCanvas("canvas", "canvas", 700, 1300);
canvas.SetFillColor(10);
canvas.SetBorderSize(2);
canvas.Draw();

topPad = ROOT.TPad("topPad", "topPad", 0.00, 0.34, 1.00, 0.995);
topPad.SetFillColor(10);
topPad.SetTopMargin(0.075);
topPad.SetLeftMargin(0.20);
topPad.SetBottomMargin(0.00);
topPad.SetRightMargin(0.04);
if options.useLogPlot : topPad.SetLogy();
bottomPad = ROOT.TPad("bottomPad", "bottomPad", 0.00, 0.01, 1.00, 0.335);
bottomPad.SetFillColor(10);
bottomPad.SetTopMargin(0.085);
bottomPad.SetLeftMargin(0.20);
bottomPad.SetBottomMargin(0.35);
bottomPad.SetRightMargin(0.04);
####################################
canvas.cd();
topPad.Draw();
topPad.cd();
hist_total.Draw("axis")
histogramStack_mc = ROOT.THStack()
print ("list of processes considered and their integrals")
for key in  dprocs.keys() :
    histogram = rebin_hist(template, fin, key, dprocs[key], divideByBinWidth)
    histogramStack_mc.Add(histogram)
    print (key, histogram.Integral())
histogramStack_mc.Draw("hist,same")
hist_total.Draw("e2,same")
if options.unblind : data.Draw("e1P,same")
hist_total.Draw("axis,same")
legend1.Draw("same")
labels = addLabel_CMS_preliminary()
for label in labels : label.Draw("same")
#################################
canvas.cd();
bottomPad.Draw();
bottomPad.cd();
bottomPad.SetLogy(0);
print ("doing bottom pad")
hist_total_err = do_hist_total_err(template, options.labelX, name_total)
hist_total_err.Draw("e2")
if options.unblind :
    dataerr = err_data(hist_total, folder, options.fromHavester)
    dataerr.Draw("e1P,same")
line = ROOT.TF1("line","0", hist_total_err.GetXaxis().GetXmin(), hist_total_err.GetXaxis().GetXmax());
line.SetLineStyle(3);
line.SetLineColor(ROOT.kBlack);
line.Draw("same");
##################################
canvas.SaveAs(options.odir+category+"_"+typeFit+".pdf")
print ("saved",options.odir+category+"_"+typeFit+".pdf")
