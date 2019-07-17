#!/usr/bin/env python
import os, shlex
from subprocess import Popen, PIPE

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--inputShapes",    type="string",       dest="inputShapes", help="Full path of prepareDatacards.root")
parser.add_option("--channel",        type="string",       dest="channel",     help="Channel to assume (to get the correct set of syst)")
parser.add_option("--cardFolder",     type="string",       dest="cardFolder",  help="Folder where to save the datacards (relative or full).\n Default: teste_datacards",  default="teste_datacards")
parser.add_option("--shapeSyst",      action="store_true", dest="shapeSyst",   help="Do apply the shape systematics. Default: False", default=False)
parser.add_option("--era",            type="int",          dest="era",         help="Era to consider (important for list of systematics). Default: 2017",  default=2017)
(options, args) = parser.parse_args()

func_file = os.environ["CMSSW_BASE"] + "/src/CombineHarvester/ttH_htt/python/data_manager.py"
execfile(func_file)

tHweights = [
  {"kt" : -1.0, "kv" : 1.0, "idx" : -1}, # the default (i.e. no weight)
  {"kt" : -3.0, "kv" : 1.0, "idx" : 0},
  {"kt" : -2.0, "kv" : 1.0, "idx" : 1},
  {"kt" : -1.5, "kv" : 1.0, "idx" : 2},
  {"kt" : -1.25, "kv" : 1.0, "idx" : 3},
  {"kt" : -0.75, "kv" : 1.0, "idx" : 4},
  {"kt" : -0.5, "kv" : 1.0, "idx" : 5},
  {"kt" : -0.25, "kv" : 1.0, "idx" : 6},
  {"kt" : 0.0, "kv" : 1.0, "idx" : 7},
  {"kt" : 0.25, "kv" : 1.0, "idx" : 8},
  {"kt" : 0.5, "kv" : 1.0, "idx" : 9},
  {"kt" : 0.75, "kv" : 1.0, "idx" : 10},
  {"kt" : 1.0, "kv" : 1.0, "idx" : 11},
  {"kt" : 1.25, "kv" : 1.0, "idx" : 12},
  {"kt" : 1.5, "kv" : 1.0, "idx" : 13},
  {"kt" : 2.0, "kv" : 1.0, "idx" : 14},
  {"kt" : 3.0, "kv" : 1.0, "idx" : 15},
  {"kt" : -2.0, "kv" : 1.5, "idx" : 17},
  {"kt" : -1.25, "kv" : 1.5, "idx" : 19},
  {"kt" : -1.0, "kv" : 1.5, "idx" : 20},
  {"kt" : -0.5, "kv" : 1.5, "idx" : 22},
  {"kt" : -0.25, "kv" : 1.5, "idx" : 23},
  {"kt" : 0.25, "kv" : 1.5, "idx" : 25},
  {"kt" : 0.5, "kv" : 1.5, "idx" : 26},
  {"kt" : 1.0, "kv" : 1.5, "idx" : 28},
  {"kt" : 1.25, "kv" : 1.5, "idx" : 29},
  {"kt" : 2.0, "kv" : 1.5, "idx" : 31},
  {"kt" : -3.0, "kv" : 0.5, "idx" : 33},
  {"kt" : -2.0, "kv" : 0.5, "idx" : 34},
  {"kt" : -1.25, "kv" : 0.5, "idx" : 36},
  {"kt" : 1.25, "kv" : 0.5, "idx" : 46},
  {"kt" : 2.0, "kv" : 0.5, "idx" : 48},
  {"kt" : 3.0, "kv" : 0.5, "idx" : 49}
]

list_couplings = [{"name" : get_tH_weight_str(entry["kt"], entry["kv"]), "ratio" : entry["kt"]/entry["kv"]} for entry in tHweights] 

for entry in list_couplings :
    cmd = "WriteDatacards.py "
    cmd += " --inputShapes %s"  % options.inputShapes 
    cmd += " --channel %s"      % options.channel
    cmd += " --cardFolder %s"   % options.cardFolder
    if options.shapeSyst : cmd += " --shapeSyst"
    cmd += " --noX_prefix"
    cmd += " --coupling %s"     % entry["name"]
    cmd += " --era %s"          % options.era
    runCombineCmd(cmd)



