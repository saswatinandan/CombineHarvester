def read_from():
    # /home/acaan/hhAnalysis/2016/hh_bb1l_7Jun_SM_default_boostedCat_central/datacards/hh_bb1l/prepareDatacards/
    withFolder = False
    label = "hh_bb1l_24Jun_SM_default_AK8_LS_fluxogramLike"
    #label = "hh_bb1l_12Jun_SM_default_AK8_LS"
    #label = "hh_bb1l_12Jun_SM_default_AK8"
    mom="/home/acaan/hhAnalysis/2016/"+label+"/datacards/hh_bb1l/prepareDatacards/"
    bdtTypes = [
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_one_jet_to_Wjj_Hbb_boosted", # _X900GeV
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_one_jet_to_Wjj_resolved", # _X900GeV
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_Wjj_Hbb_reco_boosted",
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_Wjj_Hbb_reco_Hbb_boosted",
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_Wjj_Hbb_reco_resolved",
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_Wjj_Hbb_reco_Wjj_boosted",
        ######
        #"cat_jet_2BDT_Wjj_simple_X900GeV_one_jet_to_Wjj_Hbb_boosted",
        #"cat_jet_2BDT_Wjj_simple_X900GeV_one_jet_to_Wjj_resolved",
        #"cat_jet_2BDT_Wjj_simple_X900GeV_Wjj_Hbb_reco_boosted",
        #"cat_jet_2BDT_Wjj_simple_X900GeV_Wjj_Hbb_reco_Hbb_boosted",
        #"cat_jet_2BDT_Wjj_simple_X900GeV_Wjj_Hbb_reco_resolved",
        #"cat_jet_2BDT_Wjj_simple_X900GeV_Wjj_Hbb_reco_Wjj_boosted",
        ###
        #"cat_jet_2BDT_Wjj_BDT_Wjj_Hbb_reco_Hbb_boosted",
        #"cat_jet_2BDT_Wjj_simple_Wjj_Hbb_reco_Hbb_boosted",
        ###
        #"cat_jet_2BDT_Wjj_BDT_HbbFat_WjjFat_HP_e",
        #"cat_jet_2BDT_Wjj_BDT_HbbFat_WjjFat_LP_e",
        #"cat_jet_2BDT_Wjj_BDT_WjjFat_HP_e",
        #"cat_jet_2BDT_Wjj_BDT_WjjFat_LP_e",
        #"cat_jet_2BDT_Wjj_BDT_HbbFat_WjjRes_allReco_e",
        #"cat_jet_2BDT_Wjj_BDT_HbbFat_WjjRes_MissJet_e",
        #"cat_jet_2BDT_Wjj_BDT_Res_allReco_e",
        #"cat_jet_2BDT_Wjj_BDT_Res_MissWJet_e",
        #"cat_jet_2BDT_Wjj_BDT_Res_MissBJet_e",
        ####
        #"cat_jet_2BDT_Wjj_BDT_HbbFat_WjjFat_HP_m",
        #"cat_jet_2BDT_Wjj_BDT_HbbFat_WjjFat_LP_m",
        #"cat_jet_2BDT_Wjj_BDT_WjjFat_HP_m",
        ##"cat_jet_2BDT_Wjj_BDT_WjjFat_LP_m",
        #"cat_jet_2BDT_Wjj_BDT_HbbFat_WjjRes_allReco_m",
        #"cat_jet_2BDT_Wjj_BDT_HbbFat_WjjRes_MissJet_m",
        #"cat_jet_2BDT_Wjj_BDT_Res_allReco_m",
        #"cat_jet_2BDT_Wjj_BDT_Res_MissWJet_m",
        #"cat_jet_2BDT_Wjj_BDT_Res_MissBJet_m",
        ##
        #"cat_jet_2BDT_Wjj_BDT_HbbFat_WjjFat_HP",
        #"cat_jet_2BDT_Wjj_BDT_HbbFat_WjjFat_LP",
        #"cat_jet_2BDT_Wjj_BDT_WjjFat_HP",
        #"cat_jet_2BDT_Wjj_BDT_WjjFat_LP",
        #"cat_jet_2BDT_Wjj_BDT_HbbFat_WjjRes_allReco",
        #"cat_jet_2BDT_Wjj_BDT_HbbFat_WjjRes_MissJet",
        #"cat_jet_2BDT_Wjj_BDT_Res_allReco",
        #"cat_jet_2BDT_Wjj_BDT_Res_MissWJet",
        #"cat_jet_2BDT_Wjj_BDT_Res_MissBJet",
        ##
        #"cat_jet_2BDT_Wjj_simple_Res_allReco",
        #"cat_jet_2BDT_Wjj_simple_HbbFat_WjjRes_allReco",
        ##
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_HbbFat_WjjFat_HP",
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_HbbFat_WjjFat_LP",
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_WjjFat_HP",
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_WjjFat_LP",
        "cat_jet_2BDT_Wjj_BDT_X900GeV_HbbFat_WjjRes_allReco",
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_HbbFat_WjjRes_MissJet",
        "cat_jet_2BDT_Wjj_BDT_X900GeV_Res_allReco",
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_Res_MissWJet",
        #"cat_jet_2BDT_Wjj_BDT_X900GeV_Res_MissBJet",
        ##
        "cat_jet_2BDT_Wjj_simple_X900GeV_Res_allReco",
        "cat_jet_2BDT_Wjj_simple_X900GeV_HbbFat_WjjRes_allReco",
    ]
    # If there are subcategories construct the list of files to read based on their naming convention

    channelsTypes = [ "1l_0tau" ]
    ch_nickname = "hh_bb1l_hh_bb1l"

    originalBinning=100
    #nbinRegular = np.arange(4, 31)
    #nbinRegular = np.arange(31, 41)
    nbinRegular = np.arange(30, 31)
    nbinQuant = np.arange(1, 20)

    maxlim = 2.0

    output = {
    "withFolder"      : withFolder,
    "label"           : label,
    "mom"             : mom,
    "bdtTypes"        : bdtTypes,
    "channelsTypes"   : channelsTypes,
    "originalBinning" : originalBinning,
    "nbinRegular"     : nbinRegular,
    "nbinQuant"       : nbinQuant,
    "maxlim"          : maxlim,
    "ch_nickname"     : ch_nickname,
    }

    return output
