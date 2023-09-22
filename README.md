# DR-method-evaluation
![Overview of DR evaluation](./figures/overflow_v16.png )

## Requirements
Matlab 2020a

## Installation
Download by
~~~~
git clone https://github.com/yyq83/DR-method-evaluation.git
~~~~
and install dependencies by
~~~~~
conda env create -f environment.yaml
~~~~~

## Usage
Go to the Snakemake folder
~~~~
cd Snakemake
~~~~
1. 
If you only want to get the prediction results and scalability (time and memory peak consumption) of the method on the specified dataset, run the command:
~~~~
snakemake -j 1 {outdir}/{method}_{dataset}.csv
~~~~
example : BNNR method on Fdataset  
command :`snakemake -j 1 snakemake -j 1 Evaluation/BNNR_Fdataset.csv`  
After running, you can find the prediction results in the Evalutaion folder, as well as time and memory consumption logs in the corresponding Benchmark folder and log folder below.  

2. 
If you want to get the full results of the method on the specified dataset, including prediction results, scalability,performance,auc curve and aupr curve,run the command: 
~~~~
snakemake -j 1 {outdir}/{method}/{dataset}/Plot/{method}_{dataset}_auc.png
~~~~
example : BNNR method on Cdataset  
command : `snakemake -j 1 Evaluation/BNNR/Cdataset/Plot/BNNR_Cdataset_auc.png`  
After running, you can find the full results in the Evalutaion folder, too.

## Datasets
The following datasets were used in our study：
`Fdataset`, `Cdataset`, `Ydataset`, `DNdataset`, `HDVD`, `LAGCN`, `LRSSL`, `SCMFDD_L`, `deepDR`, `iDrug`, `TLHGBI`, which is available at: [https://zenodo.org/record/8357512](https://zenodo.org/record/8357512).
