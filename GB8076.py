import random
import math
import four_homes_and_six_entries as f
import numpy
from decimal import Decimal


def bleeding_water(b, c_type, w, g):  # 泌水率
    b = random.randint(round(b * 9), round(b * 11)) / 10  # 泌水率%
    g0 = 800
    gw = 9900
    if c_type == 0:  # 基准混凝土
        g0 = random.randint(798, 812)  # 筒质量
        gw = random.randint(9900, 9910)  # 试样质量
    elif c_type == 1:  # 掺外加剂混凝土
        g0 = random.randint(1595, 1618)  # 筒质量
        gw = random.randint(9948, 9960)  # 试样质量
    w = float(w)
    g = float(g)
    vw = f.xy(Decimal(b) / (Decimal(100) / ((Decimal(w) / Decimal(g)) * Decimal(gw))), 1)
    b = f.xy(Decimal(vw) / (Decimal(w) / Decimal(g)) / Decimal(gw) * Decimal(100), 0.1)
    return g0, g0 + gw, gw, vw, b


def setting_time(s_time, h, m, c_type):  # 凝结时间计算
    s_time = random.randint(s_time - 5, s_time + 5)
    f_time = 180
    if c_type == 0:  # 基准
        f_time = 180
    elif c_type == 1:  # 外加剂（缓凝）
        f_time = 300
    elif c_type == 2:  # 外加剂（早强）
        f_time = 90
    test_strength = random.randint(2, 3) / 10  # 初次测定强度：0.2~0.3MPa
    k = (math.log(s_time) - math.log(f_time)) / (math.log(3.5) - math.log(test_strength))  # 基准斜率
    b = math.log(f_time) - k * math.log(test_strength)  # 基准截距
    x = ['0']  # 输出测定时间
    y = [0]  # 输出测量强度值
    while test_strength < 350:
        temp = int(math.e ** ((math.log(f_time) - b) / k) * 100)  # 基准曲线中当前时间下的贯入阻力
        test_strength = random.randint(temp - 10, temp + 15)  # 贯入阻力随机化
        if test_strength < 15:
            test_strength = random.randint(temp, temp + 15)  # 贯入阻力随机化
        test_strength = f.xy(test_strength, 10)  # 贯入阻力修约
        if test_strength > y[-1]:  # 判定贯入阻力是否与上次相同
            x.append(str((f_time + h * 60 + m) // 60) + ':' + '{:0>2d}'.format((f_time + h * 60 + m) % 60))
            y.append(test_strength)
            if y[-1] <= 250:  # 最后一次贯入阻力小于2.5MPa，下次测定为30min后
                f_time = f_time + 30
            elif 250 < y[-1] < 350:  # 最后一次贯入阻力在2.5~3.5MPa，下次测定为15min后
                f_time = f_time + 15
    del x[0]  # 删除第一个空值
    del y[0]  # 删除第一个空值
    return x, y


def air_content(ag):  # 含气量
    a01 = random.randint(10, 14) / 10  # 第一次骨料含气量
    a02 = random.randint(10, 14) / 10  # 第二次骨料含气量
    a0 = f.xy((Decimal(a01) + Decimal(a02)) / 2, 0.1)  # 骨料含气量
    ag = ag * 10
    ag_min = round(ag * 0.9)
    ag_max = round(ag * 1.1)
    ag = (random.randint(ag_min, ag_max) + a0 * 10) / 10  # 实测未校正含气量
    x = random.randint(0, 2) / 10  # 与平均值偏差
    ag1 = f.xy(Decimal(ag) - Decimal(x), 0.1)
    ag2 = f.xy(Decimal(ag) + Decimal(x), 0.1)
    ag = f.xy((Decimal(ag1) + Decimal(ag2)) / 2, 0.1)
    a = f.xy(Decimal(ag) - Decimal(a0), 0.1)
    return a01, a02, a0, ag1, ag2, ag, a


def shrinkage(ratio):  # 收缩率
    l0 = random.randint(3500, 3900) / 1000  # 试件长度的初始读数
    lb = 470  # 试件的测量标距
    epsilon_st_d = ratio * 10 ** -6  # 设计的收缩率
    lt = f.xy(Decimal(l0) - (Decimal(epsilon_st_d) * Decimal(lb)), 0.001)  # 测得的试件长度
    epsilon_st_t = f.xy((Decimal(l0) - Decimal(lt)) / Decimal(lb) * (Decimal(10) ** Decimal(6)), 0.1)
    return l0, lt, epsilon_st_t


def strength(s_mpa, k_type):  # 抗压强度
    if k_type == 0:
        k = Decimal(150) * Decimal(150)
    elif k_type == 1:
        k = Decimal(100) * Decimal(100) / Decimal(0.95)
    elif k_type == 2:
        k = Decimal(200) * Decimal(200) / Decimal(1.05)
    else:
        k = Decimal(150) * Decimal(150)
    k = Decimal(k) / Decimal(1000)
    f.xy(k, 0.0000001)
    s_kn = round(s_mpa * k, 1)  # 输入强度转换为力值
    s_min = int(s_kn * 0.93 * 10)  # 随机生成的最小力值
    s_max = int(s_kn * 1.07 * 10)  # 随机生成的最大力值
    kn = []  # 输出的力值
    mpa = []  # 输出的强度
    for i in range(3):  # 生成三次
        temp = f.xy(random.randint(s_min, s_max) / 10, 0.5)
        kn.append(temp)
        mpa.append(f.xy(Decimal(temp) / Decimal(k), 0.1))
    mpa_aver = f.xy(numpy.mean(mpa), 0.1)
    return kn, mpa, mpa_aver
