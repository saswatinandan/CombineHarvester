#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import ROOT
import sys, os, re, shlex
from subprocess import Popen, PIPE
#from CombineHarvester.ttH_htt.list_syst import *
sys.stdout.flush()


syst_file = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/configs/list_syst.py"
execfile(syst_file)
print ("syst values and channels options taken from: " +  syst_file)

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--inputShapes",    type="string",       dest="inputShapes", help="Full path of prepareDatacards.root")
parser.add_option("--channel",        type="string",       dest="channel",     help="Channel to assume (to get the correct set of syst)")
parser.add_option("--cardFolder",     type="string",       dest="cardFolder",  help="Folder where to save the datacards (relative or full).\n Default: teste_datacards",  default="teste_datacards")
parser.add_option("--analysis",       type="string",       dest="analysis",    help="Analysis type = 'ttH' or 'HH' (to know what to take as Higgs procs and naming convention of systematics), Default ttH", default="ttH")
parser.add_option("--output_file",    type="string",       dest="output_file", help="Name of the output file.\n Default: the same of the input, substituing 'prepareDatacards' by 'datacard'", default="none")
parser.add_option("--shapeSyst",      action="store_true", dest="shapeSyst",   help="Do apply the shape systematics. Default: False", default=False)
parser.add_option("--noX_prefix",     action="store_true", dest="noX_prefix",  help="do not assume hist from prepareDatacards starts with 'x_' prefix", default=False)
parser.add_option("--era",            type="int",          dest="era",         help="Era to consider. Default: 2017",  default=2017)
(options, args) = parser.parse_args()

inputShapes = options.inputShapes
channel     = options.channel
era         = options.era
shape       = options.shapeSyst
analysis    = options.analysis
cardFolder  = options.cardFolder

if not os.path.exists(cardFolder):
    os.makedirs(cardFolder)

#####################################################
# List processes -- do it externally

bkg_proc_from_data = info_channel[channel]["bkg_proc_from_data"]
bkg_procs_from_MC  = info_channel[channel]["bkg_procs_from_MC"]
if analysis == "ttH" : higgs_procs = higgs_procs_ttH
## add the H processes (that shall be marked as signal on the datacards)

MC_proc = sum(higgs_procs,[]) + bkg_procs_from_MC
print ("MC processes:")
print ("BKG from MC   : ", bkg_procs_from_MC)
print ("BKG from data : ", bkg_proc_from_data)
print ("signal        : ", sum(higgs_procs,[]))

###########################################
# start the list of common systematics for all channels
###########################################

cb = ch.CombineHarvester()
cats = [
    (1, "%s_%s" % (analysis, channel))
    ]
masses = ["*"]
cb.AddObservations(["*"], ["%sl" % analysis], ["13TeV"], ["*"], cats)
cb.AddProcesses(    ['*'], [''], ['13TeV'], [''], bkg_proc_from_data + bkg_procs_from_MC, cats, False)
cb.AddProcesses(    ['*'], [''], ['13TeV'], [''], sum(higgs_procs,[]), cats, True)

#######################################
print ("Adding lumi syt uncorrelated/year")
# check if we keep the lumis/era correlated or not
cb.cp().signals().AddSyst(cb, "lumi_%s" % str(era), "lnN", ch.SystMap()(lnSyst["lumi"][2017]))

#######################################
print ("Adding rateParam")
# normalizations floating individually (ttWW correlated with ttW and among signal types)
# not relevant if you do the fit expliciting things on the text2ws maker -- but it does not hurt
for proc in bkg_procs_from_MC  :
    if "TTWW" in proc :
        cb.cp().process([proc]).AddSyst(cb, 'scale_TTWW', 'rateParam', ch.SystMap()(("(@0)", "scale_TTW")))
        print ("process: " + proc + " is proportonal to TTW")
    else :
        cb.cp().process([proc]).AddSyst(cb, "scale_%s" % proc, 'rateParam', ch.SystMap()(1.0))
        print ("added rateparam to: " + proc)

