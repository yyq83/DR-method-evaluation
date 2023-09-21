import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc, RocCurveDisplay
from scipy import interp
import argparse

# Lists to store AUC values and true positive rates for each fold
all_auc = []
tprs = []
mean_fpr = np.linspace(0, 1, 100)

# Function to calculate ROC curve and AUC for a fold
def ro_curve_auc(y_pred, y_label, figure_file, method_name):
    y_label = np.array(y_label)
    y_pred = np.array(y_pred)
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    fpr[0], tpr[0], _ = roc_curve(y_label, y_pred)
    tprs.append(np.interp(mean_fpr, fpr[0], tpr[0]))
    tprs[-1][0] = 0.0

    roc_auc[0] = auc(fpr[0], tpr[0])
    print("AUC " + method_name + ": ", roc_auc[0])
    all_auc.append(roc_auc[0])
    lw = 2
    plt.plot(fpr[0], tpr[0],
             lw=lw, label=method_name + ' (area = %0.4f)' % roc_auc[0])
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    fontsize = 14
    plt.xlabel('False Positive Rate', fontsize=fontsize)
    plt.ylabel('True Positive Rate', fontsize=fontsize)
    plt.title('AUROC', fontsize=fontsize)
    plt.legend(loc="lower right")

    # Create a 'Plot' directory inside the specified 'file_path' if it doesn't exist
    plot_dir = os.path.join(file_path, "Plot")
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    # Save the plot in the 'Plot' directory
    plt.savefig(os.path.join(plot_dir, '{}_auc.png'.format(name)), dpi=300)

# Function to calculate mean ROC curve and mean AUC
def mean_auc_curve():
    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = np.mean(all_auc)  # Calculate the mean AUC value
    lw = 2
    plt.plot(mean_fpr, mean_tpr, lw=lw, color='b',
             label=r'Mean ROC (area=%0.4f)' % mean_auc, alpha=.8)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    fontsize = 14
    plt.xlabel('False Positive Rate', fontsize=fontsize)
    plt.ylabel('True Positive Rate', fontsize=fontsize)
    plt.title('mean_AUROC', fontsize=fontsize)
    plt.legend(loc="lower right")

    # Create a 'Plot' directory inside the specified 'file_path' if it doesn't exist
    plot_dir = os.path.join(file_path, "Plot")
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    # Save the plot in the 'Plot' directory
    plt.savefig(os.path.join(plot_dir, '{}_mean_auc.png'.format(name)), dpi=300)

# Function to calculate ROC curves and AUC for each fold
def col_pic_auc():
    for i in range(1, 11):
        y_label = []
        y_pred = []
        with open(f'{file_path}/final_CV_folds.csv') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                file_name = row[2]  # Assuming the file name is in the third column
                if file_name.startswith(f'origin{i}'):
                    y_label.append(int(float(row[0])))
                    y_pred.append(float(row[1]))

        ro_curve_auc(y_pred, y_label, "auc_result", "Fold" + str(i))

    plt.close()
    print("AVG AUC:", np.mean(all_auc))
    print('----------------------------------')

if __name__ == "__main__":
    # Initialize argparse
    parser = argparse.ArgumentParser(description="Generate ROC curves and calculate AUC values.")
    parser.add_argument("--method", type=str, default="default_method", help="Method name")
    parser.add_argument("--dataset", type=str, default="default_dataset", help="Dataset name")
    parser.add_argument('--file_path', type=str, help='Path to the directory containing folds final CSV files')

    # Parse the command-line arguments
    args = parser.parse_args()

    name = args.method + "_" + args.dataset
    file_path = args.file_path
    col_pic_auc()
    mean_auc_curve()
