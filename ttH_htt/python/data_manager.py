import ROOT
import array
import math

def run_cmd(command):
  print "executing command = '%s'" % command
  p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  stdout, stderr = p.communicate()
  return stdout

def AddSystQuad(list):
    ell = []
    for element in list : ell = ell + [math.pow(element, 2.)]
    quad =  math.sqrt(sum(ell))
    return quad

def rebin_total(template, folder, fin, divideByBinWidth, name_total) :
    total_hist = fin.Get(folder+"/"+name_total)
    hist = template.Clone()
    hist.SetMarkerSize(0);
    hist.SetFillColorAlpha(12, 0.40)
    #hist.SetFillColor(1)
    #hist.SetFillStyle(3244)
    hist.SetLineWidth(0)
    hist.SetMinimum(options.minY)
    hist.SetMaximum(options.maxY)
    for ii in xrange(1, template.GetXaxis().GetNbins()+1) :
        bin_width = 1.
        if divideByBinWidth : bin_width = template.GetXaxis().GetBinWidth(ii)
        hist.SetBinContent(ii, total_hist.GetBinContent(ii)/bin_width)
        if ii == 6 and "2lss_0tau_3j" in category :
            ## just this bin went wrong on Havester combo of processes..
            ## I calculated the error by hand as quadratic sum of processes -- just for this bin
            hist.SetBinError(ii, 4.5)
        else : hist.SetBinError(ii, total_hist.GetBinError(ii)/bin_width)
    #if not hist.GetSumw2N() : hist.Sumw2()
    hist.GetXaxis().SetTitleOffset(0.55);
    hist.GetXaxis().SetLabelColor(10);
    if (options.maxY > 1000.) : hist.GetYaxis().SetTitleOffset(1.75);
    else : hist.GetYaxis().SetTitleOffset(1.35);
    hist.GetYaxis().SetTitleSize(0.050);
    hist.GetYaxis().SetLabelSize(0.056);
    hist.GetYaxis().SetTickLength(0.04);
    hist.GetXaxis().SetTickLength(0.04);
    return hist

def rebin_totalCat(template, bins, folder, fin, divideByBinWidth, name_total) :
    hist = template.Clone()
    hist.SetMarkerSize(0);
    hist.SetFillColorAlpha(12, 0.40)
    #hist.SetFillColor(1)
    #hist.SetFillStyle(3244)
    hist.SetLineWidth(0)
    for bb, bin in enumerate(bins) :
        content = 0
        error = 0
        for cat in bin :
            print folder+cat+"/"+name_total
            takeFrom = fin.Get(folder+cat+"/"+name_total)
            err = ROOT.Double()
            content += takeFrom.IntegralAndError(0,takeFrom.GetXaxis().GetNbins()+1, err, "")
            error = AddSystQuad([error, err])
        hist.SetBinContent(bb+1, content)
        hist.SetBinError(bb+1, error)
        print ("filled bin", bb+1)
    if not hist.GetSumw2N() : hist.Sumw2()
    hist.GetXaxis().SetTitleOffset(0.55);
    hist.GetXaxis().SetLabelColor(10);
    hist.GetYaxis().SetTitleOffset(1.35);
    hist.GetYaxis().SetTitleSize(0.050);
    hist.GetYaxis().SetLabelSize(0.056);
    hist.GetYaxis().SetTickLength(0.04);
    hist.GetXaxis().SetTickLength(0.04);
    return hist


def rebin_hist(template, fin, name, itemDict, divideByBinWidth) :
    print folder+"/"+name
    hist = fin.Get(folder+"/"+name)
    hist_rebin = template.Clone()
    hist_rebin.SetMarkerSize(0);
    hist_rebin.SetFillColor(itemDict[0])
    hist_rebin.SetFillStyle(itemDict[1])
    if "none" not in itemDict[2] : legend1.AddEntry(hist_rebin, itemDict[2], "f");
    if itemDict[3] == True :  hist_rebin.SetLineColor(1);
    else : hist_rebin.SetLineColor(itemDict[0]);
    for ii in xrange(1, template.GetXaxis().GetNbins()+1) :
        bin_width = 1.
        if divideByBinWidth : bin_width = template.GetXaxis().GetBinWidth(ii)
        ### remove negatives
        binContent_original = hist.GetBinContent(ii)
        binError2_original = hist.GetBinError(ii)**2;
        if binContent_original < 0. :
            print ("bin with negative entry: ", binContent_original)
            binError2_modified = binError2_original + math.pow(2, binContent_original - binContent_modified)
            if not binError2_modified >= 0. : print "Bin error negative!"
            hist_rebin.SetBinError(ii, math.sqrt(binError2_modified)/bin_width);
            hist_rebin.SetBinContent(ii, 0.)
        else :
            hist_rebin.SetBinError(ii,   hist.GetBinError(ii)/bin_width);
            hist_rebin.SetBinContent(ii, hist.GetBinContent(ii)/bin_width)
    if not hist.GetSumw2N() : hist.Sumw2()
    return hist_rebin

def doCategories(template, bins, fin, name, itemDict, divideByBinWidth) :
    hist_rebin = template.Clone()
    hist_rebin.SetMarkerSize(0);
    hist_rebin.SetFillColor(itemDict[0])
    hist_rebin.SetFillStyle(itemDict[1])
    if "none" not in itemDict[2] : legend1.AddEntry(hist_rebin, itemDict[2], "f");
    if itemDict[3] == True :  hist_rebin.SetLineColor(1);
    else : hist_rebin.SetLineColor(itemDict[0]);
    for bb, bin in enumerate(bins) :
        content = 0
        for cat in bin :
            if "3l_bt" in cat and "ZZ" in name : continue
            if "3l"  in cat and "ttH_hzg" in name : continue
            if "zpeak"  in cat and "ttH_hmm" in name : continue
            if "2lss_mm" in cat and "data_flips" in name : continue
            if "2lss_mm" in cat and "Convs" in name : continue
            if "2lss_mm" in cat and "ttH_hzg" in name : continue
            if "3j" in cat and "ttH_hzg" in name : continue
            if "2lss" in cat and "ttH_hmm" in name : continue
            print folder+cat+"/"+name
            content += fin.Get(folder+cat+"/"+name).Integral()
        hist_rebin.SetBinContent(bb+1, content)
        #print ("filled bin", bb+1)
    return hist_rebin

