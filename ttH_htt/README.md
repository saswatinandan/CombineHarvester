The script on  in this repository manipulate the output of the KBFI analysis into the format necessary for the statistical analysis.

To run the scripts as executable (as the exemple bellow) you may compile the repository with

```
scram b -j 8
```

The output of the KBFI analysis jobs ("prepareDatacards") is comverted into .txt/.root combine datacards as the bellow example:

```
WriteDatacards.py  --inputShapes /absolute/or/relative/path/to/prepareDatacards_favourite.root --channel 1l_2tau --cardFolder /absolute/or/relative/path/of/folder/to/results --output_file /absolute/or/relative/name_without_txt_sufix --noX_prefix
```

Please check it out the extensive list of command line descriptions and further options by running on thie repository:

```
python scripts/WriteDatacards.py -h
```

The options for common and specific systematics are found on. 

```
configs/list_syst.py
```

- In the way that this file is loaded on the main script there is no need to recompile the folder if you change/add a systematics entry.

- the specificities of each channel are entered as dictionary entries, eg here and here -- the structure/usage of those are expected to be self explanatory in the case you need to implement a new entry.

#P.s.: 
Those are certifyed to work for all the ttH channels, 
but the same core scripts should work as well for the HH analysis if one adds to the configs. This will be done in a posterior stage.

==========================================================

With the intention of testing locally if the datacard production was succesfull we also have a script to draw prefit/postfit plots. 

```
makePostFitPlots_FromCombine.py --inputDatacard /absolute/or/relative/path/to/prepareDatacards_favourite.root --odir  /absolute/or/relative/path/of/folder/to/results --channel 2lss_1tau
```

#IMPORTANT: 
To run the latter it is imperative that you started your ssh session with at least `-Y` option (prefereable with `-XY`): e.g. `ssh -Y user@server.ser`

Please check it out the extensive list of command line descriptions and further options by running on thie repository:

```
python scripts/makePostFitPlots_FromCombine.py -h
```

The options for color code of the plots (global to each analysis ttH/HH) are found on 

```
configs/plot_options.py
```

The options for ranges of the plots (specific for each channel) are found on (at the moment only ttH subchannels are listed)

```
configs/plot_ranges_ttH.py
```

#Note:
The input of this script ia a KBFI format "prepareDatacards", as this calls inside the `WriteDatacards.py`, followed by a couple more of combine commands necessary to do prefit/postfit plots in a self contained naming convention cascade.

==========================================================

#WARNING: 
For the final combined results/plots/tables on the ttH analysis please refer to this repository, that takes as inputs only combine datacards (.txt) and is in line with the latest fit and plot options agreed for legacy paper.


