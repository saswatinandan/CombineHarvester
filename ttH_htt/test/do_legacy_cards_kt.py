#!/usr/bin/env python
import os, subprocess, sys
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from subprocess import Popen, PIPE
from io import open
exec(open(os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/python/data_manager.py").read())

output_cards = "/home/acaan/CMSSW_10_2_13/src/cards_set/legacy_TLL_03March20_kt_scan/"

eras_to_do = ["2018", "2016", "2017"] #
make_cards = True

cards_fullsyst_feb20 = {
    ## All taken from: /home/karl/ttHAnalysis/201*/2020Feb17/datacards/*/addSystFakeRates/
    ############################
    "2lss_1tau_rest"         : {"channel" : "2lss_1tau_rest", "shapes"   : "/home/acaan/ttHAnalysis/2018/2020Feb17/addSystFakeRates/2lss_1tau/addSystFakeRates_2lss_1tau_sumOS_output_NN_rest.root"}, #  -- if isMCsplit needs to write on the repo
    "2lss_1tau_tH"           : {"channel" : "2lss_1tau_tH",   "shapes"   : "/home/acaan/ttHAnalysis/2018/2020Feb17/addSystFakeRates/2lss_1tau/addSystFakeRates_2lss_1tau_sumOS_output_NN_tH.root"},
    "2lss_1tau_ttH"          : {"channel" : "2lss_1tau_ttH",  "shapes"   : "/home/acaan/ttHAnalysis/2018/2020Feb17/addSystFakeRates/2lss_1tau/addSystFakeRates_2lss_1tau_sumOS_output_NN_ttH.root"},
    #############################
    "0l_2tau"                : {"channel" : "0l_2tau",   "shapes"   : "/home/acaan/ttHAnalysis/2018/2020Feb17/addSystFakeRates/0l_2tau/addSystFakeRates_0l_2tau_0l_2tau_mvaOutput_Legacy_OS.root"},
    "1l_2tau"                : {"channel" : "1l_2tau",   "shapes"   : "/home/acaan/ttHAnalysis/2018/2020Feb17/addSystFakeRates/1l_2tau/addSystFakeRates_1l_2tau_mvaOutput_legacy_OS.root"},
    "1l_1tau"                : {"channel" : "1l_1tau",   "shapes"   : "/home/acaan/ttHAnalysis/2018/2020Feb17/addSystFakeRates/1l_1tau/addSystFakeRates_1l_1tau_1l_1tau_mvaOutput_Legacy_6_disabled.root"},
    "2los_1tau"              : {"channel" : "2los_1tau", "shapes"   : "/home/acaan/ttHAnalysis/2018/2020Feb17/addSystFakeRates/2los_1tau/addSystFakeRates_2los_1tau_mvaOutput_legacy.root"},
    ##############################
    #"2l_2tau"                : {"channel" : "2l_2tau",   "shapes"   : "/home/acaan/ttHAnalysis/2018/2l_2tau_20Feb20/datacards/2l_2tau/addSystFakeRates/addSystFakeRates_2l_2tau_lepdisabled_taudisabled_sumOS_mvaOutput_final.root"},
    "3l_1tau"                : {"channel" : "3l_1tau",   "shapes"   : "/home/acaan/ttHAnalysis/2018/2020Feb17/addSystFakeRates/3l_1tau/addSystFakeRates_3l_1tau_OS_mvaOutput_legacy.root"}, #
}

cards_to_do = cards_fullsyst_feb20

#python test/do_kt_scans.py
#--cardFolder /home/acaan/CMSSW_10_2_13/src/cards_set/legacy_TLL_20Feb20_kt_scan/
#--shapeSyst
#--inputShapes /home/acaan/ttHAnalysis/2016/2020Feb17/addSystFakeRates/1l_2tau/addSystFakeRates_1l_2tau_mvaOutput_legacy_OS.root
#--era 2016
#--channel_to_card 1l_2tau
#--channel 1l_2tau
for era in eras_to_do :
    if make_cards :
        for key in cards_to_do :
            print (key)
            print (cards_to_do[key])
            cmd = "python test/do_kt_scans.py  "
            cmd += " --inputShapes %s " % (cards_to_do[key]["shapes"].replace("2018", era))
            cmd += " --channel %s "     % (cards_to_do[key]["channel"].replace("2018", era))
            cmd += " --cardFolder %s "  % output_cards
            cmd += " --shapeSyst  "
            cmd += " --no_data "
            cmd += " --era %s " % str(era)
            cmd += " --channel_to_card %s "     % (key)
            jobfile = "%s/ttH_%s_%s.sh" % (output_cards, key, era)
            ff = open(jobfile, "w")
            ff.write(u'#!/bin/bash\n\n')
            ff.write(unicode(cmd))
            ff.close()
            cmd2 = "sbatch "
            cmd2 += " --output=%s " % jobfile.replace(".sh", ".log.job")
            #cmd2 += "--partition=small "
            cmd2 += jobfile
            #print(cmd2)
            runCombineCmd(cmd2) # , '.', "%s/ttH_%s_%s.log" % (output_cards, key, era)
            #print ("output card/log saved on: %s/ttH_%s_%s.txt/root/log" % (output_cards, key, era))