def rebin_dataCats(template, bins, folder, fin, fromHavester) :
    if not fromHavester :
        dataTGraph1 = ROOT.TGraphAsymmErrors()
        for bb, bin in enumerate(bins) :
            content = 0
            errorUp = 0
            errorDo = 0
            for cat in bin :
                dataTGraph = fin.Get(folder+cat+"/data")
                for ii in range(0, dataTGraph.GetN()) :
                    xp = ROOT.Double()
                    yp = ROOT.Double()
                    dataTGraph.GetPoint(ii,xp,yp)
                    content += yp
                    errorUp = AddSystQuad([errorUp, dataTGraph.GetErrorYhigh(ii)])
                    errorDo = AddSystQuad([errorDo, dataTGraph.GetErrorYlow(ii)])
            print ("done bin", bb , template.GetBinCenter(bb+1) , content)
            dataTGraph1.SetPoint(bb,       template.GetBinCenter(bb+1) , content)
            dataTGraph1.SetPointEYlow(bb,  errorDo)
            dataTGraph1.SetPointEYhigh(bb, errorUp)
            dataTGraph1.SetPointEXlow(bb,  template.GetBinWidth(bb+1)/2.)
            dataTGraph1.SetPointEXhigh(bb, template.GetBinWidth(bb+1)/2.)
    else :
        dataTGraph = fin.Get(folder+cat+"/data_obs")
        dataTGraph1 = template.Clone()
        for ii in xrange(1, template.GetXaxis().GetNbins()+1) :
            for bb, bin in enumerate(bins) :
                content = 0
                error = 0
                for cat in bin :
                    err = ROOT.Double()
                    content += takeFrom.IntegralAndError(0,takeFrom.GetXaxis().GetNbins()+1, err, "")
                    error = AddSystQuad([error, err])
            dataTGraph1.SetBinContent(ii, content)
            dataTGraph1.SetBinError(ii, error)
    dataTGraph1.SetMarkerColor(1);
    dataTGraph1.SetMarkerStyle(20);
    dataTGraph1.SetMarkerSize(1);
    dataTGraph1.SetLineColor(1);
    dataTGraph1.SetLineWidth(2);
    dataTGraph1.SetLineStyle(1)
    dataTGraph1.SetMinimum(options.minY)
    dataTGraph1.SetMaximum(options.maxY)
    return dataTGraph1

def rebin_data(template, folder, fin, fromHavester, errorBar=True) :
    # in the case errorBar=True does not draw markers,
    #in the case it is false it draws only markers but shifts the empty bins to negative
    if not fromHavester :
        dataTGraph = fin.Get(folder+"/data")
        dataTGraph1 = ROOT.TGraphAsymmErrors()
        for ii in xrange(0, template.GetXaxis().GetNbins()) :
            bin_width = 1.
            if divideByBinWidth : bin_width = template.GetXaxis().GetBinWidth(ii+1)
            xp = ROOT.Double()
            yp = ROOT.Double()
            dataTGraph.GetPoint(ii,xp,yp)
            if errorBar :
                dataTGraph1.SetPoint(ii,       template.GetBinCenter(ii+1) , yp/bin_width)
            elif yp < 0.2 : # do not show markers for empty bins
                dataTGraph1.SetPoint(ii,       template.GetBinCenter(ii+1) , (yp  - 10.0)/bin_width)
            else :
                dataTGraph1.SetPoint(ii,       template.GetBinCenter(ii+1) , yp/bin_width)
            if errorBar :
                dataTGraph1.SetPointEYlow(ii,  dataTGraph.GetErrorYlow(ii)/bin_width)
                dataTGraph1.SetPointEYhigh(ii, dataTGraph.GetErrorYhigh(ii)/bin_width)
            dataTGraph1.SetPointEYlow(ii,  dataTGraph.GetErrorYlow(ii)/bin_width)
            dataTGraph1.SetPointEYhigh(ii, dataTGraph.GetErrorYhigh(ii)/bin_width)
            # horizontal error bars
            dataTGraph1.SetPointEXlow(ii,  template.GetBinWidth(ii+1)/2.)
            dataTGraph1.SetPointEXhigh(ii, template.GetBinWidth(ii+1)/2.)
    else :
        dataTGraph = fin.Get(folder+"/data_obs")
        dataTGraph1 = template.Clone()
        for ii in xrange(1, template.GetXaxis().GetNbins()+1) :
            bin_width = 1.
            if divideByBinWidth : bin_width = template.GetXaxis().GetBinWidth(ii+1)
            dataTGraph1.SetBinContent(ii, dataTGraph.GetBinContent(ii)/bin_width)
            dataTGraph1.SetBinError(ii, dataTGraph.GetBinError(ii)/bin_width)
    dataTGraph1.SetMarkerColor(1);
    dataTGraph1.SetMarkerStyle(20);
    if errorBar :
        dataTGraph1.SetMarkerSize(0);
    else : dataTGraph1.SetMarkerSize(1);
    dataTGraph1.SetLineColor(1);
    dataTGraph1.SetLineWidth(2);
    dataTGraph1.SetLineStyle(1)
    dataTGraph1.SetMinimum(options.minY)
    dataTGraph1.SetMaximum(options.maxY)
    return dataTGraph1

