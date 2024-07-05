import copy
import numpy as np
import datainstantiation
import tools
from process import main_progress
import time
from initialize import Initialize
from solution_based_DM import cnbdm
from TS import Ts

if __name__ == '__main__':
    ctsnum=400
    print("任务数量为",ctsnum)
    print("算法的结果")
    P_list4 = []
    T_list4 = []
    for enpoch in range(5):
        a=main_progress(5,ctsnum,1,1,3,5,400,20,50,0.5,10,2) #
        st=time.time()
        result=a.progress()
        et=time.time()
        P_list4.append(result)
        T_list4.append(et - st)
    print("收益结果:")
    for i in range(len(P_list4)):
        print(P_list4[i])
    print("时间结果:")
    for i in range(len(T_list4)):
        print(T_list4[i])






