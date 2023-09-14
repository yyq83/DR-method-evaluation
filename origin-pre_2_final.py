import pandas as pd
import numpy as np


for i in range(1,11):
    with open(f'origin{i}.csv','r') as f:
        csv = pd.read_csv(f, header=None)
        origin_data = csv.values

    with open(f'pre{i}.csv','r') as f:
        csv = pd.read_csv(f, header=None)
        pre_data = csv.values

    # print(origin_data)
    origin = []
    pre = []
    for line in origin_data:
        # print(line)
        for item in line:
            origin.append(item)
    # print(origin)
    for line in pre_data:
        for item in line:
            pre.append(item)

    origin_array = np.array(origin)
    pre_array = np.array(pre)
    
    with open(f'final{i}.csv','w') as f:
        save = pd.DataFrame({'origin':origin,'pre':pre})
        save.to_csv(f,line_terminator='\n',index=False, header=False)
