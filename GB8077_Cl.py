import random
import math
from decimal import Decimal
import function as f


def cal(diff):
    a1 = []
    a2 = []
    a3 = []
    a4 = []
    a5 = []
    a6 = []
    a7 = []
    a8 = []
    a9 = []
    for i_f_cal in range(1, 8):
        for j_f_cal in range(1, 8):
            temp_f_cal = [i_f_cal, j_f_cal]
            a = f.xy(i_f_cal / (i_f_cal + j_f_cal), 0.1)
            if a == 0.1:
                a1.append(temp_f_cal)
            elif a == 0.2:
                a2.append(temp_f_cal)
            elif a == 0.3:
                a3.append(temp_f_cal)
            elif a == 0.4:
                a4.append(temp_f_cal)
            elif a == 0.5:
                a5.append(temp_f_cal)
            elif a == 0.6:
                a6.append(temp_f_cal)
            elif a == 0.7:
                a7.append(temp_f_cal)
            elif a == 0.8:
                a8.append(temp_f_cal)
            elif a == 0.9:
                a9.append(temp_f_cal)
    delta_1 = 0
    delta_2 = 0
    if diff == 0.01:
        n = random.randint(0, len(a1) - 1)
        delta_1 = a1[n][0]
        delta_2 = a1[n][1]
    elif diff == 0.02:
        n = random.randint(0, len(a2) - 1)
        delta_1 = a2[n][0]
        delta_2 = a2[n][1]
    elif diff == 0.03:
        n = random.randint(0, len(a3) - 1)
        delta_1 = a3[n][0]
        delta_2 = a3[n][1]
    elif diff == 0.04:
        n = random.randint(0, len(a4) - 1)
        delta_1 = a4[n][0]
        delta_2 = a4[n][1]
    elif diff == 0.05:
        n = random.randint(0, len(a5) - 1)
        delta_1 = a5[n][0]
        delta_2 = a5[n][1]
    elif diff == 0.06:
        n = random.randint(0, len(a6) - 1)
        delta_1 = a6[n][0]
        delta_2 = a6[n][1]
    elif diff == 0.07:
        n = random.randint(0, len(a7) - 1)
        delta_1 = a7[n][0]
        delta_2 = a7[n][1]
    elif diff == 0.08:
        n = random.randint(0, len(a8) - 1)
        delta_1 = a8[n][0]
        delta_2 = a8[n][1]
    elif diff == 0.09:
        n = random.randint(0, len(a9) - 1)
        delta_1 = a9[n][0]
        delta_2 = a9[n][1]
    delta = [delta_1, delta_2]
    return delta


