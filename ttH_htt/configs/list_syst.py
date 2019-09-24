### everthing that is marked as "uncorrelated" is renamed as:
### "CMS_ttHl" ->  "CMS_ttHl%s" % str(era).replace("20","")
### where era = 2016/2017/2018

# syst: theory and from MC generators - taken correlated between all years (check if that is what we want to do)
lnSyst = {
    "lumi"            : {2016: 1.023,          2017: 1.023,          2018: 1.023},
    "pdf_Higgs_ttH"   : {2016: 1.036,          2017: 1.036,          2018: 1.036},
    "QCDscale_ttH"    : {2016: (0.907, 1.058), 2017: (0.907, 1.058), 2018: (0.907, 1.058)},
    "pdf_qg"          : {2016: 1.027,          2017: 1.027,          2018: 1.027},
    "QCDscale_tH"     : {2016: (0.939, 1.046), 2017: (0.939, 1.046), 2018: (0.939, 1.046)},
    "pdf_qqbar"       : {2016: 1.04,           2017: 1.04,           2018: 1.04},
    "QCDscale_ttW"    : {2016: (0.885, 1.129), 2017: (0.885, 1.129), 2018: (0.885, 1.129)},
    "pdf_TTWW"        : {2016: 1.03,           2017: 1.03,           2018: 1.03},
    "QCDscale_ttWW"   : {2016: (0.891, 1.081), 2017: (0.891, 1.081), 2018: (0.891, 1.081)},
    "pdf_gg"          : {2016: 0.966,          2017: 0.966,          2018: 0.966},
    "QCDscale_ttZ"    : {2016: (0.904, 1.112), 2017: (0.904, 1.112), 2018: (0.904, 1.112)},
    }

## --- BR(H->XX)/BR_sm(H->XX) = (kappa_X)^2 -------------------------------------------------------------- ##
## --- Rel. Unc. on BR(H->XX) = dBR(H->XX)/BR(H->XX) = 2 * d(kappa_X)/kappa_X ---------------------------- ##
## --- Measured kappa_X values used below taken from Run-1 coupling combination (HIG-15-002) ------------- ##
## --- Table-17 (B_bsm = 0 case, "ATLAS+CMS measured" column) in HIG-15-002-paper-v14.pdf ---------------- ##
## --- In cases where 1-sigma intervals are given, we take mid-point of the interval compatible with SM -- ##
## --- as the central value --- ##    
higgsBR = {
    "hww" : 1.26, # kappa_W is 0.87 (+0.13) (-0.09) -> Expt. Unc. on H->WW BR: 2*sqrt(((0.149)^2 + (0.103)^2)/2) = 2*0.128 = 26% 
    "hzz" : 1.18, # kappa_Z = 1.035 +0.095 -0.095 -> Expt. Unc. on H->ZZ BR: 2*sqrt(((0.091)^2 + (0.091)^2)/2) =  2*0.091 = 18%
    "htt" : 1.31, # kappa_tau = 0.84 (+0.15)(-0.11) -> Expt. Unc. on H->tautau BR: 2*sqrt(((0.178)^2 + (0.131)^2)/2) = 2*0.156 = 31%
    "hzg" : 1.0,  # Not observed yet but upper bounds available 
    "hmm" : 1.0,  # Not observed yet but upper bounds available 
    "hbb" : 1.89, # kappa_b = 0.49 (+0.27)(-0.15) -> Expt. Unc. on H->bb BR: 2*sqrt(((0.550)^2 + (0.306)^2)/2) = 2*0.445 = 89%
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
MC_shape_systs_uncorrelated = []
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
    "CMS_ttHl_JES",   # renamed to "CMS_scale_j"
    "CMS_ttHl_tauES", # renamed to "CMS_scale_t"
    "CMS_ttHl_JER",
    "CMS_ttHl_UnclusteredEn",
]
btag_type_systs_correlated = [
    "HF",
    "LF",
    "cErr1",
    "cErr2"
]
for btag_type_syst in btag_type_systs_correlated :
    MC_shape_systs_correlated += ["CMS_ttHl_btag_%s" % btag_type_syst]

################################################
# syst specific to processes

