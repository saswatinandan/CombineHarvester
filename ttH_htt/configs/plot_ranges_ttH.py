def options_plot_ranges () : 
    info_channel = {
        "2lss_0tau" : { "minY" : -5., "maxY" :  115., "minYerr": 0.501, "maxYerr" : 1.59, "useLogPlot" : False}, 
        "ttWctrl"   : { "minY" : -5., "maxY" :  115., "minYerr": -0.6, "maxYerr" : 2.85, "useLogPlot" : False},
        "2lss_1tau" : { "minY" : -0.9, "maxY" :  14., "minYerr":  0.0, "maxYerr" : 2.75, "useLogPlot" : False},
        "3l_0tau"   : { "minY" : -6, "maxY" :  229., "minYerr": 0.501, "maxYerr" : 1.59, "useLogPlot" : False},
        "ttZctrl"   : { "minY" : -6, "maxY" :  229., "minYerr": -0.6, "maxYerr" : 2.85, "useLogPlot" : False},
        "2l_2tau"   : { "minY" : -0.35, "maxY" :  14., "minYerr":  0.0, "maxYerr" : 2.75, "useLogPlot" : False},
        "3l_1tau"   : { "minY" : -0.2, "maxY" :  6.9, "minYerr":  0.0, "maxYerr" : 5.35, "useLogPlot" : False}, 
        "1l_2tau"   : { "minY" : 0.07, "maxY" :  5000., "minYerr": 0.59, "maxYerr" : 1.87, "useLogPlot" : True},
        "2los_1tau" : { "minY" : 0.07, "maxY" :  5000., "minYerr": -0.6, "maxYerr" : 2.85, "useLogPlot" : False},
        "0l_2tau"   : { "minY" : 0.07, "maxY" :  5000., "minYerr": -0.6, "maxYerr" : 2.85, "useLogPlot" : False},
        "1l_1tau"   : { "minY" : 0.07, "maxY" :  5000., "minYerr": -0.6, "maxYerr" : 2.85, "useLogPlot" : False},
        "WZctrl"    : { "minY" : 0.07, "maxY" :  5000., "minYerr": -0.6, "maxYerr" : 2.85, "useLogPlot" : False},
        "4l_0tau"   : { "minY" : -0.35, "maxY" :  13.9, "minYerr": 0.601, "maxYerr" : 2.19, "useLogPlot" : False},
        "ZZctrl"    : { "minY" : -0.35, "maxY" :  13.9, "minYerr": -0.6, "maxYerr" : 2.85, "useLogPlot" : False},
    }
    return info_channel
