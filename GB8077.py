import random
from decimal import Decimal
import function as f


def hanguliang(x_d):
    m0 = random.randint(195000, 215000) / 10000

    m1 = f.xy(Decimal(m0) + Decimal(random.randint(38000, 45000) / 10000), 0.0001)
    m2 = f.xy(Decimal(x_d) / Decimal(100) * (Decimal(m1) - Decimal(m0)) + Decimal(m0), 0.0001)
    x = f.xy((Decimal(m2) - Decimal(m0)) / (Decimal(m1) - Decimal(m0)) * Decimal(100), 0.01)
    return m0, m1, m2, x


def midu(p_d):
    m0 = random.randint(308000, 321000) / 10000
    m1 = f.xy(Decimal(m0) + Decimal(50) + Decimal(random.randint(500, 13000) / 10000), 0.0001)
    m2 = f.xy(Decimal(p_d) / Decimal(0.9982) * (Decimal(m1) - Decimal(m0)) + Decimal(m0), 0.0001)
    p = f.xy((Decimal(m2) - Decimal(m0)) / (Decimal(m1) - Decimal(m0)) * Decimal(0.9982), 0.001)
    return m0, m1, m2, p


def liusuanna(naso4_d):
    m1 = random.randint(195000, 215000) / 10000
    m = 0.5
    m2 = f.xy(Decimal(naso4_d) * Decimal(m) / Decimal(60.86) + Decimal(m1), 0.0001)
    naso4 = f.xy((Decimal(m2) - Decimal(m1)) / Decimal(m) * Decimal(60.86), 0.01)
    return m1, m, m2, naso4


def zongjianliang(omega_d):
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
