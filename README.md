# 概述
本程序提供了循迹算法的试验平台，你可以自己实现循迹算法并进行仿真。感谢秦操学长提供的三体船仿真模型。PID参数已经粗略调整，但未经实船实验。

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
你需要返回一个理想首向角，首向角范围仍然是0~2PI。


![示意图](https://github.com/PengZhenghao/Trimaran-Tracking-Algorithm-Simulation-Experiment-Platform/blob/master/example.png)