def specific_syst(analysis, list_channel_opt) :
    if analysis == "ttH" :
        # the "correlated" on the dictionary means correlated between years
        # "MCproc" means that will take all the MC processes that appear for the channel that the datacard is being made for
        specific_ln_systs = {
            "CMS_ttHl_fakes"            : {"value" : 1.3,  "correlated"   : True,  "proc" : ["fakes_data"],          "channels" : [k for k,v in list_channel_opt.items() if "fakes_data"  in v["bkg_proc_from_data"]]},  # for channels with "fakes_data"
            "CMS_ttHl_QF"               : {"value" : 1.3,  "correlated"   : True,  "proc" : ["flips_data"],          "channels" : [k for k,v in list_channel_opt.items() if "flips_data"  in v["bkg_proc_from_data"]]},  # for channels with "flips_data"
            "CMS_ttHl_Convs"            : {"value" : 1.5,  "correlated"   : True,  "proc" : ["conversions"],         "channels" : [k for k,v in list_channel_opt.items() if "conversions" in v["bkg_procs_from_MC"]]},   # for channels with "conversions"
            "CMS_ttHl_EWK"              : {"value" : 1.5,  "correlated"   : True,  "proc" : ["EWK"],                 "channels" : [k for k,v in list_channel_opt.items() if "EWK" in v["bkg_procs_from_MC"]]},           # for channels with "EWK"
            "CMS_ttHl_WZ_lnU"           : {"value" : 1.3,  "correlated"   : True,  "proc" : ["WZ"],                  "channels" : [k for k,v in list_channel_opt.items() if "WZ" in v["bkg_procs_from_MC"]]},            # for channels with WZ
            "CMS_ttHl_ZZ_lnU"           : {"value" : 3.0,  "correlated"   : True,  "proc" : ["WZ"],                  "channels" : [k for k,v in list_channel_opt.items() if "WZ" in v["bkg_procs_from_MC"]]},            # for channels with WZ
            "CMS_ttHl_Rares"            : {"value" : 1.5,  "correlated"   : True,  "proc" : ["Rares"],               "channels" : [k for k,v in list_channel_opt.items() if "Rares" in v["bkg_procs_from_MC"]]},         # for channels with "Rares"
            "CMS_ttHl_trigger_uncorr"   : {"value" : 1.02, "correlated"   : False, "proc" : ["TTW", "TTZ", "Rares"], "channels" : ["2l_2tau", "2los_1tau", "2lss_1tau"]},                                                # for 2l_2tau / 2los_1tau / 2lss_1tau  --- check!
            "CMS_ttHl_trigger"          : {"value" : 1.05, "correlated"   : False, "proc" : "MCproc",                "channels" : ["3l_1tau"]},                                                                          # for 3l_1tau
            "CMS_ttHl_EWK_4j"           : {"value" : 1.3,  "correlated"   : False, "proc" : ["EWK"],                 "channels" : [k for k,v in list_channel_opt.items() if "EWK" in v["bkg_procs_from_MC"]]},           # for channels with EWK
            "CMS_eff_t"                 : {"value" : 1.1,  "correlated"   : True,  "proc" : "MCproc",                "channels" : [n for n in list(list_channel_opt.keys()) if  "2tau" in n ]},
            "CMS_eff_t"                 : {"value" : 1.05, "correlated"   : True,  "proc" : "MCproc",                "channels" : [n for n in list(list_channel_opt.keys()) if  "1tau" in n and n not in ["2lss_1tau", "3l_1tau"] ]},
            "CMS_ttHl_lepEff_elloose"   : {"value" : 1.02, "correlated"   : True,  "proc" : "MCproc",                "channels" : list(set(list(list_channel_opt.keys())) - set(["2los_1tau", "0l_2tau", "1l_1tau"]))},  # not for "2los_1tau", "0l_2tau", "1l_1tau"
            "CMS_ttHl_lepEff_etight"    : {"value" : 1.05, "correlated"   : True,  "proc" : "MCproc",                "channels" : list(set(list(list_channel_opt.keys())) - set(["2los_1tau", "0l_2tau", "1l_1tau"]))},  # not for "2los_1tau", "0l_2tau", "1l_1tau"
            "CMS_ttHl_lepEff_mtight"    : {"value" : 1.05, "correlated"   : True,  "proc" : "MCproc",                "channels" : list(set(list(list_channel_opt.keys())) - set(["2los_1tau", "0l_2tau", "1l_1tau"]))},  # not for "2los_1tau", "0l_2tau", "1l_1tau"
        }

        # channel specific shape syst
        specific_shape = {
            "CMS_ttHl_trigger"        : {"correlated" : False, "proc" : "MCproc", "channels" : list(set(list(list_channel_opt.keys())) - set(["0l_2tau", "1l_2tau", "1l_1tau", "3l_1tau"]))},   # not for 1l_2tau / 2los_1tau / 3l_1tau
            "CMS_ttHl_trigger_leptau" : {"correlated" : False, "proc" : "MCproc", "channels" : ["1l_2tau", "1l_1tau"]},
            "CMS_ttHl_trigger_tau"    : {"correlated" : False, "proc" : "MCproc", "channels" : ["0l_2tau"]},
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
    else : sys.exit("analysis " + analysis + " not implemented")
    return {
        "specific_ln_systs"             : specific_ln_systs,
        "specific_shape"                : specific_shape,
        "specific_ln_to_shape_systs"    : specific_ln_shape_systs,
        "specific_shape_to_shape_systs" : specific_shape_shape_systs
    }

# proc by channels
