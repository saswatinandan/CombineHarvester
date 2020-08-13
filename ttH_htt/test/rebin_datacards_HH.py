#!/usr/bin/env python
#python test/rebin_datacards_HH.py --channel "1l_0tau"  --signal_type res --mass spin0_900  --HHtype bbWW  --prepareDatacards_path /home/snandan/hhAnalysis/2016/full_analysis/datacards/hh_bb1l/prepareDatacards/ --output_path /home/snandan/hh_Analysis/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/dumb/ --subcats one_missing_resolved
import os, subprocess, sys
workingDir = os.getcwd()
import os, re, shlex
from ROOT import *
import numpy as np
import array as arr
from math import sqrt, sin, cos, tan, exp
import glob
from datetime import datetime
startTime = datetime.now()

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from subprocess import Popen, PIPE
# ./rebin_datacards.py --channel "4l_0tau"  --BINtype "regular" --doLimits
from io import open

functions = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/python/data_manager_rebin_datacards.py"
class mainprogram():
    def runme(self):
        execfile(functions)
this = mainprogram()
this.runme()
testPrint()

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--channel ", type="string", dest="channel", help="The ones whose variables implemented now are:\n   - 1l_2tau\n   - 2lss_1tau\n It will create a local folder and store the report*/xml", default="2lss_1tau")
parser.add_option("--variables", type="string", dest="variables", help="Add convention to file name", default="teste")
parser.add_option("--BINtype", type="string", dest="BINtype", help="regular / ranged / quantiles", default="regular")
parser.add_option("--do_signalFlat", action="store_true", dest="do_signalFlat", help="whether you want to make signal flat or total bkg flat", default=False)
parser.add_option("--output_path", type="string", dest="output_path", help="Where to copy prepareDatacards and make subdiretories with results")
parser.add_option("--prepareDatacards_path", type="string", dest="prepareDatacard_path", help="Where to copy prepareDatacards and make subdiretories with results")
parser.add_option("--doPlots", action="store_true", dest="doPlots", help="If you call this will not do plots with repport", default=False)
parser.add_option("--drawLimitsOnly", action="store_true", dest="drawLimitsOnly", help="If you call this will not do plots with repport", default=False)
parser.add_option("--doLimitsOnly", action="store_true", dest="doLimitsOnly", help="If you call this will not do plots with repport", default=False)
parser.add_option("--BDTfor", type="string", dest="BDTfor", help="type of BDT to be considered", default="SM")
parser.add_option("--plot_hadd", action="store_true", dest="plot_hadd", help="plot after doing hadd for all subcategories", default=False)
parser.add_option(
    "--signal_type",    type="string",       dest="signal_type",
    help="Options: \"nonresLO\" | \"nonresNLO\" | \"res\" ",
    default="nonresLO"
    )
parser.add_option(
    "--mass",           type="string",       dest="mass",
    help="Options: \n nonresNLO = it will be ignored \n nonresLO = \"SM\", \"BM12\", \"kl_1p00\"... \n \"spin0_900\", ...",
    default="kl_1p00"
    )
parser.add_option(
    "--HHtype",         type="string",       dest="HHtype",
    help="Options: \"bbWW\" | \"multilep\" ",
    default="bbWW"
    )
parser.add_option(
    "--era", type="int",
    dest="era",
    help="To appear on the name of the file with the final plot. If era == 0 it assumes you gave the path for the 2018 era and it will use the same naming convention to look for the 2017/2016.",
    default=2016
    )
parser.add_option(
    "--subcats", 
    choices = ["Res_allReco", "boosted_semiboosted", "one_missing_boosted", "one_missing_resolved", ""],
    dest="subcats",
    help="subcategory to be considered in rebinning",
    default=''
    )
parser.add_option(
    "--combine",
    action = "store_true",
    dest="combine",
    help="whether wan to combine the cards or skip",
    default=False
    )
parser.add_option(
    "--add_missingjet_2b",
    action = "store_true",
    dest="add_missingjet_2b",
    help="whether want to add missing jet 2b category to combine",
    default=False
    )
