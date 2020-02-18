### everthing that is marked as "uncorrelated" is renamed as:
### "CMS_ttHl" ->  "CMS_ttHl%s" % str(era).replace("20","")
### where era = 2016/2017/2018

# syst: theory and from MC generators - taken correlated between all years (check if that is what we want to do)
lumiSyst             = {2016: 1.022,          2017: 1.020,          2018: 1.015}
lumi_2016_2017_2018  = {2016: 1.009,          2017: 1.008,          2018: 1.020}
lumi_2017_2018       = {2017: 1.003,          2018: 1.004}
lumi_13TeV_BCC       = {2017: 1.003,          2018: 1.002}
lumi_2016_2017       = {2016: 1.008,          2017: 1.006}
lumi_13TeV_DB        = {2016: 1.005,          2017: 1.005}
lumi_13TeV_GS        = {2016: 1.004,          2017: 1.001}

theory_ln_Syst = {
    "pdf_Higgs_ttH"               : {"value": 1.036,              "proc" : ["ttH"]},
    "QCDscale_ttH"                : {"value": (0.907 , 1.058),    "proc" : ["ttH"]},
    "pdf_qg"                      : {"value": 1.01,               "proc" : ["tHq"]},
    "QCDscale_tHq"                : {"value": (0.933, 1.041),     "proc" : ["tHq"]},
    "pdf_qg_2"                    : {"value": 1.027,              "proc" : ["tHW"]}, # this is going to be renamed to "pdf_qg" on the main code
    "QCDscale_tHW"                : {"value": (0.939, 1.046),     "proc" : ["tHW"]},
    "pdf_ttW"                     : {"value": 1.04,               "proc" : ["TTW"]},
    "QCDscale_ttW"                : {"value": (0.885 , 1.129),    "proc" : ["TTW"]},
    "pdf_ttWW"                    : {"value": 1.03,               "proc" : ["TTWW"]},
    "QCDscale_ttWW"               : {"value": (0.891 , 1.081),    "proc" : ["TTWW"]},
    "pdf_ttZ"                     : {"value": 0.966,              "proc" : ["TTZ"]},
    "QCDscale_ttZ"                : {"value": (0.904 , 1.112),    "proc" : ["TTZ"]},
    "CMS_ttHl_WZ_theo"            : {"value": 1.07,               "proc" : ["WZ"]},
    "pdf_ttjets"                  : {"value": 1.04,               "proc" : ["TT"]},
    "QCDscale_ttjets"             : {"value": (0.996 , 1.035),    "proc" : ["TT"]},
    "TopmassUnc_ttjets"           : {"value": 1.03,               "proc" : ["TT"]},
    "pdf_DY"                      : {"value": 1.04,               "proc" : ["DY"]},
    "QCDscale_DY"                 : {"value": 1.01,               "proc" : ["DY"]},
    "pdf_HH"                      : {"value": 1.04,               "proc" : ["HH"]},
    "QCDscale_HH"                 : {"value": (0.95 , 1.022),     "proc" : ["HH"]},
    "TopmassUnc_HH"               : {"value": 1.026,              "proc" : ["HH"]},
    "QCDscale_WH"                 : {"value": (0.95 , 1.07),      "proc" : ["WH"]},
    "pdf_WH"                      : {"value": 1.019,              "proc" : ["WH"]},
    "QCDscale_ZH"                 : {"value": (0.962 , 1.031),    "proc" : ["ZH"]},
    "pdf_ZH"                      : {"value": 1.016,              "proc" : ["ZH"]},
    "pdf_qqH"                     : {"value": 1.021,              "proc" : ["qqH"]},
    "QCDscale_qqH"                : {"value": (0.96 , 1.03),      "proc" : ["ggH"]},
    "pdf_ggH"                     : {"value": 1.031,              "proc" : ["ggH"]},
    "QCDscale_ggH"                : {"value": (0.924 , 1.081),    "proc" : ["ggH"]}
    }

