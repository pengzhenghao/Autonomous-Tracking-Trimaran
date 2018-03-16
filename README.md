# 概述
本程序提供了循迹算法的试验平台，你可以自己实现循迹算法并进行仿真。感谢秦操学长提供的三体船仿真模型。
![三体船](https://github.com/PengZhenghao/Trimaran-Tracking-Algorithm-Simulation-Experiment-Platform/blob/master/trimaran.jpg)

# 环境
在使用之前，你需要安装以下支持
* Python3
* Matplotlib
* Numpy

# 使用说明
* 进入`simulator.py`可以修PID参数，以及设定轨迹点等内容，如无必要，可以不修改。
* 请确保在文件目录下新建`data`文件夹。
* 进入`decisionMaker.py`，修改其中的getDecision函数，实现你自己的循迹算法！修改完后运行`simulator.py`即可绘图。
* 在`getDecision`函数的输入为一个`Dict`，他是这样的：
```
state = {
'x': 北东系x坐标
'y': 北东系y坐标
'u': x方向速度
'v': y方向速度
'phi': 首向角，即船头与正北的夹角，范围为0~2PI
‘alpha': 首向角速度
}
```
如要取用x,y坐标，你只需要这样写：
```
x = state['x']
y = state['y']
```
decisionMaker中内置了你在`simulator.py`中预设好的一系列目标点的坐标，船在距离目标点`RAIDUS=2`米内，即被视为到达目标点。decisionMaker的构造函数中，为你提供了以下几个变量，第一个是点集，点集由simulator传入。
```
self.points = [
    [0, 0],
    [0, 50],
    [50, 50],
    [50, 0],
    [0, 0]
]
self.s = self.points[0]
self.e = self.points[1]
self.pointer = 1
```
`self.points`是一个二维list，`self.pointer`是一个数字，表示目前哪个点是目标点。`self.s`和`self.e`被初始化为(0,0)点和(0,50)点，你可以直接取出它们的值方便后续的运算：
```
x0, y0 = self.s
x1, y1 = self.e
```
记得添加一个判断条件，判断船是否到了目标点:
```
        if ((x1-x)**2 + (y1-y)**2) < RADIUS**2:
            if self.pointer == (len(self.points) - 1):
                return -1000
            self.s = self.points[self.pointer]
            self.e = self.points[self.pointer+1]
            self.pointer += 1
```
你需要返回一个理想首向角，首向角范围仍然是0~2PI。


![示意图](https://github.com/PengZhenghao/Trimaran-Tracking-Algorithm-Simulation-Experiment-Platform/blob/master/example.png)
