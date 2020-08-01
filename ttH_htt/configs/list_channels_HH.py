def list_channels( fake_mc, signal_type="none", mass="none", HHtype="none", renamedHHInput=False ) :
    #####################
    # signal_type = "noresLO" | "nonresNLO" | "res"
    # mass nonres = "cHHH1" | cHHH... || "SM", "BM12", "kl_1p00"... || "spin0_900",....
    # HHtype = "bbWW" | "multilep"
    #####################
    sigs = ["ttH", "tHq", "tHW", "WH", "ZH", "ggH", "qqH" ]
    decays = ["_hww", "_hzz", "_htt", "_hzg", "_hmm" ]
    # FIXME ---> to be used when the cards are done with Higs processes in Physics model
    # naming convention and separating by branching ratio
    # by now it will look for them (eg ttH_hww) in the prepareDatacards and not find
    decays_hh = []
    if renamedHHInput :
        if HHtype == "bbWW" :
            decays_hh = ["SL_hbb_hww", "DL_hbb_hww", "hbb_htt"]
            decays_hh_vbf = ["hbb_htt"]
        elif HHtype == "bbWW_bbtt" :
            decays_hh = ["hbb_htt"]
            decays_hh_vbf = ["hbb_htt"]
        elif HHtype == "bbWW_SL" :
            decays_hh = ["SL_hbb_hww"]
            decays_hh_vbf = []
        elif HHtype == "bbWW_DL" :
            decays_hh = ["DL_hbb_hww"]
            decays_hh_vbf = []
        else :
            print("HHtype (%s) not implemented" % ( HHtype))
            sys.exit()
    else :
        if HHtype == "bbWW" :
            decays_hh = ["bbvv_sl", "bbtt", "bbvv"]
        elif HHtype == "bbWW_SL" :
            decays_hh = ["bbvv_sl"]
        elif HHtype == "bbWW_DL" :
            decays_hh = ["bbvv"]
        else :
            print("HHtype (%s) not implemented" % ( HHtype))
            sys.exit()

    #---> by now not used, we may use to implement systematics/BR -- see how decays_hh is used in WriteDatacards
    higgs_procs = [ [y + x  for x in decays if not (x in ["hzg", "hmm"] and y != "ttH")] for y in sigs]

    prefix_VBF = "signal_ggf_nonresonant"
    SM_VBF     = "1_1_1"
    prefix_GF  = "signal_ggf_nonresonant"
    couplings_GF_NLO = [ "cHHH0", "cHHH1", "cHHH5" ]
    # --> using "cHHH2p45" as control -- check closure to see if this is the best case
    couplings_VBF    = [ "1_1_1", "1_1_2", "1_2_1", "1_1_0", "1p5_1_1", "0p5_1_1" ]
    if renamedHHInput :
        prefix_VBF = "qqHH"
        SM_VBF     = "CV_1_C2V_1_kl_1"
        prefix_GF  = "ggHH"
        couplings_GF_NLO = [ "kl_0_kt_1", "kl_1_kt_1", "kl_5_kt_1" ]
        # --> using "cHHH2p45" as control -- check closure to see if this is the best case
        couplings_VBF    = [ "CV_1_C2V_1_kl_1", "CV_1_C2V_1_kl_2", "CV_1_C2V_2_kl_1",  "CV_1_C2V_1_kl_0", "CV_1p5_C2V_1_kl_1" ] # , "CV_0p5_C2V_1_kl_1"

    if signal_type == "nonresLO" :
        listSig = []
        for decay_hh in decays_hh :
            listSig = listSig + [
            "%s_hh_%s%s"  % (prefix_GF, decay_hh, mass),
            "%s_%s_hh_%s" % (prefix_VBF, SM_VBF, decay_hh)
            ]
        sigs = [ listSig ]
    elif signal_type == "nonresNLO" :
        listSig = []
        for decay_hh in decays_hh :
            for massType in couplings_GF_NLO :
                listSig = listSig + [ "%s_%s_hh_%s" % (prefix_GF, massType , decay_hh) ]
        for decay_hh in decays_hh_vbf :
            for massType in couplings_VBF :
                listSig = listSig + [ "%s_%s_hh_%s" % (prefix_VBF, massType, decay_hh) ]
        sigs = [ listSig ]
    elif signal_type == "res" :
        listSig = []
        for decay_hh in decays_hh :
            listSig = listSig + [ "signal_ggf_%s_hh_%s" % (mass, decay_hh) ]
        sigs = [ listSig ]
    else :
        print("signal_type %s not implemented" % (signal_type))
        sys.exit()
    # FIXME ---> add VBF to nonres case (SM by default)
    # FIXME ---> add multilep options
    ######################
    #sigs = [["signal_ggf_nonresonant_cHHH1_hh_bbtt", "signal_ggf_nonresonant_cHHH1_hh_bbvv_sl", "signal_ggf_nonresonant_cHHH1_hh_bbvv"]]
    #sigs = [["signal_ggf_nonresonant_hh_bbttSM", "signal_ggf_nonresonant_hh_bbvv_slSM", "signal_ggf_nonresonant_hh_bbvvSM" ]]
    #sigs = [["signal_ggf_nonresonant_hh_bbttBM12", "signal_ggf_nonresonant_hh_bbvv_slBM12", "signal_ggf_nonresonant_hh_bbvvBM12" ]]
    #sigs = [["signal_ggf_spin0_900_hh_bbtt", "signal_ggf_spin0_900_hh_bbvv", "signal_ggf_spin0_900_hh_bbvv_sl"]]
    #sigs = [["signal_ggf_spin0_400_hh_bbtt", "signal_ggf_spin0_400_hh_bbvv", "signal_ggf_spin0_400_hh_bbvv_sl"]]
    #sigs = [["signal_ggf_nonresonant_hh_bbttkl_1p00", "signal_ggf_nonresonant_hh_bbvv_slkl_1p00", "signal_ggf_nonresonant_hh_bbvvkl_1p00"]]
    #higgs_procs = higgs_procs + sigs
    higgs_procs = sigs + [["ttH_hww", "tHW_hww", "WH_hww"]]
    #higgs_procs = sigs

    conversions = "Convs"
    if fake_mc :
        fakes       = "fakes_mc"
        flips       = "flips_mc"
    else :
        fakes       = "data_fakes"
        flips       = "data_flips"

    info_channel = {
        "2l_0tau" : {
            "bkg_proc_from_data" : [ fakes    ],
            "bkg_procs_from_MC"  : ["Convs", "TTZ", "TTW", "TTWW", "TT", "Other", "DY", "W", "WW", "WZ", "ZZ"], # "TTH", "TH", "VH",
            "isSMCSplit" : False,
            "proc_to_remove" : {}
        },
        "1l_0tau" : {
            "bkg_proc_from_data" : [ fakes    ],
            "bkg_procs_from_MC"  : ["Convs", "TTZ", "TTW", "TTWW", "TT", "Other", "DY", "W", "WW", "WZ", "ZZ"],
            "isSMCSplit" : False,
            "proc_to_remove" : {}
        }
    }
    #---> by now "TTH", "TH" and "VH" are automatically marked as BKG

    return {
        "higgs_procs"      : higgs_procs,
        "decays"           : [],
        "decays_hh"        : decays_hh,
        "info_bkg_channel" : info_channel,
        "higgs_procs_to_draw"      : sigs[0],
    }
