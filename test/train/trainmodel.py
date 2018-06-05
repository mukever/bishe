

import caffe
# 训练设置
# 使用GPU
# caffe.set_device(0) # 若不设置,默认为0
# caffe.set_mode_gpu()
# 使用CPU
caffe.set_mode_cpu()
si= caffe.layers.Slice()
print(si)
# 加载Solver，有两种常用方法
# 1. 无论模型中Slover类型是什么统一设置为SGD
solver = caffe.SGDSolver('./ResNet_18_solver_gpu.prototxt')

solver.solve()