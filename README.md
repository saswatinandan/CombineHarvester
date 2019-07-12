## ------- PLEASE FOLLOW THESE INSTRUCTIONS FOR INSTALLATION ---------
cmsrel CMSSW_8_1_0

cd CMSSW_8_1_0/src/

cmsenv

git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit

git fetch origin

git checkout v7.0.12

scramv1 b clean; scramv1 b

cd $CMSSW_BASE/src

git clone https://github.com/HEP-KBFI/CombineHarvester CombineHarvester

scram b
## -------------------------------------------------------------------- ##

