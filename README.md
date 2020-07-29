## ------- PLEASE FOLLOW THESE INSTRUCTIONS FOR INSTALLATION ---------
cmsrel CMSSW_8_1_0

cd CMSSW_8_1_0/src/

cmsenv

git init

git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit

cd HiggsAnalysis/CombinedLimit

git remote add origin https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git

git fetch origin

git checkout v7.0.12

cd $CMSSW_BASE/src

git clone https://github.com/HEP-KBFI/CombineHarvester CombineHarvester

scram b -j 8
## -------------------------------------------------------------------- ##

