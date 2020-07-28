def read_from():
    withFolderL = True
    #localL = "/afs/cern.ch/work/a/acarvalh/cards_set/hh_bb1l_26Jul_baseline_TTSL_noWjj_dataMC/"
    localL = "/afs/cern.ch/work/a/acarvalh/cards_set/hh_bb1l_26Jul_baseline_noWjj_dataMC/"
    mom    = "/afs/cern.ch/work/a/acarvalh/public/to_HH_bbWW/SL/hh_bb1l_26Jul_baseline_TTSL_noWjj_dataMC/prepareDatacards/"
    label  = "hh_bb1l_26Jul_baseline_TTSL_noWjj_dataMC"
    BDTfor = "X900GeV"
    BDTfor = "SM"
    recoWjj = "Wjj_simple"
    #recoWjj = "Wjj_BDT"
    in_more_subcats = False
    if not in_more_subcats : # did the hadd by hand
        bdtTypes =  [
        #"cat_jet_2BDT_%s_%s_HbbFat_WjjRes_MissJet" % (recoWjj, BDTfor),
        #"cat_jet_2BDT_%s_%s_HbbFat_WjjRes_allReco" % (recoWjj, BDTfor),
        #"cat_jet_2BDT_%s_%s_Res_MissWJet" % (recoWjj, BDTfor),
        #"cat_jet_2BDT_%s_%s_Res_allReco" % (recoWjj, BDTfor)
        ###
        #"cat_jet_2BDT_Wjj_BDT_%s_HbbFat_WjjRes_allReco" % (BDTfor),
        #"cat_jet_2BDT_Wjj_simple_%s_HbbFat_WjjRes_allReco" % (BDTfor),
        ##
        "cat_jet_2BDT_Wjj_BDT_%s_Res_allReco" % (BDTfor),
        "cat_jet_2BDT_Wjj_simple_%s_Res_allReco" % (BDTfor),
        ###
        #"cat_jet_2BDT_%s_%s_HbbFat_WjjRes_MissJet" % (recoWjj, BDTfor),
        #"cat_jet_2BDT_%s_%s_Res_MissWJet" % (recoWjj, BDTfor),
        ]
    else :
        bdtTypes = [
        "cat_jet_2BDT_%s_%s_HbbFat_WjjRes_MissJet_e" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_HbbFat_WjjRes_MissJet_m" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_HbbFat_WjjRes_allReco_e" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_HbbFat_WjjRes_allReco_m" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_MissWJet_1b_e" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_MissWJet_1b_m" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_MissWJet_2b_e" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_MissWJet_2b_m" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_allReco_1b_e" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_allReco_1b_m" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_allReco_2b_e" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_allReco_2b_m" % (recoWjj, BDTfor),
        ]
    # If there are subcategories construct the list of files to read based on their naming convention

    channelsTypes = [ "1l_0tau" ]
    ch_nickname = "hh_bb1l_hh_bb1l"

    originalBinning=100
    #nbinRegular = np.arange(4, 31)
    #nbinRegular = np.arange(31, 41)
    nbinRegular = np.arange(20, 15)
    nbinQuant = np.arange(20, 21)

    maxlim = 2.0
    minlim = 0.0

    output = {
    "withFolder"      : withFolderL,
    "label"           : label,
    "mom"             : mom,
    "bdtTypes"        : bdtTypes,
    "channelsTypes"   : channelsTypes,
    "originalBinning" : originalBinning,
    "nbinRegular"     : nbinRegular,
    "nbinQuant"       : nbinQuant,
    "maxlim"          : maxlim,
    "minlim"          : minlim,
    "ch_nickname"     : ch_nickname,
    "local"           : localL,
    "makePlotsBin"    : [40]
    }

    return output
