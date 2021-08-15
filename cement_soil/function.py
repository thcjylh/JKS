import time
import random
import four_homes_and_six_entries as f
from decimal import Decimal
import openpyxl


def average_judge(mpa):
    aver = sum(mpa) / len(mpa)
    judge = False
    judge1 = False
    judge2 = False
    if (abs(aver - max(mpa)) / aver * 100) >= 20:
        judge1 = True
    if (abs(aver - min(mpa)) / aver * 100) >= 20:
        judge2 = True
    if judge1 is True and judge2 is True:
        judge = True
    elif judge1 is True or judge2 is True:
        mpa.remove(max(mpa))
        mpa.remove(min(mpa))
        aver = sum(mpa) / len(mpa)
        if abs(aver - max(mpa)) / aver * 100 >= 20 or abs(aver - min(mpa)) / aver * 100 >= 20:
            judge = True
    if judge is True:
        aver = -1
    else:
        aver = aver
    return aver


def generate(design):
    u = design
    sig3 = design * 18 / 100
    sig = sig3 / 3
    create = random.normalvariate(u, sig)
    return create


class CementSoil:
    def __init__(self, require_mpa):
        self.require_mpa = require_mpa
        self.require_kn = f.xy(Decimal(require_mpa) * Decimal('4998.49') * Decimal('1.15'), 10)

    def calculate(self):
        aver_group = 0
        while aver_group < self.require_kn:
            aver_group = int(generate(self.require_kn))
        wb = openpyxl.load_workbook('F:/Documents/文件/1.建科所/4.水泥土/水泥土强度公式.xlsx')
        my_sheet = wb.get_sheet_by_name('Sheet1')
        sheet1 = []
        sheet2 = []
        for i in range(4):
            for j in range(5):
                for k in range(6):
                    sheet1.append(chr(65 + i * 3) + str(int(k + 2 + j * 9)))
                    sheet2.append(chr(65 + 1 + i * 3) + str(int(k + 2 + j * 9)))
                strength_kn = []
                for m in range(6):
                    kn = '{:.0f}'.format(f.xy(generate(aver_group), 10))
                    strength_kn.append(int(kn))
                group = 0
                if average_judge(strength_kn) > 0:
                    group = f.xy(Decimal(average_judge(strength_kn)) / Decimal('4998.49'), 0.01)
                sheet3 = chr(65 + 1 + i * 3) + str(int(8 + j * 9))
                for n in range(6):
                    my_sheet[sheet1[n]] = strength_kn[n]
                    my_sheet[sheet2[n]] = f.xy(Decimal(strength_kn[n]) / Decimal('4998.49'), 0.01)
                my_sheet[sheet3] = group
                sheet1 = []
                sheet2 = []
        wb.save('F:/Documents/文件/1.建科所/4.水泥土/水泥土强度公式' + time.strftime('%Y-%m-%d %H%M%S', time.localtime()) + '.xlsx')
