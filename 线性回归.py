# 线性回归
import numpy as np  # 快速操作结构数组的工具
import matplotlib.pyplot as plt  # 可视化绘制
from sklearn.linear_model import LinearRegression  # 线性回归
import math

# 样本数据集，第一列为x，第二列为y，在x和y之间建立回归模型
data1 = [[180, 0.2], [210, 0.3], [240, 0.4], [270, 0.67], [300, 0.7], [330, 0.9], [360, 1.2], [390, 1.5], [420, 2.2],[450,2.7],[465,3.0],[480,3.4],[495,3.7]]
data = []
for i in range(len(data1)):
    temp = []
    for j in [-1, -2]:
        temp.append(float('{:.5f}'.format(math.log(data1[i][j]))))
    data.append(temp)
# 生成X和y矩阵
dataMat = np.array(data)
X = dataMat[:, 0:1]  # 变量x
y = dataMat[:, 1]  # 变量y
# ========线性回归========
model = LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
model.fit(X, y)  # 线性回归建模
k = float('{:.3f}'.format(float(model.coef_)))  # 直线斜率
b = float('{:.3f}'.format(float(model.intercept_)))  # 直线截距
print('直线斜率:', k)
print('直线截距:', b)
initial_set_time = float(math.e ** (k * math.log(3.5) + b))  # 初凝时间
print('初凝时间：{:.0f} min'.format(initial_set_time))
print('线性回归模型:\n', model)
# 使用模型预测
predicted = model.predict(X)
# 绘制散点图 参数：x横轴 y纵轴
plt.scatter(X, y, marker='x')
plt.plot(X, predicted, c='r')
# 绘制x轴和y轴坐标
plt.xlabel("x")
plt.ylabel("y")
# 显示图形
plt.show()
