#!/usr/bin/env python
import os, subprocess, sys
from array import array
from ROOT import *
from math import sqrt, sin, cos, tan, exp
import numpy as np
import glob
#from pathlib2 import Path
execfile("../python/data_manager.py")
from random import randint
import CombineHarvester.CombineTools.ch as ch
#####################################################################
## From where to take the cards:
# The bellow is going to construct the combo card from scratch given the path of the cards by channel (see mom_2017/mom_2016)
copy_cards =  False
combine_cards = False
# If you already have the combined card put the bellow true (see mom_result)
takeCombo = True
#####################################################################

#####################################################################
## How to do?
btag_correlated = True # if true it does not manipulate the cards
JES_correlated = True # if true it does not manipulate the cards
remove_Clos_t = False
blinded = False
blindedOutput = False ## do not draw the rate on the impacts plot
sendToCondor = True ### Impacts / GOF / likelihood scans for combo need it
#####################################################################

#####################################################################
## What to do:
doFits = True ## To do any of the rest you must have ran with this being True once
## but, once it is done one there is no need to loose time repeating it

#######################
## Each of the steps bellow take time, I suggest to do on one separated runs
# (like this they can be also done in parallel)
# 1)
doCategories = False # for mu's
doLimitsByCat = False

# 2)
# for combo is almost mandatory send to grid,
# if you run on lxplus combineTool is already set to send to Condor (see bellow 'How')
doImpactCombo = False
doImpact2017 = False
# If you will run in Condor this must be done in two steps:
#  -  the first with impactsSubmit= True ---> wait for the jobs to be ready
#      - To see that is all done: check that you have the same number of root files than the number of nuissances to be considered
#  - after the jobs are done run again with impactsSubmit = False to wrap up the plot
impactsSubmit = False

# 3) -- optional
# fast version of the impacts -- Hessian approximation for quick checks
doHessImpactCombo = False
doHessImpact2017 = False

# 4)
# the bellow take lots of time, better to do on one run
# It is almost mandatory send to grid,
# if you run on lxplus combineTool is already set to send to Condor (see bellow 'How')
doGOFCombo = False
doGOF2017 = False
# If you will run in Condor this must be done in two steps:
#  -  the first with GOF_submit = True ---> wait for the jobs to be ready
#     -- each job will contain 2 toys
#        (if needed run the submission bash script created again up to you be happy with the number of toys)
#  - after the jobs are done run again with GOF_submit = False  to wrap up the plot
GOF_submit = False

# 5)
# OR you do from Combine or from from Havester
preparePostFitCombine = False
preparePostFitHavester = False

doYieldsAndPlots = False # will do the prefit and postfit table of yields.
# If any of the bellow are true it also do prefit and postfit plots
# You must have ran the respective preparePostFit... before (or put as true as well)
doPostFitCombine = False # doYieldsAndPlots must be true
doPostFitHavester = False # doYieldsAndPlots must be true

doRatesByLikScan = False
#####################################################################

# Download the bellow folders to mom and untar them on the same location than this script
# https://svnweb.cern.ch/cern/wsvn/cmshcg/trunk/cadi/HIG-18-019/
# https://svnweb.cern.ch/cern/wsvn/cmshcg/trunk/cadi/HIG-17-018/
mom_2017 = "HIG-18-019.r7705/2018jun28/" ## these are updated from svn version !!!!!!!!!!!
mom_2017_multilep = "HIG-18-019.r7705/2018jun28/multilep/"
mom_2017_tau = "HIG-18-019.r7705/2018jun28/tau/"
mom_2016 = "HIG-17-018.r7707/2016_for_hig18019/"

print "Working directory is: "+os.getcwd()+"/"
procP1=glob.glob(os.getcwd()+"/"+mom_2017+"/*/*.txt")
procP2=glob.glob(os.getcwd()+"/"+mom_2016+"*.txt")
everybody = procP1 + procP2

## The results are going to be saved on the local folder mom_result
if not takeCombo :
    if not btag_correlated : mom_result = "combo_2016_2017_uncorrJES/"
    else :
        if  blinded : mom_result = "combo_2016_2017/"
        else : mom_result = "combo_2016_2017_unblided/"
else :
    # you will need to put the combined card on the folder hardcoded bellow
    mom_result = "gpetrucc_2017/"
    #mom_result = "gpetrucc_2017_2016/"

ToCondor = " "
if sendToCondor :
    #ToCondor = " --job-mode condor --sub-opt '+MaxRuntime = 18000'"
    ToCondor = "  --job-mode lxbatch --sub-opts=\"-q 1nh\" --task-name "## you need to add a task name using it
    ## the mu's result retrieval are not working in condor -- they work with lxbatch

if blinded : blindStatement = ' -t -1 '
else : blindStatement = ' '

def decorrelate_btag(p) :
    cb.cp().process([p.process()]).RenameSystematic(cb, "CMS_ttHl16_btag_"+s , "CMS_ttHl17_btag_"+s);

def correlate_tauES(p) :
    cb.cp().process([p.process()]).RenameSystematic(cb, "CMS_ttHl_tauES", "CMS_scale_t");

def correlate_tauID(p) :
    cb.cp().process([p.process()]).RenameSystematic(cb, "CMS_ttHl17_tauID", "CMS_eff_t");

def decorrelate_JES(p) :
    cb.cp().process([p.process()]).RenameSystematic(cb, "CMS_scale_j" , "CMS_ttHl17_scale_j");