# correlate the rateparam amonf the Higgs processes 
for hsig in higgs_procs :
    for br, hsbr in enumerate(hsig) :
        if br == 0 : 
            cb.cp().process([hsbr]).AddSyst(cb, "scale_%s" % hsbr, 'rateParam', ch.SystMap()(1.0))
            print ("added rateparam to: " + hsbr)
        else :
            cb.cp().process([proc]).AddSyst(cb, 'scale_%s' % hsbr, 'rateParam', ch.SystMap()(("(@0)", "scale_%s" % hsig[0])))
            print ("process: " + hsbr + " is proportonal to", hsig[0])

########################################
# Higgs proc lnN syst 
proc_with_scale_syst = ["ttH", "tH", "ttW"]
for hsig in higgs_procs :
    if "ttH" in hsig[0] :
        cb.cp().process(hsig).AddSyst(cb, "pdf_Higgs_ttH", "lnN", ch.SystMap()(lnSyst["pdf_Higgs_ttH"][2017]))
        cb.cp().process(hsig).AddSyst(cb, "QCDscale_ttH",  "lnN", ch.SystMap()(lnSyst["QCDscale_ttH"][2017]))
    if "tHq" in hsig[0] or "tHW" in hsig[0] :
        cb.cp().process(hsig).AddSyst(cb, "pdf_qg",       "lnN", ch.SystMap()(lnSyst["pdf_qg"][2017]))
        cb.cp().process(hsig).AddSyst(cb, "QCDscale_tH",  "lnN", ch.SystMap()(lnSyst["QCDscale_tH"][2017]))
    ### add pdf and qcd scale if HH

########################################
print ("Adding theory syst (pdf/QCD scale) -- correlated between years ")
# BKG proc theory lnN syst 
if "TTZ" in bkg_procs_from_MC :
    cb.cp().process(["TTZ"]).AddSyst(cb, "pdf_gg",        "lnN", ch.SystMap()(lnSyst["pdf_gg"][2017]))
    cb.cp().process(["TTZ"]).AddSyst(cb, "QCDscale_ttZ",  "lnN", ch.SystMap()(lnSyst["QCDscale_ttZ"][2017]))
if "TTW" in bkg_procs_from_MC :
    cb.cp().process(["TTW"]).AddSyst(cb, "pdf_qqbar",     "lnN", ch.SystMap()(lnSyst["pdf_qqbar"][2017]))
    cb.cp().process(["TTW"]).AddSyst(cb, "QCDscale_ttW",  "lnN", ch.SystMap()(lnSyst["QCDscale_ttW"][2017]))
if "TTWW" in bkg_procs_from_MC :
    cb.cp().process(["TTWW"]).AddSyst(cb, "pdf_TTWW",       "lnN", ch.SystMap()(lnSyst["pdf_TTWW"][2017]))
    cb.cp().process(["TTWW"]).AddSyst(cb, "QCDscale_ttWW",  "lnN", ch.SystMap()(lnSyst["QCDscale_ttWW"][2017]))
### add more BKGs if more processes have specific PDF/scale systematics

########################################
# BR syst 
for proc in sum(higgs_procs,[]) :
    for key in higgsBR:
        if key in proc :
            cb.cp().process(hsig).AddSyst(cb, "BR_%s" % key, "lnN", ch.SystMap()(higgsBR[key]))
            print ("added " + "BR_%s" % key + " uncertanty to process: " + proc)

