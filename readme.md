# Bellman-ford算法实现

## 编译环境

### 基本编译环境
|编号|名称|版本|
|---|---|---|
|1|操作系统|window 7 x64|
|2|编程语言|python 3.7.5|

### 引用库
|编号|名称|版本|作用|
|---|---|---|---|
|1|sys|default|获取int最大值|
|2|time|default|获取时间|

## 实现思路

### 数据结构
1. 均使用list作为基础数据结构。
2. 定义以下全局变量：

|编号|名称|维度|作用|
|---|---|---|---|
|1|nodeNameList|1|存储所有节点的名称，并作为下标和名称对应的记录。|
|2|allEdgesList|X|所有边列表。没有使用。|
|3|distancesList|X|未使用。|
|4|allWeightTable|2|所有路径上的cost列表。二维列表。|
|5|allNeighborFlagTable|2|所有直接邻居指示列表。横坐标和纵坐标对应的两个节点是否是直接邻居。0表示自己，1表示直接邻居，2表示非直接邻居。|
|6|outputInfoRecord|1|输出记录信息存储List。|
|7|startConfigInfo|2|所有节点最开始的配置信息。当读取config0或者changeConfig0文件是设置该列表。|
|8|nodesCount|0|存储拓扑结构中节点的总数。|
|9|edgesCount|0|存储拓扑结构中边的总数。边的个数应该满足：$m\leq\frac{n*(n-1)}{2}$|
|10|startFilePath|0|暂时没有使用。存储初始配置文件的路径。|
|11|changeFilePath|0|暂时没有使用。存储初始修改边cost文件的路径。|

3. 本实现中下标作为了隐藏参数在使用。下标通过nodeNameList与每个节点建立的对应关系。通过二维list的下标来表示节点之间的连接关系。

## 使用说明

1. 通过config0输入路由器的拓扑结构。
    - config0的格式：
        - 第一行为节点个数，假设为n。
        - 第2至n位节点名称。
        - 第n+1行为拓扑结构中各个节点之间边的个数，假设为m。
        - 边的个数应该满足：$m\leq\frac{n*(n-1)}{2}$
2. 通过changeConfig0修改边的cost。
    - changeConfig0的格式：
        - 第一行为修改边的个数，假设为n。
        - 修改边的内容。
        - 修改边的条目数量应该等于n。
3. 通过output1文件输出各个节点上的路由表。
4. 通过修改readStartFileFromFile函数和readChangeFileFromFile函数中open中的路径来修改读取的信息。后面一个版本将修改。
5. 当存在合理config0和changeConfig0文件的情况下，运行本python文件即可以运行Bellman-Ford算法。
6. config0和changeConfig0替换本文件中相应的代码就可以修改读取文件路径的位置。不限于使用config0和changeConfig0的名字。