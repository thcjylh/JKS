import math
import random
import openpyxl
import time
import four_homes_and_six_entries as f

# 基础指标
w_c = float(input('请输入混凝土水灰比：'))  # 水灰比
cement_weight = float(input('请输入混凝土胶凝材料用量：'))  # 胶凝材料用量
sand_percent = float(input('请输入混凝土砂率：'))  # 砂率
admixture_1 = float(input('请输入混凝土掺加剂1用量：'))  # 掺加剂1用量
admixture_2 = float(input('请输入混凝土掺加剂2用量：'))  # 掺加剂2用量
addition_1 = float(input('请输入混凝土外加剂1用量：'))  # 外加剂1用量
addition_2 = float(input('请输入混凝土外加剂2用量：'))  # 外加剂2用量
liter = float(input('请输入混凝土试配量：'))  # 试配量

template_dir = 'F:/Documents/文件/2.建科所/8.配合比/配合比.xlsx'  # 表格模板路径地址

wb = openpyxl.load_workbook(template_dir)
my_sheet = wb.get_sheet_by_name('Sheet1')
liter /= 1000  # 换算

for i in range(3):
    my_sheet['B' + str(5 + i * 12)] = f.xy(float(w_c) + 0.05 * (i - 1), 0.01)
    my_sheet['B' + str(7 + i * 12)] = f.xy(float(sand_percent) + -1 * (i - 1), 1)
    my_sheet['B' + str(8 + i * 12)] = f.xy(float(admixture_1), 0.1)
    my_sheet['B' + str(9 + i * 12)] = f.xy(float(admixture_2), 0.1)
    my_sheet['B' + str(10 + i * 12)] = f.xy(float(addition_1), 0.1)
    my_sheet['B' + str(11 + i * 12)] = f.xy(float(addition_2), 0.1)
my_sheet['B18'] = cement_weight
w_c += random.randint(-5, 5) / 1000
mass_water = f.xy(cement_weight * w_c, 1)
for i in range(3):
    my_sheet['C' + str(2 + i * 12)] = f.xy(mass_water, 1)
    my_sheet['C' + str(3 + i * 12)] = f.xy(mass_water * liter, 0.01)
my_sheet['B6'] = f.xy(mass_water / (w_c - 0.05), 1)
my_sheet['B30'] = f.xy(mass_water / (w_c + 0.05), 1)
sand_percent /= 100  # 化为百分数
for i in range(3):
    # 掺加剂①用量
    mass_admixture_1 = math.floor(my_sheet['B' + str(6 + i * 12)].value * my_sheet['B' + str(8 + i * 12)].value / 100)
    my_sheet['G' + str(2 + i * 12)] = f.xy(mass_admixture_1, 1)
    my_sheet['G' + str(3 + i * 12)] = f.xy(mass_admixture_1 * liter, 0.01)
    # 掺加剂②用量
    mass_admixture_2 = math.floor(my_sheet['B' + str(6 + i * 12)].value * my_sheet['B' + str(9 + i * 12)].value / 100)
    my_sheet['H' + str(2 + i * 12)] = f.xy(mass_admixture_2, 1)
    my_sheet['H' + str(3 + i * 12)] = f.xy(mass_admixture_2 * liter, 0.01)
    # 外加剂①用量
    mass_addition_1 = f.xy(my_sheet['B' + str(6 + i * 12)].value * my_sheet['B' + str(10 + i * 12)].value / 100, 0.1)
    my_sheet['I' + str(2 + i * 12)] = f.xy(mass_addition_1, 0.1)
    my_sheet['I' + str(3 + i * 12)] = f.xy(mass_addition_1 * liter, 0.001)
    # 外加剂②用量
    mass_addition_2 = f.xy(my_sheet['B' + str(6 + i * 12)].value * my_sheet['B' + str(11 + i * 12)].value / 100, 0.1)
    my_sheet['J' + str(2 + i * 12)] = f.xy(mass_addition_2, 0.1)
    my_sheet['J' + str(3 + i * 12)] = f.xy(mass_addition_2 * liter, 0.001)
    # 水泥用量
    mass_cement = f.xy(my_sheet['B' + str(6 + i * 12)].value - mass_admixture_1 - mass_admixture_2, 1)
    my_sheet['D' + str(2 + i * 12)] = f.xy(mass_cement, 1)
    my_sheet['D' + str(3 + i * 12)] = f.xy(mass_cement * liter, 0.01)
    # 砂用量
    mass_sand = f.xy((2400 - my_sheet['B' + str(6 + i * 12)].value - mass_water - mass_addition_2) * sand_percent, 1)
    my_sheet['E' + str(2 + i * 12)] = f.xy(mass_sand, 1)
    my_sheet['E' + str(3 + i * 12)] = f.xy(mass_sand * liter, 0.01)
    # 石用量
    mass_stone = f.xy(2400 - my_sheet['B' + str(6 + i * 12)].value - mass_water - mass_addition_2 - mass_sand, 1)
    my_sheet['F' + str(2 + i * 12)] = f.xy(mass_stone, 1)
    my_sheet['F' + str(3 + i * 12)] = f.xy(mass_stone * liter, 0.01)

wb.save(template_dir[0:-5] + time.strftime('%Y-%m-%d %H%M%S', time.localtime()) + '.xlsx')
