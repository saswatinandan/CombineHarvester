import os, subprocess, sys

#...... please comment out according to your needs ........

add_shape_sys = "false"
#add_shape_sys = "true"

rebinned_hist = "false"
#rebinned_hist = "true"

run_on_asimov = False
# run_on_asimov = True

channels = [
#  "hh_2l_2tau",
    "hh_3l", 
]
shapeVariables = {
#  "mTauTauVis",
#  "dihiggsVisMass",
#  "HT",
#  "STMET",
#  "diHiggsMass"
  "mvaOutput_xgb_SUMBk_HH"
}

masses = {"400", "700"};
#masses = {"400"};

mH = 125

parent_spins = {"radion"}
# parent_spins = {"radion", "graviton"} ## We don't have graviton samples yet

workingDir = os.getcwd()
#..... If you don't have files in datacards ......
#datacardDir = "/home/ram/hhAnalysis/2017/2018Sep6/datacards/hh_2l_2tau/"
#datacardDir = "/home/ssawant/hhAnalysis/2017/20181127/datacards/hh_3l/" # vDAE18 woSyst woAK
datacardDir = "/home/ssawant/hhAnalysis/2017/20190223_vDAE_wSyst_woAK8/datacards/hh_3l/"
#datacardDir = "/home/ssawant/hhAnalysis/2017/20181205/datacards/hh_3l/" # wSyst woAK8
#datacardDir = "/home/ssawant/hhAnalysis/2017/20190120/datacards/hh_3l/" # I guess ana wAK8
datacardFiles = {
#  "hh_2l_2tau"   : "prepareDatacards_hh_2l_2tau_mTauTauVis.root",     ## Corrupted file !!! 
#  "hh_2l_2tau"   : "prepareDatacards_hh_2l_2tau_dihiggsVisMass.root",
#  "hh_2l_2tau"   : "prepareDatacards_hh_2l_2tau_HT.root",
#  "hh_2l_2tau"   : "prepareDatacards_hh_2l_2tau_STMET.root",
#  "hh_2l_2tau"   : "prepareDatacards_hh_2l_2tau_dihiggsMass.root",
#   "hh_3l"        : "prepareDatacards_hh_3l_dihiggsMass.root",
#   "hh_3l"        : "prepareDatacards_hh_3l_dihiggsMass_v1.root",
#  "hh_3l"        : "prepareDatacards_hh_3l_dihiggsVisMass_Geq1Jets.root",
#   "hh_3l"        : "prepareDatacards_hh_3l_dihiggsVisMass_Only1Jets.root",
#   "hh_3l"        : "prepareDatacards_hh_3l_dihiggsVisMass_Geq2Jets.root",   
#   "hh_3l"        : "prepareDatacards_hh_3l_hh_3l_dihiggsVisMass.root",
#   "hh_3l"        : "prepareDatacards_hh_3l_hh_3l_mvaOutput_xgb_hh_3l_SUMBk_HH.root",
   "hh_3l"        : "prepareDatacards_hh_3l_hh_3l_mvaOutput_xgb_hh_3l_SUMBk_HH_10bins.root",
}
datacardDir_output = os.path.join(workingDir, "datacards")

def run_cmd(command):
  print "executing command = '%s'" % command
  p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  stdout, stderr = p.communicate()
  return stdout

run_cmd('rm -rf %s' %datacardDir_output)
for channel in channels:
  for shapeVariable in shapeVariables:
    for mass in masses:
      for spin in parent_spins:
        datacardFile_input = os.path.join(datacardDir, datacardFiles[channel])
      ## datacardFile_input = os.path.join(workingDir, "datacards", "prepareDatacards_%s_%s.root" % (channel, shapeVariable))
        run_cmd('mkdir -p %s' %datacardDir_output)
        run_cmd('mkdir -p %s/%s/%s' %(datacardDir_output, spin, mass))
        WriteDatacard_executable = os.path.join("WriteDatacards_%s" %channel)
        datacardFilename_output = os.path.join(datacardDir_output, "%s/%s/%s_%s" %(spin, mass, channel, shapeVariable))
        datacard    = os.path.join(datacardDir_output, "%s/%s/%s_%s.txt" %(spin, mass, channel, shapeVariable))
        logFile_dc  = os.path.join(datacardDir_output, "%s/%s/%s_%s_WriteDatacards.log" %(spin, mass, channel, shapeVariable))
        run_cmd('rm %s*' % datacardFilename_output)
        run_cmd('%s --input_file=%s --output_file=%s --add_shape_sys=%s --rebinned_hist=%s --mass=%s --type=%s &> %s' % (WriteDatacard_executable, datacardFile_input, datacardFilename_output, add_shape_sys, rebinned_hist, mass, spin, logFile_dc))
        
        
        logFile_lmt  = os.path.join(datacardDir_output, "%s/%s/%s_%s_limits.log" %(spin, mass, channel, shapeVariable))
        logFile_ml   = os.path.join(datacardDir_output, "%s/%s/%s_%s_ML.log" %(spin, mass, channel, shapeVariable))        
        logFile_ws   = os.path.join(datacardDir_output, "%s/%s/%s_%s_ws.log" %(spin, mass, channel, shapeVariable))
        logFile_psf  = os.path.join(datacardDir_output, "%s/%s/%s_%s_postfit.log" %(spin, mass, channel, shapeVariable))
        oFile_ws     = os.path.join(datacardDir_output, "%s/%s/%s_%s_ws.root" %(spin, mass, channel, shapeVariable))
        oFile_psfit  = os.path.join(datacardDir_output, "%s/%s/%s_%s_postfit.root" %(spin, mass, channel, shapeVariable))
        run_cmd('rm %s %s %s %s %s %s' % (logFile_lmt, logFile_ml, logFile_ws, logFile_psf, oFile_ws, oFile_psfit))
        run_cmd('rm fitDiagnostics.Test.root')

        if run_on_asimov:
          run_cmd('combine -M AsymptoticLimits -t -1 -m %s %s &> %s' % (mH, datacard, logFile_lmt))
          run_cmd('combine -M MaxLikelihoodFit -t -1 -m %s %s &> %s' % (mH, datacard, logFile_ml))
        else:
          #run_cmd('combine -M AsymptoticLimits -m %s -d %s &> %s' % (mass, datacard, logFile_lmt))
          #run_cmd('combine -M MaxLikelihoodFit -m %s %s &> %s' % (mass, datacard, logFile_ml)) 
                    
          run_cmd('text2workspace.py %s -o %s &> %s' % (datacard, oFile_ws, logFile_ws))
          run_cmd('combineTool.py -M AsymptoticLimits %s -m %s &> %s' % (oFile_ws, mH, logFile_lmt))
          run_cmd('combineTool.py -M MaxLikelihoodFit %s -m %s &> %s' % (oFile_ws, mH, logFile_ml))
          run_cmd('PostFitShapesFromWorkspace -d %s -w %s -o %s -m %s --sampling --print  -f fitDiagnostics.Test.root:fit_s --postfit &> %s' % (datacard, oFile_ws, oFile_psfit, mH, logFile_psf)) 

          
          #        rootFile =datacardFile_output.replace(".root", "_shapes.root")    
          #        run_cmd('rm %s' % rootFile)
          #        run_cmd('PostFitShapes -d %s -o %s -m 125 -f fitDiagnostics.root:fit_s --postfit --sampling --print' % (txtFile, rootFile))
          #        makePostFitPlots_macro = os.path.join(workingDir, "macros", "makePostFitPlots_%s_%s.C" %(channel,shapeVariable))
          #        run_cmd('root -b -n -q -l %s++' % makePostFitPlots_macro)

