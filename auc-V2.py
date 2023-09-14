import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc, RocCurveDisplay
from scipy import interp

##图片名称###

name = 'BNNR_TLHGBI'

############


all_auc=[]
tprs=[]
mean_fpr=np.linspace(0,1,100)

def ro_curve_auc(y_pred, y_label, figure_file, method_name):
    y_label = np.array(y_label)
    y_pred = np.array(y_pred)
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    fpr[0], tpr[0], _ = roc_curve(y_label, y_pred)
    tprs.append(np.interp(mean_fpr,fpr[0],tpr[0]))
    tprs[-1][0]=0.0

    roc_auc[0] = auc(fpr[0], tpr[0])
    print("AUC "+method_name+": ",roc_auc[0])
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
    if not os.path.exists("result"):
        os.makedirs("result")
    plt.savefig('./result/{}_auc.png'.format(name),dpi=300)

def mean_auc_curve():
    mean_tpr=np.mean(tprs,axis=0)
    mean_tpr[-1]=1.0
    mean_auc=np.mean(all_auc)#计算平均AUC值
    lw = 2
    plt.plot(mean_fpr,mean_tpr,lw=lw,color='b',label=r'Mean ROC (area=%0.4f)'%mean_auc,alpha=.8)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    fontsize = 14
    plt.xlabel('False Positive Rate', fontsize=fontsize)
    plt.ylabel('True Positive Rate', fontsize=fontsize)
    plt.title('mean_AUROC', fontsize=fontsize)
    plt.legend(loc="lower right")
    plt.savefig('./result/{}_mean_auc.png'.format(name),dpi=300)

def col_pic_auc():
    for i in range(1, 11):
        y_label = []
        y_pred = []
        with open('final' + str(i) + '.csv') as f:
            f1 = csv.reader(f)
            for line in f1:
                y_label.append(int(float(line[0])))
                y_pred.append(float(line[1]))
            ro_curve_auc(y_pred, y_label, "auc_result", "Fold" + str(i))
            #print("Fold" + str(i))
    plt.close()
    print("AVG AUC:",np.mean(all_auc))


if __name__ == "__main__":
    col_pic_auc()
    mean_auc_curve()