def cl(x_cl_d):
    m = random.randint(45000, 48800) / 10000  # 外加剂样品质量（实测）
    c = 0.1  # 硝酸银溶液浓度（实测）
    v = f.xy(Decimal(x_cl_d) * Decimal(m) / Decimal(3.545) / Decimal(c), 0.01)  # 外加剂中氯离子消耗的硝酸银体积(计算)

    # 空白试验↓↓↓
    v01 = round(random.randint(970, 1030) / 100, 2)  # 10ml 0.1mol/L硝酸钠消耗硝酸银的体积
    if (v01 * 10) - math.floor(v01 * 10) == 0:
        v01 = round(v01 + 0.01, 2)  # 保证V01末尾不为0
    v02 = round(v01 + 10, 2)  # 20ml 0.1mol/L硝酸钠消耗硝酸银的体积
    v01_l = []  # 滴加硝酸银的体积（10ml）空组
    v02_l = []  # 滴加硝酸银的体积（20ml）空组
    v01_l.append((math.floor(v01 * 10) - 1) / 10)  # 滴加硝酸银的体积（10ml）初始值
    v02_l.append((math.floor(v01 * 10) - 1) / 10 + 10)  # 滴加硝酸银的体积（20ml）初始值
    for i in range(3):
        v01_l.append(round(v01_l[i] + 0.1, 1))  # 滴加硝酸银的体积（10ml）
        v02_l.append(round(v02_l[i] + 0.1, 1))  # 滴加硝酸银的体积（20ml）
    delta2_01 = [cal(round(v01 - v01_l[1], 2))[0] * 100, cal(round(v01 - v01_l[1], 2))[1] * -100]  # E/V二次偏导数（10ml）
    delta2_02 = [cal(round(v02 - v02_l[1], 2))[0] * 100, cal(round(v02 - v02_l[1], 2))[1] * -100]  # E/V二次偏导数（20ml）
    delta1_01 = [random.randint(9, 12) * 10]  # E/V一次导数（10ml）初始值
    delta1_02 = [random.randint(9, 12) * 10]  # E/V一次导数（20ml）初始值
    for j in range(2):
        delta1_01.append(delta1_01[j] + delta2_01[j] / 10)  # E/V一次导数（10ml）
        delta1_02.append(delta1_02[j] + delta2_01[j] / 10)  # E/V一次导数（20ml）
    e_01 = [random.randint(248, 269)]  # 电势（10ml）初始值
    e_02 = [random.randint(248, 269)]  # 电势（20ml）初始值
    for k in range(3):
        e_01.append(e_01[k] + delta1_01[k] / 10)  # 电势（10ml）
        e_02.append(e_02[k] + delta1_02[k] / 10)  # 电势（20ml）


    # 外加剂试验↓↓↓
    temp = round(v * random.randint(90, 110) / 100, 2)
    v1 = round(v01 + temp, 2)
    temp = round(v * random.randint(90, 110) / 100, 2)
    v2 = round(v02 + temp, 2)
    while v1 * 10 % 1 == 0 or v2 * 10 % 1 == 0:
        v1 = round(v1 - 0.01, 2)
        v2 = round(v2 + 0.01, 2)
    v1_l = []  # 滴加硝酸银的体积（10ml）空组
    v2_l = []  # 滴加硝酸银的体积（20ml）空组
    v1_l.append((math.floor(v1 * 10) - 1) / 10)  # 滴加硝酸银的体积（10ml）初始值
    v2_l.append((math.floor(v2 * 10) - 1) / 10)  # 滴加硝酸银的体积（20ml）初始值
    for i in range(3):
        v1_l.append(round(v1_l[i] + 0.1, 1))  # 滴加硝酸银的体积（10ml）
        v2_l.append(round(v2_l[i] + 0.1, 1))  # 滴加硝酸银的体积（20ml）
    delta2_1 = [cal(round(v1 - v1_l[1], 2))[0] * 100, cal(round(v1 - v1_l[1], 2))[1] * -100]  # E/V二次偏导数（10ml）
    delta2_2 = [cal(round(v2 - v2_l[1], 2))[0] * 100, cal(round(v2 - v2_l[1], 2))[1] * -100]  # E/V二次偏导数（20ml）
    delta1_1 = [random.randint(9, 12) * 10]  # E/V一次导数（10ml）初始值
    delta1_2 = [random.randint(9, 12) * 10]  # E/V一次导数（20ml）初始值
    for j in range(2):
        delta1_1.append(delta1_1[j] + delta2_1[j] / 10)  # E/V一次导数（10ml）
        delta1_2.append(delta1_2[j] + delta2_1[j] / 10)  # E/V一次导数（20ml）
    e_1 = [random.randint(248, 269)]  # 电势（10ml）初始值
    e_2 = [random.randint(248, 269)]  # 电势（20ml）初始值
    for k in range(3):
        e_1.append(e_1[k] + delta1_1[k] / 10)  # 电势（10ml）
        e_2.append(e_2[k] + delta1_2[k] / 10)  # 电势（20ml）
    vv = ((Decimal(v1) - Decimal(v01)) + (Decimal(v2) - Decimal(v02))) / 2
    x_cl = f.xy(Decimal(c) / Decimal(m) * Decimal('3.545') * Decimal(vv), 0.001)
    return v01_l, e_01, delta1_01, delta2_01, v01, v02_l, e_02, delta1_02, delta2_02, v02, v1_l, e_1, delta1_1, delta2_1, v1, v2_l, e_2, delta1_2, delta2_2, v2, c, m, vv, x_cl
