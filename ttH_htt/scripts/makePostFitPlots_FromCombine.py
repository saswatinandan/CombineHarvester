#!/usr/bin/env python

import os, subprocess, sys
import os, sys, time,math
import ROOT
from optparse import OptionParser
from collections import OrderedDict
import sys, os, re, shlex
from subprocess import Popen, PIPE

from optparse import OptionParser
parser = OptionParser()
parser.add_option(
    "--inputDatacard", type="string", dest="inputDatacard",
    help="PrepareDatacard from which run combine and draw the shapes from (full or relative path)"
    )
parser.add_option(
    "--odir", type="string", dest="odir",
    help="Directory for the output plots. If it is not entered it is done on the same folders that contains the inputCard",
    default="none"
    )
parser.add_option(
    "--plainBins", action="store_true", dest="plainBins",
    help="Draw the plot without rebining the X-axis as originally proposed (just as plain list of bins)",
    default=False
    )
parser.add_option(
    "--channel", type="string", dest="channel",
    help="Name of the category as it is appear on the input file",
    default="1l_2tau"
    )
parser.add_option(
    "--labelX", type="string", dest="labelX",
    help="To appear on final plot",
    default="BDT"
    )
parser.add_option(
    "--divideByBinWidth", action="store_true", dest="divideByBinWidth",
    help="If final plot shall be done dividing bin content by bin width ",
    default=False
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
    "--notRedoHavester", action="store_true", dest="notRedoHavester",
    help="If you already did this once for a given input and are only polishing the plot layout there is no need of doing the again. This option ",
    default=False
    )
parser.add_option("--analysis",       type="string",       dest="analysis",    
    help="Analysis type = 'ttH' or 'HH' (to know what to take as Higgs procs and naming convention of systematics), Default ttH", 
    default="ttH"
    )
parser.add_option("--era",       type="string",       dest="era",    
    help="Era to consider (important for list of systematics and labeling). Default: 2017", 
    default="2017"
    )
parser.add_option("--shapeSyst",      action="store_true", dest="shapeSyst",   
    help="Do apply the shape systematics. Default: False", 
    default=False
    )
(options, args) = parser.parse_args()

#ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
sys.stdout.flush()

func_file = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/python/data_manager.py"
execfile(func_file)

opt_file = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/configs/plot_options.py"
execfile(opt_file)
print ("plot options taken from: " +  opt_file)

syst_file = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/configs/list_syst.py"
execfile(syst_file)
print ("channel list options by channel options taken from: " +  syst_file)

ranges_file = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/configs/plot_ranges_ttH.py"
execfile(ranges_file)
plot_ranges = options_plot_ranges()
print ("channel list plot ranges by channel options taken from: " +  ranges_file)

plainBins        = options.plainBins
divideByBinWidth = options.divideByBinWidth
channel          = options.channel
doPostFit        = options.doPostFit
fileDatacard, pathDatacard = splitPath(options.inputDatacard)
fileDatacard = fileDatacard.replace(".root","").replace(".txt","")

analysis     = options.analysis
if analysis == "ttH" : higgs_procs = higgs_procs_ttH

labelY = "Events"
if divideByBinWidth : labelY = "Events / bin width"

labelX = options.labelX
if options.plainBins : labelX += " bin#"

odir = options.odir
if odir == "none" : 
    odir = pathDatacard

fileDat = fileDatacard.replace("prepareDatacards","datacard")
if plainBins : fileDat += "_plainBins"

inputDatacard    = "%s/%s_shapes.root" % (odir, fileDat)

if not options.notRedoHavester :
    cmd = "WriteDatacards.py "
    cmd += " --inputShapes %s/%s.root"  % (pathDatacard, fileDatacard) 
    cmd += " --channel %s"  % channel
    cmd += " --cardFolder %s" % odir 
    cmd += " --output_file %s/%s"  % (odir, fileDat) 
    if options.shapeSyst : cmd += " --shapeSyst"
    cmd += " --noX_prefix"
    runCombineCmd(cmd)
    print ("created: " + "%s/%s.txt" % (odir, fileDat) )

    cmd = "text2workspace.py"
    cmd += " %s.txt"        % fileDat
    cmd += " -o %s_WS.root" % fileDat
    runCombineCmd(cmd, odir)
    if doPostFit :
        print ("[WARNING]: the postfit plot will be done for this channel, extracting only signal (as defined on the input datacard) and without any BKG floating")
        print ("To do it for ttH channel with full fitting options please refer to: ")
    cmd = "combineTool.py -M FitDiagnostics %s_WS.root" % fileDat
    runCombineCmd(cmd, odir)
    print ("the diagnosis that input Havester is going to be on fitDiagnostics.Test.root or fitDiagnostics.root depending on your version of combine -- check if that was the case you have a crash!")
    cmd = "PostFitShapesFromWorkspace "
    cmd += " --workspace %s_WS.root" % fileDat
    cmd += " --o %s_shapes.root" % fileDat
    cmd += " --sampling --print " 
    if doPostFit         : cmd += " --postfit "
    if not options.plainBins : cmd += " -d %s.txt"        % fileDat
    runCombineCmd(cmd, odir)
    print ("created ",  "%s/%s_shapes.root" % (odir, fileDat) )
else : 
    if not os.path.isfile(inputDatacard) :
        sys.exit("you should do a run without the option --notRedoHavester")

folder      = analysis + '_'
if options.doPostFit :
    folder      += channel + "_postfit"
    typeFit     = "postfit"
else :
    folder      += channel + "_prefit"
    typeFit     = "prefit"
print ("folder", folder)

name_total = "TotalProcs"