def err_data(template, folder, fromHavester, errorBar=True) :
    # in the case errorBar=True does not draw markers,
    #in the case it is false it draws only markers but shifts the empty bins to negative
    if not fromHavester :
        dataTGraph = fin.Get(folder+"/data")
        dataTGraph1 = ROOT.TGraphAsymmErrors()
        for ii in xrange(0, template.GetXaxis().GetNbins()) :
            bin_width = 1.
            if divideByBinWidth : bin_width = template.GetXaxis().GetBinWidth(ii+1)
            dividend = template.GetBinContent(ii+1)*bin_width
            xp = ROOT.Double()
            yp = ROOT.Double()
            dataTGraph.GetPoint(ii,xp,yp)
            if 1> 0 : # yp > 0 :
                if dividend > 0 :
                    if yp < 0.2 and not errorBar :
                        dataTGraph1.SetPoint(ii, template.GetBinCenter(ii+1), yp/dividend - 0.1)
                    else :
                        dataTGraph1.SetPoint(ii, template.GetBinCenter(ii+1) , yp/dividend)
                else : dataTGraph1.SetPoint(ii, template.GetBinCenter(ii+1) , 0.0)
            if dividend > 0 and errorBar:
                dataTGraph1.SetPointEYlow(ii,  (dataTGraph.GetErrorYlow(ii))/dividend)
                dataTGraph1.SetPointEYhigh(ii, (dataTGraph.GetErrorYhigh(ii))/dividend)
            else :
                dataTGraph1.SetPointEYlow(ii,  0.0)
                dataTGraph1.SetPointEYhigh(ii, 0.0)
            dataTGraph1.SetPointEXlow(ii,  template.GetBinWidth(ii+1)/2.)
            dataTGraph1.SetPointEXhigh(ii, template.GetBinWidth(ii+1)/2.)
    else :
        dataTGraph = fin.Get(folder+"/data_obs")
        dataTGraph1 = template.Clone()
        for ii in xrange(1, template.GetXaxis().GetNbins()+1) :
            bin_width = 1.
            if divideByBinWidth : bin_width = template.GetXaxis().GetBinWidth(ii)
            dividend = template.GetBinContent(ii)*bin_width
            if dataTGraph.GetBinContent(ii) > 0 :
              if dividend > 0 :
                dataTGraph1.SetBinContent(ii, (dataTGraph.GetBinContent(ii)/dividend))
                dataTGraph1.SetBinError(ii,    dataTGraph.GetBinError(ii)/dividend) #
            else :
                dataTGraph1.SetBinContent(ii, -0.0)
        if not dataTGraph1.GetSumw2N() : dataTGraph1.Sumw2()
    dataTGraph1.SetMarkerColor(1);
    dataTGraph1.SetMarkerStyle(20);
    if errorBar :
        dataTGraph1.SetMarkerSize(0);
    else : dataTGraph1.SetMarkerSize(1);
    dataTGraph1.SetLineWidth(2)
    dataTGraph1.SetLineColor(1);
    dataTGraph1.SetLineStyle(1)
    return dataTGraph1

def err_dataCat(template, dataTGraph, folder, fromHavester) :
    if not fromHavester :
        dataTGraph1 = ROOT.TGraphAsymmErrors()
        for ii in xrange(0, template.GetXaxis().GetNbins()) :
            bin_width = 1.
            if divideByBinWidth : bin_width = template.GetXaxis().GetBinWidth(ii+1)
            dividend = template.GetBinContent(ii+1)*bin_width
            xp = ROOT.Double()
            yp = ROOT.Double()
            dataTGraph.GetPoint(ii,xp,yp)
            if yp > 0 :
                if dividend > 0 : dataTGraph1.SetPoint(ii, template.GetBinCenter(ii+1) , yp/dividend)
                else : dataTGraph1.SetPoint(ii, template.GetBinCenter(ii+1) , -0.7)
            else : dataTGraph1.SetPoint(ii, template.GetBinCenter(ii+1) , -0.7)
            if dividend > 0 :
                dataTGraph1.SetPointEYlow(ii,  dataTGraph.GetErrorYlow(ii)/dividend)
                dataTGraph1.SetPointEYhigh(ii, dataTGraph.GetErrorYhigh(ii)/dividend)
            else :
                dataTGraph1.SetPointEYlow(ii,  0.0)
                dataTGraph1.SetPointEYhigh(ii, 0.0)
            dataTGraph1.SetPointEXlow(ii,  template.GetBinWidth(ii+1)/2.)
            dataTGraph1.SetPointEXhigh(ii, template.GetBinWidth(ii+1)/2.)
    else :
        dataTGraph1 = template.Clone()
        for ii in xrange(1, template.GetXaxis().GetNbins()+1) :
            bin_width = 1.
            if divideByBinWidth : bin_width = template.GetXaxis().GetBinWidth(ii)
            dividend = template.GetBinContent(ii)*bin_width
            if dataTGraph.GetBinContent(ii) > 0 :
              if dividend > 0 :
                dataTGraph1.SetBinContent(ii, (dataTGraph.GetBinContent(ii)/dividend))
                dataTGraph1.SetBinError(ii,    dataTGraph.GetBinError(ii)/dividend) #
            else :
                dataTGraph1.SetBinContent(ii, -0.0)
        if not dataTGraph1.GetSumw2N() : dataTGraph1.Sumw2()
    dataTGraph1.SetMarkerColor(1);
    dataTGraph1.SetMarkerStyle(20);
    dataTGraph1.SetMarkerSize(1);
    dataTGraph1.SetLineColor(1);
    dataTGraph1.SetLineWidth(2);
    dataTGraph1.SetLineStyle(1)
    return dataTGraph1


