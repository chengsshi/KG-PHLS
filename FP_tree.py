class treeNode:
    def __init__(self,nameValue,numOccur,parentNode):
        self.name = nameValue  # 存放节点的名字
        self.count = numOccur  # 计数值
        self.nodeLink = None   # 用于链接相似的元素项
        self.parent = parentNode  # 指向当前节点的父节点
        self.children = {}   # 当前节点的子节点

    def inc(self,numOccur):
        """对count变量增加给定值"""
        self.count += numOccur
