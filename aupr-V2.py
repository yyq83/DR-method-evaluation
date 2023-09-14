import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import precision_recall_curve, average_precision_score, f1_score


##图片名称###

name = 'BNNR_TLHGBI'

############

all_aupr=[]
precisions = []
mean_recall = np.linspace(0,1,100)


def ro_curve_aupr(y_pred, y_label, figure_file, method_name):
    y_label = np.array(y_label)
    y_pred = np.array(y_pred)
    lr_precision, lr_recall, _ = precision_recall_curve(y_label, y_pred)
    all_aupr.append(average_precision_score(y_label, y_pred))
    precisions.append(np.interp(mean_recall,lr_precision,lr_recall))

    plt.plot(lr_recall, lr_precision, lw=2,
             label=method_name + ' (area = %0.4f)' % average_precision_score(y_label, y_pred))
    fontsize = 14
    print("AUPR "+method_name+": ",average_precision_score(y_label, y_pred))
    plt.xlabel('Recall', fontsize=fontsize)
    plt.ylabel('Precision', fontsize=fontsize)
    plt.title('AUPR')
    plt.legend(loc="lower left")
    if not os.path.exists("result"):
        os.makedirs("result")
    plt.savefig('./result/{}_aupr.png'.format(name),dpi=300)
   
def mean_aupr_curve():
    mean_precision = np.mean(precisions,axis=0)
    mean_aupr=np.mean(all_aupr)
    lw = 2
    plt.plot(mean_recall,mean_precision,lw=lw,color='b',label=r'Mean_AUPR (area=%0.4f)'%mean_aupr,alpha=.8)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    fontsize = 14
    plt.xlabel('Recall', fontsize=fontsize)
    plt.ylabel('Precision', fontsize=fontsize)
    plt.title('mean_AUPR', fontsize=fontsize)
    plt.legend(loc="lower right")
    plt.savefig('./result/{}_mean_aupr.png'.format(name),dpi=300)



def col_pic_aupr():
    for i in range(1, 11):
        y_label = []
        y_pred = []
        with open('final' + str(i) + '.csv') as f:
            f1 = csv.reader(f)
            for line in f1:
                y_label.append(float(line[0]))
                y_pred.append(float(line[1]))
            ro_curve_aupr(y_pred, y_label, "aupr_result", "Fold" + str(i))
            #print("aupr:Fold" + str(i))
    plt.close()
    print("AVG AUPR: ",np.mean(all_aupr))

if __name__ == "__main__":
    col_pic_aupr()
    mean_aupr_curve()
