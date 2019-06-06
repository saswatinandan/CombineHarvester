#!/usr/bin/env python
import os, subprocess, sys
from array import array
import CombineHarvester.CombineTools.ch as ch
from ROOT import *
from math import sqrt, sin, cos, tan, exp
import numpy as np
workingDir = os.getcwd()
#from pathlib2 import Path
execfile("../python/data_manager.py")
from collections import OrderedDict

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--input_folder", type="string", dest="input_folder", help="Where the ", default="/afs/cern.ch/work/a/acarvalh/CMSSW_8_1_0/src/CombineHarvester/ttH_htt/test/gpetrucc_2017/categories_comb_2017v2_withCR_sanity_folder/")
(options, args) = parser.parse_args()

input_folder = options.input_folder
doLog = True

dprocs = OrderedDict()
#dprocs["ttW"]    = [[], [], 12.75, "ttW"]
#dprocs["ttZ"]    = [[], [], 11.25, "ttZ"]

dprocs["ttHw2016"]            = [[], [], 12.75, "Comb.",            "Combined (with 2016)" ]
dprocs["ttH"]            = [[], [], 11.25, "Comb.",            "Combined (2017)" ]
dprocs["ttH_1l_2tau"]    = [[], [], 9.75,  "1l + 2#tau_{h}"  , r"$1\Plepton + 2\tauh$"]
dprocs["ttH_2lss_0tau"]  = [[], [], 8.25,  "2lss"            , r"$2\Plepton ss$ "]
dprocs["ttH_2lss_1tau"]  = [[], [], 6.75,  "2lss + 1#tau_{h}", r"$2\Plepton ss + 1\tauh$" ]
dprocs["ttH_2l_2tau"]    = [[], [], 5.25,  "2l + 2#tau_{h}"  , r"$2\Plepton + 2\tauh$"  ]
dprocs["ttH_3l_0tau"]    = [[], [], 3.75,  "3l"              , r"$3\Plepton$"]
dprocs["ttH_3l_1tau"]    = [[], [], 2.25,  "3l + 1#tau_{h}"  , r"$3\Plepton + 1\tauh$"]
dprocs["ttH_4l"]         = [[], [], 0.75,  "4l"              , r"$4\Plepton$" ]

#gpetrucc_2017/higgsCombineObs_from1_r_ttH_1l_2tau.AsymptoticLimits.mH120.root

def getLimits(folder, name) :
    #  higgsCombinefrom1_r_ttH_4l.AsymptoticLimits.mH120.root
    if "l" in name : toRead = folder+"higgsCombine"+name+".AsymptoticLimits.mH120.root"
    else : toRead = folder+"../higgsCombine"+name+".AsymptoticLimits.mH120.root"
    try : file = TFile(toRead,"READ")
    except :
        print('Couldnt open the file (%s).' % toRead)
        return [-1.,-1.,-1.,-1.,-1.,-1.]
    try : limitTree = file.Get("limit")
    except :
        print('Couldnt open the tree on file (%s).' % toRead)
        return [-1.,-1.,-1.,-1.,-1.,-1.]
    try : limitTree.GetEntries()
    except :
        print('Couldnt open the tree on file (%s).' % toRead)
        return [-1.,-1.,-1.,-1.,-1.,-1.]
    print "Reading limit from: "+toRead
    limitsCat = []
    for entry in limitTree : limitsCat = limitsCat + [entry.limit]
    print limitsCat
    return limitsCat


mg = TMultiGraph();
mg.SetTitle(" ")
yerr = 0.75

filey = open(input_folder+"/upper_limits.tex","w")
filey.write(r"""
\begin{center}
\begin{tabular}{|l|c|c|c|}
\hline
 & Observed limit & Expected limit & Expected limit \\
                & &  ($\mu = 0$) & ($\mu = 1$) \\
\hline
\hline"""+"\n")