def do_hist_total_err(template, labelX, name_total, category) :
    total_hist = fin.Get(folder+"/"+name_total)
    hist_total_err = template.Clone()
    hist_total_err.GetYaxis().SetTitle("Data/pred.") #"#frac{Data - Expectation}{Expectation}");
    hist_total_err.GetXaxis().SetTitleOffset(1.1);
    hist_total_err.GetYaxis().SetTitleOffset(0.8);
    hist_total_err.GetXaxis().SetTitleSize(0.105);
    hist_total_err.GetYaxis().SetTitleSize(0.10);
    hist_total_err.GetYaxis().SetLabelSize(0.105);
    hist_total_err.GetXaxis().SetLabelSize(0.10);
    hist_total_err.GetYaxis().SetTickLength(0.04);
    hist_total_err.GetXaxis().SetLabelColor(1);
    hist_total_err.GetXaxis().SetTitle(labelX)
    #hist_total_err.SetMarkerSize(0);
    hist_total_err.SetFillColorAlpha(12, 0.40)
    #hist_total_err.SetFillColorAlpha(12, 0.80)
    #hist_total_err.SetFillStyle(3244)
    hist_total_err.SetLineWidth(2)
    hist_total_err.SetMarkerSize(0);
    minYerr = -0.6
    maxYerr = 2.85
    if "3l_1tau" in category :
         minYerr = 0.0
         maxYerr = 5.35
    if "2lss_1tau" in category :
        minYerr = 0.0
        maxYerr = 2.75
    if "2l_2tau" in category :
        minYerr = 0.0
        maxYerr = 2.75
    if "1l_2tau" in category :
        minYerr = 0.59
        maxYerr = 1.87
    if "2lss_0tau" in category :
        minYerr = 0.501
        maxYerr = 1.59
    if "3l_0tau" in category :
        minYerr = 0.501
        maxYerr = 1.59
    if "4l" in category :
        minYerr = 0.601
        maxYerr = 2.19
    hist_total_err.SetMinimum(minYerr)
    hist_total_err.SetMaximum(maxYerr)
    for bin in xrange(0, hist_total_err.GetXaxis().GetNbins()) :
        hist_total_err.SetBinContent(bin+1, 1)
        if total_hist.GetBinContent(bin+1) > 0. :
            if bin == 5 and "2lss_0tau" in category :
                ## just this bin went wrong on Havester combo of processes..
                ## I calculated the error by hand as quadratic sum of processes -- just for this bin
                hist_total_err.SetBinError(bin+1, 4.5/total_hist.GetBinContent(bin+1))
            else : hist_total_err.SetBinError(bin+1, total_hist.GetBinError(bin+1)/total_hist.GetBinContent(bin+1))
        else : hist_total_err.SetBinError(bin+1, 0.01)
    return hist_total_err

def do_hist_total_errCats(templatebin, bins, binlabels, labelX, name_total, category) :
    hist_total_err = template.Clone()
    hist_total_err.GetYaxis().SetTitle("Data/pred.") #"#frac{Data - Expectation}{Expectation}");
    hist_total_err.GetXaxis().SetLabelOffset(0.015);
    hist_total_err.GetYaxis().SetTitleOffset(0.8);
    hist_total_err.GetXaxis().SetTitleSize(0.105);
    hist_total_err.GetYaxis().SetTitleSize(0.10);
    hist_total_err.GetYaxis().SetLabelSize(0.105);
    hist_total_err.GetXaxis().SetLabelSize(0.15);
    hist_total_err.GetYaxis().SetTickLength(0.04);
    hist_total_err.GetXaxis().SetLabelColor(1);
    hist_total_err.GetXaxis().SetTitle("")
    hist_total_err.GetXaxis().SetNdivisions(0)
    hist_total_err.SetMarkerSize(0);
    hist_total_err.SetFillColorAlpha(12, 0.40)
    hist_total_err.SetLineWidth(2)
    hist_total_err.SetMarkerSize(0);
    minYerr = -0.6
    maxYerr = 2.85
    if "3l" in category :
        minYerr = 0.701
        maxYerr = 1.39
    if "2lss" in category :
        minYerr = 0.701
        maxYerr = 1.39
    hist_total_err.SetMinimum(minYerr)
    hist_total_err.SetMaximum(maxYerr)
    for bin in xrange(0, hist_total_err.GetXaxis().GetNbins()) :
        hist_total_err.GetXaxis().SetBinLabel(bin+1, binlabels[bin])
        hist_total_err.SetBinContent(bin+1, 1.)
        if templatebin.GetBinContent(bin+1) > 0. :
            hist_total_err.SetBinError(bin+1, templatebin.GetBinError(bin+1)/templatebin.GetBinContent(bin+1))
        else : hist_total_err.SetBinError(bin+1, 0.01)
    return hist_total_err


def addLabel_CMS_preliminary() :

    x0 = 0.2
    y0 = 0.953
    ypreliminary = 0.95
    xlumi = 0.67
    label_cms = ROOT.TPaveText(x0, y0, x0 + 0.0950, y0 + 0.0600, "NDC");
    label_cms.AddText("CMS");
    label_cms.SetTextFont(61);
    label_cms.SetTextAlign(13);
    label_cms.SetTextSize(0.0575);
    label_cms.SetTextColor(1);
    label_cms.SetFillStyle(0);
    label_cms.SetBorderSize(0);
    label_preliminary = ROOT.TPaveText(x0 + 0.1050, ypreliminary - 0.0010, x0 + 0.2950, ypreliminary + 0.0500, "NDC");
    label_preliminary.AddText("Preliminary");
    label_preliminary.SetTextFont(52);
    label_preliminary.SetTextAlign(13);
    label_preliminary.SetTextSize(0.050);
    label_preliminary.SetTextColor(1);
    label_preliminary.SetFillStyle(0);
    label_preliminary.SetBorderSize(0);
    label_luminosity = ROOT.TPaveText(xlumi, y0 + 0.0047, xlumi + 0.1900, y0 + 0.0510, "NDC");
    label_luminosity.AddText("41.5 fb^{-1} (13 TeV)");
    label_luminosity.SetTextFont(42);
    label_luminosity.SetTextAlign(13);
    label_luminosity.SetTextSize(0.045);
    label_luminosity.SetTextColor(1);
    label_luminosity.SetFillStyle(0);
    label_luminosity.SetBorderSize(0);

    return [label_cms, label_preliminary, label_luminosity]

def finMaxMin(histSource) :
    file = TFile(histSource+".root","READ");
    file.cd()
    hSum = TH1F()
    for keyO in file.GetListOfKeys() :
       obj =  keyO.ReadObj()
       if type(obj) is not TH1F : continue
       hSumDumb = obj.Clone()
       if not hSum.Integral()>0 : hSum=hSumDumb
       else : hSum.Add(hSumDumb)
    return [
    [hSum.GetBinLowEdge(1),  hSum.GetBinCenter(hSum.GetNbinsX())+hSum.GetBinWidth(hSum.GetNbinsX())/2.],
    [hSum.GetBinLowEdge(hSum.FindFirstBinAbove(0.0)),  hSum.GetBinCenter(hSum.FindLastBinAbove (0.0))+hSum.GetBinWidth(hSum.FindLastBinAbove (0.0))/2.]]

