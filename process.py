import copy
import tools
from initialize import Initialize
import numpy as np
import random
import math
from TS import Ts
import multiprocessing as mp
from solution_based_DM import cnbdm
class main_progress:
    def __init__(self,N,tasknum,n_d,n_r,n_a,core_num,Termination,elite_sum, un_improvement,k,n,min_support):
        self.N=N
        self.tasknum=tasknum
        self.n_d=n_d
        self.n_r=n_r
        self.n_a=n_a
        self.core_num=core_num
        self.destory_probability = np.zeros((n_d,), dtype=float)
        self.repair_probability = np.zeros((n_r,), dtype=float)
        self.algorithm_probability = np.zeros((n_a,), dtype=float)
        self.Termination=Termination
        self.elite_sum=elite_sum
        self.un_improvement=un_improvement
        self.k=k
        self.n=n
        self.min_support=min_support

    def TS(self,q,init_solution,del_list,i1,un_improve1,elites,d_index_list,r_index_list,rate):#solution[i],del_list,i1,un_improve1,elites,d_index_list,r_index_list)
        TS_result=[]
        A_TS=Ts(self.tasknum,self.destory_probability,self.repair_probability,init_solution,self.Termination*rate,self.elite_sum,self.un_improvement,del_list)
        [i, i_unimprove, k,elites,d_index_list,r_index_list,profit_seq,A_index]=A_TS.ts(i1,un_improve1,elites,d_index_list,r_index_list)
        TS_result.append(i)
        TS_result.append(i_unimprove)
        TS_result.append(k)
        TS_result.append(elites)
        TS_result.append(d_index_list)
        TS_result.append(r_index_list)
        TS_result.append(profit_seq)
        TS_result.append(A_index)
        q.put(TS_result)
        print(rate)

    def multi_core(self,solution,i1,un_improve1,del_list,elites,d_index_list,r_index_list,rate):
        q = mp.Queue()
        process_list = []
        for i in range(self.core_num):
            a_p = random.random()
            if a_p < self.algorithm_probability[0]:
                p = mp.Process(target=self.TS, args=(
                q, solution[i], del_list, i1, un_improve1, elites, d_index_list, r_index_list, rate))
                p.start()
                process_list.append(p)
            elif self.algorithm_probability[0] < a_p < self.algorithm_probability[1]:
                p = mp.Process(target=self.TS, args=(q, solution[i],del_list,i1,un_improve1,elites,d_index_list,r_index_list,rate))
                p.start()
                process_list.append(p)
            else:
                p = mp.Process(target=self.TS, args=(
                q, solution[i], del_list, i1, un_improve1, elites, d_index_list, r_index_list, rate))
                p.start()
                process_list.append(p)
        res = []
        for i in range(self.core_num):
            res.append(q.get())
        return res

    def progress(self):
        init=Initialize(self.N,self.tasknum,self.n_d,self.n_r,self.n_a)
        init.initialization()
        init_solution=copy.deepcopy(init.initialization_solution)
        self.destory_probability=copy.deepcopy(init.destory_probability)
        self.repair_probability=copy.deepcopy(init.repair_probability)
        self.algorithm_probability=copy.deepcopy(init.algorithm_probability)
        del_list=np.zeros((self.tasknum,),dtype=int)
        elites=[]
        d_index_list=[]
        r_index_list=[]
        A_index_list=[]
        profit_seq=[]
        result=[]
        if self.tasknum<=150:
            res = self.multi_core(init_solution, 0, 0, del_list, [], [], [], 1)  # 先运行500代  不调用数据挖掘
            for i in range(len(res)):
                for j in range(len(res[i][3])):
                    elites.append(res[i][3][j])
                    d_index_list.append(res[i][4][j])
                    r_index_list.append(res[i][5][j])
                    A_index_list.append(res[i][7][j])
                profit_seq.append(res[i][6])
            list_temp = []
            for i in range(len(profit_seq)):
                list_temp.append(max(profit_seq[i]))
            return max(list_temp)
        else:
            res=self.multi_core(init_solution,0,0,del_list,[],[],[],0.3)   #先运行500代
            for i in range(len(res)):
                for j in range(len(res[i][3])):
                    elites.append(res[i][3][j])
                    d_index_list.append(res[i][4][j])
                    r_index_list.append(res[i][5][j])
                    A_index_list.append(res[i][7][j])
                profit_seq.append(res[i][6])
            list_temp=[]
            for i in range(len(profit_seq)):
                list_temp.append(max(profit_seq[i]))
            result.append(max(list_temp))
            news=cnbdm(elites,self.n,self.min_support,self.core_num,self.tasknum)#数据挖掘
            news.start_cnbdm()
            solutions=news.newsolution_set
            res1=self.multi_core(solutions,0,0,del_list,[],[],[],1)
            profit_seq1=[]
            for i in range(len(res1)):
                profit_seq1.append(res1[i][6])
            list_temp1=[]
            for i in range(len(profit_seq1)):
                list_temp1.append(max(profit_seq1[i]))
            result.append(max(list_temp1))
            return max(result)













