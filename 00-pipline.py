import os

#################################################
#01 BNNR calulation
os.system('''matlab -nodisplay -nosplash -nodesktop -r "run('BNNR_V1.m');exit;"''')
#################################################

#################################################
#02 origin.csv and pre.csv to final.csv
os.system("python origin-pre_2_final.py")
#################################################

#################################################
#03 calulate AUC、AUPR and F1
os.system("python auc-V2.py")
os.system("python aupr-V2.py")
os.system("python F1-V2.py")
#################################################