def getQuantiles(histoP,ntarget,xmax) :
    histoP.Scale(1./histoP.Integral());
    histoP.GetCumulative()#.Draw();
    histoP.GetXaxis().SetRangeUser(0.,1.)
    histoP.GetYaxis().SetRangeUser(0.,1.)
    histoP.SetMinimum(0.0)
    xq= array.array('d', [0.] * (ntarget+1))
    yq= array.array('d', [0.] * (ntarget+1))
    yqbin= array.array('d', [0.] * (ntarget+1)) # +2 if firsrt is not zero
    for  ii in range(0,ntarget) : xq[ii]=(float(ii)/(ntarget))
    xq[ntarget]=0.999999999
    histoP.GetQuantiles(ntarget,yq,xq)
    line = [None for point in range(ntarget)]
    line2 = [None for point in range(ntarget)]
    for  ii in range(1,ntarget+1) : yqbin[ii]=yq[ii]
    yqbin[ntarget]=xmax # +1 if first is not 0
    #print yqbin
    return yqbin

def rebinRegular(local, histSource, nbin, BINtype) :
    minmax = finMaxMin(local+"/"+histSource)
    # to know the real min and max of the distribution
    xmindef=minmax[1][0]
    xmaxdef=minmax[1][1]
    if BINtype=="ranged" :
        xmin=minmax[1][0]
        xmax=minmax[1][1]
    else :
        xmin=minmax[0][0]
        xmax=minmax[0][1]
    file = TFile(local+"/"+histSource+".root","READ");
    file.cd()
    histograms=[]
    histograms2=[]
    h2 = TH1F()
    hFakes = TH1F()
    hSumAll = TH1F()
    for nkey, keyO in enumerate(file.GetListOfKeys()) :
       obj =  keyO.ReadObj()
       if type(obj) is not TH1F : continue
       h2 = obj.Clone();
       factor=1.
       if  not h2.GetSumw2N() : h2.Sumw2()
       histograms.append(h2.Clone())
       if keyO.GetName() == "fakes_data" : hFakes=obj.Clone()
       if keyO.GetName() == "fakes_data" or keyO.GetName() =="TTZ" or keyO.GetName() =="TTW" or keyO.GetName() =="TTWW" or keyO.GetName() == "EWK" or keyO.GetName() == "tH" or keyO.GetName() == "Rares" :
           hSumDumb2 = obj
           if not hSumAll.Integral()>0 : hSumAll=hSumDumb2.Clone()
           else : hSumAll.Add(hSumDumb2)
    name=histSource+"_"+str(nbin)+"bins_"+BINtype
    fileOut  = TFile(local+"/"+name+".root", "recreate");
    histo = TH1F()
    for nn, histogram in enumerate(histograms) :
        histogramCopy=histogram.Clone()
        nameHisto=histogramCopy.GetName()
        histogram.SetName(histogramCopy.GetName()+"_"+str(nn)+BINtype)
        histogramCopy.SetName(histogramCopy.GetName()+"Copy_"+str(nn)+BINtype)
        if BINtype=="ranged" or BINtype=="regular" :
            histo= TH1F( nameHisto, nameHisto , nbin , xmin , xmax)
        elif "quantile" in BINtype :
            if "Fakes" in BINtype : nbinsQuant=getQuantiles(hFakes,nbin,xmax)
            if "All" in BINtype : nbinsQuant=getQuantiles(hSumAll ,nbin,xmax)
            histo=TH1F(nameHisto, nameHisto , nbin , nbinsQuant) # nbins+1 if first is zero
        else :
            print "not valid bin type"
            return
        histo.Sumw2()
        for place in range(0,histogramCopy.GetNbinsX() + 1) :
            content =      histogramCopy.GetBinContent(place)
            binErrorCopy = histogramCopy.GetBinError(place);
            newbin =       histo.GetXaxis().FindBin(histogramCopy.GetXaxis().GetBinCenter(place))
            binError =     histo.GetBinError(newbin);
            contentNew =   histo.GetBinContent(newbin)
            histo.SetBinContent(newbin, content+contentNew)
            histo.SetBinError(newbin, sqrt(binError*binError+binErrorCopy*binErrorCopy))
        histo.Write()
    fileOut.Write()
    print (local+"/"+name+".root"+" created")
    print ("calculated between: ",xmin,xmax)
    print ("there is MC data between: ",xmindef,xmaxdef)
    return name

def ReadLimits(limits_output):
    f = open(limits_output, 'r+')
    lines = f.readlines() # get all lines as a list (array)
    for line in  lines:
      l = []
      tokens = line.split()
      if "Expected  2.5%"  in line : do2=float(tokens[4])
      if "Expected 16.0%:" in line : do1=float(tokens[4])
      if "Expected 50.0%:" in line : central=float(tokens[4])
      if "Expected 84.0%:" in line : up1=float(tokens[4])
      if "Expected 97.5%:" in line : up2=float(tokens[4])
    return [do2,do1,central,up1,up2]


###########################################################
# doYields



