from decimal import Decimal


def xy(num, correct_to):
    num = str(num)
    correct_to = str(correct_to)
    temp = Decimal(num) / Decimal(correct_to)
    a = Decimal(temp) // Decimal('1')
    a = int(a)
    b = Decimal(temp) % Decimal('1')
    temp = str(b)
    is_5 = False
    if b < Decimal('0.5'):
        b = 0
    elif b > Decimal('0.5'):
        b = 1
    else:
        is_5 = True
        b = 1
        for i in range(3, len(temp)):
            if temp[i] != '0':
                is_5 = False
    if is_5 is True:
        if a % 2 == 0:
            num = a
        else:
            num = a + 1
    else:
        num = a + b
    num = str(num)
    num = Decimal(num) * Decimal(correct_to)
    num = float(num)
    return num
