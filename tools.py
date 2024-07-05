import copy

import datainstantiation

E = 2400
M = 2400
m0 = 1
p0 = 1
ps = 2
pa = 1


def timeordermin(t1, t2):  # t1比t2时间要早，返回真，否则返回假  [2013, 4, 20, 12, 2, 41.04, 9.076, 45.0, 0.0]
    if t1[2] < t2[2]:
        return True
    elif t1[2] > t2[2]:
        return False
    else:
        if t1[3] * 60 * 60 + t1[4] * 60 + t1[5] < t2[3] * 60 * 60 + t2[4] * 60 + t2[5]:  # 日 相同时，比较时分秒
            return True
        else:
            return False


def Calculate_transformationtime(t1, t2):
    transformationangle = abs(t1[6] - t2[6]) + abs(t1[7] - t2[7]) + abs(t2[8] - t2[8])
    if transformationangle<=10:
        transformationtime =11.66
    elif 10<transformationangle <= 30:
        transformationtime = transformationangle / 1.5 + 5
    elif 30 < transformationangle <= 60:
        transformationtime = transformationangle / 2 + 10
    elif 60 < transformationangle <= 90:
        transformationtime = transformationangle / 2.5 + 16
    else:
        transformationtime = transformationangle / 3 + 22
    return transformationtime


def Calculate_timeinterval(t1, t2):  # 前提必须是t2比t1要晚
    m = (t2[3] * 60 * 60 + t2[4] * 60 + t2[5]) - (t1[3] * 60 * 60 + t1[4] * 60 + t1[5])
    return m


def check_transformationtime(T0, T1):
    if timeordermin(T0, T1):
        if Calculate_transformationtime(T0, T1) <= Calculate_timeinterval(T0, T1):
            return True
        else:
            return False
    else:
        return False


def generateplan(taskid_profit_seq1):  # 返回任务序列
    taskid_profit_seq=copy.deepcopy(taskid_profit_seq1)
    plan = []
    plan_item = []  # 任务序号，目标经纬度，成像收益，成像持续时间，成像开始时间，成像结束时间，以及安装在了哪一个窗口上,和每个任务历史最小转换时间
    i_temp = 0
    for i in taskid_profit_seq:  # 首先安排第一个任务
        for j in range(len(datainstantiation.tasktimewindow[i])):
            if datainstantiation.tasklists[i][4] < len(datainstantiation.Attitudeangle[i][j]) - 2:
                i_temp = 1
                plan_item.append(datainstantiation.tasklists[i][0])
                plan_item.append(datainstantiation.tasklists[i][1])
                plan_item.append(datainstantiation.tasklists[i][2])
                plan_item.append(datainstantiation.tasklists[i][3])
                plan_item.append(datainstantiation.tasklists[i][4])
                plan_item.append(datainstantiation.Attitudeangle[i][j][1])  # 开始时间 包含年 月 日 时 分 秒 滚动 俯仰 偏航
                plan_item.append(
                    datainstantiation.Attitudeangle[i][j][
                        datainstantiation.tasklists[i][4] + 1])  # 结束时间 包含年 月 日 时 分 秒 滚动 俯仰 偏航
                plan_item.append(j)
                break
        if i_temp == 1:
            plan.append(plan_item)
            plan_item = []
            break
    first_task_index = taskid_profit_seq.index(i)
    for i in range(first_task_index + 1, len(taskid_profit_seq)):
        tasktime = datainstantiation.tasklists[taskid_profit_seq[i]][4]
        TW_num = len(datainstantiation.tasktimewindow[taskid_profit_seq[i]])
        for j in range(TW_num):
            TW_length = len(datainstantiation.Attitudeangle[taskid_profit_seq[i]][j]) - 2
            if TW_length <= tasktime:
                continue
            if check_transformationtime(plan[len(plan) - 1][6],
                                        datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][
                                            1]):
                plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][0])
                plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][1])
                plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][2])
                plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][3])
                plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][4])
                plan_item.append(datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][1])
                plan_item.append(datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][1 + tasktime])  # 结束时间
                plan_item.append(j)
                plan.append(plan_item)
                plan_item = []
                break
            if check_transformationtime(plan[len(plan) - 1][6],
                                        datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][
                                            TW_length - tasktime]) and not check_transformationtime(
                    plan[len(plan) - 1][6],
                    datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][TW_length - tasktime - 1]):  # 判断最后一个时间点
                plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][0])
                plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][1])
                plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][2])
                plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][3])
                plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][4])
                plan_item.append(datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][TW_length - tasktime])  # 开始时间
                plan_item.append(datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][TW_length])  # 结束时间
                plan_item.append(j)
                plan.append(plan_item)
                plan_item = []
                break
            if not check_transformationtime(plan[len(plan) - 1][6],
                                            datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][
                                                TW_length - tasktime]):
                continue
            else:
                m_min = 2
                m_max = TW_length - tasktime - 1
                i_temp = 2
                while m_min <= m_max:
                    z = (m_min + m_max) // 2
                    if check_transformationtime(plan[len(plan) - 1][6],
                                                datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][z]):  # 这一秒符合要求
                        if check_transformationtime(plan[len(plan) - 1][6],
                                                    datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][
                                                        z - 1]):
                            m_max = z - 1
                        else:
                            i_temp = 1
                            start_monment = z
                            break
                    else:
                        if check_transformationtime(plan[len(plan) - 1][6],
                                                    datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][
                                                        z + 1]):
                            i_temp = 1
                            start_monment = z + 1
                            break
                        else:
                            m_min = z + 1
                if i_temp == 1:
                    plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][0])
                    plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][1])
                    plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][2])
                    plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][3])
                    plan_item.append(datainstantiation.tasklists[taskid_profit_seq[i]][4])
                    plan_item.append(datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][start_monment])  # 开始时间
                    plan_item.append(
                        datainstantiation.Attitudeangle[taskid_profit_seq[i]][j][start_monment + tasktime])  # 结束时间
                    plan_item.append(j)
                    plan.append(plan_item)
                    plan_item = []
                    break
    return plan


