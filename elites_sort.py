import copy

import tools

class sort_elites:
    def __init__(self,elites_sum):
        self.elites_sum=copy.deepcopy(elites_sum)
        self.sorted_elites=[]
    def sort(self):
        whole_sequence=copy.deepcopy(self.elites_sum)
        profit_sequence=[]
        for i in range(len(whole_sequence)):
            profit_sequence.append(tools.calculate_profit(whole_sequence[i]))
        profit_sequence_temp=profit_sequence.copy()
        profit_sequence_temp.sort(reverse=True)
        for i in range(len(whole_sequence)):
            index=profit_sequence.index(profit_sequence_temp[i])
            profit_sequence[index]=float("inf")
            self.sorted_elites.append(whole_sequence[index])