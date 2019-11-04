def read_from():

    withFolder = False
    label = "0l_2tau_central_deepVSjVTight_veto_master_cards_2019Nov03_2018"
    #label = "0l_2tau_central_deepVSjTight_veto_master_cards_2019Oct09_2018"
    mom="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/deeptauWPS/"+label+"/prepareDatacards/"
    bdtTypes = [
        #"mva_Updated",
        "mvaOutput_0l_2tau_deeptauLoose",
        "mvaOutput_0l_2tau_deeptauVTight"
    ]
    # If there are subcategories construct the list of files to read based on their naming convention
    ## prepareDatacards_2lss_1tau_sumOS_output_NN_2lss_1tau_ttH_tH_3cat_v5_ttH_1tau.root

    channelsTypes = [ "0l_2tau" ]
    ch_nickname = "0l_2tau_0l_2tau"

    originalBinning=100
    nbinRegular = np.arange(7, 20)
    nbinQuant = np.arange(1, 12)

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
