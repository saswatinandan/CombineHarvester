#!/usr/bin/env python
import os, subprocess, sys
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from subprocess import Popen, PIPE
from io import open
exec(open(os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/python/data_manager.py").read())

output_cards = "/home/acaan/VHbbNtuples_8_0_x/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/deeptauWPS/TLL_legacy_MVAs/"
eras_to_do = ["2018"]

cards_MVA = {
    "2lss_0tau_ee_Restnode" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_output_NN_rest_ee.root"},
    "2lss_0tau_em_Restnode" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_output_NN_rest_em.root"},
    "2lss_0tau_mm_Restnode" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_output_NN_rest_mm.root"} ,
    "2lss_0tau_ee_tHQnode"  : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_output_NN_tH_ee.root"},
    "2lss_0tau_em_tHQnode"  : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_output_NN_tH_em.root"},
    "2lss_0tau_mm_tHQnode"  : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_output_NN_tH_mm.root"},
    "2lss_0tau_ee_ttHnode"  : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_output_NN_ttH_ee.root"},
    "2lss_0tau_em_ttHnode"  : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_output_NN_ttH_em.root"},
    "2lss_0tau_mm_ttHnode"  : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_output_NN_ttH_mm.root"},
    "2lss_0tau_ee_ttWnode"  : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_output_NN_ttW_ee.root"},
    "2lss_0tau_em_ttWnode"  : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_output_NN_ttW_em.root"},
    "2lss_0tau_mm_ttWnode"  : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_output_NN_ttW_mm.root"},
    ########################
    "3l_0tau_rest_eee"      : {"channel" : "3l_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_3l_0tau_2018/datacards/3l/prepareDatacards/prepareDatacards_3l_OS_output_NN_rest_eee.root"},
    "3l_0tau_rest_eem"      : {"channel" : "3l_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_3l_0tau_2018/datacards/3l/prepareDatacards/prepareDatacards_3l_OS_output_NN_rest_eem.root"},
    "3l_0tau_rest_emm"      : {"channel" : "3l_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_3l_0tau_2018/datacards/3l/prepareDatacards/prepareDatacards_3l_OS_output_NN_rest_emm.root"},
    "3l_0tau_rest_mmm"      : {"channel" : "3l_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_3l_0tau_2018/datacards/3l/prepareDatacards/prepareDatacards_3l_OS_output_NN_rest_mmm.root"},
    "3l_0tau_tH_bl"         : {"channel" : "3l_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_3l_0tau_2018/datacards/3l/prepareDatacards/prepareDatacards_3l_OS_output_NN_tH_bl.root"},
    "3l_0tau_tH_bt"         : {"channel" : "3l_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_3l_0tau_2018/datacards/3l/prepareDatacards/prepareDatacards_3l_OS_output_NN_tH_bt.root"},
    "3l_0tau_ttH_bl"        : {"channel" : "3l_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_3l_0tau_2018/datacards/3l/prepareDatacards/prepareDatacards_3l_OS_output_NN_ttH_bl.root"},
    "3l_0tau_ttH_bt"        : {"channel" : "3l_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_3l_0tau_2018/datacards/3l/prepareDatacards/prepareDatacards_3l_OS_output_NN_ttH_bt.root"},
    ###########################
    "3l_cr_eee"             : {"channel" : "3lctrl",  "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_3l_0tau_CR_2018/datacards/3lctrl/prepareDatacards/prepareDatacards_3lctrl_OS_control_eee.root"},
    "3l_cr_eem"             : {"channel" : "3lctrl",  "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_3l_0tau_CR_2018/datacards/3lctrl/prepareDatacards/prepareDatacards_3lctrl_OS_control_eem.root"},
    "3l_cr_emm"             : {"channel" : "3lctrl",  "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_3l_0tau_CR_2018/datacards/3lctrl/prepareDatacards/prepareDatacards_3lctrl_OS_control_emm.root"},
    "3l_cr_mmm"             : {"channel" : "3lctrl",  "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_3l_0tau_CR_2018/datacards/3lctrl/prepareDatacards/prepareDatacards_3lctrl_OS_control_mmm.root"},
    ###########################
    "2lss_1tau_rest"        : {"channel" : "2lss_1tau", "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_2lss_1tau_2018/datacards/2lss_1tau/prepareDatacards/prepareDatacards_2lss_1tau_sumOS_output_NN_rest.root"},
    "2lss_1tau_tH"          : {"channel" : "2lss_1tau", "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_2lss_1tau_2018/datacards/2lss_1tau/prepareDatacards/prepareDatacards_2lss_1tau_sumOS_output_NN_tH.root"},
    "2lss_1tau_ttH"         : {"channel" : "2lss_1tau", "shapes" : "/home/acaan/ttHAnalysis/2018/legacy_fullSyst_2lss_1tau_2018/datacards/2lss_1tau/prepareDatacards/prepareDatacards_2lss_1tau_sumOS_output_NN_ttH.root"},
}

cards_SVA = {
    "2lss_0tau_cr"        : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_cr.root"},
    "2lss_0tau_ee_hj_neg" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_ee_hj_neg.root"},
    "2lss_0tau_ee_hj_pos" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_ee_hj_pos.root"},
    "2lss_0tau_ee_lj_neg" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_ee_lj_neg.root"},
    "2lss_0tau_ee_lj_pos" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_ee_lj_pos.root"},
    "2lss_0tau_em_hj_neg" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_em_hj_neg.root"},
    "2lss_0tau_em_hj_pos" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_em_hj_pos.root"},
    "2lss_0tau_em_lj_neg" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_em_lj_neg.root"},
    "2lss_0tau_em_lj_pos" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_em_lj_pos.root"},
    "2lss_0tau_mm_hj_neg" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_mm_hj_neg.root"},
    "2lss_0tau_mm_hj_pos" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_mm_hj_pos.root"},
    "2lss_0tau_mm_lj_neg" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_mm_lj_neg.root"},
    "2lss_0tau_mm_lj_pos" : {"channel" : "2lss_0tau", "shapes" : "/home/acaan/ttHAnalysis/2018/2lss_0tau_central_DNN_legacy_IHEP_DNN_2018_20Dec2019/datacards/2lss/prepareDatacards/prepareDatacards_2lss_mass_2L_mm_lj_pos.root"},
    ######################
    ## 3l
    ######################
    ## 4l
}

for era in eras_to_do :
    for key in cards_MVA :
        print (key)
        print (cards_MVA[key])
        cmd = "WriteDatacards.py "
        cmd += "--inputShapes %s " % (cards_MVA[key]["shapes"].replace("2018", era))
        cmd += "--channel %s "     % (cards_MVA[key]["channel"].replace("2018", era))
        cmd += "--cardFolder %s "  % output_cards
        cmd += "--noX_prefix  "
        if not "ctrl" in key :
            cmd += "--no_data "
        cmd += "--era %s" % str(era)
        cmd += " --output_file %s/ttH_%s_%s" % (output_cards, key, era)
        # cmd += "--shapeSyst " ### for first tests
        runCombineCmd(cmd)
    #######################
    # combine cards to make plots -- the order of lists of flavours is important
    if "3l_cr_eee" in list(cards_MVA.keys()) :
        cmd = "combineCards.py "
        for flavor in ["eee", "eem", "emm", "mm"] :
            cmd += " 3lctr_%s=ttH_3l_cr_%s_%s.txt" % (flavor, flavor, era)
        cmd += " > ttH_3l_cr_%s.txt" % era
        runCombineCmd(cmd, output_cards)
    #
    if "2lss_0tau_ee_Restnode" in list(cards_MVA.keys()) :
        cmd = "combineCards.py "
        for node in ["Rest", "ttH", "ttW", "tHQ"] :
          for flavor in ["ee", "em", "mm"] :
            cmd += "2lss_0tau_%s_%snode=ttH_2lss_0tau_%s_%snode" % (flavor, node, flavor, node, era)
        cmd += " > ttH_2lss_0tau_%snode_%s.txt" % (node, era)
        runCombineCmd(cmd, output_cards)
    #
    if "3l_0tau_rest_eee" in list(cards_MVA.keys()) :
        cmd = "combineCards.py "
        for node in ["ttH", "tH"] :
          for flavor in ["bt", "bl"] :
            cmd += "3l_0tau_%s_%s=ttH_3l_0tau_%s_%s" % (node, flavor, node, flavor, era)
        cmd += " > ttH_3l_0tau_%s_%s.txt" % (node, era)
        runCombineCmd(cmd, output_cards)
        cmd = "combineCards.py "
        for flavor in ["eee", "eem", "emm", "mmm"] :
            cmd += "3l_0tau_rest_%s=ttH_3l_0tau_rest_%s" % (flavor, flavor, era)
        cmd += " > ttH_3l_0tau_rest_%s.txt" % (era)
        runCombineCmd(cmd, output_cards)
    #
    if "2lss_1tau_rest" in list(cards_MVA.keys()) :
        cmd = "combineCards.py "
        for node in ["ttH", "tH", "rest"] :
            cmd += "2lss_1tau_%s=ttH_2lss_0tau_%s_%s" % (node, node, era)
        cmd += " > ttH_2lss_1tau_%s.txt" % (era)
        runCombineCmd(cmd, output_cards)
    ##################################
    # combine all cards to make fits / era
    cmd = "combineCards.py "
    for key in list(cards_MVA.keys()) :
        cmd += " %s=ttH_%s_%s.txt" % (key, output_cards, key, era)
    cmd += " > ttH_multilep_%s.txt" % (era)
    runCombineCmd(cmd, output_cards)
############################################
# combine all cards to make fits
cmd = "combineCards.py "
for era in eras_to_do :
    cmd += " ttH_%s= ttH_multilep_%s.txt" % (era, era)
cmd += " > ttH_multilep.txt"