def recalculate_historical_min_conversion_time(a, b):
    a[b[0][0]] = 0
    for i in range(1, len(b)):
        if a[b[i][0]] < Calculate_transformationtime(b[i - 1][6], b[i][5]):
            a[b[i][0]] = Calculate_transformationtime(b[i - 1][6], b[i][5])
    return a


def recalculate_historical_max_profit_time(a, b):
    t = Calculate_timeinterval(b[0][5], b[1][6])
    if b[0][3] / t >= a[b[0][0]]:
        a[b[0][0]] = b[0][3] / t
    for i in range(1, len(b) - 1):
        t = Calculate_timeinterval(b[i - 1][5], b[i + 1][6])
        if b[i][3] / t >= a[b[i][0]]:
            a[b[i][0]] = b[i][3] / t
    t = Calculate_timeinterval(b[len(b) - 2][5], b[len(b) - 1][6])
    if b[len(b) - 1][3] / t >= a[b[len(b) - 1][0]]:
        a[b[len(b) - 1][0]] = b[len(b) - 1][3] / t
    return a


def calculate_latest_start_time1(index):
    for i in range(len(datainstantiation.tasktimewindow[index]) - 1, -1, -1):
        tasktime = datainstantiation.tasklists[index][4]
        TWlength = len(datainstantiation.Attitudeangle[index][i]) - 2
        if TWlength <= tasktime:
            continue
        else:
            return datainstantiation.Attitudeangle[index][i][TWlength - tasktime], \
                   datainstantiation.Attitudeangle[index][i][TWlength]


def calculate_early_start_time(index):
    for i in range(len(datainstantiation.tasktimewindow[index])):
        tasktime = datainstantiation.tasklists[index][4]
        TWlength = len(datainstantiation.Attitudeangle[index][i]) - 2
        if TWlength <= tasktime:
            continue
        else:
            return datainstantiation.Attitudeangle[index][i][1], datainstantiation.Attitudeangle[index][i][tasktime + 1], i