parser.add_option(
    "--add_missingjet_1b",
    action = "store_true",
    dest="add_missingjet_1b",
    help="whether want to add add missing jet 1b tagged jet category to combine",
    default=False
    )
parser.add_option(
    "--add_Resolved_2b",
    action = "store_true",
    dest="add_Resolved_2b",
    help="whether want to add Resolved 2b category to combine",
    default=False
    )
parser.add_option(
    "--add_Resolved_1b",
    action = "store_true",
    dest="add_Resolved_1b",
    help="whether want to add Resolved 1b category to combine",
    default=False
    )

parser.add_option(
    "--add_boosted",
    action = "store_true",
    dest="add_boosted",
    help="whether want to add boosted category to combine",
    default=False
    )
parser.add_option(
    "--add_semiboosted",
    action = "store_true",
    dest="add_semiboosted",
    help="whether want to add semiboosted category to combine",
    default=False
    )

parser.add_option(
    "--add_missingjet_boosted",
    action = "store_true",
    dest="add_missingjet_boosted",
    help="whether want to add missingjet boosted category to combine",
    default=False
    )

(options, args) = parser.parse_args()

doLimitsOnly   = options.doLimitsOnly
drawLimitsOnly = options.drawLimitsOnly
doPlots    = options.doPlots
channel    = options.channel
BINtype    = options.BINtype
do_signalFlat = options.do_signalFlat
signal_type  = options.signal_type
mass         = options.mass
HHtype       = options.HHtype
era          = options.era
local        = options.output_path
mom          = options.prepareDatacard_path
in_more_subcats = options.subcats
combine = options.combine
add_missingjet_2b = options.add_missingjet_2b
add_missingjet_1b = options.add_missingjet_1b
add_Resolved_2b = options.add_Resolved_2b
add_Resolved_1b = options.add_Resolved_1b
add_boosted = options.add_boosted
add_semiboosted = options.add_semiboosted
add_missingjet_boosted = options.add_missingjet_boosted
BDTfor =  options.BDTfor
plot_hadd = options.plot_hadd
## HH
if channel == "2l_0tau"   : execfile(os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt//cards/info_2l_0tau_datacards.py")
if channel == "1l_0tau"   : execfile(os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt//cards/info_1l_0tau_datacards.py")

info = read_from(in_more_subcats, BDTfor)
print ("Cards to rebin from %s" % channel)

sendToCondor = False
ToSubmit = " "
if sendToCondor :
    ToSubmit = " --job-mode condor --sub-opt '+MaxRuntime = 1800' --task-name"

sources           = []
bdtTypesToDo      = []
bdtTypesToDoLabel = []
bdtTypesToDoFile  = []
sourcesCards      = []

#local = info["local"]
import shutil,subprocess
proc=subprocess.Popen(["mkdir %s" % local],shell=True,stdout=subprocess.PIPE)
out = proc.stdout.read()

mom_datacards = "%s/datacards_rebined/" % local
proc=subprocess.Popen(["mkdir %s" % mom_datacards],shell=True,stdout=subprocess.PIPE)
out = proc.stdout.read()

print (info["bdtTypes"])

counter=0
for ii, bdtType in enumerate(info["bdtTypes"]) :
    fileName = mom   + "/prepareDatacards_" + info["ch_nickname"] + "_" + bdtType + ".root"
    source   = local + "/prepareDatacards_" + info["ch_nickname"] + "_" + bdtType
    print (fileName)
    if os.path.isfile(fileName) :
        proc              = subprocess.Popen(['cp ' + fileName + " " + local],shell=True,stdout=subprocess.PIPE)
        out = proc.stdout.read()
        sources           = sources + [source]
        bdtTypesToDo      = bdtTypesToDo +[channel+" "+bdtType]
        bdtTypesToDoLabel = bdtTypesToDoLabel + [channel+" "+bdtType]
        bdtTypesToDoFile  = bdtTypesToDoFile+[bdtType]
        ++counter
        print ("rebinning ", sources[counter])
    else : print ("does not exist ",source)
print ("I will rebin", bdtTypesToDoLabel,"(",len(sources),") BDT options")

if BINtype == "regular" or BINtype == "ranged" :
    binstoDo = info["nbinRegular"]
if BINtype == "quantiles" :
    binstoDo = info["nbinQuant"]
if BINtype == "none" :
    binstoDo=np.arange(1, info["originalBinning"])
print binstoDo

### first we do one datacard.txt / bdtType
for nn, source in enumerate(sources) :
    if BINtype == "regular" :
        outfile = "%s" % (source.replace("prepareDatacards_", "datacard_"))
    if BINtype == "quantiles" or BINtype == "ranged":
        outfile = "%s_%s" % (source.replace("prepareDatacards_", "datacard_"), BINtype )

    cmd = "WriteDatacards.py "
    cmd += "--inputShapes %s.root " % (source)
    cmd += "--channel %s " % channel
    cmd += "--output_file %s " % (outfile)
    cmd += "--noX_prefix --era 2017  --no_data --analysis HH " # --only_ttH_sig --only_BKG_sig --only_tHq_sig --fake_mc
    ## TODO add only_HH_sig in WriteDatacards
    cmd += " --signal_type %s "      % signal_type
    cmd += " --mass %s "             % mass
    cmd += " --HHtype %s "           % HHtype
    log_datacard = "%s_datacard.log" % source
    runCombineCmd(cmd, ".", log_datacard)

    didCard = False
    for line in open(log_datacard):
        if "Output file:" in line :
            fileCard = line.split(" ")[3].replace("'","").replace(",","").replace(".txt","") #splitPath(lineL)[1]
            print("done card %s.txt" % fileCard)
            didCard = True
            break
    if didCard == False :
        print ("!!!!!!!!!!!!!!!!!!!!!!!! The WriteDatacards did not worked, to debug please check %s to see up to when the script worked AND run again for chasing the error:" % log_datacard)
        print(cmd)
        sys.exit()
    sourcesCards = sourcesCards + [ fileCard ]

nameOutFileAdd = ""
if BINtype=="none" :
    nameOutFileAdd =  "bins_none"
if BINtype=="regular" or options.BINtype == "mTauTauVis":
    nameOutFileAdd =  "bins"
if BINtype=="ranged" :
    nameOutFileAdd =  "bins_ranged"
if BINtype=="quantiles" :
    nameOutFileAdd = "bins_quantiles"

colorsToDo=['r','g','b','m','y','c', 'fuchsia', "peachpuff",'k','orange','y','c'] #['r','g','b','m','y','c','k']
#########################################
if not (drawLimitsOnly or doLimitsOnly) :
    ## make rebinned datacards
    fig, ax = plt.subplots(figsize=(5, 5))
    plt.title(BINtype+" in sum of BKG ")
    lastQuant=[]
    xmaxQuant=[]
    xminQuant=[]
    bin_isMoreThan02 = []
    maxplot = -99.
    ncolor = 0
    ncolor2 = 0
    linestyletype = "-"

    for nn, sourceL in enumerate(sourcesCards) :
        print ( "rebining %s" % sourceL )
        errOcont = rebinRegular(
            sourceL,
            binstoDo,
            BINtype,
            do_signalFlat,
            info["originalBinning"],
            doPlots,
            bdtTypesToDo[nn],
            mom_datacards,
            nameOutFileAdd,
            info["withFolder"]
            )
        if max(errOcont[2]) > maxplot :
            maxplot = max(errOcont[2])
        print bdtTypesToDo[nn]
        lastQuant=lastQuant+[errOcont[4]]
        xmaxQuant=xmaxQuant+[errOcont[5]]
        xminQuant=xminQuant+[errOcont[6]]
        bin_isMoreThan02 = bin_isMoreThan02 + [errOcont[7]]

        print (binstoDo,errOcont[2])
        plt.plot(binstoDo, errOcont[2], color=colorsToDo[ncolor],linestyle=linestyletype,label=bdtTypesToDo[nn].replace("ttH_1l_2tau","BDT PAS").replace("output_NN_","NN_").replace("_ttH_tH_3cat_","").replace("1l_2tau","").replace("2lss_1tau_","").replace("_1tau","").replace("2lss","").replace("__","_"))  #.replace("3l_0tau output_NN_3l_ttH_tH_3cat_v8_", "") ) # ,label=bdtTypesToDo[nn]
        ncolor = ncolor + 1
        if ncolor == 10 :
            ncolor = 0
            ncolor2 = ncolor2 + 1
            if ncolor2 == 0 : linestyletype = "-"
            if ncolor2 == 1 : linestyletype = "-."
            if ncolor2 == 2 : linestyletype = ":"
        ax.set_xlabel('nbins')

    plt.axis((min(binstoDo),max(binstoDo),0,maxplot*1.5))
    ax.set_ylabel('err/content last bin')
    ax.legend(loc='best', fancybox=False, shadow=False, ncol=1, fontsize=8)
    plt.grid(True)
    namefig = local + '/' + options.variables + '_'+ signal_type + '_' + mass + '_' + options.subcats + '_ErrOcont_' + BINtype + '.png'
    fig.savefig(namefig)
    print ("saved",namefig)
    print (bin_isMoreThan02)
    #########################################
    ## plot quantiles boundaries
    if BINtype == "quantiles" :
        ncolor = 0
        fig, ax = plt.subplots(figsize=(5, 5))
        plt.title(BINtype+" binning "+options.variables)
        linestyletype = "-"
        for nn,source in enumerate(sources) :
            print (len(binstoDo),len(lastQuant[nn-1]))
            plt.plot(binstoDo,lastQuant[nn], color=colorsToDo[ncolor],linestyle=linestyletype)
            plt.plot(binstoDo,lastQuant[nn], color=colorsToDo[ncolor],linestyle=linestyletype,marker='o') # ,label=bdtTypesToDo[nn]
            plt.plot(binstoDo,xmaxQuant[nn], color=colorsToDo[ncolor],linestyle=linestyletype,marker='x')
            plt.plot(binstoDo,xminQuant[nn], color=colorsToDo[ncolor],linestyle=linestyletype,marker='.')
            ncolor = ncolor + 1
            if ncolor == 10 or ncolor == 20:
                ncolor = 0
                if ncolor == 10 : linestyletype = "--"
                if ncolor == 20 : linestyletype = ":"
        ax.set_xlabel('nbins')
        ax.set_ylabel('err/content last bin')
        plt.axis((min(binstoDo),max(binstoDo),0,1.0))
        line_up, = plt.plot(binstoDo, 'o-', color='k',label="last bin low")
        line_down, = ax.plot(binstoDo, 'x--', color='k',label="Max")
        line_d, = ax.plot(binstoDo, '.--', color='k',label="Min")
        legend1 = plt.legend(handles=[line_up, line_down, line_d], loc='best', fontsize=8)
        ax.set_ylabel('boundary')
        plt.grid(True)
        fig.savefig(local+'/'+options.variables+'_fullsim_boundaries_quantiles.pdf')

if not drawLimitsOnly :
    ## doint Limits
    for nn, sourceL in enumerate(sourcesCards) :
        for nbins in binstoDo :
            fileCardOnlyL = sourceL.split("/")[len(sourceL.split("/")) -1]
            fileCardOnlynBinL = "%s_%s%s" % (fileCardOnlyL, str(nbins), nameOutFileAdd)
            fileCardL = "%s/%s" % (mom_datacards, fileCardOnlynBinL)
            print ("make limit for %s.txt" % fileCardL)
            runCombineCmd("cp %s.txt %s.txt" % (sourceL, fileCardL))
            with open("%s.txt" % fileCardL,'r+') as ff:
                filedata = ff.read()
                filedata = filedata.replace(fileCardOnlyL, fileCardOnlynBinL)
                ff.truncate(0)
                ff.write(filedata)

            cmd = "combineTool.py  -M AsymptoticLimits  -t -1 %s.txt " % (fileCardL)
            if sendToCondor :
                cmd += ToSubmit + " %s_%s%s " % ()
            runCombineCmd(cmd,  local, "%s.log" % fileCardL)

            if nbins in info["makePlotsBin"] :
                # make only HH be considered signal (independent of the card marking)
                FolderOut = "%s/results/" % mom_datacards
                proc=subprocess.Popen(["mkdir %s" % FolderOut],shell=True,stdout=subprocess.PIPE)
                out = proc.stdout.read()

                cmd = "text2workspace.py"
                cmd += " %s.txt  " % (fileCardOnlynBinL)
                cmd += " -o %s/%s_WS.root" % (FolderOut, fileCardOnlynBinL)
                runCombineCmd(cmd, mom_datacards)
                print ("done %s/%s_WS.root" % (FolderOut, fileCardOnlynBinL))

                cmd = "combineTool.py -M FitDiagnostics "
                cmd += " %s_WS.root" % fileCardOnlynBinL
                #if blinded :
                #    cmd += " -t -1 "
                cmd += " --saveShapes --saveWithUncertainties "
                cmd += " --saveNormalization "
                cmd += " --skipBOnlyFit "
                cmd += " -n _shapes_combine_%s" % fileCardOnlynBinL
                runCombineCmd(cmd, FolderOut)
                fileShapes = glob.glob("%s/fitDiagnostics_shapes_combine_%s*root" % (FolderOut, fileCardOnlynBinL))[0]
                print ( "done %s" % fileShapes )

                savePlotsOn = "%s/plots/" % (mom_datacards)
                cmd = "mkdir %s" % savePlotsOn
                runCombineCmd(cmd)

                plainBins = False
                cmd = "python test/makePlots.py "
                cmd += " --input  %s" % fileShapes
                cmd += " --odir %s" % savePlotsOn
                #if doPostFit         :
                #    cmd += " --postfit "
                if not plainBins :
                    cmd += " --original %s/%s.root"        % (mom_datacards, fileCardOnlynBinL)
                cmd += " --era %s" % str(era)
                cmd += " --nameOut %s" % fileCardOnlynBinL
                #cmd += " --do_bottom "
                cmd += " --channel %s" % channel
                cmd += " --HH --binToRead HH_%s --binToReadOriginal  HH_%s " % (channel, channel)
                #cmd += "--nameLabel %s --labelX %s" % (toRead.replace(filebegin, ""), toRead.replace(filebegin, ""))
                #if not blinded         :
                #cmd += " --unblind  "
                cmd += " --signal_type %s "      % signal_type
                cmd += " --mass %s "             % mass
                cmd += " --HHtype %s "           % HHtype
                plotlog = "%s/%s_plot.log" % (savePlotsOn, fileCardOnlynBinL)
                runCombineCmd(cmd, '.', plotlog)

                didPlot = False
                for line in open(plotlog):
                    if '.pdf' in line and "saved" in line :
                        print(line)
                        didPlot = True
                        break
                if didPlot == False :
                    print ("!!!!!!!!!!!!!!!!!!!!!!!! The makePlots did not worked, to debug please check %s to see up to when the script worked AND run again for chasing the error:" % plotlog)
                    print(cmd)
                    #sys.exit()

#########################################
## make limits
print sources

print "draw limits"
fig, ax = plt.subplots(figsize=(5, 5))
if BINtype == "quantiles" :
    namefig=local+'/'+options.variables+ '_'+options.channel+'_'+signal_type +'_'+mass+'_'+options.subcats +'_fullsim_limits_quantiles'
if BINtype == "regular" or BINtype == "mTauTauVis":
    namefig=local+'/'+options.variables+'_'+options.channel+'_'+signal_type +'_'+mass+'_'+options.subcats +'_fullsim_limits'
if BINtype == "ranged" :
    namefig=local+'/'+options.variables+'_fullsim_limits_ranged'
file = open(namefig+".csv","w")
maxlimit =-99.
for nn, source in enumerate(sourcesCards) :
    fileCardOnlyL = source.split("/")[len(source.split("/")) -1]
    print(fileCardOnlyL)
    limits = ReadLimits(
        fileCardOnlyL,
        binstoDo,
        BINtype,
        channel,
        mom_datacards,
        0, 0,
        sendToCondor,
        nameOutFileAdd
        )
    print (len(binstoDo),len(limits[0]))
    print 'binstoDo= ', binstoDo
    print limits[0]
    if max(limits[0]) > maxlimit : maxlimit = max(limits[0])
    for jj in limits[0] : file.write(unicode(str(jj)+', '))
    file.write(unicode('\n'))
    plt.plot(
        binstoDo,limits[0], color=colorsToDo[nn], linestyle='-',marker='o',
        label=bdtTypesToDoFile[nn].replace("output_NN_", "").replace("_withWZ", "").replace("3l_0tau", "") #.replace("mvaOutput_0l_2tau_deeptauVTight", "mva_legacy")
        )
    plt.plot(binstoDo,limits[1], color=colorsToDo[nn], linestyle='-')
    plt.plot(binstoDo,limits[3], color=colorsToDo[nn], linestyle='-')
ax.legend(
    loc='upper left',
    fancybox=False,
    shadow=False ,
    ncol=1,
    fontsize=8
)
ax.set_xlabel('nbins')
ax.set_ylabel('limits')
maxsum=0
#maxlim = info["maxlim"]
maxlim = 1.5*maxlimit
minlim = info["minlim"]
plt.axis((min(binstoDo),max(binstoDo), minlim, maxlim))
fig.savefig(namefig+'_ttH.png')
fig.savefig(namefig+'_ttH.pdf')
file.close()
print ("saved",namefig)
print(datetime.now() - startTime)

if combine :
 firstpart = mom_datacards + "datacard_hh_bb1l_hh_bb1l_cat_jet_2BDT_Wjj_BDT_X900GeV_"
 lastpart = "_bbWW_%s_%s_12bins.txt" %(signal_type, mass)
 HbbFat_WjjFat_HP_e = firstpart+ "HbbFat_WjjFat_HP_e" +lastpart
 HbbFat_WjjFat_HP_m = firstpart+"HbbFat_WjjFat_HP_m" +lastpart
 HbbFat_WjjFat_LP_e = firstpart+"HbbFat_WjjFat_LP_e" +lastpart
 HbbFat_WjjFat_LP_m = firstpart+"HbbFat_WjjFat_LP_m" +lastpart
 HbbFat_WjjRes_allReco_e = firstpart+"HbbFat_WjjRes_allReco_e" +lastpart
 HbbFat_WjjRes_allReco_m = firstpart+"HbbFat_WjjRes_allReco_m" +lastpart
 Res_allReco_2b_e = firstpart+"Res_allReco_2b_e" +lastpart
 Res_allReco_2b_m = firstpart+"Res_allReco_2b_m" +lastpart

 Res_allReco_1b_e = firstpart+"Res_allReco_1b_e" +lastpart
 Res_allReco_1b_m = firstpart+"Res_allReco_1b_m" +lastpart

 HbbFat_WjjRes_MissJet_e = firstpart+ "HbbFat_WjjRes_MissJet_e" + lastpart
 HbbFat_WjjRes_MissJet_m = firstpart+ "HbbFat_WjjRes_MissJet_m" + lastpart
 Res_MissWJet_2b_e = firstpart + "Res_MissWJet_2b_e" + lastpart
 Res_MissWJet_2b_m = firstpart + "Res_MissWJet_2b_m" + lastpart

 Res_MissWJet_1b_e = firstpart + "Res_MissWJet_1b_e" + lastpart
 Res_MissWJet_1b_m = firstpart + "Res_MissWJet_1b_m" + lastpart

 combinecard = "combinecard_%s_%s_addResolved_2b_%s_add_Resolved_1b_%s_add_semiboosted_%s_add_boosted_%s_add_missingjet_boosted_%s_add_missingjet_2b_%s_add_missingjet_1b_%s" %(signal_type, mass, add_Resolved_2b, add_Resolved_1b, add_semiboosted, add_boosted, add_missingjet_boosted, add_missingjet_2b, add_missingjet_1b)
 FolderOut = "%s/results/" % mom_datacards

 cmd = ''
 if add_boosted :
     cmd = "combineCards.py HbbFat_WjjFat_HP_e=%s HbbFat_WjjFat_HP_m=%s HbbFat_WjjFat_LP_e=%s HbbFat_WjjFat_LP_m=%s" %(HbbFat_WjjFat_HP_e, HbbFat_WjjFat_HP_m, HbbFat_WjjFat_LP_e, HbbFat_WjjFat_LP_m)

 if add_semiboosted : 
     if len(cmd) :
         cmd += " HbbFat_WjjRes_allReco_e=%s HbbFat_WjjRes_allReco_m=%s" %(HbbFat_WjjRes_allReco_e, HbbFat_WjjRes_allReco_m)
     else :
         cmd = " combineCards.py  HbbFat_WjjRes_allReco_e=%s HbbFat_WjjRes_allReco_m=%s" %(HbbFat_WjjRes_allReco_e, HbbFat_WjjRes_allReco_m)
 if add_Resolved_2b :
     if len(cmd) :
         cmd += " Res_allReco_2b_e=%s Res_allReco_2b_m=%s " %(Res_allReco_2b_e, Res_allReco_2b_m)
     else :
         cmd = "combineCards.py  Res_allReco_2b_e=%s Res_allReco_2b_m=%s " %(Res_allReco_2b_e, Res_allReco_2b_m)
         if plot_hadd :
             cmd_hadd = "hadd %sRes_allReco_2b%s %s %s " %(firstpart, lastpart.replace("txt", "root"), Res_allReco_2b_e.replace("txt","root"), Res_allReco_2b_m.replace("txt","root"))
             print cmd_hadd
             runCombineCmd(cmd_hadd, local, "hadd_%s_%s_Res_allReco_2b.log" %(signal_type, mass))

 if add_Resolved_1b :
     if len(cmd) :
        cmd += " Res_allReco_1b_e=%s Res_allReco_1b_m=%s" %(Res_allReco_1b_e, Res_allReco_1b_m)
     else :
         cmd = "combineCards.py  Res_allReco_1b_e=%s Res_allReco_1b_m=%s " %(Res_allReco_1b_e, Res_allReco_1b_m)
         if plot_hadd :
             cmd_hadd = "hadd %sRes_allReco_1b%s %s %s " %(firstpart, lastpart.replace("txt", "root"), Res_allReco_1b_e.replace("txt","root"), Res_allReco_1b_m.replace("txt","root"))
             print cmd_hadd
             runCombineCmd(cmd_hadd, local, "hadd_%s_%s_Res_allReco_1b.log" %(signal_type, mass))
 if add_missingjet_2b :
     if len(cmd) :
         cmd += " Res_MissWJet_2b_e=%s Res_MissWJet_2b_m=%s" %(Res_MissWJet_2b_e, Res_MissWJet_2b_m)
     else :
         cmd = "combineCards.py Res_MissWJet_2b_e=%s Res_MissWJet_2b_m=%s" %(Res_MissWJet_2b_e, Res_MissWJet_2b_m)

 if add_missingjet_1b :
     if len(cmd) :
         cmd += " Res_MissWJet_1b_e=%s Res_MissWJet_1b_m=%s" %(Res_MissWJet_1b_e, Res_MissWJet_1b_m)
     else :
         cmd = "combineCards.py Res_MissWJet_1b_e=%s Res_MissWJet_1b_m=%s" %(Res_MissWJet_1b_e, Res_MissWJet_1b_m)
 if add_missingjet_boosted :
     if len(cmd) :
         cmd += " HbbFat_WjjRes_MissJet_e=%s HbbFat_WjjRes_MissJet_m=%s" %(HbbFat_WjjRes_MissJet_e, HbbFat_WjjRes_MissJet_m)
     else :
         cmd = "combineCards.py HbbFat_WjjRes_MissJet_e=%s HbbFat_WjjRes_MissJet_m=%s" %(HbbFat_WjjRes_MissJet_e, HbbFat_WjjRes_MissJet_m)

 cmd += " > %s/%s.txt" %(mom_datacards, combinecard)
 runCombineCmd(cmd, local, "combinecard.log")
 cmd = "combineTool.py  -M AsymptoticLimits  -t -1 %s/%s.txt " % (mom_datacards, combinecard)
 runCombineCmd(cmd,  local, "%s.log" % combinecard)
 if plot_hadd :
     pass
 