## --- BR(H->XX)/BR_sm(H->XX) = (kappa_X)^2 -------------------------------------------------------------- ##
## --- Rel. Unc. on BR(H->XX) = dBR(H->XX)/BR(H->XX) = 2 * d(kappa_X)/kappa_X ---------------------------- ##
## --- Measured kappa_X values used below taken from Run-1 coupling combination (HIG-15-002) ------------- ##
## --- Table-17 (B_bsm = 0 case, "ATLAS+CMS measured" column) in HIG-15-002-paper-v14.pdf ---------------- ##
## --- In cases where 1-sigma intervals are given, we take mid-point of the interval compatible with SM -- ##
## --- as the central value --- ##
higgsBR_exptl = {
    "hww" : 1.26, # kappa_W is 0.87 (+0.13) (-0.09) -> Expt. Unc. on H->WW BR: 2*sqrt(((0.149)^2 + (0.103)^2)/2) = 2*0.128 = 26%
    "hzz" : 1.18, # kappa_Z = 1.035 +0.095 -0.095 -> Expt. Unc. on H->ZZ BR: 2*sqrt(((0.091)^2 + (0.091)^2)/2) =  2*0.091 = 18%
    "htt" : 1.31, # kappa_tau = 0.84 (+0.15)(-0.11) -> Expt. Unc. on H->tautau BR: 2*sqrt(((0.178)^2 + (0.131)^2)/2) = 2*0.156 = 31%
    "hzg" : 1.0,  # Not observed yet but upper bounds available
    "hmm" : 1.0,  # Not observed yet but upper bounds available
    "hbb" : 1.89, # kappa_b = 0.49 (+0.27)(-0.15) -> Expt. Unc. on H->bb BR: 2*sqrt(((0.550)^2 + (0.306)^2)/2) = 2*0.445 = 89%
    "tttt" : 1.0330,
    "zzzz" : 1.0308,
    "wwww" : 1.0308,
    "wwzz" : 1.0308,
    "ttzz" : 1.0319,
    "ttww" : 1.0319
}

## --- Values taken from LHCHXWG TWiki: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR
higgsBR_theo = {
    "hww" : 1.0154,
    "hzz" : 1.0154,
    "htt" : 1.0165,
    "hzg" : 1.0582,
    "hmm" : 1.0168,
    "hbb" : 1.0126,
    "tttt" : 1.0330,
    "zzzz" : 1.0308,
    "wwww" : 1.0308,
    "wwzz" : 1.0308,
    "ttzz" : 1.0319,
    "ttww" : 1.0319
}

# Common fakes syst - taken uncorrelated/correlated between all years according with the name of the list
fake_shape_systs_uncorrelated = [
    "CMS_ttHl_Clos_e_shape",
    "CMS_ttHl_Clos_m_shape",
    "CMS_ttHl_Clos_t_shape",
    "CMS_ttHl_Clos_e_norm",
    "CMS_ttHl_Clos_m_norm",
    "CMS_ttHl_Clos_t_norm",
]
MC_shape_systs_uncorrelated = [
    "CMS_ttHl_trigger",
    "CMS_ttHl_l1PreFire", #-- should be 2016/2017 not 2018
]
btag_type_systs_uncorrelated = [
    "HFStats1",
    "HFStats2",
    "LFStats1",
    "LFStats2",
]
for btag_type_syst in btag_type_systs_uncorrelated :
    MC_shape_systs_uncorrelated += ["CMS_ttHl_btag_%s" % btag_type_syst]

# Common MC syst - taken uncorrelated/correlated between all years according with the name of the list
MC_shape_systs_correlated = [
    #"CMS_ttHl_JES",   # renamed to "CMS_scale_j"
    "CMS_ttHl_JER",
    "CMS_ttHl_UnclusteredEn",
    "CMS_ttHl_pileup",
    #### JEC_regrouped
    "CMS_ttHl_JESAbsolute",
    "CMS_ttHl_JESBBEC1",
    "CMS_ttHl_JESEC2",
    "CMS_ttHl_JESFlavorQCD",
    "CMS_ttHl_JESHF",
    "CMS_ttHl_JESRelativeBal",
    ### doing uncorrelated on the Writedatacards explicitelly, as other naming convention should be changed before it is easier to add it here
]
btag_type_systs_correlated = [
    "HF",
    "LF",
    "cErr1",
    "cErr2"
]
for btag_type_syst in btag_type_systs_correlated :
    MC_shape_systs_correlated += ["CMS_ttHl_btag_%s" % btag_type_syst]

JES_shape_systs_Uncorrelated = [
    "CMS_ttHl_JESAbsolute_Era",
    "CMS_ttHl_JESBBEC1_Era",
    "CMS_ttHl_JESEC2_Era",
    "CMS_ttHl_JESRelativeSample_Era",
    "CMS_ttHl_JESHF_Era"
]
################################################
# syst specific to processes

