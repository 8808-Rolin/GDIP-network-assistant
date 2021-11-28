# coding=utf-8
##############################################################
# 目标："solid", "liquid", "gas", "plasma" 四种互相转换...
# 环境： pip install transitions
# 这个库简直碉堡了...
##############################################################
from transitions import Machine


class Matter(object):
    pass


model = Matter()

# 定义状态
states = ["solid", "liquid", "gas", "plasma"]
# 定义状态转移
transitions = [
    {'trigger': 'melt', 'source': 'solid', 'dest': 'liquid'},
    {'trigger': 'evaporate', 'source': 'solid', 'dest': 'gas'},
    {'trigger': 'sublimate', 'source': 'liquid', 'dest': 'gas'},
    {'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma'},
]
# 初始化
machine = Machine(model=model, states=states, transitions=transitions, initial='solid')

print(model.state)
model.melt()
print(model.state)
