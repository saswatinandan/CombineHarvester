def list_channels(analysis) :
    if analysis == "ttH" :
        sigs = ["ttH", "tHq", "tHW", "VH"]
        decays = ["hww", "hzz", "htt", "hzg", "hmm" ]
        higgs_procs = [ [y + "_" + x  for x in decays if not (x in ["hzg", "hmm"] and y != "ttH")] for y in sigs]
        #higgs_procs = [ [y + "_" + x  for x in decays if not (x in ["hzz", "htt", "hzg", "hmm"] and y != "ttH")] for y in sigs]
        ## add the H processes (that shall be marked as signal on the datacards)

        info_channel = {
        "2lss_0tau" : { "bkg_proc_from_data" : ["fakes_data", "flips_data"], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares", "conversions"], "isSMCSplit" : False}, 
        "ttWctrl"   : { "bkg_proc_from_data" : ["fakes_data", "flips_data"], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares", "conversions"], "isSMCSplit" : False},
        "2lss_1tau" : { "bkg_proc_from_data" : ["fakes_data", "flips_data"], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares", "conversions"], "isSMCSplit" : True},
        "3l_0tau"   : { "bkg_proc_from_data" : ["fakes_data"              ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares", "conversions"], "isSMCSplit" : False},
        "1l_2tau"   : { "bkg_proc_from_data" : ["fakes_data"              ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares", "conversions"], "isSMCSplit" : False},
        "ttZctrl"   : { "bkg_proc_from_data" : ["fakes_data"              ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares", "conversions"], "isSMCSplit" : False},
        "2l_2tau"   : { "bkg_proc_from_data" : ["fakes_data"              ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares", "conversions"], "isSMCSplit" : False},
        "3l_1tau"   : { "bkg_proc_from_data" : ["fakes_data"              ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares", "conversions"], "isSMCSplit" : True}, 
        "1l_2tau"   : { "bkg_proc_from_data" : ["fakes_data"              ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares", "conversions"], "isSMCSplit" : False},
        "2los_1tau" : { "bkg_proc_from_data" : ["fakes_data"              ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares", "conversions"], "isSMCSplit" : False},
        "0l_2tau"   : { "bkg_proc_from_data" : ["fakes_data"              ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares"],                "isSMCSplit" : False},
        "1l_1tau"   : { "bkg_proc_from_data" : ["fakes_data"              ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares"],                "isSMCSplit" : False},
        "WZctrl"    : { "bkg_proc_from_data" : ["fakes_data"              ], "bkg_procs_from_MC"  : ["TTW", "TTWW", "TTZ", "EWK", "Rares"],                "isSMCSplit" : False},
        "4l_0tau"   : { "bkg_proc_from_data" : ["fakes_data"              ], "bkg_procs_from_MC"  : ["TTW", "TTZ", "ZZ",  "Rares", "conversions"],         "isSMCSplit" : False},
        "ZZctrl"    : { "bkg_proc_from_data" : ["fakes_data"              ], "bkg_procs_from_MC"  : ["TTZ",  "ZZ", "Rares"],                               "isSMCSplit" : False},
        }
    else : sys.exit("analysis " + analysis + " not implemented")
    return {
        "higgs_procs"      : higgs_procs,
        "decays"           : decays,
        "info_bkg_channel" : info_channel 
    }