def PrintTables(cmb, uargs, filey, blinded, labels, type, ColapseCat = []):

    c_cat = []
    sum_proc = []
    err_sum_proc = []
    for label in labels :
        c_cat = c_cat  + [cmb.cp().bin(['ttH_'+label])]
        sum_proc = sum_proc + [0]
        err_sum_proc = err_sum_proc + [0]

    header = r'\begin{tabular}{|l|'
    bottom = r'Observed data & '
    for ll in xrange(len(labels)) :
        header = header + r'r@{$ \,\,\pm\,\, $}l|'
        if blinded : bottom = bottom + r' \multicolumn{2}{c|}{$-$} '
        else : bottom = bottom + r' \multicolumn{2}{c|}{$%g$} ' % (c_cat[ll].cp().GetObservedRate())
        if ll == len(labels) - 1 : bottom = bottom + r' \\'
        else : bottom = bottom + ' &'
    header = header +"} \n"
    bottom = bottom +"\n"
    filey.write(header)

    if type == 'tau' :
        conversions = "conversions"
        flips = 'flips'
        fakes_data = 'fakes_data'

        filey.write(r"""
        \hline
        Process & \multicolumn{2}{c|}{$1\Plepton + 2\tauh$} & \multicolumn{2}{c|}{$2\Plepton + 2\tauh$} & \multicolumn{2}{c|}{$3\Plepton + 1\tauh$} & \multicolumn{2}{c|}{$2\Plepton ss + 1\tauh$} \\
        \hline
        \hline"""+"\n")

    if type == 'multilep2lss' :
        conversions = "Convs"
        flips = 'data_flips'
        fakes_data = 'data_fakes'

        filey.write(r"""
        \hline
        Process & \multicolumn{20}{c|}{$2\Plepton ss$}  \\ \hline
        B-tag  & \multicolumn{4}{c|}{no req.}  & \multicolumn{8}{c|}{Loose}  & \multicolumn{8}{c|}{Tight}   \\ \hline
        Leptons  & \multicolumn{4}{c|}{$ee$} & \multicolumn{4}{c|}{$em$} & \multicolumn{4}{c|}{$mm$} & \multicolumn{4}{c|}{$em$} & \multicolumn{4}{c|}{$mm$}  \\ \hline
        Signal & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} \\ \hline
        \hline
        \hline"""+"\n")

    if type == 'multilepCR2lss' :
        conversions = "Convs"
        flips = 'flips_data'
        fakes_data = 'data_fakes'

        filey.write(r"""
        \hline
        Process & \multicolumn{20}{c|}{$2\Plepton ss$}  \\ \hline
        B-tag   & \multicolumn{4}{c|}{no req.} & \multicolumn{8}{c|}{Loose}  & \multicolumn{8}{c|}{Tight}  \\ \hline
        Leptons  & \multicolumn{4}{c|}{$ee$} & \multicolumn{4}{c|}{$em$}  & \multicolumn{4}{c|}{$mm$} & \multicolumn{4}{c|}{$em$}  & \multicolumn{4}{c|}{$mm$} \\ \hline
        Signal & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} \\ \hline
        \hline
        \hline"""+"\n")

    if type == 'multilepCR3l4l' :
        conversions = "Convs"
        flips = 'flips_data'
        fakes_data = 'data_fakes'

        filey.write(r"""
        \hline
        Process & \multicolumn{10}{c|}{$3\Plepton$} & \multicolumn{2}{c|}{$4\Plepton$}  \\ \hline
        CR & \multicolumn{8}{c|}{$\PcZ$-peak} & \multicolumn{2}{c|}{$WZ$ enrich.}  & \multicolumn{2}{c|}{$ZZ$ enrich.} \\ \hline
        B-tag  & \multicolumn{4}{c|}{Loose}  & \multicolumn{4}{c|}{Tight}  & \multicolumn{4}{c|}{no req.}   \\ \hline
        Signal & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} & & \multicolumn{4}{c|}{no req.} \\ \hline
        \hline
        \hline"""+"\n")

    if type == 'multilep3l4l' :
        conversions = "Convs"
        flips = 'flips_data'
        fakes_data = 'data_fakes'

        filey.write(r"""
        \hline
        Process &  \multicolumn{8}{c|}{$3\Plepton$} & \multicolumn{2}{c|}{$4\Plepton + 1\tauh$}  \\ \hline
        B-tag  & \multicolumn{4}{c|}{no req.}  & \multicolumn{8}{c|}{Loose}  & \multicolumn{8}{c|}{Tight}  & \multicolumn{4}{c|}{Loose}  & \multicolumn{4}{c|}{Tight} & \multicolumn{2}{c|}{no req.}  \\ \hline
        Signal & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} & \multicolumn{2}{c|}{$-$} & \multicolumn{2}{c|}{$+$} \\ \hline
        \hline
        \hline"""+"\n")

    signals = [
        'ttH_hzz',
        'ttH_hww',
        'ttH_htt',
        'ttH_hmm',
        'ttH_hzg'
        ]

    TTWX = [
        'TTW',
        'TTWW'
        ]

    if 'multilep' in type :
        tH = [
        'tHW_htt',
        'tHq_htt',
        'tHW_hww',
        'tHq_hww',
        'tHW_hzz',
        'tHq_hzz'
        ]
        signalslabel_tH = [
            r'$\cPqt\PHiggs q$ $\PHiggs \to \Pgt\Pgt$& ',
            r'$\cPqt\PHiggs\PW$ $\PHiggs \to \Pgt\Pgt$& ',
            r'$\cPqt\PHiggs q$ $\PHiggs \to \PW\PW$ & ',
            r'$\cPqt\PHiggs\PW$ $\PHiggs \to \PW\PW$ & ',
            r'$\cPqt\PHiggs q$ $\PHiggs \to \cPZ\cPZ$  & ',
            r'$\cPqt\PHiggs\PW$ $\PHiggs \to \cPZ\cPZ$  & '
            ]

    if type == 'tau' :
        tH = [
        'tHq',
        'tHW'
        ]
        signalslabel_tH = [
            r'$\cPqt\PHiggs q$ & ',
            r'$\cPqt\PHiggs\PW$ & '
            ]

    EWK = [
        'ZZ',
        'WZ'
    ]

    singleCompMC = []
    if type == 'tau' : singleCompMC = singleCompMC + ['EWK']
    singleCompMC = singleCompMC + [
        'TTZ',
        fakes_data,
        conversions,
        flips,
        'Rares'
    ]

    singleCompMClabels = []
    if type == 'tau' : singleCompMClabels = singleCompMClabels + ['$\PW\cPZ + \cPZ\cPZ$']
    singleCompMClabels = singleCompMClabels + [
        '$\cPqt\cPaqt\cPZ$',
        'Misidentified',
        'Conversions',
        'signal flip',
        'Other'
    ]

    if type == 'tau' : listTosum = [signals, TTWX, tH]
    if 'multilep' in type : listTosum = [signals, TTWX, tH, EWK]
    for todo in listTosum :

        sigsum = [0.0 for i in xrange(len(labels))]
        sigsumErr = [0.0 for i in xrange(len(labels))]

        if todo == signals :
            linesigsum = 'ttH (sum) &'
            signalslabel = [
                r'$\cPqt\cPaqt\PHiggs$, $\PHiggs \to \cPZ\cPZ$ & ',
                r'$\cPqt\cPaqt\PHiggs$, $\PHiggs \to \PW\PW$ & ',
                r'$\cPqt\cPaqt\PHiggs$, $\PHiggs \to \Pgt\Pgt$ & ',
                r'$\cPqt\cPaqt\PHiggs$, $\PHiggs \to \mu\mu$ & ',
                r'$\cPqt\cPaqt\PHiggs$, $\PHiggs \to \cPZ\gamma$& ',
                ]
        elif todo == TTWX :
            linesigsum = 'ttW + ttWW &'
            signalslabel = [
                r'$\cPqt\cPaqt\PW$ & ',
                r'$\cPqt\cPaqt\PW\PW$ & '
                ]
        elif todo == tH :
            linesigsum = '$\cPqt\PHiggs$ (sum) &'
            signalslabel = signalslabel_tH
        if todo == EWK :
            linesigsum = '$\PW\cPZ + \cPZ\cPZ$ &'
            signalslabel = [
                r'$\cPZ\cPZ$ & ',
                r'$\PW\cPZ$ & '
                ]

        for ss, signal in enumerate(todo) :
            linesig = signalslabel[ss]
            for ll, label in enumerate(labels) :
                if "2lss_1tau" in label or  "3l_1tau" in label :
                    thissig = c_cat[ll].cp().process([signal+'_faketau']).GetRate() + c_cat[ll].cp().process([signal+'_gentau']).GetRate()
                    thissigErr = AddSystQuad({c_cat[ll].cp().process([signal+'_faketau']).GetUncertainty(*uargs), c_cat[ll].cp().process([signal+'_gentau']).GetUncertainty(*uargs)})
                else :
                    thissig = c_cat[ll].cp().process([signal]).GetRate()
                    thissigErr = c_cat[ll].cp().process([signal]).GetUncertainty(*uargs)
                if not thissig + thissigErr < 0.05:
                    linesig = linesig + ' $%.2f$ & $%.2f$ ' % (thissig, thissigErr)
                else : linesig = linesig + r' \multicolumn{2}{c|}{$< 0.05$} '
                if ll == len(labels) - 1 : linesig = linesig + r' \\'
                else : linesig = linesig + ' &'
                sigsum[ll] = sigsum[ll] + thissig
                sigsumErr[ll] = AddSystQuad({sigsumErr[ll], thissigErr})
                sum_proc[ll] = sum_proc[ll] + thissig
                err_sum_proc[ll] = AddSystQuad({err_sum_proc[ll], thissigErr})
            filey.write(linesig+"\n")
        filey.write(r'\hline'+"\n")

        for ll, label in enumerate(labels) :
            if not sigsum[ll] +  sigsumErr[ll] < 0.05:
                linesigsum = linesigsum + ' $%.2f$ & $%.2f$ ' % (sigsum[ll], sigsumErr[ll])
            else :  linesigsum = linesigsum + r' \multicolumn{2}{c|}{$< 0.05$} '
            if ll == len(labels) - 1 : linesigsum = linesigsum + r' \\'
            else : linesigsum = linesigsum + ' &'
        filey.write(linesigsum+"\n")
        filey.write(r'\hline'+"\n")

    for ss, signal in enumerate(singleCompMC) :
        lineTTZ = singleCompMClabels[ss]+' & '
        for ll, label in enumerate(labels) :
            if ("2lss_1tau" in label or  "3l_1tau" in label ) and signal not in ['fakes_data', 'flips']:
                thissig = c_cat[ll].cp().process([signal+'_faketau']).GetRate() + c_cat[ll].cp().process([signal+'_gentau']).GetRate()
                thissigErr = AddSystQuad({c_cat[ll].cp().process([signal+'_faketau']).GetUncertainty(*uargs), c_cat[ll].cp().process([signal+'_gentau']).GetUncertainty(*uargs)})
            else :
                thissig = c_cat[ll].cp().process([signal]).GetRate()
                thissigErr = c_cat[ll].cp().process([signal]).GetUncertainty(*uargs)
            if not thissig + thissigErr < 0.05:
                lineTTZ = lineTTZ + ' $%.2f$ & $%.2f$ ' % (thissig, thissigErr)
            else : lineTTZ = lineTTZ + r' \multicolumn{2}{c|}{$< 0.05$} '
            sum_proc[ll] = sum_proc[ll] + thissig
            err_sum_proc[ll] = AddSystQuad({err_sum_proc[ll], thissigErr})
            if ll == len(labels) - 1 : lineTTZ = lineTTZ + r' \\ '+"\n"
            else : lineTTZ = lineTTZ + ' &'
        filey.write(lineTTZ+"\n")

    lineSUM = r'\hline\hline'+"\n"+' SM expectation & '
    for ll, label in enumerate(labels) :
        if not sum_proc[ll] + err_sum_proc[ll] < 0.05:
            lineSUM = lineSUM + ' $%.2f$ & $%.2f$ ' % (sum_proc[ll] , err_sum_proc[ll] )
        else : lineSUM = lineSUM + r' \multicolumn{2}{c|}{$< 0.05$} '
        if ll == len(labels) - 1 : lineSUM = lineSUM + r' \\ '+"\n"
        else : lineSUM = lineSUM + ' &'
    filey.write(lineSUM+"\n")

    filey.write(r'\hline'+"\n")
    filey.write(bottom)
    filey.write(r"""\hline
    \end{tabular}"""+"\n")


