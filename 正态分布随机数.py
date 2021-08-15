import numpy as np
import math
import random


def standard_normal_distribution():
    u = 0  # 均值μ
    sig = 1  # 标准差δ
    x = np.linspace(u - 9999 * sig, u + 9999 * sig, 9999999)
    y = np.exp(-(x - u) ** 2 / (2 * sig ** 2)) / (math.sqrt(2 * math.pi) * sig)
    return x, y


# x,y=standard_normal_distribution()
# plt.plot(x,y)
# plt.show()


aa=0.45
s = 0
for k in range(100):
    a = 0
    for i in range(10000):
        x = random.normalvariate(0, aa)
        if x > -1 and x < 1:
            a += 1
    s = s + a / i * 100
print(s / 100)

s = 0
for k in range(100):
    a = 0
    for i in range(10000):
        x = random.normalvariate(0, aa)
        if x > -2 and x < 2:
            a += 1
    s = s + a / i * 100
print(s / 100)

s = 0
for k in range(100):
    a = 0
    for i in range(10000):
        x = random.normalvariate(0, aa)
        if x > -3 and x < 3:
            a += 1
    s = s + a / i * 100
print(s / 100)
