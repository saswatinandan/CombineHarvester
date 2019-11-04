def read_from():

    withFolder = False
    label = "2lss_1tau_central_deepVSjVLoose_veto_master_cards_withWZ_2_2019Oct09_2016/"
    #mom="/home/acaan/ttHAnalysis/2017/"+label+"/datacards/2lss"
    mom="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/deeptauWPS/" + label + "/prepareDatacards/"
    bdtTypes = [
        #"ttH_2lss_1tau_only_ttHsel",
        "output_NN_sig_1p2_rest_1_th_1p2",
        #"output_NN_sig_2_rest_2p2_th_2",
        "output_NN_sig_2_rest_2p5_th_2",
        "output_NN_sig_2_rest_2_th_2"
    ]
    # If there are subcategories construct the list of files to read based on their naming convention
    ## prepareDatacards_2lss_1tau_sumOS_output_NN_2lss_1tau_ttH_tH_3cat_v5_ttH_1tau.root
    cateDraw_type = [ "tH", "ttH" , "rest",] #
    bdtTypes_exp = []
    for bb, bdtType in enumerate(bdtTypes) :
      #if bb == 0 : bdtTypes_exp += [ bdtType ]
      #else :
      for catType in cateDraw_type :
        bdtTypes_exp += [ bdtType + "_" + catType ]
    #if len(cateDraw_type) == 0 : bdtTypes_exp = bdtTypes

    channelsTypes = [ "2lss_1tau" ]
    ch_nickname = "2lss_1tau_sumOS"

    originalBinning=100
    nbinRegular = np.arange(1, 10)
    nbinQuant = np.arange(3, 6)

    maxlim = 2.0

    output = {
    "withFolder"      : withFolder,
    "label"           : label,
    "mom"             : mom,
    "bdtTypes"        : bdtTypes_exp,
    "channelsTypes"   : channelsTypes,
    "originalBinning" : originalBinning,
    "nbinRegular"     : nbinRegular,
    "nbinQuant"       : nbinQuant,
    "maxlim"          : maxlim,
    "ch_nickname"     : ch_nickname,
    }

    return output
