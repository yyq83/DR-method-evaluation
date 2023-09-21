#####################################################
#### 1. method prediction results and scalability(Time usage and peak memory consumption)

#If you only need the prediction results and scalability of a method on a certain dataset, 
#run the code: 
#example:  BNNR method on Fdataset 
#command 1: snakemake -j 1 Evaluation/BNNR_Fdataset.csv
#command 2: snakemake -j 1 Evaluation/BNNR_Fdataset.csv --use-conda  

## When the run is completed, you can get the prediction result file BNNR_Fdataset.csv in the 'Evaluation/' folder, 
## benchmark_BNNR_Fdataset.txt under the 'Evaluation/Benchmark/' folder, which records the time and peak memory consumption(scalability), 
## and get the benchmark_BNNR_Fdataset.log file under the 'Evaluation/log/' folder.
#####################################################


#####################################################
#### 2. method performance auc,aupr,F1 and prediction results and scalability(All)

#If you need the prediction results,scalability,performance,auc curve and aupr curve of a method on a certain dataset, 
#run the code: 
#example:  BNNR method on Cdataset
#command 1: snakemake -j 1 Evaluation/BNNR/Cdataset/Plot/BNNR_Cdataset_auc.png
#command 2: snakemake -j 1 Evaluation/BNNR/Cdataset/Plot/BNNR_Cdataset_auc.png --use-conda

## When the run is completed, you can get the prediction result file BNNR_Cdataset.csv in the 'Evaluation/' folder, 
## benchmark_BNNR_Cdataset.txt under the 'Evaluation/Benchmark/' folder, which records the time and peak memory consumption(scalability), 
## get the benchmark_BNNR_Cdataset.log file under the 'Evaluation/log/' folder, which records the log.
## get 10-fold cross-validation csv file under 'Evaluation/BNNR/Cdataset'.
## get the auc curve and aupr curve under the 'Evaluation/BNNR/Cdataset/Plot/'
## get auc,aupr ,F1 value at log file 'Evaluation/log/evaluate_BNNR_Cdataset.log'
#####################################################



# Define the "all" rule, which depends on two graphic files as inputs.
rule all:
    input:
        "{outdir}/{method}/{dataset}/Plot/{method}_{dataset}_auc.png",
        "{outdir}/{method}/{dataset}/Plot/{method}_{dataset}_aupr.png"


# The "run_method_pre" rule to generate prediction results. .
# Output the prediction results of the method on the dataset.
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
        /usr/bin/time -f "\nExecution Time: %E\nPeak Memory Usage: %M KB" matlab -nodisplay -nosplash -nodesktop -r "method_pre('{wildcards.method}','{wildcards.dataset}','{wildcards.outdir}'); exit;") 2>&1 | tee {log}
        """

# The "generate_CV_folds" rule to generate cross-validation fold data.
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
        matlab -nodisplay -nosplash -nodesktop -r "crossval_method('{wildcards.method}','{wildcards.dataset}','{wildcards.outdir}'); exit;" &&
        cd .. &&
        python origin-pre_2_final.py --file_path="{wildcards.outdir}/{wildcards.method}/{wildcards.dataset}" )  2>&1 | tee {log}
        """


# The "evaluate" rule to evaluate model performance and generate graphics.
rule evaluate:
    input:
        "{outdir}/{method}/{dataset}/final_CV_folds.csv"
    output:
        "{outdir}/{method}/{dataset}/Plot/{method}_{dataset}_auc.png",
        "{outdir}/{method}/{dataset}/Plot/{method}_{dataset}_aupr.png"
    conda:
        "environment.yaml"
    log:
        "{outdir}/log/evaluate_{method}_{dataset}.log"
    benchmark:
        "{outdir}/Benchmark/evaluate_{method}_{dataset}.txt"
    shell:
        """
        # Run multiple Python scripts to calculate the auc,aupr, and F1 values.
        (python auc-V2.py --method {wildcards.method} --dataset {wildcards.dataset} --file_path "{wildcards.outdir}/{wildcards.method}/{wildcards.dataset}" &&
        python aupr-V2.py --method {wildcards.method} --dataset {wildcards.dataset} --file_path "{wildcards.outdir}/{wildcards.method}/{wildcards.dataset}" &&
        python F1-V2.py --method {wildcards.method} --dataset {wildcards.dataset} --file_path "{wildcards.outdir}/{wildcards.method}/{wildcards.dataset}" ) 2>&1 | tee {log}
        """