########################################
# th shape syst 
if shape :
    for hsig in higgs_procs :
        if "ttH" in hsig[0] :
            cb.cp().process([proc]).AddSyst(cb,  "CMS_%sl_thu_shape_ttH_x1" % analysis, "shape", ch.SystMap()(1.0))
            cb.cp().process([proc]).AddSyst(cb,  "CMS_%sl_thu_shape_ttH_y1" % analysis, "shape", ch.SystMap()(1.0))
            print ("Adding TH-like shape syst for ttH process -- correlated between years")
        if "TTW" in bkg_procs_from_MC :
            cb.cp().process([proc]).AddSyst(cb,  "CMS_%sl_thu_shape_ttW_x1" % analysis, "shape", ch.SystMap()(1.0))
            cb.cp().process([proc]).AddSyst(cb,  "CMS_%sl_thu_shape_ttW_y1" % analysis, "shape", ch.SystMap()(1.0))
            print ("Adding TH-like shape syst for ttW process -- correlated between years")
        if "TTZ" in bkg_procs_from_MC :
            cb.cp().process([proc]).AddSyst(cb,  "CMS_%sl_thu_shape_ttZ_x1" % analysis, "shape", ch.SystMap()(1.0))
            cb.cp().process([proc]).AddSyst(cb,  "CMS_%sl_thu_shape_ttZ_y1" % analysis, "shape", ch.SystMap()(1.0))
            print ("Adding TH-like shape syst for ttZ process -- correlated between years")

if shape :
    ########################################
    # fakes shape syst -- all uncorrelated
    for fake_shape_syst in fake_shape_systs_uncorrelated :
        cb.cp().process(["fakes_data"]).AddSyst(cb,  fake_shape_syst, "shape", ch.SystMap()(1.0))
        print ("added " + fake_shape_syst + " as shape uncertainty to " + "fakes_data")
    ########################################
    # MC estimated shape syst
    for MC_shape_syst in MC_shape_systs_uncorrelated + MC_shape_systs_correlated  :
        cb.cp().process(MC_proc).AddSyst(cb,  MC_shape_syst, "shape", ch.SystMap()(1.0))
        print ("added " + MC_shape_syst + " as shape uncertainty to the MC processes")

########################################
# Specific channels lnN syst
specific_ln_systs_ttH
for specific_syst in specific_ln_systs_ttH :
    if specific_ln_systs_ttH[specific_syst]["proc"] == "MCproc" : 
        procs = MC_proc
    else : 
        procs = specific_ln_systs_ttH[specific_syst]["proc"]
    name_syst = specific_syst
    if not specific_ln_systs_ttH[specific_syst]["correlated"] :
        name_syst = specific_syst.replace("%sl" % analysis, "%sl%s" % (analysis, str(era - 2000)))
        # assuming that the syst for the HH analysis with have the label HHl
    cb.cp().process(procs).AddSyst(cb,  name_syst, "lnN", ch.SystMap()(specific_ln_systs_ttH[specific_syst]["value"]))
    print ("added " + name_syst + " with value " + str(specific_ln_systs_ttH[specific_syst]["value"]) + " to processes: ",  specific_ln_systs_ttH[specific_syst]["proc"] )

