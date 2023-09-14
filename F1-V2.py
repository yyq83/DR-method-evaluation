import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import precision_recall_curve, average_precision_score, f1_score

all_F1=[]

def F1(y_pred, y_label,method_name):
    y_label = np.array(y_label)
    y_pred = np.array(y_pred)
    precision, recall, _ = precision_recall_curve(y_label, y_pred)
    F1 = 2*recall*precision/(recall+precision)
    all_F1.append(np.mean(F1))
    print("F1 "+method_name+": ",np.mean(F1))



def col_F1():
    for i in range(1, 11):
        y_label = []
        y_pred = []
        with open('final' + str(i) + '.csv') as f:
            f1 = csv.reader(f)
            for line in f1:
                y_label.append(float(line[0]))
                y_pred.append(float(line[1]))
            F1(y_pred, y_label,"Fold" + str(i))
    print("AVG F1: ",np.mean(all_F1))

if __name__ == "__main__":
    col_F1()
