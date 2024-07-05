import copy

import tools
from construct import repairing
class construction:
    def __init__(self,freqtasks,elites,newsolution_num,tasknum):
        self.freqtasks=copy.deepcopy(freqtasks)
        self.elites=copy.deepcopy(elites)
        self.tasklist_set=[]
        self.newsolution_num=newsolution_num
        self.tasknum=tasknum
        self.newsolution_set=[]

    def data_conversion(self):
        for i in range(len(self.freqtasks[0])):
            self.tasklist_set.append(self.freqtasks[0][i])
        for i in range(1,len(self.freqtasks)):
            for j in range(len(self.freqtasks[i])):
                if self.freqtasks[i][j] not in self.tasklist_set:
                    self.tasklist_set.append(self.freqtasks[i][j])

    def new_solution(self):
        self.data_conversion()
        DM_plan=tools.generateplan(self.tasklist_set)
        scheduled_tasks=[]
        for i in range(len(DM_plan)):
            scheduled_tasks.append(DM_plan[i][0])
        for i in range(self.newsolution_num):
            unscheduled_tasks=[]
            DM_plan_temp=DM_plan.copy()
            for j in range(len(self.elites[i])):
                if self.elites[i][j][0] not in scheduled_tasks:
                    unscheduled_tasks.append(self.elites[i][j][0])
            for j in range(self.tasknum):
                if j not in scheduled_tasks and j not in unscheduled_tasks:
                    unscheduled_tasks.append(j)
            R=repairing(DM_plan_temp)
            R.calculate_time_slack()
            R.Fastinsertion(unscheduled_tasks)
            self.newsolution_set.append(R.plan)