########################################
# Construct templates for fake/gentau syst if relevant
finalFile = inputShapes
created_ln_to_shape_syst = []
created_shape_to_shape_syst = []
if info_channel[channel]["isSMCSplit"] :
    print ("Doing template to fake/gen tau systematics")
    try : tfile = ROOT.TFile(inputShapes, "READ")
    except : print ("Doesn't exist" + inputShapes)
    outpuShape = inputShapes.replace(".root", "_genfakesyst.root")
    tfileout = ROOT.TFile(outpuShape, "recreate")
    tfileout.cd()
    for ln_to_shape in specific_ln_shape_systs_ttH :
        print ("==============================")
        print ("Doing themplates to: " + ln_to_shape + " with value " + str(specific_ln_shape_systs_ttH[ln_to_shape]["value"]))
        name_syst = ln_to_shape
        print("From ln: " +  name_syst)
        if not specific_ln_shape_systs_ttH[ln_to_shape]["correlated"] :
            name_syst = ln_to_shape.replace("%sl" % analysis, "%sl%s" % (analysis, str(era - 2000)))
        for proc in MC_proc :
            histUp = ROOT.TH1F()
            histDo = ROOT.TH1F()
            ## fixme: old cards does not have uniform naming convention to tH/VH
            if "tHq" in proc or "tHW" in proc or "VH" in proc or "conversions" in proc : continue
            print ("======")
            for typeHist in ["faketau", "gentau"] :
                histFind = "%s_%s" % (proc, typeHist)
                try : hist = tfile.Get(histFind)
                except : print ("Doesn't find" + histFind) 
                print (histFind, hist.Integral())
                # clone only the structure -- for the case of no shift
                if specific_ln_shape_systs_ttH[ln_to_shape]["type"] == typeHist :
                    print (histFind + " Multiply upper part by " + str(specific_ln_shape_systs_ttH[ln_to_shape]["value"]))  
                    histUp = hist.Clone()
                    histUp.Scale(specific_ln_shape_systs_ttH[ln_to_shape]["value"])
                    print (histFind + " Multiply upper part by " + str(1 - (specific_ln_shape_systs_ttH[ln_to_shape]["value"] - 1)), histUp.Integral())
                    histDo = hist.Clone()
                    histDo.Scale(1 - (specific_ln_shape_systs_ttH[ln_to_shape]["value"] - 1))
                else : 
                    print ("Adding " + histFind + " part ")
                    histUp.Copy(hist)
                    histDo.Copy(hist)
                    histUp.Add(hist)
                    histDo.Add(hist)
                    print (histDo.Integral())
            histUp.SetName("%s_%s_shapeUp"    % (proc, name_syst))
            histDo.SetName("%s_%s_shapeDown" % (proc, name_syst))
            histUp.Write()
            histDo.Write()
        created_ln_to_shape_syst += ["%s_shape" % name_syst]
        if shape : 
            for shape_to_shape in specific_shape_shape_systs_ttH :
                print ("Doing themplates to: " + shape_to_shape + " (originally shape) " )
                histUp = ROOT.TH1F()
                histDo = ROOT.TH1F()
                name_syst = shape_to_shape.replace("CMS_", "CMS_constructed_")
                if not specific_shape_shape_systs_ttH[shape_to_shape]["correlated"] :
                    name_syst = name_systreplace("%sl" % analysis, "%sl%s" % (analysis, str(era - 2000)))
                for proc in MC_proc :
                    for typeHist in ["faketau", "gentau"] :
                        histFindUp = "%s_%s_%sUp" % (proc, typeHist, shape_to_shape)
                        try : histUp = tfile.Get(histFindUp)
                        except : print ("Doesn't find" + histFindUp) 
                        histFindDown = "%s_%s_%sDown" % (proc, typeHist, shape_to_shape)
                        try : histDown = tfile.Get(histFindDown)
                        except : print ("Doesn't find" + histFindDown)
                        histUp.Add(histUp)
                        histDo.Add(histDown)
                    histUp.SetName("%s_%sUp"    % (proc, name_syst))
                    histDo.SetName("%s_%sDown" % (proc, name_syst))
                    histUp.Write()
                    histDo.Write()
                created_shape_to_shape_syst += [name_syst]  
                print ("constructed up/do templates from : " + shape_to_shape + " and saved as "+ name_syst )          
    tfileout.Close()
    print ("File with ln to shape syst: " +  outpuShape)

    finalFile = outpuShape.replace(".root", "_all.root")
    print ("File merged with fake/gen syst: ", finalFile)
    head, tail = os.path.split(inputShapes)
    print ('doing hadd in directory: ' + head)
    p = Popen(shlex.split("hadd -f %s %s %s" % (finalFile, outpuShape, inputShapes)) , stdout=PIPE, stderr=PIPE, cwd=head) 
    comboutput = p.communicate()[0]
    #if "conversions" in MC_proc : MC_proc.remove("conversions")
    ## fixme: old cards does not have uniform naming convention to tH/VH
    MC_proc_less = list(set(list(MC_proc)) - set(["conversions", "tHq_hww", "tHW_hww"]))
    for shape_syst in created_ln_to_shape_syst + created_shape_to_shape_syst :
        cb.cp().process(MC_proc_less).AddSyst(cb,  shape_syst, "shape", ch.SystMap()(1.0))
        print ("added " + shape_syst + " as shape uncertainty to the MC processes, except conversions")

