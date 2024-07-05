from data import basicdata


a = basicdata.readin(400)
a.read()
a.task_Max_conflict()
a.Calculate_middle_Attitudeangle()
a.Calculate_average_conversion_time()


# 全局变量
tasklists = a.tasklists
tasktimewindow = a.tasktimewindow
Attitudeangle = a.Attitudeangle
task_Max_conflict_seq = a.task_Max_conflict_seq
average_conversion_time=a.average_conversion_time
middle_Attitudeangle=a.middle_Attitudeangle
profit=0

for i in tasklists:
    index=i[0]
    for j in range(len(tasktimewindow[index])):
        length=len(Attitudeangle[index][j])-2
        if length>i[4]:
            profit=profit+i[3]
            break