if not takeCombo :
    if copy_cards :
        run_cmd('mkdir '+os.getcwd()+"/"+mom_result)
        # rename only on the 2017
        for nn, process in enumerate(everybody) :
            cb = ch.CombineHarvester()
            tokens = process.split("/")
            if not "ttH" in process :
                print tokens[8]+" "+tokens[9]+" ignoring card "+process
                continue
            proc_name = "Name"+str(nn+1)
            for part in tokens :
                if "ttH" in part :
                    for name in part.split(".") :
                        if "ttH" in name :
                            print " adding process "+name
                            proc_name = name
            if "HIG-18-019" in process :
                complement = "_2017"
            if "HIG-17-018" in process :
                complement = "_2016"
            cb.ParseDatacard(process, analysis = proc_name+complement, mass = "")
            if not btag_correlated and "HIG-18-019" in process:
              print "start decorrelating btag"
              for s in  ["HF", "LF", "cErr1", "cErr2"] :
                print "renaming for "+s
                cb.ForEachProc(decorrelate_btag)
            if not JES_correlated and "HIG-18-019" in process:
                cb.ForEachProc(decorrelate_JES)
            writer = ch.CardWriter(os.getcwd()+"/"+mom_result+proc_name+complement+'.txt',
                       os.getcwd()+"/"+mom_result+proc_name+complement+'.root')
            writer.WriteCards('LIMITS/cmb', cb)

    everybody = glob.glob(os.getcwd()+"/"+mom_result+"*.txt")

    if btag_correlated :
        cardToWrite = "card_combo_2016_2017_btag_correlated"
        cardToWrite_2017 = "card_combo_2017_btag_correlated"
    else :
        cardToWrite = "card_combo_2016_2017_JES_Notcorrelated"
        cardToWrite_2017 = "card_combo_2017_JES_Notcorrelated"

    if combine_cards :
        string_combine = "combineCards.py "
        string_combine_2017 = "combineCards.py "
        for nn, process in enumerate(everybody) :
            tokens = process.split("/")
            # collect the cards
            if not "ttH" in process :
                print "ignoring card "+process
                continue
            proc_name = "Name"+str(nn+1)
            file_name = "Name"
            for part in tokens :
                if "ttH" in part :
                    file_name = part
                    for name in part.split(".") :
                        if "ttH" in name :
                            print " adding process "+name
                            proc_name = name
            if "Name" in proc_name and "ttH" in process :
                print "There is a problem ..... ..... .... not ignoring card "+process
                break
            # collect the cards to run full combo
            string_combine = string_combine + proc_name+"="+file_name+" "
            if "2016" not in proc_name :
                string_combine_2017 = string_combine_2017 + proc_name+"="+file_name+" "
        string_combine = string_combine+" > "+cardToWrite+".txt"
        run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; "+string_combine+" ; cd %s"  % (os.getcwd()+"/"))
        string_combine_2017 = string_combine_2017+" > "+cardToWrite_2017+".txt"
        run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; "+string_combine_2017+" ; cd %s"  % (os.getcwd()+"/"))

### loop for combo results 2017 and 2017 + 2016
### hardcode the paths if you want to consider already combined cards
if takeCombo :
    cardToWrite_2017 = "comb_2017v2_withCR_sanity"
    cardToWrite = "../gpetrucc_2017_2016/comb_1617v2_withCR_sanity"

    if remove_Clos_t :
        newFile = os.getcwd()+"/"+mom_result+cardToWrite_2017+'_no_Clos.txt'
        path_to_file = os.getcwd()+"/"+mom_result+cardToWrite_2017+".txt"
        with open(newFile, 'w') as out_file:
            with open(path_to_file, 'r') as in_file:
                for line in in_file:
                    if "CMS_ttHl17_Clos_t_shape" not in line : out_file.write(line)
        cardToWrite_2017 = cardToWrite_2017+'_no_Clos'
        """
        cb = ch.CombineHarvester()
        cb.ParseDatacard(os.getcwd()+"/"+mom_result+cardToWrite_2017+".txt", mass = "")
        cb.cp().FilterSysts(lambda systematic : systematic.name() == "CMS_ttHl_Clos_t_shape");
        writer = ch.CardWriter(os.getcwd()+"/"+mom_result+cardToWrite_2017+'_no2l_2tau_Clos.txt',
                   os.getcwd()+"/"+mom_result+cardToWrite_2017+'_no2l_2tau_Clos.root')
        writer.WriteCards('LIMITS/cmb', cb)

        """

redefineToTTH = " --setParameters r_ttH=1,r_ttW=1,r_ttZ=1 --redefineSignalPOI r_ttH "

floating_ttV = \
" --PO 'map=.*/TTZ.*:r_ttZ[1,0,6]'\
 --PO 'map=.*/TTW:r_ttW[1,0,6]'\
 --PO 'map=.*/TTW_.*:r_ttW[1,0,6]'\
 --PO 'map=.*/TTWW.*:r_ttW[1,0,6]' "

sigRates = ["r_ttH_2lss_0tau", "r_ttH_3l_0tau", "r_ttH_4l", "r_ttH_2lss_1tau", "r_ttH_3l_1tau", "r_ttH_2l_2tau", "r_ttH_1l_2tau" ]

