#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import ROOT
import sys, os, re, shlex
from subprocess import Popen, PIPE
from CombineHarvester.ttH_htt.data_manager import rename_tH, lists_overlap, construct_templates, list_proc, make_threshold
sys.stdout.flush()

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--inputShapes",    type="string",       dest="inputShapes", help="Full path of prepareDatacards.root")
parser.add_option("--channel",        type="string",       dest="channel",     help="Channel to assume (to get the correct set of syst)")
parser.add_option("--cardFolder",     type="string",       dest="cardFolder",  help="Folder where to save the datacards (relative or full).\n Default: teste_datacards",  default="teste_datacards")
parser.add_option("--analysis",       type="string",       dest="analysis",    help="Analysis type = 'ttH' or 'HH' (to know what to take as Higgs procs and naming convention of systematics), Default ttH", default="ttH")
parser.add_option("--output_file",    type="string",       dest="output_file", help="Name of the output file.\n Default: the same of the input, substituing 'prepareDatacards' by 'datacard' (+ the coupling if the --couplings is used)", default="none")
parser.add_option("--coupling",       type="string",       dest="coupling",    help="Coupling to take in tH.\n Default: do for SM, do not add couplings on output naming convention", default="none")
parser.add_option("--shapeSyst",      action="store_true", dest="shapeSyst",   help="Do apply the shape systematics. Default: False", default=False)
parser.add_option("--noX_prefix",     action="store_true", dest="noX_prefix",  help="do not assume hist from prepareDatacards starts with 'x_' prefix", default=False)
parser.add_option("--only_ttH_sig",   action="store_true", dest="only_ttH_sig",help="consider only ttH as signal on the datacard -- for single channel tests", default=False)
parser.add_option("--era",            type="int",          dest="era",         help="Era to consider (important for list of systematics). Default: 2017",  default=2017)
(options, args) = parser.parse_args()

inputShapes = options.inputShapes
channel     = options.channel
era         = options.era
shape       = options.shapeSyst
analysis    = options.analysis
cardFolder  = options.cardFolder
coupling    = options.coupling
noX_prefix  = options.noX_prefix
only_ttH_sig = options.only_ttH_sig

print("shape", shape)

if not os.path.exists(cardFolder):
    os.makedirs(cardFolder)

syst_file = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/configs/list_syst.py"
execfile(syst_file)
print ("syst values and channels options taken from: " +  syst_file)

info_file = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/configs/list_channels.py"
execfile(info_file)
print ("list of signals/bkgs by channel taken from: " +  info_file)

higgs_procs = list_channels(analysis)["higgs_procs"]
list_channel_opt   = list_channels(analysis)["info_bkg_channel"]
bkg_proc_from_data = list_channel_opt[channel]["bkg_proc_from_data"]
bkg_procs_from_MC  = list_channel_opt[channel]["bkg_procs_from_MC"]
print (higgs_procs)
# if a coupling is done read the tH signal with that coupling on naming convention
if not (coupling == "none" or coupling == "kt_1_kv_1") :
    higgs_procs = [ [ entry.replace("tHq_", "tHq_%s_" % coupling).replace("tHW_", "tHW_%s_" % coupling) for entry in entries ] for entries in higgs_procs ]
    #tH_procs = [ entry for entry in entries if "tHq_" in entry or "tHW_" in entry]
    #print ("tH_procs = ", tH_procs)
higgs_procs_plain = sum(higgs_procs,[])
print("higgs_procs_plain", higgs_procs_plain)

# check a threshold on processes
bkg_proc_from_data = make_threshold(0.02, bkg_proc_from_data,  inputShapes)
bkg_procs_from_MC  = make_threshold(0.02, bkg_procs_from_MC, inputShapes)
higgs_procs_plain  = make_threshold(0.02, higgs_procs_plain, inputShapes)

MC_proc = higgs_procs_plain + bkg_procs_from_MC
print ("MC processes:")
print ("BKG from MC  (old)  : ", bkg_procs_from_MC)
print ("BKG from data (old) : ", bkg_proc_from_data)
print ("signal        (old ): ", higgs_procs_plain)

specific_syst_list = specific_syst(analysis, list_channel_opt)
print("list_channel_opt", list_channel_opt)
print("analysis", analysis)
print ("specific_syst_list : ", specific_syst_list)

