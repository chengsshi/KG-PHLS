import copy
import random
import datainstantiation
import tools
from construct import repairing,Destory_tabu
import math

class Ts:
    def __init__(self, tasknum, destory_probability, repair_probability, plan, Termination,elite_sum,un_improvement,del_list):  # 破坏算子的概率，修复算子的概率，一个初始方案(当前方案),破坏解的数量，历史最小转换时间,终止条件,每个算法提供的精英个体数量,禁忌列表长度
        self.tasknum = tasknum
        self.destory_probability = destory_probability
        self.repair_probability = repair_probability
        self.plan = copy.deepcopy(plan)
        self.N = int(math.ceil(0.1*len(plan)))
        self.Termination = Termination
        self.elite_sum = elite_sum
        self.un_improvement=un_improvement
        self.del_list=del_list
        self.length=math.ceil(tasknum*0.1)

    def create_newsolution1(self, plan):
        destory_plan = []
        d = random.random()
        r = random.random()
        destory_operator = Destory_tabu(plan, self.N, self.del_list)
        d_list = [destory_operator.destory2]
        if d <= self.destory_probability[0]:
            (destory_plan, destory_tasks) = d_list[0]()
            d_index = 0
        else:
            for i in range(1, len(self.destory_probability)):
                if self.destory_probability[i - 1] < d <= self.destory_probability[i]:
                    (destory_plan, destory_tasks) = d_list[i]()
                    d_index = i
                    break
        repair_operator = repairing(destory_plan)
        repair_operator.re_arrange()
        repair_operator.calculate_time_slack()
        r_list = [repair_operator.repair1]
        if r <= self.repair_probability[0]:
            unscheduled_tasklist = r_list[0]()
            repair_operator.Fastinsertion(unscheduled_tasklist)
            r_index = 0
        else:
            for i in range(1, len(self.repair_probability)):
                if self.repair_probability[i - 1] < r <= self.repair_probability[i]:
                    unscheduled_tasklist = r_list[i]()
                    repair_operator.Fastinsertion(unscheduled_tasklist)
                    r_index = i
                    break
        newsolution = repair_operator.plan
        insert_tasks = repair_operator.insert_tasks
        return newsolution, d_index, r_index, destory_tasks, insert_tasks
    def create_newsolution2(self, plan):
        destory_plan = []
        d = random.random()
        r = random.random()
        destory_operator = Destory_tabu(plan, self.N, self.del_list)
        d_list = [destory_operator.destory3]
        if d <= self.destory_probability[0]:
            (destory_plan, destory_tasks) = d_list[0]()
            d_index = 0
        else:
            for i in range(1, len(self.destory_probability)):
                if self.destory_probability[i - 1] < d <= self.destory_probability[i]:
                    (destory_plan, destory_tasks) = d_list[i]()
                    d_index = i
                    break
        repair_operator = repairing(destory_plan)
        repair_operator.re_arrange()
        repair_operator.calculate_time_slack()
        r_list = [repair_operator.repair2]
        if r <= self.repair_probability[0]:
            unscheduled_tasklist = r_list[0]()
            repair_operator.Fastinsertion(unscheduled_tasklist)
            r_index = 0
        else:
            for i in range(1, len(self.repair_probability)):
                if self.repair_probability[i - 1] < r <= self.repair_probability[i]:
                    unscheduled_tasklist = r_list[i]()
                    repair_operator.Fastinsertion(unscheduled_tasklist)
                    r_index = i
                    break
        newsolution = repair_operator.plan
        insert_tasks = repair_operator.insert_tasks
        return newsolution, d_index, r_index, destory_tasks, insert_tasks


    def renew(self,tasklist):
        for i in range(len(tasklist)):
            self.del_list[tasklist[i]]=self.length
        for i in range(len(self.del_list)):
            if self.del_list[i]!=0:
                self.del_list[i]=self.del_list[i]-1

    def ts(self, i, i_unimprove, elites1, d_index_list1, r_index_list1):
        k = 0
        elites = copy.deepcopy(elites1)
        d_index_list = copy.deepcopy(d_index_list1)
        r_index_list = copy.deepcopy(r_index_list1)
        profit_seq = []
        profit_seq.append(tools.calculate_profit(self.plan))
        A_index = []
        delay_table = []
        delay_size = 40

        while i < self.Termination:
            i = i + 1
            plan = copy.deepcopy(self.plan)
            P = random.random()
            if P>0.8:
                [newsolution, d_index, r_index, destory_tasks, insert_tasks] = self.create_newsolution1(plan)
                [elites, d_index_list, r_index_list] = tools.renew(elites, d_index_list, r_index_list, newsolution,
                                                                           d_index, r_index, self.elite_sum)
            else:
                [newsolution, d_index, r_index, destory_tasks, insert_tasks] = self.create_newsolution2(plan)
                [elites, d_index_list, r_index_list] = tools.renew(elites, d_index_list, r_index_list, newsolution,
                                                                   d_index, r_index, self.elite_sum)


            f_new = tools.calculate_profit(newsolution)
            f_cur = tools.calculate_profit(self.plan)

            if f_new == datainstantiation.profit:
                self.plan = copy.deepcopy(newsolution)
                profit_seq.append(tools.calculate_profit(self.plan))
                k = 1
                break

            if f_new > f_cur:
                self.renew(insert_tasks)
                self.plan = copy.deepcopy(newsolution)
                profit_seq.append(tools.calculate_profit(self.plan))
                i_unimprove = 0
            elif f_new == f_cur:
                self.renew(insert_tasks)
                self.plan = copy.deepcopy(newsolution)
                profit_seq.append(tools.calculate_profit(self.plan))
                i_unimprove = i_unimprove + 1
                if i_unimprove == self.un_improvement:
                    break
            else:
                delay_table.append(f_new)
                if len(delay_table) > delay_size:
                    delay_table.pop(0)
                if f_new >= delay_table[-1]:
                    self.renew(insert_tasks)
                    self.plan = copy.deepcopy(newsolution)
                    profit_seq.append(tools.calculate_profit(self.plan))
                    i_unimprove = 0
                else:
                    i_unimprove = i_unimprove + 1
                    profit_seq.append(tools.calculate_profit(self.plan))


            if i_unimprove >= self.un_improvement:
                break
        for j in range(len(elites)):
            A_index.append(1)
        return i, i_unimprove, k, elites, d_index_list, r_index_list, profit_seq, A_index
