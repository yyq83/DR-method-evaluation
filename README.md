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
If you only want to get the prediction results and scalability (time and memory peak consumption) of the method on the specified dataset, run the command:
~~~~
snakemake -j 1 {outdir}/{method}_{dataset}.csv
~~~~
example: `snakemake -j 1 snakemake -j 1 Evaluation/BNNR_Fdataset.csv`  


If you want to get the full results of the method on the specified dataset, including evaluation results, prediction results, run the command: 
~~~~
snakemake -j 1 {outdir}/{method}/{dataset}/Plot/{method}_{dataset}_auc.png
~~~~
example: `snakemake -j 1 Evaluation/BNNR/Cdataset/Plot/BNNR_Cdataset_auc.png`

## Datasets
The following datasets were used in our study：
`Fdataset`, `Cdataset`, `Ydataset`, `DNdataset`, `HDVD`, `LAGCN`, `LRSSL`, `SCMFDD_L`, `deepDR`, `iDrug`, `TLHGBI`, which is available at: [https://zenodo.org/record/8357512](https://zenodo.org/record/8357512).
