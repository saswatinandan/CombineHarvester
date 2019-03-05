import os, subprocess, sys

#...... please comment out according to your needs ........

#add_shape_sys = "false"
add_shape_sys = "true"

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
  "dihiggsVisMass",
#  "HT",
#  "STMET",
#  "diHiggsMass"
}

masses = {"400", "700"};

parent_spins = {"radion"}
# parent_spins = {"radion", "graviton"} ## We don't have graviton samples yet

workingDir = os.getcwd()
#..... If you don't have files in datacards ......
#datacardDir = "/home/ram/hhAnalysis/2017/2018Sep6/datacards/hh_2l_2tau/"
datacardDir = "/home/ssawant/hhAnalysis/2017/20181005/datacards/hh_3l/"
datacardFiles = {
#  "hh_2l_2tau"   : "prepareDatacards_hh_2l_2tau_mTauTauVis.root",     ## Corrupted file !!! 
#  "hh_2l_2tau"   : "prepareDatacards_hh_2l_2tau_dihiggsVisMass.root",
#  "hh_2l_2tau"   : "prepareDatacards_hh_2l_2tau_HT.root",
#  "hh_2l_2tau"   : "prepareDatacards_hh_2l_2tau_STMET.root",
#  "hh_2l_2tau"   : "prepareDatacards_hh_2l_2tau_dihiggsMass.root",
#   "hh_3l"        : "prepareDatacards_hh_3l_dihiggsMass.root",
#   "hh_3l"        : "prepareDatacards_hh_3l_dihiggsMass_v1.root",
  "hh_3l"        : "prepareDatacards_hh_3l_dihiggsVisMass_Geq1Jets.root",
#   "hh_3l"        : "prepareDatacards_hh_3l_dihiggsVisMass_Only1Jets.root",
#   "hh_3l"        : "prepareDatacards_hh_3l_dihiggsVisMass_Geq2Jets.root",   
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
        txtFile  = os.path.join(datacardDir_output, "%s/%s/%s_%s.txt" %(spin, mass, channel, shapeVariable))
        logFile  = os.path.join(datacardDir_output, "%s/%s/%s_%s_limits.log" %(spin, mass, channel, shapeVariable))
        logFile1 = os.path.join(datacardDir_output, "%s/%s/%s_%s_ML.log" %(spin, mass, channel, shapeVariable))
        run_cmd('rm %s*' % datacardFilename_output)
        run_cmd('%s --input_file=%s --output_file=%s --add_shape_sys=%s --rebinned_hist=%s --mass=%s --type=%s' % (WriteDatacard_executable, datacardFile_input, datacardFilename_output, add_shape_sys, rebinned_hist, mass, spin))
        print('txtFile %s' % txtFile) 
        print('logFile %s' % logFile) 
        print('logFile1 %s' % logFile1) 
        run_cmd('rm %s' % logFile)
        run_cmd('rm %s' % logFile1)
        if run_on_asimov:
          run_cmd('combine -M AsymptoticLimits -t -1 -m %s %s &> %s' % (mass, txtFile, logFile))
          run_cmd('combine -M MaxLikelihoodFit -t -1 -m %s %s &> %s' % (mass, txtFile, logFile1))
        else:
          run_cmd('combine -M AsymptoticLimits -m %s -d %s &> %s' % (mass, txtFile, logFile))
          run_cmd('combine -M MaxLikelihoodFit -m %s %s &> %s' % (mass, txtFile, logFile1)) 
          
          #        rootFile =datacardFile_output.replace(".root", "_shapes.root")    
          #        run_cmd('rm %s' % rootFile)
          #        run_cmd('PostFitShapes -d %s -o %s -m 125 -f fitDiagnostics.root:fit_s --postfit --sampling --print' % (txtFile, rootFile))
          #        makePostFitPlots_macro = os.path.join(workingDir, "macros", "makePostFitPlots_%s_%s.C" %(channel,shapeVariable))
          #        run_cmd('root -b -n -q -l %s++' % makePostFitPlots_macro)

