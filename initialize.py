#初始化解集  输入为初始化解集的数量
import random
import datainstantiation
import tools
import numpy as np



class Initialize:
    def __init__(self, N, tasknum,n_d,n_r,n_a):
        self.N = N
        self.tasknum = tasknum
        self.initialization_solution = []
        self.n_d=n_d
        self.n_r=n_r
        self.n_a=n_a
        self.destory_probability=np.zeros((n_d,),dtype=float)
        self.repair_probability = np.zeros((n_r,), dtype=float)
        self.algorithm_probability=np.zeros((n_a,),dtype=float)

    def initialization(self):


        for i in range(self.n_d):
            self.destory_probability[i]=1/self.n_d
        for i in range(self.n_r):
            self.repair_probability[i]=1/self.n_r
        for i in range(self.n_a):
            self.algorithm_probability[i]=1/self.n_a
        self.destory_probability=np.cumsum(self.destory_probability)
        self.repair_probability=np.cumsum(self.repair_probability)
        self.algorithm_probability=np.cumsum(self.algorithm_probability)

        task_profit_seq = []
        task_executetime_seq = []
        task_timewindownum_seq = []
        task_start_time_seq=[]

        for i in range(self.tasknum):
            task_profit_seq.append(datainstantiation.tasklists[i][3])
            task_executetime_seq.append(datainstantiation.tasklists[i][4])
            task_timewindownum_seq.append(len(datainstantiation.tasktimewindow[i]))
            task_start_time_seq.append(datainstantiation.Attitudeangle[i][0][0])

        task_seq_profit=[]
        task_profit_seq_temp=task_profit_seq.copy()
        task_profit_seq_temp.sort(reverse=True)
        for i in range(len(task_profit_seq_temp)):
            index=task_profit_seq.index(task_profit_seq_temp[i])
            task_seq_profit.append(index)
            task_profit_seq[index] = float("inf")
        task_plan_profit=tools.generateplan(task_seq_profit)
        task_seq_executetime=[]
        task_executetime_seq_temp=task_executetime_seq.copy()
        task_executetime_seq_temp.sort(reverse=False)
        for i in range(len(task_executetime_seq_temp)):
            index=task_executetime_seq.index(task_executetime_seq_temp[i])
            task_seq_executetime.append(index)
            task_executetime_seq[index]=float("inf")
        task_plan_executetime=tools.generateplan(task_seq_executetime)

        task_timewindownum_seq_temp=task_timewindownum_seq.copy()
        task_timewindownum_seq_temp.sort(reverse=False)
        task_seq_timewindownum=[]
        for i in range(len(task_timewindownum_seq_temp)):
            index=task_timewindownum_seq.index(task_timewindownum_seq_temp[i])
            task_seq_timewindownum.append(index)
            task_timewindownum_seq[index]=float("inf")
        task_plan_timewindownum=tools.generateplan(task_seq_timewindownum)

        time_seq=[]
        for i in range(len(task_start_time_seq)):
            time=task_start_time_seq[i][3]*60*60+task_start_time_seq[i][4]*60+task_start_time_seq[i][5]
            time_seq.append(time)
        time_seq_temp=time_seq.copy()
        time_seq_temp.sort(reverse=False)
        task_time_seq = []
        for i in range(len(time_seq_temp)):
            index=time_seq.index(time_seq_temp[i])
            task_time_seq.append(index)
            time_seq[index]=float("inf")
        task_plan_starttime=tools.generateplan(task_time_seq)

        for i in range(self.N):
            number=random.randint(0, 4)
            if number==0:
                self.initialization_solution.append(task_plan_profit)
            elif number==1:
                self.initialization_solution.append(task_plan_executetime)
            elif number==2:
                self.initialization_solution.append(task_plan_timewindownum)
            elif number==3:
                self.initialization_solution.append(task_plan_starttime)
            else:
                a = [x for x in range(self.tasknum)]
                random.shuffle(a)
                self.initialization_solution.append(tools.generateplan(a))

