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

dprocs = OrderedDict()
#dprocs["ttW"]    = [[], 12.25, "ttW"]
#dprocs["ttZ"]    = [[], 10.25, "ttZ"]
dprocs["ttH_1l_2tau"]    = [[], 9.75, "1l + 2#tau_{h}"]
dprocs["ttH_2lss_0tau"]  = [[], 8.25, "2lss"]
dprocs["ttH_2lss_1tau"]  = [[], 6.75, "2lss + 1#tau_{h}"]
dprocs["ttH_2l_2tau"]  = [[], 5.25, "2l + 2#tau_{h}"]
dprocs["ttH_3l_0tau"]    = [[], 3.75, "3l"]
dprocs["ttH_3l_1tau"]    = [[], 2.25, "3l + 1#tau_{h}"]
dprocs["ttH_4l"]         = [[], 0.75, "4l"]

dprocsExp  = OrderedDict()
#dprocsExp["ttW"]    = [[], 12.25, "ttW"]
#dprocsExp["ttZ"]    = [[], 10.25, "ttZ"]
dprocsExp["ttH_1l_2tau"]    = [[], 9.75, "1l + 2#tau_{h}"]
dprocsExp["ttH_2lss_0tau"]  = [[], 8.25, "2lss"]
dprocsExp["ttH_2lss_1tau"]  = [[], 6.75, "2lss + 1#tau_{h}"]
dprocsExp["ttH_2l_2tau"]  = [[], 5.25, "2l + 2#tau_{h}"]
dprocsExp["ttH_3l_0tau"]    = [[], 3.75, "3l"]
dprocsExp["ttH_3l_1tau"]    = [[], 2.25, "3l + 1#tau_{h}"]
dprocsExp["ttH_4l"]         = [[], 0.75, "4l"]

for key in dprocs.keys() :
    my_file = "%sr_%s_rate.txt" % (input_folder, key)
    with open(my_file, 'r') as in_file :
      for line in in_file :
        if "Observed:" in line or "Expected:" in line:
            print (key, line.split(" "))
            for li in line.split() :
                try: float(li)
                except ValueError: continue
                if "Observed:" in line : dprocs[key][0].append(float(li))
                if "Expected:" in line : dprocsExp[key][0].append(float(li))
print " "
### read combined
card = "comb_2017v2_withCR_sanity"
my_file = "%s../%s_3poi_rate_ttH.log" % (input_folder, card)
combined = []
print "Combined: "
with open(my_file, 'r') as in_file :
  for line in in_file :
    if "r_ttH :" in line :
        for li in line.split() :
            try: float(li)
            except ValueError:
                for li2 in li.split("/") :
                    try: float(li2)
                    except ValueError: continue
                    print float(li2)
                    combined = combined + [float(li2)]
                continue
            print li
            combined = combined + [float(li)]
print combined
### read combined
card = "comb_2017v2_withCR_sanity"
my_file = "%s../%s_3poi_rate_ttH_stats_only.log" % (input_folder, card)
combined_stas_only = []
print "Combined: "
with open(my_file, 'r') as in_file :
  for line in in_file :
    if "r_ttH :" in line :
        for li in line.split() :
            try: float(li)
            except ValueError:
                for li2 in li.split("/") :
                    try: float(li2)
                    except ValueError: continue
                    print float(li2)
                    combined_stas_only = combined_stas_only + [float(li2)]
                continue
            print li
            combined_stas_only = combined_stas_only + [float(li)]
print combined_stas_only



########################
y_comb = 5.0;
mu_comb_p1s_stat = combined_stas_only[2]
mu_comb_m1s_stat = abs(combined_stas_only[1])
mu_comb_p1s = combined[2]
mu_comb_m1s = abs(combined[1])
gr_mu_comb_stat = TGraphAsymmErrors();
gr_mu_comb_stat.SetPoint(0,combined_stas_only[0],y_comb);
gr_mu_comb_stat.SetPointError(0,abs(combined_stas_only[1]),combined_stas_only[2],y_comb,y_comb);
#gr_mu_comb_stat.SetPointError(0,abs(combined[1]),combined[2],y_comb,y_comb);
gr_mu_comb_stat.SetLineWidth(2);
gr_mu_comb_stat.SetMarkerSize(0);
gr_mu_comb_stat.SetFillColor(ROOT.kGreen+2);

