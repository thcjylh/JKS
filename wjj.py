import random
import math
import four_homes_and_six_entries as f
import numpy


def time_nj(cnsj):  # 凝结时间计算
    # cnsj = random.randint(440, 500)  # 初凝时间范围：440~500min
    test_time = 300  # 初次测定时间：180min
    test_strength = random.randrange(1, 3, 1) / 10  # 初次测定强度：0.1~0.2MPa
    k = (math.log(cnsj) - math.log(test_time)) / (math.log(3.5) - math.log(test_strength))  # 基准斜率
    b = math.log(test_time) - k * math.log(test_strength)  # 基准截距
    x = [0]  # 输出测定时间
    y = [0]  # 输出测量强度值
    while test_strength < 3.5:
        temp = int(math.e ** ((math.log(test_time) - b) / k) * 100)  # 基准曲线中当前时间下的贯入阻力
        test_strength = random.randint(temp - 15, temp + 15) / 100  # 贯入阻力随机化
        test_strength = f.xy(test_strength, 0.1)  # 贯入阻力修约
        if test_strength > y[-1]:  # 判定贯入阻力是否与上次相同
            x.append(test_time)
            y.append(test_strength)
            if y[-1] <= 2.5:  # 最后一次贯入阻力小于2.5MPa，下次测定为30min后
                test_time = test_time + 30
            elif 2.5 < y[-1] < 3.5:  # 最后一次贯入阻力在2.5~3.5MPa，下次测定为15min后
                test_time = test_time + 15
    del x[0]  # 删除第一个空值
    del y[0]  # 删除第一个空值
    #print(cnsj, test_strength, k, b)  # 输出基准曲线参数k，b
    print(x, y)  # 输出测定值
    return x, y


def strength(s_mpa):
    s_kn = round(s_mpa / 0.095, 1)  # 输入强度转换为力值
    s_min = int(s_kn * 0.9 * 10)  # 随机生成的最小力值
    s_max = int(s_kn * 1.1 * 10)  # 随机生成的最大力值
    kn = []  # 输出的力值
    mpa = []  # 输出的强度
    mpa_aver = 0
    for i in range(3):  # 生成三次
        temp = f.xy(random.randint(s_min, s_max) / 10, 0.5)
        kn.append(temp)
        mpa.append(f.xy(temp * 0.095, 0.1))
        mpa_aver = f.xy(numpy.mean(mpa), 0.1)
    return kn, mpa, mpa_aver


def bleeding_water(b):  # 泌水率
    b = random.randint(round(b*9), round(b*11)) / 10  # 泌水率%
    g0 = random.randint(798, 812)  # 筒质量
    gw = random.randint(9900, 9910) # 试样质量
    w = input('混凝土中用水量：')
    w = float(w)
    g = input('混凝土拌合物总质量：')
    g = float(g)
    vw = b / (100 / ((w / g) * gw))
    print(g0, g0 + gw, gw, f.xy(vw,1), b)


bleeding_water(3.5)
time_nj(420)
print(strength(16))
print(strength(23))