for card in [ cardToWrite  ] : # , cardToWrite_2017
    WS_output = card+"_3poi"
    if doFits :
        run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; text2workspace.py %s.txt -o %s.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose  --PO 'map=.*/ttH.*:r_ttH[1,-5,10]' %s ; cd -"  % (card, WS_output, floating_ttV))

        run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; combine -M Significance --signif %s.root %s %s > %s.log  ; cd -"  % (WS_output, blindStatement, redefineToTTH, WS_output))

        run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; combine -M Significance --signif %s.root %s %s > %s_asimov.log -t -1 ; cd -"  % (WS_output, blindStatement, redefineToTTH, WS_output))

        run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; combine -M MultiDimFit %s.root %s --setParameters r_ttH=1,r_ttW=1,r_ttZ=1 --algo singles --cl=0.68 -P r_ttH --floatOtherPOI=1 --saveFitResult -n step1  --saveWorkspace > %s_rate_ttH.log   ; cd -"  % (WS_output, blindStatement, WS_output))
        ## --saveWorkspace to extract the stats only part of the errors and the limit woth mu=1 injected
        ### Some example of this concept here: https://cms-hcomb.gitbooks.io/combine/content/part3/commonstatsmethods.html#useful-options-for-likelihood-scans
        run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; combine -M MultiDimFit -d  higgsCombineteststep1.MultiDimFit.mH120.root   -w w --snapshotName \"MultiDimFit\" -n teststep2 --setParameters r_ttH=1,r_ttW=1,r_ttZ=1 -P r_ttH   -S 0 --algo singles > %s_rate_ttH_stats_only.log   ; cd -"  % (WS_output))
        # --freezeParameters (instead of -S 0) also work on the above

        run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; combine -M AsymptoticLimits %s.root %s --setParameters r_ttH=1,r_ttW=1,r_ttZ=1 --redefineSignalPOI r_ttH -n from1_r_ttH > %s_limit_ttH_from1.log  --cminDefaultMinimizerType Minuit --keepFailures %s from1_r_ttH ; cd -"  % (WS_output, blindStatement, WS_output, ToCondor))

        run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; combine -M AsymptoticLimits -t -1   higgsCombineteststep1.MultiDimFit.mH120.root   --setParameters r_ttH=1,r_ttW=1,r_ttZ=1 --redefineSignalPOI r_ttH  -n from1_r_ttH --snapshotName \"MultiDimFit\"  --toysFrequentist --bypassFrequentistFit  > %s_limit_ttH_from0.log  ; cd -"  % (WS_output, ToCondor))

        # combine -M AsymptoticLimits -t -1   higgsCombineteststep1.MultiDimFit.mH120.root   --setParameters r_ttH=1,r_ttW=1,r_ttZ=1 --redefineSignalPOI r_ttH  -n from1_r_ttH --snapshotName "MultiDimFit"  --toysFrequentist --bypassFrequentistFit  &

        # combine -M AsymptoticLimits  comb_2017v2_withCR_sanity_3poi.root   --setParameters r_ttH=0,r_ttW=1,r_ttZ=1 --redefineSignalPOI r_ttH  -n from0_r_ttH  &

        # combine -M HybridNew --frequentist --testStat LHC  --fork 4 -t -1 --expectSignal 1  higgsCombineteststep1.MultiDimFit.mH120.root   --setParameters r_ttH=1,r_ttW=1,r_ttZ=1 --redefineSignalPOI r_ttH  -n frommu1_r_ttH --snapshotName "MultiDimFit"  --toysFrequentist --bypassFrequentistFit  &

        #combine -M HybridNew --frequentist --testStat LHC -H ProfileLikelihood -- fork 4 -t -1 --expectSignal 1 higgsCombinebestfit.MultiDimFit.mH125.root --snapshotName MultiDimFit --toysFrequentist --bypassFrequentistFit

        #run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; combine -M MultiDimFit %s.root %s --setParameters r_ttH=1,r_ttW=1,r_ttZ=1 --algo singles --cl=0.68  --cminDefaultMinimizerType Minuit --keepFailures > %s_rate_3D.log  ; cd -"  % (WS_output, blindStatement, WS_output))

    if (doHessImpactCombo and card == cardToWrite) or (doHessImpact2017 and card == cardToWrite2017) :
        # hessian impacts
        run_cmd("mkdir "+os.getcwd()+"/"+mom_result+"/HesseImpacts_"+card)
        enterHere = os.getcwd()+"/"+mom_result+"/HesseImpacts_"+card
        run_cmd("cd "+enterHere+" ; combineTool.py -M Impacts -d %s.root --rMin -2 --rMax 5  %s   -m 125 --doFits --approx hesse ; cd - "  % (WS_output, blindStatement))

        run_cmd("cd "+os.getcwd()+"/"+mom_result+" ; combineTool.py -M Impacts -d %s.root -m 125 -o impacts.json --approx hesse --rMin -2 --rMax 5  %s; plotImpacts.py -i impacts.json -o  impacts ; mv impacts.pdf impacts_hesse_JESCorr%s ; cd -" % (WS_output, blindStatement, str(btag_correlated)))

    if (doCategories or doLimitsByCat or  doRatesByLikScan) and card == cardToWrite_2017 :
        ### for category by category - 2017 only
        run_cmd("mkdir "+os.getcwd()+"/"+mom_result+"/categories_"+card+"_2l2t_fromZero")
        enterHere = os.getcwd()+"/"+mom_result+"/categories_"+card+"_2l2t_fromZero"
        print enterHere
        WS_output_byCat = card+"_Catpoi_final"

        floating_by_cat = "\
 --PO 'map=.*2lss_e.*/ttH.*:r_ttH_2lss_0tau[1,-5,10]'\
 --PO 'map=.*2lss_m.*/ttH.*:r_ttH_2lss_0tau[1,-5,10]'\
 --PO 'map=.*3l_b.*/ttH.*:r_ttH_3l_0tau[1,-5,10]'\
 --PO 'map=.*3l_cr.*/ttH.*:r_ttH_3l_0tau[1,-5,10]'\
 --PO 'map=.*4l.*/ttH.*:r_ttH_4l[1,-5,10]'\
 --PO 'map=.*2lss_1tau.*/ttH.*:r_ttH_2lss_1tau[1,-5,10]'\
 --PO 'map=.*3l_1tau.*/ttH.*:r_ttH_3l_1tau[1,-5,10]'\
 --PO 'map=.*2l_2tau.*/ttH.*:r_ttH_2l_2tau[1,0,10]'\
 --PO 'map=.*1l_2tau.*/ttH.*:r_ttH_1l_2tau[1,-5,10]'\
"

        run_cmd("cd "+enterHere+" ; text2workspace.py %s/../%s.txt -o %s.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose %s %s; cd -"  % (enterHere, card, WS_output_byCat, floating_ttV, floating_by_cat))

        parameters = "r_ttW=1,r_ttZ=1"
        for rate in sigRates :
            parameters = parameters+","+rate+"=1"
        print "Will fit the parameters "+parameters

        if doCategories :

            for rate in sigRates + [ "r_ttW", "r_ttZ"  ] :

                run_cmd("cd "+enterHere+" ; combineTool.py -M MultiDimFit %s.root %s --setParameters %s --algo none --cl=0.68 -P %s --floatOtherPOI=1 -S 0 --cminDefaultMinimizerType Minuit --keepFailures > %s_rate_%s.log ; cd -"  % (WS_output_byCat, blindStatement, parameters, rate, WS_output_byCat, rate)) # --algo singles

                run_cmd("cd "+enterHere+" ; combineTool.py -M AsymptoticLimits %s.root %s --setParameters %s -P %s --floatOtherPOI=1 -S 0 --cminDefaultMinimizerType Minuit --keepFailures > %s_limit_%s.log ; cd -"  % (WS_output_byCat, blindStatement, parameters, rate, WS_output_byCat, rate)) # --algo singles

        if doLimitsByCat :

            parameters0 = "r_ttW=1,r_ttZ=1"
            for rate in sigRates :
                parameters0 = parameters0+","+rate+"=0"

            for rate in ["r_ttH_2l_2tau"]: # sigRates + [ "r_ttW" , "r_ttZ" ]:

                run_cmd("cd "+enterHere+" ; combineTool.py -M AsymptoticLimits %s.root %s --setParameters %s --redefineSignalPOI %s  -n from0_%s %s from0_%s > %s_limit_from0_%s.log  ; cd -"  % (WS_output_byCat, blindStatement, parameters0, rate, rate , ToCondor, rate , WS_output_byCat, rate)) #  --floatOtherPOI=1

                run_cmd("cd "+enterHere+" ; combineTool.py -M MultiDimFit %s.root %s --setParameters %s --algo singles --cl=0.68 -P %s --floatOtherPOI=1 --saveFitResult -n step1_%s --saveWorkspace ; cd -"  % (WS_output_byCat, blindStatement, parameters, rate, rate))
                ### I do not try to submit as this is not so slow, and the output of this is needed for the next step

                run_cmd("cd "+enterHere+" ; combineTool.py -M AsymptoticLimits -t -1   higgsCombinestep1_%s.MultiDimFit.mH120.root   --setParameters %s --redefineSignalPOI %s  -n from1_%s --snapshotName \"MultiDimFit\"  --toysFrequentist --bypassFrequentistFit %s from1_%s -n from1_%s  > %s_limit_from1_%s.log ; cd -"  % (rate, parameters, rate, rate, ToCondor, rate, rate, WS_output_byCat, rate)) #  --floatOtherPOI=1
                #    --redefineSignalPOI r_ttH_thiscategory --floatOtherPOI 1 is:
                # - consider only r_ttH_thiscategory as parameter of interest
                # - the other POIs are left freely floating

        if doRatesByLikScan :
            typeFitRates      = [ " ", " -t -1 "]
            typeFitRatesLabel = [ "Obs", "Exp"]
            run_cmd("mkdir "+os.getcwd()+"/"+mom_result+"/categories_"+card+"_folder")
            #enterHere = os.getcwd()+"/"+mom_result+"/categories_"+card+"_folder"
            print enterHere
            WS_output_byCat = card+"_Catpoi_final"

            parameters = "r_ttW=1,r_ttZ=1"
            for rate in ["r_ttH_2lss_0tau", "r_ttH_3l_0tau", "r_ttH_4l", "r_ttH_2lss_1tau", "r_ttH_3l_1tau", "r_ttH_2l_2tau", "r_ttH_1l_2tau"] :
                parameters = parameters+","+rate+"=1"
            print "Will fit the parameters "+parameters

            for rate in ["r_ttH_2l_2tau"] : # sigRates + [ "r_ttW" , "r_ttZ" ] :
                for ll, label in enumerate(typeFitRatesLabel) :
                    if not "2l_2tau" in rate : continue
                    doPlotsByLikScan = False
                    if not doPlotsByLikScan :
                        submit = " "
                        ToCondor1 = ToCondor+" "+label+rate+" --split-points 40"
                        run_cmd("cd "+enterHere+" ; combineTool.py -M MultiDimFit %s.root --setParameters %s -P %s --floatOtherPOI=1 -m 125 --algo=grid --points 200 --rMin 0 --rMax 10  -n %s %s %s  ; cd -"  % (WS_output_byCat,  parameters, rate, label+"_"+rate, typeFitRates[ll],  ToCondor1 )) #
                        ### hadd the result files

                    if doPlotsByLikScan :
                        ## hadd the results, the plotter bellow will also create a file with the crossings
                        ## hadd higgsCombineObs_r_ttH_2l_2tau.POINTS.MultiDimFit.mH125.root higgsCombineObs_r_ttH_2l_2tau.POINTS.*.MultiDimFit.mH125.root
                        run_cmd("cd "+enterHere+" ; $CMSSW_BASE/src/CombineHarvester/CombineTools/scripts/plot1DScan.py higgsCombine%s_%s.MultiDimFit.mH125.root --others higgsCombine%s_%s.MultiDimFit.mH125.root:Expected:2 --POI %s -o ML_%s"  % ( label, rate, label, rate, rate, rate ))

                # hadd higgsCombineObs_r_ttH_2l_2tau.joint.MultiDimFit.mH125.root higgsCombineObs_r_ttH_2l_2tau.POINTS.*.MultiDimFit.mH125.root
                # $CMSSW_BASE/src/CombineHarvester/CombineTools/scripts/plot1DScan.py higgsCombineObs_r_ttH_2l_2tau.joint.MultiDimFit.mH125.root --others higgsCombineExp_r_ttH_2l_2tau.joint.MultiDimFit.mH125.root:Expected:2 --POI r_ttH_2l_2tau -o ML_r_ttH_2l_2tau_joint
    # $CMSSW_BASE/src/CombineHarvester/CombineTools/scripts/plot1DScan.py higgsCombineObs_r_ttH_2lss_0tau.MultiDimFit.mH125.root --others higgsCombineExp.MultiDimFit.mH125.root:Expected:1 --POI r_ttH_2lss_0tau -o ML_r_ttH_2lss_0tau

    #combine -n Obs_r_ttH_2l_2tau -M MultiDimFit -m 125 comb_2017v2_withCR_sanity_Catpoi_final.root --algo=grid --points 20  --setParameters r_ttW=1,r_ttZ=1,r_ttH_2lss_0tau=1,r_ttH_3l_0tau=1,r_ttH_4l=1,r_ttH_2lss_1tau=1,r_ttH_3l_1tau=1,r_ttH_2l_2tau=1,r_ttH_1l_2tau=1,r_ttW=1,r_ttZ=1 -P r_ttH_2l_2tau  --floatOtherPOIs=1 --rMin -4 --rMax 4
    # [#0] WARNING:Minization -- RooMinimizerFcn: Minimized function has error status. Returning maximum FCN so far (1.65516) to force MIGRAD to back out of this region. Error log follows
    # [#0] WARNING:Minization -- RooMinimizerFcn: Minimized function has error status. Returning maximum FCN so far (0.565655) to force MIGRAD to back out of this region. Error log follows

    #combine -n Exp -M MultiDimFit -m 125 comb_2017v2_withCR_sanity_Catpoi_final.root --algo=grid --points 50  --setParameters r_ttW=1,r_ttZ=1,r_ttH_2lss_0tau=1,r_ttH_3l_0tau=1,r_ttH_4l=1,r_ttH_2lss_1tau=1,r_ttH_3l_1tau=1,r_ttH_2l_2tau=1,r_ttH_1l_2tau=1,r_ttW=1,r_ttZ=1 -P r_ttH_2l_2tau  --floatOtherPOIs=1 --rMin -4 --rMax 4  -t -1

    #$CMSSW_BASE/src/CombineHarvester/CombineTools/scripts/plot1DScan.py higgsCombineObs.MultiDimFit.mH125.root --others higgsCombineExp.MultiDimFit.mH125.root:Expected:1 --POI r_ttH_2l_2tau -o ML_r_ttH_2l_2tau

    # $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/systematicsAnalyzer.py ../ttH_2l_2tau_sumOS_mvaOutput_final_x_2017.txt --all -f html > ttH_2l_2tau_sumOS_mvaOutput_final_x_card.html

    # text2workspace.py ../comb_2017v2_withCR_sanity.txt -o comb_2017v2_withCR_sanity_2l_2tau_poi.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose    --PO 'map=.*zpeak.*/ttH.*:r_ttH_2lss_0tau[1,-5,10]'    --PO 'map=.*_3l_cr.*/ttH.*:r_ttH_3l_0tau[1,-5,10]'            --PO 'map=.*_4l_cr.*/ttH.*:r_ttH_4l[1,-5,10]'             --PO 'map=.*_2l_2tau_.*/ttH.*:r_ttH_2l_2tau[1,-5,10]'             --PO 'map=.*/TTZ.*:r_ttZ[1,0,6]'  --PO 'map=.*/TTW:r_ttW[1,0,6]' --PO 'map=.*/TTW_.*:r_ttW[1,0,6]' --PO 'map=.*/TTWW.*:r_ttW[1,0,6]'

    # combine comb_2017v2_withCR_sanity_2l_2tau_poi.root -M MultiDimFit --rMin -5 --rMax 10  --setParameters r_ttW=1,r_ttZ=1,r_ttH_2l_2tau=1 -P r_ttH_2l_2tau  --cminDefaultMinimizerType Minuit --floatOtherPOIs=0

    # combine comb_2017v2_withCR_sanity_2l_2tau_only.root -M MultiDimFit --rMin -5 --rMax 10 -n toys --toysFrequentist -t 200  --setParameters r_ttW=1,r_ttZ=1,r_ttH_2l_2tau=0  --cminDefaultMinimizerType Minuit --floatOtherPOIs=0

    # text2workspace.py ../comb_2017v2_withCR_sanity.txt -o comb_2017v2_withCR_sanity_2l_2tau_only.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose        --PO 'map=.*_2l_2tau_.*/ttH.*:r_ttH_2l_2tau[1,-5,10]'

    # combine comb_2017v2_withCR_sanity_2l_2tau_poi.root -M MaxLikelihoodFit --rMin -5 --rMax 10 --expectSignal 0 -n toys  --setParameters r_ttW=1,r_ttZ=1,r_ttH_2l_2tau=1  --cminDefaultMinimizerType Minuit
    # combine comb_2017v2_withCR_sanity_2l_2tau_poi.root -M MaxLikelihoodFit --rMin -5 --rMax 10 --toysFrequentist -t 200  --expectSignal 0 -n toys  --setParameters r_ttW=1,r_ttZ=1,r_ttH_2l_2tau=0

    # root -l $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/plotParametersFromToys.C+("mlfittoys.root", "mlfit.root","comb_2017v2_withCR_sanity_2l_2tau_poi.root")'

    #combine -n Exp -M MultiDimFit -m 125 htt_tt.txt -t -1 --expectSignal=1 --algo=grid --points 300 --setParameterRanges r=-1.0,4.0
    #wget https://raw.githubusercontent.com/nucleosynthesis/HiggsAnalysis-CombinedLimit/combine_tutorial_SWAN/combine_tutorials_2016/combine_intro/plotMuScan.py
    #wget https://raw.githubusercontent.com/nucleosynthesis/HiggsAnalysis-CombinedLimit/combine_tutorial_SWAN/combine_tutorials_2016/combine_intro/tdrStyle.py
    #python plotMuScan.py
    #combine -n Obs -M MultiDimFit -m 125 htt_tt.txt -t -1 --expectSignal=1 --algo=singles --robustFit=1 --setParameterRanges r=-1.0,4.0
    #combine -n Obs -M MultiDimFit -m 125 htt_tt.txt -t -1 --toysFreq --expectSignal=1 --algo=singles --robustFit=1 --setParameterRanges r=-1.0,4.0

    if (card == cardToWrite and doImpactCombo) or (card == cardToWrite_2017 and doImpact2017) :
        ### For impacts 2017 + 2016 only
        ## there is a funcionality for ignoring the bin stats errors in this fork https://github.com/gpetruc/CombineHarvester/commit/28c66f57649a7f9b279cd3298fe905b2073e095a
        ## it creates many files !!!!
        if not sendToCondor or impactsSubmit :
            run_cmd("mkdir "+os.getcwd()+"/"+mom_result+"/impacts_"+card)
            enterHere = os.getcwd()+"/"+mom_result+"/impacts_"+card
            run_cmd("cd "+enterHere+" ; combineTool.py -M Impacts -m 125 -d %s.root  --setParameters r_ttH=1,r_ttW=1,r_ttZ=1 --redefineSignalPOI r_ttH  --parallel 8 %s --doInitialFit  --keepFailures ; cd - "  % (WS_output, blindStatement))
            run_cmd("cd "+enterHere+" ; combineTool.py -M Impacts -m 125 -d %s.root  --setParameters r_ttH=1,r_ttW=1,r_ttZ=1 --redefineSignalPOI r_ttH  --parallel 8 %s --robustFit 1 --doFits %s ; cd - "  % (WS_output, blindStatement, sendToCondor))
        if not sendToCondor or not impactsSubmit :
            blindedOutputOpt = ' '
            if blindedOutput : blindedOutputOpt =  ' --blind'
            run_cmd("cd "+enterHere+" ; combineTool.py -M Impacts -m 125 -d %s.root  -o impacts.json    %s ; plotImpacts.py -i impacts.json %s -o impacts_btagCorr%s_blinded%s  ; cd -" % (WS_output, redefineToTTH, str(blindedOutputOpt), str(btag_correlated), str(blinded)))

    if (card == cardToWrite and doGOFCombo) or (card == cardToWrite_2017 and doGOF2017) :
        ## it creates many files !!!!
        run_cmd("mkdir "+os.getcwd()+"/"+mom_result+"/gof_"+card)
        enterHere = os.getcwd()+"/"+mom_result+"/gof_"+card
        if sendToCondor :
            ### if you are submitting to condor you need to do in 2 steps, the second step collect the toys
            if GOF_submit :
                run_cmd("cd "+enterHere+' ;  combineTool.py -M GoodnessOfFit --algo=saturated  %s %s.root ; cd -' % (redefineToTTH, WS_output))
                filesh = open(enterHere+"/submit_gof.sh","w")
                filesh.write(
                    "#!/bin/bash\n"+\
                    "for ii in {1..500}\n" # this makes 1000 toys
                    "do\n"
                    "  r=$(( $RANDOM % 10000 ))\n"
                    "  #echo $r \n"
                    "  combineTool.py -M GoodnessOfFit --algo=saturated  "+redefineToTTH+"  -t 2 -s $r -n .toys$ii "+enterHere+"/"+WS_output+".root  --saveToys --toysFreq "+sendToCondor+" \n"
                    "done\n"
                    )
                run_cmd(os.getcwd()+"/"+mom_result+"/GOF"+' ; bash submit_gof.sh ; cd -' )
            else : # CollectGoodnessOfFit
                run_cmd("combineTool.py -M CollectGoodnessOfFit --input higgsCombine.Test.GoodnessOfFit.mH120.root higgsCombine*.GoodnessOfFit.mH120.*.root -o gof.json")
                run_cmd("cd "+os.getcwd()+"/"+mom_result+" ;  $CMSSW_BASE/src/CombineHarvester/CombineTools/scripts/plotGof.py --statistic saturated --mass 120.0 gof.json -o GoF_saturated_"+WS_output+'_btagCorr'+str(btag_correlated)+'_blinded'+str(blinded)+" ; cd -")
        else : # do all toys in series
            run_cmd("cd "+enterHere+' ;  combineTool.py -M GoodnessOfFit --algo=saturated  %s  %s.root ; cd -' % (redefineToTTH, WS_output))
            run_cmd("cd "+enterHere+' ; combineTool.py -M GoodnessOfFit --algo=saturated  %s  -t 1000 -s 12345  %s.root --saveToys --toysFreq ; cd -' % (redefineToTTH, WS_output))
            run_cmd("cd "+enterHere+' ; combineTool.py -M CollectGoodnessOfFit --input higgsCombineTest.GoodnessOfFit.mH120.root higgsCombineTest.GoodnessOfFit.mH120.12345.root -o gof.json ; cd -')
            run_cmd("cd "+enterHere+" ;  $CMSSW_BASE/src/CombineHarvester/CombineTools/scripts/plotGof.py --statistic saturated --mass 120.0 gof.json -o GoF_saturated_"+WS_output+'_btagCorr'+str(btag_correlated)+'_blinded'+str(blinded)+" ; cd -")

    savePostfitCombine  = "PostFitCombine_"+card
    savePostfitHavester = "PostFitHavester_"+card
    if preparePostFitCombine  and card == cardToWrite_2017 :
        ### for category by category - 2017 only
        run_cmd("mkdir "+savePostfitCombine)
        enterHere = os.getcwd()+"/"+mom_result+"/"+savePostfitCombine
        run_cmd("cd "+enterHere+' ; combineTool.py -M FitDiagnostics %s/../%s.root %s --saveNormalization --saveShapes --saveWIthUncertainties %s ; cd -' % (enterHere, WS_output, redefineToTTH, sendToCondor))
        print ("the output with the shapes is going to be fitDiagnostics.Test.root or fitDiagnostics.root depending on your version of combine")

    if preparePostFitHavester  and card == cardToWrite_2017 :
        print ("[WARNING:] combine does not deal well with autoMCstats option for bin by bin stat uncertainty")
        run_cmd("mkdir "+savePostfitHavester)
        enterHere = os.getcwd()+"/"+mom_result+"/"+savePostfitHavester
        run_cmd("cd "+enterHere+' ; combineTool.py -M FitDiagnostics %s/../%s.root %s ; cd -' % (enterHere, WS_output, redefineToTTH))
        print ("the diagnosis that input Havester is going to be on fitDiagnostics.Test.root or fitDiagnostics.root depending on your version of combine -- check if you have a crash!")
        doPostfit = " -f fitDiagnostics.root:fit_s --postfit "
        run_cmd("cd "+enterHere+' ; PostFitShapesFromWorkspace --workspace %s/../%s.root -d %s/../%s.txt -o %s_shapes.root -m 125 --sampling --print %s ; cd -' % (enterHere, WS_output, enterHere, card, WS_output, doPostfit)) # --skip-prefit
        print ("the output with the shapes is "+WS_output+"_shapes.root")

    if doYieldsAndPlots :

        #takeYields = card + "_3poi_ttVFromZero"
        takeYields = WS_output
        doPostfit = "none"
        if blinded : blindStatementPlot = '  '
        else : blindStatementPlot = ' --unblind '

        enterHere = os.getcwd()+"/"+mom_result
        doPostFitCombine = True
        if 1>0 :
            doPostfit = savePostfitCombine
            fileShapes = "fitDiagnostics.root"
            appendHavester = " "
            fileoriginal = "--original %s/../%s.root" % (enterHere,card)
        elif doPostfitHavester :
            doPostfit = savePostfitHavester
            fileShapes = WS_output+"_shapes.root"
            appendHavester = " --fromHavester "
            fileoriginal = " "
        if doPostfit == "none" :
            run_cmd("cd "+enterHere+' ; combineTool.py -M FitDiagnostics %s/../%s.root %s ; cd -' % (enterHere, WS_output, redefineToTTH))
        else : enterHere = enterHere+"/"+doPostfit

        run_cmd("cd "+enterHere+' ; python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a fitDiagnostics.root -g plots.root  -p r_ttH  ; cd -')
        gSystem.Load('libHiggsAnalysisCombinedLimit')
        print ("Retrieving yields from workspace: ", os.getcwd()+"/"+takeYields)
        fin = TFile(os.getcwd()+"/"+mom_result+takeYields+".root")
        wsp = fin.Get('w')
        cmb = ch.CombineHarvester()
        cmb.SetFlag("workspaces-use-clone", True)
        ch.ParseCombineWorkspace(cmb, wsp, 'ModelConfig', 'data_obs', False)
        print "datacard parsed"
        import os
        print ("taking uncertainties from: "+enterHere+'/fitDiagnostics.root')
        print ("the diagnosis that input Havester is going to be on fitDiagnostics.Test.root or fitDiagnostics.root depending on your version of combine -- check if you have a crash!")
        mlf = TFile(enterHere+'/fitDiagnostics.root')
        rfr = mlf.Get('fit_s')
        typeFit = " "
        for fit in ["prefit", "postfit"] :
            print fit+' tables:'
            if fit == "postfit" :
                cmb.UpdateParameters(rfr)
                print ' Parameters updated '
                typeFit = " --doPostFit "
            if not takeCombo :
                labels = [
                "1l_2tau_OS_mvaOutput_final_x_2017",
                "2l_2tau_sumOS_mvaOutput_final_x_2017",
                "3l_1tau_OS_mvaOutput_final_x_2017",
                "2lss_1tau_sumOS_mvaOutput_final_x_2017"
                ]
            else :
                labels=[
                "1l_2tau_OS",
                "2l_2tau_sumOS",
                "3l_1tau_OS",
                "2lss_1tau_sumOS"
                ]
            type = 'tau'
            colapseCat = False
            filey = open(os.getcwd()+"/"+mom_result+"yields_"+type+"_from_combo_"+fit+".tex","w")
            if fit == "prefit" : PrintTables(cmb, tuple(), filey, blindedOutput, labels, type)
            if fit == "postfit" : PrintTables(cmb, (rfr, 500), filey, blindedOutput, labels, type)
            print ("the yields are on this file: ", os.getcwd()+"/"+mom_result+"yields_"+type+"_from_combo_"+fit+".tex")
            if not doPostfit == "none" :
                optionsToPlot = [
                    ' --minY 0.07 --maxY 5000. --useLogPlot --notFlips --unblind ',
                    ' --minY -0.35 --maxY 14 --notFlips --notConversions --unblind ',
                    ' --minY -0.2 --maxY 6.9 --MC_IsSplit --notFlips --unblind ',
                    ' --minY -0.9 --maxY 24 --MC_IsSplit --unblind '
                ]
                for ll, label in enumerate(labels) :
                    run_cmd('python makePostFitPlots_FromCombine.py --channel  ttH_%s  --input %s %s %s %s %s --original %s/../%s.root > %s' % (label, enterHere+"/"+fileShapes, appendHavester, typeFit, blindStatementPlot, optionsToPlot[ll], enterHere, card, enterHere+"/"+fileShapes+"_"+label+".log"))

                    #python makePostFitPlots_FromCombine.py --channel  ttH_3l_1tau_OS  --input /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017//PostFitCombine_comb_2017v2_withCR_sanity/fitDiagnostics.root --minY -0.2 --maxY 6.9 --MC_IsSplit --notFlips --unblind  --original /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017//PostFitCombine_comb_2017v2_withCR_sanity/../comb_2017v2_withCR_sanity.root
                    # python makePostFitPlots_FromCombine.py --channel  ttH_2lss_1tau_sumOS  --input /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017//PostFitCombine_comb_2017v2_withCR_sanity/fitDiagnostics.root --minY -0.5 --maxY 24 --MC_IsSplit --unblind  --original /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017//PostFitCombine_comb_2017v2_withCR_sanity/../comb_2017v2_withCR_sanity.root
                    # python makePostFitPlots_FromCombine.py --channel  ttH_2l_2tau_sumOS  --input /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017//PostFitCombine_comb_2017v2_withCR_sanity/fitDiagnostics.root --minY -0.35 --maxY 13.9 --notFlips --notConversions --unblind  --original /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017//PostFitCombine_comb_2017v2_withCR_sanity/../comb_2017v2_withCR_sanity.root
                    # python makePostFitPlots_FromCombine.py --channel  ttH_1l_2tau_OS  --input /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017//PostFitCombine_comb_2017v2_withCR_sanity/fitDiagnostics.root --minY 0.07 --maxY 5000. --useLogPlot --notFlips --unblind --original /afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017//PostFitCombine_comb_2017v2_withCR_sanity/../comb_2017v2_withCR_sanity.root
            ######################################
            labels = [
                "2lss_ee_neg",
                "2lss_ee_pos",
                "2lss_em_bl_neg",
                "2lss_em_bl_pos",
                "2lss_mm_bl_neg",
                "2lss_mm_bl_pos",
                "2lss_em_bt_neg",
                "2lss_em_bt_pos",
                "2lss_mm_bt_neg",
                "2lss_mm_bt_pos"
                ]
            if takeCombo :
                for label in labels : label = label+"_2017"
            type = 'multilep2lss'
            colapseCat = True
            filey = open(os.getcwd()+"/"+mom_result+"yields_"+type+"_from_combo_"+fit+".tex","w")
            if fit == "prefit" : PrintTables(cmb, tuple(), filey, blindedOutput, labels, type)
            if fit == "postfit" : PrintTables(cmb, (rfr, 500), filey, blindedOutput, labels, type)
            print ("the yields are on this file: ", os.getcwd()+"/"+mom_result+"yields_"+type+"_from_combo_"+fit+".tex")
            if not doPostfit == "none" :
                for ll, label in enumerate(labels) :
                    run_cmd('python makePostFitPlots_FromCombine.py --channel ttH_%s --input %s --minY -0.8 --maxY 29 --notFlips --labelX \"BDT (ttH,tt/ttV)\" %s %s %s --original %s/../%s.root >  %s' % (label, enterHere+"/"+fileShapes, appendHavester, typeFit, blindStatementPlot, enterHere, card, enterHere+"/"+fileShapes+"_"+label+".log"))
            #################################
            labels = [
            "3l_bl_neg",
            "3l_bl_pos",
            "3l_bt_neg",
            "3l_bt_pos",
            "4l"
            ]
            if takeCombo :
                for label in labels : label = label+"_2017"
            type = 'multilep3l4l'
            colapseCat = True
            filey = open(os.getcwd()+"/"+mom_result+"yields_"+type+"_from_combo_"+fit+".tex","w")
            if fit == "prefit" : PrintTables(cmb, tuple(), filey, blindedOutput, labels, type)
            if fit == "postfit" : PrintTables(cmb, (rfr, 500), filey, blindedOutput, labels, type)
            print ("the yields are on this file: ", os.getcwd()+"/"+mom_result+"yields_"+type+"_from_combo_"+fit+".tex")
            if not doPostfit == "none" :
                for ll, label in enumerate(labels) :
                    run_cmd('python makePostFitPlots_FromCombine.py --channel  ttH_%s  --input %s  --minY -0.8 --maxY 29 --notFlips --labelX \"BDT (ttH,tt/ttV)\" %s %s %s --original %s/../%s.root >  %s' % (label, enterHere+"/"+fileShapes, appendHavester, typeFit, blindStatementPlot, enterHere, card , enterHere+"/"+fileShapes+"_"+label+".log"))
            #################################
            labels = [
             "2lss_ee_neg_3j",
             "2lss_ee_pos_3j",
             "2lss_em_bl_neg_3j",
             "2lss_em_bl_pos_3j",
             "2lss_mm_bl_neg_3j",
             "2lss_mm_bl_pos_3j",
             "2lss_em_bt_neg_3j",
             "2lss_em_bt_pos_3j",
             "2lss_mm_bt_neg_3j",
             "2lss_mm_bt_pos_3j"
            ]
            if takeCombo :
                for label in labels : label = label+"_2017"
            type = 'multilepCR2lss'
            colapseCat = True
            filey = open(os.getcwd()+"/"+mom_result+"yields_"+type+"_from_combo_"+fit+".tex","w")
            if fit == "prefit" : PrintTables(cmb, tuple(), filey, blindedOutput, labels, type)
            if fit == "postfit" : PrintTables(cmb, (rfr, 500), filey, blindedOutput, labels, type)
            print ("the yields are on this file: ", os.getcwd()+"/"+mom_result+"yields_"+type+"_from_combo_"+fit+".tex")
            if not doPostfit == "none" :
                for ll, label in enumerate(labels) :
                    run_cmd('python makePostFitPlots_FromCombine.py --channel  ttH_%s  --input %s  --minY -0.8 --maxY 29 --notFlips --labelX \"BDT (ttH,tt/ttV)\" %s %s %s --original %s/../%s.root >  %s' % (label, enterHere+"/"+fileShapes, appendHavester, typeFit, blindStatementPlot, enterHere, card, enterHere+"/"+fileShapes+"_"+label+".log"))
            #################################
            labels = [
            "3l_bl_neg_zpeak",
            "3l_bl_pos_zpeak",
            "3l_bt_neg_zpeak",
            "3l_bt_pos_zpeak",
            "3l_crwz",
            "4l_crzz"
            ]
            if takeCombo :
                for label in labels : label = label+"_2017"
            type = 'multilepCR3l4l'
            colapseCat = True
            filey = open(os.getcwd()+"/"+mom_result+"yields_"+type+"_from_combo_"+fit+".tex","w")
            if fit == "prefit" : PrintTables(cmb, tuple(), filey, blindedOutput, labels, type)
            if fit == "postfit" : PrintTables(cmb, (rfr, 500), filey, blindedOutput, labels, type)
            print ("the yields are on this file: ", os.getcwd()+"/"+mom_result+"yields_"+type+"_from_combo_"+fit+".tex")
            if not doPostfit == "none" :
                for ll, label in enumerate(labels) :
                    run_cmd('python makePostFitPlots_FromCombine.py --channel  ttH_%s  --input %s  --minY -0.8 --maxY 29 --notFlips --labelX \"BDT (ttH,tt/ttV)\" %s %s %s --original %s/../%s.root >  %s' % (label, enterHere+"/"+fileShapes, appendHavester, typeFit, blindStatementPlot, enterHere, card, enterHere+"/"+fileShapes+"_"+label+".log"))


