def read_from():

    withFolder = False
    label = "3l_0tau_central_deepVSjVLoose_veto_master_cards_withWZ_2_2019Oct09_2016"
    mom="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/deeptauWPS/"+label+"/prepareDatacards/"
    bdtTypes = [
    #"mvaDiscr_3l"
    "output_NN_sig_2p5_rest_2_th_2p5_withWZ",
    "output_NN_sig_2_rest_2p5_th_2_withWZ",
    "output_NN_sig_2_rest_2_th_2_withWZ"
    #"output_NN_3l_ttH_tH_3cat_v8"
    ]
    # If there are subcategories construct the list of files to read based on their naming convention
    cateDraw_type = [ "tH", "ttH"] # "rest"] #
    cateDraw_btag = ["bl", "bt"]
    cateDraw_flavour = [ "eee" , "eem" ,"mmm", "emm"] #
    bdtTypes_exp = []
    for bdtType in bdtTypes :
        if "output_" in bdtType :
            for catType in cateDraw_type :
                for cat_btag in cateDraw_btag :
                    for cat_flav in cateDraw_flavour :
                        if catType == "rest" :
                                if cat_flav == "eee" :
                                    bdtTypes_exp += [ bdtType + "_" + catType + "_" + cat_flav ]
                                else :
                                    bdtTypes_exp += [ bdtType + "_" + catType + "_" + cat_flav + "_" + cat_btag]
                        else :
                            bdtTypes_exp += [ bdtType + "_" + catType+ "_" + cat_btag]
        else :
            bdtTypes_exp += [bdtType]

    if len(cateDraw_type) == 0 : bdtTypes_exp = bdtTypes

    channelsTypes = [ "3l_0tau" ]
    ch_nickname = "3l_OS"

    originalBinning=100
    nbinRegular = np.arange(10, 12)
    nbinQuant = np.arange(1, 8)

    maxlim = 2.0

    output = {
    "withFolder"      : withFolder,
    "label"           : label,
    "mom"             : mom,
    "bdtTypes"        : list(set(bdtTypes_exp)),
    "channelsTypes"   : channelsTypes,
    "originalBinning" : originalBinning,
    "nbinRegular"     : nbinRegular,
    "nbinQuant"       : nbinQuant,
    "maxlim"          : maxlim,
    "ch_nickname"     : ch_nickname,
    }

    return output
