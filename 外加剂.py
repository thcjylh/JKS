import math
from decimal import Decimal
import random
import openpyxl
import time
import four_homes_and_six_entries as f
import numpy

# 基础指标
j_lv = 27  # 目标减水率
c_l = 2.3  # 外加剂掺量
liter = 20  # 试配升数

# 匀质性指标
hg = 9.2  # 含固量
ls = 2.7  # 硫酸钠含量
md = 1.038  # 密度
zj = 2.11  # 总碱量
cl_content = 0.034  # 氯离子含量

# 拌合物指标
strength_ratio_1d = 190  # 1d抗压强度比
strength_ratio_3d = 180  # 3d抗压强度比
strength_ratio_7d = 130  # 7d抗压强度比
strength_ratio_28d = 125  # 28d抗压强度比
bleed_water_ratio = 74  # 泌水率比
st_diff = 160  # 凝结时间差
ag = 3.2  # 掺外加剂含气量
shrink = 120  # 收缩率比

template_dir = 'F:/Documents/文件/2.建科所/7.外加剂/高效减水剂.xlsx'  # 表格模板路径地址


# 引用的函数
def ascii_str(asc):  # ASCII码循环
    if asc <= 90:
        return chr(asc)
    else:
        return chr(((asc - 64) // 26) * 1 + 64) + chr((asc - 65) % 26 + 65)


def cal(diff):  # 氯离子电位计算
    a1 = [[1, 6], [1, 7]]
    a2 = [[1, 3], [1, 4], [1, 5], [2, 6], [2, 7]]
    a3 = [[1, 2], [2, 4], [2, 5], [3, 6], [3, 7]]
    a4 = [[2, 3], [3, 4], [3, 5], [4, 5], [4, 6], [4, 7], [5, 7]]
    a5 = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [5, 6], [6, 5], [6, 6], [6, 7], [7, 6], [7, 7]]
    a6 = [[3, 2], [4, 3], [5, 3], [5, 4], [6, 4], [7, 4], [7, 5]]
    a7 = [[2, 1], [4, 2], [5, 2], [6, 3], [7, 3]]
    a8 = [[3, 1], [4, 1], [5, 1], [6, 2], [7, 2]]
    a9 = [[6, 1], [7, 1]]
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


def cl(x_cl_d, sheet_name):  # 单次氯离子含量计算
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
    for a in range(3):
        v01_l.append(round(v01_l[a] + 0.1, 1))  # 滴加硝酸银的体积（10ml）
        v02_l.append(round(v02_l[a] + 0.1, 1))  # 滴加硝酸银的体积（20ml）
    for a in range(4):
        sheet_name['A' + str(4 + a)] = v01_l[a]  # 输出滴加硝酸银的体积（10ml）
    for a in range(4):
        sheet_name['M' + str(4 + a)] = v02_l[a]  # 输出滴加硝酸银的体积（20ml）
    delta_temp = cal(round(v01 - v01_l[1], 2))
    delta2_01 = [delta_temp[0] * 100, delta_temp[1] * -100]  # E/V二次偏导数（10ml）
    for a in range(2):
        sheet_name['J' + str(6 + a)] = delta2_01[a]  # 输出E/V二次偏导数（10ml）
    delta_temp = cal(round(v02 - v02_l[1], 2))
    delta2_02 = [delta_temp[0] * 100, delta_temp[1] * -100]  # E/V二次偏导数（20ml）
    for a in range(2):
        sheet_name['V' + str(6 + a)] = delta2_02[a]  # 输出E/V二次偏导数（10ml）
    delta1_01 = [random.randint(9, 12) * 10]  # E/V一次导数（10ml）初始值
    delta1_02 = [random.randint(9, 12) * 10]  # E/V一次导数（20ml）初始值
    for a in range(2):
        delta1_01.append(delta1_01[a] + delta2_01[a] / 10)  # E/V一次导数（10ml）
        delta1_02.append(delta1_02[a] + delta2_02[a] / 10)  # E/V一次导数（20ml）
    for a in range(3):
        sheet_name['G' + str(5 + a)] = delta1_01[a]  # 输出E/V一次导数（10ml）
    for a in range(3):
        sheet_name['S' + str(5 + a)] = delta1_02[a]  # 输出E/V一次导数（20ml）
    e_01 = [random.randint(248, 269)]  # 电势（10ml）初始值
    e_02 = [random.randint(248, 269)]  # 电势（20ml）初始值
    for k in range(3):
        e_01.append(e_01[k] + delta1_01[k] / 10)  # 电势（10ml）
        e_02.append(e_02[k] + delta1_02[k] / 10)  # 电势（20ml）
    for a in range(4):
        sheet_name['D' + str(4 + a)] = e_01[a]  # 输出电势（10ml）
    for a in range(4):
        sheet_name['P' + str(4 + a)] = e_02[a]  # 输出电势（20ml）

    # 外加剂试验↓↓↓
    te_mp = round(v * random.randint(90, 110) / 100, 2)
    v1 = round(v01 + te_mp, 2)
    te_mp = round(v * random.randint(90, 110) / 100, 2)
    v2 = round(v02 + te_mp, 2)
    while v1 * 10 % 1 == 0 or v2 * 10 % 1 == 0:
        v1 = round(v1 - 0.01, 2)
        v2 = round(v2 + 0.01, 2)
    v1_l = []  # 滴加硝酸银的体积（10ml）空组
    v2_l = []  # 滴加硝酸银的体积（20ml）空组
    v1_l.append((math.floor(v1 * 10) - 1) / 10)  # 滴加硝酸银的体积（10ml）初始值
    v2_l.append((math.floor(v2 * 10) - 1) / 10)  # 滴加硝酸银的体积（20ml）初始值
    for a in range(3):
        v1_l.append(round(v1_l[a] + 0.1, 1))  # 滴加硝酸银的体积（10ml）
        v2_l.append(round(v2_l[a] + 0.1, 1))  # 滴加硝酸银的体积（20ml）
    for a in range(4):
        sheet_name['A' + str(14 + a)] = v1_l[a]  # 输出滴加硝酸银的体积（10ml）
    for a in range(4):
        sheet_name['M' + str(14 + a)] = v2_l[a]  # 输出滴加硝酸银的体积（20ml）
    delta_temp = cal(round(v1 - v1_l[1], 2))
    delta2_1 = [delta_temp[0] * 100, delta_temp[1] * -100]  # E/V二次偏导数（10ml）
    for a in range(2):
        sheet_name['J' + str(16 + a)] = delta2_1[a]  # 输出E/V二次偏导数（10ml）
    delta_temp = cal(round(v2 - v2_l[1], 2))
    delta2_2 = [delta_temp[0] * 100, delta_temp[1] * -100]  # E/V二次偏导数（20ml）
    for a in range(2):
        sheet_name['V' + str(16 + a)] = delta2_2[a]  # 输出E/V二次偏导数（20ml）
    delta1_1 = [random.randint(9, 12) * 10]  # E/V一次导数（10ml）初始值
    delta1_2 = [random.randint(9, 12) * 10]  # E/V一次导数（20ml）初始值
    for a in range(2):
        delta1_1.append(delta1_1[a] + delta2_1[a] / 10)  # E/V一次导数（10ml）
        delta1_2.append(delta1_2[a] + delta2_2[a] / 10)  # E/V一次导数（20ml）
    for a in range(3):
        sheet_name['G' + str(15 + a)] = delta1_1[a]  # 输出E/V一次导数（10ml）
    for a in range(3):
        sheet_name['S' + str(15 + a)] = delta1_2[a]  # 输出E/V一次导数（20ml）
    e_1 = [random.randint(248, 269)]  # 电势（10ml）初始值
    e_2 = [random.randint(248, 269)]  # 电势（20ml）初始值
    for k in range(3):
        e_1.append(e_1[k] + delta1_1[k] / 10)  # 电势（10ml）
        e_2.append(e_2[k] + delta1_2[k] / 10)  # 电势（20ml）
    for a in range(4):
        sheet_name['D' + str(14 + a)] = e_1[a]  # 输出电势（10ml）
    for a in range(4):
        sheet_name['P' + str(14 + a)] = e_2[a]  # 输出电势（20ml）
    vv = f.xy(((Decimal(v1) - Decimal(v01)) + (Decimal(v2) - Decimal(v02))) / 2, 0.01)
    x_cl = f.xy(Decimal(c) / Decimal(m) * Decimal('3.545') * Decimal(vv), 0.001)
    sheet_name['G9'] = c
    sheet_name['E10'] = m
    sheet_name['G20'] = vv
    sheet_name['S20'] = x_cl
    sheet_name['G8'] = v01
    sheet_name['S8'] = v02
    sheet_name['G18'] = v1
    sheet_name['S18'] = v2


def bleeding_water(b_f_bw, type_f_bw, w_f_bw, g_f_bw):  # 泌水率
    b_f_bw = random.randint(round(b_f_bw * 9), round(b_f_bw * 11)) / 10  # 泌水率%
    g0 = 800  # 初始化筒质量
    gw = 9900  # 初始化试样质量
    if type_f_bw == 0:  # 基准混凝土
        g0 = random.randint(798, 812)  # 筒质量
        gw = random.randint(9900, 9910)  # 试样质量
    elif type_f_bw == 1:  # 掺外加剂混凝土
        g0 = random.randint(1595, 1618)  # 筒质量
        gw = random.randint(9948, 9960)  # 试样质量
    w_f_bw = float(w_f_bw)  # 浮点化
    g_f_bw = float(g_f_bw)  # 浮点化
    vw = f.xy(Decimal(b_f_bw) / (Decimal(100) / ((Decimal(w_f_bw) / Decimal(g_f_bw)) * Decimal(gw))), 1)
    b_f_bw = f.xy(Decimal(vw) / (Decimal(w_f_bw) / Decimal(g_f_bw)) / Decimal(gw) * Decimal(100), 0.1)
    return g0, g0 + gw, gw, vw, b_f_bw


def setting_time(s_time, h, m, c_type):  # 凝结时间计算
    s_time = random.randint(s_time - 5, s_time + 5)
    f_time = 180  # 初始化第一次测定时间
    if c_type == 0:  # 基准
        f_time = 180
    elif c_type == 1:  # 外加剂（缓凝）
        f_time = 300
    elif c_type == 2:  # 外加剂（早强）
        f_time = 90
    test_strength = random.randint(2, 3) / 10  # 初次测定强度：0.2~0.3MPa
    k_f_line = (math.log(s_time) - math.log(f_time)) / (math.log(3.5) - math.log(test_strength))  # 基准斜率
    b_f_line = math.log(f_time) - k_f_line * math.log(test_strength)  # 基准截距
    x = ['0']  # 输出测定时间
    y = [0]  # 输出测量强度值
    while test_strength < 350:
        temp = int(math.e ** ((math.log(f_time) - b_f_line) / k_f_line) * 100)  # 基准曲线中当前时间下的贯入阻力
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


def air_content(ag_f_air_c):  # 含气量
    a01 = random.randint(10, 14) / 10  # 第一次骨料含气量
    a02 = random.randint(10, 14) / 10  # 第二次骨料含气量
    a0 = f.xy((Decimal(a01) + Decimal(a02)) / 2, 0.1)  # 骨料含气量
    ag_min = round(ag_f_air_c * 9)
    ag_max = round(ag_f_air_c * 11)
    ag_f_air_c = (random.randint(ag_min, ag_max) + a0 * 10) / 10  # 实测未校正含气量
    x = random.randint(0, 12) / 100  # 与平均值偏差（0~0.16）
    ag1 = f.xy(Decimal(ag_f_air_c) - Decimal(x), 0.1)
    x = random.randint(0, 12) / 100  # 与平均值偏差（0~0.16）
    ag2 = f.xy(Decimal(ag_f_air_c) + Decimal(x), 0.1)
    ag_f_air_c = f.xy((Decimal(ag1) + Decimal(ag2)) / 2, 0.1)  # 未校正含气量
    a = f.xy(Decimal(ag_f_air_c) - Decimal(a0), 0.1)  # 校正含气量
    return a01, a02, a0, ag1, ag2, ag_f_air_c, a


def shrinkage(ratio):  # 收缩率
    l0 = random.randint(3500, 3900) / 1000  # 试件长度的初始读数
    lb = 470  # 试件的测量标距
    epsilon_st_d = ratio * 10 ** -6  # 设计的收缩率
    lt = f.xy(Decimal(l0) - (Decimal(epsilon_st_d) * Decimal(lb)), 0.001)  # 测得的试件长度
    epsilon_st_t = f.xy((Decimal(l0) - Decimal(lt)) / Decimal(lb) * (Decimal(10) ** Decimal(6)), 0.1)  # 收缩率
    return l0, lt, epsilon_st_t


def strength(s_mpa, k_type):  # 抗压强度
    if k_type == 0:  # 150mm*150mm试块
        k = Decimal(150) * Decimal(150)
    elif k_type == 1:  # 100mm*100mm试块
        k = Decimal(100) * Decimal(100) / Decimal(0.95)
    elif k_type == 2:  # 200mm*200mm试块
        k = Decimal(200) * Decimal(200) / Decimal(1.05)
    else:
        k = Decimal(150) * Decimal(150)  # 其余情况默认150mm*150mm试块
    k = Decimal(k) / Decimal(1000)  # kN转换N
    k = f.xy(k, 10 ** -10)  # 修约十位小数
    s_kn = round(s_mpa * k, 1)  # 输入强度转换为力值
    s_kn = float(s_kn)
    s_min = int(s_kn * 0.93 * 10)  # 随机生成的最小力值
    s_max = int(s_kn * 1.07 * 10)  # 随机生成的最大力值
    kn = []  # 输出的力值
    mpa = []  # 输出的强度
    for i_f_strength in range(3):  # 生成三次
        temp = f.xy(random.randint(s_min, s_max) / 10, 0.5)  # 生成力值
        kn.append(temp)
        mpa.append(f.xy(Decimal(temp) / Decimal(k), 0.1))  # 生成强度
    mpa_aver = f.xy(numpy.mean(mpa), 0.1)
    return kn, mpa, mpa_aver


def solid_content(x_d):  # 含固量
    m0 = random.randint(195000, 215000) / 10000
    m1 = f.xy(Decimal(m0) + Decimal(random.randint(38000, 45000) / 10000), 0.0001)
    m2 = f.xy(Decimal(x_d) / Decimal(100) * (Decimal(m1) - Decimal(m0)) + Decimal(m0), 0.0001)
    x = f.xy((Decimal(m2) - Decimal(m0)) / (Decimal(m1) - Decimal(m0)) * Decimal(100), 0.01)
    return m0, m1, m2, x


def density(p_d):  # 密度
    m0 = random.randint(308000, 321000) / 10000
    m1 = f.xy(Decimal(m0) + Decimal(50) + Decimal(random.randint(500, 13000) / 10000), 0.0001)
    m2 = f.xy(Decimal(p_d) / Decimal(0.9982) * (Decimal(m1) - Decimal(m0)) + Decimal(m0), 0.0001)
    p = f.xy((Decimal(m2) - Decimal(m0)) / (Decimal(m1) - Decimal(m0)) * Decimal(0.9982), 0.001)
    return m0, m1, m2, p


def sodium_sulphate_content(sodium_sulphate_d):  # 硫酸钠含量
    m1 = random.randint(195000, 215000) / 10000
    m = random.randint(4950, 5050) / 10000
    m2 = f.xy(Decimal(sodium_sulphate_d) * Decimal(m) / Decimal(60.86) + Decimal(m1), 0.0001)
    sodium_sulphate = f.xy((Decimal(m2) - Decimal(m1)) / Decimal(m) * Decimal(60.86), 0.01)
    return m1, m, m2, sodium_sulphate


def alkali_content(omega_d):  # 总碱量
    m29 = random.randint(970, 1030) / 10000
    n = 2.5
    if omega_d <= 1:
        m29 = m29 * 2
        n = 1
    elif 1 < omega_d <= 5:
        m29 = m29
        n = 2.5
    elif 5 < omega_d <= 10:
        m29 = m29 / 2
        n = 2.5
    elif omega_d > 10:
        m29 = m29 / 2
        n = 5
    m31 = f.xy(Decimal(omega_d) / Decimal(n) * Decimal(10) * Decimal(m29), 0.1)
    omega = f.xy(Decimal(m31) * Decimal(n) / Decimal(m29) / Decimal(10), 0.01)
    return m29, n, m31, omega


# 随机化

j_lv *= random.randint(95, 105) / 100  # 减水率浮动5%
hg += random.randint(-38, 38) / 100  # 含固量再现性（0.50%）
ls += random.randint(-70, 70) / 100  # 硫酸钠含量再现性（0.80%）
zj += random.randint(-13, 13) / 100  # 硫酸钠含量再现性（0.15%）
md += random.randint(-5, 5) / 100  # 密度浮动0.05
cl_content *= random.randint(90, 110) / 100  # 氯离子含量浮动10%
bleed_water_ratio *= random.randint(95, 105) / 100  # 泌水率比浮动5%
strength_ratio_7d *= random.randint(95, 105) / 100  # 7d抗压强度比浮动5%
strength_ratio_28d *= random.randint(95, 105) / 100  # 28d抗压强度比浮动5%
# shrink += random.randint(-3, 3)  # 收缩率比浮动3%

# 创建文档

wb = openpyxl.load_workbook(template_dir)

# 匀质性计算

my_sheet = wb.get_sheet_by_name('匀质性')
# 含固量计算
repeat_do = f.xy(random.randint(-25, 25) / 100 / 2, 0.01)  # 含固量重复性（0.30%）
average = []
for i in range(2):
    hg += repeat_do
    item = solid_content(hg)
    average.append(item[3])
    for j in range(4):
        my_sheet[ascii_str(67 + i) + str(6 + j)] = item[j]
average_hg = f.xy(sum(average) / len(average), 0.01)  # 含固量平均值
my_sheet['E9'] = average_hg
# 硫酸钠含量计算
repeat_do = f.xy(random.randint(-40, 40) / 100 / 2, 0.01)  # 硫酸钠含量重复性（0.50%）
average = []
for i in range(2):
    ls += repeat_do
    item = sodium_sulphate_content(ls)
    average.append(item[3])
    for j in range(4):
        my_sheet[ascii_str(67 + i) + str(14 + j)] = item[j]
my_sheet['E17'] = f.xy(sum(average) / len(average), 0.01)  # 硫酸钠含量平均值
# 密度计算，密度重复性0.001g/cm3
average = []
for i in range(2):
    item = density(md)
    average.append(item[3])
    for j in range(4):
        my_sheet[ascii_str(67 + i) + str(18 + j)] = item[j]
my_sheet['E21'] = f.xy(sum(average) / len(average), 0.001)  # 密度平均值
# 总碱量计算
repeat_do = f.xy(random.randint(-8, 8) / 100 / 2, 0.01)  # 总碱量重复性（0.10%）
average = []
for i in range(2):
    zj += repeat_do
    item = alkali_content(zj)
    average.append(item[3])
    my_sheet[ascii_str(67 + i) + '29'] = item[0]
    my_sheet[ascii_str(67 + i) + '30'] = item[1]
    my_sheet[ascii_str(67 + i) + '33'] = item[2]
    my_sheet[ascii_str(67 + i) + '36'] = item[3]
my_sheet['E36'] = f.xy(sum(average) / len(average), 0.01)  # 总碱量平均值

# 外加剂试验配合比计算

my_sheet0 = wb.get_sheet_by_name('Sheet0')
my_sheet0['AX1'] = '减水剂'
dosage_addition = f.xy(my_sheet0['J2'].value * c_l / 100, 0.01)  # 外加剂添加量
my_sheet0['AX2'] = dosage_addition
dosage_water = f.xy((230 * (1 - j_lv / 100)) - dosage_addition * (1 - average_hg / 100), 1)  # 掺减水剂后水量
my_sheet0['AH2'] = dosage_water
my_sheet0['G3'] = f.xy(my_sheet0['G2'].value * liter / 1000, 0.01)
my_sheet0['J3'] = f.xy(my_sheet0['J2'].value * liter / 1000, 0.01)
my_sheet0['M3'] = f.xy(my_sheet0['M2'].value * liter / 1000, 0.01)
my_sheet0['P3'] = f.xy(my_sheet0['P2'].value * liter / 1000, 0.01)
my_sheet0['S3'] = f.xy(my_sheet0['S2'].value * liter / 1000, 0.01)
my_sheet0['AH3'] = f.xy(my_sheet0['AH2'].value * liter / 1000, 0.01)
my_sheet0['AX3'] = f.xy(my_sheet0['AX2'].value * liter / 1000, 0.001)
g = dosage_water + dosage_addition + 2170  # 所有的质量
w = (dosage_water + dosage_addition * (1 - average_hg / 100)) * 2360 / g  # 水的总量
my_sheet0['AO148'] = f.xy(w, 1)
my_sheet0['AZ148'] = f.xy((230 - w) / 230 * 100, 1)  # 减水率计算

# 氯离子含量计算

my_sheet_cl = wb.get_sheet_by_name('氯离子')
cl(cl_content, my_sheet_cl)  # 外加剂中氯离子含量

# 外加剂拌合物性能计算

my_sheet1 = wb.get_sheet_by_name('Sheet1')
# 基准
b = 3.4  # 基准泌水率
st = 390  # 基准凝结时间
compressive_strength_1d = 5  # 基准1d抗压强度
compressive_strength_3d = 10  # 基准3d抗压强度
compressive_strength_7d = 19  # 基准7d抗压强度
compressive_strength_28d = 26  # 基准28d抗压强度
for j in range(3):
    item = bleeding_water(b, 0, 230, 2400)
    for i in range(5):  # 泌水率
        my_sheet1[ascii_str(67 + 14 * j + i * 2) + '5'] = item[i]
    item = setting_time(random.randint(st - 15, st + 15), 8 + j, 30, 0)
    for i in range(len(item[0])):  # 凝结时间
        my_sheet1[ascii_str(65 + j * 14) + str(8 + i)] = item[0][i]
        my_sheet1[ascii_str(67 + j * 14) + str(8 + i)] = item[1][i]
    item = strength(compressive_strength_1d, 1)
    for i in range(3):  # 1天抗压强度
        my_sheet1[ascii_str(70 + j * 14) + str(8 + i)] = item[0][i]
        my_sheet1[ascii_str(72 + j * 14) + str(8 + i)] = item[1][i]
        my_sheet1[ascii_str(74 + j * 14) + '8'] = item[2]
    item = strength(compressive_strength_3d, 1)
    for i in range(3):  # 3天抗压强度
        my_sheet1[ascii_str(70 + j * 14) + str(13 + i)] = item[0][i]
        my_sheet1[ascii_str(72 + j * 14) + str(13 + i)] = item[1][i]
        my_sheet1[ascii_str(74 + j * 14) + '13'] = item[2]
    item = strength(compressive_strength_7d, 1)
    for i in range(3):  # 7天抗压强度
        my_sheet1[ascii_str(70 + j * 14) + str(18 + i)] = item[0][i]
        my_sheet1[ascii_str(72 + j * 14) + str(18 + i)] = item[1][i]
        my_sheet1[ascii_str(74 + j * 14) + '18'] = item[2]
    item = strength(compressive_strength_28d, 1)
    for i in range(3):  # 28天抗压强度
        my_sheet1[ascii_str(70 + j * 14) + str(23 + i)] = item[0][i]
        my_sheet1[ascii_str(72 + j * 14) + str(23 + i)] = item[1][i]
        my_sheet1[ascii_str(74 + j * 14) + '23'] = item[2]
# 掺外加剂
b *= bleed_water_ratio / 100  # 掺外加剂泌水率比
st += st_diff  # 掺外加剂凝结时间
compressive_strength_1d *= strength_ratio_1d / 100  # 掺外加剂1d抗压强度
compressive_strength_3d *= strength_ratio_3d / 100  # 掺外加剂3d抗压强度
compressive_strength_7d *= strength_ratio_7d / 100  # 掺外加剂7d抗压强度
compressive_strength_28d *= strength_ratio_28d / 100  # 掺外加剂28d抗压强度
for j in range(3):
    item = bleeding_water(b, 1, w, g)
    for i in range(5):  # 泌水率
        my_sheet1[ascii_str(67 + 14 * j + i * 2) + '31'] = item[i]
    item = setting_time(random.randint(st - 15, st + 15), 9 + j, 00, 1)
    for i in range(len(item[0])):  # 凝结时间
        my_sheet1[ascii_str(65 + j * 14) + str(34 + i)] = item[0][i]
        my_sheet1[ascii_str(67 + j * 14) + str(34 + i)] = item[1][i]
    item = strength(compressive_strength_1d, 1)
    for i in range(3):  # 1天抗压强度
        my_sheet1[ascii_str(70 + j * 14) + str(34 + i)] = item[0][i]
        my_sheet1[ascii_str(72 + j * 14) + str(34 + i)] = item[1][i]
        my_sheet1[ascii_str(74 + j * 14) + '34'] = item[2]
    item = strength(compressive_strength_3d, 1)
    for i in range(3):  # 3天抗压强度
        my_sheet1[ascii_str(70 + j * 14) + str(39 + i)] = item[0][i]
        my_sheet1[ascii_str(72 + j * 14) + str(39 + i)] = item[1][i]
        my_sheet1[ascii_str(74 + j * 14) + '39'] = item[2]
    item = strength(compressive_strength_7d, 1)
    for i in range(3):  # 7天抗压强度
        my_sheet1[ascii_str(70 + j * 14) + str(44 + i)] = item[0][i]
        my_sheet1[ascii_str(72 + j * 14) + str(44 + i)] = item[1][i]
        my_sheet1[ascii_str(74 + j * 14) + '44'] = item[2]
    item = strength(compressive_strength_28d, 1)
    for i in range(3):  # 28天抗压强度
        my_sheet1[ascii_str(70 + j * 14) + str(49 + i)] = item[0][i]
        my_sheet1[ascii_str(72 + j * 14) + str(49 + i)] = item[1][i]
        my_sheet1[ascii_str(74 + j * 14) + '49'] = item[2]
    item = air_content(ag)
    my_sheet1[ascii_str(65 + j * 14) + str(49)] = item[0]
    my_sheet1[ascii_str(66 + j * 14) + str(49)] = item[1]
    my_sheet1[ascii_str(67 + j * 14) + str(49)] = item[2]
    my_sheet1[ascii_str(65 + j * 14) + str(51)] = item[3]
    my_sheet1[ascii_str(66 + j * 14) + str(51)] = item[4]
    my_sheet1[ascii_str(67 + j * 14) + str(51)] = item[5]
    my_sheet1[ascii_str(68 + j * 14) + str(49)] = item[6]

# 收缩率计算

for j in range(3):  # 收缩率
    item = shrinkage(random.randint(450, 465))  # 基准收缩率
    my_sheet1['BC' + str(8 + j * 5)] = item[0]
    my_sheet1['BF' + str(8 + j * 5)] = item[1]
    my_sheet1['AT' + str(10 + j * 5)] = item[2]
    l_std = item[2]
    item = shrinkage(l_std * shrink * random.randint(98, 102) / 10000)  # 掺外加剂收缩率
    my_sheet1['BC' + str(34 + j * 5)] = item[0]
    my_sheet1['BF' + str(34 + j * 5)] = item[1]
    my_sheet1['AT' + str(36 + j * 5)] = item[2]
    l_28 = item[2]
    my_sheet1['BI' + str(10 + j * 5)] = f.xy(Decimal(l_28) / Decimal(l_std) * Decimal(100), 1)  # 单次收缩率比

# 基准强度平均值
for i in range(4):
    sum_cal = 0
    len_cal = 0
    for j in range(3):
        sum_cal += my_sheet1[ascii_str(ord('J') + j * 14) + str(8 + i * 5)].value
        len_cal += 1
    average_cal = f.xy(sum_cal / len_cal, 0.1)
    my_sheet1['AN' + str(10 + i * 5)] = average_cal

# 掺外加剂强度平均值
for i in range(4):
    sum_cal = 0
    len_cal = 0
    for j in range(3):
        sum_cal += my_sheet1[ascii_str(ord('J') + j * 14) + str(34 + i * 5)].value
        len_cal += 1
    average_cal = f.xy(sum_cal / len_cal, 0.1)
    my_sheet1['AN' + str(36 + i * 5)] = average_cal

# 抗压强度比计算
for i in range(4):
    strength_ratio = f.xy(my_sheet1['AN' + str(36 + i * 5)].value / my_sheet1['AN' + str(10 + i * 5)].value * 100, 1)
    my_sheet1['AN' + str(37 + i * 5)] = strength_ratio

# 收缩率比平均值
sum_cal = 0
len_cal = 0
for i in range(3):
    sum_cal += my_sheet1['BI' + str(10 + i * 5)].value
    len_cal += 1
average_cal = f.xy(sum_cal / len_cal, 1)
my_sheet1['BI23'] = average_cal

# 基准与掺外加剂泌水率平均值
for i in range(2):
    sum_cal = 0
    len_cal = 0
    for j in range(3):
        sum_cal += my_sheet1[ascii_str(ord('K') + j * 14) + str(5 + i * 26)].value
        len_cal += 1
    average_cal = f.xy(sum_cal / len_cal, 0.1)
    my_sheet1['AN' + str(7 + i * 26)] = average_cal

# 泌水率比计算
my_sheet1['AN34'] = f.xy(my_sheet1['AN33'].value / my_sheet1['AN7'].value * 100, 1)

# 含气量平均值
sum_cal = 0
len_cal = 0
for i in range(3):
    sum_cal += my_sheet1[ascii_str(ord('D') + i * 14) + '49'].value
    len_cal += 1
average_cal = f.xy(sum_cal / len_cal, 0.1)
my_sheet1['AF54'] = average_cal

# 减水率计算


# 文档保存

wb.save(template_dir[0:-5] + time.strftime('%Y-%m-%d %H%M%S', time.localtime()) + '.xlsx')
