#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "boost/program_options.hpp"
#include <TString.h>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;

int main(int argc, char** argv) {

  std::string input_file, output_file;
  double lumi = -1.;
  std::string type = "radion";
  double mass = 400.;
  bool add_shape_sys = true;
  bool rebinned_hist = false;
  bool float_sig = false;
  po::variables_map vm;
  po::options_description config("configuration");
  config.add_options()
    ("input_file,i", po::value<string>(&input_file)->default_value("Tallinn/ttH_3l_2016Jul16_Tight.input.root"))
    ("output_file,o", po::value<string>(&output_file)->default_value("hh_3l.root"))
    ("lumi,l", po::value<double>(&lumi)->default_value(lumi))
    ("add_shape_sys,s", po::value<bool>(&add_shape_sys)->default_value(true))
    ("rebinned_hist,r", po::value<bool>(&rebinned_hist)->default_value(false))
    ("float_sig,f", po::value<bool>(&float_sig)->default_value(false))
    ("type,t", po::value<string>(&type)->default_value(type))
    ("mass,m", po::value<double>(&mass)->default_value(mass));
  po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
  po::notify(vm);

  //! [part1]
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  //string aux_shapes = "/home/ram/hhAnalysis/2017/2018Sep6/datacards/hh_2l_2tau/";
  //string aux_shapes = "/home/ssawant/hhAnalysis/2017/20181005/datacards/hh_3l/";
  string aux_shapes = "/home/ssawant/hhAnalysis/2017/20181127/datacards/hh_3l/";
  if ( input_file.find_first_of("/") == 0 ) aux_shapes = ""; // set aux_shapes directory to zero in case full path to input file is given on command line

  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  // --------- MY LINES ---------
  ch::Categories cats = {
      {1, "hh_3l"}
    };
  // ch::Categories is just a typedef of vector<pair<int, string>>
  //! [part1]

  //! [part2]
  vector<string> masses = {"*"};
  //! [part2]

  //! [part3]
  cb.AddObservations(masses, {"*"}, {"13TeV"}, {"*"}, cats);
  //! [part3]


  //! [part4]
  // ---- all backgrounds
  std::string proc_fakes = "fakes_data";
  //vector<string> bkg_procs = {"TT", "TTW", "TTWW", "TTZ", "TTH", "TH", "WW", "WZ", "ZZ", "DY", "W", "VH", "Other", "conversions", "flips_data", proc_fakes};
  vector<string> bkg_procs = {"TT", "TTW", "TTWW", "TTZ", "TTH", "TH", "WW", "WZ", "ZZ", "DY", "W", "VH", "Other", "conversions", proc_fakes};
  cb.AddProcesses(masses, {"*"}, {"13TeV"}, {"*"}, {proc_fakes}, cats, false);


  // ---- all mc driven backgrounds
  vector<string> bkg_procs_MConly = {"TT", "TTW", "TTWW", "TTZ", "TTH", "TH", "WW", "WZ", "ZZ", "DY", "W", "VH", "Other", "conversions"};
  cb.AddProcesses(masses, {"*"}, {"13TeV"}, {"*"}, bkg_procs_MConly, cats, false);
 
  // ---- all signals
  vector<string> sig_procs;
  if(type == "radion"){
    if(mass == 400){
      sig_procs = {"signal_ggf_spin0_400_hh_tttt", "signal_ggf_spin0_400_hh_wwtt", "signal_ggf_spin0_400_hh_wwww"};
    }else if(mass == 700){
      sig_procs = {"signal_ggf_spin0_700_hh_tttt", "signal_ggf_spin0_700_hh_wwtt", "signal_ggf_spin0_700_hh_wwww"};
    }
  }
  cb.AddProcesses(masses, {"*"}, {"13TeV"}, {"*"}, sig_procs, cats, true);
  //! [part4]


  //Some of the code for this is in a nested namespace, so
  // we'll make some using declarations first to simplify things a bit.
  using ch::syst::SystMap;
  using ch::syst::SystMapAsymm;
  using ch::syst::SystMapFunc;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;

  //! [part5]
  cb.cp().process(sig_procs).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.023));

  // ---- No Theory (scale, pdf, alphaS) uncertainties to be applied to the HH signal 
  // if(type == "radion"){
  //   if(mass == 400){cb.cp().process(sig_procs).AddSyst(cb, "pdf_alphaS_HH", "lnN", SystMap<>::init(1.047));}
  //   if(mass == 700){cb.cp().process(sig_procs).AddSyst(cb, "pdf_alphaS_HH", "lnN", SystMap<>::init(1.063));}
  // }


  cb.cp().process(bkg_procs_MConly).AddSyst(cb, "lumi_13TeV", "lnN", SystMap<>::init(1.023));
  cb.cp().process({"TT"}).AddSyst(cb, "pdf_Higgs_tt", "lnN", SystMap<>::init(1.036));
  cb.cp().process({"TT"}).AddSyst(cb, "QCDscale_tt", "lnN", SystMapAsymm<>::init(0.915, 1.058));
  cb.cp().process({"TTW"}).AddSyst(cb, "pdf_Higgs_ttW", "lnN", SystMap<>::init(1.036));
  cb.cp().process({"TTW"}).AddSyst(cb, "QCDscale_ttW", "lnN", SystMapAsymm<>::init(0.915, 1.058));
  cb.cp().process({"TTWW"}).AddSyst(cb, "pdf_Higgs_ttWW", "lnN", SystMap<>::init(1.036)); // need modification
  cb.cp().process({"TTWW"}).AddSyst(cb, "QCDscale_ttWW", "lnN", SystMapAsymm<>::init(0.915, 1.058));// need modification 
  cb.cp().process({"TTZ"}).AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(0.966));
  cb.cp().process({"TTZ"}).AddSyst(cb, "QCDscale_ttZ", "lnN", SystMapAsymm<>::init(0.904, 1.112));
  cb.cp().process({"TTH"}).AddSyst(cb, "pdf_Higgs_ttH", "lnN", SystMap<>::init(1.036));
  cb.cp().process({"TTH"}).AddSyst(cb, "QCDscale_ttH", "lnN", SystMapAsymm<>::init(0.915, 1.058));
  cb.cp().process({"TH"}).AddSyst(cb, "Unc_TH", "lnN", SystMap<>::init(1.100)); // need modification 
  cb.cp().process({"WW"}).AddSyst(cb, "Unc_WW", "lnN", SystMap<>::init(1.100)); // need modification 
  cb.cp().process({"WZ"}).AddSyst(cb, "Unc_WZ", "lnN", SystMap<>::init(1.100)); // need modification 
  cb.cp().process({"ZZ"}).AddSyst(cb, "Unc_ZZ", "lnN", SystMap<>::init(1.100)); // taken from AN2017_020_v8.pdf: page 79 (consider only gg->ZZ igonring qq->ZZ contribution)
  cb.cp().process({"DY"}).AddSyst(cb, "Unc_DY", "lnN", SystMap<>::init(1.100)); // need modification 
  cb.cp().process({"W"}).AddSyst(cb, "Unc_W", "lnN", SystMap<>::init(1.100)); // need modification 
  // Lines below derived (for mH = 125.00 GeV) from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV
  cb.cp().process({"VH"}).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.018)); 
  cb.cp().process({"VH"}).AddSyst(cb, "QCDscale_VH", "lnN", SystMapAsymm<>::init(0.983, 1.018));
  cb.cp().process({"Other"}).AddSyst(cb, "Unc_Other", "lnN", SystMap<>::init(1.100)); // need modification 
  cb.cp().process({"conversions"}).AddSyst(cb, "Unc_conversions", "lnN", SystMap<>::init(1.500)); // need modification 
  cb.cp().process({"flips_data"}).AddSyst(cb, "Unc_flips_data", "lnN", SystMap<>::init(1.500)); // need modification 
  cb.cp().process({proc_fakes}).AddSyst(cb, "CMS_HHl17_fakes", "lnN", SystMap<>::init(1.5));        // same as CMS_ttHl17_fakes
  cb.cp().process({proc_fakes}).AddSyst(cb, "CMS_HHl17_Clos_e_norm", "lnN", SystMap<>::init(0.95)); // same as CMS_ttHl17_Clos_e_norm
  cb.cp().process({proc_fakes}).AddSyst(cb, "CMS_HHl17_Clos_m_norm", "lnN", SystMap<>::init(1.1));  // same as CMS_ttHl17_Clos_m_norm

  cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly})).AddSyst(cb, "CMS_HHl_trigger_uncorr", "lnN", SystMap<>::init(1.03)); // same as CMS_ttHl_trigger_uncorr (was absent in ttH due to bottom line) 
  cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly})).AddSyst(cb, "CMS_HHl_lepEff_elloose", "lnN", SystMap<>::init(1.04)); // same as CMS_ttHl_lepEff_elloose
  cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly})).AddSyst(cb, "CMS_HHl_lepEff_muloose", "lnN", SystMap<>::init(1.03)); // same as CMS_ttHl_lepEff_muloose
  cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly})).AddSyst(cb, "CMS_HHl_lepEff_tight", "lnN", SystMap<>::init(1.09));   // same as CMS_ttHl_lepEff_tight
  cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly})).AddSyst(cb, "CMS_HHl17_tauID", "lnN", SystMap<>::init(1.1));         // same as CMS_ttHl17_tauID

  cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly})).AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02)); // not used in ttH anymore





  //! [part5]

  //! [part6]
  // ----- Tail-Fit Systematics --- 
  if(add_shape_sys){
    // cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly})).AddSyst(cb, "CMS_ttHl_trigger", "shape", SystMap<>::init(1.0)); // not yet present in files so using the line above
    //cb.cp().process({proc_fakes}).AddSyst(cb, "EigenVec_1", "shape", SystMap<>::init(1.0));
    //cb.cp().process({proc_fakes}).AddSyst(cb, "EigenVec_2", "shape", SystMap<>::init(1.0));
    //cb.cp().process({proc_fakes}).AddSyst(cb, "FitSyst", "shape", SystMap<>::init(1.0));
    // cb.cp().process({proc_fakes}).AddSyst(cb, "CMS_ttHl_thu_shape_ttZ_x1", "shape", SystMap<>::init(1.0)); // not present in the files
    // cb.cp().process({proc_fakes}).AddSyst(cb, "CMS_ttHl_thu_shape_ttZ_y1", "shape", SystMap<>::init(1.0)); // not present in the files
    // cb.cp().process({"TTZ"}).AddSyst(cb, "CMS_HHl_thu_shape_ttZ_x1", "shape", SystMap<>::init(1.0)); // not present in the files
    // cb.cp().process({"TTZ"}).AddSyst(cb, "CMS_HHl_thu_shape_ttZ_y1", "shape", SystMap<>::init(1.0)); // not present in the files
    
    
    
    
    cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly}))
      .AddSyst(cb, "CMS_ttHl_JES", "shape", SystMap<>::init(1.0));
    
    cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly}))
      .AddSyst(cb, "CMS_ttHl_JER", "shape", SystMap<>::init(1.0));
    
    
    cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly}))
      .AddSyst(cb, "CMS_ttHl_tauES", "shape", SystMap<>::init(1.0));
    
    cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly}))
      .AddSyst(cb, "CMS_ttHl_UnclusteredEn", "shape", SystMap<>::init(1.0));
    
    // btag shapes
    for ( auto s : {"HF", "HFStats1", "HFStats2", "LF", "LFStats1", "LFStats2", "cErr1", "cErr2"} ) {
      cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly}))
	.AddSyst(cb, Form("CMS_ttHl_btag_%s", s), "shape", SystMap<>::init(1.0));
    }
    
    // -------
    cb.cp().process({"TTH"})
      .AddSyst(cb, "CMS_ttHl_thu_shape_ttH_x1", "shape", SystMap<>::init(1.0));
    cb.cp().process({"TTH"})
      .AddSyst(cb, "CMS_ttHl_thu_shape_ttH_y1", "shape", SystMap<>::init(1.0));
    
    cb.cp().process({"TTW"})
      .AddSyst(cb, "CMS_ttHl_thu_shape_ttW_x1", "shape", SystMap<>::init(1.0));
    cb.cp().process({"TTW"})
      .AddSyst(cb, "CMS_ttHl_thu_shape_ttW_y1", "shape", SystMap<>::init(1.0));
    
    cb.cp().process({"TTZ"})
      .AddSyst(cb, "CMS_ttHl_thu_shape_ttZ_x1", "shape", SystMap<>::init(1.0));
    cb.cp().process({"TTZ"})
      .AddSyst(cb, "CMS_ttHl_thu_shape_ttZ_y1", "shape", SystMap<>::init(1.0));
    
    cb.cp().process(sig_procs)
      .AddSyst(cb, "CMS_ttHl_thu_shape_HH_x1", "shape", SystMap<>::init(1.0));
    cb.cp().process(sig_procs)
      .AddSyst(cb, "CMS_ttHl_thu_shape_HH_y1", "shape", SystMap<>::init(1.0));
    
    // -------
    cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly}))
      .AddSyst(cb, "CMS_ttHl_trigger", "shape", SystMap<>::init(1.0));
    
    cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly}))
      .AddSyst(cb, "CMS_ttHl_pileup", "shape", SystMap<>::init(1.0));
    
    // DY ??
    cb.cp().process({"DY"})
      .AddSyst(cb, "CMS_ttHl_DYMCReweighting", "shape", SystMap<>::init(1.0));
    
    // CMS_ttHl_FRjt_norm to be used for bk only?
    cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly}))
      .AddSyst(cb, "CMS_ttHl_FRjt_norm", "shape", SystMap<>::init(1.0));
    
    // CMS_ttHl_FRjt_shape to be used for bk only?
    cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly}))
      .AddSyst(cb, "CMS_ttHl_FRjt_shape", "shape", SystMap<>::init(1.0));
    
    // ??
    cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly}))
      .AddSyst(cb, "CMS_ttHl_FRet_shift", "shape", SystMap<>::init(1.0));    
    
    cb.cp().process(ch::JoinStr({sig_procs, bkg_procs_MConly}))
      .AddSyst(cb, "CMS_ttHl_FRmt_shift", "shape", SystMap<>::init(1.0));
    
    // ??
    cb.cp().process({"fakes_data"})
      .AddSyst(cb, "CMS_ttHl_FRe_shape_pt", "shape", SystMap<>::init(1.0));
    
    cb.cp().process({"fakes_data"})
      .AddSyst(cb, "CMS_ttHl_FRe_shape_norm", "shape", SystMap<>::init(1.0));
    
    cb.cp().process({"fakes_data"})
      .AddSyst(cb, "CMS_ttHl_FRe_shape_eta_barrel", "shape", SystMap<>::init(1.0));
    
    cb.cp().process({"fakes_data"})
      .AddSyst(cb, "CMS_ttHl_FRm_shape_pt", "shape", SystMap<>::init(1.0));
    
    cb.cp().process({"fakes_data"})
      .AddSyst(cb, "CMS_ttHl_FRm_shape_norm", "shape", SystMap<>::init(1.0));
    
    cb.cp().process({"fakes_data"})
      .AddSyst(cb, "CMS_ttHl_FRm_shape_eta_barrel", "shape", SystMap<>::init(1.0));
       
    
  }
  //! [part6]

  
  //! [part7]
  if (rebinned_hist){
    cb.cp().backgrounds().ExtractShapes(
	aux_shapes + input_file.data(),
	"HH_2l_2tau/rebinned/$PROCESS",
	"HH_2l_2tau/rebinned/$PROCESS_$SYSTEMATIC");
    cb.cp().signals().ExtractShapes(
        aux_shapes + input_file.data(),
	"HH_2l_2tau/rebinned/$PROCESS",
	"HH_2l_2tau/rebinned/$PROCESS_$SYSTEMATIC");
  }else{
    cb.cp().backgrounds().ExtractShapes(
	aux_shapes + input_file.data(),
	"$PROCESS",
	"$PROCESS_$SYSTEMATIC");
    cb.cp().signals().ExtractShapes(
	aux_shapes + input_file.data(),
	"$PROCESS",
	"$PROCESS_$SYSTEMATIC");
  }
  //! [part7]
  

  //! [part8]
  cb.cp().SetAutoMCStats(cb, 10);
  //! [part8]

  //! [part9]
  // First we generate a set of bin names:
  set<string> bins = cb.bin_set();
  // This method will produce a set of unique bin names by considering all
  // Observation, Process and Systematic entries in the CombineHarvester
  // instance.

  // Finally we iterate through bins and write a
  // datacard.
  for (auto b : bins) {
    cout << ">> Writing datacard for bin: " << b
	 << "\n";
      // We need to filter on both the mass and the mass hypothesis,
      // where we must remember to include the "*" mass entry to get
      // all the data and backgrounds.
    //cb.cp().bin({b}).mass({"*"}).WriteDatacard(
    //	b + ".txt", output);
    // it does not work anymore with TString (after update Havester to use SetAutoMCStats)
    cb.cp().bin({b}).mass({"*"}).WriteDatacard(
      output_file + ".txt" , output_file + ".root");
  }
  //! [part9]

}