def check_task_arrange(end_time, index):
    TW_num = len(datainstantiation.tasktimewindow[index])
    tasktime = datainstantiation.tasklists[index][4]
    k = 0
    for i in range(TW_num):
        length = len(datainstantiation.Attitudeangle[index][i]) - 2
        if length - tasktime <= 0:
            continue
        if check_transformationtime(end_time,
                                    datainstantiation.Attitudeangle[index][i][length - tasktime]):  # 时间窗口内的最晚开始时间
            k = 1
            break
    if k == 1:
        return True
    else:
        return False


def calculate_next_starttime(end_time, index):
    tasktime = datainstantiation.tasklists[index][4]
    TW_num = len(datainstantiation.tasktimewindow[index])
    for j in range(TW_num):
        TW_length = len(datainstantiation.Attitudeangle[index][j]) - 2
        if TW_length <= tasktime:
            continue
        if not check_transformationtime(end_time,
                                        datainstantiation.Attitudeangle[index][j][TW_length - tasktime]):  # 最晚开始时间不符合要求
            continue
        if check_transformationtime(end_time, datainstantiation.Attitudeangle[index][j][1]):  # 返回最早的时间
            return datainstantiation.Attitudeangle[index][j][1], datainstantiation.Attitudeangle[index][j][
                tasktime + 1], j
        if check_transformationtime(end_time, datainstantiation.Attitudeangle[index][j][
            TW_length - tasktime]) and not check_transformationtime(end_time, datainstantiation.Attitudeangle[index][j][
            TW_length - tasktime - 1]):
            return datainstantiation.Attitudeangle[index][j][TW_length - tasktime], \
                   datainstantiation.Attitudeangle[index][j][TW_length], j
        else:
            m_min = 2
            m_max = TW_length - tasktime - 1
            while m_min <= m_max:
                z = (m_min + m_max) // 2
                if check_transformationtime(end_time, datainstantiation.Attitudeangle[index][j][z]):  # 这一秒符合要求
                    if check_transformationtime(end_time, datainstantiation.Attitudeangle[index][j][z - 1]):  # 上一秒符合要求
                        m_max = z - 1
                    else:
                        return datainstantiation.Attitudeangle[index][j][z], datainstantiation.Attitudeangle[index][j][
                            z + tasktime], j
                else:
                    if check_transformationtime(end_time, datainstantiation.Attitudeangle[index][j][z + 1]):  # 下一秒符合要求
                        return datainstantiation.Attitudeangle[index][j][z + 1], \
                               datainstantiation.Attitudeangle[index][j][z + tasktime + 1], j
                    else:
                        m_min = z + 1




def judge(plan, plan_set):
    k = 2.5
    for i in range(len(plan_set)):
        if plan==plan_set[i]:
            k = i
            break
    return k


def calculate_profit(plan):
    profit = 0
    for i in range(len(plan)):
        profit = profit + plan[i][3]
    return profit


def min_profit_index(elites):  # 返回方案中收益最小的下标
    profit = []
    for i in range(len(elites)):
        profit.append(calculate_profit(elites[i]))
    return profit.index(min(profit))


def renew(elites1, d_index_list1, r_index_list1, solution, d_index, r_index, elite_num):
    elites=copy.deepcopy(elites1)
    d_index_list=copy.deepcopy(d_index_list1)
    r_index_list=copy.deepcopy(r_index_list1)
    if len(elites) == 0:
        elites.append(solution)
        d_index_list.append(d_index)
        r_index_list.append(r_index)
    else:
        k = judge(solution, elites)
        if k == 2.5:
            if len(elites) < elite_num:
                elites.append(solution)
                d_index_list.append(d_index)
                r_index_list.append(r_index)
            else:
                index = min_profit_index(elites)
                if calculate_profit(solution) >= calculate_profit(elites[index]):
                    elites[index] = solution.copy()
                    d_index_list[index] = d_index
                    r_index_list[index] = r_index
        else:
            elites[k] = copy.deepcopy(solution)
            d_index_list[k] = d_index
            r_index_list[k] = r_index
    return elites, d_index_list, r_index_list


