#!/usr/bin/env python

import os, subprocess, sys, time, math, re, shlex
import ROOT
from optparse import OptionParser
from collections import OrderedDict
from subprocess import Popen, PIPE
from CombineHarvester.ttH_htt.data_manager import runCombineCmd, splitPath

from optparse import OptionParser
parser = OptionParser()
parser.add_option(
    "--inputShapes", type="string", dest="inputShapes",
    help="PrepareDatacard from which run combine and draw the shapes from (full or relative path)"
    )
parser.add_option(
    "--odir", type="string", dest="odir",
    help="Directory for the output. If it is not entered it is done on the same folders that contains the inputCard",
    default="none"
    )
parser.add_option(
    "--channel", type="string", dest="channel",
    help="Name of the category as it is appear on the input file",
    default="1l_2tau"
    )
parser.add_option(
    "--unblind", action="store_true", dest="unblind",
    help="Do subcategories from multilepton cards ",
    default=False
    )
parser.add_option(
    "--doLimits", action="store_true", dest="doLimits",
    help="Do the postfit plot",
    default=False
    )
parser.add_option(
    "--doImpacts", action="store_true", dest="doImpacts",
    help="Do the postfit plot",
    default=False
    )
parser.add_option(
    "--doGOF", action="store_true", dest="doGOF",
    help="Do the postfit plot",
    default=False
    )
parser.add_option(
    "--doPostFit", action="store_true", dest="doPostFit",
    help="Do the postfit plot",
    default=False
    )
parser.add_option(
    "--doPreFit", action="store_true", dest="doPreFit",
    help="Do the prefit plot",
    default=False
    )
parser.add_option(
    "--notRedoWS", action="store_true", dest="notRedoWS",
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
parser.add_option(
    "--plainBins", action="store_true", dest="plainBins",
    help="Draw the plot without rebining the X-axis as originally proposed (just as plain list of bins)",
    default=False
    )
(options, args) = parser.parse_args()

#ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
sys.stdout.flush()

channel          = options.channel
doPostFit        = options.doPostFit
doPreFit         = options.doPreFit
doLimits         = options.doLimits
doImpacts        = options.doImpacts
doGOF            = options.doGOF
plainBins        = options.plainBins

fileDatacard, pathDatacard = splitPath(options.inputShapes)
fileDatacard = fileDatacard.replace(".root","").replace(".txt","")

odir = options.odir
if odir == "none" : 
    odir = pathDatacard

fileDat = fileDatacard.replace("prepareDatacards","datacard")
if options.shapeSyst : 
    fileDat += "_wShapeSyst"

if not options.notRedoWS :
    cmd = "WriteDatacards.py "
    cmd += " --inputShapes %s/%s.root"  % (pathDatacard, fileDatacard) 
    cmd += " --channel %s"  % channel
    cmd += " --cardFolder %s" % odir 
    cmd += " --output_file %s/%s"  % (odir, fileDat) 
    if options.shapeSyst : cmd += " --shapeSyst"
    cmd += " --noX_prefix"
    runCombineCmd(cmd)
    print ("created datacard: " + "%s/%s.txt" % (odir, fileDat) )

    cmd = "text2workspace.py"
    cmd += " %s.txt"        % fileDat
    cmd += " -o %s_WS.root" % fileDat
    runCombineCmd(cmd, odir)
    print ("created workspace: " + "%s/%s_WS.root" % (odir, fileDat) )
elif os.path.isfile("%s_WS.root" % fileDat) :
    print ("You need to produce the workspace, remove notRedoWS from command line")

if (doPostFit or doPreFit) : 
    # to have Totalprocs computed
    cmd = "combineTool.py -M FitDiagnostics %s_WS.root" % fileDat
    runCombineCmd(cmd, odir)
    print ("the diagnosis that input Havester is going to be on fitDiagnostics.Test.root or fitDiagnostics.root depending on your version of combine -- check if that was the case you have a crash!")
 
    shapeDatacard    = "%s_shapes.root" % fileDat
    if doPostFit : 
        shapeDatacard = shapeDatacard.replace(".root", "_postfit.root")
        print ("[WARNING]: the postfit plot will be done for this channel, extracting only signal (as defined on the input datacard) and without any BKG floating")
        print ("To do it for ttH channel with full fitting options please refer to: ")
    if doPreFit  : 
        shapeDatacard = shapeDatacard.replace(".root", "_prefit.root")
    if plainBins : 
        shapeDatacard = shapeDatacard.replace(".root", "_plainBins.root")

    cmd = "PostFitShapesFromWorkspace "
    cmd += " --workspace %s_WS.root" % fileDat
    cmd += " --o %s" % shapeDatacard
    cmd += " --sampling --print " 
    if doPostFit         : cmd += " --postfit "
    if not plainBins : cmd += " -d %s.txt"        % fileDat
    runCombineCmd(cmd, odir)
    print ("created " + odir + "/" + shapeDatacard )

    cmd = "makePostFitPlots.py "
    cmd += " --inputDatacard %s/%s" % (odir, shapeDatacard)
    if not plainBins : cmd += " --original %s/%s.txt" % (odir, fileDat) 
    cmd += " --channel %s" % channel 
    ##if unblind           : cmd += " --unblind "
    if doPostFit         : cmd += " --doPostFit "
    runCombineCmd(cmd)
    print ("created plot " + odir + "/" + shapeDatacard.replace(".root", "*.pdf")  )