def specific_syst(analysis, list_channel_opt) :
    # channel specific shape syst
    HH_proc = ["HH_tttt",  "HH_zzzz",  "HH_wwww",  "HH_ttzz",  "HH_ttww",  "HH_zzww", "HH_bbtt", "HH_bbww", "HH_bbzz" , "HH"]
    ttH_proc = ["ttH_htt", "ttH_hww", "ttH_hzz", "ttH_hzg", "ttH_hzz"]
    tHq_proc = ["tHq_htt", "tHq_hww", "tHq_hzz"]
    tHW_proc = ["tHW_htt", "tHW_hww", "tHW_hzz"]
    if analysis == "ttH" :
        # the "correlated" on the dictionary means correlated between years
        # "MCproc" means that will take all the MC processes that appear for the channel that the datacard is being made for
        specific_ln_systs = {
            #"pdf_qg"                    : {"value" : 1.3,  "correlated"   : True,  "proc" : ["fakes_data"],          "channels" : [k for k,v in list_channel_opt.items() if "fakes_data"  in v["bkg_proc_from_data"]]},
            "CMS_ttHl_fakes"            : {"value" : 1.3,  "correlated"   : True,  "proc" : ["fakes_data"],          "channels" : [k for k,v in list_channel_opt.items() if "fakes_data"  in v["bkg_proc_from_data"]]},  # for channels with "fakes_data"
            "CMS_ttHl_QF"               : {"value" : 1.3,  "correlated"   : True,  "proc" : ["flips_data"],          "channels" : [k for k,v in list_channel_opt.items() if "flips_data"  in v["bkg_proc_from_data"]]},  # for channels with "flips_data"
            "CMS_ttHl_Convs"            : {"value" : 1.5,  "correlated"   : True,  "proc" : ["conversions"],         "channels" : [k for k,v in list_channel_opt.items() if "conversions" in v["bkg_procs_from_MC"]]},   # for channels with "conversions"
            #"CMS_ttHl_EWK"              : {"value" : 1.5,  "correlated"   : True,  "proc" : ["EWK"],                 "channels" : [k for k,v in list_channel_opt.items() if "EWK" in v["bkg_procs_from_MC"]]},           # for channels with "EWK"
            "CMS_ttHl_WZ_lnU"           : {"value" : 1.3,  "correlated"   : True,  "proc" : ["WZ"],                  "channels" : [k for k,v in list_channel_opt.items() if "WZ" in v["bkg_procs_from_MC"]]},            # for channels with WZ
            "CMS_ttHl_ZZ_lnU"           : {"value" : 3.0,  "correlated"   : True,  "proc" : ["ZZ"],                  "channels" : [k for k,v in list_channel_opt.items() if "ZZ" in v["bkg_procs_from_MC"]]},            # for channels with WZ
            "CMS_ttHl_Rares"            : {"value" : 1.5,  "correlated"   : True,  "proc" : ["Rares"],               "channels" : [k for k,v in list_channel_opt.items() if "Rares" in v["bkg_procs_from_MC"]]},         # for channels with "Rares"
            "CMS_ttHl_trigger_uncorr"   : {"value" : 1.02, "correlated"   : False, "proc" : ["TTW", "TTZ", "Rares"], "channels" : ["2l_2tau", "2los_1tau", "2lss_1tau"]},                                                # for 2l_2tau / 2los_1tau / 2lss_1tau  --- check!
            #"CMS_ttHl_trigger"          : {"value" : 1.05, "correlated"   : False, "proc" : "MCproc",                "channels" : ["3l_1tau"]},                                                                          # for 3l_1tau
            "CMS_ttHl_EWK_4j"           : {"value" : 1.3,  "correlated"   : False, "proc" : ["EWK"],                 "channels" : [k for k,v in list_channel_opt.items() if "EWK" in v["bkg_procs_from_MC"]]},           # for channels with EWK
            "CMS_eff_t"                 : {"value" : 1.1,  "correlated"   : True,  "proc" : "MCproc",                "channels" : [n for n in list(list_channel_opt.keys()) if  "2tau" in n ]},
            "CMS_eff_t"                 : {"value" : 1.05, "correlated"   : True,  "proc" : "MCproc",                "channels" : [n for n in list(list_channel_opt.keys()) if  "1tau" in n and n not in ["2lss_1tau", "3l_1tau"] ]},
        }

        specific_shape = {
            "CMS_ttHl_lepEff_elloose"       : {"correlated" : True,  "proc" : "MCproc", "channels" : list(set(list(list_channel_opt.keys())) - set(["0l_2tau", "1l_1tau"]))},  # not for "2los_1tau", "0l_2tau", "1l_1tau"
            "CMS_ttHl_lepEff_eltight"       : {"correlated" : True,  "proc" : "MCproc", "channels" : list(set(list(list_channel_opt.keys())) - set([ "0l_2tau", "1l_1tau"]))},  # not for "2los_1tau", "0l_2tau", "1l_1tau"
            "CMS_ttHl_lepEff_mutight"       : {"correlated" : True,  "proc" : "MCproc", "channels" : list(set(list(list_channel_opt.keys())) - set(["0l_2tau", "1l_1tau"]))},  # not for "2los_1tau", "0l_2tau", "1l_1tau"
            "CMS_ttHl_lepEff_muloose"       : {"correlated" : True,  "proc" : "MCproc", "channels" : list(set(list(list_channel_opt.keys())) - set(["0l_2tau", "1l_1tau"]))},  # not for "2los_1tau", "0l_2tau", "1l_1tau"
            ##############################
            "CMS_ttHl_tauIDSF"              : {"correlated" : False, "proc" : "MCproc", "channels" : [n for n in list(list_channel_opt.keys()) if  "2tau" in n or "1tau" in n ]},
            "CMS_ttHl_tauES"                : {"correlated" : False, "proc" : "MCproc", "channels" : [k for k,v in list_channel_opt.items() if ("2tau" in k or "1tau" in k) and not v["isSMCSplit"] ]}, # renamed to "CMS_scale_t"
            ########################### addSyst...
            "CMS_ttHl_FRe_shape_pt"         : {"correlated" : True, "proc" : ["data_fakes", "fakes_mc"], "channels" : [n for n in list(list_channel_opt.keys()) if "4l" in n or "3l" in n or "2l" in n or "1l" in n ]},
            "CMS_ttHl_FRe_shape_norm"       : {"correlated" : True, "proc" : ["data_fakes", "fakes_mc"], "channels" : [n for n in list(list_channel_opt.keys()) if "4l" in n or "3l" in n or "2l" in n or "1l" in n ]},
            "CMS_ttHl_FRe_shape_eta_barrel" : {"correlated" : True, "proc" : ["data_fakes", "fakes_mc"], "channels" : [n for n in list(list_channel_opt.keys()) if "4l" in n or "3l" in n or "2l" in n or "1l" in n ]},
            "CMS_ttHl_FRm_shape_pt"         : {"correlated" : True, "proc" : ["data_fakes", "fakes_mc"], "channels" : [n for n in list(list_channel_opt.keys()) if "4l" in n or "3l" in n or "2l" in n or "1l" in n ]},
            "CMS_ttHl_FRm_shape_norm"       : {"correlated" : True, "proc" : ["data_fakes", "fakes_mc"], "channels" : [n for n in list(list_channel_opt.keys()) if "4l" in n or "3l" in n or "2l" in n or "1l" in n ]},
            "CMS_ttHl_FRm_shape_eta_barrel" : {"correlated" : True, "proc" : ["data_fakes", "fakes_mc"], "channels" : [n for n in list(list_channel_opt.keys()) if "4l" in n or "3l" in n or "2l" in n or "1l" in n ]},
            "CMS_ttHl_FRjt_norm"            : {"correlated" : True, "proc" : ["data_fakes", "fakes_mc"], "channels" : [k for k,v in list_channel_opt.items() if  ("2tau" in k or "1tau" in k) and not v["isSMCSplit"] and not ("0l_2tau" in k or "1l_1tau" in k)]},## not isMCsplit ## FIXME: check and not ("0l_2tau" in k or "1l_1tau" in k)
            "CMS_ttHl_FRjt_shape"           : {"correlated" : True, "proc" : ["data_fakes", "fakes_mc"], "channels" : [k for k,v in list_channel_opt.items() if  ("2tau" in k or "1tau" in k) and not v["isSMCSplit"] and not ("0l_2tau" in k or "1l_1tau" in k)]},## not isMCsplit
            "CMS_ttHl_FRet_shift"           : {"correlated" : True, "proc" : ["data_fakes", "fakes_mc"], "channels" : [k for k,v in list_channel_opt.items() if  ("2tau" in k or "1tau" in k) and not v["isSMCSplit"] and not ("0l_2tau" in k or "1l_1tau" in k) ]},## not isMCsplit
            # FIXME: should be: (?)
            # CMS_ttHl_FRe_be                  shape                   -                     -                     -                     $
            # CMS_ttHl_FRe_norm                shape                   -                     -                     -                     $
            # CMS_ttHl_FRe_pt
            #################
            #"CMS_ttHl_DYMCReweighting"      : {"correlated" : True, "proc" : ["data_fakes", "fakes_mc"], "channels" : ["0l_2tau", "1l_1tau"]}, # only LO DY which we don't us
            "CMS_ttHl_DYMCNormScaleFactors" : {"correlated" : False, "proc" : ["DY"], "channels" : ["0l_2tau", "1l_1tau"]},
            "CMS_ttHl_topPtReweighting"     : {"correlated" : False, "proc" : ["TT"], "channels" : ["0l_2tau", "1l_1tau"]},
            ######## theory
            "CMS_ttHl_thu_shape_ttH"     : {"correlated" : True, "proc" : ttH_proc, "channels" : [k for k,v in list_channel_opt.items() if any(i in v["bkg_procs_from_MC"] for i in ttH_proc)]},
            "CMS_ttHl_thu_shape_tHq"     : {"correlated" : True, "proc" : tHq_proc, "channels" : [k for k,v in list_channel_opt.items() if any(i in v["bkg_procs_from_MC"] for i in tHq_proc)]},
            "CMS_ttHl_thu_shape_tHW"     : {"correlated" : True, "proc" : tHW_proc, "channels" : [k for k,v in list_channel_opt.items() if any(i in v["bkg_procs_from_MC"] for i in tHW_proc)]},
            "CMS_ttHl_thu_shape_ttW"     : {"correlated" : True, "proc" : ["TTW", "TTWW"], "channels" : [k for k,v in list_channel_opt.items() if "TTW" in v["bkg_procs_from_MC"]]},
            "CMS_ttHl_thu_shape_ttZ"     : {"correlated" : True, "proc" : ["TTZ"], "channels" : [k for k,v in list_channel_opt.items() if "TTZ" in v["bkg_procs_from_MC"]]},
            "CMS_ttHl_thu_shape_HH"      : {"correlated" : True, "proc" : HH_proc, "channels" : [k for k,v in list_channel_opt.items()  if any(i in v["bkg_procs_from_MC"] for i in HH_proc)]},
            "CMS_ttHl_thu_shape_DY"      : {"correlated" : True, "proc" : ["DY"], "channels" : [k for k,v in list_channel_opt.items() if "DY" in v["bkg_procs_from_MC"]]},
            "CMS_ttHl_thu_shape_TT"      : {"correlated" : True, "proc" : ["TT"], "channels" : [k for k,v in list_channel_opt.items() if "TT" in v["bkg_procs_from_MC"]]},
            "CMS_ttHl_thu_shape_WZ"      : {"correlated" : True, "proc" : ["WZ"], "channels" : [k for k,v in list_channel_opt.items() if "WZ" in v["bkg_procs_from_MC"]]},
            "CMS_ttHl_thu_shape_ZZ"      : {"correlated" : True, "proc" : ["ZZ"], "channels" : [k for k,v in list_channel_opt.items() if "ZZ" in v["bkg_procs_from_MC"]]},
        }

        # shape for isMCsplit -- it will be added to the list of signals + "bkg_procs_from_MC" (excluding "conversions")
        specific_ln_shape_systs = {
            "CMS_eff_t"             : {"value" : 1.05, "correlated" : True,  "type" : "gentau" , "channels" : [k for k,v in list_channel_opt.items() if v["isSMCSplit"]]},  # only for gentau
            "CMS_ttHl_FRjtMC_shape" : {"value" : 1.3,  "correlated" : True,  "type" : "faketau", "channels" : [k for k,v in list_channel_opt.items() if v["isSMCSplit"]]},  # only for fake tau
        }

        specific_shape_shape_systs = {
            "CMS_ttHl_FRjt_norm"  : {"correlated" : True, "type" : "faketau"},  ## only for faketau
            "CMS_ttHl_FRjt_shape" : {"correlated" : True, "type" : "faketau"},  ## only for faketau
        }

        created_shape_to_shape_syst = {
        "CMS_constructed_ttHl_FRjt_norm",
        "CMS_constructed_ttHl_FRjt_shape"
        }

    else : sys.exit("analysis " + analysis + " not implemented")
    return {
        "specific_ln_systs"             : specific_ln_systs,
        "specific_shape"                : specific_shape,
        "specific_ln_to_shape_systs"    : specific_ln_shape_systs,
        "specific_shape_to_shape_systs" : specific_shape_shape_systs,
        "created_shape_to_shape_syst"   : created_shape_to_shape_syst
    }
