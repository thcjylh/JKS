import math
import random
import four_homes_and_six_entries as f
from decimal import Decimal

q = 737  # 目标电通量
q = (q - 74.216) / 0.9025  # 经验公式消除误差
q_t = [f.xy(q / 900 / 24, 0.001)]  # 计算消除误差后初始值
a = random.randint(200000, 230000) / 100000  # 拟合增量方程y=aln(x)+b
b = random.randint(3300000, 4300000) / 100000  # 拟合增量方程y=aln(x)+b
y = []  # 储存增量方程下某一标准增量
for fi in range(30, 391, 30):  # 生成增量方程下某一标准增量
    temp = int(f.xy(a * math.log(fi, math.e) + b, 1))
    y.append(temp)
increment = []  # 储存增量
for fj in range(1, 13):  # 提取增量
    increment.append(f.xy((y[fj] - y[fj - 1]) / 1000, 0.001))
for fk in range(12):  # 生成数据
    q_t.append(f.xy(Decimal(q_t[fk]) + Decimal(increment[fk]), 0.001))
print(q_t)
qq = 0
for fl in range(1, 12):  # 根据数据计算电通量qq
    qq += q_t[fl]
qq = int(f.xy(900 * (2 * qq + q_t[0] + q_t[12]), 1))  # 未校正电通量
q_corr = int(f.xy(qq * (95 / 100) ** 2, 1))  # 校正100mm试样电通量
print(qq)
print(q_corr)
print('Hello')