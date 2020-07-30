def read_from():
    withFolderL = True
    label  = "hh_bb1l_26Jul_baseline_TTSL_noWjj_dataMC"
    BDTfor = "X900GeV"
    #BDTfor = "SM"
    recoWjj = "Wjj_simple"
    #recoWjj = "Wjj_BDT"
    in_more_subcats = False
    if not in_more_subcats :
        bdtTypes =  [
        #### one does he hadd's by hand of the categories you want to merge
        #"cat_jet_2BDT_%s_%s_HbbFat_WjjRes_MissWJet" % (recoWjj, BDTfor),
        #"cat_jet_2BDT_%s_%s_Res_MissWJet" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_HbbFat_WjjRes_allReco" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_allReco" % (recoWjj, BDTfor)
        ]
    else :
        bdtTypes = [
        #"cat_jet_2BDT_%s_%s_HbbFat_WjjRes_MissJet_e" % (recoWjj, BDTfor),
        #"cat_jet_2BDT_%s_%s_HbbFat_WjjRes_MissJet_m" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_HbbFat_WjjRes_allReco_e" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_HbbFat_WjjRes_allReco_m" % (recoWjj, BDTfor),
        #"cat_jet_2BDT_%s_%s_Res_MissWJet_1b_e" % (recoWjj, BDTfor),
        #"cat_jet_2BDT_%s_%s_Res_MissWJet_1b_m" % (recoWjj, BDTfor),
        #"cat_jet_2BDT_%s_%s_Res_MissWJet_2b_e" % (recoWjj, BDTfor),
        #"cat_jet_2BDT_%s_%s_Res_MissWJet_2b_m" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_allReco_1b_e" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_allReco_1b_m" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_allReco_2b_e" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_allReco_2b_m" % (recoWjj, BDTfor),
        ]

    channelsTypes = [ "1l_0tau" ]
    ch_nickname = "hh_bb1l_hh_bb1l"

    originalBinning=100
    nbinRegular = np.arange(8, 10)
    nbinQuant = np.arange(20, 21)

    maxlim = 2.0
    minlim = 0.0

    output = {
    "withFolder"      : withFolderL,
    "label"           : label,
    "bdtTypes"        : bdtTypes,
    "channelsTypes"   : channelsTypes,
    "originalBinning" : originalBinning,
    "nbinRegular"     : nbinRegular,
    "nbinQuant"       : nbinQuant,
    "maxlim"          : maxlim,
    "minlim"          : minlim,
    "ch_nickname"     : ch_nickname,
    "makePlotsBin"    : [8]
    }

    return output
