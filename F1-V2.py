import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import precision_recall_curve, average_precision_score, f1_score
import argparse

# List to store F1 scores for each fold
all_F1 = []

# Function to calculate F1 score for a fold
def F1(y_pred, y_label, method_name):
    y_label = np.array(y_label)
    y_pred = np.array(y_pred)
    precision, recall, _ = precision_recall_curve(y_label, y_pred)
    numerator = 2 * recall * precision
    denom = recall + precision
    F1 = np.divide(numerator, denom, out=np.zeros_like(denom), where=(denom != 0))
    all_F1.append(np.mean(F1))
    print("F1 " + method_name + ": ", np.mean(F1))

# Function to calculate F1 scores for all folds
def col_F1():
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
            F1(y_pred, y_label, "Fold" + str(i))
    print("AVG F1: ", np.mean(all_F1))
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
    col_F1()