if only_ttH_sig :
    print ("MC processes -- after chosing to mark as signal only ttH:")
    bkg_procs_from_MC += [ entry for entry in higgs_procs_plain if "ttH_" not in  entry]
    higgs_procs        = [ entries for entries in higgs_procs if "ttH_" in entries[0] ]
    print ("BKG from MC   (new): ", bkg_procs_from_MC)
    print ("signal        (new): ", higgs_procs)

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
cb.AddProcesses(    ['*'], [''], ['13TeV'], [''], higgs_procs_plain, cats, True)


#######################################
print ("Adding lumi syt uncorrelated/year")
# check if we keep the lumis/era correlated or not
cb.cp().signals().AddSyst(cb, "lumi_%s" % str(era), "lnN", ch.SystMap()(lnSyst["lumi"][2017]))

#######################################
# FIXME: one of the syst is logUniform -- fix
if 0 > 1 : # FIXME: remind why we added that at some point
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
#if analysis == "ttH" :
#    proc_with_scale_syst = ["ttH", "tH", "ttW"]
print("higgs_procs", higgs_procs)
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
for proc in higgs_procs_plain :
    for key in higgsBR:
        if key in proc :
            cb.cp().process([proc]).AddSyst(cb, "BR_%s" % key, "lnN", ch.SystMap()(higgsBR[key]))
            print ("added " + "BR_%s" % key + " uncertanty to process: " + proc + " of value = " + str(higgsBR[key]))

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
    # channel specific estimated shape syst
    #print("specific_shape", specific_shape)
    specific_shape_systs = specific_syst_list[specific_shape]
    print("specific_shape_systs", specific_syst_list[specific_shape])
    for specific_syst in specific_shape_systs :
        if channel not in specific_ln_systs[specific_syst]["channels"] :
            continue
        procs = list_proc(specific_ln_systs[specific_syst], MC_proc, bkg_proc_from_data + bkg_procs_from_MC, specific_syst)
        if len(procs) == 0 :
            continue
        cb.cp().process(procs).AddSyst(cb,  specific_syst, "shape", ch.SystMap()(1.0))
        print ("added " + specific_syst + " as shape uncertainty to ", procs)

########################################
# Specific channels lnN syst
specific_ln_systs  = specific_syst_list["specific_ln_systs"]

for specific_syst in specific_ln_systs :
    if channel not in specific_ln_systs[specific_syst]["channels"] :
        continue
    procs = list_proc(specific_ln_systs[specific_syst], MC_proc, bkg_proc_from_data + bkg_procs_from_MC, specific_syst)
    if len(procs) == 0 :
        continue
    name_syst = specific_syst
    if not specific_ln_systs[specific_syst]["correlated"] :
        name_syst = specific_syst.replace("%sl" % analysis, "%sl%s" % (analysis, str(era - 2000)))
        # assuming that the syst for the HH analysis with have the label HHl
    cb.cp().process(procs).AddSyst(cb,  name_syst, "lnN", ch.SystMap()(specific_ln_systs[specific_syst]["value"]))
    print ("added " + name_syst + " with value " + str(specific_ln_systs[specific_syst]["value"]) + " to processes: ",  specific_ln_systs[specific_syst]["proc"] )

########################################
# Construct templates for fake/gentau syst if relevant
finalFile = inputShapes
if list_channel_opt[channel]["isSMCSplit"] :
    specific_ln_shape_systs    = specific_syst_list["specific_ln_to_shape_systs"]
    specific_shape_shape_systs = specific_syst_list["specific_shape_to_shape_systs"]
    finalFile = construct_templates(cb, ch, specific_ln_shape_systs, specific_shape_shape_systs, inputShapes , MC_proc, shape, noX_prefix )

########################################
# bin by bin stat syst
cb.cp().SetAutoMCStats(cb, 10)

if noX_prefix :
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
        finalFile,
        "x_$PROCESS",
        "x_$PROCESS_$SYSTEMATIC")
    cb.cp().signals().ExtractShapes(
        finalFile,
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

########################################
# output the card
if options.output_file == "none" :
    output_file = cardFolder + "/" + str(os.path.basename(inputShapes)).replace(".root","").replace("prepareDatacards", "datacard")
else :
    output_file = options.output_file

if not (coupling == "none") :
    output_file += "_" + coupling

bins = cb.bin_set()
for b in bins :
    print ("\n Output file: " + output_file + ".txt")
    cb.cp().bin([b]).mass(["*"]).WriteDatacard(output_file + ".txt" , output_file + ".root")

rename_tH(output_file, "none", bins)
if not (coupling == "none" or coupling == "kt_1_kv_1") :
    print("Renaming tH processes (remove the coupling mention to combime)")
    rename_tH(output_file, coupling, bins)
sys.stdout.flush()