def setTDRStyle():
  tdrStyle =  ROOT.TStyle("tdrStyle","Style for P-TDR")

   #for the canvas:
  tdrStyle.SetCanvasBorderMode(0)
  tdrStyle.SetCanvasColor(ROOT.kWhite)
  tdrStyle.SetCanvasDefH(600) #Height of canvas
  tdrStyle.SetCanvasDefW(600) #Width of canvas
  tdrStyle.SetCanvasDefX(0)   #POsition on screen
  tdrStyle.SetCanvasDefY(0)


  tdrStyle.SetPadBorderMode(0)
  #tdrStyle.SetPadBorderSize(Width_t size = 1)
  tdrStyle.SetPadColor(ROOT.kWhite)
  tdrStyle.SetPadGridX(False)
  tdrStyle.SetPadGridY(False)
  tdrStyle.SetGridColor(0)
  tdrStyle.SetGridStyle(3)
  tdrStyle.SetGridWidth(1)

#For the frame:
  tdrStyle.SetFrameBorderMode(0)
  tdrStyle.SetFrameBorderSize(1)
  tdrStyle.SetFrameFillColor(0)
  tdrStyle.SetFrameFillStyle(0)
  tdrStyle.SetFrameLineColor(1)
  tdrStyle.SetFrameLineStyle(1)
  tdrStyle.SetFrameLineWidth(1)

