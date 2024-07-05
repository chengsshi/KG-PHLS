import copy

from datamining import FP_growth
from construction_new_solutions import construction
from elites_sort import sort_elites


class cnbdm:
    def __init__(self, elites_set, n, min_support, newsolution_num,
                 tasknum):
        self.elites_set = copy.deepcopy(elites_set)
        self.n = n
        self.min_support = min_support
        self.newsolution_num = newsolution_num
        self.tasknum = tasknum
        self.newsolution_set = []

    def start_cnbdm(self):
        a = sort_elites(self.elites_set)
        a.sort()
        z = min(len(a.sorted_elites), self.n)
        min_length = len(a.sorted_elites[0])
        for i in range(1, z):
            if len(a.sorted_elites[i]) < min_length:
                min_length = len(a.sorted_elites[i])
        k = min_length // 10
        frequenttasks = []
        for i in range(k):
            elites = []
            for j in range(z):
                elites.append(a.sorted_elites[j][10 * i + 0:10 * i + 10])
            b = FP_growth(elites, z, self.min_support)
            chain_list = b.start_data_mining()
            if chain_list != 0:
                frequenttasks.append(chain_list)
        if frequenttasks != 0:
            s = min(len(a.sorted_elites), self.newsolution_num)
            c = construction(frequenttasks, a.sorted_elites, s, self.tasknum)
            c.new_solution()
            self.newsolution_set = c.newsolution_set
