def read_from():
    withFolder = False
    label = "hh_bb2l_12May_SM_default_central"
    mom="/home/acaan/hhAnalysis/2017/"+label+"/datacards/hh_bb2l/prepareDatacards/"
    bdtTypes = [
        # SM_plainVars_noHH_withbb_ee_MHH1.root
        # M_plainVars_noHH_mm_MHH5_medMbb/low/high
        #"SM_plainVars_Xness_nocat",
        #"SM_plainVars_noHH_nocat",
        #"SM_plainVars_noHH_withbb_nocat",
        #"SM_plainVars_nocat"
        #"SM_plainVars_ee",
        #"SM_plainVars_em",
        #"SM_plainVars_mm",
        "SM_plainVars_noHH_withbb_nocat",
    ]
    # If there are subcategories construct the list of files to read based on their naming convention
    ## prepareDatacards_2lss_1tau_sumOS_output_NN_2lss_1tau_ttH_tH_3cat_v5_ttH_1tau.root

    channelsTypes = [ "0l_2tau" ]
    ch_nickname = "hh_bb2l_hh_bb2l_OS"

    originalBinning=100
    nbinRegular = np.arange(4, 31)
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