def calculate_last_time(index, nexttask_starttime1):
    nexttask_starttime=copy.deepcopy(nexttask_starttime1)
    tasktime = datainstantiation.tasklists[index][4]
    TW_num = len(datainstantiation.tasktimewindow[index])
    for i in range(TW_num - 1, -1, -1):
        length = len(datainstantiation.Attitudeangle[index][i]) - 2
        if length <= tasktime:
            continue
        if not check_transformationtime(datainstantiation.Attitudeangle[index][i][1 + tasktime],nexttask_starttime):  # 该窗口内的最早时间不满足
            continue
        if length > tasktime:
            if check_transformationtime(datainstantiation.Attitudeangle[index][i][length],nexttask_starttime):  # 如果最晚时间满足
                return datainstantiation.Attitudeangle[index][i][length - tasktime], datainstantiation.Attitudeangle[index][i][length]
            else:
                min_1 = 1
                max_1 = length - tasktime
                while min_1 <= max_1:
                    z = (min_1 + max_1) // 2
                    if check_transformationtime(datainstantiation.Attitudeangle[index][i][z + tasktime],nexttask_starttime):  # 这一秒符合要求
                        if check_transformationtime(datainstantiation.Attitudeangle[index][i][z + tasktime + 1],nexttask_starttime):  # 下一秒符合要求
                            min_1 = z + 1
                        else:
                            return datainstantiation.Attitudeangle[index][i][z],datainstantiation.Attitudeangle[index][i][z + tasktime]
                    else:
                        if check_transformationtime(datainstantiation.Attitudeangle[index][i][z + tasktime - 1],
                                                    nexttask_starttime):  # 上一秒符合
                            return datainstantiation.Attitudeangle[index][i][z - 1], datainstantiation.Attitudeangle[index][i][z - 1 + tasktime]
                        else:  #
                            max_1 = z - 1


def time_slack_whole_plan(plan1):
    plan=copy.deepcopy(plan1)
    time_slack_list = []
    for i in range(len(plan)):
        time_slack_list.append(i)
    time_slack_list_item = []
    for i in range(len(plan) - 1, -1, -1):
        index = plan[i][0]
        time_slack_list_item.append(index)
        if i == len(plan) - 1:
            [start_time, end_time] = calculate_latest_start_time1(index)
            time_slack_list_item.append(start_time)
            time_slack_list_item.append(end_time)
            time_slack_list[i] = time_slack_list_item.copy()
            time_slack_list_item = []
        else:
            [start_time, end_time] = calculate_last_time(plan[i][0], time_slack_list[i+1][1])
            time_slack_list_item.append(start_time)
            time_slack_list_item.append(end_time)
            time_slack_list[i] = time_slack_list_item.copy()
            time_slack_list_item = []
    return time_slack_list

def upgrade_plan(plan,position,plan_item,last_starttime_list1,last_endtime_list2):  #传入一个方案，位置，以及在该位置上插入的任务
    index=plan_item[0]
    new_plan=copy.deepcopy(plan)
    last_starttime_list=last_starttime_list1.copy()
    last_endtime_list=last_endtime_list2.copy()
    if position==len(plan):
        new_plan.insert(position,plan_item)
        last_starttime_list.insert(position,[])
        last_endtime_list.insert(position,[])
        time_slack_list=time_slack_whole_plan(new_plan)
        for i in range(len(time_slack_list)):
            last_starttime_list[i]=time_slack_list[i][1].copy()
            last_endtime_list[i]=time_slack_list[i][2].copy()
    elif position==0:
        new_plan.insert(0,plan_item)
        last_starttime_list.insert(position, [])
        last_endtime_list.insert(position, [])
        [last_starttime,last_endtime]=calculate_last_time(index,last_starttime_list[1])
        last_starttime_list[0]=last_starttime.copy()
        last_endtime_list[0]=last_endtime.copy()
        for i in range(1,len(new_plan)):
            [s_time,e_time,tw]=calculate_next_starttime(new_plan[i-1][6],new_plan[i][0])
            new_plan[i][5]=s_time.copy()
            new_plan[i][6]=e_time.copy()
            new_plan[i][7]=tw
    else:
        new_plan.insert(position, plan_item)
        last_starttime_list.insert(position, [])
        last_endtime_list.insert(position, [])
        for i in range(position,-1,-1):
            [start_time, end_time]=calculate_last_time(new_plan[i][0],last_starttime_list[i+1])
            last_starttime_list[i]=start_time.copy()
            last_endtime_list[i]=end_time.copy()
        for i in range(position,len(new_plan)):
            [s_time, e_time, tw] = calculate_next_starttime(new_plan[i - 1][6], new_plan[i][0])
            new_plan[i][5] = s_time.copy()
            new_plan[i][6] = e_time.copy()
            new_plan[i][7] = tw
    return new_plan, last_starttime_list, last_endtime_list



