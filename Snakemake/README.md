# DR-method-evaluation
drug repositioning method evaluation
## How to use
We use two methods HGIMC and BNNR as examples. 

1. If you only want to get the prediction results and scalability (time and memory peak consumption) of the method on the specified dataset, run the command(rule run_method_pre):
~~~~
snakemake -j 1 {outdir}/{method}_{dataset}.csv
~~~~
Example : BNNR method on Fdataset  
Command : `snakemake -j 1 Evaluation/BNNR_Fdataset.csv`  
Command : `snakemake -j 1 Evaluation/BNNR_Fdataset.csv --use-conda`  
If you add the parameter `--use-conda`, snakemake will automatically create a running environment for you.
Following the completion of the run, you'll discover the prediction results within the Evaluation folder. Additionally, you can access logs detailing time and memory consumption in their respective Benchmark and Log folders. Users can add their own data sets to the Datasets folder of the specified method folder and run. For example, put Ydataset under the folder `BNNR/Datasets`.
  
2. If you want to get the full results of the method on the specified dataset, including prediction results, scalability,performance,auc curve and aupr curve,run the command(rule evaluate): 
~~~~
snakemake -j 1 {outdir}/{method}/{dataset}/Plot/{method}_{dataset}_auc.png
~~~~
or
~~~~
snakemake -j 1 {outdir}/{method}/{dataset}/Plot/{method}_{dataset}_aupr.png  
~~~~
Example : BNNR method on Cdataset  
Command : `snakemake -j 1 Evaluation/BNNR/Cdataset/Plot/BNNR_Cdataset_auc.png`  
Command : `snakemake -j 1 Evaluation/BNNR/Cdataset/Plot/BNNR_Cdataset_auc.png --use-conda`  
If you add the parameter `--use-conda`, snakemake will automatically create a running environment for you.
After completing the run, you can locate comprehensive results in the Evaluation folder. This encompasses prediction results, AUC curves, and AUPR curves found in the Plot folder, as well as AUC, AUPR, and F1 values stored in either the Benchmark folder or the Log folder. Users can add their own data sets to the Datasets folder and run.  
  
Users can add their own datasets to the Datasets folder of the specified method folder and execute. For example, put yourdataset under the folder `BNNR/Datasets/{yourdataset}` and then execute the command: `snakemake -j Evaluation/BNNR_{yourdataset}`.
## 
## DAG
![dag of DR evaluation snakemake](./dag_evaluate.png#pic_center)
## Datasets
The following datasets were used in our study：
`Fdataset`, `Cdataset`, `Ydataset`, `DNdataset`, `HDVD`, `LAGCN`, `LRSSL`, `SCMFDD_L`, `deepDR`, `iDrug`, `TLHGBI`, which is available at: [https://zenodo.org/record/8357512](https://zenodo.org/record/8357512).  



## Adding new methods
If you wish to incorporate a new method into the process, simply follow these steps:  
1. Place the method folder in the current directory.
2. Store the corresponding dataset in the Datasets folder.
3. Utilize `method_pre.m` and `crossval_method.m` as templates to adapt the `1. import data code` and `2. algorithmic code` sections according to your specific requirements, replacing them as needed.

If the method has already been crossvalidated, you just need to place the csv file results under the corresponding folder of the method, convert it to the final_CV_folds.csv file using the `originate-pre_2_final.py` script, and then run the Snakefile's evaluate rule.
  
If your method is not written in matlab, you should replace the `< >` placeholders in the Snakefile's `run_method_prerule` and `generate_CV_folds` rule shell with your own run script and make the necessary adjustments to your code accordingly. The `evaluate` rule  do not need to be modified.
~~~~
rule run_method_pre:
    input:
        "{method}/Datasets/{dataset}.mat"
    output:
        "{outdir}/{method}_{dataset}.csv"
    conda:
        "environment.yaml"
    log:
        "{outdir}/log/benchmark_{method}_{dataset}.log"
    benchmark:
        "{outdir}/Benchmark/benchmark_{method}_{dataset}.txt"
    shell:
        """
        # Run and record execution time and memory usage to the log file.
        (cd {wildcards.method} &&
        /usr/bin/time -f "\nExecution Time: %E\nPeak Memory Usage: %M KB" <your run script> 2>&1 | tee {log}  ## modify the script and adjust your code appropriately
        """

rule generate_CV_folds:
    input:
        "{outdir}/{method}_{dataset}.csv",
        "{method}/Datasets/{dataset}.mat"
    output:
        "{outdir}/{method}/{dataset}/final_CV_folds.csv"
    conda:
        "environment.yaml"
    log:
        "{outdir}/log/CV_{method}_{dataset}.log"
    benchmark:
        "{outdir}/Benchmark/CV_{method}_{dataset}.txt"
    shell:
        """
        # Run script and generate cross-validation fold data.
        (cd {wildcards.method} &&   
        <your script> &&      ## modify the script and adjust your code appropriately
        cd .. &&
        python origin-pre_2_final.py --file_path="{wildcards.outdir}/{wildcards.method}/{wildcards.dataset}" )  2>&1 | tee {log}
        """
~~~~

