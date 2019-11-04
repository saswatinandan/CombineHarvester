def read_from():

    withFolder = False
    label = "1l_2tau_central_deepVSjVLoose_veto_master_cards_2019Oct09_2016"
    #mom="/home/acaan/ttHAnalysis/2017/"+label+"/datacards/2lss"
    mom="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/deeptauWPS/"+label+"/prepareDatacards/"
    bdtTypes = [
        "mvaOutput_legacy",
    ]
    # If there are subcategories construct the list of files to read based on their naming convention
    ## prepareDatacards_2lss_1tau_sumOS_output_NN_2lss_1tau_ttH_tH_3cat_v5_ttH_1tau.root

    channelsTypes = [ "1l_2tau" ]
    ch_nickname = "1l_2tau"

    originalBinning=100
    nbinRegular = np.arange(6, 7)
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
