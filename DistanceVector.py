#!/usr/bin/python3

# author:Administrator
# contact: SystemEngineer
# datetime:2020/6/8 16:42
# software: PyCharm

"""
Document description:

"""

import sys
import time


class DistanceVectorRoutingAlgorithm:
    def __init__(self):
        self.startFilePath = ""
        self.changeFilePath = ""
        self.state = ""

        self.nodeNameList = []
        self.allEdgesList = []
        self.distancesList = []
        self.allWeightTable = []
        self.allNeighborFlagTable = []
        self.outputInfoRecord = []

        self.nodesCount = 0
        self.edgesCount = 0

    def readStartFileFromFile(self):
        """
        :param filePath:文件路径。
        :return:
        """
        # sefl.startFilePath
        with open("config0") as f:
            lines = f.readlines()

            for i in range(len(lines)):
                lines[i] = lines[i].strip("\n")

        self.nodesCount = int(lines[0])
        self.nodeNameList = lines[1:1 + int(self.nodesCount)]

        for i in range(len(self.nodeNameList)):
            self.nodeNameList[i] = self.nodeNameList[i].lower()

        self.edgesCount = int(lines[1 + int(self.nodesCount)])
        edgesList = lines[1 + int(self.nodesCount) + 1:]
        # print(nodesCount, edgesCount)
        # 定义所有节点的路由表。
        # 多维列表的初始化真是一个坑。第一种方法会导致修改一个，会改变整个列表的值。
        # allWeightTable = [[[0] * 3] * edgesCount]*nodesCount
        # allEdgesList = [[[0 for i in range(3)]for j in range(edgesCount)]for n in range(nodesCount)]
        self.allWeightTable = [[sys.maxsize for i in range(self.nodesCount)]for j in range(self.nodesCount)]
        self.allNeighborFlagTable = [[False for i in range(self.nodesCount)]for j in range(self.nodesCount)]
        # outputInfoRecord = [["" for i in range(nodesCount + 1)]for j in range(4)]
        self.outputInfoRecord = [[""] for j in range(4)]

        self.outputInfoRecord[0][0] = "#START"
        self.outputInfoRecord[1][0] = "#INITIAL"
        self.outputInfoRecord[2][0] = "#UPDATE"
        self.outputInfoRecord[3][0] = "#FINAL"

        for i in range(self.edgesCount):
            params = edgesList[i].split(" ")
            param0 = self.nodeNameList.index(params[0].lower())
            param1 = self.nodeNameList.index(params[1].lower())
            if params[2] == "inf":
                param2 = sys.maxsize
            else:
                param2 = int(params[2])
            
            self.allWeightTable[param0][param1] = param2
            self.allWeightTable[param1][param0] = param2
            self.allWeightTable[param0][param0] = 0
            self.allWeightTable[param1][param1] = 0

            self.allNeighborFlagTable[param0][param1] = True
            self.allNeighborFlagTable[param1][param0] = True
            self.allNeighborFlagTable[param0][param0] = True
            self.allNeighborFlagTable[param1][param1] = True

            self.recordOutputInfo("start", 0, param0, param1, param1, param2)


    def recordOutputInfo(self, title, step, source, destination, neighbor, distance):
        """

        :param title:
        :param step:
        :param source:
        :param destination:
        :param neighbor:
        :param distance:
        :return:
        """
        title = title.lower()
        sourceString = self.nodeNameList[source]
        destinationString = self.nodeNameList[destination]
        neighborString = self.nodeNameList[neighbor]

        if title == "start":
            self.outputInfoRecord[0].append("t=%d distance from %s to %s via %s is %d"
            %(step, sourceString, destinationString, neighborString, distance))
            # print("t=%d distance from %s to %s via %s is %d"
            # %(step, sourceString, destinationString, neighborString, distance))
            # pass
        elif title == "initial":
            self.outputInfoRecord[1].append("router %s: %s is %d routing through %s"
            %(sourceString, destinationString, distance, neighborString))
            # print("router %s: %s is %d routing through %s"
            # %(sourceString, destinationString, neighborString, neighbor))
            # pass
        elif title == "update":
            if distance != sys.maxsize:
                # 将距离为inf的改变隐藏。
                self.outputInfoRecord[2].append("t=%d distance from %s to %s via %s is %d"
                %(step, sourceString, destinationString, neighborString, distance))
            # else:
            #     outputInfoRecord[2].append("t=%d distance from %s to %s via %s is %s"
            #     %(step, sourceString, destinationString, neighborString, "inf"))
                
            # print("t=%d distance from %s to %s via %s is %d"
            # %(step, sourceString, destinationString, neighborString, distance))
            # pass
        elif title == "final":
            self.outputInfoRecord[3].append("router %s: %s is %d routing through %s"
            %(sourceString, destinationString, distance, neighborString))
            # print("router %s: %s is %d routing through %s"
            # %(sourceString, destinationString, neighborString, neighbor))
            # pass
        else:
            print(title)
            print("ERROR")


    def BellmanFord(self):
        """

        :return:
        """
        for n in range(self.nodesCount):
            # if n == 0:
            #     print("#" + "initial".upper())
            for m in range(self.nodesCount):
                # time.sleep(0.3)
                if n == m:
                    # 如果是源节点自己，那么就不用计算。自己计算下一个。
                    continue

                # 初始化一个缓存路cost的列表，用于最后的比较。
                tempDistanceList = [sys.maxsize for i in range(self.nodesCount)]
                neighborTempRecord = -1
                # 首先判断是否和需要计算的源节点是邻居。
                if self.allNeighborFlagTable[n][m] == True:
                    # 将计算的值都存入零时表中。
                    for i in range(self.nodesCount):
                        if i == m:
                            # 如果计算的是源节点和邻居自己。
                            tempDistanceList[i] = self.allWeightTable[n][i] + self.allWeightTable[m][m]
                        else:
                            # 如果计算的是源节点需要通过另外一个邻居。
                            tempDistanceList[i] = self.allWeightTable[n][i] + self.allWeightTable[i][m]
                else:
                    # 对于和源节点不是邻居的节点，计算方式不同。
                    for i in range(self.nodesCount):
                        if self.allNeighborFlagTable[n][i] == True:
                            # 对于不是邻居的节点，需要通过邻居才能连接。
                            tempDistanceList[i] = self.allWeightTable[n][i] + self.allWeightTable[i][m]
                # 计算最小值。
                # if self.allWeightTable[n][m] != min(tempDistanceList):
                #     self.recordOutputInfo("update", 0, n, m, neighborTempRecord, self.allWeightTable[n][m])
                self.allWeightTable[n][m] = min(tempDistanceList)
                # 记录邻居点。
                neighborTempRecord = tempDistanceList.index(min(tempDistanceList))
                if self.state == "start":
                    self.recordOutputInfo("start", n, n, m, neighborTempRecord, self.allWeightTable[n][m])
                    self.recordOutputInfo("initial", 0, n, m, neighborTempRecord, self.allWeightTable[n][m])
                
                if self.state == "change":
                    self.recordOutputInfo("update", n, n, m, neighborTempRecord, self.allWeightTable[n][m])
                    self.recordOutputInfo("final", 0, n, m, neighborTempRecord, self.allWeightTable[n][m])



    def recordWriteToFile(self):
        """

        :return:
        """
        with open("output1", "w") as f:
            for n in range(4):
                for m in range(len(self.outputInfoRecord[n])):
                    # print(outputInfoRecord[n][m])
                    f.write(self.outputInfoRecord[n][m] + "\n")


    def readChangeFileFromFile(self):
        # self.changeFilePath
        with open("changedConfig2") as f:
            lines = f.readlines()

            for i in range(len(lines)):
                lines[i] = lines[i].strip("\n")
        
        modifyCount = int(lines[0])
        modifyList = lines[1:]

        for i in range(modifyCount):
            params = modifyList[i].split(" ")
            # print(params)
            param0 = self.nodeNameList.index(params[0].lower())
            param1 = self.nodeNameList.index(params[1].lower())

            if params[2] == "inf":
                param2 = sys.maxsize
            else:
                param2 = int(params[2])

            # 这里只修改权重，没有新增节点或者删除节点，所以不用修改self.allNeighborFlagTable中的内容。
            self.allWeightTable[param0][param1] = param2
            self.allWeightTable[param1][param0] = param2
            self.recordOutputInfo("update", 0, param0, param1, param1, param2)
            

if __name__ == '__main__':

    dv = DistanceVectorRoutingAlgorithm()

    dv.state = "start"
    dv.startFilePath = ""
    dv.readStartFileFromFile()
    # print(dv.allWeightTable)
    # print(dv.allNeighborFlagTable)

    # 定义所有节点到其他节点的距离。
    # 实际使用时的情况如下：
    # 1. 初始化的矩阵为nodesCount*nodesCount维度。
    # 2. 自己到自己的距离初始化为0，也固定下来。
    # 3. 初始化的值都是最大int值。
    # 4. 首先初始化为当前节点和直接相连的节点的距离。
    # 5. 收到邻居节点更新的信息。
    # 6. 当前节点计算。
    # 7. 变化发出通知，没有变化不通知。
    # 
    
    dv.BellmanFord()
    # print(allWeightTable)
    # print(outputInfoRecord)

    dv.state = "change"
    dv.readChangeFileFromFile()
    dv.BellmanFord()

    # for n in range(dv.nodesCount):
    #     for i in range(dv.nodesCount):
    #         if dv.allNeighborFlagTable[n][i] == True:
    #             dv.recordOutputInfo("final", 0, n, i, i, dv.allWeightTable[n][i])

    dv.recordWriteToFile()
    print("Completed.")