for kk, key in enumerate(dprocs.keys()) :
     dprocs[key][0] = getLimits(input_folder, "from0_r_"+key)
     dprocs[key][1] = getLimits(input_folder, "from1_r_"+key)
     filey.write( "%s & $%.2f$ & $%.2f^{+%.2f}_{-%.2f}$ & $%.2f$ & $%.2f^{+%.2f}_{-%.2f}$ \\ \n" % (dprocs[key][4], dprocs[key][0][5], dprocs[key][0][2], dprocs[key][0][3]-dprocs[key][0][2], dprocs[key][0][2]-dprocs[key][0][1], dprocs[key][1][5],dprocs[key][1][2], dprocs[key][1][3]-dprocs[key][1][2], dprocs[key][1][2]-dprocs[key][1][1] ))
     graph_exp2s = TGraphAsymmErrors(len(dprocs.keys()))
     graph_exp2s.SetPoint(kk, dprocs[key][0][2], dprocs[key][2])
     #print (dprocs[key][0][2])
     graph_exp2s.SetPointError(kk, dprocs[key][0][2]-dprocs[key][0][0], dprocs[key][0][4]-dprocs[key][0][2], yerr, yerr)
     graph_exp2s.SetFillColor(kYellow);
     graph_exp2s.SetFillStyle(1001);
     graph_exp2s.SetLineWidth(0);
     mg.Add(graph_exp2s, "2PE")
     ############
     graph_exp1s = TGraphAsymmErrors(len(dprocs.keys()))
     graph_exp1s.SetPoint(kk, dprocs[key][0][2], dprocs[key][2])
     #print (dprocs[key][0][2])
     graph_exp1s.SetPointError(kk, dprocs[key][0][2]-dprocs[key][0][1], dprocs[key][0][3]-dprocs[key][0][2], yerr, yerr)
     graph_exp1s.SetFillColor(kGreen+1);
     graph_exp1s.SetFillStyle(1001);
     graph_exp1s.SetLineWidth(0);
     mg.Add(graph_exp1s, "2PE")
     ############
     graph_exp = TGraphAsymmErrors(len(dprocs.keys()))
     graph_exp.SetPoint(kk, dprocs[key][0][2], dprocs[key][2])
     graph_exp.SetPointError(kk,0., 0., yerr, yerr)
     graph_exp.SetMarkerColor(1);
     graph_exp.SetMarkerStyle(24);
     graph_exp.SetMarkerSize(2);
     graph_exp.SetLineColor(1);
     graph_exp.SetLineStyle(2); # solid
     graph_exp.SetLineWidth(2);
     mg.Add(graph_exp, "P")
     ############
     graph_obs = TGraphAsymmErrors()
     graph_obs.SetPoint(kk, dprocs[key][0][5], dprocs[key][2])
     graph_obs.SetPointError(kk, 0.0, 0.0, yerr, yerr)
     graph_obs.SetMarkerColor(kBlack);
     graph_obs.SetMarkerStyle(20);
     graph_obs.SetMarkerSize(2);
     graph_obs.SetLineColor(kBlack);
     graph_obs.SetLineStyle(1); # solid
     graph_obs.SetLineWidth(2);
     mg.Add(graph_obs, "P")
     #########
     graph_obs_mu1 = TGraphAsymmErrors(len(dprocs.keys()))
     graph_obs_mu1.SetPoint(kk, dprocs[key][1][5], dprocs[key][2])
     graph_obs_mu1.SetPointError(kk, 0.0, 0.0, yerr, yerr)
     graph_obs_mu1.SetMarkerColor(kRed);
     graph_obs_mu1.SetMarkerStyle(24);
     graph_obs_mu1.SetMarkerSize(2);
     graph_obs_mu1.SetLineColor(kRed);
     graph_obs_mu1.SetLineStyle(2); # solid
     graph_obs_mu1.SetLineWidth(2);
     mg.Add(graph_obs_mu1, "P")
filey.close()
print dprocs

c = TCanvas("c","c",750,700);
c.SetLeftMargin(0.25);
c.SetBottomMargin(0.15);

gStyle.SetEndErrorSize(0);
if doLog :
    c.SetLogx(1);
    xmin = 0.3
    xmax = 100.
    textX = 0.08
    legX = 0.6
    legY = 0.55
else :
    xmin = 0.0
    xmax = 15.
    textX = -3.8
    legX = 0.560
    legY = 0.5500


mg.Draw("A");
mg.GetXaxis().SetLimits(xmin,xmax);
mg.GetXaxis().SetTitle("95% CL upper limit on #mu = #sigma/#sigma_{SM}");
mg.GetXaxis().SetNdivisions(505);
mg.GetXaxis().SetTitleFont(62);
mg.GetXaxis().SetTitleOffset(1.35);
mg.GetXaxis().SetTitleSize(0.035);
mg.GetXaxis().SetLabelSize(0.035);
mg.GetXaxis().SetLabelOffset(0.01);
mg.GetYaxis().SetRangeUser(0.02,12.05);
mg.GetYaxis().SetTitle("");
mg.GetYaxis().SetTitleSize(0.);
mg.GetYaxis().SetLabelSize(0.);
mg.GetYaxis().SetTickLength(0.);
mg.GetYaxis().SetTickSize(0.);

legend = TLegend(legX, legY, legX + 0.29, legY + 0.23, "", "brNDC");
legend.SetBorderSize(0);
legend.SetFillColor(0);
legend.AddEntry(graph_obs, "Observed", "lp");
legend.AddEntry(graph_exp, "Expected", "lp");
legend.AddEntry(graph_exp1s, "#pm1 s.d. expected", "f");
legend.AddEntry(graph_exp2s, "#pm2 s.d. expected", "f");
legend.AddEntry(graph_obs_mu1, "t#bar{t}H(#mu=1) injected", "lp");
legend.SetTextSize(0.03);
legend.Draw();

link = TLine(xmin, 10.53, xmax, 10.53)
link.SetLineWidth(1)
link.SetLineColor(1)
link.Draw()

tex = TLatex();
luminosity=41400;
tex.SetTextSize(0.035);
tex.SetTextFont(61);
tex.DrawLatexNDC(0.26, 0.91, "CMS");
tex.SetTextFont(42)
#tex.DrawLatexNDC(0.67, 0.91, "%.1f fb^{-1} (13 TeV)" % (luminosity/1000.));
tex.DrawLatexNDC(0.67, 0.91, "%.1f fb^{-1} (13 TeV)" % (41.5));
tex.SetTextSize(0.035);
tex.SetTextFont(52)
tex.DrawLatexNDC(0.36,0.91,"Preliminary")

tex2 = TLatex();
tex2.SetTextSize(0.035);
for kk, key in enumerate(dprocs.keys()) :
    tex2.DrawLatex(textX, dprocs[key][2]-0.25, dprocs[key][3]);
    #tex2.DrawLatex(-8.75,dprocs[key][1]-0.4, "#bf{#mu = %.2f ^{+%.2f}_{-%.2f}}" % (dprocs[key][0][0], dprocs[key][0][1], abs(dprocs[key][0][2])));

gPad.RedrawAxis();
labels = addLabel_CMS_preliminary()
c.SaveAs(input_folder+"limits_by_cat.pdf")
c.SaveAs(input_folder+"limits_by_cat.png")
print "limits on numeric form are on : "+input_folder+"/upper_limits.tex"