if analysis == "ttH" : 
    all_procs = sum(higgs_procs,[]) + info_channel[channel]["bkg_proc_from_data"] + info_channel[channel]["bkg_procs_from_MC"]
    proc_draw_options = options_plot(analysis, channel, all_procs, decays_ttH) 

label_head = "%s fit," % str(options.era)
label_head = label_head + " " + channel.replace("tau", "#tau").replace("_", " ").replace("ttZctrl", "ttZ CR").replace("ttWctrl", "ttW CR").replace("WZ", "WZ CR").replace("ZZ", "ZZ CR")

if typeFit == "prefit" : 
    label_head = label_head+" "+typeFit
else : 
    label_head = label_head+" #mu(ttH)=#hat{#mu}"
    
print ("Plotting: " +  label_head)
print ("will draw processes", list(proc_draw_options.keys()))

print ("Taking shapes from: %s/%s_shapes.root" % (odir, fileDat))
fin           = ROOT.TFile("%s/%s_shapes.root" % (odir, fileDat))
if not options.plainBins :
    # take histogram template from original datacard
    fileOrig = "%s/%s.root"  % (odir, fileDat)
    readFrom = "%s_%s/data_obs" % (analysis, channel)
else :
    fileOrig = "%s/%s_shapes.root" % (odir, fileDat)
    readFrom = folder+"/data_obs"
print ("template histogram on ", fileOrig, readFrom)
fileorriginal = ROOT.TFile(fileOrig)
template      = fileorriginal.Get(readFrom)
template.GetYaxis().SetTitle(labelY)
template.SetTitle(" ")

legend_y0 = 0.650
legend1 = ROOT.TLegend(0.2400, legend_y0, 0.9450, 0.9150)
legend1.SetNColumns(3)
legend1.SetFillStyle(0)
legend1.SetBorderSize(0)
legend1.SetFillColor(10)
legend1.SetTextSize(0.040)
legend1.SetHeader(label_head)

fromHavester = True
## FIXME
if options.unblind :
    data = rebin_data(template, folder, fin, fromHavester, plot_ranges[channel])
    legend1.AddEntry(data, "Observed", "p")
hist_total = rebin_total(template, folder, fin, divideByBinWidth, name_total, plot_ranges[channel])
legend1.AddEntry(hist_total, "Uncertainty", "f")


canvas = ROOT.TCanvas("canvas", "canvas", 1200, 1500)
canvas.SetBatch(ROOT.kTRUE)
canvas.SetFillColor(10)
canvas.SetBorderSize(2)

topPad = ROOT.TPad("topPad", "topPad", 0.00, 0.34, 1.00, 0.995)
topPad.SetBatch(ROOT.kTRUE)
topPad.SetFillColor(10)
topPad.SetTopMargin(0.075)
topPad.SetLeftMargin(0.20)
topPad.SetBottomMargin(0.00)
topPad.SetRightMargin(0.04)
if plot_ranges[channel]["useLogPlot"] : topPad.SetLogy()
dumb = topPad.Draw()
del dumb

bottomPad = ROOT.TPad("bottomPad", "bottomPad", 0.00, 0.01, 1.00, 0.34)
bottomPad.SetBatch(ROOT.kTRUE)
bottomPad.SetFillColor(10)
bottomPad.SetTopMargin(0.0)
bottomPad.SetLeftMargin(0.20)
bottomPad.SetBottomMargin(0.35)
bottomPad.SetRightMargin(0.04)
dumb = bottomPad.Draw()
del dumb

topPad.cd()
dumb = hist_total.Draw("axis")
del dumb
histogramStack_mc = ROOT.THStack()
print ("list of processes considered and their integrals")
for key in  proc_draw_options.keys() :
    histogram = rebin_hist(template, folder, fin, key, proc_draw_options[key], divideByBinWidth)
    dumb = histogramStack_mc.Add(histogram)
    del dumb
    print (key, histogram.Integral())
dumb = histogramStack_mc.Draw("hist,same")
del dumb
dumb = hist_total.Draw("e2,same")
del dumb
if options.unblind :
    dumb = data.Draw("e1P,same")
    del dumb
dumb = hist_total.Draw("axis,same")
del dumb
dumb = legend1.Draw("same")
del dumb
labels = addLabel_CMS_preliminary()
for label in labels :
    dumb = label.Draw("same")
    del dumb
#################################

bottomPad.cd()
bottomPad.SetLogy(0)
print ("doing bottom pad")
hist_total_err = do_hist_total_err(template, folder, labelX, name_total, channel, plot_ranges)
dumb = hist_total_err.Draw("e2")
del dumb
if options.unblind :
    dataerr = err_data(hist_total, folder, fromHavester)
    dumb = dataerr.Draw("e1P,same")
    del dumb
line = ROOT.TF1("line","1", hist_total_err.GetXaxis().GetXmin(), hist_total_err.GetXaxis().GetXmax())
line.SetLineStyle(3)
line.SetLineColor(ROOT.kBlack)
dumb = line.Draw("same")
del dumb
print ("done bottom pad")
##################################
oplin = "linear"
if plot_ranges[channel]["useLogPlot"] : oplin = "log"
if divideByBinWidth   : oplin += "_divideByBinWidth"

print ("made log")

if odir == "none" : 
    outputPlot       = "%s/%s"        % (pathDatacard, fileDat)
else :
    outputPlot       = "%s/%s"        % (odir, fileDat)

nameOutputPlot = outputPlot + "_" + typeFit + "_" + oplin + "_unblind" + str(options.unblind) + ".pdf" 
print (nameOutputPlot)

dumb = canvas.SaveAs(nameOutputPlot)
del dumb
canvas.Close()
ROOT.gSystem.ProcessEvents()
sys.stdout.flush()