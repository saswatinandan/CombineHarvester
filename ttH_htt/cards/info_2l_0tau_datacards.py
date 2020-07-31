def read_from():
    withFolderL = True
    label  = "hh_bb1l_26Jul_baseline_TTSL_noWjj_dataMC"

    BDTfor = "SM"
    inclusive = True
    in_more_subcats    = True
    in_flavour_subcats = True

    if inclusive :
        bdtTypes =  [
        #### one does he hadd's by hand of the categories you want to merge
        "%s_plainVars_inclusive"             % BDTfor, #
        ]
    else :
        if not in_more_subcats :
            bdtTypes =  [
            #### one does he hadd's by hand of the categories you want to merge
            "%s_plainVars_cat"             % BDTfor, #
            "%s_plainVars_cat_Hbb_boosted" % BDTfor, #
            ]
        else :
            if not in_flavour_subcats :
                bdtTypes =  [
                #### one does he hadd's by hand of the categories you want to merge
                "%s_plainVars_cat_1b"          % BDTfor,
                "%s_plainVars_cat_2b"          % BDTfor,
                #"%s_plainVars_cat_Hbb_boosted" % BDTfor,
                ]
            else :
                bdtTypes = [
                "%s_plainVars_cat_ee_1b"          % BDTfor,
                "%s_plainVars_cat_ee_2b"          % BDTfor,
                "%s_plainVars_cat_ee_Hbb_boosted" % BDTfor,
                "%s_plainVars_cat_em_1b"          % BDTfor,
                "%s_plainVars_cat_em_2b"          % BDTfor,
                "%s_plainVars_cat_em_Hbb_boosted" % BDTfor,
                "%s_plainVars_cat_mm_1b"          % BDTfor,
                "%s_plainVars_cat_mm_2b"          % BDTfor,
                "%s_plainVars_cat_mm_Hbb_boosted" % BDTfor,
                ]

    channelsTypes = [ "2l_0tau" ]
    ch_nickname = "hh_bb2l_hh_bb2l_OS"

    originalBinning=100
    nbinRegular = np.arange(30, 51)
    nbinQuant = np.arange(20, 21)

    maxlim = 20.5
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
    "makePlotsBin"    : [45]
    }

    return output
