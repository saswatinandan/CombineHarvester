def read_from(in_more_subcats, BDTfor):
    withFolderL = True
    label  = "hh_bb1l_26Jul_baseline_TTSL_noWjj_dataMC"
    #BDTfor = "X900GeV"
    #BDTfor = "SM"
    #recoWjj = "Wjj_simple"
    recoWjj = "Wjj_BDT"

    if not in_more_subcats :
        bdtTypes =  [
        #### one does he hadd's by hand of the categories you want to merge
        #"cat_jet_2BDT_%s_%s_HbbFat_WjjRes_MissWJet" % (recoWjj, BDTfor),
        #"cat_jet_2BDT_%s_%s_Res_MissWJet" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_HbbFat_WjjRes_allReco" % (recoWjj, BDTfor),
        "cat_jet_2BDT_%s_%s_Res_allReco" % (recoWjj, BDTfor)
        ]
    elif in_more_subcats == "Res_allReco" :
        bdtTypes = [

            "cat_jet_2BDT_%s_%s_Res_allReco_1b_e" % (recoWjj, BDTfor),
            "cat_jet_2BDT_%s_%s_Res_allReco_1b_m" % (recoWjj, BDTfor),
            "cat_jet_2BDT_%s_%s_Res_allReco_2b_e" % (recoWjj, BDTfor),
            "cat_jet_2BDT_%s_%s_Res_allReco_2b_m" % (recoWjj, BDTfor),
        ]
    elif in_more_subcats == "boosted_semiboosted" :
        bdtTypes = [
            "cat_jet_2BDT_%s_%s_HbbFat_WjjFat_HP_e" % (recoWjj, BDTfor),
            "cat_jet_2BDT_%s_%s_HbbFat_WjjFat_HP_m" % (recoWjj, BDTfor),
            "cat_jet_2BDT_%s_%s_HbbFat_WjjFat_LP_e" % (recoWjj, BDTfor),
            "cat_jet_2BDT_%s_%s_HbbFat_WjjFat_LP_m" % (recoWjj, BDTfor),      
            "cat_jet_2BDT_%s_%s_HbbFat_WjjRes_allReco_e" % (recoWjj, BDTfor),
            "cat_jet_2BDT_%s_%s_HbbFat_WjjRes_allReco_m" % (recoWjj, BDTfor), 
        ]
    elif in_more_subcats == "one_missing_boosted" :
        bdtTypes = [
            "cat_jet_2BDT_%s_%s_HbbFat_WjjRes_MissJet_e" % (recoWjj, BDTfor),
            "cat_jet_2BDT_%s_%s_HbbFat_WjjRes_MissJet_m" % (recoWjj, BDTfor),
        ]
    elif in_more_subcats == "one_missing_resolved" : 
        bdtTypes = [
            "cat_jet_2BDT_%s_%s_Res_MissWJet_1b_e" % (recoWjj, BDTfor),
            "cat_jet_2BDT_%s_%s_Res_MissWJet_1b_m" % (recoWjj, BDTfor),
            "cat_jet_2BDT_%s_%s_Res_MissWJet_2b_e" % (recoWjj, BDTfor),
            "cat_jet_2BDT_%s_%s_Res_MissWJet_2b_m" % (recoWjj, BDTfor),
        ]


        
    channelsTypes = [ "1l_0tau" ]
    ch_nickname = "hh_bb1l_hh_bb1l"

    originalBinning=100
    nbinRegular = np.arange(4, 40)
    nbinQuant = np.arange(5,20)

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
        "makePlotsBin"    : [14]
    }

    return output