gr_mu_comb_syst = TGraphAsymmErrors();
gr_mu_comb_syst.SetPoint(0,combined[0],y_comb);
gr_mu_comb_syst.SetPointError(0,abs(combined[1]),combined[2],y_comb,y_comb);
gr_mu_comb_syst.SetLineWidth(2);
gr_mu_comb_syst.SetMarkerSize(0);
gr_mu_comb_syst.SetFillColor(ROOT.kGreen);

gr_mu_comb = TGraphAsymmErrors();
gr_mu_comb.SetPoint(0,combined[0],y_comb);
gr_mu_comb.SetPointError(0,0,0,y_comb,y_comb);
gr_mu_comb.SetLineWidth(3);
gr_mu_comb.SetLineColor(1);
gr_mu_comb.SetMarkerSize(1);
gr_mu_comb.SetMarkerColor(1);

mg = TMultiGraph();
mg.Add(gr_mu_comb, "PL")
mg.Add(gr_mu_comb_syst, "E2")
mg.Add(gr_mu_comb_stat, "E2")
for kk, key in enumerate(dprocs.keys()) :
    gr_mu = TGraphAsymmErrors()
    gr_mu.SetPoint(0,dprocs[key][0][0], dprocs[key][1]);
    gr_mu.SetPointError(0, abs(dprocs[key][0][2]), dprocs[key][0][1],0,0);
    gr_mu.SetLineWidth(3);
    gr_mu.SetLineColor(ROOT.kRed);
    gr_mu.SetMarkerStyle(21);
    gr_mu.SetMarkerSize(1.5);
    mg.Add(gr_mu, "P")
#################################

c = TCanvas("c","c",750,700);
c.SetLeftMargin(0.25);
c.SetBottomMargin(0.15);

gStyle.SetEndErrorSize(0);
mg.Draw("A");
gPad.RedrawAxis();

xmin = -2.8

mg.GetXaxis().SetLimits(xmin,5.0);
mg.GetYaxis().SetRangeUser(0,12.);
mg.GetYaxis().SetLabelSize(0);
mg.GetYaxis().SetTickSize(0);
mg.GetXaxis().SetTitle("Best fit #mu(t#bar{t}H)");
mg.GetXaxis().SetTitleOffset(1.5);
mg.GetYaxis().SetTitle("");
mg.GetYaxis().SetTitleSize(0.);
mg.GetYaxis().SetLabelSize(0.);
mg.GetYaxis().SetTickLength(0.);
mg.GetYaxis().SetTickSize(0.);
mg.Draw("A");

link = TLine(combined[0], 0, combined[0], 10.0)
link.SetLineWidth(2)
link.SetLineColor(1)
link.Draw()

luminosity=41400;
tex = TLatex();
luminosity=41400;
tex.SetTextSize(0.035);
tex.SetTextFont(61);
tex.DrawLatexNDC(0.26, 0.91, "CMS");
tex.SetTextFont(42)
tex.DrawLatexNDC(0.67, 0.91, "%.1f fb^{-1} (13 TeV)" % (41.5));
tex.SetTextSize(0.035);
tex.SetTextFont(52)
tex.DrawLatexNDC(0.36,0.91,"Preliminary")

tex2 = TLatex();
tex2.SetTextSize(0.035);
for kk, key in enumerate(dprocs.keys()) :
    tex2.DrawLatex(-2.45+xmin,dprocs[key][1]+0.3,dprocs[key][2]);
    tex2.DrawLatex(-2.45+xmin,dprocs[key][1]-0.45, "#bf{#mu = %.2f ^{+%.2f}_{-%.2f}}" % (dprocs[key][0][0], dprocs[key][0][1], abs(dprocs[key][0][2])));

mu_comb_m1s_syst = sqrt(mu_comb_m1s*mu_comb_m1s-mu_comb_m1s_stat*mu_comb_m1s_stat);
mu_comb_p1s_syst = sqrt(mu_comb_p1s*mu_comb_p1s-mu_comb_p1s_stat*mu_comb_p1s_stat);

tex2.DrawLatex(-2.0+xmin,11.,"Combined");
tex2.SetTextSize(0.04);
tex2.DrawLatex(0.5+xmin,11., "#mu = %.2f ^{+%.2f}_{-%.2f}  #bf{#left[ {}^{+%.2f}_{-%.2f}(stat.) {}^{+%.2f}_{-%.2f}(syst.)#right]}" % (combined[0], mu_comb_p1s, mu_comb_m1s, mu_comb_p1s_stat, mu_comb_m1s_stat, mu_comb_p1s_syst, mu_comb_m1s_syst));

c.SaveAs("test_mu_ttH_obs.pdf");
c.SaveAs("test_mu_ttH_obs.png");
