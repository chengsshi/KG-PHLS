import copy

import datainstantiation
import tools
import random

class repairing:
    def __init__(self, plan):
        self.plan=copy.deepcopy(plan)
        self.unscheduled_plan=[]
        self.latest_starttime_list=[]
        self.latest_endtime_list=[]
        self.insert_tasks=[]


    def re_arrange(self):
        (s_time,e_time,tw)=tools.calculate_early_start_time(self.plan[0][0])
        self.plan[0][5]=s_time.copy()
        self.plan[0][6]=e_time.copy()
        self.plan[0][7]=tw
        for i in range(1,len(self.plan)):
                (s_time,e_time,tw)=tools.calculate_next_starttime(self.plan[i-1][6],self.plan[i][0])     #上一个任务的结束时间
                self.plan[i][5] = s_time.copy()
                self.plan[i][6] = e_time.copy()
                self.plan[i][7] = tw

    def calculate_time_slack(self):
        time_slack_list=tools.time_slack_whole_plan(self.plan)
        for i in range(len(self.plan)):
            self.latest_starttime_list.append(time_slack_list[i][1])
            self.latest_endtime_list.append(time_slack_list[i][2])


    def unscheduled(self):
        whole_tasklist=[]
        scheduled_plan=[]
        for i in range(len(datainstantiation.tasklists)):
            whole_tasklist.append(datainstantiation.tasklists[i][0])
        for i in range(len(self.plan)):
            scheduled_plan.append(self.plan[i][0])
        for i in whole_tasklist:
            if i not in scheduled_plan:
                self.unscheduled_plan.append(i)

    def Fastinsertion(self,unscheduled_tasklist):
        for i in range(len(unscheduled_tasklist)):
            index=unscheduled_tasklist[i]
            if tools.judge_taskexecute(index):
                [position, start_time_list, end_time_list, TW_list, difference_list]=tools.calculate_insert_position(self.plan,index,self.latest_starttime_list,self.latest_endtime_list)
                if len(position)>0:
                    plan_item=[]
                    a= difference_list.index(min(difference_list))
                    plan_item.append(index)
                    plan_item.append(datainstantiation.tasklists[index][1])
                    plan_item.append(datainstantiation.tasklists[index][2])
                    plan_item.append(datainstantiation.tasklists[index][3])
                    plan_item.append(datainstantiation.tasklists[index][4])
                    plan_item.append(start_time_list[a])
                    plan_item.append(end_time_list[a])
                    plan_item.append(TW_list[a])
                    [new_plan, last_starttime_list, last_endtime_list]=tools.upgrade_plan(self.plan,position[a],plan_item,self.latest_starttime_list,self.latest_endtime_list)
                    self.plan=new_plan.copy()
                    self.latest_starttime_list=last_starttime_list.copy()
                    self.latest_endtime_list=last_endtime_list.copy()
                    self.insert_tasks.append(index)

    def repair1(self):
        self.unscheduled()
        unscheduled_tasklist,profit_seq=[],[]
        for i in self.unscheduled_plan:
            profit_seq.append(datainstantiation.tasklists[i][3])
        profit_seq_temp=profit_seq.copy()
        profit_seq_temp.sort(reverse=True)
        for i in range(len(profit_seq_temp)):
            index=profit_seq.index(profit_seq_temp[i])
            unscheduled_tasklist.append(self.unscheduled_plan[index])
            profit_seq[index]=float("inf")
        return unscheduled_tasklist

    def repair2(self):
        self.unscheduled()
        unscheduled_tasklist, profit_seq = [], []
        for i in self.unscheduled_plan:
            per_profit_seq=datainstantiation.tasklists[i][3]/datainstantiation.tasklists[i][4]
            profit_seq.append(per_profit_seq)
        profit_seq_temp=profit_seq.copy()
        profit_seq_temp.sort(reverse=True)
        for i in range(len(profit_seq_temp)):
            index=profit_seq.index(profit_seq_temp[i])
            unscheduled_tasklist.append(self.unscheduled_plan[index])
            profit_seq[index]=float("inf")
        return unscheduled_tasklist
class Destory_tabu:
    def __init__(self, plan, N,del_list):
        self.plan = copy.deepcopy(plan)
        self.N = N
        self.del_list=del_list
        self.tabu_index=[]


    def get_tabu_index(self):
        for i in range(len(self.plan)):
            index=self.plan[i][0]
            if self.del_list[index]!=0:
                self.tabu_index.append(i)

    def get_full_destory_index(self,destory_index):
        destory_index_temp=destory_index.copy()
        random.shuffle(self.tabu_index)
        for i in self.tabu_index:
            destory_index_temp.append(i)
            if len(destory_index_temp)==self.N:
                break
        return destory_index_temp

    def destory2(self):
        profit_seq = []
        new_plan = []
        destory_index = []
        self.get_tabu_index()
        for i in range(len(self.plan)):
            profit_seq.append(self.plan[i][3])
        profit_seq_temp = profit_seq.copy()
        profit_seq_temp.sort(reverse=False)
        for i in range(len(self.plan)):
            index=profit_seq.index(profit_seq_temp[i])
            if self.del_list[index]==0:
                destory_index.append(index)
                profit_seq[index] = float("inf")
                if len(destory_index)>=self.N:
                    break
        if len(destory_index)<self.N:
            destory_index=self.get_full_destory_index(destory_index).copy()
        for i in range(len(self.plan)):
            if i not in destory_index:
                new_plan.append(self.plan[i])
        destory_tasks = []
        for i in destory_index:
            destory_tasks.append(self.plan[i][0])
        return new_plan, destory_tasks


    def destory3(self):
        profit_seq = []
        new_plan = []
        destory_index = []
        self.get_tabu_index()
        for i in range(len(self.plan)):
            profit_seq.append(self.plan[i][3] / self.plan[i][4])
        profit_seq_temp = profit_seq.copy()
        profit_seq_temp.sort(reverse=False)
        for i in range(len(self.plan)):
            index=profit_seq.index(profit_seq_temp[i])
            if self.del_list[index]==0:
                destory_index.append(index)
                profit_seq[index] = float("inf")
                if len(destory_index)>=self.N:
                    break
        if len(destory_index)<self.N:
            destory_index=self.get_full_destory_index(destory_index).copy()
        for i in range(len(self.plan)):
            if i not in destory_index:
                new_plan.append(self.plan[i])
        destory_tasks = []
        for i in destory_index:
            destory_tasks.append(self.plan[i][0])
        return new_plan, destory_tasks