#For the histo:
  #tdrStyle.SetHistFillColor(1)
  #tdrStyle.SetHistFillStyle(0)
  tdrStyle.SetHistLineColor(1)
  tdrStyle.SetHistLineStyle(0)
  tdrStyle.SetHistLineWidth(1)
  #tdrStyle.SetLegoInnerR(Float_t rad = 0.5)
  #tdrStyle.SetNumberContours(Int_t number = 20)

  tdrStyle.SetEndErrorSize(2)
  #tdrStyle.SetErrorMarker(20)
  #tdrStyle.SetErrorX(0.)

  tdrStyle.SetMarkerStyle(20)

#For the fit/function:
  tdrStyle.SetOptFit(1)
  tdrStyle.SetFitFormat("5.4g")
  tdrStyle.SetFuncColor(2)
  tdrStyle.SetFuncStyle(1)
  tdrStyle.SetFuncWidth(1)

#For the date:
  tdrStyle.SetOptDate(0)
  # tdrStyle.SetDateX(Float_t x = 0.01)
  # tdrStyle.SetDateY(Float_t y = 0.01)

# For the statistics box:
  tdrStyle.SetOptFile(0)
  tdrStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
  tdrStyle.SetStatColor(ROOT.kWhite)
  tdrStyle.SetStatFont(42)
  tdrStyle.SetStatFontSize(0.025)
  tdrStyle.SetStatTextColor(1)
  tdrStyle.SetStatFormat("6.4g")
  tdrStyle.SetStatBorderSize(1)
  tdrStyle.SetStatH(0.1)
  tdrStyle.SetStatW(0.15)
  # tdrStyle.SetStatStyle(Style_t style = 1001)
  # tdrStyle.SetStatX(Float_t x = 0)
  # tdrStyle.SetStatY(Float_t y = 0)

# Margins:
  tdrStyle.SetPadTopMargin(0.05)
  tdrStyle.SetPadBottomMargin(0.13)
  tdrStyle.SetPadLeftMargin(0.16)
  tdrStyle.SetPadRightMargin(0.02)

# For the Global title:

  tdrStyle.SetOptTitle(0)
  tdrStyle.SetTitleFont(42)
  tdrStyle.SetTitleColor(1)
  tdrStyle.SetTitleTextColor(1)
  tdrStyle.SetTitleFillColor(10)
  tdrStyle.SetTitleFontSize(0.05)
  # tdrStyle.SetTitleH(0) # Set the height of the title box
  # tdrStyle.SetTitleW(0) # Set the width of the title box
  # tdrStyle.SetTitleX(0) # Set the position of the title box
  # tdrStyle.SetTitleY(0.985) # Set the position of the title box
  # tdrStyle.SetTitleStyle(Style_t style = 1001)
  # tdrStyle.SetTitleBorderSize(2)

# For the axis titles:

  tdrStyle.SetTitleColor(1, "XYZ")
  tdrStyle.SetTitleFont(42, "XYZ")
  tdrStyle.SetTitleSize(0.06, "XYZ")
  # tdrStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
  # tdrStyle.SetTitleYSize(Float_t size = 0.02)
  tdrStyle.SetTitleXOffset(0.9)
  tdrStyle.SetTitleYOffset(1.25)
  # tdrStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset

# For the axis labels:

  tdrStyle.SetLabelColor(1, "XYZ")
  tdrStyle.SetLabelFont(42, "XYZ")
  tdrStyle.SetLabelOffset(0.007, "XYZ")
  tdrStyle.SetLabelSize(0.05, "XYZ")

# For the axis:

  tdrStyle.SetAxisColor(1, "XYZ")
  tdrStyle.SetStripDecimals(True)
  tdrStyle.SetTickLength(0.03, "XYZ")
  tdrStyle.SetNdivisions(510, "XYZ")
  tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
  tdrStyle.SetPadTickY(1)

# Change for log plots:
  tdrStyle.SetOptLogx(0)
  tdrStyle.SetOptLogy(0)
  tdrStyle.SetOptLogz(0)

# Postscript options:
  tdrStyle.SetPaperSize(20.,20.)
  # tdrStyle.SetLineScalePS(Float_t scale = 3)
  # tdrStyle.SetLineStyleString(Int_t i, const char* text)
  # tdrStyle.SetHeaderPS(const char* header)
  # tdrStyle.SetTitlePS(const char* pstitle)

  # tdrStyle.SetBarOffset(Float_t baroff = 0.5)
  # tdrStyle.SetBarWidth(Float_t barwidth = 0.5)
  # tdrStyle.SetPaintTextFormat(const char* format = "g")
  # tdrStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
  # tdrStyle.SetTimeOffset(Double_t toffset)
  # tdrStyle.SetHistMinimumZero(kTRUE)

  tdrStyle.SetHatchesLineWidth(5)
  tdrStyle.SetHatchesSpacing(0.05)

  tdrStyle.cd()