########################################
# bin by bin stat syst
cb.cp().SetAutoMCStats(cb, 10)

if options.noX_prefix :
    cb.cp().backgrounds().ExtractShapes(
        finalFile,
        "$PROCESS",
        "$PROCESS_$SYSTEMATIC")
    cb.cp().signals().ExtractShapes(
        finalFile,
        "$PROCESS",
        "$PROCESS_$SYSTEMATIC")
else :
    cb.cp().backgrounds().ExtractShapes(
        inputShapes,
        "x_$PROCESS",
        "x_$PROCESS_$SYSTEMATIC")
    cb.cp().signals().ExtractShapes(
        inputShapes,
        "x_$PROCESS",
        "x_$PROCESS_$SYSTEMATIC")
########################################
# rename some shape systematics according to era to keep them uncorrelated
if shape :
    ########################################
    # fakes shape syst 
    for fake_shape_syst in fake_shape_systs_uncorrelated :
        fake_shape_syst_era = fake_shape_syst.replace("CMS_ttHl", "CMS_ttHl%s" % (str(era-2000)))
        cb.cp().process(["fakes_data"]).RenameSystematic(cb, fake_shape_syst, fake_shape_syst_era)
        print ("renamed " + fake_shape_syst + " to " + "fakes_data" + " as: " + fake_shape_syst_era)
    ########################################
    # MC estimated shape syst
    for MC_shape_syst in MC_shape_systs_uncorrelated :
        MC_shape_syst_era = MC_shape_syst.replace("CMS_ttHl", "CMS_ttHl%s" % str(era).replace("20",""))
        cb.cp().process(MC_proc).RenameSystematic(cb, MC_shape_syst, MC_shape_syst_era)
        print ("renamed " + MC_shape_syst + " as shape uncertainty to MC prcesses to " + MC_shape_syst_era)

    cb.cp().process(MC_proc).RenameSystematic(cb, "CMS_ttHl_JES",   "CMS_scale_j")
    print ("renamed CMS_ttHl_JES to CMS_scale_j to the MC processes ")

    cb.cp().process(MC_proc).RenameSystematic(cb, "CMS_ttHl_tauES", "CMS_scale_t")
    print ("renamed CMS_ttHl_tauES to CMS_scale_t to the MC processes ")

    for shape_syst in created_shape_to_shape_syst : 
        cb.cp().process(MC_proc).RenameSystematic(cb, shape_syst, shape_syst.replace("CMS_constructed_", "CMS_"))
        print ("renamed " + shape_syst + " to " +  shape_syst.replace("CMS_constructed_", "CMS_") + " to the MC processes ")

#    bbb.MergeAndAdd(cb_et.cp().era(['8TeV']).bin_id([0, 1, 2]).process(['QCD','W','ZL','ZJ','VV','ZTT','TT']), cb)
########################################
# output the card

#output_file = options.output_file
if options.output_file == "none" :
    output_file = cardFolder + "/" + str(os.path.basename(inputShapes)).replace(".root","").replace("prepareDatacards", "datacard")
else :
    output_file = options.output_file
bins = cb.bin_set()
for b in bins :
    print ("\n Output file: " + output_file + ".txt")
    cb.cp().bin([b]).mass(["*"]).WriteDatacard(output_file + ".txt" , output_file + ".root")

sys.stdout.flush()