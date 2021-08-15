import random
import four_homes_and_six_entries as f
from decimal import Decimal

expect_strength = 50  # MPa
aver_strength = f.xy(expect_strength * random.randint(100, 105) / 100, 0.1)
force = []
strength = []
aver = 0

while aver != aver_strength:
    force = []
    strength = []
    for i in range(3):
        temp = f.xy(expect_strength * 22.5 * random.randint(90, 110) / 100,0.5)
        force.append(temp)
        strength.append(f.xy(Decimal(temp) / Decimal(22.5), 0.1))
    aver = f.xy(sum(strength) / len(strength), 0.1)
for i in range(len(force)):
    print(force[i],strength[i])
print('-------------')
print(aver)