def judge_taskexecute(index):  # 判断任务是否可以执行
    tasktime = datainstantiation.tasklists[index][4]  # 待插入任务的执行时长
    TW_num = len(datainstantiation.tasktimewindow[index])
    k = 0
    # 首先判断这个任务能不能做，不考虑其他任务
    for i in range(TW_num):
        length = len(datainstantiation.Attitudeangle[index][i]) - 2
        if length > tasktime:
            k = 1
            break
    if k == 1:
        return True
    if k == 0:
        return False


def calculate_insert_position(plan, index, latest_starttime_list,latest_endtime_list):
    position = []
    start_time_list = []
    end_time_list = []
    TW_list = []
    difference_list = []
    for i in range(0, len(plan) + 1):
        if i == 0:
            [start_time, end_time, TW_index] = calculate_early_start_time(index)
            if check_task_arrange(end_time,plan[0][0]):
                [next_start_time, next_end_time, next_TW_index] = calculate_next_starttime(end_time, plan[0][0])
                if timeordermin(next_start_time, latest_starttime_list[0]):
                    difference = Calculate_transformationtime(end_time, next_start_time)
                    position.append(0)
                    start_time_list.append(start_time)
                    end_time_list.append(end_time)
                    TW_list.append(TW_index)
                    difference_list.append(difference)
        elif i == len(plan):
            if check_task_arrange(plan[len(plan) - 1][6], index):
                [start_time, end_time, TW_index] = calculate_next_starttime(plan[len(plan) - 1][6], index)
                difference = Calculate_transformationtime(plan[len(plan) - 1][6], start_time)
                position.append(len(plan))
                start_time_list.append(start_time)
                end_time_list.append(end_time)
                TW_list.append(TW_index)
                difference_list.append(difference)
        else:
            if check_task_arrange(plan[i - 1][6], index):
                [start_time, end_time, TW_index] = calculate_next_starttime(plan[i - 1][6], index)
                if check_task_arrange(end_time, plan[i][0]):
                    [next_start_time, next_end_time, next_TW_index] = calculate_next_starttime(end_time, plan[i][0])
                    if timeordermin(next_start_time, latest_starttime_list[i]):
                        difference = Calculate_transformationtime(plan[i - 1][6],start_time) + Calculate_transformationtime(end_time,next_start_time) - Calculate_transformationtime(plan[i - 1][6], plan[i][5])
                        position.append(i)
                        start_time_list.append(start_time)
                        end_time_list.append(end_time)
                        TW_list.append(TW_index)
                        difference_list.append(difference)
    return position, start_time_list, end_time_list, TW_list, difference_list

def check_constrain(plan):
    k=0
    for i in range(1,len(plan)):
        if check_transformationtime(plan[i-1][6],plan[i][5]):
            k=1
        else:
            k=0
            break
    if k==1:
        return True
    if k==0:
        return False

def check_trans_time(a,b): #传入两个数组，最晚开始时间和最晚结束时间
    k=0
    for i in range(len(a)-1):
        if check_transformationtime(b[i],a[i+1]):
            k=1
        else:
            k=0
            break
    if k==1:
        return True
    else:
        return False

def checktime(plan,timelist):
    k=0
    for i in range(len(plan)):
        if timeordermin(plan[i][5],timelist[i]):
            k=1
        else:
            k = 0
    if k == 1:
        return True
    else:
        return False

def calculate_profit_index(index_list):
    profit=0
    for i in index_list:
        profit=profit+datainstantiation.tasklists[i][3]
    return profit