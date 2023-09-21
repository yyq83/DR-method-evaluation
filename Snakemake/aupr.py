import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import precision_recall_curve, average_precision_score, f1_score
import argparse

# Lists to store AUPR values and other values for each fold
all_aupr = []
precisions = []
mean_recall = np.linspace(0, 1, 100)

# Function to calculate precision-recall curve and AUPR for a fold
def ro_curve_aupr(y_pred, y_label, figure_file, method_name):
    y_label = np.array(y_label)
    y_pred = np.array(y_pred)
    lr_precision, lr_recall, _ = precision_recall_curve(y_label, y_pred)
    all_aupr.append(average_precision_score(y_label, y_pred))
    precisions.append(np.interp(mean_recall, lr_recall, lr_precision))

    plt.plot(lr_recall, lr_precision, lw=2,
             label=method_name + ' (area = %0.4f)' % average_precision_score(y_label, y_pred))
    fontsize = 14
    print("AUPR " + method_name + ": ", average_precision_score(y_label, y_pred))
    plt.xlabel('Recall', fontsize=fontsize)
    plt.ylabel('Precision', fontsize=fontsize)
    plt.title('AUPR')
    plt.legend(loc="lower left")

    # Create a 'Plot' directory inside the specified 'file_path' if it doesn't exist
    plot_dir = os.path.join(file_path, "Plot")
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    # Save the plot in the 'Plot' directory
    plt.savefig(os.path.join(plot_dir, '{}_aupr.png'.format(name)), dpi=300)

# Function to calculate mean precision-recall curve and mean AUPR
def mean_aupr_curve():
    mean_precision = np.mean(precisions, axis=0)
    mean_aupr = np.mean(all_aupr)
    lw = 2
    plt.plot(mean_recall, mean_precision, lw=lw, color='b',
             label=r'Mean_AUPR (area=%0.4f)' % mean_aupr, alpha=.8)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    fontsize = 14
    plt.xlabel('Recall', fontsize=fontsize)
    plt.ylabel('Precision', fontsize=fontsize)
    plt.title('mean_AUPR', fontsize=fontsize)
    plt.legend(loc="lower right")

    # Create a 'Plot' directory inside the specified 'file_path' if it doesn't exist
    plot_dir = os.path.join(file_path, "Plot")
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    # Save the plot in the 'Plot' directory
    plt.savefig(os.path.join(plot_dir, '{}_mean_aupr.png'.format(name)), dpi=300)

# Function to calculate precision-recall curves and AUPR for each fold
def col_pic_aupr():
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

            ro_curve_aupr(y_pred, y_label, "aupr_result", "Fold" + str(i))

    plt.close()
    print("AVG AUPR: ", np.mean(all_aupr))
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
    col_pic_aupr()
    mean_aupr_curve()
