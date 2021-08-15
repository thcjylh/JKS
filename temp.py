import GB8076 as gb8076
import random
import math
import openpyxl
import time

wb = openpyxl.load_workbook('D:/Downloads/Book1.xlsx')
my_sheet = wb.get_sheet_by_name('Sheet0')
start_time = [8, 30]
my_sheet['C11'] = str(start_time[0]) + ':' + str(start_time[1])
for i in range(3):
    temp=gb8076.bleeding_water(2.9,0,230,2400)  #基准泌水率，230和2400可改为自动获取
    my_sheet['F' + str(11 + i * 38)]=temp[0]
    my_sheet['I' + str(11 + i * 38)] = temp[1]
    my_sheet['O' + str(11 + i * 38)] = temp[2]
    my_sheet['S' + str(11 + i * 38)] = temp[3]
    my_sheet['W' + str(11 + i * 38)] = temp[4]










# my_sheet[ascii_str(70 + j * 14) + str(23 + i)] = item[0][i]


wb.save('D:/Downloads/1/测试' + time.strftime('%Y-%m-%d %H%M%S', time.localtime()) + '.xlsx')