"""
crab status -d crab_HHTo4T_madgraph_pythia8_CP5_M400_lhe_p1 &
crab status -d crab_HHTo4T_madgraph_pythia8_CP5_M700_lhe_p1 &
crab status -d crab_HHTo4T_madgraph_pythia8_CP5_M700_lhe_p1 &
crab status -d crab_HHTo4T_madgraph_pythia8_CP5_M400_lhe_p1 &
crab status -d crab_HHTo4V_madgraph_pythia8_CP5_M700_lhe_p1 &
crab status -d crab_HHTo4V_madgraph_pythia8_CP5_M400_lhe_p1 &
crab status -d crab_HHTo2T2V_madgraph_pythia8_CP5_M400_lhe_p1 &
crab status -d crab_HHTo2T2V_madgraph_pythia8_CP5_M700_lhe_p1 &

"""

#combineTool.py -M AsymptoticLimits comb_2017v2_withCR_sanity_Catpoi_final.root --setParameters r_ttW=1,r_ttZ=1,r_ttH_2lss_0tau=0,r_ttH_3l_0tau=0,r_ttH_4l=0,r_ttH_2lss_1tau=0,r_ttH_3l_1tau=0,r_ttH_2l_2tau=0,r_ttH_1l_2tau=0 --redefineSignalPOI r_ttH_4l -n from0_r_ttH_4l  --cminDefaultMinimizerType Minuit

#[3]+  Done                    combineTool.py -M AsymptoticLimits comb_2017v2_withCR_sanity_Catpoi_final.root --setParameters r_ttW=1,r_ttZ=1,r_ttH_2lss_0tau=1,r_ttH_3l_0tau=1,r_ttH_4l=1,r_ttH_2lss_1tau=1,r_ttH_3l_1tau=1,r_ttH_2l_2tau=1,r_ttH_1l_2tau=1 --redefineSignalPOI r_ttH_4l -n from1_r_ttH_4l
